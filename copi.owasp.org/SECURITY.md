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
| Game Creation | 20 requests | per hour per IP |
| Player Creation | 60 requests | per hour per IP |
| WebSocket Connections | 333 connections | per second per IP |

### Configuration

Rate limits are configurable via environment variables:

```bash
# Game creation limits
RATE_LIMIT_GAME_CREATION_LIMIT=20
RATE_LIMIT_GAME_CREATION_WINDOW=3600  # seconds

# Player creation limits
RATE_LIMIT_PLAYER_CREATION_LIMIT=60
RATE_LIMIT_PLAYER_CREATION_WINDOW=3600  # seconds

# Connection limits
RATE_LIMIT_CONNECTION_LIMIT=333
RATE_LIMIT_CONNECTION_WINDOW=1  # seconds
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

### ATJ: Mark can access resources or services because there is no authentication requirement, or it was mistakenly assumed that authentication would be undertaken by some other system or performed in some previous action.

#### What can go wrong?

Be aware of data exposure risk! Copi does not support authentication.
We have not implemented Authentication when using Copi, instead we use a secure randomized string to prevent accidental data exposure. Still, an attacker may get hold of such a url by spoofing Copi or other Colleagues in your organization by leveraging various social engineering techniques like establishing a rogue location: [https://capec.mitre.org/data/definitions/616.html](https://capec.mitre.org/data/definitions/616.html).

An attacker could use various tools for capturing logs or http requests which may lead to information disclosure if your participants' network has been comporised: [https://capec.mitre.org/data/definitions/569.html](https://capec.mitre.org/data/definitions/569.html).

Do you think this is strange? Indeed, in this day and age, it is, but if we were to implement authentication, we would also have to process more personal information, which would open us up to more threats. We could indeed mitigate those threats, but we would rather remain privacy-friendly and process as little personal information as possible.

Game integrity is still enforceable only by client behavior in a few important paths. During the game, the app only checks that a voted card belongs to the same game before inserting a vote, so a crafted client can self-vote because there is no server-side owner check. The app separately creates the votes table without a uniqueness constraint, and dealt cards stores played_in_round without any DB-level rule that limits a player to one card per round. A malicious or racing client can therefore duplicate votes or play multiple cards in the same round.

#### What are we going to do about it?

We are not working towards implementing authentication in Copi. Instead, we are utilizing magic links. Arguable this is not authentication, but it's worth noting that your threat model is not stored on copi.owasp.org, just your game and the cards you voted on. For a threat actor to be able to piece together this information and use it against you, given that he gets hold of the magic link, you would have to use your full name and add the URL to your project in the game name field when creating the game. We are working towards informing users that they should under no circumstances do this kind of thing, but even in the case that you still do. The cards themselves are too generic and don't contain the sensitive discussions that you had during your game.
As a security measure, you can choose to run Copi on a private cluster
You should avoid using your own name or the name of a company or project when creating players and games at copi.owasp.org. And remind others not to do so as well. Instead, use a pseudonym and a fake threat model name.

There is a GitHub issue to resolve the voting integrity vulnerability (see:  https://github.com/OWASP/cornucopia/issues/2568). The damage is limited by the fact that most players during a game know each other and by having the url to the game being a random magic link.

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

The Fly.io reverse proxy does not strip or rewrite untrusted X-Forwarded-For headers before traffic reaches Phoenix. It is therefor still possible to circumvent the rate-limiter. 

#### What are we going to do about it?

We are working on minimizing the probability of functionality misuse by implementing rate limiting on the creation of games and players (see: [issues/1877](https://github.com/OWASP/cornucopia/issues/1877)). Once that is taken care of, you should be able to configure these limits to prevent DoS attacks when hosting Copi yourself. It's vital that you limit the number of sockets the application accepts concurrently. On fly.io that is done in the following way: [fly.toml](https://github.com/OWASP/cornucopia/blob/fb9aae62531dde8db154729d0df4aa28a3400063/copi.owasp.org/fly.toml#L27) A 30 socket limit for Copi should allow you to handle 20.000 requests per min if you have 2 single cpu nodes Which we have tested against that setup.

Use of Fly-Client-IP has been considered. We are looking into implementing this for Copi (see: https://github.com/OWASP/cornucopia/issues/3227).

### CK: Grant can utilize the application to deny service to some or all of its users

#### What can go wrong?

Given that  a threat actor can  execute a distributed denial of service attack against the application, he could deny access to some or all of copi.owasp.org users.

#### What are we going to do about it?

We are not working towards implementing any specific controls to prevent DoS attacks against copi.owasp.org. Most probably, it would be impossible to stop a distributed denial of service attack if executed properly. When we did load testing against copi.owasp.org, we found that the application could handle 20.000 request per min. I is f we went higher than that, Cloudflare, which hosts the DNS, would identify us as a DoS actor and return HTTP status 520. Still, conceptually, you could execute a DoS from one million machines and deny access to the application for other users. Even though this is a risk, we accept it. If you are worried about distributed DoS, please host the application on a private network or whitelist IP access to the application.
If you are hosting Copi yourself, please set the rate limiting according to your needs (see: [Configuration](SECURITY.md#configuration).

### Did we do a good job?

We welcome any input or improvements you might be willing to share with us regarding our current threat model.
Arguably, we created the system before we were able to identify all these threats, and several improvements need to be made to properly balance the inherent risks of compromise against the current security controls. For anyone choosing to host the game engine, please take this into account.

