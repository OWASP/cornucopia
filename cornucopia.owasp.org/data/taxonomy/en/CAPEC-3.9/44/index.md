# CAPEC™ 44: Overflow Binary Resource File

## Description

An attack of this type exploits a buffer overflow vulnerability in the handling of binary resources. Binary resources may include music files like MP3, image files like JPEG files, and any other binary file. These attacks may pass unnoticed to the client machine through normal usage of files, such as a browser loading a seemingly innocent JPEG file. This can allow the adversary access to the execution stack and execute arbitrary code in the target process.

Source: [CAPEC™ 44](https://capec.mitre.org/data/definitions/44.html)

