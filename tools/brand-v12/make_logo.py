#!/usr/bin/env python3
"""
make_logo.py - generator for the V12 "馬蓋先 MacGyver Engineering Academy" logo.

One source of truth: the keyframe TRACKS defined in `tracks()` drive
  * the CSS-animated vector  (logo-animated.svg, no scripts), and
  * every raster frame       (rendered by headless Chromium at 4x, then
                              box-downsampled in premultiplied alpha).

Outputs go to public/academy/assets/brand/ (see README.md there).

Usage (from the project root):
    python3 tools/brand-v12/make_logo.py            # build everything
    python3 tools/brand-v12/make_logo.py --frames DIR   # also dump RGBA review frames into DIR

Needs: Python 3, Pillow, numpy, playwright (+ chromium), ImageMagick `convert`.
"""
from __future__ import annotations

import argparse
import math
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / "public" / "academy" / "assets" / "brand"

# ----------------------------------------------------------------- palette --
DEEP = "#153c35"     # deep green
GREEN = "#4b755a"    # green
SAGE = "#739578"     # sage
CREAM = "#f5f1e6"    # cream
MIST = "#edf2e5"     # light cream-green
GOLD = "#d7bd75"     # gold accent
ORANGE = "#c8643b"   # warm accent (used sparingly: spark core, tail lamp)
NIGHT = "#111b20"    # dark UI background

LIGHT_MATTE = "#f8f6ef"   # edge matte for the light GIFs (between cream and #fcfcf9 sidebar)
DARK_MATTE = "#15222a"    # edge matte for the dark GIF (between #111b20 page and #19282f sidebar)

# --------------------------------------------------------------- timeline --
FRAMES = 48                      # 48 frames ...
DELAYS_CS = [7, 7, 6] * 16       # ... = 320 cs = 3.2 s loop (~15 fps)
LOOP_S = sum(DELAYS_CS) / 100.0
SS = 4                           # supersampling factor

EASE = {
    "lin": (0.0, 0.0, 1.0, 1.0),
    "io": (0.42, 0.0, 0.58, 1.0),     # ease-in-out
    "in": (0.32, 0.0, 0.67, 0.0),     # ease-in (cubic)
    "out": (0.33, 1.0, 0.68, 1.0),    # ease-out (cubic)
    "arrive": (0.22, 0.75, 0.36, 1.0),  # fast entry, long soft stop
}


def bezier(p: float, x1: float, y1: float, x2: float, y2: float) -> float:
    """CSS cubic-bezier() timing function, evaluated exactly like browsers do."""
    if (x1, y1, x2, y2) == (0.0, 0.0, 1.0, 1.0):
        return p
    lo, hi = 0.0, 1.0
    for _ in range(60):
        u = (lo + hi) / 2
        x = 3 * (1 - u) ** 2 * u * x1 + 3 * (1 - u) * u ** 2 * x2 + u ** 3
        if x < p:
            lo = u
        else:
            hi = u
    u = (lo + hi) / 2
    return 3 * (1 - u) ** 2 * u * y1 + 3 * (1 - u) * u ** 2 * y2 + u ** 3


def num(v: float) -> str:
    s = f"{v:.3f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


class Track:
    """A keyframed transform on one <g>. keys: [(frame, value, ease_to_next)]."""

    def __init__(self, kind: str, keys: list, rest=None):
        self.kind = kind
        self.keys = sorted(keys, key=lambda k: k[0])
        self.rest = rest if rest is not None else self.value(0)

    def value(self, f: float):
        ks = self.keys
        if f <= ks[0][0]:
            return ks[0][1]
        for (f0, v0, e), (f1, v1, _) in zip(ks, ks[1:]):
            if f0 <= f < f1:
                p = bezier((f - f0) / (f1 - f0), *EASE[e or "lin"])
                if isinstance(v0, tuple):
                    return tuple(a + (b - a) * p for a, b in zip(v0, v1))
                return v0 + (v1 - v0) * p
        return ks[-1][1]

    def fmt(self, v, css: bool) -> str:
        px, dg = ("px", "deg") if css else ("", "")
        k = self.kind
        if k == "tx":
            return f"translate({num(v)}{px},0{px})"
        if k == "ty":
            return f"translate(0{px},{num(v)}{px})"
        if k == "txy":
            return f"translate({num(v[0])}{px},{num(v[1])}{px})"
        if k == "rot":
            return f"rotate({num(v)}{dg})"
        if k == "sx":
            return f"scale({num(v)},1)"
        if k == "sy":
            return f"scale(1,{num(v)})"
        if k == "s":
            return f"scale({num(v)})"
        if k == "ts":
            return f"translate({num(v[0])}{px},0{px}) scale({num(v[1])})"
        raise ValueError(k)

    def is_identity(self, v) -> bool:
        k = self.kind
        if k in ("tx", "ty", "rot"):
            return abs(v) < 1e-4
        if k in ("sx", "sy", "s"):
            return abs(v - 1) < 1e-4
        if k == "txy":
            return abs(v[0]) < 1e-4 and abs(v[1]) < 1e-4
        return False

    def css_keyframes(self, name: str) -> str:
        ks = list(self.keys)
        if ks[0][0] > 0:
            ks.insert(0, (0, ks[0][1], "lin"))
        if ks[-1][0] < FRAMES:
            ks.append((FRAMES, ks[-1][1], None))
        rows = []
        for f, v, e in ks:
            pct = num(f / FRAMES * 100)
            tf = ""
            if f < FRAMES and (e or "lin") != "lin":
                tf = ";animation-timing-function:cubic-bezier({},{},{},{})".format(*map(num, EASE[e]))
            rows.append(f"{pct}%{{transform:{self.fmt(v, True)}{tf}}}")
        return f"@keyframes {name}{{{''.join(rows)}}}"


