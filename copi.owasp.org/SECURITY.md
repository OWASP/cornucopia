# Security - Rate Limiting Implementation

## Overview

Copi implements IP-based rate limiting to protect against CAPEC-212 (Functionality Misuse) attacks and ensure service availability under potential abuse scenarios.

## Rate Limiting Strategy

The application uses a GenServer-based rate limiter that tracks requests per IP address across different action types. This prevents malicious actors from overwhelming the service while maintaining usability for legitimate users.

### Protected Actions

1. **Game Creation**: Limited to prevent mass game creation attacks
2. **Player Creation**: Limited to prevent player spam
3. **WebSocket Connections**: Limited to prevent connection flooding

## Default Rate Limits

| Action | Limit | Time Window |
| --- | --- | --- |
| Game Creation | 20 requests | per hour per IP |
| Player Creation | 60 requests | per hour per IP |
| WebSocket Connections | 333 connections | per second per IP |

## Configuration

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

## Implementation Details

### Architecture

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

### Rate Limit Response

When rate limits are exceeded:

- **Game/Player Creation**: User receives a flash error message: "Too many [action] attempts. Please try again later."
- **WebSocket Connections**: Connection is denied (returns `:error`)
- **Logging**: Rate limit violations are logged for monitoring

### IP Address Handling

- Supports both IPv4 and IPv6
- Accepts IP addresses as tuples or strings
- Normalizes IP formats for consistent tracking
- **Proxy Support**: Automatically reads `X-Forwarded-For` header to get real client IP when behind reverse proxies
  - Uses leftmost IP from X-Forwarded-For (original client IP)
  - Falls back to `remote_ip` if header is missing or invalid
- Falls back gracefully when IP is unavailable

## Testing

Comprehensive test coverage in:
- `test/copi/rate_limiter_test.exs`: Core rate limiter functionality
- `test/copi_web/channels/user_socket_test.exs`: WebSocket connection rate limiting

## Security Considerations

### Limitations

1. **IP-based tracking**: Can be bypassed by users with multiple IP addresses or using proxies
2. **Shared IPs**: Users behind NAT may share rate limits
3. **No authentication**: Current implementation doesn't require user authentication

### Future Enhancements

If rate limiting proves insufficient, consider:
1. Implementing user authentication and associating limits with user accounts
2. Adding browser fingerprinting for better user identification
3. Implementing CAPTCHA for repeated violations
4. Adding IP allowlisting for trusted networks
5. Implementing more sophisticated detection patterns (behavioral analysis)

## Monitoring

The RateLimiter logs configuration on startup and warnings when limits are exceeded. Monitor these logs to:
- Detect potential attacks
- Adjust rate limits based on legitimate usage patterns
- Identify problematic IPs

## Threat Model

This implementation addresses:

- **CAPEC-212 (Functionality Misuse)**: Prevents abuse of game/player creation
- **Resource exhaustion**: Prevents overwhelming the system
- **Service availability**: Ensures legitimate users can access the service

## Contact

For security issues or questions, please refer to the main repository [SECURITY.md](../../SECURITY.md).
