<img src="./resources/logos/cornucopia_logo.svg?raw=true" width="150">

[![OWASP Production Project](https://img.shields.io/badge/owasp-production%20project-brightgreen)](https://owasp.org/other_projects/)
[![OpenSSF Best Practices](https://bestpractices.coreinfrastructure.org/projects/7125/badge)](https://bestpractices.coreinfrastructure.org/projects/7125)
[![Maintainability](https://api.codeclimate.com/v1/badges/4a7cda6ef1c2932a34f9/maintainability)](https://codeclimate.com/github/OWASP/cornucopia/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/4a7cda6ef1c2932a34f9/test_coverage)](https://codeclimate.com/github/OWASP/cornucopia/test_coverage)

# OWASP Cornucopia project
OWASP Cornucopia is a mechanism in the form of a card game to assist software development teams 
identify security requirements in Agile, conventional and formal development processes. 
It is language, platform and technology agnostic.

## The cross-references on the Web App Edition deck relate to the following versions of other OWASP and external resources:
* OWASP SCP OWASP_Secure_Coding_Practices_Checklist v2
* OWASP ASVS OWASP_Application_Security_Verification_Standard v4 (2019)
* OWASP AppSensor AppSensor_DetectionPoints
* CAPEC Mitre Common Attack Pattern Enumeration and Classification v1.7.1
* SAFECode SAFECode Practical Security Stories and Security Tasks for Agile Development Environments July 2012
* MASTG OWASP Mobile Application Security Testing Guide 1.7
* MASVS OWASP Mobile Application Security Verification Standard 2.0

## Credits
Cornucopia was originally conceived and created by Colin Watson 
and has since had contributions from a worldwide team of volunteers.
Please see [Project Page](https://owasp.org/www-project-cornucopia/) for more details.

## License

### General Licensing Terms

© 2025 OWASP Foundation
Except, where otherwise noted, content in this repository is licensed under a [CC-BY-SA-3.0](./LICENSE.md)

### Elevation of Privilege (EoP)

© 2010 Microsoft Corporation. Text for Elevation of Privilege (EoP) is licensed under [CC-BY-SA-3.0](./LICENSE.md) 

### OWASP Cornucopia Mobile App Edition

Text and code mapping for OWASP Cornucopia Mobile App Edition is licensed under [CC-BY-SA-3.0](./LICENSE.md)

### OWASP Cornucopia Website App Edition

Text and code mapping for OWASP Cornucopia Website App Edition is licensed under [CC-BY-SA-3.0](./LICENSE.md)

### Font licensing

For font licensing, please read font [README.md](./resources/templates/Fonts/README.md)

### version-up.sh

 Copyright (C) 2017, Oleksandr Kucherenko under [MIT](https://opensource.org/license/mit)


### Cloudflare Worker Content Security Policy Nonce Generator (nonce-worker.js)

MIT License Copyright (c) 2020 Move Your Digital, Inc.

please read [README.md](./cornucopia.owasp.org/script/README.md)

## Building the Deck

Merges to the main branch will generate new DOCX and IDML files to use to print off new version of the deck but if you wish to produce these locally yourself then use the ./scripts/convert.py scipt to do this:

```bash
(cornucopia) ➜  cornucopia git:(master) ✗ python ./scripts/convert.py --help
usage: convert.py [-h] [-i INPUTFILE] [-v VERSION] [-o OUTPUTFILE] [-p] [-d] [-l LANGUAGE] [-t TEMPLATE] [-e EDITION]
                  [-lt LAYOUT]

Tool to output OWASP Cornucopia playing cards into different file types and languages.
Example usage: $ scripts/convert.py --pdf -lt guide -l es -v 2.00
Example usage: $ scripts/convert.py -t tarot -l en -lt cards  -v 1.0 -e eop -i ./resources/templates/eop_ver_cards_tarot_lang.idml -o ./output/eop-1.0-cards-en.idml
Example usage: c:\cornucopia\scripts\convert.py -t bridge -lt cards -l fr -v 2.00 -o 'my_output_folder\owasp_cornucopia_edition_version_layout_language_template.idml'

options:
  -h, --help            show this help message and exit
  -i INPUTFILE, --inputfile INPUTFILE
                        Input (template) file to use.
                        Default=resources\templates\owasp_cornucopia_edition_ver_layout_document_template_lang.(docx|idml)
                        Template type is dependent on the file (-o) specified.
  -v VERSION, --version VERSION
                        Output version to produce. [`all`, `latest`, `1.00`, `1.22`, `2.00`]
                        Version 1.22 and 1.2x will deliver cards mapped to ASVS 3.0
                        Version 2.00 and 2.0x will deliver cards mapped to ASVS 4.0
                        Version 1.00 and 1.0x will deliver cards mapped to MASVS 2.0
                        Version all will deliver all versions of cornucopia
                        Version latest will deliver the latest deck versions of cornucopia
                        You can also specify another version explicitly if needed. If so, there needs to be a yaml file in the source folder where the name contains the version code. Eg. edition-template-ver-lang.yaml
  -o OUTPUTFILE, --outputfile OUTPUTFILE
                        Specify a path and name of output file to generate. (caution: existing file will be overwritten).
                        Eg. output\owasp_cornucopia_edition_ver_layout_document_template_lang.(docx|pdf|idml)
  -p, --pdf             Whether to generate a pdf in addition to the printable document. Does not generate a pdf by default. Only docx can be converted to pdf for the moment.
  -d, --debug           Output additional information to debug script
  -l LANGUAGE, --language LANGUAGE
                        Output language to produce. [`en`, `es`, `fr`, `nl`, `no-nb`, `pt-br`, `it`] you can also specify your own language file. If so, there needs to be a yaml file in the source folder where the name ends with the language code. Eg. edition-template-ver-lang.yaml
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

## Printing

The latest printable files are released under the [pre-release](https://github.com/OWASP/cornucopia/releases/tag/pre-release). Please download final printable files from there.
The docx/pdf files can be easily printed by any desktop printer, but for the best quality use the idml InDesign files. When sending the files to a printing facility you may have to supply the fonts that has been used in order to create the work. 
In case the printing facility doesn't have the fonts at hand you'll find the installable fonts under `resources/templates/Fonts` in this repository. They are both open source and free for commercial use.
The fonts can also be downloaded from the web.
Fivo Sans: https://www.fontsc.com/font/fivo-sans
Atkinson Hyperlegible: https://brailleinstitute.org/freefont

The following fonts are used:

- Deck: Fivo Sans and Atkinson Hyperlegible
- Leaflet: Fivo Sans
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

### Coding style 


Before you push your changes please format files with

```bash
make fmt
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

###  Code coverage

check that your code have sufficient test coverage

```bash
make coverage-check
```

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
