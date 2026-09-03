# Downloads the raw HTML of every Wix blog post listed in wix_posts.csv.
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$rawDir = Join-Path $PSScriptRoot 'raw'
New-Item -ItemType Directory -Force -Path $rawDir | Out-Null

$posts = Import-Csv (Join-Path $PSScriptRoot 'wix_posts.csv')
foreach ($p in $posts) {
    $out = Join-Path $rawDir "$($p.slug).html"
    if ((Test-Path $out) -and ((Get-Item $out).Length -gt 50000)) {
        Write-Host "SKIP $($p.slug)"
        continue
    }
    try {
        Invoke-WebRequest "https://www.juniperkiss.com/post/$($p.slug)" -UseBasicParsing -TimeoutSec 120 -OutFile $out
        Write-Host "OK   $($p.slug)"
    }
    catch {
        Write-Host "FAIL $($p.slug): $($_.Exception.Message)"
    }
}
