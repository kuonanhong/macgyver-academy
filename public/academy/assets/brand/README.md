# 馬蓋先 MacGyver Engineering Academy: V12 brand mark

## Concept

**"The engineer and his sidekick"**, drawn as an abstract brand mark. It does not show a character.

- **Engineer badge.** A deep-green circular badge with a gold ring. Inside it is an "M" built from tools:
  - the left stem is an open-end wrench (gold);
  - the middle is a folding-tool linkage that forms a V with a pivot rivet;
  - the right stem is a multitool blade that folds out of its handle.
  
  A four-point spark sits above the M. It is gold with a warm-orange core.
- **Rover sidekick.** A small, friendly engineering rover:
  - a rounded sage body with a green bumper and a gold seam;
  - a dark visor with two round headlight eyes;
  - an antenna whose tip is a turning gear;
  - chunky tread wheels.
  
  Every element has a cream sticker outline, so the mark reads on both light and dark UI.

**Loop.** The loop lasts 3.2 s, in 48 frames at about 15 fps. Times below are in frames.

| Frames | Motion |
| --- | --- |
| 0 | Rest: the full mark is shown (frame 0 is a complete logo). |
| 1–5 | The rover blinks. |
| 6–22 | The wrench turns a quarter turn, holds, then snaps back to re-form the "M" with a small overshoot. The rover's eyes follow it. |
| 17–27 | A spark burst plays: the star grows and rotates 90°, and four particles fly out. |
| 24–28 | The rover double-blinks. |
| 29–36 | The rover hops, turns round, and drives off with speed lines. |
| 37–48 | The rover rolls back in, brakes with a nose-dip, and the antenna wobbles before settling. |

The antenna gear turns the whole time, 180° per loop, which is seamless for an 8-tooth gear.

## Palette

| Token | Hex | Used for |
| --- | --- | --- |
| deep green | `#153c35` | badge disc, tyres, visor |
| green | `#4b755a` | rover bumper |
| sage | `#739578` | rover body, speed lines, ruler |
| cream | `#f5f1e6` | sticker outline, M, eyes |
| gold | `#d7bd75` | wrench, ring, gear, spark |
| warm orange | `#c8643b` | spark core, tail lamp (used sparingly) |
| night | `#111b20` | dark UI reference |

## Files

| File | Size / format | Use |
| --- | --- | --- |
| `logo-animated.gif` | 192×192 | Sidebar / brand slot on light UI. Transparent, edges matted to `#f8f6ef`. |
| `logo-dark.gif` | 192×192 | Same loop with edges matted for dark UI (`#111b20` / `#19282f`). |
| `logo-animated-wide.gif` | 480×144 | Banner. The badge and rover sit side by side on an engineering ruler. Light version. |
| `logo-animated-wide-dark.gif` | 480×144 | Banner, dark version. |
| `logo-animated.svg` | vector | CSS-animated vector of the same loop. It contains no scripts and honours `prefers-reduced-motion`. |
| `logo-static.svg` | vector | Resting frame. |
| `logo-static.png` | 192×192 | Resting frame with full alpha. Use it for reduced motion. |
| `favicon.svg` | vector | Simplified badge, for 16–64 px. |
| `favicon-32.png` | 32×32 | Raster version of the simplified badge. |
| `preview.html` | page | Every asset on light and dark backgrounds, plus a 10-frame storyboard. |

The main GIF also reads well on dark backgrounds at 40–56 px because of its cream outline. Use `logo-dark.gif` when it is shown at full size on dark backgrounds, so the edges stay clean.

Example markup:

```html
<picture>
  <source srcset="assets/brand/logo-static.png" media="(prefers-reduced-motion: reduce)">
  <source srcset="assets/brand/logo-dark.gif" media="(prefers-color-scheme: dark)">
  <img src="assets/brand/logo-animated.gif" width="43" height="43" alt="馬蓋先 MacGyver Academy">
</picture>
```

## Regenerate

From the project root, run:

```sh
python3 tools/brand-v12/make_logo.py            # all assets, plus preview.html and tools/brand-v12/preview.png
python3 tools/brand-v12/make_logo.py --only svg # vectors only
```

It needs:

- Python 3 with Pillow and numpy;
- `playwright` with Chromium installed;
- ImageMagick `convert`.

The script works from one set of keyframe tracks:

1. It emits the CSS keyframes for the animated SVG from those tracks.
2. It renders each raster frame from the same tracks in headless Chromium at 4×, then box-downsamples it in premultiplied alpha.
3. It builds each GIF:
   - one shared palette (brand colours kept exact);
   - 1-bit transparency;
   - ImageMagick frame and transparency optimisation.
4. It decodes the result again to verify it.

## Originality

This mark was designed from scratch for the academy. It is geometric and abstract:

- No person or likeness of any actor appears. There is no hairstyle and no clothing.
- The vehicle is a rounded green toy-like rover with headlight eyes. It is not a black sports coupé and is not modelled on any real car.
- There is no red light bar or scanning animation.
- It is not based on any existing TV or film character, logo or artwork.

The only letterform is the tool-built "M".
