# Level 2 controls

Level 2 contains 183 controls listed below: 

## 01-encoding-and-sanitization

### 01-encoding-and-sanitization-architecture

- [V1.1.1](/taxonomy/asvs-4.0.3/01-encoding-and-sanitization/01-encoding-and-sanitization-architecture#V1.1.1) *Input is decoded or unescaped into a canonical for ...* 

- [V1.1.2](/taxonomy/asvs-4.0.3/01-encoding-and-sanitization/01-encoding-and-sanitization-architecture#V1.1.2) *The application performs output encoding and escap ...* 

### 02-injection-prevention

- [V1.2.6](/taxonomy/asvs-4.0.3/01-encoding-and-sanitization/02-injection-prevention#V1.2.6) *The application protects against ldap injection vu ...* 

- [V1.2.7](/taxonomy/asvs-4.0.3/01-encoding-and-sanitization/02-injection-prevention#V1.2.7) *The application is protected against xpath injecti ...* 

- [V1.2.8](/taxonomy/asvs-4.0.3/01-encoding-and-sanitization/02-injection-prevention#V1.2.8) *Latex processors are configured securely (such as  ...* 

- [V1.2.9](/taxonomy/asvs-4.0.3/01-encoding-and-sanitization/02-injection-prevention#V1.2.9) *The application escapes special characters in regu ...* 

### 03-sanitization

- [V1.3.3](/taxonomy/asvs-4.0.3/01-encoding-and-sanitization/03-sanitization#V1.3.3) *Data being passed to a potentially dangerous conte ...* 

- [V1.3.4](/taxonomy/asvs-4.0.3/01-encoding-and-sanitization/03-sanitization#V1.3.4) *User-supplied scalable vector graphics (svg) scrip ...* 

- [V1.3.5](/taxonomy/asvs-4.0.3/01-encoding-and-sanitization/03-sanitization#V1.3.5) *The application sanitizes or disables user-supplie ...* 

- [V1.3.6](/taxonomy/asvs-4.0.3/01-encoding-and-sanitization/03-sanitization#V1.3.6) *The application protects against server-side reque ...* 

- [V1.3.7](/taxonomy/asvs-4.0.3/01-encoding-and-sanitization/03-sanitization#V1.3.7) *The application protects against template injectio ...* 

- [V1.3.8](/taxonomy/asvs-4.0.3/01-encoding-and-sanitization/03-sanitization#V1.3.8) *The application appropriately sanitizes untrusted  ...* 

- [V1.3.9](/taxonomy/asvs-4.0.3/01-encoding-and-sanitization/03-sanitization#V1.3.9) *The application sanitizes content before it is sen ...* 

- [V1.3.10](/taxonomy/asvs-4.0.3/01-encoding-and-sanitization/03-sanitization#V1.3.10) *Format strings which might resolve in an unexpecte ...* 

- [V1.3.11](/taxonomy/asvs-4.0.3/01-encoding-and-sanitization/03-sanitization#V1.3.11) *The application sanitizes user input before passin ...* 

### 04-memory-string-and-unmanaged-code

- [V1.4.1](/taxonomy/asvs-4.0.3/01-encoding-and-sanitization/04-memory-string-and-unmanaged-code#V1.4.1) *The application uses memory-safe string, safer mem ...* 

- [V1.4.2](/taxonomy/asvs-4.0.3/01-encoding-and-sanitization/04-memory-string-and-unmanaged-code#V1.4.2) *Sign, range, and input validation techniques are u ...* 

- [V1.4.3](/taxonomy/asvs-4.0.3/01-encoding-and-sanitization/04-memory-string-and-unmanaged-code#V1.4.3) *Dynamically allocated memory and resources are rel ...* 

### 05-safe-deserialization

- [V1.5.2](/taxonomy/asvs-4.0.3/01-encoding-and-sanitization/05-safe-deserialization#V1.5.2) *Deserialization of untrusted data enforces safe in ...* 

## 02-validation-and-business-logic

### 01-validation-and-business-logic-documentation

- [V2.1.2](/taxonomy/asvs-4.0.3/02-validation-and-business-logic/01-validation-and-business-logic-documentation#V2.1.2) *The application's documentation defines how to val ...* 

- [V2.1.3](/taxonomy/asvs-4.0.3/02-validation-and-business-logic/01-validation-and-business-logic-documentation#V2.1.3) *Expectations for business logic limits and validat ...* 

### 02-input-validation

- [V2.2.3](/taxonomy/asvs-4.0.3/02-validation-and-business-logic/02-input-validation#V2.2.3) *The application ensures that combinations of relat ...* 

### 03-business-logic-security

- [V2.3.2](/taxonomy/asvs-4.0.3/02-validation-and-business-logic/03-business-logic-security#V2.3.2) *Business logic limits are implemented per the appl ...* 

- [V2.3.3](/taxonomy/asvs-4.0.3/02-validation-and-business-logic/03-business-logic-security#V2.3.3) *Transactions are being used at the business logic  ...* 

- [V2.3.4](/taxonomy/asvs-4.0.3/02-validation-and-business-logic/03-business-logic-security#V2.3.4) *Business logic level locking mechanisms are used t ...* 

### 04-anti-automation

- [V2.4.1](/taxonomy/asvs-4.0.3/02-validation-and-business-logic/04-anti-automation#V2.4.1) *Anti-automation controls are in place to protect a ...* 

## 03-web-frontend-security

### 03-cookie-setup

- [V3.3.2](/taxonomy/asvs-4.0.3/03-web-frontend-security/03-cookie-setup#V3.3.2) *Each cookie's 'samesite' attribute value is set ac ...* 

- [V3.3.3](/taxonomy/asvs-4.0.3/03-web-frontend-security/03-cookie-setup#V3.3.3) *Cookies have the '__host-' prefix for the cookie n ...* 

- [V3.3.4](/taxonomy/asvs-4.0.3/03-web-frontend-security/03-cookie-setup#V3.3.4) *If the value of a cookie is not meant to be access ...* 

### 04-browser-security-mechanism-headers

- [V3.4.3](/taxonomy/asvs-4.0.3/03-web-frontend-security/04-browser-security-mechanism-headers#V3.4.3) *Http responses include a content-security-policy r ...* 

- [V3.4.4](/taxonomy/asvs-4.0.3/03-web-frontend-security/04-browser-security-mechanism-headers#V3.4.4) *All http responses contain an 'x-content-type-opti ...* 

- [V3.4.5](/taxonomy/asvs-4.0.3/03-web-frontend-security/04-browser-security-mechanism-headers#V3.4.5) *The application sets a referrer policy to prevent  ...* 

- [V3.4.6](/taxonomy/asvs-4.0.3/03-web-frontend-security/04-browser-security-mechanism-headers#V3.4.6) *The web application uses the frame-ancestors direc ...* 

### 05-browser-origin-separation

- [V3.5.4](/taxonomy/asvs-4.0.3/03-web-frontend-security/05-browser-origin-separation#V3.5.4) *Separate applications are hosted on different host ...* 

- [V3.5.5](/taxonomy/asvs-4.0.3/03-web-frontend-security/05-browser-origin-separation#V3.5.5) *Messages received by the postmessage interface are ...* 

### 07-other-browser-security-considerations

- [V3.7.1](/taxonomy/asvs-4.0.3/03-web-frontend-security/07-other-browser-security-considerations#V3.7.1) *The application only uses client-side technologies ...* 

- [V3.7.2](/taxonomy/asvs-4.0.3/03-web-frontend-security/07-other-browser-security-considerations#V3.7.2) *The application will only automatically redirect t ...* 

## 04-api-and-web-service

### 01-generic-web-service-security

- [V4.1.2](/taxonomy/asvs-4.0.3/04-api-and-web-service/01-generic-web-service-security#V4.1.2) *Only user-facing endpoints (intended for manual we ...* 

- [V4.1.3](/taxonomy/asvs-4.0.3/04-api-and-web-service/01-generic-web-service-security#V4.1.3) *Any http header field used by the application and  ...* 

### 02-http-message-structure-validation

- [V4.2.1](/taxonomy/asvs-4.0.3/04-api-and-web-service/02-http-message-structure-validation#V4.2.1) *All application components (including load balance ...* 

### 03-graphql

- [V4.3.1](/taxonomy/asvs-4.0.3/04-api-and-web-service/03-graphql#V4.3.1) *A query allowlist, depth limiting, amount limiting ...* 

- [V4.3.2](/taxonomy/asvs-4.0.3/04-api-and-web-service/03-graphql#V4.3.2) *Graphql introspection queries are disabled in the  ...* 

### 04-websocket

- [V4.4.2](/taxonomy/asvs-4.0.3/04-api-and-web-service/04-websocket#V4.4.2) *, during the initial http websocket handshake, the ...* 

- [V4.4.3](/taxonomy/asvs-4.0.3/04-api-and-web-service/04-websocket#V4.4.3) *, if the application's standard session management ...* 

- [V4.4.4](/taxonomy/asvs-4.0.3/04-api-and-web-service/04-websocket#V4.4.4) *Dedicated websocket session management tokens are  ...* 

## 05-file-handling

### 01-file-handling-documentation

- [V5.1.1](/taxonomy/asvs-4.0.3/05-file-handling/01-file-handling-documentation#V5.1.1) *The documentation defines the permitted file types ...* 

### 02-file-upload-and-content

- [V5.2.3](/taxonomy/asvs-4.0.3/05-file-handling/02-file-upload-and-content#V5.2.3) *The application checks compressed files (e.g., zip ...* 

### 04-file-download

- [V5.4.1](/taxonomy/asvs-4.0.3/05-file-handling/04-file-download#V5.4.1) *The application validates or ignores user-submitte ...* 

- [V5.4.2](/taxonomy/asvs-4.0.3/05-file-handling/04-file-download#V5.4.2) *File names served (e.g., in http response header f ...* 

- [V5.4.3](/taxonomy/asvs-4.0.3/05-file-handling/04-file-download#V5.4.3) *Files obtained from untrusted sources are scanned  ...* 

## 06-authentication

### 01-authentication-documentation

- [V6.1.2](/taxonomy/asvs-4.0.3/06-authentication/01-authentication-documentation#V6.1.2) *A list of context-specific words is documented in  ...* 

- [V6.1.3](/taxonomy/asvs-4.0.3/06-authentication/01-authentication-documentation#V6.1.3) *, if the application includes multiple authenticat ...* 

### 02-password-security

- [V6.2.9](/taxonomy/asvs-4.0.3/06-authentication/02-password-security#V6.2.9) *Passwords of at least 64 characters are permitted. ...* 

- [V6.2.10](/taxonomy/asvs-4.0.3/06-authentication/02-password-security#V6.2.10) *A user's password stays valid until it is discover ...* 

- [V6.2.11](/taxonomy/asvs-4.0.3/06-authentication/02-password-security#V6.2.11) *The documented list of context specific words is u ...* 

- [V6.2.12](/taxonomy/asvs-4.0.3/06-authentication/02-password-security#V6.2.12) *Passwords submitted during account registration or ...* 

### 03-general-authentication-security

- [V6.3.3](/taxonomy/asvs-4.0.3/06-authentication/03-general-authentication-security#V6.3.3) *Either a multi-factor authentication mechanism or  ...* 

- [V6.3.4](/taxonomy/asvs-4.0.3/06-authentication/03-general-authentication-security#V6.3.4) *, if the application includes multiple authenticat ...* 

### 04-authentication-factor-lifecycle-and-recovery

- [V6.4.3](/taxonomy/asvs-4.0.3/06-authentication/04-authentication-factor-lifecycle-and-recovery#V6.4.3) *A secure process for resetting a forgotten passwor ...* 

- [V6.4.4](/taxonomy/asvs-4.0.3/06-authentication/04-authentication-factor-lifecycle-and-recovery#V6.4.4) *If a multi-factor authentication factor is lost, e ...* 

### 05-general-multi-factor-authentication-requirements

- [V6.5.1](/taxonomy/asvs-4.0.3/06-authentication/05-general-multi-factor-authentication-requirements#V6.5.1) *Lookup secrets, out-of-band authentication request ...* 

- [V6.5.2](/taxonomy/asvs-4.0.3/06-authentication/05-general-multi-factor-authentication-requirements#V6.5.2) *, when being stored in the application's backend,  ...* 

- [V6.5.3](/taxonomy/asvs-4.0.3/06-authentication/05-general-multi-factor-authentication-requirements#V6.5.3) *Lookup secrets, out-of-band authentication code, a ...* 

- [V6.5.4](/taxonomy/asvs-4.0.3/06-authentication/05-general-multi-factor-authentication-requirements#V6.5.4) *Lookup secrets and out-of-band authentication code ...* 

- [V6.5.5](/taxonomy/asvs-4.0.3/06-authentication/05-general-multi-factor-authentication-requirements#V6.5.5) *Out-of-band authentication requests, codes, or tok ...* 

### 06-out-of-band-authentication-mechanisms

- [V6.6.1](/taxonomy/asvs-4.0.3/06-authentication/06-out-of-band-authentication-mechanisms#V6.6.1) *Authentication mechanisms using the public switche ...* 

- [V6.6.2](/taxonomy/asvs-4.0.3/06-authentication/06-out-of-band-authentication-mechanisms#V6.6.2) *Out-of-band authentication requests, codes, or tok ...* 

- [V6.6.3](/taxonomy/asvs-4.0.3/06-authentication/06-out-of-band-authentication-mechanisms#V6.6.3) *A code based out-of-band authentication mechanism  ...* 

### 08-authentication-with-an-identity-provider

- [V6.8.1](/taxonomy/asvs-4.0.3/06-authentication/08-authentication-with-an-identity-provider#V6.8.1) *, if the application supports multiple identity pr ...* 

- [V6.8.2](/taxonomy/asvs-4.0.3/06-authentication/08-authentication-with-an-identity-provider#V6.8.2) *The presence and integrity of digital signatures o ...* 

- [V6.8.3](/taxonomy/asvs-4.0.3/06-authentication/08-authentication-with-an-identity-provider#V6.8.3) *Saml assertions are uniquely processed and used on ...* 

- [V6.8.4](/taxonomy/asvs-4.0.3/06-authentication/08-authentication-with-an-identity-provider#V6.8.4) *, if an application uses a separate identity provi ...* 

## 07-session-management

### 01-session-management-documentation

- [V7.1.1](/taxonomy/asvs-4.0.3/07-session-management/01-session-management-documentation#V7.1.1) *The user's session inactivity timeout and absolute ...* 

- [V7.1.2](/taxonomy/asvs-4.0.3/07-session-management/01-session-management-documentation#V7.1.2) *The documentation defines how many concurrent (par ...* 

- [V7.1.3](/taxonomy/asvs-4.0.3/07-session-management/01-session-management-documentation#V7.1.3) *All systems that create and manage user sessions a ...* 

### 03-session-timeout

- [V7.3.1](/taxonomy/asvs-4.0.3/07-session-management/03-session-timeout#V7.3.1) *There is an inactivity timeout such that re-authen ...* 

- [V7.3.2](/taxonomy/asvs-4.0.3/07-session-management/03-session-timeout#V7.3.2) *There is an absolute maximum session lifetime such ...* 

### 04-session-termination

- [V7.4.3](/taxonomy/asvs-4.0.3/07-session-management/04-session-termination#V7.4.3) *The application gives the option to terminate all  ...* 

- [V7.4.4](/taxonomy/asvs-4.0.3/07-session-management/04-session-termination#V7.4.4) *All pages that require authentication have easy an ...* 

- [V7.4.5](/taxonomy/asvs-4.0.3/07-session-management/04-session-termination#V7.4.5) *Application administrators are able to terminate a ...* 

### 05-defenses-against-session-abuse

- [V7.5.1](/taxonomy/asvs-4.0.3/07-session-management/05-defenses-against-session-abuse#V7.5.1) *The application requires full re-authentication be ...* 

- [V7.5.2](/taxonomy/asvs-4.0.3/07-session-management/05-defenses-against-session-abuse#V7.5.2) *Users are able to view and (having authenticated a ...* 

### 06-federated-re-authentication

- [V7.6.1](/taxonomy/asvs-4.0.3/07-session-management/06-federated-re-authentication#V7.6.1) *Session lifetime and termination between relying p ...* 

- [V7.6.2](/taxonomy/asvs-4.0.3/07-session-management/06-federated-re-authentication#V7.6.2) *Creation of a session requires either the user's c ...* 

## 08-authorization

### 01-authorization-documentation

- [V8.1.2](/taxonomy/asvs-4.0.3/08-authorization/01-authorization-documentation#V8.1.2) *Authorization documentation defines rules for fiel ...* 

### 02-general-authorization-design

- [V8.2.3](/taxonomy/asvs-4.0.3/08-authorization/02-general-authorization-design#V8.2.3) *The application ensures that field-level access is ...* 

### 04-other-authorization-considerations

- [V8.4.1](/taxonomy/asvs-4.0.3/08-authorization/04-other-authorization-considerations#V8.4.1) *Multi-tenant applications use cross-tenant control ...* 

## 09-self-contained-tokens

### 02-token-content

- [V9.2.2](/taxonomy/asvs-4.0.3/09-self-contained-tokens/02-token-content#V9.2.2) *The service receiving a token validates the token  ...* 

- [V9.2.3](/taxonomy/asvs-4.0.3/09-self-contained-tokens/02-token-content#V9.2.3) *The service only accepts tokens which are intended ...* 

- [V9.2.4](/taxonomy/asvs-4.0.3/09-self-contained-tokens/02-token-content#V9.2.4) *, if a token issuer uses the same private key for  ...* 

## 10-oauth-and-oidc

### 01-generic-oauth-and-oidc-security

- [V10.1.1](/taxonomy/asvs-4.0.3/10-oauth-and-oidc/01-generic-oauth-and-oidc-security#V10.1.1) *Tokens are only sent to components that strictly n ...* 

- [V10.1.2](/taxonomy/asvs-4.0.3/10-oauth-and-oidc/01-generic-oauth-and-oidc-security#V10.1.2) *The client only accepts values from the authorizat ...* 

### 02-oauth-client

- [V10.2.1](/taxonomy/asvs-4.0.3/10-oauth-and-oidc/02-oauth-client#V10.2.1) *, if the code flow is used, the oauth client has p ...* 

- [V10.2.2](/taxonomy/asvs-4.0.3/10-oauth-and-oidc/02-oauth-client#V10.2.2) *, if the oauth client can interact with more than  ...* 

### 03-oauth-resource-server

- [V10.3.1](/taxonomy/asvs-4.0.3/10-oauth-and-oidc/03-oauth-resource-server#V10.3.1) *The resource server only accepts access tokens tha ...* 

- [V10.3.2](/taxonomy/asvs-4.0.3/10-oauth-and-oidc/03-oauth-resource-server#V10.3.2) *The resource server enforces authorization decisio ...* 

- [V10.3.3](/taxonomy/asvs-4.0.3/10-oauth-and-oidc/03-oauth-resource-server#V10.3.3) *If an access control decision requires identifying ...* 

- [V10.3.4](/taxonomy/asvs-4.0.3/10-oauth-and-oidc/03-oauth-resource-server#V10.3.4) *, if the resource server requires specific authent ...* 

### 04-oauth-authorization-server

- [V10.4.6](/taxonomy/asvs-4.0.3/10-oauth-and-oidc/04-oauth-authorization-server#V10.4.6) *, if the code grant is used, the authorization ser ...* 

- [V10.4.7](/taxonomy/asvs-4.0.3/10-oauth-and-oidc/04-oauth-authorization-server#V10.4.7) *If the authorization server supports unauthenticat ...* 

- [V10.4.8](/taxonomy/asvs-4.0.3/10-oauth-and-oidc/04-oauth-authorization-server#V10.4.8) *Refresh tokens have an absolute expiration, includ ...* 

- [V10.4.9](/taxonomy/asvs-4.0.3/10-oauth-and-oidc/04-oauth-authorization-server#V10.4.9) *Refresh tokens and reference access tokens can be  ...* 

- [V10.4.10](/taxonomy/asvs-4.0.3/10-oauth-and-oidc/04-oauth-authorization-server#V10.4.10) *Confidential client is authenticated for client-to ...* 

- [V10.4.11](/taxonomy/asvs-4.0.3/10-oauth-and-oidc/04-oauth-authorization-server#V10.4.11) *The authorization server configuration only assign ...* 

### 05-oidc-client

- [V10.5.1](/taxonomy/asvs-4.0.3/10-oauth-and-oidc/05-oidc-client#V10.5.1) *The client (as the relying party) mitigates id tok ...* 

- [V10.5.2](/taxonomy/asvs-4.0.3/10-oauth-and-oidc/05-oidc-client#V10.5.2) *The client uniquely identifies the user from id to ...* 

- [V10.5.3](/taxonomy/asvs-4.0.3/10-oauth-and-oidc/05-oidc-client#V10.5.3) *The client rejects attempts by a malicious authori ...* 

- [V10.5.4](/taxonomy/asvs-4.0.3/10-oauth-and-oidc/05-oidc-client#V10.5.4) *The client validates that the id token is intended ...* 

- [V10.5.5](/taxonomy/asvs-4.0.3/10-oauth-and-oidc/05-oidc-client#V10.5.5) *, when using oidc back-channel logout, the relying ...* 

### 06-openid-provider

- [V10.6.1](/taxonomy/asvs-4.0.3/10-oauth-and-oidc/06-openid-provider#V10.6.1) *The openid provider only allows values 'code', 'ci ...* 

- [V10.6.2](/taxonomy/asvs-4.0.3/10-oauth-and-oidc/06-openid-provider#V10.6.2) *The openid provider mitigates denial of service th ...* 

### 07-consent-management

- [V10.7.1](/taxonomy/asvs-4.0.3/10-oauth-and-oidc/07-consent-management#V10.7.1) *The authorization server ensures that the user con ...* 

- [V10.7.2](/taxonomy/asvs-4.0.3/10-oauth-and-oidc/07-consent-management#V10.7.2) *When the authorization server prompts for user con ...* 

- [V10.7.3](/taxonomy/asvs-4.0.3/10-oauth-and-oidc/07-consent-management#V10.7.3) *The user can review, modify, and revoke consents w ...* 

## 11-cryptography

### 01-cryptographic-inventory-and-documentation

- [V11.1.1](/taxonomy/asvs-4.0.3/11-cryptography/01-cryptographic-inventory-and-documentation#V11.1.1) *There is a documented policy for management of cry ...* 

- [V11.1.2](/taxonomy/asvs-4.0.3/11-cryptography/01-cryptographic-inventory-and-documentation#V11.1.2) *A cryptographic inventory is performed, maintained ...* 

### 02-secure-cryptography-implementation

- [V11.2.1](/taxonomy/asvs-4.0.3/11-cryptography/02-secure-cryptography-implementation#V11.2.1) *Industry-validated implementations (including libr ...* 

- [V11.2.2](/taxonomy/asvs-4.0.3/11-cryptography/02-secure-cryptography-implementation#V11.2.2) *The application is designed with crypto agility su ...* 

- [V11.2.3](/taxonomy/asvs-4.0.3/11-cryptography/02-secure-cryptography-implementation#V11.2.3) *All cryptographic primitives utilize a minimum of  ...* 

### 03-encryption-algorithms

- [V11.3.3](/taxonomy/asvs-4.0.3/11-cryptography/03-encryption-algorithms#V11.3.3) *Encrypted data is protected against unauthorized m ...* 

### 04-hashing-and-hash-based-functions

- [V11.4.2](/taxonomy/asvs-4.0.3/11-cryptography/04-hashing-and-hash-based-functions#V11.4.2) *Passwords are stored using an approved, computatio ...* 

- [V11.4.3](/taxonomy/asvs-4.0.3/11-cryptography/04-hashing-and-hash-based-functions#V11.4.3) *Hash functions used in digital signatures, as part ...* 

- [V11.4.4](/taxonomy/asvs-4.0.3/11-cryptography/04-hashing-and-hash-based-functions#V11.4.4) *The application uses approved key derivation funct ...* 

### 05-random-values

- [V11.5.1](/taxonomy/asvs-4.0.3/11-cryptography/05-random-values#V11.5.1) *All random numbers and strings which are intended  ...* 

### 06-public-key-cryptography

- [V11.6.1](/taxonomy/asvs-4.0.3/11-cryptography/06-public-key-cryptography#V11.6.1) *Only approved cryptographic algorithms and modes o ...* 

## 12-secure-communication

### 01-general-tls-security-guidance

- [V12.1.2](/taxonomy/asvs-4.0.3/12-secure-communication/01-general-tls-security-guidance#V12.1.2) *Only recommended cipher suites are enabled, with t ...* 

- [V12.1.3](/taxonomy/asvs-4.0.3/12-secure-communication/01-general-tls-security-guidance#V12.1.3) *The application validates that mtls client certifi ...* 

### 03-general-service-to-service-communication-security

- [V12.3.1](/taxonomy/asvs-4.0.3/12-secure-communication/03-general-service-to-service-communication-security#V12.3.1) *An encrypted protocol such as tls is used for all  ...* 

- [V12.3.2](/taxonomy/asvs-4.0.3/12-secure-communication/03-general-service-to-service-communication-security#V12.3.2) *Tls clients validate certificates received before  ...* 

- [V12.3.3](/taxonomy/asvs-4.0.3/12-secure-communication/03-general-service-to-service-communication-security#V12.3.3) *Tls or another appropriate transport encryption me ...* 

- [V12.3.4](/taxonomy/asvs-4.0.3/12-secure-communication/03-general-service-to-service-communication-security#V12.3.4) *Tls connections between internal services use trus ...* 

## 13-configuration

### 01-configuration-documentation

- [V13.1.1](/taxonomy/asvs-4.0.3/13-configuration/01-configuration-documentation#V13.1.1) *All communication needs for the application are do ...* 

### 02-backend-communication-configuration

- [V13.2.1](/taxonomy/asvs-4.0.3/13-configuration/02-backend-communication-configuration#V13.2.1) *Communications between backend application compone ...* 

- [V13.2.2](/taxonomy/asvs-4.0.3/13-configuration/02-backend-communication-configuration#V13.2.2) *Communications between backend application compone ...* 

- [V13.2.3](/taxonomy/asvs-4.0.3/13-configuration/02-backend-communication-configuration#V13.2.3) *If a credential has to be used for service authent ...* 

- [V13.2.4](/taxonomy/asvs-4.0.3/13-configuration/02-backend-communication-configuration#V13.2.4) *An allowlist is used to define the external resour ...* 

- [V13.2.5](/taxonomy/asvs-4.0.3/13-configuration/02-backend-communication-configuration#V13.2.5) *The web or application server is configured with a ...* 

### 03-secret-management

- [V13.3.1](/taxonomy/asvs-4.0.3/13-configuration/03-secret-management#V13.3.1) *A secrets management solution, such as a key vault ...* 

- [V13.3.2](/taxonomy/asvs-4.0.3/13-configuration/03-secret-management#V13.3.2) *Access to secret assets adheres to the principle o ...* 

### 04-unintended-information-leakage

- [V13.4.2](/taxonomy/asvs-4.0.3/13-configuration/04-unintended-information-leakage#V13.4.2) *Debug modes are disabled for all components in pro ...* 

- [V13.4.3](/taxonomy/asvs-4.0.3/13-configuration/04-unintended-information-leakage#V13.4.3) *Web servers do not expose directory listings to cl ...* 

- [V13.4.4](/taxonomy/asvs-4.0.3/13-configuration/04-unintended-information-leakage#V13.4.4) *Using the http trace method is not supported in pr ...* 

- [V13.4.5](/taxonomy/asvs-4.0.3/13-configuration/04-unintended-information-leakage#V13.4.5) *Documentation (such as for internal apis) and moni ...* 

## 14-data-protection

### 01-data-protection-documentation

- [V14.1.1](/taxonomy/asvs-4.0.3/14-data-protection/01-data-protection-documentation#V14.1.1) *All sensitive data created and processed by the ap ...* 

- [V14.1.2](/taxonomy/asvs-4.0.3/14-data-protection/01-data-protection-documentation#V14.1.2) *All sensitive data protection levels have a docume ...* 

### 02-general-data-protection

- [V14.2.2](/taxonomy/asvs-4.0.3/14-data-protection/02-general-data-protection#V14.2.2) *The application prevents sensitive data from being ...* 

- [V14.2.3](/taxonomy/asvs-4.0.3/14-data-protection/02-general-data-protection#V14.2.3) *Defined sensitive data is not sent to untrusted pa ...* 

- [V14.2.4](/taxonomy/asvs-4.0.3/14-data-protection/02-general-data-protection#V14.2.4) *Controls around sensitive data related to encrypti ...* 

### 03-client-side-data-protection

- [V14.3.2](/taxonomy/asvs-4.0.3/14-data-protection/03-client-side-data-protection#V14.3.2) *The application sets sufficient anti-caching http  ...* 

- [V14.3.3](/taxonomy/asvs-4.0.3/14-data-protection/03-client-side-data-protection#V14.3.3) *Data stored in browser storage (such as localstora ...* 

## 15-secure-coding-and-architecture

### 01-secure-coding-and-architecture-documentation

- [V15.1.2](/taxonomy/asvs-4.0.3/15-secure-coding-and-architecture/01-secure-coding-and-architecture-documentation#V15.1.2) *An inventory catalog, such as software bill of mat ...* 

- [V15.1.3](/taxonomy/asvs-4.0.3/15-secure-coding-and-architecture/01-secure-coding-and-architecture-documentation#V15.1.3) *The application documentation identifies functiona ...* 

### 02-security-architecture-and-dependencies

- [V15.2.2](/taxonomy/asvs-4.0.3/15-secure-coding-and-architecture/02-security-architecture-and-dependencies#V15.2.2) *The application has implemented defenses against l ...* 

- [V15.2.3](/taxonomy/asvs-4.0.3/15-secure-coding-and-architecture/02-security-architecture-and-dependencies#V15.2.3) *The production environment only includes functiona ...* 

### 03-defensive-coding

- [V15.3.2](/taxonomy/asvs-4.0.3/15-secure-coding-and-architecture/03-defensive-coding#V15.3.2) *Where the application backend makes calls to exter ...* 

- [V15.3.3](/taxonomy/asvs-4.0.3/15-secure-coding-and-architecture/03-defensive-coding#V15.3.3) *The application has countermeasures to protect aga ...* 

- [V15.3.4](/taxonomy/asvs-4.0.3/15-secure-coding-and-architecture/03-defensive-coding#V15.3.4) *All proxying and middleware components transfer th ...* 

- [V15.3.5](/taxonomy/asvs-4.0.3/15-secure-coding-and-architecture/03-defensive-coding#V15.3.5) *The application explicitly ensures that variables  ...* 

- [V15.3.6](/taxonomy/asvs-4.0.3/15-secure-coding-and-architecture/03-defensive-coding#V15.3.6) *Javascript code is written in a way that prevents  ...* 

- [V15.3.7](/taxonomy/asvs-4.0.3/15-secure-coding-and-architecture/03-defensive-coding#V15.3.7) *The application has defenses against http paramete ...* 

## 16-security-logging-and-error-handling

### 01-security-logging-documentation

- [V16.1.1](/taxonomy/asvs-4.0.3/16-security-logging-and-error-handling/01-security-logging-documentation#V16.1.1) *An inventory exists documenting the logging perfor ...* 

### 02-general-logging

- [V16.2.1](/taxonomy/asvs-4.0.3/16-security-logging-and-error-handling/02-general-logging#V16.2.1) *Each log entry includes necessary metadata (such a ...* 

- [V16.2.2](/taxonomy/asvs-4.0.3/16-security-logging-and-error-handling/02-general-logging#V16.2.2) *Time sources for all logging components are synchr ...* 

- [V16.2.3](/taxonomy/asvs-4.0.3/16-security-logging-and-error-handling/02-general-logging#V16.2.3) *The application only stores or broadcasts logs to  ...* 

- [V16.2.4](/taxonomy/asvs-4.0.3/16-security-logging-and-error-handling/02-general-logging#V16.2.4) *Logs can be read and correlated by the log process ...* 

- [V16.2.5](/taxonomy/asvs-4.0.3/16-security-logging-and-error-handling/02-general-logging#V16.2.5) *When logging sensitive data, the application enfor ...* 

### 03-security-events

- [V16.3.1](/taxonomy/asvs-4.0.3/16-security-logging-and-error-handling/03-security-events#V16.3.1) *All authentication operations are logged, includin ...* 

- [V16.3.2](/taxonomy/asvs-4.0.3/16-security-logging-and-error-handling/03-security-events#V16.3.2) *Failed authorization attempts are logged. for l3,  ...* 

- [V16.3.3](/taxonomy/asvs-4.0.3/16-security-logging-and-error-handling/03-security-events#V16.3.3) *The application logs the security events that are  ...* 

- [V16.3.4](/taxonomy/asvs-4.0.3/16-security-logging-and-error-handling/03-security-events#V16.3.4) *The application logs unexpected errors and securit ...* 

### 04-log-protection

- [V16.4.1](/taxonomy/asvs-4.0.3/16-security-logging-and-error-handling/04-log-protection#V16.4.1) *All logging components appropriately encode data t ...* 

- [V16.4.2](/taxonomy/asvs-4.0.3/16-security-logging-and-error-handling/04-log-protection#V16.4.2) *Logs are protected from unauthorized access and ca ...* 

- [V16.4.3](/taxonomy/asvs-4.0.3/16-security-logging-and-error-handling/04-log-protection#V16.4.3) *Logs are securely transmitted to a logically separ ...* 

### 05-error-handling

- [V16.5.1](/taxonomy/asvs-4.0.3/16-security-logging-and-error-handling/05-error-handling#V16.5.1) *A generic message is returned to the consumer when ...* 

- [V16.5.2](/taxonomy/asvs-4.0.3/16-security-logging-and-error-handling/05-error-handling#V16.5.2) *The application continues to operate securely when ...* 

- [V16.5.3](/taxonomy/asvs-4.0.3/16-security-logging-and-error-handling/05-error-handling#V16.5.3) *The application fails gracefully and securely, inc ...* 

## 17-webrtc

### 01-turn-server

- [V17.1.1](/taxonomy/asvs-4.0.3/17-webrtc/01-turn-server#V17.1.1) *The traversal using relays around nat (turn) servi ...* 

### 02-media

- [V17.2.1](/taxonomy/asvs-4.0.3/17-webrtc/02-media#V17.2.1) *The key for the datagram transport layer security  ...* 

- [V17.2.2](/taxonomy/asvs-4.0.3/17-webrtc/02-media#V17.2.2) *The media server is configured to use and support  ...* 

- [V17.2.3](/taxonomy/asvs-4.0.3/17-webrtc/02-media#V17.2.3) *Secure real-time transport protocol (srtp) authent ...* 

- [V17.2.4](/taxonomy/asvs-4.0.3/17-webrtc/02-media#V17.2.4) *The media server is able to continue processing in ...* 

### 03-signaling

- [V17.3.1](/taxonomy/asvs-4.0.3/17-webrtc/03-signaling#V17.3.1) *The signaling server is able to continue processin ...* 

- [V17.3.2](/taxonomy/asvs-4.0.3/17-webrtc/03-signaling#V17.3.2) *The signaling server is able to continue processin ...* 

