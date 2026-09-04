$patterns = @(
  'IMG-20260424-WA0003', '_MG_0401', '_MG_0579', 'IMG-20241102-WA0006', '_MG_6139', 'IMG_3186',
  '_MG_6262', '_MG_7097', '_MG_6261', '_MG_3537', '496924556_', '_MG_1950B', '_MG_1300', '_MG_9837',
  '52905704_', 'PhenomePoster', 'IMG_8212', 'IMG_8071', '650050993_', 'lucidpress', '20170712_111415',
  '143417', '2020-03-01 10.08.31', '2020-02-26 09.02.31', '20150802_220021', 'Greenhouse', 'BSB'
)

$roots = @('C:\Users\junip\Dropbox', 'C:\Users\junip\Downloads')
$found = New-Object System.Collections.Generic.List[string]
$stack = New-Object System.Collections.Generic.Stack[string]
foreach ($r in $roots) { $stack.Push($r) }

while ($stack.Count -gt 0) {
    $dir = $stack.Pop()
    try {
        foreach ($f in [System.IO.Directory]::EnumerateFiles($dir)) {
            $n = [System.IO.Path]::GetFileName($f)
            foreach ($p in $patterns) {
                if ($n -like "*$p*") { $found.Add($f); break }
            }
        }
    }
    catch {}
    try {
        foreach ($d in [System.IO.Directory]::EnumerateDirectories($dir)) { $stack.Push($d) }
    }
    catch {}
}

$found | Sort-Object
Write-Output "---- TOTAL: $($found.Count)"
