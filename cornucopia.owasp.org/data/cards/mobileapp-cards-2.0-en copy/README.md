# Mobile app cards 2.0 explanations

These explanations use `source/mobileapp-cards-2.0-en.yaml` for the card wording and
names, and `source/mobileapp-mappings-2.0.yaml` for each card's threats, attack
vectors, MASWE weaknesses, MASTG tests, best practices, and knowledge references.
The cross-links in `source/mobileapp-maswe-2.0.yaml` (MASWE to MASTG) and
`source/mobileapp-mastg-2.0.yaml` (MASTG to MASWE, knowledge, and best practices)
were used to keep each list reciprocal, then the corresponding source text was
checked in
`C:\Users\johan\src\maswe\weaknesses`, `C:\Users\johan\src\mastg\best-practices`,
`C:\Users\johan\src\mastg\knowledge`, and `C:\Users\johan\src\mastg\tests-beta`.

The mapped sources were selected because they describe the same trust boundary and
failure mode as the card, while the mapped application attacks show how a person
would actually reach that boundary on a phone. Keeping those lists card-specific
prevents a plausible control from one card being presented as evidence for another.
All completed pages is described with a light-hearted example under `### Example`. Their failure and remediation sections explain the card-specific threat and attack routes before reproducing the mapped source IDs and text. The 11 pages that already contained prose were left unchanged. Wildcard pages deliberately label their application attack as invented; they use mapped guidance only when the mapping files provide it.
