# Security

This document addresses various security concerns you might have when running the service. Keep in mind that Copi does not use authentication. This is because Copi has been implemented to be privacy-friendly. If we had implemented authentication, we would have had to store your email address. As we want to allow users to use our service without having to provide their email, the service must be open. To avoid misuse, we have implemented the following measures. 

## Rate Limiting Implementation

### Overview

Copi implements IP-based rate limiting to protect against CAPEC-212 (Functionality Misuse) attacks and ensure service availability under potential abuse scenarios.

This implementation addresses:

- **CAPEC-212 (Functionality Misuse)**: Prevents abuse of game/player creation
- **Resource exhaustion**: Prevents overwhelming the system
- **Service availability**: Ensures legitimate users can access the service

### Rate Limiting Strategy

The application uses a GenServer-based rate limiter that tracks requests per IP address across different action types. This prevents malicious actors from overwhelming the service while maintaining usability for legitimate users.

#### Protected Actions

1. **Game Creation**: Limited to prevent mass game creation attacks
2. **Player Creation**: Limited to prevent player spam
3. **WebSocket Connections**: Limited to prevent connection flooding

### Default Rate Limits

| Action | Limit | Time Window |
| --- | --- | --- |
| Game Creation | 10 requests | per hour per IP |
| Player Creation | 60 requests | per hour per IP |
| WebSocket Connections | 133 connections | per second per IP |

### Configuration

Rate limits are configurable via environment variables:

```bash
# Game creation limits
RATE_LIMIT_GAME_CREATION_LIMIT=10
RATE_LIMIT_GAME_CREATION_WINDOW=3600  # seconds

# Player creation limits
RATE_LIMIT_PLAYER_CREATION_LIMIT=60
RATE_LIMIT_PLAYER_CREATION_WINDOW=3600  # seconds

# Connection limits
RATE_LIMIT_CONNECTION_LIMIT=133
RATE_LIMIT_CONNECTION_WINDOW=1  # seconds

# This option can be used for fly.io so that the application uses a validated client IP.
# By default this option is set to false, which means that the `X-Forwarded-For` header will be used.
# For obvious reasons, the `X-Forwarded-For` header may be manipulated and is therefore less safe.
USE_FLY_CLIENT_IP = true
```

**Note**: Environment variables must be positive integers. Invalid values will log a warning and fall back to defaults.

### Implementation Details

#### Architecture

- **RateLimiter GenServer** (`lib/copi/rate_limiter.ex`): Core rate limiting logic
  - Tracks requests per IP and action type
  - Implements sliding window algorithm
  - Auto-cleanup of expired entries every 5 minutes
  
- **IPHelper Module** (`lib/copi/ip_helper.ex`): IP extraction utilities
  - Provides DRY interface for IP extraction
  - Handles LiveView sockets, Phoenix sockets, and Plug connections
  
- **Integration Points**:
  - Game creation: `lib/copi_web/live/game_live/create_game_form.ex`
  - Player creation: `lib/copi_web/live/player_live/form_component.ex`
  - WebSocket connections: `lib/copi_web/channels/user_socket.ex`

#### Rate Limit Response

When rate limits are exceeded:

- **Game/Player Creation**: User receives a flash error message: "Too many [action] attempts. Please try again later."
- **WebSocket Connections**: Connection is denied (returns `:error`)
- **Logging**: Rate limit violations are logged for monitoring

#### IP Address Handling

- Supports both IPv4 and IPv6
- Accepts IP addresses as tuples or strings
- Normalizes IP formats for consistent tracking
- **Proxy Support**: Automatically reads `X-Forwarded-For` header to get real client IP when behind reverse proxies
  - Uses leftmost IP from X-Forwarded-For (original client IP)
  - To use the Fly client IP instead (only available for fly.io), set USE_FLY_CLIENT_IP = true
  - Falls back to `remote_ip` if header is missing or invalid
- Falls back gracefully when IP is unavailable

### Testing

Comprehensive test coverage in:
- `test/copi/rate_limiter_test.exs`: Core rate limiter functionality
- `test/copi_web/channels/user_socket_test.exs`: WebSocket connection rate limiting

### Security Considerations

#### Limitations

1. **IP-based tracking**: Can be bypassed by users with multiple IP addresses or using proxies
2. **Shared IPs**: Users behind NAT may share rate limits
3. **No authentication**: Current implementation doesn't require user authentication

