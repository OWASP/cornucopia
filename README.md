[![OWASP Lab](https://img.shields.io/badge/owasp-lab%20project-yellow.svg)](https://owasp.org/other_projects/)
[![OpenSSF Best Practices](https://bestpractices.coreinfrastructure.org/projects/7125/badge)](https://bestpractices.coreinfrastructure.org/projects/7125)
[![Maintainability](https://api.codeclimate.com/v1/badges/4a7cda6ef1c2932a34f9/maintainability)](https://codeclimate.com/github/OWASP/cornucopia/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/4a7cda6ef1c2932a34f9/test_coverage)](https://codeclimate.com/github/OWASP/cornucopia/test_coverage)

# OWASP Cornucopia project
OWASP Cornucopia is a mechanism in the form of a card game to assist software development teams 
identify security requirements in Agile, conventional and formal development processes. 
It is language, platform and technology agnostic.

### The cross-references relate to the following versions of other OWASP and external resources:
* OWASP SCP OWASP_Secure_Coding_Practices_Checklist v2
* OWASP ASVS OWASP_Application_Security_Verification_Standard v4 (2019)
* OWASP AppSensor AppSensor_DetectionPoints
* CAPEC Mitre Common Attack Pattern Enumeration and Classification v1.7.1
* SAFECode SAFECode Practical Security Stories and Security Tasks for Agile Development Environments July 2012

### Credits
Cornucopia was originally conceived and created by Darío De Filippis 
and has since had contributions from a worldwide team of volunteers.
Please see [Project Page](https://owasp.org/www-project-cornucopia/) for more details.

## Building the Deck

Merges to the main branch will generate new DOCX and IDML files to use to print off new version of the deck but if you wish to produce these locally yourself then use the ./scripts/convert.py scipt to do this:

```bash
(cornucopia) ➜  cornucopia git:(master) ✗ python ./scripts/convert.py --help
usage: convert.py [-h] [-i INPUTFILE] [-t {all,docx,pdf,idml}] [-o OUTPUTFILE] [-l {template,all,en,es,fr,nl,no-nb,pt-br}] [-d] [-s {all,static,dynamic}] [-u URL]

Tool to output OWASP Cornucopia playing cards into different file types and languages. 
Example usage: $ ./cornucopia/convert.py -t docx -l es -v 1.30
Example usage: c:\cornucopia\scripts\convert.py -t idml -l fr -s static -v 1.30 -o 'my_output_folder/owasp_cornucopia_edition_language_version.idml'

options:
  -h, --help            show this help message and exit
  -i INPUTFILE, --inputfile INPUTFILE
                        Input (template) file to use.
                        Default=resources/templates/owasp_cornucopia_edition_lang_ver_template.(docx|idml)
                        Template type is dependent on output type (-t) or file (-o) specified.
  -v {1.20,1.21,1.30}, --version {1.20,1.21,1.30}
                        Output version to produce. [`1.20`, `1.21`, `1.30`]
                        Version 1.20 and 1.2x will deliver cards mapped to ASVS 3.0.1
                        Version 1.30 and 1.3x will deliver cards mapped to ASVS 4.0
  -t {all,docx,pdf,idml}, --outputfiletype {all,docx,pdf,idml}
                        Type of file to output. Default = docx. If specified, this overwrites the output file extension
  -o OUTPUTFILE, --outputfile OUTPUTFILE
                        Specify a path and name of output file to generate. (caution: existing file will be overwritten). 
                        default = output/owasp_cornucopia_edition_component_lang_ver.(docx|pdf|idml)
  -l {template,all,en,es,fr,nl,no-nb,pt-br}, --language {template,all,en,es,fr,nl,no-nb,pt-br}
                        Output language to produce. [`en`, `es`, `fr`, `nl`, `no-nb`, `pt-br`, `template`] 
                        Template will attempt to create a template from the english input file and 
                        replacing strings with the template lookup codes
  -d, --debug           Output additional information to debug script
  -s {all,static,dynamic}, --style {all,static,dynamic}
                        Output style to produce. [`static` or `dynamic`] 
                        Static cards have the mappings printed on them, dynamic ones a QRCode that points to an maintained list.
  -u URL, --url URL     Specify a URL to use in generating dynamic cards. (caution: URL will be suffixed with / and the card ID). 
```

## Printing

The latest printable files are added to the `output` folder in this repository.
The docx/pdf files can be easily printed by any desktop printer, but for the best quality use the idml InDesign files. When sending the files to a printing facility you may have to supply the fonts that has been used in order to create the work. 
In case the printing facility doesn't have the fonts at hand you'll find the installable fonts under `resources/fonts` in this repository. They are both open source and free for commercial use.
The fonts can also be downloaded from the web.
Fivo Sans: https://www.fontsc.com/font/fivo-sans
Atkinson Hyperlegible: https://brailleinstitute.org/freefont

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
