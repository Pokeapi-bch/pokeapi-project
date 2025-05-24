# Example pre-commit hook script in PowerShell
Write-Host "Running pre-commit checks..."

# Run pre-commit framework if installed
if (Get-Command pre-commit -ErrorAction SilentlyContinue) {
    pre-commit run --all-files
} else {
    Write-Host "pre-commit not installed, skipping."
}

# Add any additional pre-commit checks here

exit 0
