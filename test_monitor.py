#!/usr/bin/env python3

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def test_basic():
    print("=== TESTE BÁSICO ===")
    
    # Teste 1: Console básico
    console.print("[bold blue]Teste 1: Console funcionando![/bold blue]")
    
    # Teste 2: Panel
    panel = Panel("Teste de Panel", title="Panel OK", border_style="blue")
    console.print(panel)
    
    # Teste 3: Table
    table = Table(title="Teste de Tabela")
    table.add_column("Nome")
    table.add_column("Status")
    table.add_row("C1", "✅ OK")
    table.add_row("P1", "❌ ERROR")
    console.print(table)
    
    print("=== FIM DO TESTE ===")

if __name__ == "__main__":
    test_basic()
