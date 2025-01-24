A lack of input validation is often the root cause of many security issues. Since the validation needs to be context specific, generic sanitisation routines will not suffice and the developer needs to understand how data are formatted/composed, why the data is being sent, what it is used for and the meaning of the values. This input validation should ensure that

Only the permitted inputs (field/parameter names) are supplied.
All the mandatory inputs are supplied.
The values associated with the field/parameter name are of the expected format, type, range, length, etc.
NB: This card relates to generic input validation. See VE 4 for the similar additional context-specific checks.
