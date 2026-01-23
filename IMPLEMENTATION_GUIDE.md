# Rate Limiting Fresh PR - Implementation Guide

## Completed Files

1. **lib/copi/rate_limiter.ex** - GenServer for rate limiting
2. **lib/copi_web/helpers/ip_helper.ex** - Shared IP extraction helper
3. **lib/copi/application.ex** - Added RateLimiter to supervision tree
4. **config/runtime.exs** - Runtime configuration for rate limits
5. **test/copi/rate_limiter_test.exs** - Comprehensive tests
## Remaining Updates Needed

### File 1: create_game_form.ex

Add to top of file after `use CopiWeb, :live_component`:
```elixir
alias CopiWeb.Helpers.IPHelper
```

Replace the `save_game` function for `:new` action with:
```elixir
defp save_game(socket, :new, game_params) do
  # Get the IP address for rate limiting
  ip_address = IPHelper.get_connect_ip(socket)
  
  # Check rate limit before creating game
  case Copi.RateLimiter.check_rate(ip_address, :game_creation) do
    {:ok, _remaining} ->
      case Cornucopia.create_game(game_params) do
        {:ok, game} ->
          # Record the action after successful creation
          Copi.RateLimiter.record_action(ip_address, :game_creation)
          
          {:noreply,
           socket
           |> put_flash(:info, "Game created successfully")
           |> push_navigate(to: ~p"/games/#{game.id}")}

        {:error, %Ecto.Changeset{} = changeset} ->
          {:noreply, assign_form(socket, changeset)}
      end
      
    {:error, :rate_limited, retry_after} ->
      {:noreply,
       socket
       |> put_flash(
         :error,
         "Rate limit exceeded. Too many games created from your IP address. " <>
         "Please try again in #{retry_after} seconds. " <>
         "This limit helps ensure service availability for all users."
       )
       |> assign_form(socket.assigns.form.source)}
  end
end
```

### File 2: game_live/index.ex

Add to top after `use CopiWeb, :live_view`:
```elixir
alias CopiWeb.Helpers.IPHelper
```

Update `mount` function:
```elixir
@impl true
def mount(_params, _session, socket) do
  # Rate limit WebSocket connections
  ip_address = IPHelper.get_connect_ip(socket)
  
  case Copi.RateLimiter.check_rate(ip_address, :connection) do
    {:ok, _remaining} ->
      if connected?(socket) do
        Phoenix.PubSub.subscribe(Copi.PubSub, "games")
      end
      
      {:ok, assign(socket, games: list_games())}
      
    {:error, :rate_limited, retry_after} ->
      {:ok,
       socket
       |> put_flash(
         :error,
         "Rate limit exceeded. Too many connections from your IP address. " <>
         "Please try again in #{retry_after} seconds."
       )
       |> assign(games: [])}
  end
end
```

### File 3: player_live/form_component.ex

Add to top after `use CopiWeb, :live_component`:
```elixir
alias CopiWeb.Helpers.IPHelper
```

Replace `save_player` for `:new` with:
```elixir
defp save_player(socket, :new, player_params) do
  # Get the IP address for rate limiting
  ip_address = IPHelper.get_connect_ip(socket)
  
  # Check rate limit before creating player
  case Copi.RateLimiter.check_rate(ip_address, :player_creation) do
    {:ok, _remaining} ->
      case Cornucopia.create_player(player_params) do
        {:ok, player} ->
          # Record the action after successful creation
          Copi.RateLimiter.record_action(ip_address, :player_creation)

          {:ok, updated_game} = Cornucopia.Game.find(socket.assigns.player.game_id)
          CopiWeb.Endpoint.broadcast(topic(updated_game.id), "game:updated", updated_game)

          {:noreply,
           socket
           |> assign(:game, updated_game)
           |> push_navigate(to: ~p"/games/#{player.game_id}/players/#{player.id}")}

        {:error, %Ecto.Changeset{} = changeset} ->
          {:noreply, assign_form(socket, changeset)}
      end
      
    {:error, :rate_limited, retry_after} ->
      {:noreply,
       socket
       |> put_flash(
         :error,
         "Rate limit exceeded. Too many players created from your IP address. " <>
         "Please try again in #{retry_after} seconds. " <>
         "This limit helps ensure service availability for all users."
       )
       |> assign_form(socket.assigns.form.source)}
  end
end
```

### File 4: SECURITY.md

Create this file with:
```markdown
# Security Policy for Copi

## Rate Limiting

Copi implements IP-based rate limiting to protect against CAPEC-212 (Functionality Misuse) attacks and ensure service availability.

### Protected Actions

1. **Game Creation**: Limited to prevent abuse
   - Default: 10 games per IP per hour
   - Configurable via `MAX_GAMES_PER_IP` and `GAME_CREATION_WINDOW_SECONDS`

2. **Player Creation**: Separate limit from game creation
   - Default: 20 players per IP per hour
   - Configurable via `MAX_PLAYERS_PER_IP` and `PLAYER_CREATION_WINDOW_SECONDS`

3. **WebSocket Connections**: Prevents connection flooding
   - Default: 50 connections per IP per 5 minutes
   - Configurable via `MAX_CONNECTIONS_PER_IP` and `CONNECTION_WINDOW_SECONDS`

### Configuration

All limits can be adjusted via environment variables in production:

\`\`\`bash
MAX_GAMES_PER_IP=10
GAME_CREATION_WINDOW_SECONDS=3600
MAX_PLAYERS_PER_IP=20
PLAYER_CREATION_WINDOW_SECONDS=3600
MAX_CONNECTIONS_PER_IP=50
CONNECTION_WINDOW_SECONDS=300
\`\`\`

### Reporting Security Issues

If you discover a security vulnerability, please email security@owasp.org with details.
Do not create public GitHub issues for security problems.
```

## Testing

After making all updates, run:
```bash
cd copi.owasp.org
mix deps.get
mix test test/copi/rate_limiter_test.exs
```

# Committing

```bash
cd c:\Users\HUAWEI\Downloads\oswap\cornucopia-clean

git add .
git status  # Verify changes

git commit -S -m "Add IP-based rate limiting with separate limits for games/players

- Implements Copi.RateLimiter GenServer for tracking rate limits per IP
- Adds separate rate limiting for game creation, player creation, and connections
- Creates shared IPHelper module (DRY) for IP extraction
- Moves configuration to runtime.exs for proper env var handling
- Removes 'unknown' IP fallback for security
- Adds comprehensive tests and SECURITY.md documentation

Addresses feedback from PR #1920:
- Config moved to runtime.exs (@sydseter)
- Refactored duplicated get_connect_ip/1 (@sydseter)
- Removed 'unknown' IP security issue (@sydseter)
- All commits GPG signed and verified (@sydseter)

Fixes #1877"
```

# Pushing & Creating PR

```bash
git push myfork feat/rate-limiting-clean

# Then go to GitHub and create PR:
# - Base: OWASP:master
# - Head: immortal71:feat/rate-limiting-clean
# - Title: Add IP-based rate limiting for Copi (fixes #1877)
# - In description, mention: "Supersedes #1920"
```

