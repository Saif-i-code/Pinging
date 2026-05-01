from icmplib import ping
import time
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console()

banner_text = Text("⚡ The Devloper: Saif Ali ⚡", style="bold italic cyan")
console.print(Panel(banner_text, border_style="blue", title="[bold magenta]Monitoring Tool[/bold magenta]"))
console.print("[dim white]Note: Please run as Admin/Root if you encounter issues.[/dim white]\n")
target = console.input("[bold green]Enter Target Host/IP: [/bold green]")
try:
    size_input = console.input("[bold white]Packet Size (default 32): [/bold white]")
    size = int(size_input) if size_input else 32
    
    timeout_input = console.input("[bold white]Timeout in seconds (default 2): [/bold white]")
    timeout = int(timeout_input) if timeout_input else 2
except ValueError:
    console.print("[red]Invalid entry. Defaulting to 32 bytes and 2s timeout.[/red]")
    size = 32
    timeout = 2

total = 0
success = 0
min_rtt = float('inf')
max_rtt = 0.0
total_rtt = 0.0

console.print(f"\n[bold yellow]Pinging {target}... (Ctrl+C to stop)[/bold yellow]\n")

try:
    while True:
        res = ping(target, count=1, timeout=timeout, payload_size=size)
        total += 1
        
        if res.is_alive:
            success += 1
            current_rtt = res.avg_rtt
            total_rtt += current_rtt
            
            if current_rtt < min_rtt: min_rtt = current_rtt
            if current_rtt > max_rtt: max_rtt = current_rtt
            
            console.print(f"[bold green]✔[/bold green] [cyan]{res.address}[/cyan] | time=[bold white]{current_rtt}ms[/bold white] | [dim]min={min_rtt}ms max={max_rtt}ms[/dim]")
        else:
            console.print(f"[bold red]✘[/bold red] [red]{target} timed out[/red]")
            
        time.sleep(1)

except KeyboardInterrupt:
    # Final Table
    console.print("\n")
    if total > 0:
        summary = Table(title="[bold blue]📊 Session Summary[/bold blue]", border_style="cyan")
        summary.add_column("Measurement", style="magenta")
        summary.add_column("Value", style="bold white")
        
        summary.add_row("Target Host", target)
        summary.add_row("Packets Sent", str(total))
        summary.add_row("Packets Received", str(success))
        
        loss = ((total - success) / total * 100)
        loss_style = "green" if loss == 0 else "yellow" if loss < 10 else "red"
        summary.add_row("Packet Loss", f"[{loss_style}]{loss:.1f}%[/{loss_style}]")
        
        if success > 0:
            summary.add_row("Minimum RTT", f"{min_rtt}ms")
            summary.add_row("Maximum RTT", f"{max_rtt}ms")
        
        console.print(summary)
    
    console.print("\n[bold green]Thank you for using Ping Pro![/bold green]")

except Exception as e:
    if "NoneType" in str(e) or "operation not permitted" in str(e).lower():
        console.print(Panel(f"[bold red]Permission Error![/bold red]\nYou must run as [bold yellow]Administrator[/bold yellow] (Windows) or [bold yellow]Sudo[/bold yellow] (Linux).", border_style="red", title="[bold white]Access Denied[/bold white]"))
    else:
        console.print(f"[bold red]Error:[/bold red] {e}")
