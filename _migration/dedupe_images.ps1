$targets = @(
  '_MG_6139', '_MG_6261', '_MG_6262', '_MG_7097', '_MG_3537', '_MG_1300', '_MG_9837',
  'IMG_3186', 'IMG_8071', 'IMG_8212', '20150802_220021'
)

$roots = @('C:\Users\junip\Dropbox', 'C:\Users\junip\Downloads')
$stack = New-Object System.Collections.Generic.Stack[string]
foreach ($r in $roots) { $stack.Push($r) }
$rows = New-Object System.Collections.Generic.List[object]

while ($stack.Count -gt 0) {
    $dir = $stack.Pop()
    try {
        foreach ($f in [System.IO.Directory]::EnumerateFiles($dir)) {
            $n = [System.IO.Path]::GetFileName($f)
            foreach ($t in $targets) {
                if ($n -like "*$t*") {
                    $fi = New-Object System.IO.FileInfo $f
                    $rows.Add([pscustomobject]@{
                            Key   = $t
                            Size  = $fi.Length
                            Taken = $fi.LastWriteTime.ToString('yyyy-MM-dd')
                            Path  = $f
                        })
                    break
                }
            }
        }
    }
    catch {}
    try { foreach ($d in [System.IO.Directory]::EnumerateDirectories($dir)) { $stack.Push($d) } } catch {}
}

$rows | Sort-Object Key, Size | Group-Object Key | ForEach-Object {
    Write-Output "=== $($_.Name) : $(($_.Group | Select-Object -ExpandProperty Size -Unique).Count) distinct size(s) ==="
    $_.Group | Group-Object Size | ForEach-Object {
        $first = $_.Group[0]
        Write-Output ("  [{0} bytes | {1}] x{2}  ->  {3}" -f $first.Size, $first.Taken, $_.Count, $first.Path)
    }
}
