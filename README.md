[![OpenSSF Best Practices](https://bestpractices.coreinfrastructure.org/projects/7125/badge)](https://bestpractices.coreinfrastructure.org/projects/7125)

# OWASP Cornucopia project
OWASP Cornucopia is a mechanism in the form of a card game to assist software development teams 
identify security requirements in Agile, conventional and formal development processes. 
It is language, platform and technology agnostic.

### The cross-references relate to the following versions of other OWASP and external resources:
* OWASP SCP OWASP_Secure_Coding_Practices_Checklist v2
* OWASP ASVS OWASP_Application_Security_Verification_Standard v2 (2014)
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
usage: convert.py [-h] [-i INPUTFILE] [-t {all,docx,pdf,idml}] [-o OUTPUTFILE] [-l {template,all,en,es,fr,nl,pt-br}] [-d] [-s {all,static,dynamic}] [-u URL]

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
  -l {template,all,en,es,fr,nl,pt-br}, --language {template,all,en,es,fr,nl,pt-br}
                        Output language to produce. [`en`, `es`, `fr`, `pt-br`, `template`] 
                        Template will attempt to create a template from the english input file and 
                        replacing strings with the template lookup codes
  -d, --debug           Output additional information to debug script
  -s {all,static,dynamic}, --style {all,static,dynamic}
                        Output style to produce. [`static` or `dynamic`] 
                        Static cards have the mappings printed on them, dynamic ones a QRCode that points to an maintained list.
  -u URL, --url URL     Specify a URL to use in generating dynamic cards. (caution: URL will be suffixed with / and the card ID). 
```

## Contributing to Development

Before you push your changes please format files with

```bash
make fmt
```

run static analysis checks

```bash
make static-check
```

run all available smoke, unit and integration tests

```bash
make test
```

check that your code have sufficient test coverage

```bash
make coverage-check
```

All python unit tests with fixtures in `testdata` folder support updating
_golden_ files from real output of tests

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

```bash
make release
```

Docker images are build in [Jenkins][4] and published to [Artifactory][5]
keeping 3 tags:

- `latest` mirrors state of `master` branch.
- `current` mirrors state of the most recent Git tag.
- `previous` mirrors state of the previous Git tag.

Images are also pushed with `git describe` version.
