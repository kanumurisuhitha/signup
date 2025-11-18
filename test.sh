# -------------------------------
# Windows PowerShell test script
# -------------------------------

# Configurable variables
$baseUrl = "http://127.0.0.1:8000"
$username = "testuser"
$password = "Password123"
$fname = "John"
$lname = "Doe"

# Start FastAPI server in background
Write-Host "Starting FastAPI server..."
$server = Start-Process -FilePath "python" -ArgumentList "-m uvicorn main:app --host 0.0.0.0 --port 8000" -PassThru

# Wait a few seconds to ensure the server is ready
Start-Sleep -Seconds 3

# Run Newman tests
Write-Host "Running Newman tests..."
newman run `
    --env-var baseUrl="$baseUrl" `
    --env-var username="$username" `
    --env-var password="$password" `
    --env-var fname="$fname" `
    --env-var lname="$lname" `
    https://raw.githubusercontent.com/UXGorilla/hiring-backend/main/collection.json

# Stop the FastAPI server
Write-Host "Stopping FastAPI server..."
Stop-Process -Id $server.Id

Write-Host "Test run completed."
