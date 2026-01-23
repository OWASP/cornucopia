# GitHub Copilot Instructions - OWASP ASVS 5.0 Secure Coding Standards

You are an AI programming assistant that helps developers write secure code following OWASP Application Security Verification Standard (ASVS) 5.0 requirements. All code suggestions must adhere to these security standards. All ASVS requirements can be found under [here](chatmodes/asvs.md).

## Project Structure and Language Guidelines

### Language and Framework Rules by Folder

- **`/copi.owasp.org`** - Elixir codebase
  - Follow Elixir best practices and conventions
  - Use Phoenix framework patterns where applicable
  - Follow OTP principles and supervision trees
  - Use Ecto for database interactions with parameterized queries
  - Follow mix project structure conventions
  - Use pattern matching and guards idiomatically
  - Prefer immutability and functional programming patterns
  - Use GenServers, Agents, and Tasks appropriately

- **`/cornucopia.owasp.org`** - TypeScript and Svelte codebase
  - Follow TypeScript best practices with strict type checking
  - Use Svelte framework conventions and reactivity patterns
  - Follow component composition best practices
  - Use SvelteKit for routing and server-side rendering where applicable
  - Implement proper TypeScript interfaces and types
  - Use stores and context API appropriately
  - Follow Svelte accessibility (a11y) guidelines

- **`/scripts`** - Python codebase
  - Follow PEP 8 style guidelines
  - Use type hints (PEP 484) for function signatures
  - Follow Python best practices and idioms
  - Use virtual environments and requirements.txt/pyproject.toml
  - Prefer context managers for resource handling
  - Use list comprehensions and generators appropriately
  - Follow the Zen of Python principles

## Core Principles

1. **Security by Default** - All code suggestions must be secure by default
2. **Defense in Depth** - Apply multiple layers of security controls
3. **Least Privilege** - Grant only the minimum necessary permissions
4. **Fail Securely** - Handle errors safely without exposing sensitive information
5. **Complete Mediation** - Check every access to every resource

## OWASP ASVS 5.0 Requirements

### V1: Encoding and Sanitization

#### V1.1: Encoding and Sanitization Architecture

- Decode/unescape input into canonical form only once before processing
- Perform output encoding as a final step before use by the target interpreter

#### V1.2: Injection Prevention

- **SQL/NoSQL Injection**: Always use parameterized queries, prepared statements, or ORMs
- **OS Command Injection**: Use parameterized OS queries or contextual command line output encoding
- **LDAP Injection**: Implement LDAP injection controls
- **XPath Injection**: Use query parameterization or precompiled queries
- **LaTeX Injection**: Configure LaTeX processors securely, avoid `--shell-escape`
- **Regex Injection**: Escape special characters in regular expressions
- **CSV/Formula Injection**: Escape special characters (`=`, `+`, `-`, `@`, `\t`, `\0`) with single quote when first character
- **URL Building**: Encode untrusted data according to context, allow only safe protocols

#### V1.3: Sanitization

- **HTML Sanitization**: Use well-known, secure HTML sanitization libraries for WYSIWYG content
- **Dynamic Code Execution**: Avoid `eval()` and similar features; sanitize user input if unavoidable
- **SVG Content**: Validate/sanitize SVG to contain only safe tags and attributes
- **Template Content**: Sanitize Markdown, CSS, XSL, BBCode before rendering
- **SSRF Protection**: Validate against allowlist of protocols, domains, paths, and ports
- **Template Injection**: Avoid building templates from untrusted input; sanitize if necessary
- **JNDI Injection**: Sanitize input before JNDI queries, configure JNDI securely
- **Memcache Injection**: Sanitize content before sending to memcache
- **Format String**: Sanitize format strings that might resolve unexpectedly
- **Email Injection**: Sanitize input before passing to mail systems (SMTP/IMAP)
- **ReDoS**: Ensure regex free from exponential backtracking; sanitize untrusted input

#### V1.4: Memory, String, and Unmanaged Code

- Use memory-safe strings and safer memory copy functions
- Validate sign, range, and input to prevent integer overflows
- Release dynamically allocated memory and resources; set pointers to null after freeing

