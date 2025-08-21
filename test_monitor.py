#!/usr/bin/env python3

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def test_monitor_simulation():
    print("=== TESTE SIMULAÇÃO DO MONITOR ===")
    
    # Simula exatamente o que o monitor faz
    console.clear()
    
    # 1. Título (igual ao monitor)
    console.print(Panel.fit(
        "[bold blue]🎯 Monitor de Automações JC Decor[/bold blue]\n"
        "[dim]Sistema de Centralização de Logs[/dim]",
        border_style="blue"
    ))
    
    # 2. Tabela (igual ao monitor)
    table = Table(
        title="🎯 Painel de Controle - Automações JC Decor",
        show_lines=True,
        title_style="bold blue",
        header_style="bold white"
    )
    
    table.add_column("Automação", style="bold cyan", width=10)
    table.add_column("Status", style="bold", width=12)
    table.add_column("Mensagem", width=30)
    
    table.add_row("C1", "✅ OK", "Cliente inserido com sucesso")
    table.add_row("P1", "❌ ERROR", "Exception na execução")
    
    console.print(table)
    
    # 3. Comandos
    console.print("\n[bold green]Comandos:[/bold green] force <nome> | refresh | quit")
    
    print("=== FIM DO TESTE ===")

if __name__ == "__main__":
    test_monitor_simulation()
