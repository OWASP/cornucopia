# OWASP Cornucopia project
OWASP Cornucopia is a mechanism in the form of a card game to assist software development teams 
identify security requirements in Agile, conventional and formal development processes. 
It is language, platform and technology agnostic.

## Changes & Updates
### 2021-05-28
Updated templates with tags.
convert.py script pulls language files data and replaces tags with language text.
Functions available to output idml files or docx files.

Script can also create template files using the matching text to populate with tags. 
As text does not all match correctly, this function still requires manual intervention for completing the template setup.

Todo: 
Add meta data to the processing for editions, languages and versions.
Add logging.
Add testing.

## Changes & Updates
### 2024-04-30

- Adding editions, languages and versions to the deck converter.
- Adding the mobile app edition.
- Adding functionality for building the leaflet.
- Update the ASVS mapping version to ASVS 4.0.3.