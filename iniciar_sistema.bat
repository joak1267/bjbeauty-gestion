@echo off
chcp 65001 > nul
title BJ BEAUTY - Sistema de Ventas & Base de Datos MySQL
color 0B

echo ================================================================
echo           💎 BJ BEAUTY - SISTEMA INTEGRAL DE GESTIÓN 💎
echo ================================================================
echo.

:: 1. Verificar y levantar MySQL
echo [1/3] Verificando servicio de MySQL (XAMPP)...
tasklist /FI "IMAGENAME eq mysqld.exe" 2>NUL | find /I /N "mysqld.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo       [OK] MySQL ya se encuentra activo en el puerto 3306.
) else (
    echo       Iniciando MySQL en segundo plano...
    if exist "C:\xampp\mysql\bin\mysqld.exe" (
        start "" /B "C:\xampp\mysql\bin\mysqld.exe" --defaults-file="C:\xampp\mysql\bin\my.ini" --console
        timeout /t 3 > nul
        echo       [OK] MySQL iniciado con éxito en C:\xampp.
    ) else (
        echo       [ADVERTENCIA] No se encontró mysqld.exe en C:\xampp\mysql\bin.
        echo       Asegúrate de tener XAMPP con MySQL iniciado.
    )
)

echo.
:: 2. Iniciar servidor API Flask
echo [2/3] Iniciando Servidor API de Base de Datos (servidor_db.py)...
start "BJ BEAUTY - Servidor API MySQL" cmd /k "color 0A && title BJ BEAUTY - Servidor API MySQL && cd /d %~dp0 && python servidor_db.py"

timeout /t 2 > nul

echo.
:: 3. Abrir sistema en el navegador
echo [3/3] Abriendo el panel de ventas en tu navegador...
start http://localhost:5000

echo.
echo ================================================================
echo  ✅ ¡SISTEMA INICIADO EXITOSAMENTE!
echo ================================================================
echo  * Panel Web:    http://localhost:5000
echo  * Base Datos:   MySQL (MariaDB) -> bj_beauty_db
echo  * Tablas:       ventas, compras_mercaderia, stock, reservas_pedidos
echo  * Módulos:      Ventas, Costos, Reservas & Encargos, Catálogo Oficial (556 fragancias)
echo.
echo  Deja abierta la ventana de la API mientras uses el sistema.
echo ================================================================
echo.
pause