def tracks(travel: float, wheel_r: float) -> dict[str, Track]:
    """All motion of the loop, in frames (0..48).  `travel` is the rover's
    off-screen distance in rover-local units for the current layout."""
    A = travel / wheel_r * 180 / math.pi          # wheel spin for that distance
    over = -0.025                                 # tiny overshoot on arrival
    T = {
        # rover drives off (after turning round) and rolls back in from the right
        "rvx": Track("tx", [(0, 0, "lin"), (31, 0, "in"), (36, travel, "lin"), (37, travel, "arrive"),
                            (43, over * travel, "io"), (45, 0, "lin"), (48, 0, None)]),
        "wheel": Track("rot", [(0, 0, "lin"), (31, 0, "in"), (36, -A, "lin"), (36.5, -A, "lin"),
                               (36.501, A, "lin"), (37, A, "arrive"), (43, over * A, "io"),
                               (45, 0, "lin"), (48, 0, None)]),
        "flip": Track("sx", [(0, 1, "lin"), (29, 1, "io"), (32, -1, "lin"), (36.5, -1, "lin"),
                             (36.501, 1, "lin"), (48, 1, None)]),
        "hop": Track("ty", [(0, 0, "lin"), (29, 0, "out"), (30.5, -9, "in"), (32, 0, "lin"), (48, 0, None)]),
        "tilt": Track("rot", [(0, 0, "lin"), (31, 0, "out"), (33, 4, "io"), (36, 1.5, "lin"), (37, 0, "lin"),
                              (40, 1.2, "io"), (43, -6, "io"), (44.5, 2.5, "io"), (46, -1, "io"),
                              (47.5, 0, "lin"), (48, 0, None)]),
        "antenna": Track("rot", [(0, 0, "lin"), (29, 0, "io"), (30.5, -8, "io"), (32, 6, "io"),
                                 (33.5, 13, "io"), (36, 8, "lin"), (37, -4, "lin"), (42, -7, "out"),
                                 (43.3, -16, "io"), (44.6, 10, "io"), (45.8, -5, "io"),
                                 (46.9, 2.5, "io"), (48, 0, None)]),
        "gear": Track("rot", [(0, 0, "lin"), (48, 180, None)]),
        "blink": Track("sy", [(0, 1, "lin"), (1, 1, "in"), (3, 0.1, "out"), (5, 1, "lin"),
                              (24, 1, "in"), (25, 0.12, "out"), (26, 1, "in"), (27, 0.12, "out"),
                              (28, 1, "lin"), (48, 1, None)]),
        "look": Track("txy", [(0, (0.0, 0.0), "lin"), (5, (0.0, 0.0), "io"), (8, (-0.8, -1.6), "lin"),
                              (20, (-0.8, -1.6), "io"), (23, (0.0, 0.0), "lin"), (48, (0.0, 0.0), None)]),
        # the wrench turns a quarter turn (clockwise) and snaps back into the "M"
        "wrench": Track("rot", [(0, 0, "lin"), (6, 0, "io"), (13, 90, "lin"), (15, 90, "in"),
                                (18, -8, "io"), (20, 3, "io"), (22, 0, "lin"), (48, 0, None)]),
        "spark": Track("s", [(0, 1, "lin"), (17, 1, "out"), (19, 1.75, "io"), (22, 0.8, "io"),
                             (25, 1.1, "io"), (27, 1, "lin"), (48, 1, None)]),
        "sparkrot": Track("rot", [(0, 0, "lin"), (17, 0, "out"), (27, 90, "lin"), (48, 90, None)], rest=0),
        "burst": Track("ts", [(0, (8.0, 0.0), "lin"), (18, (8.0, 0.0), "lin"), (18.01, (9.0, 1.0), "out"),
                              (24, (24.0, 0.0), "lin"), (48, (24.0, 0.0), None)], rest=(8.0, 0.0)),
        "speed": Track("s", [(0, 0, "lin"), (31, 0, "out"), (33, 1, "lin"), (37, 1, "lin"),
                             (40, 1, "io"), (42.5, 0, "lin"), (48, 0, None)], rest=0),
    }
    return T


# ------------------------------------------------------------------ drawing --
class Ctx:
    """Emits animated groups either as static transforms (frame f) or CSS classes."""

    def __init__(self, T: dict[str, Track], frame: float | None, prefix: str = "mg"):
        self.T, self.f, self.prefix = T, frame, prefix
        self.used: set[str] = set()

    def g(self, name: str, inner: str) -> str:
        tr = self.T[name]
        if self.f is None:                                   # animated vector
            self.used.add(name)
            rest = tr.rest
            attr = "" if tr.is_identity(rest) else f' transform="{tr.fmt(rest, False)}"'
            return f'<g class="{self.prefix}-a {self.prefix}-{name}"{attr}>{inner}</g>'
        v = tr.value(self.f)
        if (tr.kind == "s" and abs(v) < 1e-4) or (tr.kind == "ts" and abs(v[1]) < 1e-4):
            return ""                                        # scaled to nothing: omit
        if tr.is_identity(v):
            return inner
        return f'<g transform="{tr.fmt(v, False)}">{inner}</g>'

    def css(self) -> str:
        p = self.prefix
        out = [f".{p}-a{{transform-box:view-box;transform-origin:0 0;"
               f"animation:{LOOP_S:g}s linear infinite both}}"]
        for n in sorted(self.used):
            out.append(f".{p}-{n}{{animation-name:{p}-{n}}}")
            out.append(self.T[n].css_keyframes(f"{p}-{n}"))
        out.append(f"@media (prefers-reduced-motion:reduce){{.{p}-a{{animation:none}}}}")
        return "".join(out)


