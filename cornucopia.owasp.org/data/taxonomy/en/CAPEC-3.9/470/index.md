# CAPEC™ 470: Expanding Control over the Operating System from the Database

## Description

An attacker is able to leverage access gained to the database to read / write data to the file system, compromise the operating system, create a tunnel for accessing the host machine, and use this access to potentially attack other machines on the same network as the database machine. Traditionally SQL injections attacks are viewed as a way to gain unauthorized read access to the data stored in the database, modify the data in the database, delete the data, etc. However, almost every data base management system (DBMS) system includes facilities that if compromised allow an attacker complete access to the file system, operating system, and full access to the host running the database. The attacker can then use this privileged access to launch subsequent attacks. These facilities include dropping into a command shell, creating user defined functions that can call system level libraries present on the host machine, stored procedures, etc.

Source: [CAPEC™ 470](https://capec.mitre.org/data/definitions/470.html)

