# PDF Automation — Installation and Usage

How to install the deck generator and produce print-ready PDFs.

This pipeline builds OWASP Cornucopia card decks from the translated card data,
for any edition, language and card format, without opening Scribus by hand.

---

## 1. Prerequisites

| Requirement | Notes |
|---|---|
| **Scribus 1.6 or newer** | Needed for PDF export only |
| **Python 3.8+** | Your normal system Python, for the merge step |
| **Noto Sans fonts** | See §3 — a missing font is substituted *silently* |

Scribus is at <https://www.scribus.net/downloads/>.

### The one thing that surprises people

**Scribus ships its own private Python.** It does not use the Python on your
PATH, and it cannot see packages you installed with a normal `pip install`.

That means there are **two** environments to set up:

| Environment | Runs | Needs |
|---|---|---|
| Scribus's bundled Python | `generate_deck.py` | `pyyaml`, `qrcode`, `pypng` |
| Your system Python | `merge_pdfs.py` | `pyyaml`, `pymupdf` |

Getting this wrong is the most common failure, and it shows up as
`ModuleNotFoundError: No module named 'yaml'` when you run the generator.

---

## 2. Install the Python packages

### Scribus's Python

Scribus bundles a `python.exe` with `pip` already available.

**Windows** — adjust the version number in the path to match your install:

```bat
"C:\Program Files\Scribus 1.6.6\python\python.exe" -m pip install pyyaml qrcode pypng
```

If you get a permissions error, run the terminal as Administrator — the path is
under `Program Files`.

**Linux / macOS** — Scribus normally uses the system Python there, so:

```bash
python3 -m pip install pyyaml qrcode pypng
```

`pypng` matters: `qrcode` uses Pillow by default, but Pillow is awkward to
install into a bundled interpreter. With `pypng` present, `qrcode` falls back to
a pure-Python PNG writer and no compiled dependency is needed.

### Your system Python

```bash
python -m pip install pyyaml pymupdf
```

### Check both

```bash
python -c "import yaml, pymupdf; print('system python OK')"
```

For Scribus's side, the `--dry-run` in §5 is the real check.

---

## 3. Install the fonts

The templates reference these families:

- **Noto Sans** — Light, Medium, Medium Italic, ExtraBold
- **Noto Sans Devanagari** — Light, Medium, Regular *(needed for Hindi)*

