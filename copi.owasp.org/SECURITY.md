# Security Implementation for Copi

This document describes the security measures implemented in Copi to protect against abuse and ensure service availability.

## Overview

Copi has implemented IP-based rate limiting to protect against **CAPEC 212 (Functionality Misuse)** attacks. These protections help ensure that the service remains available for all legitimate users by preventing a single source from overwhelming the system.

## Implemented Protections

### 1. Game Creation Rate Limiting

**Purpose**: Prevents a single IP address from creating an excessive number of games, which could lead to database exhaustion or denial of service.

**Default Configuration**:
- Maximum games per IP: 10
- Time window: 3600 seconds (1 hour)

**Behavior**:
- Tracks game creation attempts by IP address
- When the limit is exceeded, users receive a clear error message
- The limit resets after the time window expires
- Different IP addresses have independent limits

**Configuration**:
```bash
export MAX_GAMES_PER_IP=10
export GAME_CREATION_WINDOW_SECONDS=3600
```

### 2. WebSocket Connection Rate Limiting

**Purpose**: Prevents a single IP address from opening excessive WebSocket connections, which could exhaust server resources.

**Default Configuration**:
- Maximum connections per IP: 50
- Time window: 300 seconds (5 minutes)

**Behavior**:
- Tracks connection attempts by IP address
- When the limit is exceeded, connections are rejected with an error message
- The limit resets after the time window expires
- Does not affect existing active connections

**Configuration**:
```bash
export MAX_CONNECTIONS_PER_IP=50
export CONNECTION_WINDOW_SECONDS=300
```

## Technical Implementation

### Architecture

The rate limiting system consists of several components:

1. **Copi.RateLimiter** (`lib/copi/rate_limiter.ex`)
   - GenServer that maintains rate limit state
   - Tracks requests per IP address and action type
   - Automatically cleans up expired entries every 5 minutes
   - Provides a simple API for checking and recording actions

2. **CopiWeb.Plugs.RateLimiter** (`lib/copi_web/plugs/rate_limiter.ex`)
   - Plug for HTTP request rate limiting
   - Extracts IP addresses from connections
   - Handles X-Forwarded-For headers for reverse proxies
   - Returns proper HTTP 429 status codes when limits are exceeded

3. **LiveView Integration**
   - Game creation rate limiting in `CopiWeb.GameLive.CreateGameForm`
   - Connection rate limiting in `CopiWeb.GameLive.Index`
   - Provides user-friendly error messages

### IP Address Handling

The system correctly handles:
- IPv4 addresses (e.g., 192.168.1.1)
- IPv6 addresses (e.g., 2001:db8::1)
- X-Forwarded-For headers (for reverse proxy deployments)
- Multiple IP addresses in X-Forwarded-For (uses the first one)

### Rate Limit Response Headers

When rate limiting is active, the following headers are included in responses:

- `X-RateLimit-Remaining`: Number of requests remaining in the current window
- `Retry-After`: Seconds until the rate limit resets (only included when rate limited)

### Error Messages

Users who exceed rate limits receive clear, informative error messages:

```
Rate limit exceeded. Too many games created from your IP address.
Please try again in 3600 seconds.
This limit helps ensure service availability for all users.
```

## Deployment Considerations

### Reverse Proxy Configuration

If deploying behind a reverse proxy (nginx, HAProxy, Cloudflare, etc.), ensure the real client IP is passed through:

**Nginx**:
```nginx
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
```

**Apache**:
```apache
RequestHeader set X-Forwarded-For "%{REMOTE_ADDR}s"
```

**Cloudflare**:
Cloudflare automatically sets the CF-Connecting-IP header. The X-Forwarded-For header should also be present.

### Monitoring

Monitor the following metrics to detect abuse or adjust rate limits:

- Rate limit rejections (logged as warnings)
- Rate limit state size (number of tracked IPs)
- 429 HTTP responses
- Flash messages about rate limiting

### Adjusting Rate Limits

Rate limits can be adjusted based on your deployment needs:

**For Development/Testing**:
```bash
export MAX_GAMES_PER_IP=100
export MAX_CONNECTIONS_PER_IP=200
```

**For High-Traffic Production**:
```bash
export MAX_GAMES_PER_IP=5
export GAME_CREATION_WINDOW_SECONDS=7200  # 2 hours
export MAX_CONNECTIONS_PER_IP=30
export CONNECTION_WINDOW_SECONDS=600  # 10 minutes
```

**For Low-Traffic/Internal Use**:
```bash
export MAX_GAMES_PER_IP=50
export MAX_CONNECTIONS_PER_IP=100
```

## Testing

The implementation includes comprehensive tests:

- **Unit tests** for the RateLimiter GenServer (`test/copi/rate_limiter_test.exs`)
- **Integration tests** for the RateLimiter Plug (`test/copi_web/plugs/rate_limiter_test.exs`)

Run tests:
```bash
mix test
```

Run specific rate limiter tests:
```bash
mix test test/copi/rate_limiter_test.exs
mix test test/copi_web/plugs/rate_limiter_test.exs
```

## Future Enhancements

Potential future security enhancements (not currently implemented):

1. **Authentication Integration**
   - Associate rate limits with authenticated users
   - Different limits for authenticated vs. anonymous users
   - Per-user rate limiting instead of just per-IP

2. **Geographic Rate Limiting**
   - Different limits based on geographic location
   - Blocking or stricter limits for high-risk regions

3. **Adaptive Rate Limiting**
   - Automatically adjust limits based on system load
   - Stricter limits during high traffic periods

4. **CAPTCHA Integration**
   - Require CAPTCHA after repeated rate limit violations
   - Optional CAPTCHA for game creation

5. **Rate Limit Dashboard**
   - Admin interface to view current rate limit state
   - Ability to manually block/unblock IPs
   - Real-time monitoring of rate limit violations

## Reporting Security Issues

If you discover a security vulnerability in Copi, please report it to the OWASP Cornucopia team through the [GitHub Security Advisories](https://github.com/OWASP/cornucopia/security/advisories) page.

## References

- [CAPEC-212: Functionality Misuse](https://capec.mitre.org/data/definitions/212.html)
- [OWASP API Security Top 10 - API4:2023 Unrestricted Resource Consumption](https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/)
- [Phoenix Framework Security](https://hexdocs.pm/phoenix/security.html)
