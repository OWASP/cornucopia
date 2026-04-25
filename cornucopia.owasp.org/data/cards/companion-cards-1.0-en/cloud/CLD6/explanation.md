## Scenario: Monica's Exploitation of a Poorly Protected Cloud API

Monica exploits a cloud management or backend API that lacks adequate authentication, authorization, and input validation, allowing her to enumerate cloud resources and manipulate backend services. This occurs because:

1. **Weak or Missing API Authentication:** The cloud API accepts requests without requiring valid credentials, or uses authentication tokens that are not properly validated.

2. **Missing Object-Level Authorisation:** API endpoints return resource details or accept commands for any resource identifier supplied, without verifying that the caller is authorised to access that specific resource.

3. **Unrestricted Resource Enumeration:** Error messages or API behaviour differ enough between existing and non-existing resources that Monica can systematically map out the cloud environment.

### Example

Monica is assessing a SaaS platform that exposes a cloud management API for provisioning tenant resources. She notices that the API returns detailed error messages distinguishing between "resource not found" and "access denied." Using a script to iterate over predictable resource identifiers, she maps out the tenant isolation boundaries. She then discovers that a status endpoint does not validate the `tenant_id` parameter. It queries the underlying cloud provider API directly using whatever value is supplied. By substituting other tenants' identifiers, Monica reads configuration data and billing information belonging to other customers, then uses the same endpoint to trigger resource deletion on a test account to confirm write access.

## Threat Modeling

### STRIDE

The scenario maps directly to STRIDE: **Information Disclosure**.

Monica is able to read cloud resources and configuration data belonging to other users or tenants, because the API does not enforce proper authorization checks. A secondary category of **Tampering** applies when the same authorization failures allow Monica to modify or delete resources she should not be able to reach.

### What can go wrong?

A poorly protected cloud API can expose the entire cloud environment to unauthorized access. Resource enumeration allows attackers to build a detailed picture of the infrastructure for further exploitation. Missing authorization checks can lead to cross-tenant data leakage in multi-tenant systems, one of the most serious forms of cloud isolation failure. If write operations are also unprotected, attackers can modify configurations, disrupt services, or destroy data across customer boundaries.

### What are we going to do about it?

Apply strong authentication, authorization, and input validation at every cloud API endpoint.

1. Require authentication for all API endpoints, using short-lived, scoped tokens rather than long-lived credentials or API keys.
2. Implement object-level authorization checks that verify the caller's right to access a specific resource by identifier — never trust caller-supplied resource IDs without validation.
3. Return consistent, non-revealing error responses for both "not found" and "access denied" cases to prevent enumeration based on response differences.