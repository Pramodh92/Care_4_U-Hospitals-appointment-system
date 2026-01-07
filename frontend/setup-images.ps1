# Image Setup Script for Care_4_U Hospitals Frontend

# Create images directory
$imagesDir = "c:\Projects\AWS-Driven Doctor Appointment System – Care_4_U Hospitals\frontend\images"
if (-not (Test-Path $imagesDir)) {
    New-Item -ItemType Directory -Path $imagesDir -Force
    Write-Host "Created images directory" -ForegroundColor Green
}

# Source directory with generated images
$sourceDir = "C:\Users\pramo\.gemini\antigravity\brain\6272a320-17ce-40dd-a831-0325beba98f1"

# Copy images
Write-Host "Copying generated images..." -ForegroundColor Cyan

Copy-Item "$sourceDir\hero_background_1767764951376.png" "$imagesDir\hero-background.png" -Force
Write-Host "✓ Copied hero-background.png" -ForegroundColor Green

Copy-Item "$sourceDir\hospital_exterior_1767764967495.png" "$imagesDir\hospital-exterior.png" -Force
Write-Host "✓ Copied hospital-exterior.png" -ForegroundColor Green

Copy-Item "$sourceDir\doctor_1_1767764986421.png" "$imagesDir\doctor-1.png" -Force
Write-Host "✓ Copied doctor-1.png" -ForegroundColor Green

Copy-Item "$sourceDir\doctor_2_1767765001742.png" "$imagesDir\doctor-2.png" -Force
Write-Host "✓ Copied doctor-2.png" -ForegroundColor Green

Copy-Item "$sourceDir\doctor_3_1767765018855.png" "$imagesDir\doctor-3.png" -Force
Write-Host "✓ Copied doctor-3.png" -ForegroundColor Green

Copy-Item "$sourceDir\doctor_4_1767765036457.png" "$imagesDir\doctor-4.png" -Force
Write-Host "✓ Copied doctor-4.png" -ForegroundColor Green

Copy-Item "$sourceDir\doctor_5_1767765061845.png" "$imagesDir\doctor-5.png" -Force
Write-Host "✓ Copied doctor-5.png" -ForegroundColor Green

Copy-Item "$sourceDir\doctor_6_1767765081625.png" "$imagesDir\doctor-6.png" -Force
Write-Host "✓ Copied doctor-6.png" -ForegroundColor Green

Write-Host "`nAll images copied successfully!" -ForegroundColor Green
Write-Host "Images are now available in: $imagesDir" -ForegroundColor Cyan
