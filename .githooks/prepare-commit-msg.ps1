param(
    [string]$commitMsgFile
)

Write-Host "Running prepare-commit-msg hook..."

if (Test-Path $commitMsgFile) {
    $content = Get-Content $commitMsgFile
    if (-not $content.StartsWith("[PokeAPI]")) {
        "[PokeAPI] " + $content | Set-Content $commitMsgFile
        Write-Host "Commit message prefix added."
    } else {
        Write-Host "Commit message already has prefix."
    }
} else {
    Write-Host "Commit message file not found."
}

exit 0
