# Start billion-context (bili) proxy in a supervised way.
#
# Background:
#   - billion-context 0.1.195 lives at $BILI_HOME (see below).
#   - The running DSH Desktop instance was started by the Electron app WITHOUT
#     BILLION_CONTEXT_PROXY in its environment, so its bili-acp plugin never
#     registers the compress/decompress/search_context/acp_status tools.
#   - Registering those tools requires the *host* process to be launched by
#     `bili dsh`. An already-running host cannot be retro-fitted.
#   - This script therefore starts the proxy itself, so the WEB UI, /__bili/*
#     endpoints and /acp-cache style reports become reachable immediately, and
#     prints the exact command to launch a bili-managed dsh host.

[CmdletBinding()]
param(
  [int]$Port = 8788,
  [string]$BindHost = '127.0.0.1',
  [switch]$Restart,
  [switch]$EnableAutoStart,
  [switch]$RemoveAutoStart,
  [switch]$Status
)

$ErrorActionPreference = 'Stop'

$BiliHome = 'C:\Users\Administrator\AppData\Roaming\dsh-desktop\harness\profiles\.generations\live\billion-context+0.1.195+fca8e318722e\node_modules\billion-context'
$BiliEntry = Join-Path $BiliHome 'dist\index.js'
$BiliConfig = Join-Path $env:USERPROFILE '.config\billion-context\billion-context.json'
$ProxyPorts = @(18792, 18787, 8788, 18793, 18794, 18795)
$LogDir = Join-Path $env:USERPROFILE '.local\share\billion-context'
$LogFile = Join-Path $env:USERPROFILE '.local\share\billion-context\proxy.out.log'
$ErrFile = Join-Path $env:USERPROFILE '.local\share\billion-context\proxy.err.log'

# Node runtime used by DSH Desktop. Fall back to bundled node.exe.
$NodeCandidates = @(
  'C:\Users\Administrator\.workbuddy-ai\binaries\node\versions\22.22.2-6\node.exe',
  'C:\Program Files\DSH Desktop\resources\app.asar.unpacked\node_modules\node\bin\node.exe'
)
$Node = $NodeCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $Node) { throw "No usable node.exe found. Tried: $($NodeCandidates -join '; ')" }

$StartupDir = Join-Path $env:APPDATA 'Microsoft\Windows\Start Menu\Programs\Startup'
$ShortcutPath = Join-Path $StartupDir 'billion-context-proxy.lnk'

function Get-BiliProcess {
  Get-CimInstance Win32_Process -Filter "Name='node.exe'" -ErrorAction SilentlyContinue |
    Where-Object { $_.CommandLine -and $_.CommandLine -match 'billion-context.*dist[\\/]index\.js' }
}

function Get-Listening($p) {
  Get-NetTCPConnection -State Listen -LocalPort $p -ErrorAction SilentlyContinue
}

function Ensure-Config {
  $dir = Split-Path $BiliConfig -Parent
  if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
  if (-not (Test-Path $BiliConfig)) {
    @{ port = $Port; host = $BindHost; providers = @{} } | ConvertTo-Json -Depth 6 | Set-Content $BiliConfig -Encoding UTF8
    Write-Host "[bili] wrote default config -> $BiliConfig"
    return
  }
  try { $cfg = Get-Content $BiliConfig -Raw | ConvertFrom-Json } catch { $cfg = $null }
  if ($null -eq $cfg) {
    @{ port = $Port; host = $BindHost; providers = @{} } | ConvertTo-Json -Depth 6 | Set-Content $BiliConfig -Encoding UTF8
    Write-Host "[bili] config was unparsable, rewrote -> $BiliConfig"
    return
  }
  $changed = $false
  if ($null -eq $cfg.port) { $cfg | Add-Member -NotePropertyName port -NotePropertyValue $Port -Force; $changed = $true }
  if ($null -eq $cfg.host) { $cfg | Add-Member -NotePropertyName host -NotePropertyValue $BindHost -Force; $changed = $true }
  if ($null -eq $cfg.providers) { $cfg | Add-Member -NotePropertyName providers -NotePropertyValue @{} -Force; $changed = $true }
  if ($changed) {
    $cfg | ConvertTo-Json -Depth 10 | Set-Content $BiliConfig -Encoding UTF8
    Write-Host "[bili] normalised config -> $BiliConfig"
  }
}

