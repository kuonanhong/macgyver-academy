#!/usr/bin/env python3
"""Assign one unique, representative line icon to every MacGyver Engineering Academy V12 project.

Stdlib only.  Run from anywhere:

    python3 -I tools/icons-v12/assign_icons.py \
        --tabler /path/to/tabler-icons/icons/outline \
        --mdi    /path/to/MaterialDesign-SVG

Sources (fetch once, nothing is downloaded by this script):
    git clone --depth 1 https://github.com/tabler/tabler-icons.git            (MIT)
    git clone --depth 1 --filter=blob:none --sparse \
        https://github.com/Templarian/MaterialDesign-SVG.git && \
        git -C MaterialDesign-SVG sparse-checkout set svg                       (Apache-2.0)

If --tabler / --mdi are omitted the script looks at $ICONS_V12_TABLER / $ICONS_V12_MDI and a few
conventional locations.  MDI is optional; without it every glyph comes from Tabler.

Writes:
    public/academy/data/project-icons.json
    public/academy/assets/icons/LICENSES.md
    tools/icons-v12/REPORT.md

Method (deterministic, no randomness):
  1. Terms.  Every project yields weighted origin terms: English title n-grams (1.0), Traditional
     Chinese title keywords translated through the zh table (0.8), proper nouns via the names table
     (1.0), sub-category (0.45), diagram hints (0.3/0.2), catalog category (0.3) and the English
     summary (0.25, table terms only).  Generic words ("control", "system" ...) are down-weighted.
  2. Synonyms.  Each term expands through synonyms.json to icon targets (full icon names or name
     tokens, with weights); a term without an entry matches icon names/tags literally.
  3. Evidence per glyph = match (best target per term: full name 1.0, name token 0.7, MDI alias 0.55;
     tags 0.3 capped; diminishing returns 0.6^k across terms; x name-coverage factor) + category
     theme (curated per-category list, then name-prefix families) + inheritance (badge variants such
     as airplane-cog inherit a share of their base glyph's match).  q = 1 - exp(-raw / 1.1).
  4. Selection score = match x glyph prior (UI-ish families such as arrows or text formatting rank
     lower) x 0.6 for MDI (an MDI glyph must match ~67% better than the best unused Tabler glyph)
     + theme + inheritance; flagship courses (named ids) get first pick.
  5. Uniqueness.  Global best-first greedy over all (project, glyph, score) pairs, so strong matches
     are never consumed by weak projects; then exchange chains of depth <= 2 that raise the summed
     score; then category / neutral pools.  Weak picks with neither concept nor theme evidence are
     replaced by neutral geometric glyphs (never a misleading pictogram).
  6. Policy.  Never: brand / logo glyphs, product trademarks outside the Brand category (Steam,
     PlayStation, Olympic rings, Apple devices ...), religious, weapon and drug symbols.  Avoid tier
     (last resort, unused in practice): letters, numbers, zodiac, gender, mood, laundry, gestures,
     badges, -off variants, badge variants of UI glyphs and trivial glyphs.
"""
import argparse
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
CATALOG = os.path.join(ROOT, 'public', 'academy', 'data', 'catalog.json')
OUT_JSON = os.path.join(ROOT, 'public', 'academy', 'data', 'project-icons.json')
OUT_LICENSES = os.path.join(ROOT, 'public', 'academy', 'assets', 'icons', 'LICENSES.md')
OUT_REPORT = os.path.join(HERE, 'REPORT.md')
SYNONYMS = os.path.join(HERE, 'synonyms.json')

GEOMETRY_ATTRS = ('d', 'cx', 'cy', 'r', 'x', 'y', 'width', 'height', 'rx', 'ry', 'points', 'x1', 'y1', 'x2', 'y2')
ELEMENTS = ('path', 'circle', 'line', 'rect', 'polyline', 'polygon', 'ellipse')

# ---- source weights -------------------------------------------------------------------------
W_TITLE, W_ZH, W_SUB, W_DIAG_TYPE, W_DIAG_LABEL, W_CAT, W_SUMMARY = 1.0, 0.8, 0.45, 0.3, 0.2, 0.3, 0.25
COVERED_UNIGRAM = 0.55          # unigram inside a longer matched phrase
M_FULL, M_NAME, M_ALIAS, M_TAG, M_MDI_TAG = 1.0, 0.7, 0.55, 0.3, 0.12
TAG_CAP = 0.6
DECAY = 0.6                     # 2nd, 3rd ... matching term for the same glyph counts 0.6, 0.36 ...
COV_BASE = 0.15                 # name-coverage factor = COV_BASE + (1 - COV_BASE) * matched share
THEME_BONUS = 0.3               # category theme pool bonus (first-listed glyph; last gets 40% of it)
FAMILY_BONUS = 0.12             # glyphs of the category's name-prefix families (after the explicit theme list)
TAG_FAMILY_BONUS = 0.0          # (disabled) category-wide icon groups proved too loose: snowman for a radio array
MIN_EFF = 0.04                  # candidates below this are noise
Q_SCALE = 1.1
MDI_FACTOR = 0.6               # MDI must match ~67% better than the best unused Tabler glyph to be chosen
VARIANT_FACTOR = 0.96
CANDIDATES_PER_PROJECT = 160
SWAP_MARGIN = 0.03
CHAIN_BRANCH = 12               # candidates explored per step of an exchange chain
INHERIT_TOP = 15                # a project's best concept glyphs whose badge variants inherit a share of the score
INHERIT_SHARE = 0.3
FLAGSHIP_BOOST = 2.2            # flagship courses (named ids, not a001-style) pick before minor topics
TAIL_EFF = 0.15                 # weaker picks that are neither concept-derived nor on-theme become neutral geometry
CHAIN_SCAN = 80                 # how deep to look for a free alternative

