# Scripts used to build Cornucopia

## Building the Cornucopia Card Decks

Merges to the main branch will generate new DOCX and IDML files to use to print off new version of the deck but if you wish to produce these locally yourself then use the [convert.py](convert.py) scipt to do this:

```bash
(cornucopia) ➜  cornucopia git:(master) ✗ python ./scripts/convert.py --help
usage: convert.py [-h] [-i INPUTFILE] [-v VERSION] [-o OUTPUTFILE] [-p] [-d] [-l LANGUAGE] [-t TEMPLATE] [-e EDITION]
                  [-lt LAYOUT]

Tool to output OWASP Cornucopia playing cards into different file types and languages.
Example usage: $ scripts/convert.py --pdf -lt guide -l es -v 2.2
Example usage: $ scripts/convert.py -t tarot -l en -lt cards  -v 5.0 -e eop -i ./resources/templates/eop_ver_cards_tarot_lang.idml -o ./output/eop-5.0-cards-en.idml
Example usage: c:\cornucopia\scripts\convert.py -t bridge -lt cards -l fr -v 2.2 -o 'my_output_folder\owasp_cornucopia_edition_version_layout_language_template.idml'

options:
  -h, --help            show this help message and exit
  -i INPUTFILE, --inputfile INPUTFILE
                        Input (template) file to use.
                        Default=resources\templates\owasp_cornucopia_edition_ver_layout_document_template_lang.(docx|idml)
                        Template type is dependent on the file (-o) specified.
  -v VERSION, --version VERSION
                        Output version to produce. [`all`, `latest`, `1.0`, `1.1`, `2.2`, `3.0`]
                        For the Website edition:
                        Version 3.0 will deliver cards mapped to ASVS 5.0
                        Version 2.2 and 2.0x will deliver cards mapped to ASVS 4.0
                        For the Mobile edition:
                        Version 1.1 and 1.0x will deliver cards mapped to MASVS 2.0
                        Version all will deliver all versions of cornucopia
                        Version latest will deliver the latest deck versions of cornucopia
                        You can also specify another version explicitly if needed. If so, there needs to be a yaml file in the source folder where the name contains the version code. Eg. edition-template-ver-lang.yaml
  -o OUTPUTFILE, --outputfile OUTPUTFILE
                        Specify a path and name of output file to generate. (caution: existing file will be overwritten).
                        Eg. output\owasp_cornucopia_edition_ver_layout_document_template_lang.(docx|pdf|idml)
  -p, --pdf             Whether to generate a pdf in addition to the printable document. Does not generate a pdf by default. Only docx can be converted to pdf for the moment.
  -d, --debug           Output additional information to debug script
  -l LANGUAGE, --language LANGUAGE
                        Output language to produce. [`en`, `es`, `fr`, `nl`, `no-nb`, `pt-br`, `pt-pt`, `it`, `ru`] you can also specify your own language file. If so, there needs to be a yaml file in the source folder where the name ends with the language code. Eg. edition-template-ver-lang.yaml
  -t TEMPLATE, --template TEMPLATE
                        From which template to produce the document. [`bridge`, `bridge_qr`, `tarot` or  `tarot_qr`]
                        Templates need to be added to ./resource/templates or specified with (-i or --inputfile)
                        Bridge cards are 2.25 x 3.5 inch and have the mappings printed on them,
                        tarot cards are 2.75 x 4.75 (71 x 121 mm) inch large,
                        qr cards have a QRCode that points to an maintained list.
                        You can also speficy your own template. If so, there needs to be a file in the templates folder where the name contains the template code. Eg. owasp_cornucopia_edition_ver_layout_template_lang.idml
  -e EDITION, --edition EDITION
                        Output decks to produce. [`all`, `webapp` or `mobileapp`]
                        The various Cornucopia decks. `web` will give you the Website App edition.
                        `mobileapp` will give you the Mobile App edition.
                        You can also speficy your own edition. If so, there needs to be a yaml file in the source folder where the name contains the edition code. Eg. edition-template-ver-lang.yaml
  -lt LAYOUT, --layout LAYOUT
                        Document layouts to produce. [`all`, `guide`, `leaflet` or `cards`]
                        The various Cornucopia document layouts.
                        `cards` will output the high quality print card deck.
                        `guide` will generate the docx guide with the low quality print deck.
                        `leaflet` will output the high quality print leaflet.
                        You can also speficy your own layout. If so, there needs to be a yaml file in the source folder where the name contains the layout code. Eg. edition-layout-ver-lang.yaml
```

