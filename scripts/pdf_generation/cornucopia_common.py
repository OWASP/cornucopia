"""
Shared configuration, discovery and resolution layer for the OWASP Cornucopia
deck generator.

This module deliberately depends on nothing but PyYAML and the standard library
so that it can be imported both by ``generate_deck.py`` (which runs inside
Scribus' embedded Python) and by ``merge_pdfs.py`` (which runs in a normal
system Python).

Everything that used to be a hardcoded constant in the engine lives here as a
lookup against ``pdf_config.yaml``. The engine asks this module questions; it
never assumes how many editions, languages, suits or jokers exist.
"""

import os
import re

import yaml


# --------------------------------------------------------------------------
# Basic loading
# --------------------------------------------------------------------------

def load_yaml(path, default=None):
    """Load a YAML file, returning ``default`` when it is missing or empty."""
    if not path or not os.path.exists(path):
        return {} if default is None else default
    with open(path, 'r', encoding='utf-8') as handle:
        return yaml.safe_load(handle) or ({} if default is None else default)


def load_config(script_dir, config_name='pdf_config.yaml'):
    """Load the central control-panel config."""
    return load_yaml(os.path.join(script_dir, config_name))


def load_assets(config, script_dir):
    """Load the optional assets.yaml override table."""
    rel = config.get('paths', {}).get('assets_config_path', 'assets.yaml')
    return load_yaml(os.path.join(script_dir, rel))


# --------------------------------------------------------------------------
# Path helpers
# --------------------------------------------------------------------------

def resolve_asset_path(base_dir, config, relative_subpath):
    """Resolve a path underneath the configured asset root."""
    asset_root = config.get('paths', {}).get('asset_root', 'Assets')
    clean = str(relative_subpath).replace('\\', '/').lstrip('/')
    if clean.lower().startswith('assets/'):
        clean = clean[7:]
    if os.path.isabs(asset_root):
        return os.path.join(asset_root, clean).replace('\\', '/')
    return os.path.join(base_dir, asset_root, clean).replace('\\', '/')


def data_template(config):
    """The configured naming pattern for card data files."""
    return config.get('paths', {}).get(
        'card_data_path', 'source/%edition%/%language%/cornucopia_%language%.yaml')


def card_data_path(config, base_dir, edition, language, version=None):
    """Absolute path to the source YAML for one edition/language pair."""
    template = data_template(config)
    if version is None and '%edition_version%' in template:
        version = edition_data_version(config, base_dir, edition)
    rel = (template
           .replace('%edition%', edition)
           .replace('%language%', language)
           .replace('%edition_version%', str(version or '')))
    return os.path.join(base_dir, rel)


def output_dir(config, base_dir):
    return os.path.join(base_dir, config.get('paths', {}).get('output_dir', 'Generated_Cards'))


def qr_dir(config, base_dir):
    return os.path.join(base_dir, config.get('paths', {}).get('qr_code_dir', 'Assets/QRCodes'))


# --------------------------------------------------------------------------
# Dynamic discovery — the "all" keyword
# --------------------------------------------------------------------------

_TOKEN_PATTERNS = {
    'edition': r'[A-Za-z0-9_-]+?',
    'language': r'[A-Za-z0-9_]+',
    'edition_version': r'[0-9][0-9.]*',
}


def _data_pattern_regex(config):
    """
    Turn ``card_data_path`` into a regex that can recognise a card file.

    Discovery is derived from the configured pattern rather than assuming a
    directory layout, so the same code finds the data whether it is stored as
    one file per language directory or as a flat folder of files named
    ``<edition>-cards-<version>-<language>.yaml``.
    """
    parts = re.split(r'(%[a-z_]+%)', data_template(config))
    seen, out = set(), []
    for part in parts:
        token = re.fullmatch(r'%([a-z_]+)%', part)
        if not token:
            out.append(re.escape(part).replace('/', r'[\\/]'))
            continue
        name = token.group(1)
        body = _TOKEN_PATTERNS.get(name)
        if body is None:
            out.append(re.escape(part))
        elif name in seen:
            # A token used twice must match the same text both times.
            out.append('(?P=%s)' % name)
        else:
            seen.add(name)
            out.append('(?P<%s>%s)' % (name, body))
    return re.compile('^' + ''.join(out) + '$', re.IGNORECASE)


