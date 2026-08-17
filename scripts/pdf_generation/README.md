# PDF Automation — Installation and Usage

The code in this folder generates print-ready PDF card decks from the Cornucopia card data. The intention is that it will be run automatically to produce the PDFs for each release, but it can also be run locally on demand using the instructions below.

Running it locally lets you generate some or all of the Cornucopia editions, in any of the available languages, or even a single suit or an individual card. It also means the card text in the referenced `.yaml` files can be modified locally — to suit a particular application scope, to use technology-specific terminology, or to meet an organisation's needs — separately from what is in the official Cornucopia repository, with the custom PDFs then generated manually using these scripts.

---

## 1. Prerequisites

| Requirement | Notes |
|---|---|
| **Scribus 1.6 or newer** | Needed for PDF export only |
| **Python 3.8 or newer** | Your normal system Python, for the merge step |
| **Noto Sans fonts** | See §4 — most are already in this repository |

Commands below use `python3`, which is what macOS and most Linux distributions provide. On Windows the command is usually `python` (or `py`), so substitute accordingly.

### Installing Scribus

Go to the [Scribus downloads page](https://www.scribus.net/downloads/) and find the section headed *Currently the stable branch is the 1.6.x series*. Choose the download for your operating system:

- **Windows** — the `.exe` installer, 64-bit unless you know you need otherwise
- **macOS** — the `.dmg` disk image
- **Linux** — your distribution's package, or the AppImage/Flatpak build

If a checksum is published next to the download, verify it before installing. On macOS or Linux, `shasum -a 256 <file>` prints the SHA-256 of what you downloaded; compare it with the published value. On Windows, use `Get-FileHash <file>` in PowerShell.

Then install it the usual way for your platform — run the installer on Windows, drag Scribus to Applications on macOS, or use your package manager on Linux.

### The one thing that surprises people

**Scribus runs scripts in its own Python, not the one on your PATH.** On Windows it bundles its own interpreter outright; on macOS and Linux it uses a system one that is frequently a different installation from the `python3` you type. Either way, it usually cannot see packages you installed with a normal `pip install`.

That means there are **two** environments to set up:

| Environment | Runs | Needs |
|---|---|---|
| Scribus's bundled Python | `generate_deck.py` | `pyyaml`, `qrcode`, `pypng`, `defusedxml` |
| Your system Python | `merge_pdfs.py` | `pyyaml`, `pymupdf` |

Getting this wrong is the most common failure, and it shows up as `ModuleNotFoundError: No module named 'yaml'` when you run the generator.

---

## 2. Get the repository

The scripts read the card data and artwork from elsewhere in this repository, so you need a local copy of the whole thing rather than just this folder:

```bash
git clone https://github.com/OWASP/cornucopia.git
cd cornucopia
```

If you already have a clone, make sure it is up to date with `git pull`.

Everything the generator needs is in the repository — you do not have to download card text or artwork separately.

---

## 3. Install the Python packages

### Scribus's Python

**Windows** — Scribus bundles its own `python.exe` with `pip` already available. Adjust the path to match where you installed Scribus and which version you have:

```bat
"C:\Program Files\Scribus 1.6.6\python\python.exe" -m pip install pyyaml qrcode pypng defusedxml
```

If that fails with a permissions error, you need to run the command with administrative rights. Click Start, type `cmd`, right-click **Command Prompt** and choose **Run as administrator**, then run the command again in that window. The same applies if you prefer PowerShell.

**macOS and Linux** — Scribus uses a Python interpreter that is often *not* the `python3` on your PATH. On macOS in particular, if your `python3` came from Homebrew, Scribus will not see anything you install with it, and you will get `ModuleNotFoundError: No module named 'yaml'` even though the install succeeded.

The reliable approach is to install the packages into a folder of your own and point Scribus at it:

```bash
python3 -m pip install --target ~/cornucopia-python-libs pyyaml qrcode pypng defusedxml
```

Then **export** `PYTHONPATH` so Scribus inherits it:

```bash
export PYTHONPATH=~/cornucopia-python-libs
```

The `export` matters. Writing `PYTHONPATH=~/cornucopia-python-libs` on a line by itself sets a shell variable that is *not* passed to programs you run afterwards, so Scribus would still report the module as missing. Either use `export` as above, or put the assignment and the command on the same line.

Check it took effect before going further:

```bash
echo $PYTHONPATH
```

That must print the path. It applies to the current terminal window only, so run it again in any new one.

All of these are pure Python, so they work whichever interpreter version Scribus uses.

If your Scribus does share the system Python — run the check below to find out — then a plain `python3 -m pip install pyyaml qrcode pypng defusedxml` is enough, and you can drop the `PYTHONPATH` prefix. Add `--user` if you hit a permissions error.

`pypng` matters: `qrcode` draws with Pillow by default, and Pillow is a compiled package that is awkward to install into a bundled interpreter. `pypng` is pure Python, and the generator asks for it by name, so no compiled dependency is needed and every machine produces an identical QR code.

`defusedxml` is a hardened XML parser, used for reading the Scribus templates. It is pure Python like the others. It is the one package here that is optional — without it the generator falls back to the standard library parser and still works — but install it, since the security scanner in CI expects it.

### Your system Python

```bash
python3 -m pip install pyyaml pymupdf
```

### Check it worked

`check_environment.py` reports which interpreter is running and whether it can find each package. Run it **both ways** and compare — this is the quickest way to diagnose a missing module.

Through your system Python:

```bash
python3 check_environment.py
```

And through Scribus, using the command for your platform from §7:

```bash
/Applications/Scribus.app/Contents/MacOS/Scribus --no-splash --no-gui \
  --python-script check_environment.py
```

Each run prints its `Install prefix`. If the two differ — which is normal — then packages installed with one are invisible to the other, and they need installing for each. The report also lists exactly which packages that interpreter is missing, and writes a copy to `check_environment.txt`.

---

## 4. Install the fonts

The fonts are already in this repository, so you can install them from your local clone rather than downloading anything.

| Family | Location in this repository | Needed for |
|---|---|---|
| **Noto Sans** — Light, Medium, Medium Italic, ExtraBold | `resources/templates/Fonts/NotoSans/` | every language, including Russian and Ukrainian, since Noto Sans covers Cyrillic |
| **Noto Sans Devanagari** — Light, Medium, Regular | `resources/templates/Fonts/NotoSansDevanagari/` | **only Hindi**, the one language whose script Noto Sans does not cover |

If you would rather fetch them online, they are also in the repository on GitHub at [resources/templates/Fonts](https://github.com/OWASP/cornucopia/tree/master/resources/templates/Fonts), or from [Google Fonts](https://fonts.google.com/noto) as a last resort.

To install:

- **Windows** — select the `.ttf` files, right-click, then *Install for all users*
- **macOS** — double-click each file and click *Install Font*, or drag them into Font Book
- **Linux** — copy them to `~/.local/share/fonts/` and run `fc-cache -f -v`

**Restart Scribus after installing fonts**, because it only scans for fonts at startup. Quit it completely rather than just closing the window:

- **Windows** — close all Scribus windows, then start it again
- **macOS** — *Scribus → Quit Scribus*, or ⌘Q. Closing the window is not enough; the app keeps running.
- **Linux** — close the application, then start it again

> Scribus substitutes a missing font silently. The PDF still exports, and the problem only shows up when you look closely at a proof. If text looks wrong, check the fonts first.

---

## 5. Where things live

This folder holds the tool:

```
scripts/pdf_generation/
    assets.yaml                 per-suit colours
    big_master.sla              big (Tarot) template
    check_environment.py        reports which Python is in use, and what it can find
    cornucopia_common.py        shared code used by both scripts
    generate_deck.py            the engine
    merge_pdfs.py               the deck assembler
    pdf_config.yaml             build settings
    README.md                   this instruction file
    small_master.sla            small (Bridge) template
    output/                     generated PDFs and logs (gitignored)
```

It reads these files from elsewhere in the repository:

| What | Where | Notes |
|---|---|---|
| Card text | `source/<edition>-cards-<version>-<language>.yaml` | e.g. `source/webapp-cards-3.0-en.yaml`. Read in place, never copied, so there is no second copy to keep in step. Edit these to customise card text. |
| Card artwork | `resources/card_artwork/<edition>/` | Card faces and backs, as PNG |
| Fonts | `resources/templates/Fonts/` | Installed onto your system, see §4 |

Nothing else in the repository is used. Run the commands below from `scripts/pdf_generation/`; `output/` is created automatically.

---

## 6. First check — a dry run

This validates your setup without exporting anything. It takes a few seconds and does not need Scribus:

```bash
cd scripts/pdf_generation
python3 generate_deck.py --dry-run
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

`Scribus not detected` is expected here, because you ran it with system Python. The line confirms it would fall back to writing `.sla` files only.

What to look for:

- three editions listed: `webapp`, `mobileapp`, `companion`
- `all artwork resolved` on each target
- `0 warning(s)` at the end

`source/` also holds card data for decks this tool does not build, such as EoP, DBD, Cumulus and Elevation of MLsec. They are excluded because `generation_targets` names the three editions explicitly, rather than building everything it finds.

---

## 7. Build one card

The fastest end-to-end proof — a few seconds on most machines.

### Finding the Scribus command

Scribus is a desktop application, so on macOS and Windows there is normally **no `scribus` command on your PATH** — you have to call the executable inside the application. You do not need Scribus to be open; the command starts its own instance and closes it again. It is easiest if the app is *not* already running.

- **macOS** — the executable lives inside the application bundle:

  ```bash
  /Applications/Scribus.app/Contents/MacOS/Scribus
  ```

  If you installed it elsewhere, find it with `ls -d /Applications/Scribus*.app` and add `/Contents/MacOS/Scribus` to the result.

- **Windows** — `"C:\Program Files\Scribus 1.6.6\Scribus.exe"`, adjusting for your install location and version.

- **Linux** — `scribus` is usually on your PATH after a package install. For Flatpak, use `flatpak run net.scribus.Scribus` instead.

### Running it

**macOS** — if you installed the packages with `--target` in §3, make sure `PYTHONPATH` is exported in this terminal first (`echo $PYTHONPATH` should print the path):

```bash
export PYTHONPATH=~/cornucopia-python-libs

/Applications/Scribus.app/Contents/MacOS/Scribus --no-splash --no-gui \
  --python-script generate_deck.py \
  --edition companion --language en --size bridge --cards LLM2
```

**Windows:**

```bat
"C:\Program Files\Scribus 1.6.6\Scribus.exe" --no-splash --no-gui ^
  --python-script generate_deck.py ^
  --edition companion --language en --size bridge --cards LLM2
```

**Linux:**

```bash
scribus --no-splash --no-gui \
  --python-script generate_deck.py \
  --edition companion --language en --size bridge --cards LLM2
```

`--python-script` must be the **last** option, as Scribus treats everything after it as arguments for the script.

You can also run it from the Scribus GUI via **Script → Execute Script**, though you cannot pass arguments that way — it will build everything set in `pdf_config.yaml`, so adjust `generation_targets` first.

Expected, in `output/build_log.txt`:

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

Open the PDF. It should be two pages, the card front then the card back, at 62 × 93 mm with a 3 mm bleed on every edge.

Note what this step produces: **one PDF per card**, each holding that card's face and back, plus a `.sla` Scribus file per card. Combining them into a single print-ready deck is a separate, optional step covered in §9. The `.sla` files are not needed for that — the merge reads only the PDFs — so they are kept purely so you can open a card in Scribus and see what was injected.

---

## 8. Build a deck

To build complete decks rather than a single card, take the command from §7 and remove the `--size` and `--cards` options, so `--size bridge --cards LLM2` comes off the end. That builds every card in the edition, in both sizes. Replace `scribus` below with the command for your platform:

```bash
scribus --no-splash --no-gui --python-script generate_deck.py \
  --edition companion --language en
```

That is the Companion Edition's 78 cards in each size — small (Bridge) and big (Tarot) — so 156 PDFs. Expect anywhere from a couple of minutes to around twenty, depending on your machine.

Flags combine, and can be repeated to select several:

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

A full build of every edition and language is about 2,556 cards. How long that takes varies a lot with the machine, so time a small run first and scale up from there. CMYK output is large, so allow a few GB of disk space.

---

## 9. Merge into decks

This combines the per-card PDFs from §8 into one file per deck. It reads only the PDFs, so the `.sla` files are not required at this point. It runs in your **system** Python, not Scribus:

```bash
python3 merge_pdfs.py --edition companion
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

`matched 78/78` is the number to check. Anything less means some card PDFs are missing, and the details are written to `output/merge_gaps.json`.

Each deck interleaves the cards **back page then front page**, which is what a duplex printer expects.

To package them:

```bash
python3 merge_pdfs.py --edition companion --zip
```

Zipping is off unless you ask for it, so building one deck never produces a large archive as a side effect.

---

## 10. Configuration

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

**Colour space** — `cmyk` is the default, as the PDFs are primarily for print, and it preserves the values defined in `assets.yaml` rather than converting them. Use `rgb` for screen, or for print-on-demand vendors that ask for it:

```yaml
output:
  color_mode: "cmyk"     # or "rgb"
```

CMYK files are roughly three times larger, because images carry four channels instead of three.

**Bleed and printer's marks** — each profile produces its own PDF per card, so a production file and a proof can be made in one run:

```yaml
export_profiles:
  - name: "print_3mm"
    bleed_mm: 3.0
    printers_marks: false
  - name: "proof_6mm"
    bleed_mm: 6.0
    printers_marks: true
```

**Font sizes** — if a translation overflows its frame, adjust the offset for that language. Values are in points, applied on top of the base size:

```yaml
font_scaling:
  attack_text:
    default: 0.0
    hi: -1.0
    ru: -0.75
```

### `assets.yaml`

Per-suit colours, given either as an existing Scribus swatch name or as CMYK values, which get injected into the template at build time:

```yaml
companion:
  suits:
    - id: LLM
      color: {c: 30, m: 87, y: 31, k: 17}     # pip card numbers
      court_color: {c: 0, m: 0, y: 0, k: 12}  # optional; defaults to white
```

---

## 11. Adding content

**A new language** — add the card file to `source/` using the existing naming, then rerun. Nothing else is needed:

```
source/webapp-cards-3.0-de.yaml
```

**A new edition** — four things:

1. card data in `source/`, named `<edition>-cards-<version>-<lang>.yaml`
2. artwork in `resources/card_artwork/<edition>/`, named `<suit>-<small|big>-<default|court>.png`
3. suit colours in `assets.yaml`
4. the edition added to `generation_targets.editions`, with its `data_version` under `editions:`

If the edition has jokers, name the joker suit in `pdf_config.yaml`:

```yaml
editions:
  myedition:
    joker_suits: ["wc"]
```

If it has none, leave the entry out. Companion has no jokers and needs no special handling.

Run `--dry-run` afterwards to confirm everything resolves.

---

## 12. Troubleshooting

**`command not found: scribus`**
There is normally no `scribus` command on macOS or Windows. Call the executable inside the application instead, as described in §7. Opening the Scribus app does not create the command.

**`ModuleNotFoundError: No module named 'yaml'`**
The package went into the wrong Python. Scribus uses its own — see §3.

**`Scribus not detected — PDF export disabled`**
You ran the generator with system Python. It writes `.sla` files only; use the `--python-script` form from §7 to export PDFs.

**A language is missing from the build**
Its card file does not match the expected naming, or it belongs to a different `data_version` than the one pinned for that edition in `pdf_config.yaml`.

**`WARNING: No suit colour mapped for …`**
That suit has no entry in `assets.yaml`, so it falls back to the default grey.

**A deck you did not expect gets built**
`generation_targets.editions` lists which editions to build. Setting it to `"all"` picks up every deck with card data in `source/`, including EoP and DBD.

**`WARNING: Artwork missing for card …`**
A filename does not match `<suit>-<small|big>-<default|court>.png`. The warning gives the path it looked for.

**Text is cut off on a card**
The frame overflowed. Increase the negative offset for that language under `font_scaling` and rebuild. Scribus does not render text that does not fit, so it truncates silently.

**The PDF looks like the wrong font**
The font is not installed, and Scribus substituted one without complaint. Check §4, and remember to quit and restart Scribus after installing fonts.

**`matched 70/80` when merging**
Some card PDFs are missing. `output/merge_gaps.json` lists which; rerun the generator for those, or use `--skip-existing` to fill the gaps.

---

## 13. Command reference

```bash
# generate_deck.py — run through Scribus for PDF export
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

Every run writes `output/build_log.txt` and `output/build_manifest.json`, recording what was built and any warnings. These are the records to check after a long run.
