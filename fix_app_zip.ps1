$appZipPath = "build\flutter\windows\build\runner\Release\data\flutter_assets\app\app.zip"
if (-not (Test-Path $appZipPath)) {
    Write-Host "Searching for app.zip..."
    $foundZip = Get-ChildItem -Path build -Recurse -Filter "app.zip" -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($foundZip) {
        $appZipPath = $foundZip.FullName
        Write-Host "Found at: $appZipPath"
    } else {
        Write-Host "ERROR: app.zip not found"
        exit 1
    }
}

Write-Host "Checking app.zip contents..."
Add-Type -AssemblyName System.IO.Compression.FileSystem
$zip = [System.IO.Compression.ZipFile]::OpenRead($appZipPath)
$hasMain = $zip.Entries | Where-Object { $_.FullName -eq "main.pyc" -or $_.FullName -like "main.*" } | Select-Object -First 1
$hasSrc = $zip.Entries | Where-Object { $_.FullName -like "src\*" } | Select-Object -First 1
$zip.Dispose()

if (-not $hasMain -or -not $hasSrc) {
    Write-Host "app.zip is missing main.pyc or src/ - rebuilding..."
    
    $tempDir = "temp_app_rebuild"
    if (Test-Path $tempDir) {
        Remove-Item -Path $tempDir -Recurse -Force
    }
    New-Item -ItemType Directory -Force -Path $tempDir | Out-Null
    
    Write-Host "Compiling main.py..."
    python -m py_compile main.py
    if (Test-Path "main.pyc") {
        Copy-Item "main.pyc" -Destination "$tempDir\main.pyc" -Force
        Remove-Item "main.pyc" -Force
    } else {
        Write-Host "ERROR: Failed to compile main.py"
        exit 1
    }
    
    Write-Host "Copying src directory..."
    if (Test-Path "src") {
        Copy-Item -Path "src" -Destination "$tempDir\src" -Recurse -Force
        
        Write-Host "Compiling Python files in src..."
        Get-ChildItem -Path "$tempDir\src" -Recurse -Filter "*.py" | ForEach-Object {
            $pyFile = $_.FullName
            $pycFile = $pyFile + "c"
            python -m py_compile $pyFile
            if (Test-Path $pycFile) {
                Remove-Item $pyFile -Force
                Write-Host "  Compiled: $($_.Name)"
            }
        }
    } else {
        Write-Host "ERROR: src directory not found"
        exit 1
    }
    
    Write-Host "Creating new app.zip..."
    $zipDir = Split-Path $appZipPath -Parent
    if (-not (Test-Path $zipDir)) {
        New-Item -ItemType Directory -Force -Path $zipDir | Out-Null
    }
    
    if (Test-Path $appZipPath) {
        Remove-Item $appZipPath -Force
    }
    
    [System.IO.Compression.ZipFile]::CreateFromDirectory($tempDir, $appZipPath, [System.IO.Compression.CompressionLevel]::Optimal, $false)
    
    Write-Host "Calculating hash..."
    $hashBytes = [System.Security.Cryptography.SHA256]::Create().ComputeHash([System.IO.File]::ReadAllBytes($appZipPath))
    $hash = [System.BitConverter]::ToString($hashBytes).Replace("-", "").ToLower()
    
    $hashPath = $appZipPath -replace "\.zip$", ".zip.hash"
    [System.IO.File]::WriteAllText($hashPath, $hash)
    
    Write-Host "Cleaning up..."
    Remove-Item -Path $tempDir -Recurse -Force
    
    Write-Host "✓ app.zip rebuilt successfully"
} else {
    Write-Host "✓ app.zip already contains main.pyc and src/"
}

