# 2026-09-03 - one-off check for hero carousel source image existence
$paths = @(
'C:\Users\junip\Dropbox\Camera Uploads\FB\20240521032708__MG_1744[[]1[]]_edited*',
'C:\Users\junip\Dropbox\Camera Uploads\FB\_MG_7227[[]1[]]_edited*',
'C:\Users\junip\Dropbox\Camera Uploads\FB\_MG_7255[[]1[]]_edited*',
'C:\Users\junip\Dropbox\PICS\AFRICA\11227937_1005018492882774_6809939664731933044_o.jpg',
'C:\Users\junip\Dropbox\PICS\Instagram\_MG_3102*',
'C:\Users\junip\Dropbox\PICS\Costa Rica\FB\a.jpg',
'C:\Users\junip\Dropbox\PICS\Costa Rica\FB\_MG_1300*',
'C:\Users\junip\Dropbox\PICS\Costa Rica\cccc.png',
'C:\Users\junip\Dropbox\PICS\Indonesia 2025\_MG_9785.JPG',
'C:\Users\junip\Dropbox\PICS\AUS\PICS\Tenerife PS\_MG_3790 copy.png',
'C:\Users\junip\Dropbox\UK\Southampton\KISS - PNG - Report\Counting the number of sweet potato varieties in a very steep garden with local children and Shen, an masters student from New Guinea Binatang Research Centre.jpg',
'C:\Users\junip\Dropbox\UK\Southampton\Sweet potato garden in Sinopas.jpg',
'C:\Users\junip\Dropbox\Camera Uploads\FB\IMG_20210730_150637_262*',
'C:\Users\junip\Dropbox\Camera Uploads\FB\IMG_20210804_004137_910*',
'C:\Users\junip\Dropbox\PICS\Instagram\CostaRica2*',
'C:\Users\junip\Dropbox\PICS\Instagram\_MG_9928.JPG',
'C:\Users\junip\Dropbox\PICS\AUS\Dally\20221111_151228.jpg',
'C:\Users\junip\Dropbox\PICS\AUS\Dally\20221107_150023.jpg',
'C:\Users\junip\Dropbox\PICS\AUS\Dally\20221013_130013.jpg',
'C:\Users\junip\Dropbox\UK\Southampton\KISS - PNG - Report\Soil DNA extraction trials with beads*',
'C:\Users\junip\Dropbox\UK\Southampton\KISS - PNG - Report\Microcentrifuge and DNA extraction kit testing at the University of Southampton, pre-trip*',
'C:\Users\junip\Dropbox\PICS\Instagram\b.png',
'C:\Users\junip\Dropbox\PICS\Instagram\_MG_8572.JPG',
'C:\Users\junip\Dropbox\Camera Uploads\FB\IMG_20200111_132501_346*',
'C:\Users\junip\Dropbox\Camera Uploads\FB\IMG_20190801_071933_852*',
'C:\Users\junip\Dropbox\PICS\AUS\Perth - Oct 2022\1*',
'C:\Users\junip\Dropbox\UK\Southampton\We had great chats beside the evening fires with community leaders and farmers.jpg',
'C:\Users\junip\Dropbox\UK\View from Sinopas of an old hut with Mt Wilhelm in the background.jpg',
'C:\Users\junip\Dropbox\PICS\Instagram\_MG_8599.JPG',
'C:\Users\junip\Dropbox\UK\Southampton\KISS - PNG - Report\IMG20220102103818*',
'C:\Users\junip\Dropbox\PICS\Indonesia 2025\_MG_8524.JPG',
'C:\Users\junip\Dropbox\PICS\Indonesia 2025\_MG_9084.JPG',
'C:\Users\junip\Dropbox\PICS\Instagram\_MG_0408*',
'C:\Users\junip\Dropbox\PICS\AUS\PICS\Tenerife PS\_MG_3646 copy.png',
'C:\Users\junip\Dropbox\Camera Uploads\2025-09-02 08.50.01*',
'C:\Users\junip\Dropbox\PICS\Indonesia 2025\_MG_9232.JPG',
'C:\Users\junip\Dropbox\Camera Uploads\2025-09-06 11.20.27*',
'C:\Users\junip\Dropbox\PICS\Indonesia 2025\_MG_9519.JPG',
'C:\Users\junip\Dropbox\PICS\Indonesia 2025\_MG_9707v*',
'C:\Users\junip\Dropbox\PICS\AUS\Darwin\_MG_8125*',
'C:\Users\junip\Dropbox\PICS\AUS\PICS\Tenerife PS\_MG_3383 copy.png',
'C:\Users\junip\Dropbox\PICS\AUS\PICS\Tenerife PS\_MG_3520 copy.png',
'C:\Users\junip\Dropbox\Camera Uploads\2025-09-14 12.26.48-3.JPG'
)
$out = @()
$i = 0
foreach ($p in $paths) {
  $i++
  $found = Get-ChildItem -Path $p -File -ErrorAction SilentlyContinue
  if ($found) {
    foreach ($m in $found) { $out += "[$i] FOUND: $($m.FullName) | $([math]::Round($m.Length/1kb))KB" }
  } else {
    $out += "[$i] MISSING: $p"
  }
}
$out | Out-File -FilePath "$PSScriptRoot\carousel_sources_check.txt" -Encoding utf8
$out
