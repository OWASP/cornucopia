# CAPEC™ 471: Search Order Hijacking

## Description

An adversary exploits a weakness in an application's specification of external libraries to exploit the functionality of the loader where the process loading the library searches first in the same directory in which the process binary resides and then in other directories. Exploitation of this preferential search order can allow an attacker to make the loading process load the adversary's rogue library rather than the legitimate library. This attack can be leveraged with many different libraries and with many different loading processes. No forensic trails are left in the system's registry or file system that an incorrect library had been loaded.

Source: [CAPEC™ 471](https://capec.mitre.org/data/definitions/471.html)

