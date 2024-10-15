$filegroups = get-childitem api | group-object { ($_.Name -split '\?view=')[0] }
$priority = @(
  'net-9.0.html',
  'net-8.0.html',
  'netstandard-2.0.html',
  'netcore-3.1.html',
  'netcore-2.0.html',
  'netcore-1.1.html',
  'netframework-4.8.1.html',
  'netframework-3.5.html',
  'netframework-1.1.html',
  'dotnet-uwp-10.0.html',
  'windowsdesktop-8.0.html'
)
$filegroups | Where { $_.Count -gt 1 } | % { $_.Group | Sort-Object -Property {$priority.IndexOf(($_.Name -split '\?view=')[1])} | Select -Skip 1 } | Remove-Item
