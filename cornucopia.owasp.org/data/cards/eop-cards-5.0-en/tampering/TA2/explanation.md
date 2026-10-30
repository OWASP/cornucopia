## Scenario: The Grand Bodge's keycards open every room and the minibar

### Example

The Grand Bodge hotel's CTO rejected a commercial keycard system as too expensive, so he built BodgeLock. Each card holds the room number, checkout date, and role (`guest` or `staff`), encrypted with a key derived by repeating those public values and XORing a salt printed in every lock's maintenance manual. A CRC-16 covers the card.

Guest Sam reads his card, derives the key, changes `412` to `999`, flips `guest` to `staff`, re-encrypts with the penthouse key, and recalculates the CRC with a free online tool. The penthouse and minibar open. No encryption was broken; it was never protecting anything.

WEP made the same mistake at scale. IEEE 802.11 combined RC4, a 24-bit IV, and a CRC-32 integrity check — standard primitives in a homemade protocol. CRC-32 is linear and unkeyed, so frames can be altered and the checksum repaired without the key; short IVs repeat and leak keystream. FMS (2001) broke WEP on paper, PTW (2007) recovered a 104-bit key from under 40,000 frames in about a minute, and the FBI demonstrated a three-minute 128-bit crack in 2005. WEP was deprecated in 2004, yet routers kept shipping it with a reassuring padlock.

