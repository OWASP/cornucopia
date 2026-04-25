## Scenario: Sophia's JWT Forgery and Token Reuse

Sophia forges, predicts, or reuses authentication tokens to impersonate legitimate users and take over their sessions without knowing their passwords. This occurs because:

1. **Weak or absent token signing:** JWTs are signed with a weak secret, use the `none` algorithm, or are validated incorrectly — allowing Sophia to craft tokens the server will accept as genuine.

2. **Predictable token values:** Tokens or session identifiers are generated using a weak random number generator or contain user-controlled fields that Sophia can enumerate or manipulate.

3. **Long-lived tokens without revocation:** Access tokens or refresh tokens remain valid for extended periods with no server-side revocation mechanism, so a token obtained through any means continues to work long after the legitimate user has moved on.

### Example

Sophia finds that an application issues JWTs signed with a symmetric HMAC secret stored in the client-accessible configuration file bundled with the frontend. She reads the secret, crafts a JWT with `"sub": "admin", "role": "administrator"` in the payload, signs it with the extracted key, and submits it to the API. The server validates the signature successfully and grants her full administrative access. Sophia has never interacted with the actual administrator's account and the server logs show a valid token being presented — nothing appears out of the ordinary.

## Threat Modeling

### STRIDE

The scenario maps directly to STRIDE: **Spoofing**.

Sophia presents a token that the server believes is genuine, allowing her to impersonate any user or role she chooses to encode. The attack targets the trust the server places in the token's authenticity.

### What can go wrong?

Forged or compromised tokens grant the attacker the identity and permissions of any user in the system, including administrators. Because the token is structurally valid, the server processes requests normally and audit logs attribute the attacker's actions to the impersonated account. Token reuse after a breach or account closure extends the window of exposure indefinitely if there is no revocation mechanism.

### What are we going to do about it?

Sign tokens with strong secrets that are never exposed to clients, validate them rigorously, and limit their lifespan.

1. Sign JWTs with asymmetric keys (RS256 or ES256) so that only the server holds the private key; the public key used by verifiers cannot be used to forge tokens.
2. Never accept the `alg: none` algorithm; explicitly allowlist the expected signing algorithm on the server side during validation.
3. Store signing secrets server-side only, never in frontend bundles, environment variables accessible to clients, or source code repositories.
4. Set short expiry times on access tokens (minutes to hours) and use refresh token rotation so that a stolen token's usefulness degrades quickly.
5. Implement token revocation for sensitive operations (logout, password change, account suspension) using a server-side denylist or short-lived tokens tied to a session record.
