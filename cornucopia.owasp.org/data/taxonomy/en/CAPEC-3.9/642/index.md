# CAPEC™ 642: Replace Binaries

## Description

Adversaries know that certain binaries will be regularly executed as part of normal processing. If these binaries are not protected with the appropriate file system permissions, it could be possible to replace them with malware. This malware might be executed at higher system permission levels. A variation of this pattern is to discover self-extracting installation packages that unpack binaries to directories with weak file permissions which it does not clean up appropriately. These binaries can be replaced by malware, which can then be executed.

Source: [CAPEC™ 642](https://capec.mitre.org/data/definitions/642.html)