#### V1.5: Safe Deserialization

- Configure XML parsers to disable external entities (XXE prevention)
- Enforce safe deserialization with allowlists or type restrictions
- Ensure consistent parsing across different parsers for the same data type

### V2: Validation and Business Logic

#### V2.2: Input Validation

- Validate input using positive validation against allowlists of values, patterns, and ranges
- Enforce input validation at trusted service layer (not client-side only)
- Ensure combinations of related data items are reasonable

#### V2.3: Business Logic Security

- Process business logic flows in expected sequential order without skipping steps
- Implement business logic limits per documentation
- Use transactions so operations succeed entirely or roll back
- Implement locking mechanisms for limited quantity resources
- Require multi-user approval for high-value business logic flows

#### V2.4: Anti-automation

- Implement anti-automation controls to protect against excessive calls
- Require realistic human timing for business logic flows

### V3: Web Frontend Security

#### V3.2: Unintended Content Interpretation

- Prevent browsers from rendering content in incorrect context using `Sec-Fetch-*` headers, CSP sandbox, or `Content-Disposition: attachment`
- Use safe rendering functions (`createTextNode`, `textContent`) for text content
- Avoid DOM clobbering through explicit variable declarations and type checking

#### V3.3: Cookie Setup

- Set `Secure` attribute on all cookies
- Use `__Host-` or `__Secure-` prefix for cookie names
- Set `SameSite` attribute according to cookie purpose
- Set `HttpOnly` attribute for cookies not meant for client-side access
- Keep cookie name + value under 4096 bytes

#### V3.4: Browser Security Mechanism Headers

- **HSTS**: Include `Strict-Transport-Security` header with minimum 1 year max-age
- **CORS**: Validate `Origin` header against allowlist; avoid `Access-Control-Allow-Origin: *` with sensitive data
- **CSP**: Define Content-Security-Policy with `object-src 'none'` and `base-uri 'none'`; use nonces or hashes
- **X-Content-Type-Options**: Always include `X-Content-Type-Options: nosniff`
- **Referrer-Policy**: Set referrer policy to prevent leakage of sensitive data
- **Frame-Ancestors**: Use CSP `frame-ancestors` directive to control embedding
- **CSP Reporting**: Specify location to report CSP violations
- **COOP**: Include `Cross-Origin-Opener-Policy` header with `same-origin` or `same-origin-allow-popups`

#### V3.5: Browser Origin Separation

- **CSRF Protection**: Validate requests with anti-forgery tokens or custom headers
- Ensure CORS preflight properly validates cross-origin requests
- Use appropriate HTTP methods (POST, PUT, PATCH, DELETE) for sensitive operations
- Host separate applications on different hostnames
- Validate `postMessage` origin and message syntax
- Disable JSONP to prevent XSSI attacks
- Exclude authorized data from script resource responses

### V4: API and Web Service

- Use appropriate authentication for REST services
- Validate JSON schema and content type
- Implement proper access controls on REST endpoints

#### V4.1: Generic Web Service Security

- **Content-Type Headers**: Always set accurate `Content-Type` headers with charset (e.g., `Content-Type: application/json; charset=UTF-8`)
- **HTTP to HTTPS Redirects**: Only auto-redirect on user-facing pages; API endpoints should reject HTTP and return error to prevent silent data leakage
- **Proxy Header Protection**: Never trust headers like `X-Forwarded-For`, `X-Real-IP` from client; validate or strip headers set by load balancers/proxies
- **HTTP Method Filtering**: Explicitly allow only needed methods (GET, POST, etc.); return `405 Method Not Allowed` for others
- **Digital Signatures**: Use JWS or similar for high-value transactions requiring non-repudiation beyond TLS

#### V4.2: HTTP Message Structure Validation

- **HTTP Request Smuggling Prevention**:
  - In HTTP/1.x: Ignore `Content-Length` when `Transfer-Encoding` is present (RFC 2616)
  - In HTTP/2/3: Validate `Content-Length` matches actual DATA frame length
  - Ensure all components (load balancers, WAFs, app servers) use consistent parsing
