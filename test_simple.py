#!/usr/bin/env python3
"""
Script de teste simples para verificar dependências
"""

print("=== Teste de Dependências ===")

try:
    print("1. Importando rich.console...")
    from rich.console import Console
    print("   ✅ rich.console OK")
    
    print("2. Importando rich.table...")
    from rich.table import Table
    print("   ✅ rich.table OK")
    
    print("3. Importando rich.live...")
    from rich.live import Live
    print("   ✅ rich.live OK")
    
    print("4. Importando rich.panel...")
    from rich.panel import Panel
    print("   ✅ rich.panel OK")
    
    print("5. Testando console...")
    console = Console()
    console.print("[green]✅ Console funcionando![/green]")
    
    print("6. Testando tabela...")
    table = Table(title="Teste")
    table.add_column("Coluna 1")
    table.add_column("Coluna 2")
    table.add_row("Valor 1", "Valor 2")
    console.print(table)
    
    print("7. Testando painel...")
    panel = Panel("Teste de painel", title="Teste")
    console.print(panel)
    
    print("\n🎯 Todas as dependências estão funcionando!")
    
except ImportError as e:
    print(f"❌ Erro de importação: {e}")
    print("Execute: pip3 install rich>=13.0.0")
except Exception as e:
    print(f"❌ Erro geral: {e}")
    import traceback
    traceback.print_exc()