def star(r: float, k: float = 0.16) -> str:
    """4-point sparkle with concave sides."""
    c = r * k
    return (f"M0 {num(-r)}Q{num(c)} {num(-c)} {num(r)} 0Q{num(c)} {num(c)} 0 {num(r)}"
            f"Q{num(-c)} {num(c)} {num(-r)} 0Q{num(-c)} {num(-c)} 0 {num(-r)}Z")


def rrect(x0, y0, x1, y1, tl, tr, br, bl) -> str:
    return (f"M{num(x0 + tl)} {num(y0)}H{num(x1 - tr)}"
            f"{'A%s %s 0 0 1 %s %s' % (num(tr), num(tr), num(x1), num(y0 + tr)) if tr else ''}"
            f"V{num(y1 - br)}"
            f"{'A%s %s 0 0 1 %s %s' % (num(br), num(br), num(x1 - br), num(y1)) if br else ''}"
            f"H{num(x0 + bl)}"
            f"{'A%s %s 0 0 1 %s %s' % (num(bl), num(bl), num(x0), num(y1 - bl)) if bl else ''}"
            f"V{num(y0 + tl)}"
            f"{'A%s %s 0 0 1 %s %s' % (num(tl), num(tl), num(x0 + tl), num(y0)) if tl else ''}Z")


def gear_path(teeth: int, r_out: float, r_in: float, tw: float = 0.5) -> str:
    """Gear outline with trapezoid teeth. tw = tooth share of the pitch."""
    pts = []
    step = 2 * math.pi / teeth
    for i in range(teeth):
        a = i * step - math.pi / 2
        half_root = step * tw * 0.62
        half_tip = step * tw * 0.36
        for ang, r in ((a - half_root, r_in), (a - half_tip, r_out), (a + half_tip, r_out), (a + half_root, r_in)):
            pts.append((r * math.cos(ang), r * math.sin(ang)))
    d = "M" + "L".join(f"{num(x)} {num(y)}" for x, y in pts) + "Z"
    return d


def wrench_head_path(r: float = 16.0, h: float = 5.6, c: float = -3.0) -> str:
    """Open-end wrench head: circle of radius r with a U-slot (half width h)
    whose round bottom is centred at y=c. Slot opens towards -y."""
    yt = -math.sqrt(r * r - h * h)
    return (f"M{num(h)} {num(yt)}A{num(r)} {num(r)} 0 1 1 {num(-h)} {num(yt)}"
            f"L{num(-h)} {num(c)}A{num(h)} {num(h)} 0 0 0 {num(h)} {num(c)}Z")


# Badge geometry lives in a 200-unit box centred on 0,0 (outer radius 100).
WRENCH_X, WRENCH_Y = -36.0, 2.0
BLADE_X = 39.0
V_PTS = ((-27, -19), (1.5, 14), (36, -26))
SPARK_POS = (0.0, -62.0)


def badge(cx: Ctx, outline: str = CREAM, simple: bool = False) -> str:
    """Circular academy badge with the tool-built "M".  simple=True drops the
    hairline details (rivets, holes, particles) and thickens strokes for favicons."""
    s = []
    s.append(f'<circle r="100" fill="{outline}"/>')
    s.append(f'<circle r="{94.5 if simple else 93.5}" fill="{DEEP}"/>')
    s.append(f'<circle r="{85 if simple else 84}" fill="none" stroke="{GOLD}" stroke-width="{5 if simple else 3.6}"/>')
    m = []
    # 'V' of the M: two arms meeting at a pivot (a folding-tool linkage)
    (x0, y0), (x1, y1), (x2, y2) = V_PTS
    m.append(f'<path d="M{x0} {y0}L{x1} {y1}L{x2} {y2}" fill="none" stroke="{CREAM}" '
             f'stroke-width="{17 if simple else 15.5}" stroke-linejoin="miter" stroke-miterlimit="3" '
             f'stroke-linecap="round"/>')
    if not simple:
        m.append(f'<circle cx="{x1}" cy="{y1 + 1}" r="3.4" fill="{DEEP}"/>')
    # right stem: multitool blade folding out of its handle
    bx = BLADE_X
    m.append(f'<path d="M{num(bx - 7.5)} -3.5H{num(bx + 7.5)}V40.5A7.5 7.5 0 0 1 {num(bx - 7.5)} 40.5Z" fill="{CREAM}"/>')
    m.append(f'<path d="M{num(bx - 7.5)} {2 if simple else -6.5}H{num(bx + 7.5)}V-38Q{num(bx + 7.5)} -49 {num(bx + 1.5)} -56'
             f'Q{num(bx - 6.5)} -47 {num(bx - 7.5)} -31Z" fill="{CREAM}"/>')
    if not simple:
        m.append(f'<circle cx="{num(bx)}" cy="2.5" r="3.2" fill="{DEEP}"/>')
        m.append(f'<circle cx="{num(bx)}" cy="33" r="2.6" fill="{DEEP}"/>')
    # left stem: open-end wrench, turns about its centre
    w = (f'<g transform="translate(0,-32) rotate(14)"><path d="{wrench_head_path()}" fill="{GOLD}"/></g>'
         f'<path d="M-10.5 -26L10.5 -26L7.6 -12V40.4A7.6 7.6 0 0 1 -7.6 40.4V-12Z" fill="{GOLD}"/>'
         + ("" if simple else f'<circle cy="37" r="3.6" fill="{DEEP}"/>'))
    m.append(f'<g transform="translate({WRENCH_X},{WRENCH_Y})">' + cx.g("wrench", w) + "</g>")
    if simple:
        s.append('<g transform="translate(0,6) scale(1.1)">' + "".join(m) + "</g>")
        s.append(f'<g transform="translate({SPARK_POS[0]},{SPARK_POS[1] + 2})"><path d="{star(17, 0.2)}" fill="{GOLD}"/></g>')
        return "".join(s)
    # spark (with a burst of particles when the M snaps together)
    parts = []
    for i, ang in enumerate((45, 135, 225, 315)):
        col = GOLD if i % 2 == 0 else CREAM
        dot = cx.g("burst", f'<circle r="3" fill="{col}"/>')
        if dot:
            parts.append(f'<g transform="rotate({ang})">{dot}</g>')
    sp = (f'<path d="{star(17)}" fill="{GOLD}"/>'
          f'<circle r="3.6" fill="{ORANGE}"/>')
    s.append(f'<g transform="translate({SPARK_POS[0]},{SPARK_POS[1]})">' + "".join(parts)
             + cx.g("spark", cx.g("sparkrot", sp)) + "</g>")
    # the wrench is drawn last so that it sits on top while it turns
    s.extend(m)
    return "".join(s)


