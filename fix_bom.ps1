$path = 'C:\Users\KIIT\cornucopia\copi.owasp.org\test\copi_web\live\player_live\show_test.exs'
$content = Get-Content $path -Raw
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText($path, $content, $utf8NoBom)
Write-Host "Done! BOM removed."