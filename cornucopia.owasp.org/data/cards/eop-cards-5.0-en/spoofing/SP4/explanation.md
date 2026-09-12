## Scenario: Meridian's internal API trusts the network, not the caller

### Example

Meridian has an internal API that assumes the API gateway has already authenticated every request. Because of this, the API itself does not perform an authentication check. If an attacker can bypass or directly access the API, they may be able to send requests without proving who they are. This can allow unauthorized users to access or modify protected data.

## Threat Modeling

### STRIDE

This is **Spoofing** because an attacker can pretend to be a trusted caller by sending requests directly to the internal API without authentication. **Elevation of Privilege** can also apply if the attacker gains access to actions or data that should only be available to authenticated or higher-privileged users.

### What can go wrong?

The main design mistake is trusting the network or gateway instead of verifying the identity of the caller at the API itself. If the gateway is bypassed, misconfigured, or compromised, the API has no protection of its own. This goes against the zero-trust principle of not automatically trusting requests based on network location.
Source: [NIST Zero Trust Architecture](https://www.nist.gov/publications/zero-trust-architecture)

### What are we going to do about it?

The API should authenticate and authorize every request, even when the request comes through a trusted gateway. Each layer should independently verify the caller and enforce the required permissions. This follows a **zero-trust** approach, where no user or system is trusted automatically just because it is inside the network.
Source: [NIST Zero Trust Architecture](https://www.nist.gov/publications/zero-trust-architecture)