# Rover geometry: ground at y=0, front faces -x. ~100 units long.
WHEELS = (-29.0, 29.0)
WHEEL_Y = -17.0
WHEEL_R = 16.0
OUTL = 5.5           # sticker outline width (rover units)
BODY = (-50.0, -74.0, 48.0, -25.0)
ANT_BASE = (27.0, -73.0)
ANT_TOP = (29.0, -99.0)


def rover(cx: Ctx, outline: str = CREAM) -> str:
    bx0, by0, bx1, by1 = BODY
    body_d = rrect(bx0, by0, bx1, by1, 25, 15, 11, 11)
    ax, ay = ANT_BASE
    tx, ty = ANT_TOP[0] - ax, ANT_TOP[1] - ay        # antenna tip relative to its base
    gear_r = 10.5

    # --- sticker outline layer (everything that sticks out gets a cream rim)
    o = []
    ant_o = (f'<path d="M0 0L{num(tx)} {num(ty)}" stroke="{outline}" stroke-width="{num(4.6 + 2 * OUTL)}" '
             f'stroke-linecap="round"/><circle cx="{num(tx)}" cy="{num(ty - 5)}" r="{num(gear_r + OUTL)}" fill="{outline}"/>')
    ant_o_g = f'<g transform="translate({ax},{ay})">' + cx.g("antenna", ant_o) + "</g>"
    o.append(f'<g transform="translate(0,{WHEEL_Y})">' + cx.g("tilt", f'<g transform="translate(0,{-WHEEL_Y})">'
             + ant_o_g + f'<path d="{body_d}" fill="{outline}" stroke="{outline}" stroke-width="{2 * OUTL}" '
             f'stroke-linejoin="round"/></g>') + "</g>")
    for wx in WHEELS:
        o.append(f'<circle cx="{wx}" cy="{WHEEL_Y}" r="{num(WHEEL_R + 3 + OUTL)}" fill="{outline}"/>')

    # --- speed lines (behind the rover, only while driving)
    sl = "".join(f'<path d="M{a} {y}H{b}" stroke="{SAGE}" stroke-width="4.4" stroke-linecap="round"/>'
                 for a, b, y in ((4, 24, -60), (0, 30, -45), (8, 22, -30)))
    speed = cx.g("speed", sl)
    speed = f'<g transform="translate({num(bx1 + 12)},0)">{speed}</g>' if speed else ""

    # --- antenna with spinning gear
    gear = (f'<g transform="translate({num(tx)},{num(ty - 5)})">'
            + cx.g("gear", f'<path d="{gear_path(8, gear_r, 7.6)}" fill="{GOLD}"/>'
                           f'<circle r="3" fill="{DEEP}"/>') + "</g>")
    ant = (f'<path d="M0 0L{num(tx)} {num(ty)}" stroke="{DEEP}" stroke-width="4.6" stroke-linecap="round"/>' + gear)
    ant_g = f'<g transform="translate({ax},{ay})">' + cx.g("antenna", ant) + "</g>"

    # --- body: sage shell, green bumper, gold seam, visor face with headlight eyes
    eye_r = 7.4
    eyes = []
    for ex in (-35.0, -16.5):
        e = (f'<circle r="{eye_r}" fill="{CREAM}"/>'
             f'<circle r="{eye_r}" fill="none" stroke="{GOLD}" stroke-width="1.6"/>'
             + f'<g transform="translate(-1.6,-1.2)">' + cx.g("look", f'<circle r="3.3" fill="{DEEP}"/>'
                                                          f'<circle cx="1.1" cy="-1.1" r="1" fill="{CREAM}"/>') + "</g>")
        eyes.append(f'<g transform="translate({ex},-53)">' + cx.g("blink", e) + "</g>")
    bumper = rrect(bx0, -38, bx1, by1, 0, 0, 11, 11)
    body = (f'<path d="{body_d}" fill="{SAGE}"/>'
            f'<path d="{bumper}" fill="{GREEN}"/>'
            f'<path d="M{bx0} -38H{bx1}" stroke="{GOLD}" stroke-width="2.4"/>'
            f'<path d="{rrect(-46, -67, -6, -39, 14, 12, 12, 12)}" fill="{DEEP}"/>'
            + "".join(eyes)
            + f'<circle cx="{num(bx1 - 6)}" cy="-52" r="3.6" fill="{ORANGE}"/>'
            + f'<path d="M14 -64V-44" stroke="{GREEN}" stroke-width="2.2" stroke-linecap="round"/>'
            + f'<circle cx="-33" cy="-31.5" r="1.9" fill="{DEEP}"/><circle cx="33" cy="-31.5" r="1.9" fill="{DEEP}"/>')
    body_g = (f'<g transform="translate(0,{WHEEL_Y})">' + cx.g("tilt", f'<g transform="translate(0,{-WHEEL_Y})">'
              + ant_g + body + "</g>") + "</g>")

    # --- chunky wheels with tread knobs, rolling
    wheels = []
    for wx in WHEELS:
        knobs = "".join(f'<rect x="-3.6" y="{num(-WHEEL_R - 3)}" width="7.2" height="7" rx="2" '
                        f'transform="rotate({k * 45})" fill="{DEEP}"/>' for k in range(8))
        lugs = "".join(f'<circle cx="{num(5.2 * math.cos(math.radians(a)))}" cy="{num(5.2 * math.sin(math.radians(a)))}" '
                       f'r="1.7" fill="{DEEP}"/>' for a in (-90, 30, 150))
        w = (f'{knobs}<circle r="{WHEEL_R}" fill="{DEEP}"/><circle r="9.4" fill="{CREAM}"/>{lugs}'
             f'<circle r="2.6" fill="{GOLD}"/>')
        wheels.append(f'<g transform="translate({wx},{WHEEL_Y})">' + cx.g("wheel", w) + "</g>")

    # outline layer first (cream rim around the union of all parts), then the fills
    return speed + "".join(o) + body_g + "".join(wheels)