## Additional Utility Scripts

### Converting CAPEC Data

The `scripts/convert_capec.py` script converts CAPEC (Common Attack Pattern Enumeration and Classification) JSON data into Markdown format for the Cornucopia website taxonomy.

```bash
python ./scripts/convert_capec.py --help
usage: convert_capec.py [-h] [-o OUTPUT_PATH] [-i INPUT_PATH] [-d]
Convert CAPEC JSON to Cornucopia format

options:
  -h, --help            show this help message and exit
  -o OUTPUT_PATH, --output-path OUTPUT_PATH
                        Directory to store converted CAPEC files
  -i INPUT_PATH, --input-path INPUT_PATH
                        Path to read CAPEC JSON files from
  -d, --debug           Output additional information to debug script
```

**Example usage:**

```bash
# Convert CAPEC data using default paths
python scripts/convert_capec.py

# Convert with custom input and output paths
python scripts/convert_capec.py -i data/capec-3.9/3000.json -o cornucopia.owasp.org/data/taxonomy/en/CAPEC-3.9

# Enable debug logging
python scripts/convert_capec.py -d
```

**Default paths:**

- Input: `cornucopia.owasp.org/data/capec-3.9/3000.json`
- Output: `cornucopia.owasp.org/data/taxonomy/en/CAPEC-3.9/`

The script creates individual Markdown files for each CAPEC attack pattern with descriptions and links to the official CAPEC database.

### Converting CAPEC Mappings to ASVS Format

The `scripts/convert_capec_map_to_asvs_map.py` script processes webapp-mappings YAML files and generates a consolidated CAPEC-to-ASVS (Application Security Verification Standard) mapping file.

```bash
python ./scripts/convert_capec_map_to_asvs_map.py --help
usage: convert_capec_map_to_asvs_map.py [-h] [-i INPUT_PATH] [-o OUTPUT_PATH] [-d]

Convert webapp-mappings YAML to CAPEC-to-ASVS mapping format

options:
  -h, --help            show this help message and exit
  -i INPUT_PATH, --input-path INPUT_PATH
                        Path to input webapp-mappings YAML file
  -o OUTPUT_PATH, --output-path OUTPUT_PATH
                        Directory to save converted CAPEC-to-ASVS mapping and ASVS-to-CAPEC mapping YAML files
  -v, --version         Version of the output file (e.g., 3 for 3.0)
  -e, --edition.        edition of the output file (e.g., webapp or mobileapp)
  -d, --debug           Output additional information to debug script
```

**Example usage:**

```bash
# Convert mappings using default paths
python scripts/convert_capec_map_to_asvs_map.py

# Convert with custom input and output paths
python scripts/convert_capec_map_to_asvs_map.py -i source/webapp-mappings-3.0.yaml -o source/webapp-capec-3.0.yaml

# Enable debug logging
python scripts/convert_capec_map_to_asvs_map.py -d
```

**Default paths:**

- Input: `source/webapp-mappings-3.0.yaml`
- Output: `source/webapp-capec-3.0.yaml`

The script:

1. Reads CAPEC mappings from the `suits -> cards -> capec_map` structure
2. Merges all OWASP ASVS requirements for each unique CAPEC code
3. Outputs a unified YAML file mapping CAPEC codes to their associated ASVS requirements

**Output format:**

```yaml
54:
  owasp_asvs: [4.3.2, 13.2.2, 13.4.1, ...]
116:
  owasp_asvs: [13.2.2, 15.2.3, ...]
```

