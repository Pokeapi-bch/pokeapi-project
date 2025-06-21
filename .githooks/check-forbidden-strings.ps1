# Define las cadenas de texto prohibidas y si se requiere un patrón de ticket.
# Por ejemplo, 'TODO:' debe ir seguido de un numero (ej: TODO: #123)
# Si no quieres que requiera un ticket, simplemente usa 'FIXME'
$ForbiddenStrings = @(
    @{ String = "TODO:"; RequiresTicket = $true; TicketPattern = "#\d+" }, # Requiere un '#número'
    @{ String = "FIXME"; RequiresTicket = $false },                        # No requiere ticket, solo no debe estar
    @{ String = "DEBUG_PRINT"; RequiresTicket = $false }                 # Ejemplo de cadena a evitar
)

# Define los tipos de archivo a escanear (separados por | )
$FilePatterns = "*.py" # Solo archivos Python. Añade |*.html si también quieres HTML.

$ErrorFound = $false
$FilesToScan = @(Get-ChildItem -Recurse -Path . -Include $FilePatterns | Select-Object -ExpandProperty FullName)

Write-Host "Running custom forbidden string checks..."

foreach ($file in $FilesToScan) {
    $fileContent = Get-Content $file -Raw
    $relativeFilePath = $file.Replace($PSScriptRoot, ".")

    foreach ($forbidden in $ForbiddenStrings) {
        $stringToFind = $forbidden.String
        $requiresTicket = $forbidden.RequiresTicket
        $ticketPattern = $forbidden.TicketPattern

        # Escanear por la cadena prohibida
        $matches = [regex]::Matches($fileContent, [regex]::Escape($stringToFind))
        foreach ($match in $matches) {
            $lineNum = ($fileContent.Substring(0, $match.Index).Split([char]10)).Count
            $context = $fileContent.Substring($match.Index, [System.Math]::Min(50, $fileContent.Length - $match.Index))

            if ($requiresTicket) {
                $hasTicket = $false
                if ($match.Index + $match.Length -1 -lt $fileContent.Length) {
                    # Busca el patrón del ticket justo después de la cadena prohibida en la misma línea
                    $lineEndIndex = $fileContent.IndexOf([char]10, $match.Index)
                    if ($lineEndIndex -eq -1) { $lineEndIndex = $fileContent.Length }
                    $lineContent = $fileContent.Substring($match.Index, $lineEndIndex - $match.Index)
                    if ($lineContent -match "$([regex]::Escape($stringToFind))\s*$ticketPattern") {
                        $hasTicket = $true
                    }
                }
                if (-not $hasTicket) {
                    Write-Host "ERROR: Found forbidden string '$stringToFind' without required ticket in $relativeFilePath at line $lineNum. Context: '$context...'" -ForegroundColor Red
                    $ErrorFound = $true
                }
            } else {
                Write-Host "ERROR: Found forbidden string '$stringToFind' in $relativeFilePath at line $lineNum. Context: '$context...'" -ForegroundColor Red
                $ErrorFound = $true
            }
        }
    }
}

if ($ErrorFound) {
    Write-Host "Custom forbidden string check FAILED." -ForegroundColor Red
    exit 1 # Fallar el hook
} else {
    Write-Host "Custom forbidden string check PASSED." -ForegroundColor Green
    exit 0
}