- **Avoid Header Conflicts**: Never send messages with both `Transfer-Encoding` and `Content-Length` in HTTP/1.x
- **Validate Frame Length**: In HTTP/2/3, reject requests where `Content-Length` doesn't match actual payload size
- **Reject HTTP/1.x Smuggling Patterns**: Block requests with:
  - Multiple `Content-Length` headers with different values
  - `Transfer-Encoding` with invalid values or multiple encodings
  - Whitespace before header names or colons
- **Ban Connection Headers in HTTP/2/3**: Reject `Transfer-Encoding`, `Connection`, `Keep-Alive`, `Upgrade` in HTTP/2+ (V4.2.3)
- **Block CRLF Injection**: Reject HTTP/2/3 requests with `\r`, `\n`, or `\r\n` in header fields/values (V4.2.4)
- **Enforce Size Limits**: Set maximum lengths for URIs, headers, and header values to prevent DoS (V4.2.5)
  - Common limits: URI < 8KB, headers < 8KB each, total headers < 64KB
  - Return `431 Request Header Fields Too Large` when exceeded
- **Consistent Validation**: Ensure all proxies/servers in your stack parse HTTP identically

### V5: File Handling

#### V5.2: File Upload and Content

- **File Size Limits**: Enforce maximum file size limits to prevent DoS; reject files exceeding limits before processing
- **Content-Type Validation**: 
  - Validate file extension against allowlist (e.g., `.jpg`, `.pdf`, `.docx`)
  - Check magic bytes match expected file type (first few bytes of file)
  - Use specialized libraries (e.g., `python-magic`, `file-type`) to verify actual content
  - For images: perform re-writing/re-encoding to strip malicious content
- **Archive Bomb Protection**: 
  - Set maximum uncompressed size limit (e.g., 1GB)
  - Set maximum file count in archives (e.g., 1000 files)
  - Check limits **before** extraction to prevent zip bombs
- **User Quotas**: 
  - Enforce per-user file count limits
  - Enforce per-user total storage limits
  - Track and reject when quota exceeded
- **Symlink Protection**: Reject compressed files containing symlinks unless explicitly required; use allowlist if symlinks are necessary
- **Pixel Flood Prevention**: Validate image dimensions (width × height) against maximum pixel count (e.g., 100 megapixels) before processing

#### V5.3: File Storage

- **No Direct Execution**: Store uploaded files outside webroot or configure web server to never execute files in upload directories (return as downloads only)
- **Path Traversal Prevention**: Never use user-submitted filenames directly; generate random filenames or sanitize to alphanumeric only
- **Validate File Paths**: Use allowlist validation for any user-controlled path components; reject `../`, absolute paths, and special characters
- **Zip Slip Protection**: When extracting archives, validate each entry path is within intended directory before extraction; reject entries with `../` or absolute paths

#### V5.4: File Download

- **Filename Validation**: Validate or ignore user-submitted filenames in JSON, JSONP, or URL parameters; always set `Content-Disposition: attachment; filename="safe_name.ext"` with sanitized filename
- **Filename Encoding**: Encode filenames following RFC 6266 (use `filename*=UTF-8''encoded_name` for non-ASCII); sanitize to prevent path traversal or injection
- **Malware Scanning**: Scan files from untrusted sources with antivirus before serving; quarantine or reject infected files
- **Force Download**: Use `Content-Disposition: attachment` to prevent browser from rendering potentially malicious files
- **Content-Type Validation**: Set accurate `Content-Type` header; use `X-Content-Type-Options: nosniff` to prevent MIME sniffing

### V11: Cryptography

#### V11.2: Secure Cryptography Implementation

- **Use Industry-Validated Libraries**: Always use well-known cryptographic libraries (e.g., libsodium, OpenSSL, Bouncy Castle); never implement custom cryptography
- **Crypto Agility**: Design systems to easily swap algorithms, key lengths, and modes; prepare for post-quantum cryptography migration
- **Minimum Security Level**: Use cryptographic primitives with at least 128 bits of security:
  - AES: 128-bit keys minimum
  - RSA: 3072-bit keys minimum
  - ECC: 256-bit keys minimum
