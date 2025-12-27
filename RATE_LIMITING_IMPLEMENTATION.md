# Rate Limiting Implementation for Player Creation

## Overview
This implementation addresses GitHub Issue #1877 by adding IP-based rate limiting for player creation, separate from the existing game creation rate limit, to protect against CAPEC 212 (Functionality Misuse) attacks.

## Changes Made

### 1. Rate Limiter Module (`lib/copi/rate_limiter.ex`)

**Added player_creation action:**
- Updated `check_rate/2` to accept `:player_creation` action
- Updated `record_action/2` to accept `:player_creation` action
- Added player creation configuration with default limits:
  - Maximum players per IP: 20
  - Time window: 3600 seconds (1 hour)

**Configuration:**
```elixir
player_creation: %{
  max_requests: get_env(:max_players_per_ip, 20),
  window_seconds: get_env(:player_creation_window_seconds, 3600)
}
```

### 2. Player Form Component (`lib/copi_web/live/player_live/form_component.ex`)

**Added rate limiting to player creation:**
- Added `get_connect_ip/1` helper function to extract IP address from socket
- Modified `save_player/3` for `:new` action to:
  1. Get the connecting IP address
  2. Check rate limit before creating player
  3. Only create player if rate limit is not exceeded
  4. Record the action after successful creation
  5. Display user-friendly error message if rate limited

**Error message shown to users:**
```
"Rate limit exceeded. Too many players created from your IP address. 
Please try again in X seconds. This limit helps ensure service 
availability for all users."
```

### 3. Tests (`test/copi/rate_limiter_test.exs`)

**Added comprehensive test coverage:**
- Test that player creation is allowed under the limit
- Test that player creation is blocked when limit is exceeded
- Test that player creation limit is separate from game creation limit
- Updated configuration test to verify player_creation config exists

## Key Features

### Separate Limits
The player creation rate limit is maintained **separately** from the game creation rate limit. This means:
- An IP that has exhausted its game creation quota can still create players
- An IP that has exhausted its player creation quota can still create games
- Each limit is tracked independently in the GenServer state

### Configurable Limits
The limits can be configured via application environment:
```elixir
config :copi, Copi.RateLimiter,
  max_players_per_ip: 20,
  player_creation_window_seconds: 3600
```

### User-Friendly Error Handling
When rate limited, users receive:
- Clear explanation of why they were blocked
- Time until they can try again (retry_after in seconds)
- Explanation that this protects service availability

## Security Benefits

1. **CAPEC 212 Mitigation**: Prevents functionality misuse by limiting the rate of player creation from a single IP
2. **DoS Protection**: Helps maintain service availability under attack
3. **Resource Conservation**: Prevents database and system resource exhaustion
4. **Granular Control**: Separate limits allow fine-tuned protection for different actions

## Default Limits Summary

| Action | Max Requests | Time Window |
|--------|--------------|-------------|
| Game Creation | 10 | 1 hour |
| Player Creation | 20 | 1 hour |
| Connection | 50 | 5 minutes |

## Testing

Run the test suite:
```bash
mix test test/copi/rate_limiter_test.exs
```

All tests should pass, including the new player creation rate limiting tests.

## Future Enhancements

As mentioned in the issue, if this is still insufficient, the next step would be:
- Implement authentication
- Associate rate limits with user accounts in addition to IP addresses
- Track browser fingerprints along with IP addresses

---

**Issue Reference:** OWASP/cornucopia#1877  
**Related Security Control:** CAPEC-212 (Functionality Misuse)  
**Implemented by:** @immortal71
