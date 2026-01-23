<img src="./resources/logos/cornucopia_logo.svg?raw=true" width="150">

[![OWASP Production Project](https://img.shields.io/badge/owasp-production%20project-brightgreen)](https://owasp.org/other_projects/)
[![OpenSSF Best Practices](https://bestpractices.coreinfrastructure.org/projects/7125/badge)](https://bestpractices.coreinfrastructure.org/projects/7125)
[![Maintainability](https://api.codeclimate.com/v1/badges/4a7cda6ef1c2932a34f9/maintainability)](https://codeclimate.com/github/OWASP/cornucopia/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/4a7cda6ef1c2932a34f9/test_coverage)](https://codeclimate.com/github/OWASP/cornucopia/test_coverage)

# OWASP Cornucopia project
OWASP Cornucopia is a mechanism in the form of a card game to assist software development teams 
identify security requirements in Agile, conventional and formal development processes. 
It is language, platform and technology agnostic. Visit: https://cornucopia.owasp.org/

## The cross-references on the Web App Edition deck relate to the following versions of other OWASP and external resources:
* [OWASP Dev Guide Web Application Checklist](https://devguide.owasp.org/en/04-design/02-web-app-checklist/)
* OWASP ASVS OWASP_Application_Security_Verification_Standard v4 (2019)
* OWASP AppSensor AppSensor_DetectionPoints
* CAPEC™ Mitre Common Attack Pattern Enumeration and Classification v3.9
* SAFECode SAFECode Practical Security Stories and Security Tasks for Agile Development Environments July 2012
* MASTG OWASP Mobile Application Security Testing Guide 1.7
* MASVS OWASP Mobile Application Security Verification Standard 2.1

## Building and Deploying the Cornucopia website

https://cornucopia.owasp.org contains the card browser for each of the cards in the cornucopia suits together with the taxonomy and in depth explaination for each of the cards in the suits.

please read [README.md](cornucopia.owasp.org/README.md)

## Building and Deploying the Cornucopia Game Engine: Copi

Copi (https://copi.owasp.org) is an online game engine where you can play Cornucopia and Elevation of Privilege. You can play all the editions of Cornucopia (website and mobile) as well as the Elevation of Privileges game.

please read [README.md](copi.owasp.org/README.md)

## Building the Cornucopia Card Decks

Merges to the main branch will generate new DOCX and IDML files to use to print off new version of the deck but if you wish to produce these locally yourself then use the ./scripts/convert.py scipt to do this:

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

## Printing

The latest printable files are released under the [pre-release](https://github.com/OWASP/cornucopia/releases/tag/pre-release). Please download final printable files from there.
The docx/pdf files can be easily printed by any desktop printer, but for the best quality use the idml InDesign files. When sending the files to a printing facility you may have to supply the fonts that has been used in order to create the work. 
In case the printing facility doesn't have the fonts at hand you'll find the installable fonts under `resources/templates/Fonts` in this repository. They are both open source and free for commercial use.
The fonts can also be downloaded from the web.
Fivo Sans: https://www.fontsc.com/font/fivo-sans
Atkinson Hyperlegible: https://brailleinstitute.org/freefont

The following fonts are used:

- Leaflet: Noto Sans (Light/Regular/Italic/Medium (Italic)/SemiBoldItalic/Extra Bold)
- Leaflet: Noto Sans (Thin/Light (Italic)/Italic/Medium//Extra Bold)
- case
  - Noto Sans Condensed Bold
  - Noto Sans Condensed Extra Bold
  - Noto Sans Condensed Medium
  - Noto Sans ExtraCondensed Extra Bold
  - Noto Sans ExtraCondensed Extra Medium
- Logos:
  - Noto Sans Condensed Bold
  - Noto Sans Condensed Extra Bold
  - Noto Sans Extra Condensed Extra Bold

### Dimensions

#### Card decks:

The "bridge" files are  (2.25 x 3.5" or 57mm x 88.8mm) standard playing cards.
The "tarot" files are (2.75 x 4.75" or 71mm x 121 mm) standard playing cards.

#### Cases:

The "bridge" is 60 x 89.25 mm x 27.15 mm
The "tarot" is 122.2 x 73.1 x 29.1 mm

the "tarrot" box has standard dimensions used by Agile Stationary to print their Cyber Security Cornucopia Edition.
the "bridge" box may need some refitting if used.

#### Leaflets:

The "bridge" files are  55mm x 87mm
The "tarot" files are (2.75 x 4.75")

The "bridge" and "tarot" version is 16-20 page spread depending on in which language you print.

Please be aware, that the table of content for the indesign leaflet has to be adjusted for all language versions before printing except for the english version!! 
This is because indesign does not support auto adjusting the TOC.
You may need to adjust the font size to fit either a 16 or a 20 page leaflet spread.
DO NOT PRINT an 18 Page leaflet! It won't look good.

### Blead:

A standard blead set to 3mm for all 4 sides. 

### Paper

Use 300gsm for both the bridge cards and the tarot cards.
For the case, we would recommend folding box board with anti-scuff lamination and 100gsm uncoated stock for the leaflet. The leaflets could also be laminated, but it might make them springy.

## Contributing to Development

### Large binary files

Please install git-lfs to ensure you can download the output files.

Install from https://git-lfs.com/ 

Then pull the binaries from git lfs.

```bash

git lfs pull

```

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

## Release process

This repository follows [semver](https://semver.org/) approach. Release a new
version means to tag commit in `master` branch. Please do not use same tag
twice.

To avoid common mistakes there is a script which will guide you through process
and push correct tag from your machine.

To release a new patch:

```bash
make release
```

```bash
make release-patch
```

To release a new minor version:

```bash
make release-minor
```
To release a new major version:

```bash
make release-major
```

Once the 

Docker images are build in [Jenkins][4] and published to [Artifactory][5]
keeping 3 tags:

- `latest` mirrors state of `master` branch.
- `current` mirrors state of the most recent Git tag.
- `previous` mirrors state of the previous Git tag.

Images are also pushed with `git describe` version.

## Credits
Cornucopia was originally conceived and created by Colin Watson 
and has since had contributions from a worldwide team of volunteers.
Please see [About Cornucopia](https://cornucopia.owasp.org/about#Acknowledgements) for more details.

## License

### General Licensing Terms

© 2025 OWASP Foundation
Except, where otherwise noted, content in this repository is licensed under a [CC-BY-SA-4.0](./LICENSE.md)
The OWASP Cornucopia converter and Website are examples of this.
If you want to use any of the work in your own project please link back to our [website](https://cornucopia.owasp.org/about)
and give credit to OWASP Cornucopia.
Individuals that have contributed to parts of the project are credited through the OWASP Cornucopia project.
You may refer to the [CC-BY-SA-4.0](./LICENSE.md) license for guidance as long as you are using our latest work.

### Elevation of Privilege (EoP)

© 2010 Microsoft Corporation. Text for Elevation of Privilege (EoP) is licensed under [CC-BY-SA-3.0](./LICENSE-CC-BY-SA-3.0.md)
EoP is created by Affiliate Prof. Adam Shostack (see: [adamshostack/eop](https://github.com/adamshostack/eop))

### Elevation of MLSec (MLSec)

© 2024 Kantega AS. Text for Elevation of MLSec (MLSec) is licensed under [CC-BY-SA-4.0](./LICENSE.md).
Elevation of MLSec is created by Elias Brattli Sørensen (design: Jorun Kristin Bremseth) when working at Kantega AS (see: [kantega/elevation-of-mlsec](https://github.com/kantega/elevation-of-mlsec)).

### OWASP Cumulus

© 2025 OWASP Foundation. Text for OWASP Cumulus is licensed under [CC-BY-SA-4.0](./LICENSE.md).
OWASP Cumulus is created by Christoph Niehoff. More information can be found on their site (see: [owasp.org/www-project-cumulus](https://owasp.org/www-project-cumulus/)).

### OWASP Cornucopia Mobile App Edition (version smaller than 2.0)

Text and code mapping for OWASP Cornucopia Mobile App Edition is licensed under [CC-BY-SA-3.0](./LICENSE-CC-BY-SA-3.0.md)

### OWASP Cornucopia Website App Edition (version smaller than 3.0)

Text and code mapping for OWASP Cornucopia Website App Edition is licensed under [CC-BY-SA-3.0](./LICENSE-CC-BY-SA-3.0.md)

### Copi - The Cornucopia Game Engine

Copi - The Cornucopia Game Engine is licensed under [GNU AFFERO GENERAL PUBLIC LICENSE](copi.owasp.org/LICENSE)

### Font licensing

For font licensing, please read font [README.md](./resources/templates/Fonts/README.md)

### version-up.sh

 Copyright (C) 2017, Oleksandr Kucherenko under [MIT](https://opensource.org/license/mit)


### Cloudflare Worker Content Security Policy Nonce Generator (nonce-worker.js)

MIT License Copyright (c) 2020 Move Your Digital, Inc.

please read [README.md](./cornucopia.owasp.org/script/README.md)

### Common Attack Pattern Enumeration and Classification (CAPEC™)

Use of the Common Attack Pattern Enumeration and Classification (CAPEC), and the associated references from capec.mitre.org are subject to the [Terms of Use](CAPEC.md). Copyright © 2007–2025, The MITRE Corporation. CAPEC and the CAPEC logo are trademarks of The MITRE Corporation.

## Our Threat Models

You may review the threat model for Cornucopia and Copi by using [OWASP Threat Dragon](https://www.threatdragon.com/#/dashboard) and opening copi.json or cornucopia.json at [ThreatDragonModels](ThreatDragonModels).

Note: If you are looking into using Copi, it may be worth looking at some of [Copi's known threats](copi.owasp.org/README.md#our-threat-model) before doing so to make sure you have prepared yourself accordingly and taken our known threats into account.