# ---- icon policy ----------------------------------------------------------------------------
TABLER_NEVER_CATEGORIES = {'Brand'}
TABLER_AVOID_CATEGORIES = {'Letters', 'Numbers', 'Zodiac', 'Gender', 'Mood', 'Laundry', 'Gestures', 'Badges'}
MDI_NEVER_TAGS = {'Brand / Logo', 'Religion', 'Holiday', 'Emoji'}
MDI_AVOID_TAGS = {'Alpha / Numeric', 'Gaming / RPG', 'Clothing'}
# trademarks / product names that are not in the Brand category, plus symbols unsuitable for an
# engineering curriculum (religious, weapons, drugs, death, ratings).
NEVER_NAME_PATTERNS = [
    r'airpods', r'(^|-)imac($|-)', r'(^|-)ipad($|-)', r'vision-pro', r'nintendo', r'airtag', r'playstation',
    r'(^|-)xbox', r'cardboards', r'face-id', r'shareplay', r'michelin', r'mickey', r'olympic', r'^rings$',
    r'pokeball', r'pokemon', r'^steam$', r'trademark', r'^registered$', r'servicemark', r'copyright', r'copyleft',
    r'creative-commons', r'^ce$', r'file-excel', r'file-word', r'file-type-(doc|docx|ppt|xls|pdf)$', r'^pdf$',
    r'(^|-)lego', r'segway', r'jetski', r'bluetooth', r'^usb$', r'usb-port', r'bitcoin', r'monero', r'ethereum',
    r'burj-al-arab', r'^command$', r'^option$', r'^xd$', r'border-corner-ios', r'space-invaders', r'pac-?man',
    r'firewire', r'^nfc', r'chademo', r'ev-plug-tesla', r'tesla', r'android', r'apple-', r'google', r'microsoft',
    r'facebook', r'twitter', r'github', r'linux', r'ubuntu', r'debian', r'windows', r'dolby', r'firefox', r'firebase',
    r'church', r'mosque', r'^cross$', r'christianity', r'jewish', r'menorah', r'^om$', r'^pray', r'torii', r'ankh',
    r'confucius', r'pentagram', r'yin-yang', r'christmas', r'candelabra', r'cannabis', r'^bong$', r'smoking',
    r'^poo', r'^xxx$', r'rating-\d', r'coffin', r'grave', r'ghost', r'pumpkin', r'^skull$', r'skull-crossbones',
    r'bomb', r'(^|-)swords?($|-)', r'^tank$', r'pistol', r'^gun', r'knife', r'chemical-weapon', r'axe-battle',
    r'hammer-sickle', r'mars-', r'^mars$', r'^venus$', r'venus-', r'^gender', r'dragon$', r'cookie-man',
    r'moustache', r'diaper', r'beer$', r'glass-cocktail', r'glass-gin', r'liquor', r'bottle-tonic-skull',
    r'emoticon', r'^sticker-smile$', r'flag-bitcoin', r'^peace$', r'^spy$', r'prison',
    r'death-star', r'deathly-hallows', r'ninja', r'pirate', r'wizard', r'handcuffs', r'^police', r'magazine-(pistol|rifle)',
    r'^nuke$', r'shield-sword', r'sword-cross', r'bow-arrow', r'liquor', r'wine', r'cigar', r'dance-', r'lipstick',
    r'halloween', r'egg-easter', r'robot-(angry|confused|dead|excited|happy|love)', r'domino-mask', r'hands-pray',
    r'^cross-', r'slot-machine', r'^cards', r'^dice', r'baby-face', r'cowboy', r'space-invaders', r'^kiss', r'bikini',
    r'pill-off', r'skull-crossbones', r'^stomach$', r'^toilet-paper$', r'^poop', r'^vomit', r'^beer', r'bottle-soda',
    r'^ghost', r'^zombie', r'^vampire', r'^devil', r'teddy-bear', r'^mustache', r'^gamepad', r'controller-classic', r'^power-socket-(au|ch|de|eu|fr|it|jp|uk|us)$'
]
AVOID_NAME_PATTERNS = [r'(^|-)off($|-)', r'^alpha-', r'^numeric-', r'^letter-', r'^number-', r'^square-f\d', r'^dice',
                       r'^play-card', r'^cards-playing', r'^rewind-', r'^percentage-\d', r'^clock-hour-',
                       r'^time-duration-', r'^multiplier-', r'^tallymark', r'^battery-\d0', r'^wifi-strength',
                       r'^network-strength', r'^signal-cellular', r'^hexagon-slice', r'^moon-wa', r'^format-',
                       r'^keyboard', r'^emoticon', r'^account-', r'^human-(?!wheelchair)', r'^face-', r'^ufo$', r'^alien',
                       r'poker', r'credit-card', r'^cash', r'^coin', r'moneybag', r'^receipt', r'discount', r'shopping',
                       r'^basket', r'wallet', r'tip-jar', r'pig-money', r'^gift', r'^ticket', r'french-fries',
                       r'-dollar$', r'-euro$', r'-pound$', r'-yen$', r'-yuan$', r'-rupee$', r'currency', r'^cards?-',
                       r'^casino', r'^slot-machine', r'^cart', r'^sale', r'^tag-', r'^tags-', r'^store',
                       # media / chat / text-formatting / UI glyphs that only match engineering words by coincidence
                       r'^music', r'^playlist', r'^player-', r'^album', r'^clef', r'^keyframe', r'^bubble-', r'^message',
                       r'^align-', r'^box-align-', r'^text-', r'^layout-align', r'^baseline', r'^letter-case', r'^list-',
                       r'^indent', r'^h-\d', r'^heading', r'^format-', r'^line-height', r'^pilcrow', r'^quote',
                       r'^help', r'^camera-selfie', r'^selfie', r'^mood-', r'^thumb-', r'^chat-', r'^comment',
                       r'^device-(tablet|mobile|desktop|watch|laptop|tv)-(bolt|cancel|check|code|cog|dollar|down|exclamation|'
                       r'minus|pause|pin|plus|question|search|share|star|up|x|off|heart)$', r'^devices-',
                       r'^calendar-(?!time$|stats$|event$|clock$|repeat$)', r'^clock-(?!24$|hour)', r'^bell-',
                       r'^(square|circle|triangle|hexagon|octagon|pentagon|rectangle|rosette|square-rounded)-(.*-)?'
                       r'(plus|minus|x|check|asterisk|percentage|key|forbid|heart|dot|letter-.*|number-.*)(-\d)?$',
                       # household fixtures and furniture
                       r'sconce', r'water-boiler', r'ceiling', r'floor-lamp', r'^lamps', r'desk-lamp', r'globe-light',
                       r'^bed', r'^sofa', r'wardrobe', r'dresser', r'bathtub', r'^shower', r'^toilet', r'^armchair',
                       r'scale-bathroom', r'lava-lamp', r'vanity', r'coach-lamp', r'^lamp-', r'outdoor-lamp',
                       r'^table-furniture', r'^chair', r'^stool', r'^mirror-rectangle', r'fridge-(alert|off|variant)',
                       r'^burger', r'^pizza', r'^cookie', r'^ice-cream', r'^candy', r'^lollipop', r'^cake', r'^donut',
                       r'^seatbelt', r'^bag-', r'^taxi', r'^hail$', r'^guitar', r'^nurse$', r'^ad-', r'^ad$',
                       r'^uhd$', r'^hdr$', r'^4k', r'^http-', r'^api-app', r'^menu-', r'^decimal', r'^error-404',
                       r'^parking$', r'^align', r'^military', r'^loader', r'^edit-circle', r'^exclamation',
                       r'garden-cart', r'rickshaw', r'rollercoaster', r'^sleigh', r'^camper', r'^caravan', r'unicycle',
                       r'skateboard', r'^horse', r'^carousel', r'^circus', r'^balloon', r'^cherry', r'^clubs', r'^spade',
                       r'^(?!map|home-map|map-marker).*-marker(-outline)?$', r'^fishbowl', r'^seat-', r'^dock-',
                       r'^ticket', r'^rewind', r'^backspace', r'^restart', r'^playstation', r'^arrange-',
                       r'^window-(close|closed|open|restore|maximize|minimize|shutter)', r'^safety-goggles$',
                       r'^explicit$', r'^credits$', r'^desk', r'^waterpolo', r'^water-polo', r'^hash$', r'^jetpack',
                       r'^rv-truck', r'^fast-forward', r'^vacuum-cleaner', r'^robot-vacuum', r'^robot-mower', r'^gavel',
                       r'^lighter$', r'^tabs$', r'^asset$', r'^marquee', r'^border-style', r'^disc-player',
                       r'^brightness-\d', r'^power-cycle', r'^ev-plug-ccs', r'^ev-plug-type', r'^periodic-table',
                       # glyphs too trivial to read as a pictogram on their own
                       r'^line$', r'^minus-vertical$', r'^minus$', r'^slash$', r'^backslash$', r'^point$', r'^tilde$',
                       r'^separator', r'^power-on$', r'^power-off$', r'^stroke-straight$', r'^equal$', r'^period$', r'^space$', r'^spaces$', r'^x$', r'^check$', r'^plus$']
NEVER_RE = re.compile('|'.join(NEVER_NAME_PATTERNS))
# modifier suffixes of systematic icon families: whimsical / commercial ones never act as theme glyphs
BAD_MODIFIER_RE = re.compile(r'(^|-)(heart|star|smile|sad|dollar|discount|bitcoin|euro|pound|yen|yuan|rupee|music|love|'
                             r'angry|confused|dead|excited|happy|cancel|question|x|remove|minus|off|pause|edit|plus|'
                             r'account|ai|sparkle|spark|percent|favorite|star-outline)($|-)')
GOOD_MODIFIERS = ('', 'outline', 'variant', 'cog', 'bolt', 'check', 'search', 'code', 'scan', 'settings', 'sync', 'network',
                  'share', 'export', 'import', 'up', 'down', 'signal', 'marker', 'pin', 'clock', 'lock', 'alert')


def modifier_rank(suffix):
    toks = [t for t in suffix.split('-') if t]
    if not toks:
        return 0
    return 1 + max((GOOD_MODIFIERS.index(t) if t in GOOD_MODIFIERS else len(GOOD_MODIFIERS)) for t in toks)


# prior on how often a glyph family yields a meaningful engineering pictogram (selection only, not q)
TABLER_CATEGORY_PRIOR = {'Arrows': 0.4, 'Text': 0.3, 'Currencies': 0.3, 'Communication': 0.5, 'Document': 0.7,
                         'E-commerce': 0.6, 'Games': 0.5, 'Sport': 0.6, 'Animals': 0.8, 'Media': 0.6, 'Mood': 0.3,
                         'Extensions': 0.5, 'Version control': 0.9, 'Food': 0.75}
MDI_TAG_PRIOR = {'Arrow': 0.4, 'Text / Content / Format': 0.3, 'Files / Folders': 0.6, 'Account / User': 0.5,
                 'Home Automation': 0.75, 'Food / Drink': 0.75, 'Date / Time': 0.7, 'Vector': 0.6, 'Math': 0.8,
                 'Banking': 0.4, 'Currency': 0.3, 'Shopping': 0.4, 'Social Media': 0.4, 'Cellphone / Phone': 0.7,
                 'Form': 0.6, 'Tooltip': 0.4, 'Arrange': 0.5, 'Edit / Modify': 0.7, 'Music': 0.6, 'Video / Movie': 0.7,
                 'People / Family': 0.6, 'Notification': 0.7, 'Sport': 0.7, 'Clothing': 0.6, 'Gaming / RPG': 0.5}


BADGE_GOOD = {'cog', 'bolt', 'check', 'search', 'code', 'up', 'down', 'share', 'pin', 'spark', 'scan', 'sync', 'lock',
              'clock', 'settings', 'network', 'alert', 'marker', 'export', 'import', 'arrow', 'auto', 'variant', 'outline',
              'box', 'circle', 'multiple'}
BADGE_BAD = {'plus', 'minus', 'x', 'cancel', 'question', 'exclamation', 'heart', 'star', 'dollar', 'pause', 'off', 'remove',
             'edit', 'smile', 'sad', 'ai', 'percent', 'discount', 'euro', 'pound', 'yen', 'yuan', 'rupee', 'bitcoin',
             'sparkle', 'refresh', 'cancel', 'forbid', 'dots', 'move', 'link', 'hand', 'user', 'account', 'music', 'play',
             'stop', 'record', 'empty', 'full', 'open', 'closed', 'left', 'right', 'top', 'bottom', 'horizontal',
             'vertical', 'chevron', 'small', 'big', 'thin', 'thick', 'bold'}
BASE_NAMES = set()