def _version_key(text):
    """Sort versions numerically, so 3.0 outranks 2.2 and 1.1 outranks 1.0."""
    return tuple(int(p) if p.isdigit() else 0 for p in str(text).split('.'))


def scan_card_files(config, base_dir):
    """Every file under the source root whose name matches the data pattern."""
    root = os.path.join(base_dir, config.get('paths', {}).get('source_root', 'source'))
    if not os.path.isdir(root):
        return []

    regex = _data_pattern_regex(config)
    found = []
    for dirpath, _dirnames, filenames in os.walk(root):
        for name in filenames:
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, base_dir).replace('\\', '/')
            match = regex.match(rel)
            if not match:
                continue
            fields = match.groupdict()
            found.append({
                'edition': fields.get('edition') or '',
                'language': fields.get('language') or '',
                'version': fields.get('edition_version') or '',
                'path': full,
            })
    return found


def edition_data_version(config, base_dir, edition):
    """
    Which release of an edition's data to build.

    Taken from that edition's ``data_version`` in the config when set, so a
    build is pinned to a known release. Otherwise the highest version present
    is used, so a newly added release is picked up without a config change.
    """
    declared = edition_config(config, edition).get('data_version')
    if declared:
        return str(declared)
    versions = {f['version'] for f in scan_card_files(config, base_dir)
                if f['edition'].lower() == str(edition).lower() and f['version']}
    return max(versions, key=_version_key) if versions else ''


def supported_editions(config):
    """
    The editions this tool is set up to build, named in the config.

    ``source/`` also holds card data for decks this tool does not produce --
    EoP, DBD, Cumulus and others -- so what is on disk is not the same as what
    can be built. Asking for one of those should be refused, not attempted.
    """
    return sorted((config.get('editions', {}) or {}).keys())


def discover_editions(config, base_dir):
    """
    Every edition that is both configured and has card data present.

    Configured but missing data is left out, so the list offered to a user is
    what they can actually build right now.
    """
    on_disk = {f['edition'] for f in scan_card_files(config, base_dir) if f['edition']}
    configured = supported_editions(config)
    if not configured:
        return sorted(on_disk)
    return [name for name in configured if name in on_disk]


def discover_languages(config, base_dir, edition):
    """Every language available for an edition, at the version being built."""
    wanted = edition_data_version(config, base_dir, edition)
    return sorted({f['language'] for f in scan_card_files(config, base_dir)
                   if f['edition'].lower() == str(edition).lower()
                   and f['language']
                   and (not wanted or f['version'] == wanted)})


def find_misnamed_files(config, base_dir):
    """
    Files sitting with the card data that carry an unexpected extension.

    A mistyped extension is the one way a language can vanish from a build
    without anything else noticing, so it is reported rather than ignored.
    """
    root = os.path.join(base_dir, config.get('paths', {}).get('source_root', 'source'))
    if not os.path.isdir(root):
        return []
    odd = []
    for dirpath, _dirnames, filenames in os.walk(root):
        for name in filenames:
            if os.path.splitext(name)[1].lower() not in ('.yaml', '.yml'):
                odd.append(os.path.join(dirpath, name))
    return odd


def expand_selection(requested, available, label, warnings):
    """
    Resolve the ``"all"`` keyword against what actually exists on disk.

    A string that is not ``"all"`` is treated as a single-item selection.
    Explicit entries that do not exist are reported rather than ignored, so a
    typo fails loudly instead of quietly producing a short deck.
    """
    if requested is None:
        requested = 'all'
    if isinstance(requested, str):
        if requested.strip().lower() == 'all':
            return list(available)
        requested = [requested]

    resolved, missing = [], []
    for item in requested:
        item = str(item).strip()
        if item in available:
            resolved.append(item)
        else:
            missing.append(item)
    if missing:
        warnings.append(
            "Requested {0} not found: {1} (available: {2})".format(
                label, ', '.join(missing), ', '.join(available) or 'none'))
    return resolved