### Enriching CAPEC Mappings with Names

The `scripts/capec_map_enricher.py` script enriches CAPEC-to-ASVS mapping files by adding descriptive names from the CAPEC JSON catalog to each CAPEC entry.

```bash
python ./scripts/capec_map_enricher.py --help
usage: capec_map_enricher.py [-h] [-c CAPEC_JSON] [-i INPUT_PATH] [-v VERSION] [-e EDITION]
                              [-s SOURCE_DIR] [-o OUTPUT_PATH] [-d]

Enrich CAPEC mappings with names from CAPEC JSON catalog

options:
  -h, --help            show this help message and exit
  -c CAPEC_JSON, --capec-json CAPEC_JSON
                        Path to CAPEC JSON file (3000.json)
  -i INPUT_PATH, --input-path INPUT_PATH
                        Path to input CAPEC mapping YAML file (overrides edition/version)
  -v VERSION, --version VERSION
                        Version of the CAPEC mapping file (e.g., 3.0)
  -e EDITION, --edition EDITION
                        Edition of the CAPEC mapping file (e.g., webapp or mobileapp)
  -s SOURCE_DIR, --source-dir SOURCE_DIR
                        Source directory containing CAPEC mapping files
  -o OUTPUT_PATH, --output-path OUTPUT_PATH
                        Path to save enriched CAPEC mapping YAML file (default: overwrites input)
  -d, --debug           Output additional information to debug script
```

**Example usage:**

```bash
# Enrich using default paths
python scripts/capec_map_enricher.py

# Enrich with custom input and output paths
python scripts/capec_map_enricher.py -i source/webapp-capec-3.0.yaml -o source/webapp-capec-3.0-enriched.yaml

# Enrich specific edition and version
python scripts/capec_map_enricher.py -e webapp -v 3.0

# Enable debug logging
python scripts/capec_map_enricher.py -d
```

**Default paths:**

- CAPEC JSON: `cornucopia.owasp.org/data/capec-3.9/3000.json`
- Input: `source/edition-capec-latest.yaml` (or `source/edition-capec-version.yaml` if version specified)
- Output: Same as input (overwrites by default)

The script:

1. Extracts CAPEC ID and Name from the JSON catalog (`Attack_Pattern_Catalog -> Attack_Patterns -> Attack_Pattern`)
2. Loads existing CAPEC-to-ASVS mappings from YAML file
3. Enriches each CAPEC entry by adding a `name` field alongside the existing `owasp_asvs` mappings
4. Saves the enriched mappings back to YAML format

**Input format:**

```yaml
54:
  owasp_asvs: [4.3.2, 13.2.2, 13.4.1]
116:
  owasp_asvs: [13.2.2, 15.2.3]
```

**Output format:**

```yaml
54:
  name: "Session Credential Falsification through Prediction"
  owasp_asvs: [4.3.2, 13.2.2, 13.4.1]
116:
  name: "Excavation"
  owasp_asvs: [13.2.2, 15.2.3]
```

## Contributing to Development

### LibreOffice Installation

LibreOffice is required to convert `.docx` files to `.pdf` format.

- **Windows**: `winget install -e --id TheDocumentFoundation.LibreOffice`
- **Mac OS X**: `brew install --cask libreoffice`
- **Ubuntu**: `sudo apt update && sudo apt install libreoffice`

### Dev setup for the Cornucopia Converter

For copi.owasp.org and cornucopia.owasp.org see separate README.md
On Mac OSX and Ubuntu you may not need to go through all of these steps, but this should at least be a bulletproof way of getting started.

    pip install -r requirements.txt --user
    # To get path to your python executable, you can
    # python -c "import os, sys; print(os.path.dirname(sys.executable))" 
    python -m pipenv shell --python "{path to python}"
    python -m pip install -r requirements.txt
    python -m pipenv install --dev


### Coding style 

Before you push your changes please format files with

```bash
make fmt
```

#### Coding Style Check on Windows

Install shfmt

    winget install --id=mvdan.shfmt  -e