UI_BASES = set('''user users mail message message-2 message-circle folder file files phone device-mobile device-tablet
device-desktop device-laptop device-watch device-imac device-ipad devices calendar clock bell browser app-window table layout
pointer pencil basket shopping-cart shopping-bag credit-card tag tags bookmark note notes clipboard id address-book receipt
wallet cash coin ticket flag photo video movie music playlist headphones keyboard mouse archive inbox category apps sticker
mood heart star thumb book books palette world-www sitemap cast subtitles text pennant forms location map-pin pin
square-rounded account card cards comment chat email'''.split())
SOFT_BASES = set('eye zoom adjustments filter shield lock navigation settings cloud world map home building database server'.split())
BADGE_WORDS = None


def demote_badge_variants(icons, rejected):
    """Badge variants (base glyph + small modifier badge, e.g. user-bolt, droplet-cancel) only ever match engineering
    terms by coincidence: move UI-base variants and negative/whimsical badges to the avoid tier.  Compounds such as
    photo-sensor or heart-pulse are not badge variants and stay usable."""
    words = BADGE_GOOD | BADGE_BAD
    for ic in icons:
        if ic.tier != 0:
            continue
        toks = ic.name.split('-')
        for cut in range(len(toks) - 1, 0, -1):
            base = '-'.join(toks[:cut])
            if base not in BASE_NAMES:
                continue
            badge = toks[cut:]
            if not all(t in words or t.isdigit() for t in badge):
                break
            if all(t in ('outline', 'variant') or t.isdigit() for t in badge):
                break
            bad = any(t in BADGE_BAD for t in badge)
            if bad or (base in UI_BASES and base not in SOFT_BASES):
                ic.tier = 1
                rejected['badge variant demoted to avoid tier'] += 1
            break


def prior(icon):
    if icon.src == 't':
        p = TABLER_CATEGORY_PRIOR.get(icon.cat, 1.0)
    else:
        p = min([MDI_TAG_PRIOR.get(t, 1.0) for t in icon.tags] or [1.0])
    toks = icon.name.split('-')
    if len(toks) >= 2:
        # systematic "base + badge" variant (e.g. droplet-cancel, server-minus): a weaker pictogram than a distinct glyph
        for cut in (1, 2):
            if len(toks) > cut and '-'.join(toks[:-cut]) in BASE_NAMES:
                badge = toks[-cut:]
                if any(t in BADGE_BAD for t in badge):
                    p *= 0.45
                elif not all(t in BADGE_GOOD or t.isdigit() for t in badge):
                    p *= 0.8
                elif not all(t in ('variant', 'outline') or t.isdigit() for t in badge):
                    p *= 0.75
                break
    return p
AVOID_RE = re.compile('|'.join(AVOID_NAME_PATTERNS))

STEM_KEEP = {'lens', 'gas', 'bus', 'series', 'species', 'news', 'physics', 'chassis', 'analysis', 'diagnosis',
             'synthesis', 'basis', 'axis', 'genesis', 'canvas', 'atlas', 'plus', 'minus', 'status', 'campus',
             'radius', 'virus', 'bonus', 'iris', 'mars', 'venus', 'sirius', 'thesis', 'osmosis', 'electrolysis',
             'dialysis', 'hemodialysis', 'kinematics', 'dynamics', 'mechanics', 'optics', 'electronics',
             'photonics', 'robotics', 'acoustics', 'hydraulics', 'aerodynamics', 'avionics', 'logistics',
             'ceramics', 'plastics', 'metrics', 'statistics', 'mathematics', 'genomics', 'diagnostics',
             'cryogenics', 'textiles', 'ethics', 'graphics', 'haptics', 'prosthetics', 'pneumatics', 'glass',
             'mass', 'class', 'process', 'access', 'stress', 'press', 'boss', 'loss', 'moss', 'cross', 'gauss',
             'compass', 'biomass', 'bypass', 'overpass', 'grass', 'brass', 'chess', 'harness', 'thickness',
             'tightness', 'fitness', 'wireless', 'stainless', 'brushless', 'sensorless', 'gearless', 'seamless',
             'trenchless', 'driverless', 'always', 'perhaps', 'its', 'this', 'has', 'was', 'is', 'us', 'yes',
             'pages', 'kiwis', 'atlas', 'jupiter', 'glasses', 'goggles', 'sunglasses', 'means'}


def stem(word):
    w = word.lower()
    if len(w) <= 3 or w in STEM_KEEP:
        return w
    if w.endswith('ics') and w[:-1] in STEM_KEEP:
        return w
    if w.endswith('ies') and len(w) > 4:
        return w[:-3] + 'y'
    if w.endswith('sses'):
        return w[:-2]
    if w.endswith(('ches', 'shes', 'xes', 'zes')) and len(w) > 5:
        return w[:-2]
    if w.endswith('s') and not w.endswith(('ss', 'us', 'is', 'ys')):
        return w[:-1]
    return w


def norm_words(text):
    """Lower-case words; hyphens, slashes and punctuation split words."""
    text = (text or '').lower().replace('\u2013', ' ').replace('\u2014', ' ').replace('&', ' and ')
    text = text.replace('x-ray', 'xray ').replace('x ray', 'xray')
    return re.findall(r"[a-z0-9]+(?:'[a-z]+)?", text)


def norm_key(phrase):
    return ' '.join(stem(w) for w in norm_words(phrase))


# ---- icon loading --------------------------------------------------------------------------
class Icon:
    __slots__ = ('key', 'name', 'src', 'cat', 'tags', 'name_tokens', 'alias_tokens', 'tag_tokens',
                 'markup', 'tier', 'variant', 'meaningful')

    def __init__(self, name, src, cat, tags, aliases, markup):
        self.key = src + ':' + name
        self.name = name
        self.src = src
        self.cat = cat
        self.tags = tags
        toks = [t for t in name.split('-') if t]
        self.name_tokens = {stem(t) for t in toks if not t.isdigit()}
        self.meaningful = [stem(t) for t in toks if not t.isdigit() and t not in ('outline', 'variant', 'alt')]
        self.alias_tokens = set()
        for a in aliases:
            for t in a.split('-'):
                if t and not t.isdigit():
                    self.alias_tokens.add(stem(t))
        self.alias_tokens -= self.name_tokens
        self.tag_tokens = set()
        for tag in tags:
            for t in norm_words(tag):
                if not t.isdigit():
                    self.tag_tokens.add(stem(t))
        self.tag_tokens -= self.name_tokens
        self.markup = markup
        self.variant = bool(re.search(r'-(\d|variant|alt|outline)$', name)) or bool(re.search(r'-\d-', name))
        self.tier = 0


ELEMENT_RE = re.compile(r'<(' + '|'.join(ELEMENTS) + r')\b([^<>]*?)/?>(?:</\1>)?', re.S)
ATTR_RE = re.compile(r'([a-zA-Z_:][-a-zA-Z0-9_:.]*)\s*=\s*"([^"]*)"')


def clean_markup(inner):
    """Return canonical inner markup with geometry attributes only, or None if anything else is present."""
    out = []
    pos = 0
    for m in ELEMENT_RE.finditer(inner):
        if inner[pos:m.start()].strip():
            return None
        pos = m.end()
        attrs = ATTR_RE.findall(m.group(2))
        if not attrs:
            return None
        for k, _ in attrs:
            if k not in GEOMETRY_ATTRS:
                return None
        rest = ATTR_RE.sub('', m.group(2)).strip().rstrip('/').strip()
        if rest:
            return None
        parts = []
        for k, v in attrs:
            v = re.sub(r'\s+', ' ', v.strip())
            if not re.fullmatch(r'[-0-9.eE,MmLlHhVvCcSsQqTtAaZz\s]*', v):
                return None
            parts.append('%s="%s"' % (k, v))
        out.append('<%s %s/>' % (m.group(1), ' '.join(parts)))
    if inner[pos:].strip() or not out:
        return None
    return ''.join(out)


def load_tabler(directory, rejected):
    icons = []
    for fn in sorted(os.listdir(directory)):
        if not fn.endswith('.svg'):
            continue
        name = fn[:-4]
        with open(os.path.join(directory, fn), encoding='utf-8') as fh:
            text = fh.read()
        m = re.search(r'<!--(.*?)-->', text, re.S)
        meta = m.group(1) if m else ''
        cm = re.search(r'category:\s*(.+)', meta)
        cat = cm.group(1).strip().strip('"\'') if cm else ''
        tm = re.search(r'tags:\s*\[(.*?)\]', meta, re.S)
        tags = [t.strip().strip('"\'') for t in tm.group(1).split(',')] if tm else []
        body = re.sub(r'<!--.*?-->', '', text, flags=re.S)
        sm = re.search(r'<svg\b[^>]*>(.*)</svg>', body, re.S)
        markup = clean_markup(sm.group(1)) if sm else None
        if markup is None:
            rejected['tabler: non-geometry markup'] += 1
            continue
        icon = Icon(name, 't', cat, tags, [], markup)
        if cat in TABLER_NEVER_CATEGORIES or NEVER_RE.search(name):
            icon.tier = 9
        elif cat in TABLER_AVOID_CATEGORIES or AVOID_RE.search(name):
            icon.tier = 1
        icons.append(icon)
    return icons


