# DEPRECATED: ASVS 4.0 Index

## Table of Contents

- [Objective](#objective)
- [V1: Architecture, Design and Threat Modeling Requirements](#V1-Architecture-Design-and-Threat-Modeling-Requirements)
    - [V1.1 Secure Software Development Lifecycle Requirements](#V1.1-Secure-Software-Development-Lifecycle-Requirements)
    - [V1.2 Authentication Architecture Requirements](#V1.2-Authentication-Architecture-Requirements)
    - [V1.3 Session Management Architecture Requirements](#V1.3-Session-Management-Architecture-Requirements)
    - [V1.4 Access Control Architecture Requirements](#V1.4-Access-Control-Architecture-Requirements)
    - [V1.5 Input and Output Architecture Requirements](#V1.5-Input-and-Output-Architecture-Requirements)
    - [V1.6 Cryptographic Architecture Requirements](#V1.6-Cryptographic-Architecture-Requirements)
    - [V1.7 Errors, Logging and Auditing Architecture Requirements](#V1.7-Errors-Logging-and-Auditing-Architecture-Requirements)
    - [V1.8 Data Protection and Privacy Architecture Requirements](#V1.8-Data-Protection-and-Privacy-Architecture-Requirements)
    - [V1.9 Communications Architecture Requirements](#V1.9-Communications-Architecture-Requirements)
    - [V1.10 Malicious Software Architecture Requirements](#V1.10-Malicious-Software-Architecture-Requirements)
    - [V1.11 Business Logic Architecture Requirements](#V1.11-Business-Logic-Architecture-Requirements)
    - [V1.12 Secure File Upload Architecture Requirements](#V1.12-Secure-File-Upload-Architecture-Requirements)
    - [V1.13 API Architecture Requirements](#V1.13-API-Architecture-Requirements)
    - [V1.14 Configuration Architecture Requirements](#V1.14-Configuration-Architecture-Requirements)
- [V2: Authentication Verification Requirements](#V2-Authentication-Verification-Requirements)
    - [V2.1 Password Security Requirements](#V2.1-Password-Security-Requirements)
    - [V2.2 General Authenticator Requirements](#V2.2-General-Authenticator-Requirements)
    - [V2.3 Authenticator Lifecycle Requirements](#V2.3-Authenticator-Lifecycle-Requirements)
    - [V2.4 Credential Storage Requirements](#V2.4-Credential-Storage-Requirements)
    - [V2.5 Credential Recovery Requirements](#V2.5-Credential-Recovery-Requirements)
    - [V2.6 Look-up Secret Verifier Requirements](#V2.6-Look-up-Secret-Verifier-Requirements)
    - [V2.7 Out of Band Verifier Requirements](#V2.7-Out-of-Band-Verifier-Requirements)
    - [V2.8 Single or Multi Factor One Time Verifier Requirements](#V2.8-Single-or-Multi-Factor-One-Time-Verifier-Requirements)
    - [V2.9 Cryptographic Software and Devices Verifier Requirements](#V2.9-Cryptographic-Software-and-Devices-Verifier-Requirements)
    - [V2.10 Service Authentication Requirements](#V2.10-Service-Authentication-Requirements)
- [V3: Session Management Verification Requirements](#V3-Session-Management-Verification-Requirements)
    - [V3.1 Fundamental Session Management Requirements](#V3.1-Fundamental-Session-Management-Requirements)
    - [V3.2 Session Binding Requirements](#V3.2-Session-Binding-Requirements)
    - [V3.3 Session Logout and Timeout Requirements](#V3.3-Session-Logout-and-Timeout-Requirements)
    - [V3.4 Cookie-based Session Management](#V3.4-Cookie-based-Session-Management)
    - [V3.5 Token-based Session Management](#V3.5-Token-based-Session-Management)
    - [V3.6 Re-authentication from a Federation or Assertion](#V3.6-Re-authentication-from-a-Federation-or-Assertion)
    - [V3.7 Defenses Against Session Management Exploits](#V3.7-Defenses-Against-Session-Management-Exploits)
- [V4: Access Control Verification Requirements](#V4-Access-Control-Verification-Requirements)
    - [V4.1 General Access Control Design](#V4.1-General-Access-Control-Design)
    - [V4.2 Operation Level Access Control](#V4.2-Operation-Level-Access-Control)
    - [V4.3 Other Access Control Considerations](#V4.3-Other-Access-Control-Considerations)
- [V5: Validation, Sanitization and Encoding Verification Requirements](#V5-Validation-Sanitization-and-Encoding-Verification-Requirements)
    - [V5.1 Input Validation Requirements](#V5.1-Input-Validation-Requirements)
    - [V5.2 Sanitization and Sandboxing Requirements](#V5.2-Sanitization-and-Sandboxing-Requirements)
    - [V5.3 Output encoding and Injection Prevention Requirements](#V5.3-Output-encoding-and-Injection-Prevention-Requirements)
    - [V5.4 Memory, String, and Unmanaged Code Requirements](#V5.4-Memory-String-and-Unmanaged-Code-Requirements)
    - [V5.5 Deserialization Prevention Requirements](#V5.5-Deserialization-Prevention-Requirements)
- [V6: Stored Cryptography Verification Requirements](#V6-Stored-Cryptography-Verification-Requirements)
    - [V6.1 Data Classification](#V6.1-Data-Classification)
    - [V6.2 Algorithms](#V6.2-Algorithms)
    - [V6.3 Random Values](#V6.3-Random-Values)
    - [V6.4 Secret Management](#V6.4-Secret-Management)
- [V7: Error Handling and Logging Verification Requirements](#V7-Error-Handling-and-Logging-Verification-Requirements)
    - [V7.1 Log Content Requirements](#V7.1-Log-Content-Requirements)
    - [V7.2 Log Processing Requirements](#V7.2-Log-Processing-Requirements)
    - [V7.3 Log Protection Requirements](#V7.3-Log-Protection-Requirements)
    - [V7.4 Error Handling](#V7.4-Error-Handling)
- [V8: Data Protection Verification Requirements](#V8-Data-Protection-Verification-Requirements)
    - [V8.1 General Data Protection](#V8.1-General-Data-Protection)
    - [V8.2 Client-side Data Protection](#V8.2-Client-side-Data-Protection)
    - [V8.3 Sensitive Private Data](#V8.3-Sensitive-Private-Data)
- [V9: Communications Verification Requirements](#V9-Communications-Verification-Requirements)
    - [V9.1 Communications Security Requirements](#V9.1-Communications-Security-Requirements)
    - [V9.2 Server Communications Security Requirements](#V9.2-Server-Communications-Security-Requirements)
- [V10: Malicious Code Verification Requirements](#V10-Malicious-Code-Verification-Requirements)
    - [V10.1 Code Integrity Controls](#V10.1-Code-Integrity-Controls)
    - [V10.2 Malicious Code Search](#V10.2-Malicious-Code-Search)
    - [V10.3 Deployed Application Integrity Controls](#V10.3-Deployed-Application-Integrity-Controls)
- [V11: Business Logic Verification Requirements](#V11-Business-Logic-Verification-Requirements)
    - [V11.1 Business Logic Security Requirements](#V11.1-Business-Logic-Security-Requirements)
- [V12: File and Resources Verification Requirements](#V12-File-and-Resources-Verification-Requirements)
    - [V12.1 File Upload Requirements](#V12.1-File-Upload-Requirements)
    - [V12.2 File Integrity Requirements](#V12.2-File-Integrity-Requirements)
    - [V12.3 File execution Requirements](#V12.3-File-execution-Requirements)
    - [V12.4 File Storage Requirements](#V12.4-File-Storage-Requirements)
    - [V12.5 File Download Requirements](#V12.5-File-Download-Requirements)
    - [V12.6 SSRF Protection Requirements](#V12.6-SSRF-Protection-Requirements)
- [V13: API and Web Service Verification Requirements](#V13-API-and-Web-Service-Verification-Requirements)
    - [V13.1 Generic Web Service Security Verification Requirements](#V13.1-Generic-Web-Service-Security-Verification-Requirements)
    - [V13.2 RESTful Web Service Verification Requirements](#V13.2-RESTful-Web-Service-Verification-Requirements)
    - [V13.3 SOAP Web Service Verification Requirements](#V13.3-SOAP-Web-Service-Verification-Requirements)
    - [V13.4 GraphQL and other Web Service Data Layer Security Requirements](#V13.4-GraphQL-and-other-Web-Service-Data-Layer-Security-Requirements)
- [V14: Configuration Verification Requirements](#V14-Configuration-Verification-Requirements)
    - [V14.1 Build](#V14.1-Build-and-Deploy-Requirements)
    - [V14.2 Dependency](#V14.2-Dependency-Requirements)
    - [V14.3 Unintended Security Disclosure Requirements](#V14.3-Unintended-Security-Disclosure-Requirements)
    - [V14.4 HTTP Security Headers Requirements](#V14.4-HTTP-Security-Headers-Requirements)
    - [V14.5 Validate HTTP Request Header Requirements](#V14.5-Validate-HTTP-Request-Header-Requirements)

## Objective

The objective of this index is to help an OWASP [Application Security Verification Standard](https://owasp.org/www-project-application-security-verification-standard/) (ASVS) user clearly identify which cheat sheets are useful for each section during his or her usage of the ASVS.

This index is based on the version 4.0.x of the ASVS.

## V1: Architecture, Design and Threat Modeling Requirements

### V1.1 Secure Software Development Lifecycle Requirements

[Threat Modeling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet)

[Abuse Case Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Abuse_Case_Cheat_Sheet)

[Attack Surface Analysis Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Attack_Surface_Analysis_Cheat_Sheet)

### V1.2 Authentication Architecture Requirements

None.

### V1.3 Session Management Architecture Requirements

None.

### V1.4 Access Control Architecture Requirements

[Docker Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet)

### V1.5 Input and Output Architecture Requirements

[Abuse Case Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Abuse_Case_Cheat_Sheet)

[Deserialization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet)

### V1.6 Cryptographic Architecture Requirements

[Cryptographic Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet)

[Key Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Key_Management_Cheat_Sheet)

### V1.7 Errors, Logging and Auditing Architecture Requirements

[Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet)

### V1.8 Data Protection and Privacy Architecture Requirements

[Abuse Case Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Abuse_Case_Cheat_Sheet)

[User Privacy Protection Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/User_Privacy_Protection_Cheat_Sheet)

### V1.9 Communications Architecture Requirements

[Transport Layer Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet)

### V1.10 Malicious Software Architecture Requirements

[Third Party Javascript Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Third_Party_Javascript_Management_Cheat_Sheet)

[Virtual Patching Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Virtual_Patching_Cheat_Sheet)

### V1.11 Business Logic Architecture Requirements

[Abuse Case Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Abuse_Case_Cheat_Sheet)

### V1.12 Secure File Upload Architecture Requirements

None.

### V1.13 API Architecture Requirements

[REST Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet)

### V1.14 Configuration Architecture Requirements

None.

## V2: Authentication Verification Requirements

### V2.1 Password Security Requirements

[Choosing and Using Security Questions Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Choosing_and_Using_Security_Questions_Cheat_Sheet)

[Forgot Password Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet)

[Credential Stuffing Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Credential_Stuffing_Prevention_Cheat_Sheet)

### V2.2 General Authenticator Requirements

[Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet)

[Transport Layer Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet)

### V2.3 Authenticator Lifecycle Requirements

None.

### V2.4 Credential Storage Requirements

[Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet)

### V2.5 Credential Recovery Requirements

[Choosing and Using Security Questions Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Choosing_and_Using_Security_Questions_Cheat_Sheet)

[Forgot Password Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet)

### V2.6 Look-up Secret Verifier Requirements

None.

### V2.7 Out of Band Verifier Requirements

[Forgot Password Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet)

### V2.8 Single or Multi Factor One Time Verifier Requirements

None.

### V2.9 Cryptographic Software and Devices Verifier Requirements

[Cryptographic Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet)

[Key Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Key_Management_Cheat_Sheet)

### V2.10 Service Authentication Requirements

None.

## V3: Session Management Verification Requirements

### V3.1 Fundamental Session Management Requirements

None.

### V3.2 Session Binding Requirements

[Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet)

[Transport Layer Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet)

### V3.3 Session Logout and Timeout Requirements

[Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet)

### V3.4 Cookie-based Session Management

[Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet)

[Cross-Site Request Forgery Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet)

### V3.5 Token-based Session Management

[JSON Web Token Cheat Sheet for Java](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet)

[REST Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet)

### V3.6 Re-authentication from a Federation or Assertion

None.

### V3.7 Defenses Against Session Management Exploits

[Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet)

[Transaction Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Transaction_Authorization_Cheat_Sheet)

## V4: Access Control Verification Requirements

### V4.1 General Access Control Design

[Access Control Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Access_Control_Cheat_Sheet)

[Authorization Testing Automation](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Testing_Automation_Cheat_Sheet)

### V4.2 Operation Level Access Control

[Insecure Direct Object Reference Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet)

[Cross-Site Request Forgery Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet)

[Authorization Testing Automation](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Testing_Automation_Cheat_Sheet)

### V4.3 Other Access Control Considerations

[REST Assessment Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Assessment_Cheat_Sheet)
[Multifactor Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet)

## V5: Validation, Sanitization and Encoding Verification Requirements

### V5.1 Input Validation Requirements

[Mass Assignment Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet)

[Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet)

### V5.2 Sanitization and Sandboxing Requirements

[Server Side Request Forgery Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet)

[XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet)

[DOM based XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet)

[Unvalidated Redirects and Forwards Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet)

### V5.3 Output encoding and Injection Prevention Requirements

[XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet)

[DOM based XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet)

[HTML5 Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet)

[Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_Cheat_Sheet)

[Injection Prevention Cheat Sheet in Java](https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_in_Java_Cheat_Sheet)

[Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet)

[LDAP Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LDAP_Injection_Prevention_Cheat_Sheet)

[OS Command Injection Defense Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet)

[Protect File Upload Against Malicious File](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet)

[Query Parameterization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Query_Parameterization_Cheat_Sheet)

[SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet)

[Unvalidated Redirects and Forwards Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet)

[Bean Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Bean_Validation_Cheat_Sheet)

[XXE Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet)

[XML Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/XML_Security_Cheat_Sheet)

### V5.4 Memory, String, and Unmanaged Code Requirements

None.

### V5.5 Deserialization Prevention Requirements

[Deserialization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet)

[XXE Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet)

[XML Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/XML_Security_Cheat_Sheet)

## V6: Stored Cryptography Verification Requirements

### V6.1 Data Classification

[Abuse Case Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Abuse_Case_Cheat_Sheet)

[User Privacy Protection Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/User_Privacy_Protection_Cheat_Sheet)

### V6.2 Algorithms

[Cryptographic Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet)

[Key Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Key_Management_Cheat_Sheet)

### V6.3 Random Values

None.

### V6.4 Secret Management

[Key Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Key_Management_Cheat_Sheet)

## V7: Error Handling and Logging Verification Requirements

### V7.1 Log Content Requirements

[Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet)

### V7.2 Log Processing Requirements

[Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet)

### V7.3 Log Protection Requirements

[Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet)

### V7.4 Error Handling

[Error Handling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet)

## V8: Data Protection Verification Requirements

### V8.1 General Data Protection

None.

### V8.2 Client-side Data Protection

None.

### V8.3 Sensitive Private Data

None.

## V9: Communications Verification Requirements

### V9.1 Communications Security Requirements

[HTTP Strict Transport Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Strict_Transport_Security_Cheat_Sheet)

[Transport Layer Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet)

### V9.2 Server Communications Security Requirements

[Transport Layer Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet)

## V10: Malicious Code Verification Requirements

### V10.1 Code Integrity Controls

[Third Party Javascript Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Third_Party_Javascript_Management_Cheat_Sheet)

### V10.2 Malicious Code Search

None.

### V10.3 Deployed Application Integrity Controls

[Docker Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet)

## V11: Business Logic Verification Requirements

### V11.1 Business Logic Security Requirements

[Abuse Case Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Abuse_Case_Cheat_Sheet)

## V12: File and Resources Verification Requirements

### V12.1 File Upload Requirements

[Protect File Upload Against Malicious File](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet)

### V12.2 File Integrity Requirements

[Protect File Upload Against Malicious File](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet)

[Third Party Javascript Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Third_Party_Javascript_Management_Cheat_Sheet)

### V12.3 File execution Requirements

None.

### V12.4 File Storage Requirements

None.

### V12.5 File Download Requirements

None.

### V12.6 SSRF Protection Requirements

[Server Side Request Forgery Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet)

[Unvalidated Redirects and Forwards Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet)

## V13: API and Web Service Verification Requirements

### V13.1 Generic Web Service Security Verification Requirements

[Web Service Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Web_Service_Security_Cheat_Sheet)

[Server Side Request Forgery Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet)

### V13.2 RESTful Web Service Verification Requirements

[REST Assessment Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Assessment_Cheat_Sheet)

[REST Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet)

[Cross-Site Request Forgery Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet)

[Transport Layer Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet)

### V13.3 SOAP Web Service Verification Requirements

[XML Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/XML_Security_Cheat_Sheet)

### V13.4 GraphQL and other Web Service Data Layer Security Requirements

None.

## V14: Configuration Verification Requirements

### V14.1 Build and Deploy Requirements

[Docker Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet)

### V14.2 Dependency Requirements

[Docker Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet)

[Vulnerable Dependency Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Vulnerable_Dependency_Management_Cheat_Sheet)

### V14.3 Unintended Security Disclosure Requirements

[Error Handling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet)

### V14.4 HTTP Security Headers Requirements

[Content Security Policy Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet)

### V14.5 Validate HTTP Request Header Requirements

None.