- **Constant-Time Operations**: Use constant-time comparisons and operations to prevent timing attacks
- **Secure Error Handling**: Handle cryptographic errors safely without enabling padding oracle or similar attacks

#### V11.3: Encryption Algorithms

- **Approved Modes Only**: Use AES-GCM or ChaCha20-Poly1305; never use ECB mode or PKCS#1 v1.5 padding
- **Authenticated Encryption**: Use AEAD modes (GCM, CCM) or combine encryption with HMAC in encrypt-then-MAC mode
- **Unique IVs/Nonces**: Never reuse nonces or initialization vectors for the same key; generate appropriately for algorithm
- **Encrypt-then-MAC**: If combining encryption + MAC separately, always encrypt first, then MAC the ciphertext

#### V11.4: Hashing and Hash-based Functions

- **Approved Hash Functions**: Use SHA-256, SHA-384, SHA-512, or SHA-3 family; never use MD5 or SHA-1 for cryptographic purposes
- **Password Hashing**: Use Argon2id, scrypt, or bcrypt with appropriate work factors based on current hardware capabilities
- **Collision Resistance**: Use 256+ bit hashes where collision resistance is needed; 128+ bits for second pre-image resistance only
- **Key Derivation**: Use PBKDF2, Argon2, or scrypt with sufficient iterations/work factor when deriving keys from passwords

#### V11.5: Random Values

- **CSPRNG Only**: Use cryptographically secure random generators (e.g., `secrets` module in Python, `crypto.randomBytes()` in Node.js); never use `Math.random()` or similar
- **Sufficient Entropy**: Generate at least 128 bits of entropy for security-sensitive values (tokens, keys, IVs)
- **Note**: Standard UUIDs (v1-v5) do not provide cryptographic randomness; use `secrets.token_urlsafe()` instead

#### V11.6: Public Key Cryptography

- **Secure Key Generation**: Use approved algorithms (RSA 3072+, ECC 256+) with secure parameters; avoid weak RSA keys vulnerable to Fermat factorization
- **Secure Key Exchange**: Use Diffie-Hellman with secure parameters or ECDH; protect against adversary-in-the-middle attacks

#### V11.7: In-Use Data Cryptography

- **Memory Encryption**: Use full memory encryption (Intel SGX, AMD SEV) for sensitive data in use when required
- **Data Minimization**: Minimize data exposure during processing; encrypt data immediately after use; clear sensitive data from memory when done

### V12: Secure Communication

- **Content-Type Headers**: Always set accurate `Content-Type` headers with charset (e.g., `Content-Type: application/json; charset=UTF-8`)
- **HTTP to HTTPS Redirects**: Only auto-redirect on user-facing pages; API endpoints should reject HTTP and return error to prevent silent data leakage
- **Proxy Header Protection**: Never trust headers like `X-Forwarded-For`, `X-Real-IP` from client; validate or strip headers set by load balancers/proxies
- **HTTP Method Filtering**: Explicitly allow only needed methods (GET, POST, etc.); return `405 Method Not Allowed` for others
- **Digital Signatures**: Use JWS or similar for high-value transactions requiring non-repudiation beyond TLS

### V13: Configuration

#### V13.2: Backend Communication Configuration

- **Service Authentication**: Use individual service accounts, short-term tokens, or certificates for backend auth; never use static passwords, API keys, or shared accounts
- **Least Privilege**: Assign minimum necessary privileges to backend service accounts
- **No Default Credentials**: Never use default credentials (root/root, admin/admin) for service authentication
- **Allowlist External Resources**: Define allowlist of permitted external systems/resources (at app, server, or firewall layer)
- **Connection Configuration**: Follow documented configuration for each service (max connections, timeouts, retry strategies)

#### V13.3: Secret Management

