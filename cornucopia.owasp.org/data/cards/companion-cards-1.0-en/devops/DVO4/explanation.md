## Scenario: Bart's Unauthorized Access to Backup Data

Consider a scenario where Bart gains unauthorized access to backup data and is able to delete, overwrite, or download it. This vulnerability arises from:

1. **Insufficient Access Controls on Backups:** Backup storage locations lack proper authentication and authorization, allowing unauthorized users to interact with them.

2. **Lack of Immutability Protections:** Backups are stored in a way that allows anyone with write access to overwrite or delete them, rather than using append-only or immutable storage.

### Example

Bart discovers that the nightly backup job simply writes to a storage location, overwriting the previous backup each time. The write credentials used by the backup job are shared broadly and anyone with access to the build environment can use them. Bart realizes he can perform the same write operation himself, replacing the legitimate backup with arbitrary data. The storage does not enforce immutability or versioning, so the overwritten backup is gone for good. Bart also finds that the same credentials grant read access, allowing him to download the backup and access all the data it contains, including records he would not normally have permission to view.

## Threat Modeling

### STRIDE

This scenario maps to STRIDE: **Tampering**, **Information Disclosure**, and **Denial of Service**.

**Tampering** applies because Bart can overwrite backups with arbitrary data, corrupting the recovery data.

**Information Disclosure** fits because downloading backups exposes all the data they contain, which may include sensitive information not otherwise accessible to Bart.

**Denial of Service** is relevant because overwriting or deleting backups removes the ability to recover from incidents, effectively denying the service's continuity.

While three categories may seem broad, this card explicitly describes three distinct actions (delete, overwrite, download), each mapping naturally to a different threat category.

### What can go wrong?

Inadequately protected backups expose organizations to data theft and undermine their ability to recover from incidents. This can manifest in various forms, including but not limited to:

- Exfiltration of sensitive data from backup files
- Deletion or overwriting of backups, rendering disaster recovery impossible or significantly more costly and challenging
- Ransomware attacks targeting backup storage to prevent recovery
- Unauthorized access to historical data that may no longer be protected by current access controls

### What are we going to do about it?

1. Use immutable or append-only storage for backups so they cannot be overwritten or deleted, even by accounts that have write access.
2. Make sure only the backup process and designated administrators can access backup storage.
3. Use separate, dedicated credentials for backup operations that are not shared with other systems or users.
4. Store backups separately from the production environment, with their own access controls.
5. Encrypt backups both in transit and at rest to protect against unauthorized data access. If you do encrypt your backups at rest, make sure your encryption keys don't get lost in an incident.
6. Set up monitoring on access to backup storage, including reads, writes, and deletions.
7. Use versioning for backups so that even if one is corrupted, previous versions can still be recovered.
