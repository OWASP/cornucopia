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
