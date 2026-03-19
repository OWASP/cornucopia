# Level 3 controls

Level 3 contains 92 controls listed below: 

## 01-encoding-and-sanitization

### 02-injection-prevention

- [V1.2.10](/taxonomy/asvs-5.0/01-encoding-and-sanitization/02-injection-prevention#V1.2.10) *The application is protected against csv and formu ...* 

### 03-sanitization

- [V1.3.12](/taxonomy/asvs-5.0/01-encoding-and-sanitization/03-sanitization#V1.3.12) *Regular expressions are free from elements causing ...* 

### 05-safe-deserialization

- [V1.5.3](/taxonomy/asvs-5.0/01-encoding-and-sanitization/05-safe-deserialization#V1.5.3) *Different parsers used in the application for the  ...* 

## 02-validation-and-business-logic

### 03-business-logic-security

- [V2.3.5](/taxonomy/asvs-5.0/02-validation-and-business-logic/03-business-logic-security#V2.3.5) *High-value business logic flows require multi-user ...* 

### 04-anti-automation

- [V2.4.2](/taxonomy/asvs-5.0/02-validation-and-business-logic/04-anti-automation#V2.4.2) *Business logic flows require realistic human timin ...* 

## 03-web-frontend-security

### 01-web-frontend-security-documentation

- [V3.1.1](/taxonomy/asvs-5.0/03-web-frontend-security/01-web-frontend-security-documentation#V3.1.1) *Application documentation states the expected secu ...* 

### 02-unintended-content-interpretation

- [V3.2.3](/taxonomy/asvs-5.0/03-web-frontend-security/02-unintended-content-interpretation#V3.2.3) *The application avoids dom clobbering when using c ...* 

### 03-cookie-setup

- [V3.3.5](/taxonomy/asvs-5.0/03-web-frontend-security/03-cookie-setup#V3.3.5) *When the application writes a cookie, the cookie n ...* 

### 04-browser-security-mechanism-headers

- [V3.4.7](/taxonomy/asvs-5.0/03-web-frontend-security/04-browser-security-mechanism-headers#V3.4.7) *The content-security-policy header field specifies ...* 

- [V3.4.8](/taxonomy/asvs-5.0/03-web-frontend-security/04-browser-security-mechanism-headers#V3.4.8) *All http responses that initiate a document render ...* 

### 05-browser-origin-separation

- [V3.5.6](/taxonomy/asvs-5.0/03-web-frontend-security/05-browser-origin-separation#V3.5.6) *Jsonp functionality is not enabled anywhere across ...* 

- [V3.5.7](/taxonomy/asvs-5.0/03-web-frontend-security/05-browser-origin-separation#V3.5.7) *Data requiring authorization is not included in sc ...* 

- [V3.5.8](/taxonomy/asvs-5.0/03-web-frontend-security/05-browser-origin-separation#V3.5.8) *Authenticated resources (such as images, videos, s ...* 

### 06-external-resource-integrity

- [V3.6.1](/taxonomy/asvs-5.0/03-web-frontend-security/06-external-resource-integrity#V3.6.1) *Client-side assets, such as javascript libraries,  ...* 

### 07-other-browser-security-considerations

- [V3.7.3](/taxonomy/asvs-5.0/03-web-frontend-security/07-other-browser-security-considerations#V3.7.3) *The application shows a notification when the user ...* 

- [V3.7.4](/taxonomy/asvs-5.0/03-web-frontend-security/07-other-browser-security-considerations#V3.7.4) *The application's top-level domain (e.g., site.tld ...* 

- [V3.7.5](/taxonomy/asvs-5.0/03-web-frontend-security/07-other-browser-security-considerations#V3.7.5) *The application behaves as documented (such as war ...* 

## 04-api-and-web-service

### 01-generic-web-service-security

- [V4.1.4](/taxonomy/asvs-5.0/04-api-and-web-service/01-generic-web-service-security#V4.1.4) *Only http methods that are explicitly supported by ...* 

- [V4.1.5](/taxonomy/asvs-5.0/04-api-and-web-service/01-generic-web-service-security#V4.1.5) *Per-message digital signatures are used to provide ...* 

### 02-http-message-structure-validation

- [V4.2.2](/taxonomy/asvs-5.0/04-api-and-web-service/02-http-message-structure-validation#V4.2.2) *When generating http messages, the content-length  ...* 

- [V4.2.3](/taxonomy/asvs-5.0/04-api-and-web-service/02-http-message-structure-validation#V4.2.3) *The application does not send nor accept http/2 or ...* 

- [V4.2.4](/taxonomy/asvs-5.0/04-api-and-web-service/02-http-message-structure-validation#V4.2.4) *The application only accepts http/2 and http/3 req ...* 

- [V4.2.5](/taxonomy/asvs-5.0/04-api-and-web-service/02-http-message-structure-validation#V4.2.5) *, if the application (backend or frontend) builds  ...* 

## 05-file-handling

### 02-file-upload-and-content

- [V5.2.4](/taxonomy/asvs-5.0/05-file-handling/02-file-upload-and-content#V5.2.4) *A file size quota and maximum number of files per  ...* 

- [V5.2.5](/taxonomy/asvs-5.0/05-file-handling/02-file-upload-and-content#V5.2.5) *The application does not allow uploading compresse ...* 

- [V5.2.6](/taxonomy/asvs-5.0/05-file-handling/02-file-upload-and-content#V5.2.6) *The application rejects uploaded images with a pix ...* 

### 03-file-storage

- [V5.3.3](/taxonomy/asvs-5.0/05-file-handling/03-file-storage#V5.3.3) *Server-side file processing, such as file decompre ...* 

## 06-authentication

### 03-general-authentication-security

- [V6.3.5](/taxonomy/asvs-5.0/06-authentication/03-general-authentication-security#V6.3.5) *Users are notified of suspicious authentication at ...* 

- [V6.3.6](/taxonomy/asvs-5.0/06-authentication/03-general-authentication-security#V6.3.6) *Email is not used as either a single-factor or mul ...* 

- [V6.3.7](/taxonomy/asvs-5.0/06-authentication/03-general-authentication-security#V6.3.7) *Users are notified after updates to authentication ...* 

- [V6.3.8](/taxonomy/asvs-5.0/06-authentication/03-general-authentication-security#V6.3.8) *Valid users cannot be deduced from failed authenti ...* 

### 04-authentication-factor-lifecycle-and-recovery

- [V6.4.5](/taxonomy/asvs-5.0/06-authentication/04-authentication-factor-lifecycle-and-recovery#V6.4.5) *Renewal instructions for authentication mechanisms ...* 

- [V6.4.6](/taxonomy/asvs-5.0/06-authentication/04-authentication-factor-lifecycle-and-recovery#V6.4.6) *Administrative users can initiate the password res ...* 

### 05-general-multi-factor-authentication-requirements

- [V6.5.6](/taxonomy/asvs-5.0/06-authentication/05-general-multi-factor-authentication-requirements#V6.5.6) *Any authentication factor (including physical devi ...* 

- [V6.5.7](/taxonomy/asvs-5.0/06-authentication/05-general-multi-factor-authentication-requirements#V6.5.7) *Biometric authentication mechanisms are only used  ...* 

- [V6.5.8](/taxonomy/asvs-5.0/06-authentication/05-general-multi-factor-authentication-requirements#V6.5.8) *Time-based one-time passwords (totps) are checked  ...* 

### 06-out-of-band-authentication-mechanisms

- [V6.6.4](/taxonomy/asvs-5.0/06-authentication/06-out-of-band-authentication-mechanisms#V6.6.4) *, where push notifications are used for multi-fact ...* 

### 07-cryptographic-authentication-mechanism

- [V6.7.1](/taxonomy/asvs-5.0/06-authentication/07-cryptographic-authentication-mechanism#V6.7.1) *The certificates used to verify cryptographic auth ...* 

- [V6.7.2](/taxonomy/asvs-5.0/06-authentication/07-cryptographic-authentication-mechanism#V6.7.2) *The challenge nonce is at least 64 bits in length, ...* 

## 07-session-management

### 05-defenses-against-session-abuse

- [V7.5.3](/taxonomy/asvs-5.0/07-session-management/05-defenses-against-session-abuse#V7.5.3) *The application requires further authentication wi ...* 

## 08-authorization

### 01-authorization-documentation

- [V8.1.3](/taxonomy/asvs-5.0/08-authorization/01-authorization-documentation#V8.1.3) *The application's documentation defines the enviro ...* 

- [V8.1.4](/taxonomy/asvs-5.0/08-authorization/01-authorization-documentation#V8.1.4) *Authentication and authorization documentation def ...* 

### 02-general-authorization-design

- [V8.2.4](/taxonomy/asvs-5.0/08-authorization/02-general-authorization-design#V8.2.4) *Adaptive security controls based on a consumer's e ...* 

### 03-operation-level-authorization

- [V8.3.2](/taxonomy/asvs-5.0/08-authorization/03-operation-level-authorization#V8.3.2) *Changes to values on which authorization decisions ...* 

- [V8.3.3](/taxonomy/asvs-5.0/08-authorization/03-operation-level-authorization#V8.3.3) *Access to an object is based on the originating su ...* 

### 04-other-authorization-considerations

- [V8.4.2](/taxonomy/asvs-5.0/08-authorization/04-other-authorization-considerations#V8.4.2) *Access to administrative interfaces incorporates m ...* 

## 10-oauth-and-oidc

### 02-oauth-client

- [V10.2.3](/taxonomy/asvs-5.0/10-oauth-and-oidc/02-oauth-client#V10.2.3) *The oauth client only requests the required scopes ...* 

### 03-oauth-resource-server

- [V10.3.5](/taxonomy/asvs-5.0/10-oauth-and-oidc/03-oauth-resource-server#V10.3.5) *The resource server prevents the use of stolen acc ...* 

### 04-oauth-authorization-server

- [V10.4.12](/taxonomy/asvs-5.0/10-oauth-and-oidc/04-oauth-authorization-server#V10.4.12) *For a given client, the authorization server only  ...* 

- [V10.4.13](/taxonomy/asvs-5.0/10-oauth-and-oidc/04-oauth-authorization-server#V10.4.13) *Grant type 'code' is always used together with pus ...* 

- [V10.4.14](/taxonomy/asvs-5.0/10-oauth-and-oidc/04-oauth-authorization-server#V10.4.14) *The authorization server issues only sender-constr ...* 

- [V10.4.15](/taxonomy/asvs-5.0/10-oauth-and-oidc/04-oauth-authorization-server#V10.4.15) *, for a server-side client (which is not executed  ...* 

- [V10.4.16](/taxonomy/asvs-5.0/10-oauth-and-oidc/04-oauth-authorization-server#V10.4.16) *The client is confidential and the authorization s ...* 

## 11-cryptography

### 01-cryptographic-inventory-and-documentation

- [V11.1.3](/taxonomy/asvs-5.0/11-cryptography/01-cryptographic-inventory-and-documentation#V11.1.3) *Cryptographic discovery mechanisms are employed to ...* 

- [V11.1.4](/taxonomy/asvs-5.0/11-cryptography/01-cryptographic-inventory-and-documentation#V11.1.4) *A cryptographic inventory is maintained. this must ...* 

### 02-secure-cryptography-implementation

- [V11.2.4](/taxonomy/asvs-5.0/11-cryptography/02-secure-cryptography-implementation#V11.2.4) *All cryptographic operations are constant-time, wi ...* 

- [V11.2.5](/taxonomy/asvs-5.0/11-cryptography/02-secure-cryptography-implementation#V11.2.5) *All cryptographic modules fail securely, and error ...* 

### 03-encryption-algorithms

- [V11.3.4](/taxonomy/asvs-5.0/11-cryptography/03-encryption-algorithms#V11.3.4) *Nonces, initialization vectors, and other single-u ...* 

- [V11.3.5](/taxonomy/asvs-5.0/11-cryptography/03-encryption-algorithms#V11.3.5) *Any combination of an encryption algorithm and a m ...* 

### 05-random-values

- [V11.5.2](/taxonomy/asvs-5.0/11-cryptography/05-random-values#V11.5.2) *The random number generation mechanism in use is d ...* 

### 06-public-key-cryptography

- [V11.6.2](/taxonomy/asvs-5.0/11-cryptography/06-public-key-cryptography#V11.6.2) *Approved cryptographic algorithms are used for key ...* 

### 07-in-use-data-cryptography

- [V11.7.1](/taxonomy/asvs-5.0/11-cryptography/07-in-use-data-cryptography#V11.7.1) *Full memory encryption is in use that protects sen ...* 

- [V11.7.2](/taxonomy/asvs-5.0/11-cryptography/07-in-use-data-cryptography#V11.7.2) *Data minimization ensures the minimal amount of da ...* 

## 12-secure-communication

### 01-general-tls-security-guidance

- [V12.1.4](/taxonomy/asvs-5.0/12-secure-communication/01-general-tls-security-guidance#V12.1.4) *Proper certification revocation, such as online ce ...* 

- [V12.1.5](/taxonomy/asvs-5.0/12-secure-communication/01-general-tls-security-guidance#V12.1.5) *Encrypted client hello (ech) is enabled in the app ...* 

### 03-general-service-to-service-communication-security

- [V12.3.5](/taxonomy/asvs-5.0/12-secure-communication/03-general-service-to-service-communication-security#V12.3.5) *Services communicating internally within a system  ...* 

## 13-configuration

### 01-configuration-documentation

- [V13.1.2](/taxonomy/asvs-5.0/13-configuration/01-configuration-documentation#V13.1.2) *For each service the application uses, the documen ...* 

- [V13.1.3](/taxonomy/asvs-5.0/13-configuration/01-configuration-documentation#V13.1.3) *The application documentation defines resource‑man ...* 

- [V13.1.4](/taxonomy/asvs-5.0/13-configuration/01-configuration-documentation#V13.1.4) *The application's documentation defines the secret ...* 

### 02-backend-communication-configuration

- [V13.2.6](/taxonomy/asvs-5.0/13-configuration/02-backend-communication-configuration#V13.2.6) *Where the application connects to separate service ...* 

### 03-secret-management

- [V13.3.3](/taxonomy/asvs-5.0/13-configuration/03-secret-management#V13.3.3) *All cryptographic operations are performed using a ...* 

- [V13.3.4](/taxonomy/asvs-5.0/13-configuration/03-secret-management#V13.3.4) *Secrets are configured to expire and be rotated ba ...* 

### 04-unintended-information-leakage

- [V13.4.6](/taxonomy/asvs-5.0/13-configuration/04-unintended-information-leakage#V13.4.6) *The application does not expose detailed version i ...* 

- [V13.4.7](/taxonomy/asvs-5.0/13-configuration/04-unintended-information-leakage#V13.4.7) *The web tier is configured to only serve files wit ...* 

## 14-data-protection

### 02-general-data-protection

- [V14.2.5](/taxonomy/asvs-5.0/14-data-protection/02-general-data-protection#V14.2.5) *Caching mechanisms are configured to only cache re ...* 

- [V14.2.6](/taxonomy/asvs-5.0/14-data-protection/02-general-data-protection#V14.2.6) *The application only returns the minimum required  ...* 

- [V14.2.7](/taxonomy/asvs-5.0/14-data-protection/02-general-data-protection#V14.2.7) *Sensitive information is subject to data retention ...* 

- [V14.2.8](/taxonomy/asvs-5.0/14-data-protection/02-general-data-protection#V14.2.8) *Sensitive information is removed from the metadata ...* 

## 15-secure-coding-and-architecture

### 01-secure-coding-and-architecture-documentation

- [V15.1.4](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/01-secure-coding-and-architecture-documentation#V15.1.4) *Application documentation highlights third-party l ...* 

- [V15.1.5](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/01-secure-coding-and-architecture-documentation#V15.1.5) *Application documentation highlights parts of the  ...* 

### 02-security-architecture-and-dependencies

- [V15.2.4](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/02-security-architecture-and-dependencies#V15.2.4) *Third-party components and all of their transitive ...* 

- [V15.2.5](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/02-security-architecture-and-dependencies#V15.2.5) *The application implements additional protections  ...* 

### 04-safe-concurrency

- [V15.4.1](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/04-safe-concurrency#V15.4.1) *Shared objects in multi-threaded code (such as cac ...* 

- [V15.4.2](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/04-safe-concurrency#V15.4.2) *Checks on a resource's state, such as its existenc ...* 

- [V15.4.3](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/04-safe-concurrency#V15.4.3) *Locks are used consistently to avoid threads getti ...* 

- [V15.4.4](/taxonomy/asvs-5.0/15-secure-coding-and-architecture/04-safe-concurrency#V15.4.4) *Resource allocation policies prevent thread starva ...* 

## 16-security-logging-and-error-handling

### 05-error-handling

- [V16.5.4](/taxonomy/asvs-5.0/16-security-logging-and-error-handling/05-error-handling#V16.5.4) *A "last resort" error handler is defined which wil ...* 

## 17-webrtc

### 01-turn-server

- [V17.1.2](/taxonomy/asvs-5.0/17-webrtc/01-turn-server#V17.1.2) *The traversal using relays around nat (turn) servi ...* 

### 02-media

- [V17.2.5](/taxonomy/asvs-5.0/17-webrtc/02-media#V17.2.5) *The media server is able to continue processing in ...* 

- [V17.2.6](/taxonomy/asvs-5.0/17-webrtc/02-media#V17.2.6) *The media server is not susceptible to the "client ...* 

- [V17.2.7](/taxonomy/asvs-5.0/17-webrtc/02-media#V17.2.7) *Any audio or video recording mechanisms associated ...* 

- [V17.2.8](/taxonomy/asvs-5.0/17-webrtc/02-media#V17.2.8) *The datagram transport layer security (dtls) certi ...* 