Download from [Google Fonts](https://fonts.google.com/noto), then install:

- **Windows** — select the `.ttf` files, right-click, *Install for all users*
- **macOS** — open in Font Book and click *Install*
- **Linux** — copy to `~/.local/share/fonts/` and run `fc-cache -f`

**Restart Scribus afterwards** — it scans for fonts at startup.

> Scribus substitutes a missing font silently. The PDF still exports, and the
> problem only shows up when you look closely at a proof. If text looks wrong,
> check fonts first.

---

## 4. Where things live

Everything is inside the repository already:

```
scripts/pdf_generation/     the tool
    generate_deck.py            the engine
    merge_pdfs.py               the deck assembler
    cornucopia_common.py        shared code used by both
    pdf_config.yaml             build settings
    assets.yaml                 per-suit colours
    small_master.sla            Bridge template
    big_master.sla              Tarot template
    output/                     generated PDFs (gitignored)

source/                     card data, read directly -- not copied
resources/card_artwork/     card faces and backs, per edition
```

The card data is the repository's existing `source/` files, read in place, so
there is no second copy to keep in step. Run the commands below from
`scripts/pdf_generation/`; `output/` is created automatically.

---

## 5. First check — a dry run

This validates your setup without exporting anything. It takes a few seconds
and does not need Scribus:

```bash
cd scripts/pdf_generation
python generate_deck.py --dry-run
```

Expected:

```
Building 32 target(s) across edition(s): companion, mobileapp, webapp
Scribus not detected — PDF export disabled (.sla only)

--- webapp | EN | bridge ---
  80 cards, 7 suit(s), 2 joker(s)
  all artwork resolved

--- webapp | EN | tarot ---
  80 cards, 7 suit(s), 2 joker(s)
  all artwork resolved
...
Done. 2556 card file(s), 0 PDF(s), 0 warning(s).
```

`Scribus not detected` is expected here — you ran it with system Python. The
line confirms it would fall back to writing `.sla` files only.

What to look for:

- three editions listed: `webapp`, `mobileapp`, `companion`
- `all artwork resolved` on each target
- `0 warning(s)` at the end

`source/` also holds card data for decks this tool does not build — EoP, DBD,
Cumulus, Elevation of MLsec. They are excluded because `generation_targets`
names the three editions explicitly, rather than building everything it finds.

---

## 6. Build one card

The fastest end-to-end proof. Roughly ten seconds.

**Windows:**

```bat
"C:\Program Files\Scribus 1.6.6\Scribus.exe" --no-splash --no-gui ^
  --python-script generate_deck.py ^
  --edition companion --language en --size bridge --cards LLM2
```

**Linux / macOS:**

```bash
scribus --no-splash --no-gui \
  --python-script generate_deck.py \
  --edition companion --language en --size bridge --cards LLM2
```

You can also run it from the Scribus GUI via **Script → Execute Script**, though
you cannot pass arguments that way — it will build everything in
`pdf_config.yaml`, so set `generation_targets` first.

Expected, in `build_log.txt`:

```
--- companion | EN | bridge ---
  1 cards, 6 suit(s), 0 joker(s)
  generated 1 card file(s), 1 PDF(s)

Done. 1 card file(s), 1 PDF(s), 0 warning(s).
```

And in `output/`:

```
LLM2_companion_bridge_en_Generated.sla
owasp_cornucopia_companion_LLM2_bridge_3.0_en_3mmbleed_noprintersmarks.pdf
```

Open the PDF. It should be two pages — the card front, then the card back —
at 62 × 93 mm, with a 3 mm bleed on every edge.

---

## 7. Build a deck

Drop `--cards` to build a full one:

```bash
scribus --no-splash --no-gui --python-script generate_deck.py \
  --edition companion --language en
```

That is 78 cards in both formats, 156 PDFs, around 15 minutes.

Flags combine, and repeat to select several:

```bash
# one language, both formats
--edition webapp --language en

# two languages
--edition webapp --language en --language fr

# everything discoverable
(no flags)

# resume after an interruption
--skip-existing
```

Allow roughly **6 seconds per card**. A full build of all editions and
languages is about 2,556 cards, so several hours — and CMYK output is large,
so budget a few GB of disk.

---

## 8. Merge into decks

This runs in your **system** Python, not Scribus:

```bash
python merge_pdfs.py --edition companion
```

Expected:

```
Merging profile: bleed 3mm | noprintersmarks
--- companion | bridge | EN --- matched 78/78
    wrote cornucopia_companion_bridge_en_3mm.pdf (156 pages)
--- companion | tarot | EN --- matched 78/78
    wrote cornucopia_companion_tarot_en_3mm.pdf (156 pages)

Skipped packaging (pass --zip or set packaging.create_zip to enable).

Done. 2 deck(s) merged.
```

`matched 78/78` is the number to check — anything less means some card PDFs are
missing, and the details are written to `merge_gaps.json`.

Each deck interleaves the cards **back page then front page**, which is what a
duplex printer expects.

To package them:

```bash
python merge_pdfs.py --edition companion --zip
```

Zipping is off unless you ask for it, so building one deck never produces a
large archive as a side effect.

---

## 9. Configuration

Nothing above requires editing Python. The two YAML files cover the rest.

### `pdf_config.yaml`

Set defaults so you do not have to type flags. Each accepts `"all"` or a list:

```yaml
generation_targets:
  editions: "all"
  languages: ["en", "fr"]
  sizes: ["bridge"]
```

Command-line flags override these.

**Colour space** — `cmyk` is the default, as the PDFs are primarily for print.
CMYK preserves the values defined in `assets.yaml` rather than converting them.
Use `rgb` for screen, or for print-on-demand vendors that ask for it:

```yaml
output:
  color_mode: "cmyk"     # or "rgb"
```

CMYK files are roughly three times larger, because images carry four channels
instead of three.

**Bleed and printer's marks** — each profile produces its own PDF per card, so a
production file and a proof can be made in one run:

```yaml
export_profiles:
  - name: "print_3mm"
    bleed_mm: 3.0
    printers_marks: false
  - name: "proof_6mm"
    bleed_mm: 6.0
    printers_marks: true
```

**Font sizes** — if a translation overflows its frame, adjust the offset for
that language. Values are points, applied on top of the base size:

```yaml
font_scaling:
  attack_text:
    default: 0.0
    hi: -1.0
    ru: -0.75
```

### `assets.yaml`

Per-suit colours, as an existing Scribus swatch name or as CMYK values, which
get injected into the template at build time:

```yaml
companion:
  suits:
    - id: LLM
      color: {c: 30, m: 87, y: 31, k: 17}     # pip card numbers
      court_color: {c: 0, m: 0, y: 0, k: 12}  # optional; defaults to white
```

---

## 10. Adding content

**A new language** — add the card file to `source/` using the existing naming,
and rerun. Nothing else:

```
source/webapp-cards-3.0-de.yaml
```

**A new edition** — four things:

1. card data in `source/`, named `<edition>-cards-<version>-<lang>.yaml`
2. artwork in `resources/card_artwork/<edition>/`, named
   `<suit>-<small|big>-<default|court>.png`
3. suit colours in `assets.yaml`
4. the edition added to `generation_targets.editions`, with its
   `data_version` under `editions:`

If the edition has jokers, name the joker suit in `pdf_config.yaml`:

```yaml
editions:
  myedition:
    joker_suits: ["wc"]
```

If it has none, leave the entry out — Companion has no jokers and needs no
special handling.

Run `--dry-run` afterwards to confirm everything resolves.

---

## 11. Troubleshooting

**`ModuleNotFoundError: No module named 'yaml'`**
The package went into the wrong Python. Scribus uses its own — see §2.

**`Scribus not detected — PDF export disabled`**
You ran the generator with system Python. It writes `.sla` files only; use the
`--python-script` form from §6 to export PDFs.

**A language is missing from the build**
Its card file does not match the expected naming, or belongs to a different
`data_version` than the one pinned for that edition in `pdf_config.yaml`.

**`WARNING: No suit colour mapped for …`**
That suit has no entry in `assets.yaml`, so it falls back to the default grey.

**A deck you did not expect gets built**
`generation_targets.editions` lists which editions to build. Setting it to
`"all"` picks up every deck with card data in `source/`, including EoP and DBD.

**`WARNING: Artwork missing for card …`**
A filename does not match `<suit>-<small|big>-<default|court>.png`. The warning
gives the path it looked for.

**Text is cut off on a card**
The frame overflowed. Increase the negative offset for that language under
`font_scaling` and rebuild — Scribus does not render text that does not fit, so
it truncates silently.

**The PDF looks like the wrong font**
The font is not installed, and Scribus substituted one without complaint.
Check §3 and restart Scribus.

**`matched 70/80` when merging**
Some card PDFs are missing. `merge_gaps.json` lists which; rerun the generator
for those, or use `--skip-existing` to fill the gaps.

---

## 12. Command reference

```bash
# generate_deck.py — run inside Scribus for PDF export
--edition NAME        edition to build (repeatable)
--language CODE       language to build (repeatable)
--size NAME           bridge or tarot (repeatable)
--cards A,B,C         only these card IDs
--profile NAME        a single export profile
--output-dir PATH     write elsewhere
--config PATH         use a different config file
--dry-run             report and exit
--skip-existing       skip cards already exported

# merge_pdfs.py — run in system Python
--edition NAME        edition to merge (repeatable)
--language CODE       language to merge (repeatable)
--size NAME           bridge or tarot (repeatable)
--bleed-mm N          which bleed variant to merge
--printers-marks      merge the marks variant
--zip / --no-zip      package, or do not
--dry-run             report and exit
```

Every run writes `build_log.txt` and `build_manifest.json`, recording what was
built and any warnings — the record to check after a long run.
