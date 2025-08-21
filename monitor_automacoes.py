#!/usr/bin/env python3
"""
Monitor de Automações - Dashboard CLI para Centralização de Logs
Empresa: JC Decor
Autor: Sistema de Automação
"""

import os
import time
import threading
import queue
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel

import select
import sys

# Configuração
LOG_FILE = "run.log"
console = Console()
command_queue = queue.Queue()


class Automacao:
    def __init__(self, nome, diretorio, horarios, logs_ok, logs_fail):
        self.nome = nome
        self.diretorio = diretorio
        self.horarios = horarios
        self.logs_ok = logs_ok
        self.logs_fail = logs_fail
        self.status = "UNKNOWN"
        self.ultima_msg = ""
        self.ultima_verificacao = ""
        self._horarios_executados = set()
        self.ultima_execucao = "Nunca"

    def get_last_log_line(self):
        log_path = os.path.join(self.diretorio, LOG_FILE)
        if not os.path.exists(log_path):
            return None
        try:
            with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
                if not lines:
                    return None
                
                # Procura pelas últimas linhas relevantes após o timestamp
                for i, line in enumerate(reversed(lines)):
                    line = line.strip()
                    if line and "===" in line:  # Linha de timestamp
                        # Pega as próximas linhas após o timestamp
                        start_idx = len(lines) - i
                        relevant_lines = []
                        
                        for j in range(start_idx, len(lines)):
                            line_content = lines[j].strip()
                            if line_content and not line_content.startswith("==="):
                                relevant_lines.append(line_content)
                        
                        # Retorna a última linha com conteúdo relevante
                        if relevant_lines:
                            # Prioriza linhas com indicadores de sucesso/erro
                            for line_content in reversed(relevant_lines):
                                if any(indicator in line_content.lower() 
                                      for indicator in ["sucesso", "erro", "exception", 
                                                       "falha", "error", "failed", 
                                                       "linhas afetadas", "inserido"]):
                                    return line_content
                            return relevant_lines[-1]
                        break
                        
                # Se não encontrou timestamp, retorna a última linha não vazia
                for line in reversed(lines):
                    line = line.strip()
                    if line:
                        return line
                        
                return None
        except Exception as e:
            return f"[ERRO AO LER LOG: {e}]"

    def verificar(self):
        self.status = "Verificando..."
        self.ultima_msg = ""
        self.ultima_verificacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        last_line = self.get_last_log_line()
        if not last_line:
            self.status = "NO_LOG"
            self.ultima_msg = "Nenhum log encontrado"
            return

        # Verifica se há erros primeiro
        if any(p.lower() in last_line.lower() for p in self.logs_fail):
            self.status = "ERROR"
        elif any(p.lower() in last_line.lower() for p in self.logs_ok):
            self.status = "OK"
        else:
            # Se não encontrou padrões específicos, verifica se executou com sucesso
            exit_code_0 = "exit code 0" in last_line.lower()
            sucesso = "sucesso" in last_line.lower()
            if exit_code_0 or sucesso:
                self.status = "OK"
            exit_code_present = "exit code" in last_line.lower()
            if exit_code_present and not exit_code_0:
                self.status = "ERROR"
            else:
                self.status = "UNKNOWN"

        # Trunca mensagem se for muito longa
        if len(last_line) > 80:
            self.ultima_msg = last_line[:80] + "..."
        else:
            self.ultima_msg = last_line
        self.ultima_verificacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def deve_verificar(self):
        now = datetime.now().strftime("%H:%M")
        if now in self.horarios and now not in self._horarios_executados:
            self._horarios_executados.add(now)
            return True
        return False

    def forcar_verificacao(self):
        self.verificar()
        self.ultima_execucao = datetime.now().strftime("%H:%M:%S")


