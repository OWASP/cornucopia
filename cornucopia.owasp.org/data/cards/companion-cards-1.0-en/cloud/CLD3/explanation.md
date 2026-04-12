## Scenario: Roupe's Discovery of a Publicly Accessible Cloud Storage Bucket

Roupe finds and downloads sensitive customer data stored in a cloud object storage bucket that has been misconfigured to allow public access. This occurs because:

1. **Misconfigured Bucket ACLs or Policies:** The storage bucket has access control lists or bucket policies that permit unauthenticated read access, either intentionally or by mistake.

2. **No Blocking of Public Access:** Cloud provider safeguards that prevent public exposure (such as AWS S3 Block Public Access) are either disabled or not applied at the account level.

3. **Sensitive Data Stored Without Access Controls:** Files containing customer records, credentials, or business data are placed in the bucket without being encrypted or access-restricted at the object level.

### Example

Roupe discovers the application's domain name and infers that file storage might be hosted on a well-known cloud provider. Using publicly available tools to enumerate bucket names derived from the company's domain, he identifies a particular available bucket name. He queries the bucket URL directly in a browser and finds that the access control list is set to public read. Within minutes, Roupe downloads a set of CSV files containing full names, email addresses, dates of birth, and payment history for tens of thousands of customers - without authenticating at any point.

## Threat Modeling

### STRIDE

The scenario maps directly to STRIDE: **Information Disclosure**.

The bucket is publicly accessible, meaning any person on the internet can read the data it contains without authentication. Roupe does not need to break any security control, the data is simply left open.

### What can go wrong?

Publicly exposed cloud storage buckets are one of the most common sources of large-scale data breaches. Sensitive customer data, internal configuration files, database backups, and credentials can all be exposed. The impact ranges from regulatory penalties and legal liability to reputational damage and direct fraud against affected customers. Because cloud storage URLs follow predictable patterns, automated scanners routinely find these misconfigurations before the data owners do.

### What are we going to do about it?

Ensure that cloud storage buckets are private by default and that sensitive data is never publicly accessible.

1. Enable cloud provider-level controls that block all public access to storage buckets at the account and organisation level (e.g., AWS S3 Block Public Access settings).
2. Audit existing storage buckets regularly for public ACLs or permissive bucket policies; remediate any that allow unauthenticated access.
3. Apply server-side encryption to all stored objects and ensure that encryption keys are properly managed and rotated.
4. Implement lifecycle policies and inventory scanning to detect newly created buckets that deviate from the expected private configuration.