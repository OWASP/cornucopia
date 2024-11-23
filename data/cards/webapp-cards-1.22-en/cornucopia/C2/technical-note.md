This card is framework/language-specific. Examples include:

Beware of un-trusted data.
Check buffer sizes.
Do not rely on garbage collection.
Use non-executable stacks when available.
Avoid the use of known vulnerable functions.
Properly free allocated memory.
Use checksums or hashes to verify the integrity of interpreted code, libraries, executables, and configuration files.
Utilize locking to prevent multiple simultaneous requests.
Use a synchronization mechanism to prevent race conditions.
Protect shared variables and resources from inappropriate concurrent access.
Explicitly initialize all your variables and other data store.
In cases where the application must run with elevated privileges, raise privileges as late as possible, and drop them as soon as possible.
Make no assumptions about availability of other resources, and handle exceptions.
