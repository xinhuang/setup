param(
  [switch]$install
)

function Try-ImportModule($module, [ScriptBlock]$onError) {
  try {
    Import-Module $module -ErrorAction Stop
  } catch {
    & $onError
    Import-Module $module
  } 
}

Try-ImportModule 'PsGet' -OnError {
  (new-object Net.WebClient).DownloadString("http://psget.net/GetPsGet.ps1") | iex 
}

Try-ImportModule 'PsReadLine' -OnError {
  Install-Module PsReadLine
}

function prompt
{
  $_locationStackDepthString = New-Object string ([char] '+'), (Get-Location -Stack).Count

  $color = 'Yellow'

  Write-Host '>> ' -nonewline -ForegroundColor $color
  Write-Host $(Get-Date -Format T) -ForegroundColor 'Green' -NoNewLine
  Write-Host " " $PWD.Path -ForegroundColor 'Cyan'
  Write-Host ($_locationStackDepthString + '>') -nonewline -ForegroundColor $color

  return " "
}

function Write-Callstack([System.Management.Automation.ErrorRecord]$ErrorRecord=$null, [int]$Skip=1) {
    Write-Host # blank line
    if ($ErrorRecord) {
        Write-Host -ForegroundColor Red "$ErrorRecord $($ErrorRecord.InvocationInfo.PositionMessage)"

        if ($ErrorRecord.Exception) {
            Write-Host -ForegroundColor Red $ErrorRecord.Exception
        }

        if ((Get-Member -InputObject $ErrorRecord -Name ScriptStackTrace) -ne $null) {
            #PS 3.0 has a stack trace on the ErrorRecord; if we have it, use it & skip the manual stack trace below
            Write-Host -ForegroundColor Red $ErrorRecord.ScriptStackTrace
            return
        }
    }

    Get-PSCallStack | Select -Skip $Skip | % {
        Write-Host -ForegroundColor Yellow -NoNewLine "! "
        Write-Host -ForegroundColor Red $_.Command $_.Location $(if ($_.Arguments.Length -le 80) { $_.Arguments })
    }
}

try {
    if ($install) {
      if ($PsVersionTable.PsVersion.Major -lt 4) {
        Write-Error "This runtime config file requires PowerShell minimum version 4.0."
        return
      }
      $thisFile = $MyInvocation.MyCommand.Path
      $sourceMeLine = ". $thisFile"
      if (Test-Path $profile -PathType Leaf) {
        $sourcedMe = Get-Content $profile | % { $_.Trim() } | ? { $_ -eq $sourceMeLine }
      } else {
        $sourcedMe = $False
      }
      if (-Not $sourcedMe) {
        "`n$sourceMeLine`n" | Out-File $profile -Append
      }
      iex $sourceMeLine
    }
} catch {
    Write-Callstack $Error[0]
    Write-Callstack $Error[0]
}