def load_mdi(directory, rejected, taken_names):
    meta_path = os.path.join(directory, 'meta.json')
    svg_dir = os.path.join(directory, 'svg')
    if not (os.path.isfile(meta_path) and os.path.isdir(svg_dir)):
        return []
    with open(meta_path, encoding='utf-8') as fh:
        meta = json.load(fh)
    icons = []
    for item in sorted(meta, key=lambda i: i['name']):
        name = item['name']
        tags = item.get('tags') or []
        if item.get('deprecated'):
            rejected['mdi: deprecated'] += 1
            continue
        if name in taken_names:
            rejected['mdi: same name as a Tabler icon'] += 1
            continue
        path = os.path.join(svg_dir, name + '.svg')
        if not os.path.isfile(path):
            rejected['mdi: svg missing'] += 1
            continue
        with open(path, encoding='utf-8') as fh:
            text = fh.read()
        sm = re.search(r'<svg\b[^>]*>(.*)</svg>', text, re.S)
        markup = clean_markup(sm.group(1)) if sm else None
        if markup is None:
            rejected['mdi: non-geometry markup'] += 1
            continue
        aliases = item.get('aliases') or []
        icon = Icon(name, 'm', ', '.join(tags), tags, aliases, markup)
        if any(t in MDI_NEVER_TAGS for t in tags) or NEVER_RE.search(name) or any(NEVER_RE.search(a) for a in aliases):
            icon.tier = 9
        elif any(t in MDI_AVOID_TAGS for t in tags) or AVOID_RE.search(name):
            icon.tier = 1
        icons.append(icon)
    return icons


# ---- synonym tables ------------------------------------------------------------------------
def parse_targets(spec):
    out = []
    for tok in spec.split():
        if ':' in tok:
            name, w = tok.rsplit(':', 1)
            w = float(w)
        else:
            name, w = tok, 1.0
        if w > 0:
            out.append((name, w))
    return out


def load_synonyms():
    def no_dupes(pairs):
        seen = {}
        for k, v in pairs:
            if k in seen:
                raise SystemExit('synonyms.json: duplicate key %r' % k)
            seen[k] = v
        return seen
    with open(SYNONYMS, encoding='utf-8') as fh:
        raw = json.load(fh, object_pairs_hook=no_dupes)
    en = {}
    for k, v in raw['en'].items():
        nk = norm_key(k)
        targets = parse_targets(v)
        if nk in en:   # e.g. "x-ray" and "x ray" normalise identically: merge
            merged = dict(en[nk])
            for n, w in targets:
                merged[n] = max(merged.get(n, 0), w)
            targets = sorted(merged.items())
        en[nk] = targets
    names = {}
    for k, v in raw['names'].items():
        names[norm_key(k)] = [t.strip() for t in v.split('|') if t.strip()]
    zh = {k: [t.strip() for t in v.split('|') if t.strip()] for k, v in raw['zh'].items()}
    category = {k: [t.strip() for t in v.split('|') if t.strip()] for k, v in raw['category'].items()}
    themes = {k: v.split() for k, v in raw.get('themes', {}).items()}
    families = {k: v.split() for k, v in raw.get('theme_prefixes', {}).items()}
    families = {k: (v, raw.get('theme_tags', {}).get(k, [])) for k, v in families.items()}
    generic = {stem(k): float(v) for k, v in raw['generic'].items()}
    stop = {w for w in raw['stop']}
    summary_stop = {stem(w) for w in raw.get('summary_stop', [])} | {w for w in raw.get('summary_stop', [])}
    return en, names, zh, category, themes, families, generic, stop, summary_stop


# ---- scoring -------------------------------------------------------------------------------
class Matcher:
    def __init__(self, icons, en, names, generic, stop):
        self.icons = icons
        self.en, self.names, self.generic, self.stop = en, names, generic, stop
        self.full = {}
        self.tok = defaultdict(list)
        for i, ic in enumerate(icons):
            self.full[ic.name] = i
            for t in ic.name_tokens:
                self.tok[t].append((i, 'name'))
            for t in ic.alias_tokens:
                self.tok[t].append((i, 'alias'))
            for t in ic.tag_tokens:
                self.tok[t].append((i, 'tag'))
        self.max_n = max([len(k.split()) for k in list(en) + list(names)] + [1])
        self.cache = {}
        self.unknown_targets = Counter()

    def target_matches(self, target, tw):
        """icon index -> (strength, is_name_kind, matched_token or None, full)"""
        res = {}
        if target in self.full:
            res[self.full[target]] = (tw * M_FULL, True, None, True)
            if '-' in target:
                return res
        if '-' in target:
            self.unknown_targets[target] += 1
            return res
        st = stem(target)
        if st in self.full and self.full[st] not in res:
            res[self.full[st]] = (tw * M_FULL, True, None, True)
        for i, kind in self.tok.get(st, ()):
            if i in res and res[i][3]:
                continue
            ic = self.icons[i]
            if kind == 'name':
                s, nk, mt = tw * M_NAME, True, st
            elif kind == 'alias':
                s, nk, mt = tw * M_ALIAS, True, None
            else:
                s, nk, mt = tw * (M_MDI_TAG if ic.src == 'm' else M_TAG), False, None
            prev = res.get(i)
            if prev is None or s > prev[0]:
                res[i] = (s, nk, mt, False)
        return res

    def term_matches(self, term):
        """Per origin term: icon -> (name_strength, tag_strength, tokens, full)."""
        if term in self.cache:
            return self.cache[term]
        if term in self.en:
            targets = self.en[term]
        else:
            targets = [(term, 1.0)]
        agg = {}
        for target, tw in targets:
            for i, (s, nk, mt, full) in self.target_matches(target, tw).items():
                ns, ts, toks, fl = agg.get(i, (0.0, 0.0, frozenset(), False))
                if nk:
                    if s > ns:
                        ns = s
                    if mt:
                        toks = toks | {mt}
                    fl = fl or full
                else:
                    ts = max(ts, s)
                agg[i] = (ns, ts, toks, fl)
        self.cache[term] = agg
        return agg

    def known(self, term):
        return term in self.en or term in self.tok or term in self.full


def phrase_terms(words, en, names, stop, max_n):
    """Find table phrases (longest first) and remaining unigrams. Returns list of (key, kind, factor)."""
    stems = [stem(w) for w in words]
    n = len(stems)
    covered = [0] * n
    found = []
    for size in range(min(max_n, n), 1, -1):
        for i in range(0, n - size + 1):
            key = ' '.join(stems[i:i + size])
            if key in names and not all(covered[i:i + size]):
                found.append((key, 'name', 1.0))
                for j in range(i, i + size):
                    covered[j] = max(covered[j], 2)
            elif key in en and not all(c == 2 for c in covered[i:i + size]):
                inner = all(c >= 1 for c in covered[i:i + size])
                found.append((key, 'en', COVERED_UNIGRAM if inner else 1.0))
                for j in range(i, i + size):
                    covered[j] = max(covered[j], 1)
    for i, s in enumerate(stems):
        if s in stop or words[i] in stop or s.isdigit() and s not in names and s not in en:
            continue
        if covered[i] == 2:
            continue
        factor = COVERED_UNIGRAM if covered[i] else 1.0
        if s in names and not covered[i]:
            found.append((s, 'name', 1.0))
        else:
            found.append((s, 'word', factor))
    return found


class ProjectTerms:
    def __init__(self, en, names, zh, category, generic, stop, summary_stop, matcher):
        self.en, self.names, self.zh, self.category = en, names, zh, category
        self.generic, self.stop, self.summary_stop = generic, stop, summary_stop
        self.m = matcher
        self.zh_keys = sorted(zh, key=lambda k: (-len(k), k))
        self.name_hits = Counter()

    def expand(self, phrase):
        """English phrase from a table value -> list of origin term keys."""
        words = norm_words(phrase)
        key = norm_key(phrase)
        if key in self.en or key in self.m.full:
            return [key]
        out = []
        for k, kind, f in phrase_terms(words, self.en, {}, self.stop, self.m.max_n):
            out.append(k)
        return out

    def add_text(self, acc, text, weight, summary=False, track_names=False):
        local = {}
        for key, kind, factor in phrase_terms(norm_words(text), self.en, self.names, self.stop, self.m.max_n):
            if summary and (key in self.summary_stop or key in self.generic):
                continue
            if kind == 'name':
                if track_names:
                    self.name_hits[key] += 1
                for ph in self.names[key]:
                    for k in self.expand(ph):
                        local[k] = max(local.get(k, 0), weight * factor)
                continue
            if kind == 'word' and not self.m.known(key):
                continue
            if summary and key not in self.en:
                continue
            w = weight * factor * self.generic.get(key, 1.0)
            local[key] = max(local.get(key, 0), w)
        for k, w in local.items():
            acc[k] = acc.get(k, 0) + w

    def add_zh(self, acc, text, weight):
        text = text or ''
        used = [False] * len(text)
        local = {}
        for key in self.zh_keys:
            start = 0
            while True:
                i = text.find(key, start)
                if i < 0:
                    break
                if not any(used[i:i + len(key)]):
                    for j in range(i, i + len(key)):
                        used[j] = True
                    for ph in self.zh[key]:
                        for k in self.expand(ph):
                            w = weight * self.generic.get(k, 1.0)
                            local[k] = max(local.get(k, 0), w)
                start = i + 1
        for k, w in local.items():
            acc[k] = acc.get(k, 0) + w

    def project_terms(self, p):
        acc = {}
        self.add_text(acc, p.get('titleEn') or '', W_TITLE, track_names=True)
        self.add_zh(acc, p.get('title') or '', W_ZH)
        if p.get('subcategoryTitleEn'):
            self.add_text(acc, p['subcategoryTitleEn'], W_SUB)
        diag = p.get('diagram') or {}
        if isinstance(diag, dict):
            if diag.get('type'):
                self.add_text(acc, str(diag['type']).replace('-', ' '), W_DIAG_TYPE)
            labels = diag.get('labelsEn') or []
            if labels:
                self.add_text(acc, ' . '.join(str(x) for x in labels[:8]), W_DIAG_LABEL, summary=True)
        for ph in self.category.get(p.get('category'), []):
            for k in self.expand(ph):
                acc[k] = acc.get(k, 0) + W_CAT * self.generic.get(k, 1.0)
        if p.get('summaryEn'):
            self.add_text(acc, p['summaryEn'], W_SUMMARY, summary=True)
        return acc


