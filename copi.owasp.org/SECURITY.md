# Security Policy for Copi

## Rate Limiting

Copi implements IP-based rate limiting to protect against CAPEC-212 (Functionality Misuse) attacks and ensure service availability.

## Protected Actions

1. **Game Creation**: Limited to prevent abuse
   - Default: 10 games per IP per hour
   - Configurable via `MAX_GAMES_PER_IP` and `GAME_CREATION_WINDOW_SECONDS`

2. **Player Creation**: Separate limit from game creation
   - Default: 20 players per IP per hour
   - Configurable via `MAX_PLAYERS_PER_IP` and `PLAYER_CREATION_WINDOW_SECONDS`

3. **WebSocket Connections**: Prevents connection flooding
   - Default: 50 connections per IP per 5 minutes
   - Configurable via `MAX_CONNECTIONS_PER_IP` and `CONNECTION_WINDOW_SECONDS`

## Configuration

All limits can be adjusted via environment variables in production:

```bash
MAX_GAMES_PER_IP=10
GAME_CREATION_WINDOW_SECONDS=3600
MAX_PLAYERS_PER_IP=20
PLAYER_CREATION_WINDOW_SECONDS=3600
MAX_CONNECTIONS_PER_IP=50
CONNECTION_WINDOW_SECONDS=300
```

### Reporting Security Issues

If you discover a security vulnerability, please email security@owasp.org with details.
Do not create public GitHub issues for security problems. '-'
