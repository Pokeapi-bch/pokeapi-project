# .githooks/pre-commit.ps1

Write-Host "Running pre-commit checks..."

# --- 1. Ejecutar el hook personalizado de cadenas prohibidas ---
Write-Host "Running custom forbidden string checks..."
# Usamos '& "$PSScriptRoot\..."' para asegurar que el script se ejecute
# correctamente sin importar el directorio actual, ya que '$PSScriptRoot'
# apunta a la carpeta donde se encuentra este script (githooks/).
& "$PSScriptRoot\check-forbidden-strings.ps1"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Custom forbidden strings check FAILED. Aborting commit." -ForegroundColor Red
    exit 1 # Fallar el hook principal si el script personalizado falla
}

# --- 2. Ejecutar el framework pre-commit (que maneja los hooks de .pre-commit-config.yaml) ---
Write-Host "Running pre-commit framework checks..."
# Verificamos si 'pre-commit' está instalado antes de intentar ejecutarlo
if (Get-Command pre-commit -ErrorAction SilentlyContinue) {
    pre-commit run --all-files
    # '$LASTEXITCODE' contiene el código de salida del último comando ejecutado.
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Pre-commit framework checks FAILED. Aborting commit." -ForegroundColor Red
        exit 1 # Fallar el hook principal si el framework pre-commit falla
    }
} else {
    Write-Host "Warning: 'pre-commit' framework is not installed. Skipping its checks." -ForegroundColor Yellow
    # Este mensaje es solo una advertencia, no detiene el hook principal si no está instalado.
    # Pero 'pre-commit' sí debería estar instalado en CI y localmente para que todo funcione.
}

# Si todos los checks anteriores pasaron sin exit 1, entonces este hook principal pasa
Write-Host "All pre-commit checks PASSED." -ForegroundColor Green
exit 0 # Salida exitosa del hook
