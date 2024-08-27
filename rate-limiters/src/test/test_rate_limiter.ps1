for ($i = 1, $i -le 20; $i++){
    Invoke-WebRequest -Uri http://127.0.0.1:5000/api/resource -Method GET
    Start-Sleep -Milliseconds 100
}