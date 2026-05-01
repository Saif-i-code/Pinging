from icmplib import ping
import time
import sys
import threading 
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.table import Table
from rich.text import Text


console = Console()
layout = Layout()

layout.split_row(
    Layout(name="left", ratio=1),
    Layout(name="right", ratio=1)
)

ping_history = []
rtt_history = []

def left_panel_task(target):
    global rtt_history
    try:
        while True:
           
            width = 60
            height = 15
            
            padded = [0] * (width - len(rtt_history)) + rtt_history
            max_val = max(padded) if padded and max(padded) > 0 else 1
            
            lines = []
            for row in range(height, 0, -1):
                threshold = max_val * (row / height)
                line = ""
                for val in padded:
                    if val == 0:
                        line += "[red]x[/red]" if row == 1 else " "
                    elif val >= threshold:
                        color = "green" if val < 50 else "yellow" if val < 150 else "red"
                        line += f"[{color}]█[/{color}]"
                    else:
                        line += " "
                
                if row == height:
                    line += f" [cyan]{max_val:.1f}ms[/cyan] (Max)"
                elif row == 1:
                    line += " [cyan]0ms[/cyan]"
                    
                lines.append(line)
            
            content = "\n".join(lines)
            content += f"\n\n[dim]Target:[/dim] [bold white]{target}[/bold white]"
            
            layout["left"].update(Panel(content, title="[bold green]📊 Live RTT Graph[/bold green]", border_style="cyan"))
            time.sleep(1)
    except Exception as e:
        layout["left"].update(Panel(f"[red]Error: {e}[/red]"))

def right_panel_task(target, timeout, size, interval):
    global ping_history
    total = 0
    success = 0
    try:
        while True:
            res = ping(target, count=1, timeout=timeout, payload_size=size)
            total += 1
            if res.is_alive:
                success += 1
                rtt_history.append(res.avg_rtt)
                status = f"[bold green]✔[/bold green] IP: [cyan]{res.address}[/cyan] | RTT: [white]{res.avg_rtt}ms[/white] | Alive: [green]{res.is_alive}[/green]"
            else:
                rtt_history.append(0)
                status = f"[bold red]✘[/bold red] IP: [cyan]{target}[/cyan] | Packet #{total} Timed Out | Alive: [red]False[/red]"
            
            if len(rtt_history) > 45: rtt_history.pop(0)
            
            ping_history.append(f"{status} | [dim]S:{total} R:{success}[/dim]")
            if len(ping_history) > 18: ping_history.pop(0)
            
            layout["right"].update(Panel("\n".join(ping_history), title=f"Live Ping", border_style="blue"))
            
            time.sleep(interval)
    except Exception as e:
        layout["right"].update(Panel(f"[red]Error: {e}[/red]"))

banner_text = Text("⚡ Developer: Saif Ali ⚡", style="bold italic cyan")
console.print(Panel(banner_text, border_style="blue", title="Monitoring Tool"))

target = console.input("[bold green]Enter Target Host/IP: [/bold green]")

try:
    size_input = console.input("[bold white]Packet Size (default 32): [/bold white]")
    size = int(size_input) if size_input else 32

    interval_input = console.input("[bold white]Interval (Min 0.05, Default 1): [/bold white]")
    interval = float(interval_input) if interval_input else 1.0
    if interval < 0.05: interval = 0.05
    
    timeout_input = console.input("[bold white]Timeout (default 2): [/bold white]")
    timeout = int(timeout_input) if timeout_input else 2
except:
    size, interval, timeout = 32, 1.0, 2

try:
    with Live(layout, screen=True, refresh_per_second=10):
        t1 = threading.Thread(target=right_panel_task, args=(target, timeout, size, interval), daemon=True)
        t2 = threading.Thread(target=left_panel_task, args=(target,), daemon=True)
        t1.start()
        t2.start()
        
        while True:
            time.sleep(1)
except KeyboardInterrupt:
    console.print("\n[bold green]Stopped.[/bold green]")
