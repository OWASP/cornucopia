Centralized input validation routines are a good programming practice, but like other routines, developers need to understand how they work, how to use them and any limitations. Such routines can be tested independently of other code and not only provide assurance on the quality of the input validation, but it make refactorization an easy task and eliminate code duplicates and bad interpretations. Use of white list validation is recommended where possible. Black lists are usually good as a double-check complement, as they can trigger alerts for fake positives. Common attacks to bad implementation (or lack) of validation rutines are:

Buffer overflows.
Code injection.
Fuzzing.
If third party input validation libraries are used, it is important to test each routine before its implementation.

NB: This card relates to bypass of input data validation. See VE 5 for the similar bypass of output encoding.