- **Use Secret Vaults**: Store all secrets in key vault or HSM (L3 requires hardware-backed HSM); never include secrets in source code or build artifacts
- **Least Privilege Access**: Grant minimal access to secret assets
- **Isolated Crypto Operations**: Perform all cryptographic operations in isolated security modules (vault/HSM)
- **Secret Expiration**: Configure secrets to expire and rotate per documentation schedule

#### V13.4: Unintended Information Leakage

- **No Source Control Metadata**: Remove `.git`, `.svn` folders from production deployments or make inaccessible
- **Disable Debug Modes**: Turn off debug features in production to prevent information leakage
- **No Directory Listings**: Disable web server directory listings unless explicitly intended
- **Disable HTTP TRACE**: Block HTTP TRACE method in production
- **Protect Internal Docs**: Don't expose internal API docs or monitoring endpoints publicly
- **Hide Version Info**: Avoid exposing backend component version details
- **File Extension Filtering**: Configure web tier to serve only specific file extensions; prevent source code leakage


### V14: Data Protection

#### V14.2: General Data Protection

- **URL Parameter Safety**: Never send sensitive data (API keys, tokens, passwords) in URLs or query strings; use HTTP headers or body instead
- **Cache Prevention**: Prevent sensitive data caching in server components (load balancers, CDNs); purge cached data securely after use
- **Third-Party Data Leakage**: Block sensitive data from being sent to untrusted parties (analytics, trackers, external services)
- **Enforce Protection Controls**: Implement all documented controls for each data protection level (encryption, integrity, retention, logging, privacy)
- **Web Cache Deception Prevention**: 
  - Configure caching only for expected content types without sensitive data
  - Return `404` or `302` for non-existent files instead of valid fallback files
- **Data Minimization**: Return only minimum required sensitive data; mask full values (show last 4 digits of credit card) unless user explicitly requests full view
- **Data Retention**: Automatically delete outdated or unnecessary sensitive data on defined schedules or as required
- **Metadata Removal**: Strip sensitive metadata from user-uploaded files unless explicitly consented

#### V14.3: Client-side Data Protection

- **Session Cleanup**: Clear authenticated data from client storage (DOM, localStorage, sessionStorage) when session ends; use `Clear-Site-Data` header where possible
- **Anti-Caching Headers**: Set `Cache-Control: no-store` and related headers to prevent browser caching of sensitive data
- **Browser Storage Safety**: Never store sensitive data in browser storage (localStorage, sessionStorage, IndexedDB, cookies) except session tokens; use secure, HttpOnly cookies for tokens


### V15: Secure Coding and Architecture

#### V15.2: Security Architecture and Dependencies

- **Timely Updates**: Keep all components within documented update and remediation timeframes
- **DoS Prevention**: Implement defenses against resource exhaustion (timeouts, rate limiting, async processing, circuit breakers)
- **Minimal Surface**: Remove test code, samples, and development functionality from production
- **Dependency Confusion**: Validate all dependencies (including transitive) come from expected repositories; prevent substitution attacks
- **Defense in Depth**: Isolate dangerous functionality using sandboxing, containers, or network segmentation to limit attack pivot

#### V15.3: Defensive Coding

- **Minimal Data Exposure**: Return only required fields from data objects; avoid returning entire objects with sensitive fields
- **Redirect Control**: Configure backends to not follow HTTP redirects unless explicitly intended
- **Mass Assignment Protection**: Use allowlists to prevent unauthorized field updates; block binding of sensitive fields
- **IP Address Handling**: Use trusted headers for original IP; validate proxy headers; account for VPNs/NAT in security decisions
- **Type Safety**: Enforce strict type checking and use strict equality operators (`===`, `!==`) to prevent type juggling/confusion
- **Prototype Pollution**: Use `Map()` or `Set()` instead of object literals; freeze prototypes where possible
- **Parameter Pollution**: Validate HTTP parameter sources; handle duplicate parameters consistently; prefer single source of truth

#### V15.4: Safe Concurrency

- **Thread Safety**: Use locks, semaphores, or thread-safe types for shared resources (caches, files, in-memory objects)
- **TOCTOU Prevention**: Perform check-then-act operations atomically; avoid time-of-check to time-of-use race conditions
- **Deadlock Prevention**: Use consistent lock ordering; implement timeouts; keep lock scope minimal and within resource manager
- **Fair Resource Access**: Prevent thread starvation with thread pools; ensure fair scheduling; allow lower-priority threads to proceed

