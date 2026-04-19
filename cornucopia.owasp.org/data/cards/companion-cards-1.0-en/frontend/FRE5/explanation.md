## Scenario: Victor's CDN Script Supply Chain Compromise

Victor compromises a third-party JavaScript library hosted on a CDN and delivers malicious code to every user of any application that loads the script without integrity verification. This occurs because:

1. **Unverified external scripts:** The application loads JavaScript from a CDN or third-party URL using a plain `<script src>` tag, with no Subresource Integrity (SRI) hash to verify the file's authenticity.

2. **Implicit trust in third-party providers:** The application assumes that scripts loaded from a known CDN will always be legitimate, without considering that the CDN itself, the package maintainer's account, or the distribution pipeline could be compromised.

### Example

Victor discovers a vulnerability in the build pipeline of a popular analytics library used by thousands of websites. He injects a payload into the minified bundle hosted on the library's CDN: a few extra lines that silently collect form field values — including usernames, passwords, and payment card numbers — and forward them to a server he controls. Within hours, the malicious version propagates to every website that loads the script without an integrity check. Millions of users submit sensitive data that is simultaneously captured by Victor's exfiltration endpoint.

## Threat Modeling

### STRIDE

The scenario maps directly to STRIDE: **Tampering**.

Victor modifies a trusted script at its source or distribution point, altering the code that all downstream applications and users receive. The integrity of the supply chain has been broken.

### What can go wrong?

A single compromised third-party script can turn every application that loads it into a credential harvester or data exfiltration tool, affecting all users simultaneously. Because the script runs in the application's origin, it bypasses same-origin policy protections, can read any cookie not marked `HttpOnly`, access DOM content, and make authenticated API requests. The attack is invisible to the application's own server-side logs and difficult to detect without client-side monitoring.

### What are we going to do about it?

Treat every externally loaded asset as potentially hostile and reduce your exposure to third-party script compromise.

1. Apply Subresource Integrity (SRI) hashes to all externally loaded scripts and stylesheets; the browser will refuse to execute any file whose hash does not match.
2. Audit and minimise the number of third-party scripts loaded by the application — every external dependency is an additional attack surface.
3. Host critical third-party libraries yourself rather than loading them from an external CDN, so you control when and how updates are applied.
4. Implement a strict Content Security Policy (CSP) that restricts which origins are allowed to serve scripts, limiting the blast radius of a compromised CDN.