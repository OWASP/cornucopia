# Complete Rate Limiting Implementation Script
# Run this after the core files have been created

Write-Host "Setting up rate limiting for LiveView files..." -ForegroundColor Green

# The following files still need to be updated with rate limiting:
# 1. copi.owasp.org/lib/copi_web/live/game_live/create_game_form.ex
# 2. copi.owasp.org/lib/copi_web/live/game_live/index.ex
# 3. copi.owasp.org/lib/copi_web/live/player_live/form_component.ex
# 4. copi.owasp.org/SECURITY.md

Write-Host "`nCore files created:" -ForegroundColor Cyan
Write-Host "✓ lib/copi/rate_limiter.ex" -ForegroundColor Green
Write-Host "✓ lib/copi_web/helpers/ip_helper.ex" -ForegroundColor Green
Write-Host "✓ lib/copi/application.ex (updated)" -ForegroundColor Green
Write-Host "✓ config/runtime.exs (updated)" -ForegroundColor Green
Write-Host "✓ test/copi/rate_limiter_test.exs" -ForegroundColor Green

Write-Host "`nNext steps to complete:" -ForegroundColor Yellow
Write-Host "1. Update create_game_form.ex to add game creation rate limiting"
Write-Host "2. Update index.ex to add connection rate limiting"
Write-Host "3. Update form_component.ex to add player creation rate limiting"
Write-Host "4. Create/update SECURITY.md with rate limiting documentation"
Write-Host "5. Run tests: cd copi.owasp.org && mix test"
Write-Host "6. Commit changes with signed commit"
Write-Host "7. Push to your fork and create PR"

Write-Host "`nWould you like me to generate the remaining file updates? (Y/N)" -ForegroundColor Cyan
