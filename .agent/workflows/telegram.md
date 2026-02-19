---
description: Check Telegram inbox and reply via outbox
---

// turbo-all

## Check Telegram Messages

1. Read all inbox messages:
```
Get-ChildItem "d:\Antigravity Telegram Bot\bridge\inbox\*.json" | Sort-Object Name | ForEach-Object { Write-Host "--- $($_.Name) ---"; Get-Content $_.FullName; Write-Host "" }
```

2. After reading, process each message and write your response:
```
Set-Content -Path "d:\Antigravity Telegram Bot\bridge\outbox\response.txt" -Value "YOUR RESPONSE HERE"
```

3. The bot will automatically pick up the response file, send it to Telegram, and delete it.

4. Clean up processed inbox messages:
```
Remove-Item "d:\Antigravity Telegram Bot\bridge\inbox\*.json"
```
