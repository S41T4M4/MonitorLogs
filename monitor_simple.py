#!/usr/bin/env python3
"""
Versão simplificada para debug
"""

print("🚀 Iniciando Monitor Simplificado...")

try:
    print("1. Importando módulos...")
    import os
    import time
    from datetime import datetime
    print("   ✅ Módulos básicos OK")
    
    print("2. Importando Rich...")
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    print("   ✅ Rich OK")
    
    print("3. Criando console...")
    console = Console()
    print("   ✅ Console criado")
    
    print("4. Testando painel...")
    panel = Panel("Teste", title="Teste")
    console.print(panel)
    print("   ✅ Painel OK")
    
    print("5. Testando tabela...")
    table = Table(title="Teste")
    table.add_column("Nome")
    table.add_column("Status")
    table.add_row("C1", "OK")
    console.print(table)
    print("   ✅ Tabela OK")
    
    print("\n🎯 Sistema funcionando! Pressione Ctrl+C para sair...")
    
    # Loop simples
    while True:
        console.print(f"⏰ {datetime.now().strftime('%H:%M:%S')} - Sistema rodando...")
        time.sleep(2)
        
except Exception as e:
    print(f"❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