#### Future Enhancements

If rate limiting proves insufficient, consider:
1. Implementing user authentication and associating limits with user accounts
2. Adding browser fingerprinting for better user identification
3. Implementing CAPTCHA for repeated violations
4. Adding IP allowlisting for trusted networks
5. Implementing more sophisticated detection patterns (behavioral analysis)

### Monitoring

The RateLimiter logs configuration on startup and warnings when limits are exceeded. Monitor these logs to:
- Detect potential attacks
- Adjust rate limits based on legitimate usage patterns
- Identify problematic IPs

## Player Capabilities

Anyone with a game link can watch that game. Watching does not require a player session.

Player actions have a separate check. When a player is created, Copi signs a capability that contains the game ID, the player ID, and the `player` purpose. The capability expires after 5 minutes. The browser sends it in the body of a CSRF-protected POST request. The endpoint adds the player to the encrypted session cookie and returns the normal player URL without the capability.

Each capability is intended for one exchange. Copi stores only a SHA-256 digest for 5 minutes. The check and update are one atomic operation in each replay store. The bearer value is not stored in a replay registry.

By default, replay protection uses memory on one application node. When `DNS_CLUSTER_QUERY` enables Erlang clustering, each node first uses one globally registered registry. If it cannot reach that registry, it uses its local registry and synchronizes active digests after the connection returns. This keeps capability exchange available during a cluster outage, but the same capability may be accepted independently on both sides of a partition before synchronization. Synchronization cannot undo an exchange that already succeeded. In-memory entries are also lost when a node restarts.

PostgreSQL storage can be enabled with `POSTGRES_SESSION_STORE_ENABLED=true`. In that mode, a unique database insert provides replay protection across all nodes that use the same database. PostgreSQL replay protection takes precedence over the local and clustered registries. If the database is unavailable, the exchange fails instead of falling back to memory.

The player session lasts for up to 7 days. By default, it is stored in the signed and encrypted Phoenix session cookie. With PostgreSQL storage enabled, the cookie contains an opaque session ID protected by Phoenix cookie encryption, while session data written to the `copi_sessions` table is encrypted with `COPI_ENCRYPTION_KEY` using AES-256-GCM. `COPI_ENCRYPTION_KEY` is not used for browser cookie encryption or capability signing. One session can contain several player capabilities for the same game and for different games. Adding a player does not remove existing players. The cookie is HTTP-only, uses `SameSite=Lax`, and is marked secure in production.

The game ID and player ID in the URL select the active player. Copi accepts the action only when that exact game and player pair is present in the cookie. A player ID from another stored game cannot be combined with the current game ID. Copi also checks that the card belongs to the selected player. Card play uses CSRF protection.

A game link and a player capability are not interchangeable. A game link allows someone to watch a game. It does not allow that person to play a card as another player.

The player capability is a bearer secret until it is exchanged or expires. Sending it in a POST body keeps it out of the address bar, browser history, referrer headers, and normal URL logs. The exchange response uses `Cache-Control: no-store`. Use HTTPS and make sure proxies and application monitoring do not log request bodies containing capabilities.

Cluster mode improves replay protection while nodes are connected, but it is not a consensus or durable store. A network partition, global registry timeout, node restart, or cluster restart can allow reuse during the 5-minute capability lifetime. PostgreSQL mode avoids those replay gaps when every node uses the same available database, but it adds session availability and confidentiality dependence on PostgreSQL. Use verified database TLS and restrict access to the session tables.

The encrypted session cookie is also a bearer credential. In default cookie mode, a stolen copy can be used until it expires unless the signing key is rotated. In PostgreSQL mode, a copied cookie refers to the same server-side row and can be invalidated by deleting that row, but it remains usable until expiry if no revocation occurs. The cookie is not tied to an IP address because client addresses change and may be shared or supplied through an untrusted proxy header. A compromised browser or script running in the Copi origin may still perform actions using an HTTP-only cookie even though it cannot read the cookie value.

## Encryption Key Setup

Game and player names are encrypted at the application level using AES-256-GCM.
You must set the `COPI_ENCRYPTION_KEY` environment variable before deploying.

### Generate a secure encryption key

    openssl rand -base64 32

### Set the key in your environment