def resolve_targets(config, base_dir, editions=None, languages=None, sizes=None):
    """
    Build the full generation matrix.

    Returns ``(targets, warnings)`` where each target is a dict carrying the
    edition, language and size to build. CLI arguments take precedence over
    ``generation_targets`` in the config; both accept ``"all"`` or a list.
    """
    warnings = []
    wanted = config.get('generation_targets', {}) or {}

    requested_editions = editions if editions else wanted.get('editions', 'all')
    requested_languages = languages if languages else wanted.get('languages', 'all')
    requested_sizes = sizes if sizes else wanted.get('sizes', 'all')

    available_editions = discover_editions(config, base_dir)
    chosen_editions = expand_selection(requested_editions, available_editions, 'edition', warnings)

    available_sizes = list((config.get('size_profiles', {}) or {}).keys())
    chosen_sizes = expand_selection(requested_sizes, available_sizes, 'size', warnings)

    targets = []
    for edition in chosen_editions:
        available_languages = discover_languages(config, base_dir, edition)
        chosen_languages = expand_selection(
            requested_languages, available_languages,
            "language for edition '{0}'".format(edition), warnings)
        for language in chosen_languages:
            for size in chosen_sizes:
                targets.append({'edition': edition, 'language': language, 'size': size})

    for path in find_misnamed_files(config, base_dir):
        warnings.append(
            "Ignored '{0}': not a .yaml file (check the extension)".format(path))
    return targets, warnings


# --------------------------------------------------------------------------
# Card data
# --------------------------------------------------------------------------

def parse_cards(yaml_path):
    """
    Read one source YAML into a flat card list.

    Returns ``(cards, suit_order)``. ``suit_order`` is the order the suits
    appear in the file, which is the canonical print order unless an edition
    overrides it in config.
    """
    data = load_yaml(yaml_path)
    cards, suit_order = [], []

    for index, suit in enumerate(data.get('suits', []) or []):
        suit_id = str(suit.get('id', '')).strip()
        suit_order.append(suit_id)
        for card in suit.get('cards', []) or []:
            cards.append({
                'suit_name': suit.get('name', '') or '',
                'suit_id': suit_id,
                'suit_index': index,
                'card_id': str(card.get('id', '')).strip(),
                'value': str(card.get('value', '')),
                'attack_text': card.get('desc', '') or '',
                'misc_text': card.get('misc', '') or '',
                'card_kind': str(card.get('card', '') or '').strip(),
                'url': card.get('url', '') or '',
            })
    return cards, suit_order


def sort_deck(cards, config, edition, suit_order, language=None):
    """
    Sort into factory/print order: by suit, then by card value.

    Suit order comes from the source file unless the edition declares an
    override. The sort is stable, so anything the value map does not know
    about keeps its original relative position.
    """
    semantics = card_semantics(config, language)
    value_order = {str(k).upper(): int(v)
                   for k, v in (semantics.get('value_order', {}) or {}).items()}

    override = (edition_config(config, edition).get('suit_order') or suit_order)
    positions = {str(s).lower(): i for i, s in enumerate(override)}

    def key(card):
        return (positions.get(str(card['suit_id']).lower(), 999),
                value_order.get(str(card['value']).upper().strip(), 999))

    return sorted(cards, key=key)


# --------------------------------------------------------------------------
# Card semantics — all derived from data or config, never hardcoded
# --------------------------------------------------------------------------

def edition_config(config, edition):
    return (config.get('editions', {}) or {}).get(edition, {}) or {}


def card_semantics(config, language=None):
    """
    Card semantics for a language, with any per-language overrides merged in.

    Needed because card values are localised: Russian and Ukrainian write the
    court cards as B/D/K in Cyrillic rather than J/Q/K, so a single global list
    would silently fail to recognise them as court cards.
    """
    base = config.get('card_semantics', {}) or {}
    override = ((base.get('language_overrides', {}) or {}).get(language, {}) or {}) if language else {}
    if not override:
        return base

    merged = dict(base)
    if override.get('court_values'):
        merged['court_values'] = list(base.get('court_values', []) or []) + list(override['court_values'])
    if override.get('value_order'):
        values = dict(base.get('value_order', {}) or {})
        values.update(override['value_order'])
        merged['value_order'] = values
    return merged