function Show-Status {
  Write-Host "== node        : $Node"
  Write-Host "== bili entry  : $BiliEntry  (exists: $(Test-Path $BiliEntry))"
  Write-Host "== config      : $BiliConfig"
  if (Test-Path $BiliConfig) { Write-Host "   content    : $((Get-Content $BiliConfig -Raw).Trim())" }
  $procs = Get-BiliProcess
  if ($procs) {
    foreach ($p in $procs) { Write-Host "== proxy pid   : $($p.ProcessId)" }
  } else {
    Write-Host "== proxy pid   : (none running)"
  }
  # Probe every candidate lane port. A lane port is whatever the running
  # process actually LISTENs on - command-line --port may lie (lane drift).
  $live = @()
  foreach ($p in $ProxyPorts) {
    $l = Get-Listening $p
    if (-not $l) { continue }
    $ownerPid = $l[0].OwningProcess
    $owner = (Get-Process -Id $ownerPid -ErrorAction SilentlyContinue).ProcessName
    try {
      $r = Invoke-WebRequest -Uri "http://127.0.0.1:$p/__bili/plugin/manifest" -TimeoutSec 3 -UseBasicParsing
      $j = $r.Content | ConvertFrom-Json
      Write-Host "== port $p     : LISTEN pid $ownerPid ($owner) -> bili v$($j.version) ALIVE"
      Write-Host "   tools      : $($j.toolNames -join ', ')"
      Write-Host "   web UI     : http://127.0.0.1:$p"
      $live += [pscustomobject]@{ Port = $p; Pid = $ownerPid; Version = $j.version; Tools = $j.toolNames }
    } catch {
      Write-Host "== port $p     : LISTEN pid $ownerPid ($owner) but NOT bili"
    }
  }
  if (-not $live) { Write-Host "== port probe  : no live bili lane found on $($ProxyPorts -join ', ')" }
  Write-Host ''
  Write-Host "== this session: $env:DSH_SESSION_ID"
  foreach ($x in $live) {
    try {
      $u = "http://127.0.0.1:$($x.Port)/__bili/plugin/status?conversationId=$env:DSH_SESSION_ID"
      $s = (Invoke-WebRequest -Uri $u -TimeoutSec 4 -UseBasicParsing).Content | ConvertFrom-Json
      $match = ($s.sessionId -eq $env:DSH_SESSION_ID)
      $verdict = if ($match) { '(MATCH: this session is proxied)' } else { '(not this session)' }
      Write-Host "   [$($x.Port)] conversationId -> $($s.sessionId)  $verdict"
      Write-Host "        model=$($s.model) ctx=$($s.contextTokens)/$($s.contextLimit) source=$($s.contextTokensSource) reqs=$($s.requests)"
    } catch { }
  }
  Write-Host ''
  Write-Host "== to register ACP tools in a NEW host: run  bili dsh --profile web"
  if (Test-Path $ShortcutPath) { Write-Host "== autostart   : ENABLED ($ShortcutPath)" } else { Write-Host "== autostart   : disabled" }
}

function Stop-Bili {
  $procs = Get-BiliProcess
  foreach ($p in $procs) {
    Write-Host "[bili] stopping pid $($p.ProcessId)"
    Stop-Process -Id $p.ProcessId -Force -ErrorAction SilentlyContinue
  }
  Start-Sleep -Milliseconds 800
}

function Start-Bili {
  if (-not (Test-Path $BiliEntry)) { throw "bili entry missing: $BiliEntry" }
  if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Force -Path $LogDir | Out-Null }

  # Refuse to fight over the port with another listener that is not bili.
  $existing = Get-Listening $Port
  if ($existing) {
    $ownerPid = $existing[0].OwningProcess
    $owner = Get-Process -Id $ownerPid -ErrorAction SilentlyContinue
    $isBili = (Get-BiliProcess | Where-Object { $_.ProcessId -eq $ownerPid })
    if (-not $isBili) {
      throw "Port $Port is held by pid $ownerPid ($($owner.ProcessName)), not by a bili proxy. Pick another -Port (e.g. -Port 8789)."
    }
    Write-Host "[bili] port $Port already served by bili pid $ownerPid; nothing to do."
    return
  }

  $args = @($BiliEntry, '--port', "$Port", '--host', $BindHost)
  Write-Host "[bili] launching: `"$Node`" $($args -join ' ')"
  $p = Start-Process -FilePath $Node -ArgumentList $args `
    -RedirectStandardOutput $LogFile -RedirectStandardError $ErrFile `
    -WindowStyle Hidden -PassThru
  Write-Host "[bili] pid $($p.Id), logs: $LogFile"

  for ($i = 0; $i -lt 40; $i++) {
    Start-Sleep -Milliseconds 500
    try {
      $r = Invoke-WebRequest -Uri "http://127.0.0.1:$Port/__bili/plugin/manifest" -TimeoutSec 2 -UseBasicParsing
      if ($r.StatusCode -eq 200) {
        $j = $r.Content | ConvertFrom-Json
        Write-Host "[bili] UP after $([math]::Round(($i + 1) * 0.5, 1))s - version $($j.version)"
        Write-Host "[bili] web UI : http://127.0.0.1:$Port"
        Write-Host "[bili] status : http://127.0.0.1:$Port/__bili/status"
        return
      }
    } catch { }
  }
  Write-Host "[bili] WARNING: proxy process started but /__bili/plugin/manifest never answered."
  Write-Host "[bili] tail of stderr:"
  if (Test-Path $ErrFile) { Get-Content $ErrFile -Tail 30 | Write-Host }
  Write-Host "[bili] tail of stdout:"
  if (Test-Path $LogFile) { Get-Content $LogFile -Tail 30 | Write-Host }
}

function Enable-AutoStart {
  $ws = New-Object -ComObject WScript.Shell
  $sc = $ws.CreateShortcut($ShortcutPath)
  $sc.TargetPath = 'powershell.exe'
  $sc.Arguments = "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$PSCommandPath`" -Port $Port > `"$LogDir\autostart.log`" 2>&1"
  $sc.WorkingDirectory = $env:USERPROFILE
  $sc.WindowStyle = 7
  $sc.Save()
  Write-Host "[bili] autostart shortcut created: $ShortcutPath"
}

function Remove-AutoStart {
  if (Test-Path $ShortcutPath) { Remove-Item $ShortcutPath -Force; Write-Host "[bili] autostart shortcut removed." }
  else { Write-Host "[bili] no autostart shortcut present." }
}

if ($RemoveAutoStart) { Remove-AutoStart; exit 0 }
if ($Status) { Show-Status; exit 0 }

Ensure-Config
if ($Restart) { Stop-Bili }
Start-Bili
if ($EnableAutoStart) { Enable-AutoStart }
Write-Host ''
Show-Status


