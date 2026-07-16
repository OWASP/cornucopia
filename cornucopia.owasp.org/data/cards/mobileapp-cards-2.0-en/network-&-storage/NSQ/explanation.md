## Scenario: Ahmed can read and modify data in transit because the communication is transmitted over an unencrypted channel

Consider a scenario where Ahmed is sitting in a café operating a rogue access point. The target app makes some API calls over HTTPS but a subset of older API endpoints still use HTTP — a legacy from when the API was first launched. Ahmed intercepts the HTTP requests, reads the session token in the `Authorization` header, and replays it against the HTTPS endpoints. The session token was transmitted in cleartext over HTTP. One unencrypted request is all it takes.

1. HTTP transmits all content in cleartext; anyone who can observe the network can read and modify it.
2. A single HTTP request carrying a session token or credentials compromises the session even if all other requests use HTTPS.
3. Mixed-content scenarios: an app that starts with HTTPS but follows an HTTP redirect or loads resources over HTTP is partially exposed.

### Example

Ahmed's rogue access point logs all traffic. He filters for HTTP requests from mobile apps. He sees `GET http://api.target.com/profile` with `Authorization: ****** He uses the token to make authenticated HTTPS requests to the same API. He now has full account access. The developer had marked the `/profile` endpoint as "low-risk" because it only read data. The session token, once captured, gave access to everything else.

## Threat Modeling

### STRIDE

This scenario falls under **Information Disclosure** and **Tampering**.

Cleartext HTTP communication allows passive interception (disclosure) and active modification (tampering) of all data in transit, including authentication credentials that enable further attacks.

### What can go wrong?

- Credentials and session tokens transmitted over HTTP are captured and replayed.
- API responses are modified by an on-path attacker to inject malicious content.
- Users on untrusted networks (public Wi-Fi, mobile hotspots) are exposed to interception without any indication.

### What are we going to do about it?

- Migrate all API endpoints to HTTPS; there are no legitimate exceptions for endpoints that carry authentication credentials.
- Set `cleartextTrafficPermitted="false"` on Android and enforce ATS on iOS.
- Implement HTTP Strict Transport Security (HSTS) on the server to prevent protocol downgrade even if a client does not enforce HTTPS.
- Audit all URLs in the app's source code for `http://` scheme references.