def is_joker(card, config, edition):
    """
    A card is a joker if its suit is declared as a joker suit for the edition,
    or if the source data marks it as one.

    Both paths are needed: the data marker is localised (Italian says "Jolly"),
    so matching on its text alone is unreliable, and some editions have no
    jokers at all.
    """
    joker_suits = {str(s).lower()
                   for s in (edition_config(config, edition).get('joker_suits') or [])}
    if str(card.get('suit_id', '')).lower() in joker_suits:
        return True
    return str(card.get('card_kind', '')).strip().lower() == 'joker'


def is_court(card, config, language=None):
    """Court cards (J/Q/K, or their localised equivalents) take court artwork."""
    court = {str(v).upper() for v in (card_semantics(config, language).get('court_values') or [])}
    return str(card.get('value', '')).upper().strip() in court


def has_special_text(card):
    """
    The special-text frame is rendered when the card carries misc text.

    This is purely data-driven, which is what lets jokerless editions such as
    Companion work without any special-casing in the engine.
    """
    return bool(str(card.get('misc_text', '') or '').strip())


# --------------------------------------------------------------------------
# Fonts and sizing
# --------------------------------------------------------------------------

def get_font(config, language, role='body'):
    """Font for a language and role ('body' or 'accent'), falling back to default."""
    handling = config.get('font_handling', {}) or {}
    default = handling.get('default', {}) or {}
    per_language = handling.get(language, {}) or {}
    return per_language.get(role, default.get(role, 'Noto Sans Light'))


def get_font_size(config, size_key, frame, language):
    """
    Base size for a frame in a size profile, plus any per-language offset.

    Offsets are declared per frame so that shrinking a dense language affects
    only the frames that actually overflow.
    """
    profile = (config.get('size_profiles', {}) or {}).get(size_key, {}) or {}
    base = float((profile.get('base_font_sizes', {}) or {}).get(frame, 0.0))

    scaling = config.get('font_scaling', {}) or {}
    frame_scaling = scaling.get(frame, {})
    if isinstance(frame_scaling, dict):
        offset = frame_scaling.get(language, frame_scaling.get('default', 0.0))
    else:
        offset = frame_scaling
    return base + float(offset or 0.0)


# --------------------------------------------------------------------------
# Colours
# --------------------------------------------------------------------------

def _suit_entry(assets_data, edition, suit_id):
    """The assets.yaml block for one suit, if it has one."""
    if not assets_data:
        return {}
    block = assets_data.get(edition)
    if isinstance(block, dict):
        suits = block.get('suits', []) or []
    else:
        suits = assets_data.get('suits', []) or []
    for suit in suits:
        if str(suit.get('id', '')).lower() == str(suit_id).lower():
            return suit
    return {}


def _swatch(value, generated_name, definitions):
    """
    Accept either a Scribus swatch name or an inline CMYK mapping.

    An inline mapping is registered under a generated name so it can be
    injected into the template, which is what lets a palette be declared
    purely as data.
    """
    if isinstance(value, dict) and value:
        definitions[generated_name] = {k: int(value.get(k, 0)) for k in ('c', 'm', 'y', 'k')}
        return generated_name
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def card_colors(config, assets_data, edition, card, language=None):
    """
    Resolve the swatch names a single card needs.

    Precedence for both the suit colour and the court-card number colour:
      1. the suit's entry in assets.yaml (name or inline CMYK),
      2. the edition block in pdf_config.yaml,
      3. the global default.

    The court colour is per suit rather than global, so a suit can deviate
    from white without touching any code.

    Returns ``(suit_color, number_color, definitions_to_inject)``.
    """
    suit_id = str(card.get('suit_id', ''))
    entry = _suit_entry(assets_data, edition, suit_id)
    defaults = config.get('defaults', {}) or {}
    ed_cfg = edition_config(config, edition)
    definitions = {}

    suit_color = _swatch(entry.get('color'),
                         'Suit_{0}_{1}'.format(edition.capitalize(), suit_id.upper()),
                         definitions)
    if not suit_color:
        suit_color = {str(k).lower(): v
                      for k, v in (ed_cfg.get('suit_colors') or {}).items()}.get(suit_id.lower())
    if not suit_color:
        suit_color = defaults.get('suit_color', 'Data_Color')

    court_color = _swatch(entry.get('court_color'),
                          'Court_{0}_{1}'.format(edition.capitalize(), suit_id.upper()),
                          definitions)
    if not court_color:
        court_color = {str(k).lower(): v
                       for k, v in (ed_cfg.get('court_colors') or {}).items()}.get(suit_id.lower())
    if not court_color:
        court_color = defaults.get('court_text_color', 'Pure_White')

    number_color = court_color if is_court(card, config, language) else suit_color
    return suit_color, number_color, definitions


