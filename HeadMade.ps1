$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
wt.exe cmd /c "`"$scriptDir\HeadMade.bat`""