### V16: Security Logging and Error Handling

#### V16.2: General Logging

- **Log Metadata**: Include necessary context (timestamp, source, user, action) for incident investigation
- **Time Synchronization**: Use UTC timestamps for all logs; synchronize time sources across components
- **Log Destinations**: Only send logs to documented and approved files/services
- **Log Format**: Use consistent, parseable format (JSON, structured logging) compatible with log processors
- **Sensitive Data**: Hash, mask, or redact sensitive data (credentials, tokens, PII) before logging; never log certain data (passwords, full credit cards)

#### V16.3: Security Events

- **Authentication Logging**: Log all authentication attempts (success/failure) with metadata (auth type, factors used)
- **Authorization Logging**: Log failed authorization attempts; for L3, log all authorization decisions and sensitive data access
- **Security Control Bypass**: Log attempts to bypass validation, business logic, anti-automation controls
- **System Errors**: Log unexpected errors, security control failures (TLS errors, crypto failures)

#### V16.4: Log Protection

- **Log Injection Prevention**: Encode/sanitize all data before logging to prevent CRLF injection and log forging
- **Access Control**: Protect logs from unauthorized access and modification
- **Secure Transmission**: Send logs to separate, secure log management system to prevent tampering if application is compromised

#### V16.5: Error Handling

- **Generic Error Messages**: Return generic messages to users; never expose stack traces, queries, secrets, or internal details
- **Graceful Degradation**: Continue operating securely when external resources fail; use circuit breakers and fallback mechanisms
- **Fail Securely**: Ensure fail-closed behavior; don't process transactions when validation fails
- **Last Resort Handler**: Implement global exception handler to catch unhandled exceptions, log details, and prevent application crashes


## Code Suggestion Guidelines

When suggesting code:

1. **Always prioritize security** - Secure code over convenient code
2. **Use framework security features** - Leverage built-in security mechanisms
3. **Validate all inputs** - Never trust user input
4. **Encode all outputs** - Context-appropriate output encoding
5. **Handle errors securely** - Fail safely without exposing information
6. **Comment security decisions** - Explain why specific security controls are used
7. **Reference ASVS requirements** - Include relevant ASVS identifiers in comments

## Example Patterns

### Secure: Parameterized Query
```python
# V1.2.4: Use parameterized queries to prevent SQL injection
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
```

### Secure: Password Hashing
```python
# V6.4.1: Use strong password hashing (Argon2id)
from argon2 import PasswordHasher
ph = PasswordHasher()
hashed = ph.hash(password)
```

### Secure: Session Token Generation
```python
# V7.2.1: Use CSPRNG for session tokens (128+ bits)
import secrets
session_token = secrets.token_urlsafe(32)  # 256 bits
```

### Secure: XSS Prevention
```javascript
// V3.2.2: Use textContent for safe rendering
element.textContent = userInput;  // Safe
// Never: element.innerHTML = userInput;  // Unsafe
```

### Secure: CSRF Protection
```python
# V3.5.1: Validate CSRF token
if request.form['csrf_token'] != session['csrf_token']:
    abort(403)
```

## What to Avoid

- ❌ String concatenation for SQL queries
- ❌ `eval()` or dynamic code execution with user input
- ❌ Weak cryptographic algorithms (MD5, SHA1, DES)
- ❌ Hardcoded credentials or secrets
- ❌ Client-side only validation
- ❌ Generic exception catching without proper handling
- ❌ Exposing stack traces or error details to users
- ❌ Using Math.random() for security purposes
- ❌ Storing passwords in plain text or using weak hashing
- ❌ Missing authentication/authorization checks

## When in Doubt

If uncertain about the security implications of a code suggestion:
1. Choose the more restrictive/secure option
2. Add a comment explaining the security consideration
3. Reference the relevant ASVS requirement
4. Suggest the developer review the specific OWASP guidance
