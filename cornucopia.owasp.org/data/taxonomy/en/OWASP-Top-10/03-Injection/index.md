# Injection
## Description
An application is vulnerable to attack when:

- User-supplied data is not validated, filtered, or sanitized by the application.
- Dynamic queries or non-parameterized calls without context-aware escaping are used directly in the interpreter.
- Hostile data is used within object-relational mapping (ORM) search parameters to extract additional, sensitive records.
- Hostile data is directly used or concatenated. The SQL or command contains the structure and malicious data in dynamic queries, commands, or stored procedures.

Some of the more common injections are SQL, NoSQL, OS command, Object Relational Mapping (ORM), LDAP, and Expression Language (EL) or Object Graph Navigation Library (OGNL) injection. The concept is identical among all interpreters. Source code review is the best method of detecting if applications are vulnerable to injections. Automated testing of all parameters, headers, URL, cookies, JSON, SOAP, and XML data inputs is strongly encouraged. Organizations can include static (SAST), dynamic (DAST), and interactive (IAST) application security testing tools into the CI/CD pipeline to identify introduced injection flaws before production deployment.

## How to Prevent
- The preferred option is to use a safe API, which avoids using the interpreter entirely, provides a parameterized interface, or migrates to Object Relational Mapping Tools (ORMs).
Note: Even when parameterized, stored procedures can still introduce SQL injection if PL/SQL or T-SQL concatenates queries and data or executes hostile data with EXECUTE IMMEDIATE or exec().
- Use positive server-side input validation. This is not a complete defense as many applications require special characters, such as text areas or APIs for mobile applications.
- For any residual dynamic queries, escape special characters using the specific escape syntax for that interpreter.
Note: SQL structures such as table names, column names, and so on cannot be escaped, and thus user-supplied structure names are dangerous. This is a common issue in report-writing software.
- Use LIMIT and other SQL controls within queries to prevent mass disclosure of records in case of SQL injection.

[Source: OWASP TOP 10 Injection](https://owasp.org/Top10/A03_2021-Injection/)

## Cheatsheets
[Injection Cheatcheats](https://cheatsheetseries.owasp.org/IndexTopTen.html#a032021-injection)

## Cards
### Data-validation-&-encoding
- [Data-validation-&-encoding 2](/cards/VE2)
- [Data-validation-&-encoding 3](/cards/VE3)
- [Data-validation-&-encoding 4](/cards/VE4)
- [Data-validation-&-encoding 5](/cards/VE5)
- [Data-validation-&-encoding 6](/cards/VE6)
- [Data-validation-&-encoding 7](/cards/VE7)
- [Data-validation-&-encoding 8](/cards/VE8)
- [Data-validation-&-encoding 9](/cards/VE9)
- [Data-validation-&-encoding J](/cards/VEJ)
- [Data-validation-&-encoding Q](/cards/VEQ)
- [Data-validation-&-encoding K](/cards/VEK)

### Authentication
- [Authentication 2](/cards/AT2)
- [Authentication 3](/cards/AT3)
- [Authentication 4](/cards/AT4)
- [Authentication 5](/cards/AT5)
- [Authentication 8](/cards/AT8)
- [Authentication J](/cards/ATJ)
- [Authentication Q](/cards/ATQ)
- [Authentication K](/cards/ATK)

### Session-management
- [Session-management 2](/cards/SM2)

### Authorization
- [Authorization 2](/cards/AZ2)
- [Authorization 3](/cards/AZ3)
- [Authorization 8](/cards/AZ8)
- [Authorization 9](/cards/AZ9)
- [Authorization Q](/cards/AZQ)

### Cryptography
- [Cryptography 8](/cards/CR8)

### Cornucopia
- [Cornucopia 3](/cards/C3)
- [Cornucopia 5](/cards/C5)
