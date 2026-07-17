<img src="./resources/logos/cornucopia_logo.svg?raw=true" width="150">

[![OWASP Production Project](https://img.shields.io/badge/owasp-production%20project-brightgreen)](https://owasp.org/projects/)
[![OpenSSF Best Practices](https://bestpractices.coreinfrastructure.org/projects/7125/badge)](https://bestpractices.coreinfrastructure.org/projects/7125)
[![Maintainability](https://qlty.sh/gh/OWASP/projects/cornucopia/maintainability.svg)](https://qlty.sh/gh/OWASP/projects/cornucopia)
[![Code Coverage](https://qlty.sh/gh/OWASP/projects/cornucopia/coverage.svg)](https://qlty.sh/gh/OWASP/projects/cornucopia)

# OWASP Cornucopia project
OWASP Cornucopia is a mechanism in the form of a card game to assist software development teams 
Identify security requirements in Agile, conventional, and formal development processes. 
It is language, platform, and technology agnostic. Visit: https://cornucopia.owasp.org/

## The cross-references on the Web App Edition deck relate to the following versions of other OWASP and external resources:

### Standards

* [OWASP Artificial Intelligence Security Verification Standard v1.0 (AISVS)](https://owasp.org/www-project-artificial-intelligence-security-verification-standard-aisvs-docs/)
* [OWASP Application Security Verification Standard (ASVS) v4 (2019) and v5 (2025)](https://owasp.org/www-project-application-security-verification-standard/)
* [OWASP Mobile Application Security Verification Standard (MASVS) v2.1](https://mas.owasp.org/MASVS/)

### Maturity Models

* [OWASP DSOMM](https://dsomm.owasp.org/mapping)
* [OWASP SAMM](https://github.com/owaspsamm/core/tree/develop/model/activities)

### Top 10:

* [OWASP Agentic Top 10](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
* [OWASP LLM Top 10](https://genai.owasp.org/llm-top-10)
* [OWASP Top 10](https://owasp.org/Top10/2025/)
* [OWASP Top 10 Client-Side Security Risks](https://owasp.org/www-project-top-10-client-side-security-risks/)

### Guides

* [OWASP Automated Threats to Web Applications](https://github.com/OWASP/www-project-automated-threats-to-web-applications/tree/master/assets/oats/EN)
* [OWASP AI Testing Guide](https://owasp.org/www-project-ai-testing-guide/)
* [OWASP Mobile Application Security Testing Guide (MASTG) v1.7](https://mas.owasp.org/MASTG/)

### Other sources:

* [Mitre ATT&CK](https://attack.mitre.org/)
* [Mitre Atlas™](https://atlas.mitre.org/)
* [Mitre CAPEC™ v3.9](https://capec.mitre.org/data/definitions/2000.html)
* [OWASP Dev Guide Web Application Checklist](https://devguide.owasp.org/en/04-design/02-web-app-checklist/)
* [SAFECode Practical Security Stories and Security Tasks for Agile Development Environments (SAFECode) July 2012](https://safecode.org/publication/SAFECode_Agile_Dev_Security0712.pdf)
* [STRIDE](https://en.wikipedia.org/wiki/STRIDE_model)

## Contributing to Development

### Large binary files

Please install git-lfs to ensure you can download the output files.

Install from https://git-lfs.com/ 

Then pull the binaries from git lfs.

```bash

git lfs pull

```

### Using Scripts to develop and build Cornucopia

#### Scripts to build the Cornucopia Card Decks

Please read [README.md](./scripts/README.md)

#### Additional Utility Scripts

Please read [README.md](./scripts/README.md)

### Security Scanning

First time setup:
```bash
pip install pre-commit
pre-commit install
```

A Bandit pre-commit hook scans Python scripts for security issues on commit.
It runs automatically via pre-commit (medium severity, high confidence).

To run manually:
```bash
pre-commit run bandit --all-files
```

### Building and Deploying the Cornucopia website

https://cornucopia.owasp.org contains the card browser for each of the cards in the cornucopia suits together with the taxonomy and in depth explaination for each of the cards in the suits.

please read [README.md](cornucopia.owasp.org/README.md)

### Building and Deploying the Cornucopia Game Engine: Copi

Copi (https://copi.owasp.org) is an online game engine where you can play Cornucopia and Elevation of Privilege. You can play all the editions of Cornucopia (website and mobile) as well as the Elevation of Privileges game.

please read [README.md](copi.owasp.org/README.md)

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

The "bridge" files are  (2.25 x 3.5" or 56mm x 87mm) standard playing cards.
The "tarot" files are (2.75 x 4.75" or 70mm x 121 mm) standard playing cards.

#### Cases:

The "bridge" is 60 x 89.25 mm x 27.15 mm
The "tarot" is 122.2 x 73.1 x 29.1 mm

the "tarot" box has standard dimensions used by Agile Stationary to print their Cyber Security Cornucopia Edition.

#### Leaflets:

The "bridge" files are  56mm x 87mm
The "tarot" files are (2.75 x 4.75")

The "bridge" and "tarot" version is 16-20 page spread depending on in which language you print.

Please be aware, that the table of content for the indesign leaflet has to be adjusted for all language versions before printing except for the english version!! 
This is because indesign does not support auto adjusting the TOC.
You may need to adjust the font size to fit either a 16 or a 20 page leaflet spread.
DO NOT PRINT an 18 Page leaflet! It won't look good.

### Bleed:

A standard bleed set to 3mm for all 4 sides. 

### Paper

Use 300gsm for both the bridge cards and the tarot cards.
For the case, we would recommend folding box board with anti-scuff lamination and 100gsm uncoated stock for the leaflet. The leaflets could also be laminated, but it might make them springy.

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

See: [SECURITY.md](/SECURITY.md#our-threat-models)

