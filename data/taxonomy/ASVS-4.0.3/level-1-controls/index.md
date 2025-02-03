# Level 1 controls
Level 1 contains 128 controls listed below: 
## 02-authentication
### 01-password-security
- [V2.1.1](/taxonomy/ASVS-4.0.3/02-authentication/01-password-security#V2.1.1) *User set passwords are at least 12 characters in l ...* 
- [V2.1.2](/taxonomy/ASVS-4.0.3/02-authentication/01-password-security#V2.1.2) *Passwords of at least 64 characters are permitted, ...* 
- [V2.1.3](/taxonomy/ASVS-4.0.3/02-authentication/01-password-security#V2.1.3) *Password truncation is not performed. however, con ...* 
- [V2.1.4](/taxonomy/ASVS-4.0.3/02-authentication/01-password-security#V2.1.4) *Any printable unicode character, including languag ...* 
- [V2.1.5](/taxonomy/ASVS-4.0.3/02-authentication/01-password-security#V2.1.5) *Verify users can change their password. ...* 
- [V2.1.6](/taxonomy/ASVS-4.0.3/02-authentication/01-password-security#V2.1.6) *Password change functionality requires the user's  ...* 
- [V2.1.7](/taxonomy/ASVS-4.0.3/02-authentication/01-password-security#V2.1.7) *Passwords submitted during account registration, l ...* 
- [V2.1.8](/taxonomy/ASVS-4.0.3/02-authentication/01-password-security#V2.1.8) *A password strength meter is provided to help user ...* 
- [V2.1.9](/taxonomy/ASVS-4.0.3/02-authentication/01-password-security#V2.1.9) *There are no password composition rules limiting t ...* 
- [V2.1.10](/taxonomy/ASVS-4.0.3/02-authentication/01-password-security#V2.1.10) *There are no periodic credential rotation or passw ...* 
- [V2.1.11](/taxonomy/ASVS-4.0.3/02-authentication/01-password-security#V2.1.11) *"paste" functionality, browser password helpers, a ...* 
- [V2.1.12](/taxonomy/ASVS-4.0.3/02-authentication/01-password-security#V2.1.12) *The user can choose to either temporarily view the ...* 
### 02-general-authenticator-security
- [V2.2.1](/taxonomy/ASVS-4.0.3/02-authentication/02-general-authenticator-security#V2.2.1) *Anti-automation controls are effective at mitigati ...* 
- [V2.2.2](/taxonomy/ASVS-4.0.3/02-authentication/02-general-authenticator-security#V2.2.2) *The use of weak authenticators (such as sms and em ...* 
- [V2.2.3](/taxonomy/ASVS-4.0.3/02-authentication/02-general-authenticator-security#V2.2.3) *Secure notifications are sent to users after updat ...* 
### 03-authenticator-lifecycle
- [V2.3.1](/taxonomy/ASVS-4.0.3/02-authentication/03-authenticator-lifecycle#V2.3.1) *Verify system generated initial passwords or activ ...* 
### 05-credential-recovery
- [V2.5.1](/taxonomy/ASVS-4.0.3/02-authentication/05-credential-recovery#V2.5.1) *A system generated initial activation or recovery  ...* 
- [V2.5.2](/taxonomy/ASVS-4.0.3/02-authentication/05-credential-recovery#V2.5.2) *Verify password hints or knowledge-based authentic ...* 
- [V2.5.3](/taxonomy/ASVS-4.0.3/02-authentication/05-credential-recovery#V2.5.3) *Verify password credential recovery does not revea ...* 
- [V2.5.4](/taxonomy/ASVS-4.0.3/02-authentication/05-credential-recovery#V2.5.4) *Verify shared or default accounts are not present  ...* 
- [V2.5.5](/taxonomy/ASVS-4.0.3/02-authentication/05-credential-recovery#V2.5.5) *If an authentication factor is changed or replaced ...* 
- [V2.5.6](/taxonomy/ASVS-4.0.3/02-authentication/05-credential-recovery#V2.5.6) *Verify forgotten password, and other recovery path ...* 
### 07-out-of-band-verifier
- [V2.7.1](/taxonomy/ASVS-4.0.3/02-authentication/07-out-of-band-verifier#V2.7.1) *Clear text out of band (nist "restricted") authent ...* 
- [V2.7.2](/taxonomy/ASVS-4.0.3/02-authentication/07-out-of-band-verifier#V2.7.2) *The out of band verifier expires out of band authe ...* 
- [V2.7.3](/taxonomy/ASVS-4.0.3/02-authentication/07-out-of-band-verifier#V2.7.3) *The out of band verifier authentication requests,  ...* 
- [V2.7.4](/taxonomy/ASVS-4.0.3/02-authentication/07-out-of-band-verifier#V2.7.4) *The out of band authenticator and verifier communi ...* 
### 08-one-time-verifier
- [V2.8.1](/taxonomy/ASVS-4.0.3/02-authentication/08-one-time-verifier#V2.8.1) *Time-based otps have a defined lifetime before exp ...* 
## 03-session-management
### 01-fundamental-session-management-security
- [V3.1.1](/taxonomy/ASVS-4.0.3/03-session-management/01-fundamental-session-management-security#V3.1.1) *Verify the application never reveals session token ...* 
### 02-session-binding
- [V3.2.1](/taxonomy/ASVS-4.0.3/03-session-management/02-session-binding#V3.2.1) *Verify the application generates a new session tok ...* 
- [V3.2.2](/taxonomy/ASVS-4.0.3/03-session-management/02-session-binding#V3.2.2) *Session tokens possess at least 64 bits of entropy ...* 
- [V3.2.3](/taxonomy/ASVS-4.0.3/03-session-management/02-session-binding#V3.2.3) *Verify the application only stores session tokens  ...* 
### 03-session-termination
- [V3.3.1](/taxonomy/ASVS-4.0.3/03-session-management/03-session-termination#V3.3.1) *Logout and expiration invalidate the session token ...* 
- [V3.3.2](/taxonomy/ASVS-4.0.3/03-session-management/03-session-termination#V3.3.2) *If authenticators permit users to remain logged in ...* 
### 04-cookie-based-session-management
- [V3.4.1](/taxonomy/ASVS-4.0.3/03-session-management/04-cookie-based-session-management#V3.4.1) *Cookie-based session tokens have the 'secure' attr ...* 
- [V3.4.2](/taxonomy/ASVS-4.0.3/03-session-management/04-cookie-based-session-management#V3.4.2) *Cookie-based session tokens have the 'httponly' at ...* 
- [V3.4.3](/taxonomy/ASVS-4.0.3/03-session-management/04-cookie-based-session-management#V3.4.3) *Cookie-based session tokens utilize the 'samesite' ...* 
- [V3.4.4](/taxonomy/ASVS-4.0.3/03-session-management/04-cookie-based-session-management#V3.4.4) *Cookie-based session tokens use the "__host-" pref ...* 
- [V3.4.5](/taxonomy/ASVS-4.0.3/03-session-management/04-cookie-based-session-management#V3.4.5) *If the application is published under a domain nam ...* 
### 07-defenses-against-session-management-exploits
- [V3.7.1](/taxonomy/ASVS-4.0.3/03-session-management/07-defenses-against-session-management-exploits#V3.7.1) *Verify the application ensures a full, valid login ...* 
## 04-access-control
### 01-general-access-control-design
- [V4.1.1](/taxonomy/ASVS-4.0.3/04-access-control/01-general-access-control-design#V4.1.1) *The application enforces access control rules on a ...* 
- [V4.1.2](/taxonomy/ASVS-4.0.3/04-access-control/01-general-access-control-design#V4.1.2) *All user and data attributes and policy informatio ...* 
- [V4.1.3](/taxonomy/ASVS-4.0.3/04-access-control/01-general-access-control-design#V4.1.3) *The principle of least privilege exists - users sh ...* 
- [V4.1.5](/taxonomy/ASVS-4.0.3/04-access-control/01-general-access-control-design#V4.1.5) *Access controls fail securely including when an ex ...* 
### 02-operation-level-access-control
- [V4.2.1](/taxonomy/ASVS-4.0.3/04-access-control/02-operation-level-access-control#V4.2.1) *Sensitive data and apis are protected against inse ...* 
- [V4.2.2](/taxonomy/ASVS-4.0.3/04-access-control/02-operation-level-access-control#V4.2.2) *The application or framework enforces a strong ant ...* 
### 03-other-access-control-considerations
- [V4.3.1](/taxonomy/ASVS-4.0.3/04-access-control/03-other-access-control-considerations#V4.3.1) *Verify administrative interfaces use appropriate m ...* 
- [V4.3.2](/taxonomy/ASVS-4.0.3/04-access-control/03-other-access-control-considerations#V4.3.2) *Directory browsing is disabled unless deliberately ...* 
## 05-validation-sanitization-and-encoding
### 01-input-validation
- [V5.1.1](/taxonomy/ASVS-4.0.3/05-validation-sanitization-and-encoding/01-input-validation#V5.1.1) *The application has defenses against http paramete ...* 
- [V5.1.2](/taxonomy/ASVS-4.0.3/05-validation-sanitization-and-encoding/01-input-validation#V5.1.2) *Frameworks protect against mass parameter assignme ...* 
- [V5.1.3](/taxonomy/ASVS-4.0.3/05-validation-sanitization-and-encoding/01-input-validation#V5.1.3) *All input (html form fields, rest requests, url pa ...* 
- [V5.1.4](/taxonomy/ASVS-4.0.3/05-validation-sanitization-and-encoding/01-input-validation#V5.1.4) *Structured data is strongly typed and validated ag ...* 
- [V5.1.5](/taxonomy/ASVS-4.0.3/05-validation-sanitization-and-encoding/01-input-validation#V5.1.5) *Url redirects and forwards only allow destinations ...* 
### 02-sanitization-and-sandboxing
- [V5.2.1](/taxonomy/ASVS-4.0.3/05-validation-sanitization-and-encoding/02-sanitization-and-sandboxing#V5.2.1) *All untrusted html input from wysiwyg editors or s ...* 
- [V5.2.2](/taxonomy/ASVS-4.0.3/05-validation-sanitization-and-encoding/02-sanitization-and-sandboxing#V5.2.2) *Unstructured data is sanitized to enforce safety m ...* 
- [V5.2.3](/taxonomy/ASVS-4.0.3/05-validation-sanitization-and-encoding/02-sanitization-and-sandboxing#V5.2.3) *The application sanitizes user input before passin ...* 
- [V5.2.4](/taxonomy/ASVS-4.0.3/05-validation-sanitization-and-encoding/02-sanitization-and-sandboxing#V5.2.4) *The application avoids the use of eval() or other  ...* 
- [V5.2.5](/taxonomy/ASVS-4.0.3/05-validation-sanitization-and-encoding/02-sanitization-and-sandboxing#V5.2.5) *The application protects against template injectio ...* 
- [V5.2.6](/taxonomy/ASVS-4.0.3/05-validation-sanitization-and-encoding/02-sanitization-and-sandboxing#V5.2.6) *The application protects against ssrf attacks, by  ...* 
- [V5.2.7](/taxonomy/ASVS-4.0.3/05-validation-sanitization-and-encoding/02-sanitization-and-sandboxing#V5.2.7) *The application sanitizes, disables, or sandboxes  ...* 
- [V5.2.8](/taxonomy/ASVS-4.0.3/05-validation-sanitization-and-encoding/02-sanitization-and-sandboxing#V5.2.8) *The application sanitizes, disables, or sandboxes  ...* 
### 03-output-encoding-and-injection-prevention
- [V5.3.1](/taxonomy/ASVS-4.0.3/05-validation-sanitization-and-encoding/03-output-encoding-and-injection-prevention#V5.3.1) *Output encoding is relevant for the interpreter an ...* 
- [V5.3.2](/taxonomy/ASVS-4.0.3/05-validation-sanitization-and-encoding/03-output-encoding-and-injection-prevention#V5.3.2) *Output encoding preserves the user's chosen charac ...* 
- [V5.3.3](/taxonomy/ASVS-4.0.3/05-validation-sanitization-and-encoding/03-output-encoding-and-injection-prevention#V5.3.3) *Context-aware, preferably automated - or at worst, ...* 
- [V5.3.4](/taxonomy/ASVS-4.0.3/05-validation-sanitization-and-encoding/03-output-encoding-and-injection-prevention#V5.3.4) *Data selection or database queries (e.g. sql, hql, ...* 
- [V5.3.5](/taxonomy/ASVS-4.0.3/05-validation-sanitization-and-encoding/03-output-encoding-and-injection-prevention#V5.3.5) *Where parameterized or safer mechanisms are not pr ...* 
- [V5.3.6](/taxonomy/ASVS-4.0.3/05-validation-sanitization-and-encoding/03-output-encoding-and-injection-prevention#V5.3.6) *The application protects against json injection at ...* 
- [V5.3.7](/taxonomy/ASVS-4.0.3/05-validation-sanitization-and-encoding/03-output-encoding-and-injection-prevention#V5.3.7) *The application protects against ldap injection vu ...* 
- [V5.3.8](/taxonomy/ASVS-4.0.3/05-validation-sanitization-and-encoding/03-output-encoding-and-injection-prevention#V5.3.8) *The application protects against os command inject ...* 
- [V5.3.9](/taxonomy/ASVS-4.0.3/05-validation-sanitization-and-encoding/03-output-encoding-and-injection-prevention#V5.3.9) *The application protects against local file inclus ...* 
- [V5.3.10](/taxonomy/ASVS-4.0.3/05-validation-sanitization-and-encoding/03-output-encoding-and-injection-prevention#V5.3.10) *The application protects against xpath injection o ...* 
### 05-deserialization-prevention
- [V5.5.1](/taxonomy/ASVS-4.0.3/05-validation-sanitization-and-encoding/05-deserialization-prevention#V5.5.1) *Serialized objects use integrity checks or are enc ...* 
- [V5.5.2](/taxonomy/ASVS-4.0.3/05-validation-sanitization-and-encoding/05-deserialization-prevention#V5.5.2) *The application correctly restricts xml parsers to ...* 
- [V5.5.3](/taxonomy/ASVS-4.0.3/05-validation-sanitization-and-encoding/05-deserialization-prevention#V5.5.3) *Deserialization of untrusted data is avoided or is ...* 
- [V5.5.4](/taxonomy/ASVS-4.0.3/05-validation-sanitization-and-encoding/05-deserialization-prevention#V5.5.4) *When parsing json in browsers or javascript-based  ...* 
## 06-stored-cryptography
### 02-algorithms
- [V6.2.1](/taxonomy/ASVS-4.0.3/06-stored-cryptography/02-algorithms#V6.2.1) *All cryptographic modules fail securely, and error ...* 
## 07-error-handling-and-logging
### 01-log-content
- [V7.1.1](/taxonomy/ASVS-4.0.3/07-error-handling-and-logging/01-log-content#V7.1.1) *The application does not log credentials or paymen ...* 
- [V7.1.2](/taxonomy/ASVS-4.0.3/07-error-handling-and-logging/01-log-content#V7.1.2) *The application does not log other sensitive data  ...* 
### 04-error-handling
- [V7.4.1](/taxonomy/ASVS-4.0.3/07-error-handling-and-logging/04-error-handling#V7.4.1) *A generic message is shown when an unexpected or s ...* 
## 08-data-protection
### 02-client-side-data-protection
- [V8.2.1](/taxonomy/ASVS-4.0.3/08-data-protection/02-client-side-data-protection#V8.2.1) *Verify the application sets sufficient anti-cachin ...* 
- [V8.2.2](/taxonomy/ASVS-4.0.3/08-data-protection/02-client-side-data-protection#V8.2.2) *Data stored in browser storage (such as localstora ...* 
- [V8.2.3](/taxonomy/ASVS-4.0.3/08-data-protection/02-client-side-data-protection#V8.2.3) *Authenticated data is cleared from client storage, ...* 
### 03-sensitive-private-data
- [V8.3.1](/taxonomy/ASVS-4.0.3/08-data-protection/03-sensitive-private-data#V8.3.1) *Sensitive data is sent to the server in the http m ...* 
- [V8.3.2](/taxonomy/ASVS-4.0.3/08-data-protection/03-sensitive-private-data#V8.3.2) *Users have a method to remove or export their data ...* 
- [V8.3.3](/taxonomy/ASVS-4.0.3/08-data-protection/03-sensitive-private-data#V8.3.3) *Users are provided clear language regarding collec ...* 
- [V8.3.4](/taxonomy/ASVS-4.0.3/08-data-protection/03-sensitive-private-data#V8.3.4) *All sensitive data created and processed by the ap ...* 
## 09-communication
### 01-client-communication-security
- [V9.1.1](/taxonomy/ASVS-4.0.3/09-communication/01-client-communication-security#V9.1.1) *Tls is used for all client connectivity, and does  ...* 
- [V9.1.2](/taxonomy/ASVS-4.0.3/09-communication/01-client-communication-security#V9.1.2) *Verify using up to date tls testing tools that onl ...* 
- [V9.1.3](/taxonomy/ASVS-4.0.3/09-communication/01-client-communication-security#V9.1.3) *Only the latest recommended versions of the tls pr ...* 
## 10-malicious-code
### 03-application-integrity
- [V10.3.1](/taxonomy/ASVS-4.0.3/10-malicious-code/03-application-integrity#V10.3.1) *If the application has a client or server auto-upd ...* 
- [V10.3.2](/taxonomy/ASVS-4.0.3/10-malicious-code/03-application-integrity#V10.3.2) *The application employs integrity protections, suc ...* 
- [V10.3.3](/taxonomy/ASVS-4.0.3/10-malicious-code/03-application-integrity#V10.3.3) *The application has protection from subdomain take ...* 
## 11-business-logic
### 01-business-logic-security
- [V11.1.1](/taxonomy/ASVS-4.0.3/11-business-logic/01-business-logic-security#V11.1.1) *The application will only process business logic f ...* 
- [V11.1.2](/taxonomy/ASVS-4.0.3/11-business-logic/01-business-logic-security#V11.1.2) *The application will only process business logic f ...* 
- [V11.1.3](/taxonomy/ASVS-4.0.3/11-business-logic/01-business-logic-security#V11.1.3) *Verify the application has appropriate limits for  ...* 
- [V11.1.4](/taxonomy/ASVS-4.0.3/11-business-logic/01-business-logic-security#V11.1.4) *The application has anti-automation controls to pr ...* 
- [V11.1.5](/taxonomy/ASVS-4.0.3/11-business-logic/01-business-logic-security#V11.1.5) *Verify the application has business logic limits o ...* 
## 12-files-and-resources
### 01-file-upload
- [V12.1.1](/taxonomy/ASVS-4.0.3/12-files-and-resources/01-file-upload#V12.1.1) *The application will not accept large files that c ...* 
### 03-file-execution
- [V12.3.1](/taxonomy/ASVS-4.0.3/12-files-and-resources/03-file-execution#V12.3.1) *User-submitted filename metadata is not used direc ...* 
- [V12.3.2](/taxonomy/ASVS-4.0.3/12-files-and-resources/03-file-execution#V12.3.2) *User-submitted filename metadata is validated or i ...* 
- [V12.3.3](/taxonomy/ASVS-4.0.3/12-files-and-resources/03-file-execution#V12.3.3) *User-submitted filename metadata is validated or i ...* 
- [V12.3.4](/taxonomy/ASVS-4.0.3/12-files-and-resources/03-file-execution#V12.3.4) *The application protects against reflective file d ...* 
- [V12.3.5](/taxonomy/ASVS-4.0.3/12-files-and-resources/03-file-execution#V12.3.5) *Untrusted file metadata is not used directly with  ...* 
### 04-file-storage
- [V12.4.1](/taxonomy/ASVS-4.0.3/12-files-and-resources/04-file-storage#V12.4.1) *Files obtained from untrusted sources are stored o ...* 
- [V12.4.2](/taxonomy/ASVS-4.0.3/12-files-and-resources/04-file-storage#V12.4.2) *Files obtained from untrusted sources are scanned  ...* 
### 05-file-download
- [V12.5.1](/taxonomy/ASVS-4.0.3/12-files-and-resources/05-file-download#V12.5.1) *The web tier is configured to serve only files wit ...* 
- [V12.5.2](/taxonomy/ASVS-4.0.3/12-files-and-resources/05-file-download#V12.5.2) *Direct requests to uploaded files will never be ex ...* 
### 06-ssrf-protection
- [V12.6.1](/taxonomy/ASVS-4.0.3/12-files-and-resources/06-ssrf-protection#V12.6.1) *The web or application server is configured with a ...* 
## 13-api-and-web-service
### 01-generic-web-service-security
- [V13.1.1](/taxonomy/ASVS-4.0.3/13-api-and-web-service/01-generic-web-service-security#V13.1.1) *All application components use the same encodings  ...* 
- [V13.1.3](/taxonomy/ASVS-4.0.3/13-api-and-web-service/01-generic-web-service-security#V13.1.3) *Verify api urls do not expose sensitive informatio ...* 
### 02-restful-web-service
- [V13.2.1](/taxonomy/ASVS-4.0.3/13-api-and-web-service/02-restful-web-service#V13.2.1) *Enabled restful http methods are a valid choice fo ...* 
- [V13.2.2](/taxonomy/ASVS-4.0.3/13-api-and-web-service/02-restful-web-service#V13.2.2) *Json schema validation is in place and verified be ...* 
- [V13.2.3](/taxonomy/ASVS-4.0.3/13-api-and-web-service/02-restful-web-service#V13.2.3) *Restful web services that utilize cookies are prot ...* 
### 03-soap-web-service
- [V13.3.1](/taxonomy/ASVS-4.0.3/13-api-and-web-service/03-soap-web-service#V13.3.1) *Xsd schema validation takes place to ensure a prop ...* 
## 14-configuration
### 02-dependency
- [V14.2.1](/taxonomy/ASVS-4.0.3/14-configuration/02-dependency#V14.2.1) *All components are up to date, preferably using a  ...* 
- [V14.2.2](/taxonomy/ASVS-4.0.3/14-configuration/02-dependency#V14.2.2) *All unneeded features, documentation, sample appli ...* 
- [V14.2.3](/taxonomy/ASVS-4.0.3/14-configuration/02-dependency#V14.2.3) *If application assets, such as javascript librarie ...* 
### 03-unintended-security-disclosure
- [V14.3.2](/taxonomy/ASVS-4.0.3/14-configuration/03-unintended-security-disclosure#V14.3.2) *Web or application server and application framewor ...* 
- [V14.3.3](/taxonomy/ASVS-4.0.3/14-configuration/03-unintended-security-disclosure#V14.3.3) *The http headers or any part of the http response  ...* 
### 04-http-security-headers
- [V14.4.1](/taxonomy/ASVS-4.0.3/14-configuration/04-http-security-headers#V14.4.1) *Every http response contains a content-type header ...* 
- [V14.4.2](/taxonomy/ASVS-4.0.3/14-configuration/04-http-security-headers#V14.4.2) *All api responses contain a content-disposition: a ...* 
- [V14.4.3](/taxonomy/ASVS-4.0.3/14-configuration/04-http-security-headers#V14.4.3) *A content security policy (csp) response header is ...* 
- [V14.4.4](/taxonomy/ASVS-4.0.3/14-configuration/04-http-security-headers#V14.4.4) *All responses contain a x-content-type-options: no ...* 
- [V14.4.5](/taxonomy/ASVS-4.0.3/14-configuration/04-http-security-headers#V14.4.5) *A strict-transport-security header is included on  ...* 
- [V14.4.6](/taxonomy/ASVS-4.0.3/14-configuration/04-http-security-headers#V14.4.6) *A suitable referrer-policy header is included to a ...* 
- [V14.4.7](/taxonomy/ASVS-4.0.3/14-configuration/04-http-security-headers#V14.4.7) *The content of a web application cannot be embedde ...* 
### 05-http-request-header-validation
- [V14.5.1](/taxonomy/ASVS-4.0.3/14-configuration/05-http-request-header-validation#V14.5.1) *The application server only accepts the http metho ...* 
- [V14.5.2](/taxonomy/ASVS-4.0.3/14-configuration/05-http-request-header-validation#V14.5.2) *The supplied origin header is not used for authent ...* 
- [V14.5.3](/taxonomy/ASVS-4.0.3/14-configuration/05-http-request-header-validation#V14.5.3) *The cross-origin resource sharing (cors) access-co ...* 
