# Example pre-push hook script in PowerShell
Write-Host "Running pre-push checks..."

# Example: Run tests before push (customize as needed)
if (Get-Command pytest -ErrorAction SilentlyContinue) {
    pytest
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Tests failed. Aborting push."
        exit 1
    } else {
        Write-Host "Tests passed."
    }
} else {
    Write-Host "pytest not installed, skipping tests."
}

exit 0
