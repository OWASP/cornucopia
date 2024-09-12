Centralized output encoding routines are a good programming practice, but developers need to understand how they work, how to use them and any limitations. Such routines can be tested independently of other code and not only provide assurance on the quality of the validation, but it makes refactorization an easy task and it eliminates code duplicates and bad interpretations. Ouput encodings are a must when handling data from un-trusted sources. It should also be a mandatory security check when outputting data to queries for SQL, XML, and LDAP and in every case when hazardous special characters must be allowed as input (such as < > " ' % ( ) & + \ \' \"). Some common attacks of bad implementation (or lack) of output encoding routines are:

Cross Site Scripting (XSS).
Code injection.
Fuzzing.
If third party output encoding libraries are used, it is important to test each routine before its implementation.

NB: This card relates to bypass of output encoding. See VE 6 for the similar bypass of input data validation.