def has_suit_color(config, assets_data, edition, suit_id):
    """True when a suit has an explicit colour, rather than falling back."""
    if _suit_entry(assets_data, edition, suit_id).get('color'):
        return True
    declared = {str(k).lower()
                for k in (edition_config(config, edition).get('suit_colors') or {})}
    return str(suit_id).lower() in declared


def suit_colors_for_edition(config, edition):
    """
    Named swatches this edition may reference, for injection into the template.

    Inline CMYK palettes declared in assets.yaml are handled separately by
    card_colors(), which returns them per card.
    """
    names = set((edition_config(config, edition).get('suit_colors') or {}).values())
    defaults = config.get('defaults', {}) or {}
    for key in ('suit_color', 'court_text_color', 'suit_name_color'):
        if defaults.get(key):
            names.add(defaults[key])
    return sorted(n for n in names if n)


# --------------------------------------------------------------------------
# Artwork resolution — convention first, assets.yaml as override only
# --------------------------------------------------------------------------

def asset_key(config, size_key):
    profile = (config.get('size_profiles', {}) or {}).get(size_key, {}) or {}
    return profile.get('asset_key', 'small')


def suit_asset_id(config, edition, suit_id):
    """
    Map a suit ID onto its artwork filename stem.

    Needed because some editions ship artwork whose stem differs from the suit
    ID in the source data (Mobile App: suit ``RS`` -> ``r``, ``WC`` -> ``wcm``).
    """
    aliases = {str(k).lower(): str(v).lower()
               for k, v in (edition_config(config, edition).get('suit_asset_aliases') or {}).items()}
    key = str(suit_id).lower().strip()
    return aliases.get(key, key)


def _assets_override(assets_data, edition, suit_id, card_id, size_token):
    """
    Look for explicit filenames in assets.yaml.

    Returns ``(card_level, suit_level)``. The two are kept apart because they
    rank differently: a per-card entry is a deliberate exception and outranks
    everything, whereas a suit-level entry is only that suit's *default*
    artwork and must not override court art for a court card.
    """
    if not assets_data:
        return None, None
    suits = []
    if edition in assets_data and isinstance(assets_data.get(edition), dict):
        suits = assets_data[edition].get('suits', []) or []
    elif 'suits' in assets_data:
        suits = assets_data.get('suits', []) or []

    for suit in suits:
        if str(suit.get('id', '')).lower() != str(suit_id).lower():
            continue
        card_level = None
        for card in suit.get('cards', []) or []:
            if str(card.get('id', '')).lower() == str(card_id).lower():
                card_level = card.get(size_token)
                break
        return card_level, (suit.get('backgrounds', {}) or {}).get(size_token)
    return None, None


def resolve_background(config, assets_data, base_dir, edition, card, size_key, language=None):
    """
    Resolve a card's front artwork.

    Order of preference:
      1. a per-card filename in assets.yaml (deliberate exception),
      2. the naming convention for court art, when the card is a court card,
      3. a suit-level filename in assets.yaml (that suit's default art),
      4. the naming convention for default suit art,
      5. the global default background.

    Returns ``(absolute_path, was_found)``.
    """
    assets_cfg = config.get('assets', {}) or {}
    pattern = assets_cfg.get('background_pattern', '%edition%/%suit%-%size%-%variant%.png')
    image_dir = assets_cfg.get('image_dir', 'Backgrounds')
    size_token = asset_key(config, size_key)
    stem = suit_asset_id(config, edition, card.get('suit_id', ''))

    def build(variant):
        return (pattern
                .replace('%edition%', edition)
                .replace('%suit%', stem)
                .replace('%size%', size_token)
                .replace('%variant%', variant))

    card_override, suit_override = _assets_override(
        assets_data, edition, card.get('suit_id', ''), card.get('card_id', ''), size_token)

    candidates = []
    if card_override:
        candidates.append(card_override)
    if is_court(card, config, language):
        candidates.append(build('court'))
    if suit_override:
        candidates.append(suit_override)
    candidates.append(build('default'))

    global_default = ((assets_data or {}).get('default', {}) or {}).get('backgrounds', {}) or {}
    if global_default.get(size_token):
        candidates.append(global_default[size_token])

    for candidate in candidates:
        full = resolve_asset_path(base_dir, config, os.path.join(image_dir, candidate))
        if os.path.exists(full):
            return full, True

    last = resolve_asset_path(base_dir, config, os.path.join(image_dir, candidates[-1]))
    return last, False