def decayed(values):
    return sum(v * DECAY ** k for k, v in enumerate(sorted(values, reverse=True)))


def score_project(terms, matcher, theme=None, parts=None):
    """Return {icon_index: raw_score}.  theme: {icon_index: bonus} for the project's category.
    parts (optional dict) receives icon_index -> (name_score, tag_score, theme_score)."""
    name_part = defaultdict(list)
    tag_part = defaultdict(list)
    tokens = defaultdict(set)
    full = set()
    for term, w in terms.items():
        for i, (ns, ts, toks, fl) in matcher.term_matches(term).items():
            if ns > 0:
                name_part[i].append(w * ns)
                tokens[i] |= toks
                if fl:
                    full.add(i)
            elif ts > 0:
                tag_part[i].append(w * ts)
    scores = {}
    icons = matcher.icons
    theme = theme or {}
    for i in set(name_part) | set(tag_part) | set(theme):
        ic = icons[i]
        if i in full:
            cov = 1.0
        else:
            mean = ic.meaningful or list(ic.name_tokens) or ['?']
            cov = sum(1 for t in mean if t in tokens[i]) / len(mean)
        ns = decayed(name_part.get(i, ())) * (COV_BASE + (1 - COV_BASE) * cov)
        ts = min(decayed(tag_part.get(i, ())), TAG_CAP)
        th = theme.get(i, 0.0)
        raw = ns + ts + th
        if ic.variant:
            raw *= VARIANT_FACTOR
        if raw > 0:
            scores[i] = raw
            if parts is not None:
                parts[i] = (ns, ts, th, 0.0)
    return scores


def effective(parts, icon):
    """Selection score.  The MDI handicap applies to the match evidence, not to the category theme evidence,
    so that a thematic MDI glyph can still beat coincidental token matches of leftover Tabler glyphs."""
    ns, ts, th, inh = parts
    e = (ns + ts) * prior(icon) * (MDI_FACTOR if icon.src == 'm' else 1.0) + th + inh
    if icon.variant:
        e *= VARIANT_FACTOR
    return e


def q_of(raw):
    return round(1.0 - math.exp(-raw / Q_SCALE), 2)


# ---- assignment ----------------------------------------------------------------------------
def badge_families(icons):
    """base glyph index -> [variant indices] for systematic variants such as airplane-cog, droplet-bolt."""
    by_name = {ic.name: i for i, ic in enumerate(icons)}
    fam = defaultdict(list)
    for i, ic in enumerate(icons):
        if ic.tier != 0:
            continue
        toks = ic.name.split('-')
        for cut in range(len(toks) - 1, 0, -1):
            base = '-'.join(toks[:cut])
            if base in by_name and icons[by_name[base]].src == ic.src:
                if not all(t in BADGE_GOOD or t in BADGE_BAD or t.isdigit() for t in toks[cut:]):
                    break     # a compound such as car-fan has its own meaning; only badge variants inherit
                if not BAD_MODIFIER_RE.search('-'.join(toks[cut:])) or not re.search(
                        r'(^|-)(heart|star|smile|sad|dollar|discount|bitcoin|euro|pound|yen|yuan|rupee|music|love|'
                        r'angry|confused|dead|excited|happy|off|account|percent|favorite)($|-)', '-'.join(toks[cut:])):
                    fam[by_name[base]].append(i)
                break
    for b in fam:
        fam[b].sort(key=lambda i: (modifier_rank(icons[i].name[len(icons[b].name):]), icons[i].name))
    return fam


def inherit_from_families(all_scores, all_parts, icons):
    """Give each project's strongest concept glyphs' badge variants a discounted share of the base score, so a
    project whose concept glyphs are all taken still gets a glyph derived from its concept."""
    fam = badge_families(icons)
    for pi, scores in enumerate(all_scores):
        top = sorted(((all_parts[pi][i][0] * (MDI_FACTOR if icons[i].src == 'm' else 1.0), i) for i in scores
                      if icons[i].tier == 0 and all_parts[pi][i][0] > 0), reverse=True)[:INHERIT_TOP]
        for e, b in top:
            for rank, v in enumerate(fam.get(b, ())):
                inh = e * INHERIT_SHARE * (1 - 0.3 * rank / max(1, len(fam[b]) - 1))
                ns, ts, th, old = all_parts[pi].get(v, (0.0, 0.0, 0.0, 0.0))
                if inh > old:
                    all_parts[pi][v] = (ns, ts, th, inh)
                    all_scores[pi][v] = max(all_scores[pi].get(v, 0.0), ns + ts + th + inh)


NEUTRAL_GEOMETRY = ('cube cylinder sphere cone pyramid prism frustum diabolo octahedron icosahedron hemisphere '
                    'irregular-polyhedron hexagonal-prism hexagonal-pyramid rectangular-prism triangle-square-circle '
                    'cube-unfolded cube-3d-sphere perspective polygon vector-triangle box-model box-model-2 shape '
                    'shape-2 shape-3 square-rotated octagon pentagon hexagon triangle triangles squares circles '
                    'circle-dashed circle-dotted cone-2 sphere-2 cube-send blob blob-dashed oval oval-vertical '
                    'rectangle rectangle-vertical capsule capsule-horizontal hexagons squares-diagonal grid-dots '
                    'circle-half circle-half-2 circle-half-vertical square-half border-outer border-corners').split()


def is_flagship(project):
    pid = str(project.get('id', ''))
    return not re.fullmatch(r'[a-d]\d{3}', pid) and not pid.startswith('v11-')


def assign(projects, all_scores, all_parts, icons, category_pools, neutral_pool, neutral_geometry):
    n = len(projects)
    boost = [FLAGSHIP_BOOST if is_flagship(p) else 1.0 for p in projects]
    cands = []
    for pi in range(n):
        lst = [(effective(all_parts[pi][i], icons[i]) * boost[pi], r, i) for i, r in all_scores[pi].items()
               if icons[i].tier == 0]
        lst = [x for x in lst if x[0] >= MIN_EFF]
        lst.sort(key=lambda x: (-x[0], -x[1], icons[x[2]].key))
        cands.append(lst[:CANDIDATES_PER_PROJECT])
    pairs = [(e, r, pi, i) for pi in range(n) for (e, r, i) in cands[pi]]
    pairs.sort(key=lambda x: (-x[0], -x[1], x[2], icons[x[3]].key))
    owner = {}
    chosen = [None] * n
    for e, r, pi, i in pairs:
        if chosen[pi] is not None or i in owner:
            continue
        chosen[pi] = i
        owner[i] = pi

    eff_of = [dict((i, e) for e, r, i in cands[pi]) for pi in range(n)]

    def eff_for(pi, i):
        if i is None:
            return 0.0
        e = eff_of[pi].get(i)
        if e is not None:
            return e
        r = all_scores[pi].get(i, 0.0)
        return effective(all_parts[pi][i], icons[i]) * boost[pi] if r > 0 else -1.0

    # local improvement (ejection chains of depth <= 2): B takes X from A; A moves to Y, which is either free
    # or taken from C, who then moves to a free Z.  Applied only when the summed effective score rises.
    def first_free(pi, banned, cur_free):
        for k, (e, r, i) in enumerate(cands[pi]):
            if k >= CHAIN_SCAN:
                break
            if i in banned:
                continue
            if i not in owner or i == cur_free:
                return e, i
        return None

    swaps = 0
    for _round in range(4):
        changed = False
        order = sorted(range(n), key=lambda p: (eff_for(p, chosen[p]), p))
        for b in order:
            cur_b = chosen[b]
            s_b = eff_for(b, cur_b)
            best_gain, plan = SWAP_MARGIN, None
            for kx, (e_bx, r_bx, x) in enumerate(cands[b]):
                if e_bx <= s_b + SWAP_MARGIN or kx >= CHAIN_BRANCH:
                    break
                a = owner.get(x)
                if a is None:
                    gain = e_bx - s_b
                    if gain > best_gain:
                        best_gain, plan = gain, [(b, x)]
                    break
                if a == b:
                    break
                s_ax = eff_for(a, x)
                for ky, (e_ay, r_ay, y) in enumerate(cands[a]):
                    if ky >= CHAIN_BRANCH or e_ay - s_ax + e_bx - s_b <= best_gain:
                        break
                    if y == x:
                        continue
                    c = owner.get(y)
                    if c is None or y == cur_b:
                        gain = e_bx - s_b + e_ay - s_ax
                        if gain > best_gain:
                            best_gain, plan = gain, [(b, x), (a, y)]
                        break
                    if c == b:
                        continue
                    alt = first_free(c, (x, y), cur_b)
                    if alt is None:
                        continue
                    gain = e_bx - s_b + e_ay - s_ax + alt[0] - eff_for(c, y)
                    if gain > best_gain:
                        best_gain, plan = gain, [(b, x), (a, y), (c, alt[1])]
            if plan:
                for pj, _ in plan:
                    if chosen[pj] is not None and owner.get(chosen[pj]) == pj:
                        del owner[chosen[pj]]
                for pj, ic in plan:
                    chosen[pj] = ic
                    owner[ic] = pj
                swaps += 1
                changed = True
        if not changed:
            break

    fallback = Counter()
    for pi in range(n):
        if chosen[pi] is not None:
            continue
        pick = next((i for i in category_pools.get(projects[pi].get('category'), []) if i not in owner), None)
        how = 'category pool'
        if pick is None:
            pick = next((i for i in neutral_pool if i not in owner), None)
            how = 'neutral pool'
        if pick is None:
            full = sorted(((r, i) for i, r in all_scores[pi].items() if icons[i].tier == 1),
                          key=lambda x: (-x[0], icons[x[1]].key))
            pick = next((i for r, i in full if i not in owner), None)
            how = 'avoid tier (last resort)'
        if pick is None:
            raise SystemExit('ran out of icons for ' + projects[pi]['id'])
        chosen[pi] = pick
        owner[pick] = pi
        fallback[how] += 1
    # tail rule: a weak pick with no concept or theme evidence is a coincidental pictogram (e.g. a sleigh for an
    # aircraft topic); replace it by an unused neutral geometric glyph, which does not mislead.
    neutral_set = set(neutral_geometry)
    for pi in sorted(range(n), key=lambda p: (eff_for(p, chosen[p]), p)):
        i = chosen[pi]
        parts = all_parts[pi].get(i, (0.0, 0.0, 0.0, 0.0))
        if parts[0] + parts[1] >= TAIL_EFF or parts[2] >= 0.12 or parts[3] > 0 or i in neutral_set:
            continue
        pick = next((g for g in neutral_geometry if g not in owner), None)
        if pick is None:
            break
        del owner[i]
        chosen[pi] = pick
        owner[pick] = pi
        fallback['neutral geometry (tail)'] += 1
    return chosen, swaps, fallback


