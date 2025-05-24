# Example prepare-commit-msg hook script in PowerShell
Write-Host "Running prepare-commit-msg hook..."

# Example: Add a prefix to commit message (customize as needed)
param(
    [string]$commitMsgFile
)

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