Run Coding Style Check

    shfmt -l -w .
    pipenv run black --line-length=120 .
    pipenv run flake8 --max-line-length=120 --max-complexity=10 --ignore=E203,W503 --exclude ./.venv/
    pipenv run mypy --namespace-packages --strict ./scripts/

### Docker container

You may run the converter inside a docker container. This is useful if you do not want to install all dependencies on your local machine and not worry about permission issues.
You can also run the converter inside a docker container. To build the container run:

```powershell
docker build --target pipenv `
  --build-arg user_id=1000 `
  --build-arg group_id=1000 `
  --build-arg home=/home/builder `
  --build-arg workdir=/workspace `
  -t cornucopia-converter .
```

To install dependencies inside the container run:

```powershell
    docker run --rm -v ${PWD}:/workspace cornucopia-converter run pip install -r requirements.txt
    docker run --rm -v ${PWD}:/workspace cornucopia-converter install --dev
```

To login to the container and mount the current working directory inside the container run:

```powershell
    docker run --rm -it --entrypoint "/bin/bash" -v ${PWD}:/workspace cornucopia-converter
```

Run the converter tests inside the container:

```powershell

    #unit tests
    docker run --rm -v ${PWD}:/workspace cornucopia-converter run coverage run --append --branch --omit "*_?test.py,*/.local/*" --module unittest discover --verbose --start-directory "tests/scripts" --pattern "*_utest.py"

    #integration tests
    docker run --rm -v ${PWD}:/workspace cornucopia-converter run coverage run --append --branch --omit "*_?test.py,*/.local/*" --module unittest discover --verbose --start-directory "tests/scripts" --pattern "*_utest.py"

    #See code coverage
    docker run --rm -v ${PWD}:/workspace cornucopia-converter run coverage report scripts/convert.py

```

### Static analysis

run static analysis checks

```bash
make static-check
```

### Tests

run all available smoke, unit and integration tests

```bash
make test
```

#### Testing on windows

Unit tests:

    pipenv run coverage run --append --branch --omit "*_?test.py,*/.local/*" --module unittest discover --verbose --start-directory "tests/scripts" --pattern "*_utest.py"

Integration tests:

    pipenv run coverage run --append --branch --omit "*_?test.py,*/.local/*" --module unittest discover --verbose --start-directory "tests/scripts" --pattern "*_itest.py"

###  Code coverage

check that your code have sufficient test coverage

```bash
make coverage-check
```

#### Code coverage check on windows

    pipenv run coverage xml
    pipenv run coverage report --fail-under 85

### Developing fuzzers

We are using ClusterFuzzlite as a continuous fuzzing solution in order to run tests locally you need oss-fuzz.
For more information on how to write tests see: https://google.github.io/clusterfuzzlite/build-integration/python-lang/

How to test locally:

```bash
export PATH_TO_PROJECT=$(pwd)
cd ../
git clone https://github.com/google/oss-fuzz
cd ../oss-fuzz
python infra/helper.py build_image --external $PATH_TO_PROJECT
python infra/helper.py build_fuzzers --external $PATH_TO_PROJECT --sanitizer address 
python infra/helper.py check_build --external $PATH_TO_PROJECT --sanitizer address
```

### Golden files

All python unit tests with fixtures in `testdata` folder support updating _golden_ files from real output of tests

```bash
make python-test-update-golden-files
```

this is useful if you have made changes in code and you do not want to update
all fixtures manually or when you have updated inputs and therefore fixtures
needs to be updated.

### Improve development experience

Instead of manually running those commands, you may wish to add them to the Git
pre-commit hook. This will mean that the commands will run automatically
whenever you commit your changes. If the command fails, then the commit will not
be completed.

1. In the project root, open your `.git` directory
2. Create a file called `pre-commit` (no suffix)
3. Add the following code:

    ```bash
    #!/bin/sh

    make fmt
    make static-check
    make test
    make coverage-check
    ```

4. Save the file.
5. All done. Now whenever you commit changes, Git will run the commands in that
   file.