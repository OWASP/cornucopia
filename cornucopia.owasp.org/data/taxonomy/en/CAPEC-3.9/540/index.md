# CAPEC™ 540: Overread Buffers

## Description

An adversary attacks a target by providing input that causes an application to read beyond the boundary of a defined buffer. This typically occurs when a value influencing where to start or stop reading is set to reflect positions outside of the valid memory location of the buffer. This type of attack may result in exposure of sensitive information, a system crash, or arbitrary code execution.

Source: [CAPEC™ 540](https://capec.mitre.org/data/definitions/540.html)

