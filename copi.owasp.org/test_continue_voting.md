# Continue Voting Implementation Test

## Overview
This document tests the "Vote to Continue" functionality implementation for OWASP Cornucopia.

## Implementation Summary

### 1. Database Changes
- Added `round_open` field to games table (default: true)
- Created continue_votes table to track player votes to continue rounds

### 2. Backend Logic
- Added continue voting helper functions to Game module:
  - `continue_vote_count/1` - Count continue votes
  - `has_continue_vote?/2` - Check if player voted
  - `majority_continue_votes_reached?/1` - Check if majority voted
  - `can_continue_round?/1` - Check if round can be continued

### 3. Frontend Changes
- Added "Vote to Continue" button in player live view
- Shows vote count and required votes
- Updates button state based on voting status
- Added continue voting status to game live view for spectators

### 4. Event Handling
- Added `toggle_continue_vote` event handler
- Modified `next_round` to check for continue votes
- Added delayed round progression when continue votes reach majority

## Test Scenarios

### Scenario 1: Normal Game Flow
1. Game starts with `round_open: true`
2. Players play cards normally
3. When all players play, `round_open?` returns false
4. "Next Round" button becomes enabled
5. Continue voting is not needed

### Scenario 2: Player Disconnects
1. Game in progress, one player hasn't played their card
2. `round_open?` returns true (some players still to play)
3. "Vote to Continue" button appears
4. Other players can vote to continue
5. When majority votes, "Next Round" button becomes enabled
6. Round proceeds without disconnected player

### Scenario 3: Continue Voting Process
1. 4 players in game, need 3 votes to continue (majority)
2. Player 1 votes: "Vote to Continue" (1/3 votes)
3. Player 2 votes: "Vote to Continue" (2/3 votes)
4. Player 3 votes: "Voted to Continue" (3/3 votes - majority reached)
5. "Next Round" button becomes enabled
6. Any player can click "Next Round" to proceed

### Scenario 4: Vote Toggling
1. Player votes to continue
2. Button shows "Voted to Continue" with amber color
3. Player clicks again to remove vote
4. Button shows "Vote to Continue" with gray color
5. Vote count decreases

## Expected Behavior

### For Players:
- "Vote to Continue" button appears when round is open
- Button shows current vote count vs required votes
- Button state changes based on player's vote status
- "Next Round" button enabled when majority continue votes reached

### For Spectators:
- Can see continue vote count in round information
- No voting capability (view-only)

### For Game State:
- `round_open` field tracks if round is open/closed
- Continue votes are tracked per player per game
- Round progression respects continue voting when needed

## Files Modified

1. **Database Migrations:**
   - `20260206100557_add_round_open_to_games.exs`
   - `20260206100558_create_continue_votes.exs`

2. **Backend Models:**
   - `lib/copi/cornucopia/game.ex` - Added round_open field and continue voting functions
   - `lib/copi/cornucopia/continue_vote.ex` - New continue vote schema

3. **Frontend Components:**
   - `lib/copi_web/live/player_live/show.ex` - Added continue voting event handlers
   - `lib/copi_web/live/player_live/show.html.heex` - Added "Vote to Continue" button
   - `lib/copi_web/live/game_live/show.html.heex` - Added continue vote status for spectators

## Validation

The implementation follows these principles:
1. **Majority Rule**: Requires more than half of players to vote to continue
2. **One Vote Per Player**: Each player can vote only once per game
3. **Graceful Degradation**: Normal gameplay unaffected when all players are present
4. **Clear UI Feedback**: Players see vote status and progress
5. **Spectator Awareness**: Observers can see continue voting status

This implementation solves the original problem where games get stuck when players disconnect, while maintaining the integrity of the game's voting mechanics.