Sources: [FMS's RC4 key-scheduling analysis](https://www.cs.cornell.edu/people/egs/615/rc4_ksaproc.pdf), [the PTW attack paper](https://eprint.iacr.org/2007/120), [SmallNetBuilder's account of the FBI demonstration](https://www.smallnetbuilder.com/wireless/wireless-features/thefedscanownyourwlantoo/), and [IEEE 802.11i-2004, which deprecated WEP](https://doi.org/10.1109/ieeestd.2004.94585).

## Threat Modeling

### STRIDE

**Tampering** is primary: Sam changes the room number and role, re-encrypts the card, and recalculates the checksum, so the lock accepts modified data. **Spoofing** follows because a forged `staff` card lets him act as an employee, and a cloned card lets him act as another guest. **Elevation of Privilege** is the same edit one field later, from `guest` to `staff`. **Information Disclosure** covers the derivable key: the lock's "secret" is built from data printed on the card and a salt shipped in every lock, so anyone who reads the manual can decrypt any card. **Repudiation** is weak because the lock log records the room number from the card, which the attacker controls. **Denial of Service** is possible by writing malformed cards that crash the lock, or by reusing an old checkout date to lock a guest out.

### What can go wrong?

**A checksum is not a MAC.** CRC-16 and CRC-32 detect accidental corruption, not deliberate modification. They are linear and unkeyed, so anyone can recompute them after changing the data; a secret prefix or a hardcoded salt does not turn a CRC into a MAC. Use a standard MAC or AEAD. See [CWE-353](https://cwe.mitre.org/data/definitions/353.html), [CWE-345](https://cwe.mitre.org/data/definitions/345.html), [NIST SP 800-38B](https://csrc.nist.gov/pubs/sp/800/38/b/upd1/final), and [OWASP ASVS 5.0 V11.3.3](https://github.com/OWASP/ASVS/blob/master/5.0/en/0x20-V11-Cryptography.md).

**Keys derived from public data are not secret.** The room number and checkout date are printed on the card or known to the guest, and the salt ships in every lock; repeating them into 128 bits adds length, not entropy. A key must come from a secret with at least 128 bits of entropy, stored per device, and never hardcoded. See [CWE-321](https://cwe.mitre.org/data/definitions/321.html), [CWE-330](https://cwe.mitre.org/data/definitions/330.html), [NIST SP 800-57 Part 1 Rev. 5](https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final), and [OWASP ASVS 5.0 V11.5.1](https://github.com/OWASP/ASVS/blob/master/5.0/en/0x20-V11-Cryptography.md).

**Deterministic encryption and short IVs leak patterns.** BodgeLock has no per-card randomness, so two cards with the same data produce the same ciphertext. WEP's 24-bit IV collides after a few thousand frames, and reusing a stream-cipher nonce exposes the XOR of two plaintexts; reusing an AEAD nonce is worse. Nonces must be unique per key, with a size and generation method that make collisions negligible. See [CWE-323](https://cwe.mitre.org/data/definitions/323.html), [NIST SP 800-38D §8.2](https://csrc.nist.gov/pubs/sp/800/38/d/final), and [OWASP ASVS 5.0 V11.3.4](https://github.com/OWASP/ASVS/blob/master/5.0/en/0x20-V11-Cryptography.md).

**Home-made protocols hide the flaws until someone looks.** BodgeLock passed every internal demo because the demos used valid cards; WEP passed every interoperability test because interoperability was the requirement. Custom designs rarely get the adversarial review that standard protocols receive, and the weaknesses tend to be in the composition rather than the primitives. See [CWE-327](https://cwe.mitre.org/data/definitions/327.html), the [OWASP Cryptographic Storage Cheat Sheet on custom algorithms](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html#custom-algorithms), and [OWASP ASVS 5.0 V11.2.1](https://github.com/OWASP/ASVS/blob/master/5.0/en/0x20-V11-Cryptography.md).

### What are we going to do about it?

**Use a vetted protocol instead of designing one.** For transport, TLS 1.3, WireGuard, or Noise; for access cards, a current product with published cryptanalysis and a real key-management story. Do not let a facilities manager with a soldering iron specify the cipher suite. See [RFC 8446](https://www.rfc-editor.org/rfc/rfc8446), the [Noise Protocol Framework](https://noiseprotocol.org/noise.html), [NIST SP 800-52 Rev. 2](https://csrc.nist.gov/pubs/sp/800/52/r2/final), and [OWASP ASVS 5.0 V11.6.2](https://github.com/OWASP/ASVS/blob/master/5.0/en/0x20-V11-Cryptography.md).

**Use AEAD or a proper MAC, never a CRC.** AES-GCM or ChaCha20-Poly1305 for messages; AES-CMAC or HMAC when encryption and integrity are separate, combined encrypt-then-MAC with independent keys. See [NIST SP 800-38D](https://csrc.nist.gov/pubs/sp/800/38/d/final), [NIST SP 800-38B](https://csrc.nist.gov/pubs/sp/800/38/b/upd1/final), [RFC 5116](https://www.rfc-editor.org/rfc/rfc5116), and [OWASP ASVS 5.0 V11.3.2 and V11.3.5](https://github.com/OWASP/ASVS/blob/master/5.0/en/0x20-V11-Cryptography.md).

**Derive keys with a standard KDF and manage them per device.** Use HKDF or a protocol's built-in key schedule, give each lock and card its own keys, rotate them, and keep the root key in an HSM or secure element rather than a maintenance manual. See [RFC 5869](https://www.rfc-editor.org/rfc/rfc5869), [NIST SP 800-108 Rev. 1](https://csrc.nist.gov/pubs/sp/800/108/r1/upd1/final), [NIST SP 800-57 Part 1 Rev. 5](https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final), and [OWASP ASVS 5.0 V11.1.1](https://github.com/OWASP/ASVS/blob/master/5.0/en/0x20-V11-Cryptography.md).

**Use vetted libraries and constant-time comparisons.** libsodium, Tink, or the platform's audited crypto library; compare MACs with a constant-time function; prefer hardware-backed keystores and secure elements for physical tokens. See [libsodium's documentation](https://doc.libsodium.org/), [Google Tink](https://developers.google.com/tink), [CWE-208](https://cwe.mitre.org/data/definitions/208.html), and [OWASP ASVS 5.0 V11.2.1 and V11.2.4](https://github.com/OWASP/ASVS/blob/master/5.0/en/0x20-V11-Cryptography.md).
