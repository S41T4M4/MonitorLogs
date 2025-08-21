@echo off
REM Script de instalação do Monitor de Automações para Windows

echo 🎯 Instalando Monitor de Automações JC Decor...

REM Verifica se Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python não encontrado. Por favor, instale o Python primeiro.
    echo Baixe em: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Instala as dependências
echo 📦 Instalando dependências...
pip install -r requirements.txt

REM Cria um script de inicialização
echo @echo off > start_monitor.bat
echo cd /d "%%~dp0" >> start_monitor.bat
echo python monitor_automacoes.py >> start_monitor.bat
echo pause >> start_monitor.bat

echo ✅ Instalação concluída!
echo.
echo 📖 Como usar:
echo    start_monitor.bat  - Inicia o monitor
echo    ou
echo    python monitor_automacoes.py
echo.
echo 💡 Comandos disponíveis no monitor:
echo    force C1     - Força verificação da automação C1
echo    refresh      - Atualiza todas as automações
echo    quit         - Sai do sistema
echo.
pause