# Configuração das Automações
AUTOMACOES = [
    Automacao(
        nome="C1",
        diretorio="/home/jc-automation/Downloads/REALTIME/C1",
        horarios=["08:00", "12:00", "16:00"],
        logs_ok=["sucesso", "inserido/atualizado com sucesso", "inserida com sucesso", 
                "atualizados", "linhas afetadas", "exit code 0"],
        logs_fail=["erro", "exception", "falha", "error", "failed", "exit code 1", "exit code 2"]
    ),
    Automacao(
        nome="CAT1",
        diretorio="/home/jc-automation/Downloads/REALTIME/CAT1",
        horarios=["09:00", "13:00", "17:00"],
        logs_ok=["sucesso", "inserido/atualizado com sucesso", "inserida com sucesso", 
                "atualizados", "linhas afetadas", "exit code 0"],
        logs_fail=["erro", "exception", "falha", "error", "failed", "exit code 1", "exit code 2"]
    ),
    Automacao(
        nome="CR1",
        diretorio="/home/jc-automation/Downloads/REALTIME/CR1",
        horarios=["07:00", "11:00", "15:00"],
        logs_ok=["sucesso", "inserido/atualizado com sucesso", "inserida com sucesso", 
                "atualizados", "linhas afetadas", "exit code 0"],
        logs_fail=["erro", "exception", "falha", "error", "failed", "exit code 1", "exit code 2"]
    ),
    Automacao(
        nome="EM1",
        diretorio="/home/jc-automation/Downloads/REALTIME/EM1",
        horarios=["08:30", "12:30", "16:30"],
        logs_ok=["sucesso", "inserido/atualizado com sucesso", "inserida com sucesso", 
                "atualizados", "linhas afetadas", "exit code 0"],
        logs_fail=["erro", "exception", "falha", "error", "failed", "exit code 1", "exit code 2"]
    ),
    Automacao(
        nome="NC1",
        diretorio="/home/jc-automation/Downloads/REALTIME/NC1",
        horarios=["09:30", "13:30", "17:30"],
        logs_ok=["sucesso", "inserido/atualizado com sucesso", "inserida com sucesso", 
                "atualizados", "linhas afetadas", "exit code 0"],
        logs_fail=["erro", "exception", "falha", "error", "failed", "exit code 1", "exit code 2"]
    ),
    Automacao(
        nome="NF1",
        diretorio="/home/jc-automation/Downloads/REALTIME/NF1",
        horarios=["07:30", "11:30", "15:30"],
        logs_ok=["sucesso", "inserido/atualizado com sucesso", "inserida com sucesso", 
                "atualizados", "linhas afetadas", "exit code 0"],
        logs_fail=["erro", "exception", "falha", "error", "failed", "exit code 1", "exit code 2"]
    ),
    Automacao(
        nome="NF2",
        diretorio="/home/jc-automation/Downloads/REALTIME/NF2",
        horarios=["08:15", "12:15", "16:15"],
        logs_ok=["sucesso", "inserido/atualizado com sucesso", "inserida com sucesso", 
                "atualizados", "linhas afetadas", "exit code 0"],
        logs_fail=["erro", "exception", "falha", "error", "failed", "exit code 1", "exit code 2"]
    ),
    Automacao(
        nome="ODC1",
        diretorio="/home/jc-automation/Downloads/REALTIME/ODC1",
        horarios=["09:15", "13:15", "17:15"],
        logs_ok=["sucesso", "inserido/atualizado com sucesso", "inserida com sucesso", 
                "atualizados", "linhas afetadas", "exit code 0"],
        logs_fail=["erro", "exception", "falha", "error", "failed", "exit code 1", "exit code 2"]
    ),
    Automacao(
        nome="ODC2",
        diretorio="/home/jc-automation/Downloads/REALTIME/ODC2",
        horarios=["07:45", "11:45", "15:45"],
        logs_ok=["sucesso", "inserido/atualizado com sucesso", "inserida com sucesso", 
                "atualizados", "linhas afetadas", "exit code 0"],
        logs_fail=["erro", "exception", "falha", "error", "failed", "exit code 1", "exit code 2"]
    ),
    Automacao(
        nome="ORC1",
        diretorio="/home/jc-automation/Downloads/REALTIME/ORC1",
        horarios=["08:45", "12:45", "16:45"],
        logs_ok=["sucesso", "inserido/atualizado com sucesso", "inserida com sucesso", 
                "atualizados", "linhas afetadas", "exit code 0"],
        logs_fail=["erro", "exception", "falha", "error", "failed", "exit code 1", "exit code 2"]
    ),
    Automacao(
        nome="P1",
        diretorio="/home/jc-automation/Downloads/REALTIME/P1",
        horarios=["08:00", "14:00"],
        logs_ok=["sucesso", "inserido/atualizado com sucesso", "inserida com sucesso", 
                "atualizados", "linhas afetadas", "exit code 0"],
        logs_fail=["erro", "exception", "falha", "error", "failed", "exit code 1", "exit code 2"]
    ),
    Automacao(
        nome="P2",
        diretorio="/home/jc-automation/Downloads/REALTIME/P2",
        horarios=["09:00", "15:00"],
        logs_ok=["sucesso", "inserido/atualizado com sucesso", "inserida com sucesso", 
                "atualizados", "linhas afetadas", "exit code 0"],
        logs_fail=["erro", "exception", "falha", "error", "failed", "exit code 1", "exit code 2"]
    ),
    Automacao(
        nome="PG1",
        diretorio="/home/jc-automation/Downloads/REALTIME/PG1",
        horarios=["10:00", "16:00"],
        logs_ok=["sucesso", "inserido/atualizado com sucesso", "inserida com sucesso", 
                "atualizados", "linhas afetadas", "exit code 0"],
        logs_fail=["erro", "exception", "falha", "error", "failed", "exit code 1", "exit code 2"]
    ),
    Automacao(
        nome="PR1",
        diretorio="/home/jc-automation/Downloads/REALTIME/PR1",
        horarios=["07:00", "13:00"],
        logs_ok=["sucesso", "inserido/atualizado com sucesso", "inserida com sucesso", 
                "atualizados", "linhas afetadas", "exit code 0"],
        logs_fail=["erro", "exception", "falha", "error", "failed", "exit code 1", "exit code 2"]
    ),
    Automacao(
        nome="PR2",
        diretorio="/home/jc-automation/Downloads/REALTIME/PR2",
        horarios=["08:30", "14:30"],
        logs_ok=["sucesso", "inserido/atualizado com sucesso", "inserida com sucesso", 
                "atualizados", "linhas afetadas", "exit code 0"],
        logs_fail=["erro", "exception", "falha", "error", "failed", "exit code 1", "exit code 2"]
    ),
    Automacao(
        nome="V1",
        diretorio="/home/jc-automation/Downloads/REALTIME/V1",
        horarios=["10:30", "16:30"],
        logs_ok=["sucesso", "inserido/atualizado com sucesso", "inserida com sucesso", 
                "atualizados", "linhas afetadas", "exit code 0"],
        logs_fail=["erro", "exception", "falha", "error", "failed", "exit code 1", "exit code 2"]
    ),
]