def rover_group(cx: Ctx, outline: str = CREAM) -> str:
    """Rover with drive / hop / flip groups (local units)."""
    return cx.g("rvx", cx.g("hop", cx.g("flip", rover(cx, outline))))


# ----------------------------------------------------------------- layouts --
class Layout:
    def __init__(self, name, w, h, badge_c, badge_r, rover_xy, rover_s, ruler=None):
        self.name, self.w, self.h = name, w, h
        self.badge_c, self.badge_r = badge_c, badge_r
        self.rover_xy, self.rover_s = rover_xy, rover_s
        self.ruler = ruler
        # distance (rover units) that takes the rover + its speed lines fully off the right edge
        ext = 112.0
        self.travel = (w - rover_xy[0]) / rover_s + ext
        self.T = tracks(self.travel, WHEEL_R + 1.5)

    def svg(self, frame: float | None, outline: str = CREAM, title: str | None = None,
            prefix: str = "mg") -> str:
        cx = Ctx(self.T, frame, prefix)
        bs = self.badge_r / 100.0
        parts = []
        if self.ruler:
            x0, x1, y = self.ruler
            ticks = "".join(
                f'<path d="M{x} {y + 1}v{5 if (x - x0) % 50 == 0 else 2.6}" stroke="{SAGE}" stroke-width="1.6"/>'
                for x in range(int(x0), int(x1) + 1, 10))
            parts.append(f'<g><path d="M{x0} {y}H{x1}" stroke="{SAGE}" stroke-width="2" stroke-linecap="round"/>{ticks}</g>')
        parts.append(f'<g transform="translate({num(self.badge_c[0])},{num(self.badge_c[1])}) scale({num(bs)})">'
                     + badge(cx, outline) + "</g>")
        rx, ry = self.rover_xy
        parts.append(f'<g transform="translate({num(rx)},{num(ry)}) scale({num(self.rover_s)})">'
                     + rover_group(cx, outline) + "</g>")
        body = "".join(parts)
        style = f"<style>{cx.css()}</style>" if frame is None else ""
        t = f"<title>{title}</title>" if title else ""
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
                f'width="{self.w}" height="{self.h}" role="img">{t}{style}{body}</svg>')


SQUARE = Layout("square", 192, 192, badge_c=(80, 80), badge_r=76, rover_xy=(141, 186), rover_s=0.8)
WIDE = Layout("wide", 480, 144, badge_c=(186, 72), badge_r=63, rover_xy=(318, 135), rover_s=0.76,
              ruler=(120, 466, 137))


def favicon_svg(size: int = 64) -> str:
    """Simplified badge for 16-32 px: disc, gold ring, bold M (wrench + V + blade), spark."""
    cx = Ctx(SQUARE.T, 0)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-100 -100 200 200" width="{size}" height="{size}">'
            f'<title>MacGyver Engineering Academy</title>{badge(cx, simple=True)}</svg>\n')