def resolve_card_back(config, base_dir, edition, size_key):
    """Resolve the shared card back for an edition/size."""
    assets_cfg = config.get('assets', {}) or {}
    pattern = (edition_config(config, edition).get('card_back')
               or assets_cfg.get('card_back_pattern',
                                 '%edition%/back_of_card_%size%_expanded_outlined_6mmbleed.png'))
    image_dir = assets_cfg.get('image_dir', 'Backgrounds')
    rel = (pattern
           .replace('%edition%', edition)
           .replace('%size%', asset_key(config, size_key)))
    full = resolve_asset_path(base_dir, config, os.path.join(image_dir, rel))
    return full, os.path.exists(full)


# --------------------------------------------------------------------------
# Output naming — shared so the generator and the merger cannot drift apart
# --------------------------------------------------------------------------

def format_bleed(bleed_mm):
    """Render a bleed value the same way everywhere: 3.0 -> '3', 1.5 -> '1.5'."""
    value = float(bleed_mm)
    return str(int(value)) if value.is_integer() else str(value)


def marks_token(printers_marks):
    return 'printersmarks' if printers_marks else 'noprintersmarks'


def _fill_tokens(template, config, **tokens):
    result = template
    result = result.replace('%version%', str(config.get('project', {}).get('version', '1.0')))
    for key, value in tokens.items():
        result = result.replace('%{0}%'.format(key), str(value))
    return result


def card_pdf_name(config, edition, card_id, size_key, language, bleed_mm, printers_marks):
    template = (config.get('output', {}) or {}).get(
        'filename_format',
        'owasp_cornucopia_%edition%_%card_id%_%size%_%version%_%language%'
        '_%bleed%mmbleed_%printersmarks%.pdf')
    return _fill_tokens(template, config,
                        edition=edition, card_id=card_id, size=size_key,
                        language=language, bleed=format_bleed(bleed_mm),
                        printersmarks=marks_token(printers_marks))


def deck_pdf_name(config, edition, size_key, language, bleed_mm):
    template = (config.get('output', {}) or {}).get(
        'deck_filename_format', 'cornucopia_%edition%_%size%_%language%_%bleed%mm.pdf')
    return _fill_tokens(template, config,
                        edition=edition, size=size_key, language=language,
                        bleed=format_bleed(bleed_mm))


def zip_name(config, edition):
    template = (config.get('packaging', {}) or {}).get(
        'zip_name', 'OWASP_Cornucopia_%edition%_v%version%.zip')
    return _fill_tokens(template, config, edition=edition)


def sla_name(config, edition, card_id, size_key, language):
    template = (config.get('output', {}) or {}).get(
        'sla_filename_format', '%card_id%_%edition%_%size%_%language%_Generated.sla')
    return _fill_tokens(template, config,
                        edition=edition, card_id=card_id, size=size_key, language=language)


# --------------------------------------------------------------------------
# Export profiles
# --------------------------------------------------------------------------

def get_export_profiles(config, profile_name=None, bleed_mm=None, printers_marks=None):
    """Select export profiles, optionally narrowed by name or overridden by CLI."""
    profiles = config.get('export_profiles', []) or [
        {'name': 'default', 'bleed_mm': 3.0, 'printers_marks': False}]

    if profile_name:
        matched = [p for p in profiles if p.get('name') == profile_name]
        if not matched:
            raise ValueError(
                "No export profile named '{0}'. Available: {1}".format(
                    profile_name, ', '.join(str(p.get('name')) for p in profiles)))
        profiles = matched

    if bleed_mm is not None or printers_marks is not None:
        selected = dict(profiles[0])
        if bleed_mm is not None:
            selected['bleed_mm'] = bleed_mm
        if printers_marks is not None:
            selected['printers_marks'] = printers_marks
        return [selected]

    return profiles