def build_dashboard():
    # Cria apenas a tabela principal (versão simplificada)
    table = Table(
        title="🎯 Painel de Controle - Automações JC Decor",
        show_lines=True,
        title_style="bold blue",
        header_style="bold white"
    )
    
    table.add_column("Automação", style="bold cyan", width=10)
    table.add_column("Horário", style="dim", width=15)
    table.add_column("Status", style="bold", width=12)
    table.add_column("Última Mensagem", overflow="fold", width=35)
    table.add_column("Verificação", style="dim", width=18)

    for auto in AUTOMACOES:
        # Define cores baseadas no status
        if auto.status == "OK":
            status_color = "green"
            status_icon = "✅"
        elif auto.status == "ERROR":
            status_color = "red"
            status_icon = "❌"
        elif auto.status == "Verificando...":
            status_color = "cyan"
            status_icon = "🔄"
        elif auto.status == "NO_LOG":
            status_color = "grey37"
            status_icon = "❓"
        else:
            status_color = "grey37"
            status_icon = "❓"

        # Formata horários
        horarios_str = ",".join(auto.horarios[:2])  # Mostra só os 2 primeiros
        if len(auto.horarios) > 2:
            horarios_str += "..."
        
        table.add_row(
            auto.nome,
            horarios_str,
            f"[{status_color}]{status_icon} {auto.status}[/{status_color}]",
            auto.ultima_msg[:35] + "..." if len(auto.ultima_msg) > 35 else auto.ultima_msg,
            auto.ultima_verificacao[-8:] if auto.ultima_verificacao else "Nunca"  # Só hora
        )
    
    return table




