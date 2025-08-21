#!/bin/bash
# Script de instalação do Monitor de Automações

echo "🎯 Instalando Monitor de Automações JC Decor..."

# Verifica se Python3 está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado. Instalando..."
    sudo apt update
    sudo apt install -y python3 python3-pip
fi

# Instala as dependências
echo "📦 Instalando dependências..."
pip3 install -r requirements.txt

# Torna o script principal executável
chmod +x monitor_automacoes.py

# Cria um script de inicialização
cat > start_monitor.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
python3 monitor_automacoes.py
EOF

chmod +x start_monitor.sh

echo "✅ Instalação concluída!"
echo ""
echo "📖 Como usar:"
echo "   ./start_monitor.sh  - Inicia o monitor"
echo "   ou"
echo "   python3 monitor_automacoes.py"
echo ""
echo "💡 Comandos disponíveis no monitor:"
echo "   force C1     - Força verificação da automação C1"
echo "   refresh      - Atualiza todas as automações" 
echo "   quit         - Sai do sistema"
echo ""