# --------------------------------------------------------------- rendering --
class Renderer:
    def __init__(self):
        from playwright.sync_api import sync_playwright
        self._pw = sync_playwright().start()
        self.browser = self._pw.chromium.launch()
        self.pages = {}

    def page(self, w, h, scale):
        key = (w, h, scale)
        if key not in self.pages:
            ctx = self.browser.new_context(viewport={"width": w, "height": h}, device_scale_factor=scale)
            p = ctx.new_page()
            p.set_content("<!doctype html><html><head><style>html,body{margin:0;background:transparent}"
                          "#s,#s svg{display:block}</style></head><body><div id='s'></div></body></html>")
            self.pages[key] = p
        return self.pages[key]

    def render(self, svg: str, w: int, h: int, ss: int = SS) -> np.ndarray:
        """Render SVG markup at ss x and return a float RGBA array (premultiplied box downsample)."""
        p = self.page(w, h, ss)
        p.evaluate("s => { document.getElementById('s').innerHTML = s; }", svg)
        png = p.screenshot(clip={"x": 0, "y": 0, "width": w, "height": h}, omit_background=True)
        import io
        im = Image.open(io.BytesIO(png)).convert("RGBA")
        a = np.asarray(im, dtype=np.float64) / 255.0
        H, W = a.shape[0] // ss, a.shape[1] // ss
        al = a[..., 3]
        pm = a[..., :3] * al[..., None]
        pm = pm[: H * ss, : W * ss].reshape(H, ss, W, ss, 3).mean(axis=(1, 3))
        al = al[: H * ss, : W * ss].reshape(H, ss, W, ss).mean(axis=(1, 3))
        rgb = np.where(al[..., None] > 1e-6, pm / np.maximum(al[..., None], 1e-6), 0.0)
        return np.dstack([np.clip(rgb, 0, 1), al])

    def close(self):
        self.browser.close()
        self._pw.stop()


def to_rgba_image(fr: np.ndarray) -> Image.Image:
    return Image.fromarray(np.round(fr * 255).astype(np.uint8), "RGBA")


def hex_rgb(h: str) -> np.ndarray:
    return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], dtype=np.float64) / 255.0