def process_command(cmd):
    cmd = cmd.strip().lower()
    
    if cmd.startswith("force "):
        nome = cmd.split()[1].upper()
        for auto in AUTOMACOES:
            if auto.nome == nome:
                auto.forcar_verificacao()
                msg = f"[green]✓ Verificação forçada para {nome}[/green]"
                console.print(msg)
                return True
        console.print(f"[red]✗ Automação {nome} não encontrada[/red]")
        return True
        
    elif cmd == "refresh":
        for auto in AUTOMACOES:
            auto.verificar()
        msg = "[green]✓ Todas as automações foram atualizadas[/green]"
        console.print(msg)
        return True
        
    elif cmd == "quit" or cmd == "exit":
        console.print("[yellow]👋 Saindo do sistema...[/yellow]")
        return False
        
    elif cmd == "help":
        console.print(build_help_panel())
        return True
        
    elif cmd == "":
        return True
        
    else:
        msg = f"[yellow]⚠️ Comando inválido: {cmd}[/yellow]"
        console.print(msg)
        msg = "[dim]Digite 'help' para ver os comandos disponíveis[/dim]"
        console.print(msg)
        return True


def input_thread():
    """Thread separada para capturar input sem bloquear o loop principal"""
    while True:
        try:
            if select.select([sys.stdin], [], [], 0.1)[0]:
                cmd = input().strip()
                command_queue.put(cmd)
        except (EOFError, KeyboardInterrupt):
            break


def main():
    print("DEBUG: Iniciando main()")
    console.clear()
    print("DEBUG: Console limpo")
    
    console.print(Panel.fit(
        "[bold blue]🎯 Monitor de Automações JC Decor[/bold blue]\n"
        "[dim]Sistema de Centralização de Logs[/dim]",
        border_style="blue"
    ))
    print("DEBUG: Título exibido")
    
    # Inicia thread de input
    print("DEBUG: Iniciando thread de input...")
    input_thread_obj = threading.Thread(target=input_thread, daemon=True)
    input_thread_obj.start()
    print("DEBUG: Thread de input iniciada")
    
    # Primeira verificação
    print("DEBUG: Iniciando primeira verificação...")
    for i, auto in enumerate(AUTOMACOES):
        print(f"DEBUG: Verificando {auto.nome} ({i+1}/{len(AUTOMACOES)})")
        auto.verificar()
    print("DEBUG: Primeira verificação concluída")
    
    try:
        print("DEBUG: Iniciando Live...")
        with Live(
            build_dashboard(),
            refresh_per_second=1,
            screen=True
        ) as live:
            print("DEBUG: Live iniciado, entrando no loop principal")
            
            while True:
                # Processa comandos pendentes
                try:
                    while not command_queue.empty():
                        cmd = command_queue.get_nowait()
                        if not process_command(cmd):
                            break
                except queue.Empty:
                    pass
                
                # Verificações automáticas
                for auto in AUTOMACOES:
                    if auto.deve_verificar():
                        auto.verificar()
                
                # Atualiza interface
                live.update(build_dashboard())
                
                time.sleep(1)
                
    except KeyboardInterrupt:
        console.print("\n[yellow]👋 Sistema interrompido pelo usuário[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Erro no sistema: {e}[/red]")


if __name__ == "__main__":
    main()
