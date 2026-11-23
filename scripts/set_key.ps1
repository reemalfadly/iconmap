# iconMap: save your ElevenLabs API key once, without showing it and without typing it in a chat.
# Run in a terminal:  powershell -ExecutionPolicy Bypass -File set_key.ps1
# The key is stored only on this computer in  %USERPROFILE%\.iconmap\elevenlabs.key  (never inside a project folder).
$dir = Join-Path $env:USERPROFILE ".iconmap"
New-Item -ItemType Directory -Force $dir | Out-Null
$sec = Read-Host "ElevenLabs API key (hidden)" -AsSecureString
$bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($sec)
$key = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr)
[Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)
if (-not $key -or $key.Length -lt 10) { Write-Host "No key saved."; exit 1 }
[IO.File]::WriteAllText((Join-Path $dir "elevenlabs.key"), $key.Trim(), (New-Object Text.UTF8Encoding($false)))
icacls (Join-Path $dir "elevenlabs.key") /inheritance:r /grant:r "$($env:USERNAME):(R,W)" | Out-Null
Write-Host "Saved. Test: python scripts\eleven.py voices --language ar"