def make_gif(frames: list[np.ndarray], matte: str, path: Path, colors: int = 160, thr: float = 0.5) -> int:
    """1-bit-alpha GIF: composite edge pixels onto `matte`, share one global palette,
    then let ImageMagick do frame/transparency optimisation."""
    bg = hex_rgb(matte)
    rgbs, masks = [], []
    for fr in frames:
        a = fr[..., 3:4]
        rgb = fr[..., :3] * a + bg * (1 - a)
        rgbs.append(np.round(rgb * 255).astype(np.uint8))
        masks.append(fr[..., 3] >= thr)
    # global palette from all opaque pixels; brand colours are snapped back to exact values
    samples = np.concatenate([r[m] for r, m in zip(rgbs, masks)], axis=0)
    strip = Image.fromarray(samples.reshape(-1, 1, 3), "RGB")
    pal_img = strip.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    pal = np.array(pal_img.getpalette()[: colors * 3], dtype=np.int32).reshape(-1, 3)
    for hx in (DEEP, GREEN, SAGE, CREAM, GOLD, ORANGE):
        c = np.round(hex_rgb(hx) * 255).astype(np.int32)
        d = np.abs(pal - c).sum(1)
        i = int(d.argmin())
        if d[i] <= 24:
            pal[i] = c
    pal_ref = Image.new("P", (1, 1))
    pal_ref.putpalette(pal.astype(np.uint8).flatten().tolist() + [0] * (768 - pal.size))
    tmp = Path(tempfile.mkdtemp(prefix="mglogo-"))
    try:
        names = []
        for i, (rgb, m) in enumerate(zip(rgbs, masks)):
            q = Image.fromarray(rgb, "RGB").quantize(palette=pal_ref, dither=Image.Dither.NONE).convert("RGB")
            arr = np.dstack([np.asarray(q), (m * 255).astype(np.uint8)])
            arr[~m, :3] = 0
            fn = tmp / f"f{i:03d}.png"
            Image.fromarray(arr, "RGBA").save(fn)
            names.append(fn)
        cmd = ["convert", "-loop", "0", "-dispose", "Background"]
        for i, fn in enumerate(names):
            cmd += ["-delay", str(DELAYS_CS[i % len(DELAYS_CS)]), str(fn)]
        cmd += ["-layers", "Optimize", "+remap", str(path)]
        subprocess.run(cmd, check=True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return path.stat().st_size


def verify_gif(path: Path, frames: list[np.ndarray], matte: str, thr: float = 0.5) -> float:
    """Coalesce the GIF with ImageMagick, re-composite on the matte and return the
    worst per-frame mean error (0..255) against the intended anti-aliased frame."""
    bg = hex_rgb(matte)
    worst = 0.0
    tmp = Path(tempfile.mkdtemp(prefix="mgcheck-"))
    try:
        subprocess.run(["convert", str(path), "-coalesce", str(tmp / "c_%03d.png")], check=True)
        for i, fr in enumerate(frames):
            got = np.asarray(Image.open(tmp / f"c_{i:03d}.png").convert("RGBA"), dtype=np.float64)
            ga = got[..., 3:4] / 255.0
            g = got[..., :3] * ga + bg * 255 * (1 - ga)
            a = fr[..., 3:4]
            want = (fr[..., :3] * a + bg * (1 - a)) * 255
            worst = max(worst, float(np.abs(g - want).mean()))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return worst


# ------------------------------------------------------------------ preview --
STORY = [(0, "rest"), (3, "blink"), (10, "wrench turns"), (14, "quarter turn"), (19, "snaps back · spark"),
         (25, "double blink"), (30, "turns round"), (34, "drives off"), (40, "rolls in"), (44, "brakes · antenna wobble")]


def write_preview(sizes: dict[str, int]) -> None:
    anim = (OUT / "logo-animated.svg").read_text(encoding="utf-8").strip()
    kb = {k: f"{v / 1024:.1f} KB" for k, v in sizes.items()}
    story_css = "".join(
        f".sb{i} .mg-a{{animation-delay:-{f / FRAMES * LOOP_S:.3f}s;animation-play-state:paused}}"
        for i, (f, _) in enumerate(STORY))
    bare = anim[: anim.index("<style>")] + anim[anim.index("</style>") + 8:]
    story = "".join(f'<figure class="sb{i}"><div class="cell">{anim if i == 0 else bare}</div>'
                    f'<figcaption>{f:02d} · {lab}</figcaption></figure>' for i, (f, lab) in enumerate(STORY))

    def tile(src, size, label, bg_cls=""):
        return (f'<figure class="tile {bg_cls}"><img src="{src}" width="{size}" height="{size}" alt="">'
                f'<figcaption>{label}</figcaption></figure>')

    def brand_row(src):
        return (f'<a class="brand"><img src="{src}" width="43" height="43" alt="">'
                f'<span>馬蓋先<small>MACGYVER ACADEMY</small></span></a>')

    swatches = "".join(f'<span class="sw"><i style="background:{c}"></i>{n}<code>{c}</code></span>'
                       for n, c in (("deep green", DEEP), ("green", GREEN), ("sage", SAGE), ("cream", CREAM),
                                    ("mist", MIST), ("gold", GOLD), ("orange", ORANGE), ("night", NIGHT)))
    html = f"""<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>V12 Brand Mark Preview</title>
<link rel="icon" href="favicon.svg">
<style>
:root{{--deep:{DEEP};--green:{GREEN};--sage:{SAGE};--cream:{CREAM};--gold:{GOLD};--night:{NIGHT};
--mono:ui-monospace,"SFMono-Regular",Menlo,Consolas,monospace}}
*{{box-sizing:border-box}}
body{{margin:0;background:#e9ece4;color:var(--deep);font:15px/1.5 "Noto Sans CJK TC","Noto Sans TC",system-ui,sans-serif}}
main{{max-width:1180px;margin:0 auto;padding:32px 16px 48px}}
header{{display:flex;align-items:center;gap:20px;margin-bottom:22px}}
header h1{{margin:0;font-size:26px;letter-spacing:.04em}}
header p{{margin:2px 0 0;color:#4f6457;font-size:14px}}
.eyebrow{{font:600 11px var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--green)}}
.swatches{{display:flex;flex-wrap:wrap;gap:8px 18px;margin:0 0 26px}}
.sw{{display:flex;align-items:center;gap:7px;font-size:12.5px}}
.sw i{{width:22px;height:22px;border-radius:6px;box-shadow:inset 0 0 0 1px #0002}}
.sw code{{font:11px var(--mono);color:#5b6d61}}
.panel{{border-radius:16px;padding:22px 22px 18px;margin:0 0 18px}}
.light{{background:#fcfcf9;box-shadow:0 0 0 1px #dce2d9}}
.cream{{background:var(--cream)}}
.dark{{background:var(--night);color:#e0eaed}}
.dark .eyebrow{{color:#9fc0a5}} .dark figcaption{{color:#a8bcc4}}
.panel h2{{margin:0 0 14px;font-size:15px;font-weight:700}}
.row{{display:flex;flex-wrap:wrap;align-items:flex-end;gap:22px}}
figure{{margin:0;display:flex;flex-direction:column;align-items:center;gap:6px}}
figcaption{{font:11px/1.35 var(--mono);color:#5b6d61;text-align:center}}
.tile img{{display:block}}
.sep{{width:1px;align-self:stretch;background:#0001}} .dark .sep{{background:#fff2}}
.brand{{flex:0 0 auto;display:flex;align-items:center;gap:11px;font-size:24px;font-weight:700;letter-spacing:2px;color:inherit;text-decoration:none;
padding:14px 18px;border-radius:12px;min-width:230px}}
.brand small{{display:block;font:8px var(--mono);letter-spacing:1px;margin-top:2px}}
.light .brand{{background:#fcfcf9;box-shadow:0 0 0 1px #dce2d9}}
.dark .brand{{background:#19282f}}
.wide img{{display:block;max-width:100%;height:auto}}
.story{{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:16px 14px}}
.story .cell{{width:100%;max-width:168px;aspect-ratio:1;border-radius:12px;background:#fcfcf9;box-shadow:0 0 0 1px #dce2d9;padding:8px}}
.story svg{{width:100%;height:100%;display:block}}
@media (max-width:640px){{.story{{grid-template-columns:repeat(2,minmax(0,1fr))}}}}
{story_css}
.meta{{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:4px 22px;font:12px var(--mono);color:#4f6457;margin:0;padding:0;list-style:none}}
</style></head>
<body><main>
<header><img src="logo-animated.gif" width="72" height="72" alt="">
<div><div class="eyebrow">MacGyver Engineering Academy · V12 brand</div><h1>馬蓋先 — engineer badge &amp; rover sidekick</h1>
<p>Loop {LOOP_S:g} s · {FRAMES} frames · all assets in <code>assets/brand/</code></p></div></header>
<div class="swatches">{swatches}</div>

<section class="panel light"><div class="eyebrow">Light UI · sidebar #fcfcf9</div><h2>Square mark</h2>
<div class="row">
{tile("logo-animated.gif", 192, "logo-animated.gif<br>192 · " + kb["logo-animated.gif"])}
{tile("logo-animated.svg", 192, "logo-animated.svg<br>CSS loop · " + kb["logo-animated.svg"])}
{tile("logo-static.png", 192, "logo-static.png<br>" + kb["logo-static.png"])}
{tile("logo-static.svg", 192, "logo-static.svg<br>" + kb["logo-static.svg"])}
</div><div class="row" style="margin-top:20px">
{tile("logo-animated.gif", 56, "56 px")}{tile("logo-animated.gif", 48, "48 px")}{tile("logo-animated.gif", 40, "40 px")}
{tile("logo-static.svg", 48, "static.svg<br>48 px")}
<div class="sep"></div>
{tile("favicon.svg", 64, "favicon.svg<br>64")}{tile("favicon.svg", 32, "32")}{tile("favicon-32.png", 32, "favicon-32.png")}{tile("favicon.svg", 16, "16")}
<div class="sep"></div>{brand_row("logo-animated.gif")}
</div>
</section>

<section class="panel dark"><div class="eyebrow">Dark UI · page #111b20 · sidebar #19282f</div><h2>Square mark on dark</h2>
<div class="row">
{tile("logo-dark.gif", 192, "logo-dark.gif<br>192 · " + kb["logo-dark.gif"])}
{tile("logo-animated.svg", 192, "logo-animated.svg")}
{tile("logo-static.png", 192, "logo-static.png")}
{tile("logo-static.svg", 192, "logo-static.svg")}
</div><div class="row" style="margin-top:20px">
{tile("logo-dark.gif", 56, "56 px")}{tile("logo-dark.gif", 48, "48 px")}{tile("logo-dark.gif", 40, "40 px")}
{tile("logo-animated.gif", 48, "light gif<br>on dark")}
<div class="sep"></div>
{tile("favicon.svg", 64, "favicon.svg")}{tile("favicon.svg", 32, "32")}{tile("favicon-32.png", 32, "png 32")}{tile("favicon.svg", 16, "16")}
<div class="sep"></div>{brand_row("logo-dark.gif")}
</div>
</section>

<section class="panel cream wide"><div class="eyebrow">Banner · 480×144 · cream #f5f1e6</div><h2>logo-animated-wide.gif · {kb["logo-animated-wide.gif"]}</h2>
<img src="logo-animated-wide.gif" width="480" height="144" alt=""></section>
<section class="panel dark wide"><div class="eyebrow">Banner on dark</div><h2>logo-animated-wide-dark.gif · {kb["logo-animated-wide-dark.gif"]}</h2>
<img src="logo-animated-wide-dark.gif" width="480" height="144" alt=""></section>

<section class="panel light"><div class="eyebrow">Storyboard</div><h2>The loop, paused at ten moments (inline copies of logo-animated.svg)</h2>
<div class="story">{story}</div></section>

<section class="panel light"><div class="eyebrow">Files</div>
<ul class="meta">{"".join(f"<li>{k} — {v}</li>" for k, v in kb.items())}</ul></section>
</main></body></html>
"""
    (OUT / "preview.html").write_text(html, encoding="utf-8")


def screenshot_preview(path: Path) -> None:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1240, "height": 900}, device_scale_factor=1)
        pg.goto((OUT / "preview.html").as_uri())
        pg.wait_for_load_state("networkidle")
        pg.wait_for_timeout(60)
        pg.screenshot(path=str(path), full_page=True)
        b.close()


