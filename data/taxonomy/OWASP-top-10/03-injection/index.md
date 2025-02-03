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
- [Data-validation-&-encoding 2](/data-validation-&-encoding/2)
- [Data-validation-&-encoding 3](/data-validation-&-encoding/3)
- [Data-validation-&-encoding 4](/data-validation-&-encoding/4)
- [Data-validation-&-encoding 5](/data-validation-&-encoding/5)
- [Data-validation-&-encoding 6](/data-validation-&-encoding/6)
- [Data-validation-&-encoding 7](/data-validation-&-encoding/7)
- [Data-validation-&-encoding 8](/data-validation-&-encoding/8)
- [Data-validation-&-encoding 9](/data-validation-&-encoding/9)
- [Data-validation-&-encoding J](/data-validation-&-encoding/J)
- [Data-validation-&-encoding Q](/data-validation-&-encoding/Q)
- [Data-validation-&-encoding K](/data-validation-&-encoding/K)

### Authentication
- [Authentication 2](/authentication/2)
- [Authentication 3](/authentication/3)
- [Authentication 4](/authentication/4)
- [Authentication 5](/authentication/5)
- [Authentication 8](/authentication/8)
- [Authentication J](/authentication/J)
- [Authentication Q](/authentication/Q)
- [Authentication K](/authentication/K)

### Session-management
- [Session-management 2](/session-management/2)

### Authorization
- [Authorization 2](/authorization/2)
- [Authorization 3](/authorization/3)
- [Authorization 8](/authorization/8)
- [Authorization 9](/authorization/9)
- [Authorization Q](/authorization/Q)

### Cryptography
- [Cryptography 8](/cryptography/8)

### Cornucopia
- [Cornucopia 3](/cornucopia/3)
- [Cornucopia 5](/cornucopia/5)