# ---- outputs -------------------------------------------------------------------------------
def find_dir(cli, env, candidates, probe):
    for c in [cli, os.environ.get(env)] + candidates:
        if c and os.path.exists(os.path.join(c, probe)):
            return c
    return None


def git_rev(path):
    try:
        d = path
        for _ in range(5):
            head = os.path.join(d, '.git', 'HEAD')
            if os.path.isfile(head):
                ref = open(head).read().strip()
                if ref.startswith('ref:'):
                    rp = os.path.join(d, '.git', ref.split(' ', 1)[1])
                    if os.path.isfile(rp):
                        return open(rp).read().strip()[:12]
                    packed = os.path.join(d, '.git', 'packed-refs')
                    if os.path.isfile(packed):
                        for line in open(packed):
                            if line.strip().endswith(ref.split(' ', 1)[1]):
                                return line.split()[0][:12]
                return ref[:12]
            d = os.path.dirname(d)
    except OSError:
        pass
    return 'unknown'


def write_licenses(tabler_root, mdi_root, used_counts, revs):
    tabler_license = ''
    lp = os.path.join(tabler_root, 'LICENSE') if tabler_root else None
    if lp and os.path.isfile(lp):
        tabler_license = open(lp, encoding='utf-8').read().strip()
    apache = ''
    for cand in [os.path.join(mdi_root or '', 'LICENSE-APACHE'), '/usr/share/common-licenses/Apache-2.0']:
        if cand and os.path.isfile(cand):
            apache = open(cand, encoding='utf-8').read().rstrip()
            break
    if not apache and os.path.isfile(OUT_LICENSES):
        # regenerating on a machine without a local copy: keep the full text written previously
        prev = open(OUT_LICENSES, encoding='utf-8').read()
        m = re.search(r'### Full text of the Apache License, Version 2\.0\n\n```\n(.*?)\n```', prev, re.S)
        if m:
            apache = m.group(1)
    mdi_notice = ''
    if mdi_root and os.path.isfile(os.path.join(mdi_root, 'LICENSE')):
        mdi_notice = open(os.path.join(mdi_root, 'LICENSE'), encoding='utf-8').read().strip()
    lines = [
        '# Project icon licenses',
        '',
        'The 2,066 project glyphs in `data/project-icons.json` (rendered by `project-icons.js`) are unmodified',
        'vector geometry from two open-source icon sets. **The icons were selected and assigned to projects by',
        'the MacGyver Engineering Academy** (`tools/icons-v12/assign_icons.py`); neither icon project endorses',
        'the academy. Only the inner path geometry is stored; the academy\'s renderer supplies the SVG wrapper,',
        'stroke width and colour. No brand or logo icons are used.',
        '',
        '| Source | Glyphs used | License | Upstream revision |',
        '| --- | ---: | --- | --- |',
        '| [Tabler Icons](https://tabler.io/icons) (outline set) | %d | MIT | `%s` |' % (used_counts.get('t', 0), revs.get('t', 'unknown')),
        '| [Material Design Icons](https://pictogrammers.com/library/mdi/) by Pictogrammers | %d | Apache-2.0 | `%s` |' % (used_counts.get('m', 0), revs.get('m', 'unknown')),
        '',
        '## Tabler Icons — MIT License',
        '',
        'Source: https://github.com/tabler/tabler-icons',
        '',
        '```',
        tabler_license or 'MIT License\n\nCopyright (c) 2020-2026 Paweł Kuna\n\n(see https://github.com/tabler/tabler-icons/blob/main/LICENSE)',
        '```',
        '',
        '## Material Design Icons (Pictogrammers) — Apache License 2.0',
        '',
        'Source: https://github.com/Templarian/MaterialDesign-SVG',
        '',
        'Copyright (c) Pictogrammers and the Material Design Icons contributors. Licensed under the Apache',
        'License, Version 2.0 (the "License"); you may not use these files except in compliance with the',
        'License. You may obtain a copy of the License at https://www.apache.org/licenses/LICENSE-2.0.',
        'Unless required by applicable law or agreed to in writing, software distributed under the License',
        'is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or',
        'implied. The academy did not modify the path data of any MDI glyph.',
        '',
    ]
    if mdi_notice:
        lines += ['Upstream notice (`LICENSE` in MaterialDesign-SVG):', '', '```', mdi_notice, '```', '']
    if apache:
        lines += ['### Full text of the Apache License, Version 2.0', '', '```', apache, '```', '']
    os.makedirs(os.path.dirname(OUT_LICENSES), exist_ok=True)
    with open(OUT_LICENSES, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(lines))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    scratch_guess = [os.path.join(ROOT, '.cache', 'icons-v12'), os.path.join(HERE, '.cache')]
    ap.add_argument('--tabler', help='tabler-icons/icons/outline directory')
    ap.add_argument('--mdi', help='MaterialDesign-SVG checkout (meta.json + svg/)')
    ap.add_argument('--no-mdi', action='store_true')
    ap.add_argument('--debug', help='print the term/score breakdown for a project id')
    ap.add_argument('--explain', help='after assignment, list a project\'s best candidates and their owners')
    args = ap.parse_args()

    tabler_dir = find_dir(args.tabler, 'ICONS_V12_TABLER',
                          [os.path.join(g, 'tabler', 'icons', 'outline') for g in scratch_guess], 'telescope.svg')
    if not tabler_dir:
        raise SystemExit('Tabler outline icons not found: pass --tabler <tabler-icons/icons/outline>')
    tabler_root = os.path.dirname(os.path.dirname(os.path.abspath(tabler_dir)))
    mdi_dir = None
    if not args.no_mdi:
        mdi_dir = find_dir(args.mdi, 'ICONS_V12_MDI', [os.path.join(g, 'mdi') for g in scratch_guess], 'meta.json')

    with open(CATALOG, encoding='utf-8') as fh:
        catalog = json.load(fh)
    if isinstance(catalog, dict):
        catalog = catalog.get('projects') or catalog.get('items') or []
    ids = [p['id'] for p in catalog]
    if len(set(ids)) != len(ids):
        raise SystemExit('catalog has duplicate ids')

    rejected = Counter()
    icons = load_tabler(tabler_dir, rejected)
    tabler_names = {ic.name for ic in icons}
    if mdi_dir:
        icons += load_mdi(mdi_dir, rejected, tabler_names)
    # identical geometry is one glyph: keep the first (Tabler before MDI, alphabetical)
    BASE_NAMES.update(ic.name for ic in icons)
    demote_badge_variants(icons, rejected)
    seen_markup = {}
    for ic in icons:
        if ic.markup in seen_markup:
            ic.tier = 9
            rejected['duplicate geometry'] += 1
        else:
            seen_markup[ic.markup] = ic.key

    en, names, zh, category, themes, families, generic, stop, summary_stop = load_synonyms()
    matcher = Matcher(icons, en, names, generic, stop)
    pt = ProjectTerms(en, names, zh, category, generic, stop, summary_stop, matcher)

    name_index = {ic.name: i for i, ic in enumerate(icons) if ic.tier != 9}
    theme_bonus = {}
    for cat, lst in themes.items():
        tb = {}
        for rank, nm in enumerate(lst):
            if nm in name_index and name_index[nm] not in tb:
                tb[name_index[nm]] = THEME_BONUS * (1 - 0.6 * rank / max(1, len(lst) - 1))
            elif nm not in name_index:
                matcher.unknown_targets['theme:' + nm] += 1
        fam = []
        prefixes, tag_groups = families.get(cat, ([], []))
        for prefix in prefixes:
            members = [i for i, ic in enumerate(icons)
                       if ic.tier == 0 and i not in tb and (ic.name == prefix or ic.name.startswith(prefix + '-'))
                       and not BAD_MODIFIER_RE.search(ic.name[len(prefix):])]
            members.sort(key=lambda i: (modifier_rank(icons[i].name[len(prefix):]), icons[i].src != 't',
                                        icons[i].name.count('-'), icons[i].name))
            for i in members:
                if i not in tb and i not in fam:
                    fam.append(i)
        for rank, i in enumerate(fam):
            tb[i] = FAMILY_BONUS * (1 - 0.5 * rank / max(1, len(fam) - 1))
        grp = []
        for g in (tag_groups if TAG_FAMILY_BONUS > 0 else []):
            src, label = g.split(':', 1)
            members = [i for i, ic in enumerate(icons) if ic.tier == 0 and i not in tb and ic.src == src
                       and (label in ic.tags if src == 'm' else ic.cat == label)
                       and not BAD_MODIFIER_RE.search(ic.name)]
            members.sort(key=lambda i: (icons[i].name.count('-'), icons[i].name.endswith('-outline'), icons[i].name))
            grp += [i for i in members if i not in grp]
        for rank, i in enumerate(grp):
            tb[i] = TAG_FAMILY_BONUS * (1 - 0.5 * rank / max(1, len(grp) - 1))
        theme_bonus[cat] = tb
    all_terms = [pt.project_terms(p) for p in catalog]
    all_parts = [dict() for _ in catalog]
    all_scores = [score_project(t, matcher, theme_bonus.get(p.get('category')), parts)
                  for t, p, parts in zip(all_terms, catalog, all_parts)]

    if args.debug:
        pi = ids.index(args.debug)
        p = catalog[pi]
        print(p['titleEn'], '|', p['title'])
        for k, w in sorted(all_terms[pi].items(), key=lambda x: -x[1]):
            print('  term %-32s %.2f' % (k, w))
        top = sorted(((i, r) for i, r in all_scores[pi].items() if icons[i].tier != 9),
                     key=lambda x: -effective(all_parts[pi][x[0]], icons[x[0]]))[:25]
        for i, r in top:
            print('  %-40s raw=%.2f eff=%.2f q=%.2f' % (icons[i].key, r, effective(all_parts[pi][i], icons[i]), q_of(r)))
        return

    # category pools (for the fallback): icons matching the category terms, best first
    category_pools = {}
    for cat, phrases in category.items():
        acc = {}
        for ph in phrases:
            for k in pt.expand(ph):
                acc[k] = acc.get(k, 0) + 1.0
        sc = score_project(acc, matcher)
        category_pools[cat] = [i for i, r in sorted(sc.items(), key=lambda x: (-x[1], icons[x[0]].key))
                               if icons[i].tier == 0]
    neutral_cats = ['Devices', 'System', 'Design', 'Shapes', 'Map', 'Vehicles', 'Weather', 'Nature', 'Health',
                    'Electrical', 'Computers', 'Charts', 'Development', 'Database', 'Buildings', 'Math',
                    'Photography', 'Media', 'Logic']
    neutral_pool = [i for c in neutral_cats for i, ic in sorted(enumerate(icons), key=lambda x: x[1].name)
                    if ic.src == 't' and ic.cat == c and ic.tier == 0]

    inherit_from_families(all_scores, all_parts, icons)
    tabler_by_name = {ic.name: i for i, ic in enumerate(icons) if ic.src == 't' and ic.tier == 0}
    neutral_geometry = [tabler_by_name[nm] for nm in NEUTRAL_GEOMETRY if nm in tabler_by_name]
    extra = [i for i, ic in enumerate(icons) if ic.tier == 0 and i not in neutral_geometry and (
             (ic.src == 't' and ic.cat == 'Shapes') or (ic.src == 'm' and {'Shape', 'Vector'} & set(ic.tags)))
             and not re.search(r'heart|star|club|spade|diamond|cards|rosette|asterisk|percent|forbid|check|key|'
                               r'plus|minus|remove|x$|-x-|cancel|question|alert|lock|dot$', ic.name)]
    extra.sort(key=lambda i: (icons[i].src != 't', icons[i].name.count('-'), icons[i].name))
    neutral_geometry += extra
    chosen, swaps, fallback = assign(catalog, all_scores, all_parts, icons, category_pools, neutral_pool,
                                     neutral_geometry)
    if args.explain:
        owner = {i: catalog[pi]['id'] for pi, i in enumerate(chosen)}
        pi = ids.index(args.explain)
        print(catalog[pi]['titleEn'], '->', icons[chosen[pi]].key, 'q=%.2f' % q_of(all_scores[pi][chosen[pi]]))
        top = sorted(((i, r) for i, r in all_scores[pi].items() if icons[i].tier == 0),
                     key=lambda x: -effective(all_parts[pi][x[0]], icons[x[0]]))[:40]
        for i, r in top:
            o = owner.get(i, '-')
            ot = next((p['titleEn'] for p in catalog if p['id'] == o), '') if o != '-' else ''
            print('  %-36s raw=%.2f eff=%.2f parts=%s  owner=%s %s' % (
                icons[i].key, r, effective(all_parts[pi][i], icons[i]), tuple(round(x, 2) for x in all_parts[pi][i]), o, ot[:50]))
        free = sorted(((i, r) for i, r in all_scores[pi].items() if icons[i].tier == 0 and i not in owner),
                      key=lambda x: -effective(all_parts[pi][x[0]], icons[x[0]]))[:20]
        print('  -- best free:')
        for i, r in free:
            print('  %-36s raw=%.2f eff=%.2f parts=%s' % (icons[i].key, r, effective(all_parts[pi][i], icons[i]),
                                                       tuple(round(x, 2) for x in all_parts[pi][i])))
        return

    # ---- build outputs
    out_icons = {}
    rows = []
    for pi, p in enumerate(catalog):
        ic = icons[chosen[pi]]
        raw = all_scores[pi].get(chosen[pi], 0.0)
        q = q_of(raw)
        out_icons[p['id']] = {'n': ic.name, 's': ic.src, 'd': ic.markup, 'q': q}
        rows.append((p, ic, q, raw))
    names_used = [r[1].name for r in rows]
    assert len(set(names_used)) == len(names_used), 'duplicate glyph names'
    assert len({r[1].markup for r in rows}) == len(rows), 'duplicate glyph geometry'
    assert all(r[1].tier != 9 for r in rows), 'blocked icon assigned'

    doc = {
        'version': 12,
        'sources': {
            'tabler': {'license': 'MIT', 'url': 'https://tabler.io/icons'},
            'mdi': {'license': 'Apache-2.0', 'url': 'https://pictogrammers.com/library/mdi/'},
        },
        'icons': out_icons,
    }
    text = json.dumps(doc, ensure_ascii=False, separators=(',', ':'))
    with open(OUT_JSON, 'w', encoding='utf-8') as fh:
        fh.write(text)

    src_counts = Counter(r[1].src for r in rows)
    revs = {'t': git_rev(tabler_dir), 'm': git_rev(mdi_dir) if mdi_dir else 'n/a'}
    write_licenses(tabler_root, mdi_dir, src_counts, revs)
    write_report(rows, catalog, icons, rejected, swaps, fallback, matcher, pt, len(text.encode('utf-8')), revs,
                 tabler_dir, mdi_dir)

    qs = sorted(r[2] for r in rows)
    print('project icons: %d projects, %d distinct glyphs (tabler %d, mdi %d), json %.1f KB' % (
        len(rows), len(set(names_used)), src_counts.get('t', 0), src_counts.get('m', 0), len(text.encode('utf-8')) / 1024))
    print('q: min %.2f  p10 %.2f  median %.2f  mean %.3f  p90 %.2f  max %.2f  | swaps %d  fallback %s' % (
        qs[0], qs[len(qs) // 10], qs[len(qs) // 2], sum(qs) / len(qs), qs[len(qs) * 9 // 10], qs[-1], swaps,
        dict(fallback) or 'none'))
    if matcher.unknown_targets:
        print('note: %d synonym targets name no loaded icon (e.g. %s)' % (
            len(matcher.unknown_targets), ', '.join(sorted(matcher.unknown_targets)[:12])))


def md_escape(s):
    return str(s).replace('|', '\\|').replace('\n', ' ')


def write_report(rows, catalog, icons, rejected, swaps, fallback, matcher, pt, size, revs, tabler_dir, mdi_dir):
    n = len(rows)
    clusters = []
    for label, pat in (('tunnel', r'\btunnels?\b'), ('bridge', r'\bbridges?\b'), ('dam', r'\bdams?\b'),
                       ('telescope', r'\btelescopes?\b'), ('aircraft / airliner', r'\b(aircraft|airliner)s?\b'),
                       ('wind', r'\bwind\b'), ('hydropower', r'hydro(power|electric)')):
        clusters.append('%d %s titles' % (sum(1 for p in catalog if re.search(pat, (p.get('titleEn') or '').lower())), label))
    cluster_text = ', '.join(clusters)
    src_counts = Counter(r[1].src for r in rows)
    lines = ['# V12 project icons — assignment report', '',
             'Generated by `tools/icons-v12/assign_icons.py` (deterministic; rerun to regenerate).', '',
             '## Summary', '',
             '| Metric | Value |', '| --- | ---: |',
             '| Projects | %d |' % n,
             '| Distinct glyphs | %d |' % len({r[1].name for r in rows}),
             '| Tabler (MIT) | %d |' % src_counts.get('t', 0),
             '| Material Design Icons (Apache-2.0) | %d |' % src_counts.get('m', 0),
             '| `project-icons.json` size | %.1f KB |' % (size / 1024),
             '| Icons loaded (usable / avoid / never) | %d / %d / %d |' % (
                 sum(1 for i in icons if i.tier == 0), sum(1 for i in icons if i.tier == 1),
                 sum(1 for i in icons if i.tier == 9)),
             '| Exchange improvements | %d |' % swaps,
             '| Fallback assignments | %s |' % (', '.join('%s %d' % kv for kv in sorted(fallback.items())) or 'none'),
             '| Avoid-tier glyphs used | %d |' % sum(1 for r in rows if r[1].tier == 1),
             '| MDI picks with q ≥ 0.6 / q < 0.3 | %d / %d |' % (
                 sum(1 for r in rows if r[1].src == 'm' and r[2] >= 0.6), sum(1 for r in rows if r[1].src == 'm' and r[2] < 0.3)),
             '| Flagship courses (named ids) mean q | %.2f |' % (
                 sum(r[2] for r in rows if is_flagship(r[0])) / max(1, sum(1 for r in rows if is_flagship(r[0])))),
             '| Tabler revision | `%s` |' % revs.get('t'),
             '| MDI revision | `%s` |' % revs.get('m'),
             '']
    if rejected:
        lines += ['Icons skipped while loading: ' + ', '.join('%s %d' % kv for kv in sorted(rejected.items())), '']

    qs = [r[2] for r in rows]
    lines += ['## Score distribution', '',
              '`q` is the match strength (0–1): `1 - exp(-raw / %.1f)`, where *raw* sums the weighted matches of '
              'the project\'s title / Chinese title / sub-category / summary terms against the glyph\'s name, '
              'aliases and tags.' % Q_SCALE, '',
              '| Statistic | q |', '| --- | ---: |',
              '| min | %.2f |' % min(qs), '| 10th percentile | %.2f |' % sorted(qs)[n // 10],
              '| median | %.2f |' % sorted(qs)[n // 2], '| mean | %.3f |' % (sum(qs) / n),
              '| 90th percentile | %.2f |' % sorted(qs)[n * 9 // 10], '| max | %.2f |' % max(qs), '',
              '| q range | Projects | Share |', '| --- | ---: | ---: |']
    bins = [(0.0, 0.2), (0.2, 0.4), (0.4, 0.6), (0.6, 0.8), (0.8, 1.01)]
    for lo, hi in bins:
        c = sum(1 for q in qs if lo <= q < hi)
        lines.append('| %.1f–%.1f | %d | %.1f%% |' % (lo, min(hi, 1.0), c, 100.0 * c / n))
    lines.append('')

    lines += ['## By catalog category', '', '| Category | Projects | Tabler | MDI | mean q | min q |',
              '| --- | ---: | ---: | ---: | ---: | ---: |']
    bycat = defaultdict(list)
    for r in rows:
        bycat[r[0].get('category')].append(r)
    for cat in sorted(bycat):
        rs = bycat[cat]
        lines.append('| %s | %d | %d | %d | %.2f | %.2f |' % (
            cat, len(rs), sum(1 for r in rs if r[1].src == 't'), sum(1 for r in rs if r[1].src == 'm'),
            sum(r[2] for r in rs) / len(rs), min(r[2] for r in rs)))
    lines.append('')

    lines += ['## By icon source category', '', '| Source / icon category | Glyphs |', '| --- | ---: |']
    bysrc = Counter()
    for r in rows:
        if r[1].src == 't':
            bysrc['Tabler / ' + (r[1].cat or '(uncategorised)')] += 1
        else:
            bysrc['MDI / ' + ((r[1].tags or ['(untagged)'])[0])] += 1
    for k, v in sorted(bysrc.items(), key=lambda kv: (-kv[1], kv[0])):
        lines.append('| %s | %d |' % (md_escape(k), v))
    lines.append('')

    lines += ['## 30 lowest-scoring assignments', '',
              'These projects mostly have proper-noun titles or abstract topics; their glyphs come from secondary '
              'terms (summary, sub-category, category).', '',
              '| q | Project | Title | Glyph |', '| ---: | --- | --- | --- |']
    low = sorted(rows, key=lambda r: (r[2], r[0]['id']))[:30]
    for p, ic, q, raw in low:
        lines.append('| %.2f | `%s` | %s / %s | `%s` (%s) |' % (q, p['id'], md_escape(p.get('titleEn', '')),
                                                           md_escape(p.get('title', '')), ic.name, ic.src))
    lines.append('')

    good = [r for r in rows if r[2] >= 0.75]
    good.sort(key=lambda r: r[0]['id'])
    step = max(1, len(good) // 40)
    sample = good[::step][:40]
    lines += ['## Sample of 40 strong assignments (q ≥ 0.75, evenly spaced by id)', '',
              '| q | Project | Title | Glyph |', '| ---: | --- | --- | --- |']
    for p, ic, q, raw in sample:
        lines.append('| %.2f | `%s` | %s | `%s` (%s) |' % (q, p['id'], md_escape(p.get('titleEn', '')), ic.name, ic.src))
    lines.append('')

    mdi_rows = sorted((r for r in rows if r[1].src == 'm'), key=lambda r: r[0]['id'])
    if mdi_rows:
        lines += ['## All MDI picks', '', '<details><summary>%d MDI glyphs (expand)</summary>' % len(mdi_rows), '',
                  'MDI candidates carry a handicap (selection score x %.2f, i.e. they must match about %d%% better) '
                  'and are only chosen when clearly more representative than every unused Tabler glyph.' % (
                      MDI_FACTOR, round(100 / MDI_FACTOR - 100)), '',
                  '| q | Project | Title | Glyph |', '| ---: | --- | --- | --- |']
        for p, ic, q, raw in mdi_rows:
            lines.append('| %.2f | `%s` | %s | `%s` |' % (q, p['id'], md_escape(p.get('titleEn', '')), ic.name))
        lines += ['', '</details>', '']

    lines += ['## Method', '',
              '1. **Terms.** English title n-grams (weight 1.0), Chinese title keywords via the zh table (0.8), '
              'proper nouns via the names table (1.0), sub-category (0.45), diagram hints (0.3/0.2), catalog '
              'category (0.3) and summary (0.25, synonym-table terms only). Generic words are down-weighted.',
              '2. **Synonyms.** `tools/icons-v12/synonyms.json` maps %d English engineering terms, %d proper nouns '
              'and %d Chinese keywords to icon names/tokens, plus per-category theme lists and name-prefix '
              'families.' % (len(pt.en), len(pt.names), len(pt.zh)),
              '3. **Evidence.** Best target match per term (full name 1.0, name token 0.7, MDI alias 0.55, tag 0.3 '
              'capped at %.1f), diminishing returns across terms (x%.1f each), name-coverage factor %.2f–1.0; '
              'category theme bonus up to %.2f; badge variants (e.g. `airplane-cog`) inherit %d%% of their base '
              'glyph\'s match.' % (TAG_CAP, DECAY, COV_BASE, THEME_BONUS, round(INHERIT_SHARE * 100)),
              '4. **Selection.** Match evidence x glyph prior x %.1f for MDI (an MDI glyph must match about %d%% '
              'better than every unused Tabler glyph) + theme + inheritance. The %d flagship courses (named ids) '
              'get a x%.1f boost so they pick first.' % (MDI_FACTOR, round(100 / MDI_FACTOR - 100),
                                                         sum(1 for p in catalog if is_flagship(p)), FLAGSHIP_BOOST),
              '5. **Uniqueness.** Global best-first greedy over all (project, glyph, score) pairs, then exchange '
              'chains (depth ≤ 2) that raise the summed score, then category / neutral pools. Weak picks with '
              'neither concept nor theme evidence become neutral geometric glyphs rather than misleading pictograms.',
              '6. **Policy.** Never: Tabler *Brand*, MDI *Brand / Logo*, product trademarks (e.g. Steam, PlayStation, '
              'Olympic rings, Apple devices, Death Star), religious, weapon and drug symbols. Last resort only: '
              'letters, numbers, zodiac, gender, mood, laundry, gestures, badges, `-off` variants, badge variants of '
              'UI glyphs and trivial glyphs.', '',
              '## Why the tail is weak', '',
              'Several concept clusters have far more projects than distinct glyphs exist for them (e.g. %s). '
              'Once the on-concept glyphs are taken, the remaining members receive the best still-free themed '
              'glyph, a badge variant of their concept, or a neutral geometric shape (q close to 0).' % cluster_text, '']
    with open(OUT_REPORT, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(lines))


if __name__ == '__main__':
    main()