# --------------------------------------------------------------------- main --
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", metavar="DIR", help="also dump the RGBA review frames into DIR")
    ap.add_argument("--only", choices=["svg", "all"], default="all")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    title = "馬蓋先 MacGyver Engineering Academy"

    # ---- vectors
    (OUT / "logo-animated.svg").write_text(SQUARE.svg(None, title=title) + "\n", encoding="utf-8")
    (OUT / "logo-static.svg").write_text(SQUARE.svg(0, title=title) + "\n", encoding="utf-8")
    (OUT / "favicon.svg").write_text(favicon_svg(), encoding="utf-8")
    if args.only == "svg":
        return

    r = Renderer()
    try:
        sq = [r.render(SQUARE.svg(f), SQUARE.w, SQUARE.h) for f in range(FRAMES)]
        wd = [r.render(WIDE.svg(f), WIDE.w, WIDE.h) for f in range(FRAMES)]
        fav32 = r.render(favicon_svg(32), 32, 32, ss=8)
    finally:
        r.close()

    to_rgba_image(sq[0]).save(OUT / "logo-static.png", optimize=True)
    to_rgba_image(fav32).save(OUT / "favicon-32.png", optimize=True)

    report = []
    for frames, matte, name in ((sq, LIGHT_MATTE, "logo-animated.gif"),
                                (sq, DARK_MATTE, "logo-dark.gif"),
                                (wd, LIGHT_MATTE, "logo-animated-wide.gif"),
                                (wd, DARK_MATTE, "logo-animated-wide-dark.gif")):
        size = make_gif(frames, matte, OUT / name)
        err = verify_gif(OUT / name, frames, matte)
        report.append(f"{name:30s} {size / 1024:7.1f} KB   {len(frames)} frames   mean err {err:.2f}")

    names = ["logo-animated.gif", "logo-animated-wide.gif", "logo-dark.gif", "logo-animated-wide-dark.gif",
             "logo-animated.svg", "logo-static.svg", "logo-static.png", "favicon.svg", "favicon-32.png"]
    write_preview({n: (OUT / n).stat().st_size for n in names})
    screenshot_preview(HERE / "preview.png")
    report.append(f"preview: {OUT / 'preview.html'}  ->  {HERE / 'preview.png'}")

    if args.frames:
        fd = Path(args.frames)
        fd.mkdir(parents=True, exist_ok=True)
        for i, fr in enumerate(sq):
            to_rgba_image(fr).save(fd / f"sq-{i:02d}.png")
        for i, fr in enumerate(wd):
            to_rgba_image(fr).save(fd / f"wide-{i:02d}.png")
    print("\n".join(report))


if __name__ == "__main__":
    main()
