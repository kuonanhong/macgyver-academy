param(
    [switch]$Download,
    [switch]$Vision,
    [switch]$Both,
    [Parameter(ValueFromRemainingArguments=$true)][string[]]$ServerArgs
)
$ErrorActionPreference = 'Stop'
$TaskRoot = $PSScriptRoot
if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
    throw 'Install a compatible Ollama from https://ollama.com/ and start it first.'
}
& ollama list | Out-Null
if ($LASTEXITCODE -ne 0) { throw 'Start the Ollama application or run ollama serve in another terminal.' }
$env:OLLAMA_BASE_URL = 'http://127.0.0.1:11434'
$Models = @()
if (-not $Vision -or $Both) {
    $env:OLLAMA_TEXT_MODEL = if ($env:MACGYVER_MODEL) { $env:MACGYVER_MODEL } else { 'qwen3:4b' }
    $Models += $env:OLLAMA_TEXT_MODEL
}
if ($Vision -or $Both) {
    $env:OLLAMA_VISION_MODEL = if ($env:MACGYVER_VISION_MODEL) { $env:MACGYVER_VISION_MODEL } else { 'qwen3-vl:2b' }
    $Models += $env:OLLAMA_VISION_MODEL
}
foreach ($ModelName in $Models) {
    if ($ModelName -notmatch '^[a-zA-Z0-9][a-zA-Z0-9_.:/-]*$') { throw 'Invalid model name.' }
    if ($Download) {
        & ollama pull $ModelName
        if ($LASTEXITCODE -ne 0) { throw 'Model download failed; run with -Download again to resume.' }
    } else {
        & ollama show $ModelName 2>$null | Out-Null
        if ($LASTEXITCODE -ne 0) { throw "Model $ModelName is not installed. Add -Download to explicitly authorize its download." }
    }
}
Write-Host 'Use the local website shown next. Sign in to a local account to use the configured AI routes.'
& "$TaskRoot\run-local.bat" @ServerArgs
exit $LASTEXITCODE
