"""
System information and monitoring utilities.
Provides system stats, process management, and network information.
"""

import os
import platform
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


class SystemMonitor:
    """Handles system information and monitoring."""
    
    def __init__(self):
        """Initialize the system monitor."""
        pass
    
    def get_system_info(self) -> None:
        """Display comprehensive system information."""
        try:
            import psutil
            
            # System info
            table = Table(title="💻 System Information", show_header=False)
            table.add_column("Property", style="cyan")
            table.add_column("Value", style="bold")
            
            table.add_row("OS", f"{platform.system()} {platform.release()}")
            table.add_row("Version", platform.version())
            table.add_row("Architecture", platform.machine())
            table.add_row("Processor", platform.processor())
            table.add_row("Hostname", platform.node())
            
            # CPU info
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            table.add_row("CPU Usage", f"{cpu_percent}%")
            table.add_row("CPU Cores", str(cpu_count))
            
            # Memory info
            memory = psutil.virtual_memory()
            table.add_row("Total RAM", self.format_bytes(memory.total))
            table.add_row("Available RAM", self.format_bytes(memory.available))
            table.add_row("RAM Usage", f"{memory.percent}%")
            
            console.print(table)
            
        except ImportError:
            console.print("[yellow]Install psutil for detailed system info: pip install psutil[/yellow]")
            # Fallback to basic info
            table = Table(title="💻 System Information", show_header=False)
            table.add_column("Property", style="cyan")
            table.add_column("Value", style="bold")
            
            table.add_row("OS", f"{platform.system()} {platform.release()}")
            table.add_row("Architecture", platform.machine())
            table.add_row("Hostname", platform.node())
            
            console.print(table)
        except Exception as e:
            console.print(f"[red]Error getting system info: {e}[/red]")
    
    def format_bytes(self, bytes_val: int) -> str:
        """Format bytes in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_val < 1024.0:
                return f"{bytes_val:.1f} {unit}"
            bytes_val /= 1024.0
        return f"{bytes_val:.1f} PB"
    
    def get_disk_usage(self) -> None:
        """Display disk usage for all drives."""
        try:
            import psutil
            
            table = Table(title="💾 Disk Usage", show_header=True)
            table.add_column("Drive", style="cyan")
            table.add_column("Total", justify="right")
            table.add_column("Used", justify="right")
            table.add_column("Free", justify="right")
            table.add_column("Usage", justify="right")
            
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    table.add_row(
                        partition.device,
                        self.format_bytes(usage.total),
                        self.format_bytes(usage.used),
                        self.format_bytes(usage.free),
                        f"{usage.percent}%"
                    )
                except PermissionError:
                    continue
            
            console.print(table)
            
        except ImportError:
            console.print("[yellow]Install psutil for disk info: pip install psutil[/yellow]")
        except Exception as e:
            console.print(f"[red]Error getting disk usage: {e}[/red]")
    
    def list_processes(self, limit: int = 20) -> None:
        """Display running processes."""
        try:
            import psutil
            
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Sort by CPU usage
            processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
            
            table = Table(title=f"⚙️ Top {limit} Processes", show_header=True)
            table.add_column("PID", style="dim", width=8)
            table.add_column("Name", style="bold")
            table.add_column("CPU %", justify="right")
            table.add_column("Memory %", justify="right")
            
            for proc in processes[:limit]:
                table.add_row(
                    str(proc.get('pid', 'N/A')),
                    proc.get('name', 'Unknown'),
                    f"{proc.get('cpu_percent', 0):.1f}%",
                    f"{proc.get('memory_percent', 0):.1f}%"
                )
            
            console.print(table)
            
        except ImportError:
            console.print("[yellow]Install psutil for process info: pip install psutil[/yellow]")
        except Exception as e:
            console.print(f"[red]Error listing processes: {e}[/red]")
    
    def get_network_info(self) -> None:
        """Display network interface information."""
        try:
            import psutil
            import socket
            
            table = Table(title="🌐 Network Information", show_header=True)
            table.add_column("Interface", style="cyan")
            table.add_column("Address", style="bold")
            table.add_column("Netmask")
            
            for interface, addrs in psutil.net_if_addrs().items():
                for addr in addrs:
                    if addr.family == socket.AF_INET:
                        table.add_row(
                            interface,
                            addr.address,
                            addr.netmask or "N/A"
                        )
            
            console.print(table)
            
            # Network stats
            net_io = psutil.net_io_counters()
            stats_table = Table(title="📊 Network Statistics", show_header=False)
            stats_table.add_column("Metric", style="cyan")
            stats_table.add_column("Value", style="bold")
            
            stats_table.add_row("Bytes Sent", self.format_bytes(net_io.bytes_sent))
            stats_table.add_row("Bytes Received", self.format_bytes(net_io.bytes_recv))
            stats_table.add_row("Packets Sent", str(net_io.packets_sent))
            stats_table.add_row("Packets Received", str(net_io.packets_recv))
            
            console.print(stats_table)
            
        except ImportError:
            console.print("[yellow]Install psutil for network info: pip install psutil[/yellow]")
        except Exception as e:
            console.print(f"[red]Error getting network info: {e}[/red]")
    
    def get_environment_vars(self, filter_str: Optional[str] = None) -> None:
        """Display environment variables."""
        table = Table(title="🔐 Environment Variables", show_header=True)
        table.add_column("Variable", style="cyan", no_wrap=True)
        table.add_column("Value", style="white")
        
        env_vars = sorted(os.environ.items())
        
        for key, value in env_vars:
            if filter_str and filter_str.lower() not in key.lower():
                continue
            # Truncate long values
            display_value = value[:80] + "..." if len(value) > 80 else value
            table.add_row(key, display_value)
        
        console.print(table)
