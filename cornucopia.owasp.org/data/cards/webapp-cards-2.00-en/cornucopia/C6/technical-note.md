Ensure all forms of error are handled robustly and consistently (e.g. web server, application server, database server, JavaScript, other interpreters). This encompasses:

Implement generic error messages and use custom error pages.
The application should handle application errors and not rely on the server configuration.
Properly free allocated memory when error conditions occur.
Error handling logic associated with security controls should deny access by default.
When exceptions occur, fail securely.