**Fly.io:**

    fly secrets set COPI_ENCRYPTION_KEY=<your-generated-key> --app <app name>

**Heroku:**

    heroku config:set COPI_ENCRYPTION_KEY=<your-generated-key>

**Local development:**

   export COPI_ENCRYPTION_KEY=<your-generated-key>

## Contact

For security issues or questions, please refer to the main repository [SECURITY.md](/SECURITY.md).

## Our Threat Model

The Copi threat model can be found at [ThreatDragonModels/copi.json](https://github.com/OWASP/cornucopia/blob/master/ThreatDragonModels/copi.json). You may review it by using [OWASP Threat Dragon](https://www.threatdragon.com/#/dashboard).

Please also read [SECURITY.md](SECURITY.md) to ensure you have taken the appropriate measures to secure Copi if you are running the service yourself.

Here is a short summary of what you need to be aware of:

### ATJ: Anyone with a game link can watch the game

#### What can go wrong?

Copi does not use user accounts. Anyone with a game link can watch that game. This is intended.

Someone may obtain a game link, a short-lived player capability, or a player session cookie through social engineering, logs, a compromised browser, or a compromised network. See [CAPEC-616](https://capec.mitre.org/data/definitions/616.html) and [CAPEC-569](https://capec.mitre.org/data/definitions/569.html).

Watching a game does not grant player access. Player access requires a signed capability that expires after 5 minutes. If someone steals that capability before it is used, they may exchange it and become that player. The capability is sent in a POST body, so a proxy or monitoring service that records request bodies may capture it.

By default, Copi remembers used capabilities in the memory of one application node. That record is lost when the node restarts. In a cluster, nodes normally share this check through one global registry. If the nodes lose contact, each node uses its own local record. The same capability may then be accepted by more than one node. Synchronizing the records later cannot undo an exchange that has already succeeded.

An optional PostgreSQL mode avoids these replay gaps by keeping the session and replay records in one database. This makes player sessions depend on the database being available. The session records are encrypted, but anyone who obtains both the database contents and `COPI_ENCRYPTION_KEY` can read them.

The player session cookie is a bearer credential. Anyone who steals a valid copy can act as every player stored in that session until it expires. In the default cookie mode, an individual stolen session cannot be revoked. In PostgreSQL mode, deleting the server-side session record revokes it.

Voting and card play still have race conditions. The votes table has no uniqueness constraint, so two requests made at nearly the same time may create duplicate votes. The database also has no rule that limits a player to one played card per round, so concurrent requests may play more than one card.

#### What are we going to do about it?

Use HTTPS. Do not record capability exchange request bodies in proxies, application monitoring, or access logs. Protect `SECRET_KEY_BASE` and `COPI_ENCRYPTION_KEY`, and rotate the affected key if it is exposed.

Use PostgreSQL session storage when a capability must be accepted only once across several application nodes. Restrict access to the session tables and use verified TLS for the database connection. Without PostgreSQL mode, accept that a restart or cluster partition can allow a capability to be reused during its 5-minute lifetime.

Copi stores game and card choices, but not the discussion held by the players. Do not use a real person, company, or project name for a game or player. Use a pseudonym and a made-up threat model name.

Run Copi on a private network if viewing by game link is not suitable for your use case.

Voting integrity is tracked in [issue 2568](https://github.com/OWASP/cornucopia/issues/2568).

## CR6: Romain can read and modify unencrypted data in memory or in transit (e.g., cryptographic secrets, credentials, session identifiers, personal and commercially-sensitive data), in use or in communications within the application, or between the application and users, or between the application and external systems.

#### What can go wrong?

Production database transport security is not safely configured by default. The DB SSL option is set at startup to either false or verify_none, and the app applies that value directly to the Repo. In other words, the current code path never enables verified TLS to Postgres by default. If the database is not strictly local/private, credentials and application data can be exposed or modified in transit.
If deploying Copi, configure TLS between the DB and your app and between the nodes in your app cluster.
Erlang clustering does not happen over TLS by default. This may allow an attacker to launch an MTM attack and do RCE against your cluster. It may also allow an attacker to take over your database connection and both disclose sensitive information and compromise the integrity of the data sent between your database and Copi.

Cookie and TLS hardening still depend on deployment discipline rather than being enforced by the app. The repo ships a fixed secret_key_base in config.exs, the session cookie is only marked secure during app start-up, and HTTPS enforcement is only documented, not enabled by default. If a staging or self-hosted deployment ever runs outside strict prod/TLS settings, session confidentiality and integrity may degrade quickly.

#### What are we going to do about it?

If you deploy Copi yourself, make sure you configure TLS appropriately according to your needs.
OWASP host Copi on Fly.io that uses a built-in, WireGuard-encrypted 6PN (IPv6 Private Networking) mesh to automatically connect all your app instances, providing zero-config, secure, private communication with internal DNS (e.g., app-name.internal), allowing services to talk as if they're on the same network, even across regions, for simple and secure microservices communication. This mesh handles complex routing, making it easy to build distributed apps securely without manual VPN setup.

### AZ: Mike can misuse an application by using a valid feature too fast, or too frequently, or in any other way that is not intended, or consumes the application's resources, or causes race conditions, or over-utilizes a feature.

#### What can go wrong?

An attacker can deny access to user's by CAPEC 212, functionality misuse by continuing to create an unlimited amount of games and players until the application stops responding.

The current rate-limiting design is easy to evade in common proxy or multi-instance deployments. The rate limiting trusts the left-most X-Forwarded-For value and explicitly skips connection limiting when only remote_ip is available. The counters are kept in the in-memory GenServer. That means spoofed forwarded headers, multiple app nodes, or proxy/header misconfiguration can let an attacker bypass the main abuse-control mechanism. We are more than happy to get suggestions for how to improve the rate-limiting. Currently we are not seeing a lot of issues concerning the misuse of our services in production.

The Fly.io reverse proxy does not strip or rewrite untrusted X-Forwarded-For headers before traffic reaches Phoenix. It is therefore still possible to circumvent the rate-limiter.

#### What are we going to do about it?

We are working on minimizing the probability of functionality misuse by implementing rate limiting on the creation of games and players (see: [issues/1877](https://github.com/OWASP/cornucopia/issues/1877)). Once that is taken care of, you should be able to configure these limits to prevent DoS attacks when hosting Copi yourself. It's vital that you limit the number of sockets the application accepts concurrently. On fly.io that is done in the following way: [fly.toml](https://github.com/OWASP/cornucopia/blob/fb9aae62531dde8db154729d0df4aa28a3400063/copi.owasp.org/fly.toml#L27) A 30 socket limit for Copi should allow you to handle 20.000 requests per min if you have 2 single cpu nodes Which we have tested against that setup.

When Copi receives traffic directly from Fly Proxy, set `USE_FLY_CLIENT_IP=true`. [Fly.io documents `Fly-Client-IP`](https://fly.io/docs/networking/request-headers/#fly-client-ip) as the client IP address from Fly Proxy's perspective and says it may be a better choice than `X-Forwarded-For`, which must be treated with caution to avoid spoofing. Using it prevents Copi's rate limiter from trusting a client-controlled, left-most `X-Forwarded-For` value. If another reverse proxy is in front of Fly.io, `Fly-Client-IP` contains that proxy's address instead of the original client's address; in that deployment, parse `X-Forwarded-For` using an explicit trusted-proxy configuration.

### CK: Grant can utilize the application to deny service to some or all of its users

#### What can go wrong?

Given that  a threat actor can  execute a distributed denial of service attack against the application, he could deny access to some or all of copi.owasp.org users.

#### What are we going to do about it?

We are not working towards implementing any specific controls to prevent DoS attacks against copi.owasp.org. Most probably, it would be impossible to stop a distributed denial of service attack if executed properly. When we did load testing against copi.owasp.org, we found that the application could handle 20.000 request per min. I is f we went higher than that, Cloudflare, which hosts the DNS, would identify us as a DoS actor and return HTTP status 520. Still, conceptually, you could execute a DoS from one million machines and deny access to the application for other users. Even though this is a risk, we accept it. If you are worried about distributed DoS, please host the application on a private network or whitelist IP access to the application.
If you are hosting Copi yourself, please set the rate limiting according to your needs (see: [Configuration](SECURITY.md#configuration).

### Did we do a good job?

We welcome any input or improvements you might be willing to share with us regarding our current threat model.
Arguably, we created the system before we were able to identify all these threats, and several improvements need to be made to properly balance the inherent risks of compromise against the current security controls. For anyone choosing to host the game engine, please take this into account.

