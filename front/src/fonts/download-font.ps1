# PowerShell script to download Monigue DEMO font
# Run this script: .\download-font.ps1

$fontUrl = "https://www.dafont.com/monigue-demo.font"
$downloadPage = "https://exfont.com/moniguedemo-regular.font"

Write-Host "Monigue DEMO Font Download Instructions:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "The font needs to be downloaded manually due to website restrictions." -ForegroundColor Yellow
Write-Host ""
Write-Host "Please follow these steps:" -ForegroundColor Green
Write-Host "1. Visit: $downloadPage" -ForegroundColor White
Write-Host "2. Download the font file (usually a ZIP file)" -ForegroundColor White
Write-Host "3. Extract the font file (.ttf, .otf, or .woff format)" -ForegroundColor White
Write-Host "4. Rename it to one of these:" -ForegroundColor White
Write-Host "   - MonigueDEMO.woff2" -ForegroundColor Cyan
Write-Host "   - MonigueDEMO.woff" -ForegroundColor Cyan
Write-Host "   - MonigueDEMO.ttf" -ForegroundColor Cyan
Write-Host "   - MonigueDEMO.otf" -ForegroundColor Cyan
Write-Host "5. Place it in this directory: $PSScriptRoot" -ForegroundColor White
Write-Host ""
Write-Host "Alternative: Try downloading from:" -ForegroundColor Yellow
Write-Host "https://www.dafont.com/monigue-demo.font" -ForegroundColor Cyan
Write-Host ""

# Try to open the download page
$open = Read-Host "Would you like to open the download page in your browser? (Y/N)"
if ($open -eq 'Y' -or $open -eq 'y') {
    Start-Process $downloadPage
    Write-Host "Download page opened in browser!" -ForegroundColor Green
}

