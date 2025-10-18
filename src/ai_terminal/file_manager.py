"""
File browser and management utilities.
Provides visual directory browsing and file management operations.
"""

import os
import shutil
import glob
from datetime import datetime
from pathlib import Path
from typing import List, Tuple, Optional
from rich.console import Console
from rich.table import Table
from rich.tree import Tree
from rich.panel import Panel
from rich.columns import Columns

console = Console()


class FileManager:
    """Handles file browsing and management operations."""
    
    def __init__(self):
        """Initialize the file manager."""
        self.bookmarks = {}
        self.command_history = []
        self.load_bookmarks()
    
    def load_bookmarks(self):
        """Load saved bookmarks from config file."""
        bookmark_file = Path.home() / '.ai_terminal_bookmarks'
        if bookmark_file.exists():
            try:
                with open(bookmark_file, 'r') as f:
                    for line in f:
                        if '=' in line:
                            name, path = line.strip().split('=', 1)
                            self.bookmarks[name] = path
            except Exception as e:
                console.print(f"[yellow]Could not load bookmarks: {e}[/yellow]")
    
    def save_bookmarks(self):
        """Save bookmarks to config file."""
        bookmark_file = Path.home() / '.ai_terminal_bookmarks'
        try:
            with open(bookmark_file, 'w') as f:
                for name, path in self.bookmarks.items():
                    f.write(f"{name}={path}\n")
        except Exception as e:
            console.print(f"[yellow]Could not save bookmarks: {e}[/yellow]")
    
    def format_size(self, size: int) -> str:
        """Format file size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"
    
    def format_date(self, timestamp: float) -> str:
        """Format timestamp in readable format."""
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime('%Y-%m-%d %H:%M')
    
    def list_directory(self, path: str, show_hidden: bool = False, detailed: bool = True) -> None:
        """
        Display directory contents in a formatted table.
        
        Args:
            path: Directory path to list
            show_hidden: Whether to show hidden files
            detailed: Show detailed information
        """
        try:
            entries = []
            for entry in os.scandir(path):
                if not show_hidden and entry.name.startswith('.'):
                    continue
                
                try:
                    stat = entry.stat()
                    entries.append({
                        'name': entry.name,
                        'type': 'DIR' if entry.is_dir() else 'FILE',
                        'size': stat.st_size if entry.is_file() else 0,
                        'modified': stat.st_mtime,
                        'is_dir': entry.is_dir()
                    })
                except Exception:
                    continue
            
            # Sort: directories first, then alphabetically
            entries.sort(key=lambda x: (not x['is_dir'], x['name'].lower()))
            
            if detailed:
                table = Table(title=f"📁 {path}", show_header=True, header_style="bold cyan")
                table.add_column("Type", style="dim", width=6)
                table.add_column("Name", style="bold")
                table.add_column("Size", justify="right", style="cyan")
                table.add_column("Modified", style="dim")
                
                for entry in entries:
                    name_style = "bold blue" if entry['is_dir'] else "white"
                    icon = "📁" if entry['is_dir'] else "📄"
                    table.add_row(
                        entry['type'],
                        f"{icon} {entry['name']}",
                        self.format_size(entry['size']) if not entry['is_dir'] else "",
                        self.format_date(entry['modified'])
                    )
                
                console.print(table)
                console.print(f"\n[dim]Total: {len(entries)} items[/dim]")
            else:
                # Simple column view
                names = [f"[bold blue]{e['name']}[/]" if e['is_dir'] else e['name'] for e in entries]
                console.print(Columns(names, equal=True, expand=True))
                
        except PermissionError:
            console.print(f"[red]Permission denied: {path}[/red]")
        except Exception as e:
            console.print(f"[red]Error listing directory: {e}[/red]")
    
    def tree_view(self, path: str, max_depth: int = 2) -> None:
        """
        Display directory tree structure.
        
        Args:
            path: Root directory path
            max_depth: Maximum depth to traverse
        """
        def add_tree_items(tree_obj, dir_path: Path, current_depth: int = 0):
            if current_depth >= max_depth:
                return
            
            try:
                items = sorted(dir_path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
                for item in items[:50]:  # Limit to 50 items per directory
                    if item.is_dir():
                        branch = tree_obj.add(f"📁 [bold blue]{item.name}[/]")
                        add_tree_items(branch, item, current_depth + 1)
                    else:
                        tree_obj.add(f"📄 {item.name}")
            except PermissionError:
                tree_obj.add("[red]Permission denied[/]")
            except Exception:
                pass
        
        try:
            root_path = Path(path)
            tree = Tree(f"📁 [bold cyan]{root_path}[/]")
            add_tree_items(tree, root_path)
            console.print(tree)
        except Exception as e:
            console.print(f"[red]Error creating tree: {e}[/red]")
    
    def search_files(self, path: str, pattern: str, recursive: bool = True) -> List[str]:
        """
        Search for files matching pattern.
        
        Args:
            path: Directory to search in
            pattern: File pattern (wildcards supported)
            recursive: Search subdirectories
            
        Returns:
            List of matching file paths
        """
        try:
            if recursive:
                search_pattern = os.path.join(path, '**', pattern)
                matches = glob.glob(search_pattern, recursive=True)
            else:
                search_pattern = os.path.join(path, pattern)
                matches = glob.glob(search_pattern)
            
            return matches
        except Exception as e:
            console.print(f"[red]Search error: {e}[/red]")
            return []
    
    def get_disk_info(self, path: str) -> None:
        """Display disk usage information."""
        try:
            import psutil
            disk = psutil.disk_usage(path)
            
            table = Table(title="💾 Disk Information", show_header=True)
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="bold")
            
            table.add_row("Total", self.format_size(disk.total))
            table.add_row("Used", self.format_size(disk.used))
            table.add_row("Free", self.format_size(disk.free))
            table.add_row("Usage", f"{disk.percent}%")
            
            console.print(table)
        except ImportError:
            console.print("[yellow]Install psutil for disk info: pip install psutil[/yellow]")
        except Exception as e:
            console.print(f"[red]Error getting disk info: {e}[/red]")
    
    def file_info(self, path: str) -> None:
        """Display detailed information about a file or directory."""
        try:
            p = Path(path)
            if not p.exists():
                console.print(f"[red]Path does not exist: {path}[/red]")
                return
            
            stat = p.stat()
            
            table = Table(title=f"📋 File Information: {p.name}", show_header=False)
            table.add_column("Property", style="cyan")
            table.add_column("Value", style="bold")
            
            table.add_row("Full Path", str(p.absolute()))
            table.add_row("Type", "Directory" if p.is_dir() else "File")
            table.add_row("Size", self.format_size(stat.st_size))
            table.add_row("Created", self.format_date(stat.st_ctime))
            table.add_row("Modified", self.format_date(stat.st_mtime))
            table.add_row("Accessed", self.format_date(stat.st_atime))
            
            if p.is_file():
                table.add_row("Extension", p.suffix or "None")
            
            console.print(table)
            
        except Exception as e:
            console.print(f"[red]Error getting file info: {e}[/red]")
    
    def copy_file(self, src: str, dst: str) -> bool:
        """Copy file or directory."""
        try:
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
            console.print(f"[green]✓ Copied: {src} → {dst}[/green]")
            return True
        except Exception as e:
            console.print(f"[red]Copy failed: {e}[/red]")
            return False
    
    def move_file(self, src: str, dst: str) -> bool:
        """Move/rename file or directory."""
        try:
            shutil.move(src, dst)
            console.print(f"[green]✓ Moved: {src} → {dst}[/green]")
            return True
        except Exception as e:
            console.print(f"[red]Move failed: {e}[/red]")
            return False
    
    def delete_file(self, path: str, recursive: bool = False) -> bool:
        """Delete file or directory."""
        try:
            if os.path.isdir(path):
                if recursive:
                    shutil.rmtree(path)
                else:
                    os.rmdir(path)
            else:
                os.remove(path)
            console.print(f"[green]✓ Deleted: {path}[/green]")
            return True
        except Exception as e:
            console.print(f"[red]Delete failed: {e}[/red]")
            return False
    
    def create_directory(self, path: str) -> bool:
        """Create a new directory."""
        try:
            os.makedirs(path, exist_ok=True)
            console.print(f"[green]✓ Created directory: {path}[/green]")
            return True
        except Exception as e:
            console.print(f"[red]Failed to create directory: {e}[/red]")
            return False
    
    def preview_file(self, path: str, lines: int = 20) -> None:
        """Preview text file contents."""
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = []
                for i, line in enumerate(f):
                    if i >= lines:
                        break
                    content.append(line.rstrip())
                
                panel = Panel(
                    '\n'.join(content),
                    title=f"📄 {Path(path).name}",
                    border_style="cyan"
                )
                console.print(panel)
                
        except Exception as e:
            console.print(f"[red]Preview failed: {e}[/red]")
