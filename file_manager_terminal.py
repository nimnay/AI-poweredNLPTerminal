"""
AI-powered Windows File Manager Terminal
----------------------------------------

A comprehensive file management system with AI-powered natural language commands,
visual file browsing, system monitoring, and advanced file operations.

Features:
- Natural language command generation with Gemini AI
- Visual file browser with detailed information
- Built-in file operations (copy, move, delete, search)
- System monitoring and information
- Bookmarks and command history
- Directory navigation with cd support
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import Optional

import google.generativeai as genai
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

# Import our modules
sys.path.insert(0, str(Path(__file__).parent / 'src'))
from ai_terminal.file_manager import FileManager
from ai_terminal.system_monitor import SystemMonitor

console = Console()


class FileManagerTerminal:
    """Enhanced AI terminal with file management capabilities."""
    
    def __init__(self):
        """Initialize the terminal."""
        self.cwd = os.getcwd()
        self.file_manager = FileManager()
        self.system_monitor = SystemMonitor()
        self.command_history = []
        self.setup_gemini()
        
    def setup_gemini(self):
        """Configure Gemini API."""
        api_key = self.load_api_key()
        if not api_key:
            console.print("[red]Error: GEMINI_API_KEY not found![/red]")
            console.print("[yellow]Set it as environment variable or in .env file[/yellow]")
            exit(1)
        
        genai.configure(api_key=api_key)
        try:
            self.model = genai.GenerativeModel('models/gemini-2.5-flash')
            console.print(f"[green]✓ Gemini AI ready[/green]")
        except Exception as e:
            console.print(f"[red]Error initializing AI: {e}[/red]")
            exit(1)
    
    def load_api_key(self) -> Optional[str]:
        """Load API key from environment or .env file."""
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            return api_key
        
        env_path = Path(__file__).parent / '.env'
        if env_path.exists():
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('GEMINI_API_KEY=') and not line.startswith('#'):
                        api_key = line.split('=', 1)[1].strip()
                        if api_key and api_key != 'your-api-key-here':
                            return api_key
        return None
    
    def show_help(self):
        """Display help information with available commands."""
        help_text = """
# 🤖 AI File Manager Terminal - Help

## Built-in Commands (Direct, no AI)

### Navigation & Viewing
- `ls` / `ll` / `dir` - List directory contents (detailed)
- `ls simple` - Simple list view
- `tree` - Show directory tree structure
- `cd <path>` - Change directory
- `pwd` - Show current directory
- `info <file>` - Show detailed file/directory information
- `preview <file>` - Preview text file contents

### File Operations
- `copy <src> <dst>` - Copy file or directory
- `move <src> <dst>` - Move/rename file or directory
- `delete <path>` - Delete file or directory
- `mkdir <path>` - Create directory
- `search <pattern>` - Search for files matching pattern

### System Information
- `sysinfo` - Show system information
- `disk` - Show disk usage for all drives
- `processes` - Show running processes
- `network` - Show network information
- `env [filter]` - Show environment variables

### Bookmarks
- `bookmark <name>` - Save current directory as bookmark
- `bookmarks` - List all bookmarks
- `jump <name>` - Jump to bookmarked directory

### Other
- `help` - Show this help
- `clear` - Clear screen
- `history` - Show command history
- `exit` / `quit` - Exit terminal

## Natural Language Commands (AI-Powered)

For any other input, the AI will convert your natural language to Windows commands:
- "find all python files"
- "count lines in main.py"
- "show me files larger than 1MB"
- "search for TODO in all files"

**Note**: All AI-generated commands require confirmation before execution.
        """
        console.print(Markdown(help_text))
    
    def process_builtin_command(self, user_input: str) -> bool:
        """
        Process built-in commands that don't need AI.
        
        Returns:
            True if command was handled, False if should use AI
        """
        parts = user_input.strip().split(maxsplit=1)
        cmd = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""
        
        # Help
        if cmd in ['help', '?']:
            self.show_help()
            return True
        
        # Navigation
        if cmd == 'cd':
            target = arg or os.path.expanduser('~')
            try:
                new_cwd = os.path.abspath(os.path.join(self.cwd, target))
                if os.path.isdir(new_cwd):
                    self.cwd = new_cwd
                    console.print(f"[green]📁 {self.cwd}[/green]")
                else:
                    console.print(f"[red]Directory not found: {new_cwd}[/red]")
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
            return True
        
        if cmd == 'pwd':
            console.print(f"[cyan]{self.cwd}[/cyan]")
            return True
        
        # File listing
        if cmd in ['ls', 'll', 'dir']:
            detailed = 'simple' not in arg.lower()
            show_hidden = '-a' in arg or '--all' in arg
            self.file_manager.list_directory(self.cwd, show_hidden, detailed)
            return True
        
        if cmd == 'tree':
            max_depth = 2
            if arg and arg.isdigit():
                max_depth = int(arg)
            self.file_manager.tree_view(self.cwd, max_depth)
            return True
        
        # File info
        if cmd == 'info':
            if not arg:
                console.print("[yellow]Usage: info <file>[/yellow]")
            else:
                path = os.path.join(self.cwd, arg)
                self.file_manager.file_info(path)
            return True
        
        if cmd == 'preview':
            if not arg:
                console.print("[yellow]Usage: preview <file> [lines][/yellow]")
            else:
                parts_arg = arg.split()
                filename = parts_arg[0]
                lines = int(parts_arg[1]) if len(parts_arg) > 1 else 20
                path = os.path.join(self.cwd, filename)
                self.file_manager.preview_file(path, lines)
            return True
        
        # File operations
        if cmd == 'copy':
            args = arg.split()
            if len(args) < 2:
                console.print("[yellow]Usage: copy <source> <destination>[/yellow]")
            else:
                src = os.path.join(self.cwd, args[0])
                dst = os.path.join(self.cwd, args[1])
                self.file_manager.copy_file(src, dst)
            return True
        
        if cmd == 'move':
            args = arg.split()
            if len(args) < 2:
                console.print("[yellow]Usage: move <source> <destination>[/yellow]")
            else:
                src = os.path.join(self.cwd, args[0])
                dst = os.path.join(self.cwd, args[1])
                self.file_manager.move_file(src, dst)
            return True
        
        if cmd == 'delete':
            if not arg:
                console.print("[yellow]Usage: delete <path>[/yellow]")
            else:
                path = os.path.join(self.cwd, arg)
                confirm = input(f"Delete {path}? [y/N]: ").lower() == 'y'
                if confirm:
                    self.file_manager.delete_file(path, recursive=True)
            return True
        
        if cmd == 'mkdir':
            if not arg:
                console.print("[yellow]Usage: mkdir <path>[/yellow]")
            else:
                path = os.path.join(self.cwd, arg)
                self.file_manager.create_directory(path)
            return True
        
        if cmd == 'search':
            if not arg:
                console.print("[yellow]Usage: search <pattern>[/yellow]")
            else:
                matches = self.file_manager.search_files(self.cwd, arg, recursive=True)
                if matches:
                    console.print(f"[green]Found {len(matches)} matches:[/green]")
                    for match in matches[:50]:  # Limit display
                        console.print(f"  {match}")
                    if len(matches) > 50:
                        console.print(f"[dim]... and {len(matches) - 50} more[/dim]")
                else:
                    console.print("[yellow]No matches found[/yellow]")
            return True
        
        # System info
        if cmd == 'sysinfo':
            self.system_monitor.get_system_info()
            return True
        
        if cmd == 'disk':
            self.system_monitor.get_disk_usage()
            return True
        
        if cmd == 'processes':
            limit = int(arg) if arg and arg.isdigit() else 20
            self.system_monitor.list_processes(limit)
            return True
        
        if cmd == 'network':
            self.system_monitor.get_network_info()
            return True
        
        if cmd == 'env':
            self.system_monitor.get_environment_vars(arg if arg else None)
            return True
        
        # Bookmarks
        if cmd == 'bookmark':
            if not arg:
                console.print("[yellow]Usage: bookmark <name>[/yellow]")
            else:
                self.file_manager.bookmarks[arg] = self.cwd
                self.file_manager.save_bookmarks()
                console.print(f"[green]✓ Bookmarked {self.cwd} as '{arg}'[/green]")
            return True
        
        if cmd == 'bookmarks':
            if self.file_manager.bookmarks:
                console.print("[bold cyan]📖 Bookmarks:[/]")
                for name, path in self.file_manager.bookmarks.items():
                    console.print(f"  {name}: {path}")
            else:
                console.print("[yellow]No bookmarks saved[/yellow]")
            return True
        
        if cmd == 'jump':
            if not arg:
                console.print("[yellow]Usage: jump <bookmark>[/yellow]")
            elif arg in self.file_manager.bookmarks:
                self.cwd = self.file_manager.bookmarks[arg]
                console.print(f"[green]📁 {self.cwd}[/green]")
            else:
                console.print(f"[red]Bookmark not found: {arg}[/red]")
            return True
        
        # Utility
        if cmd == 'clear':
            console.clear()
            return True
        
        if cmd == 'history':
            if self.command_history:
                console.print("[bold cyan]Command History:[/]")
                for i, hist_cmd in enumerate(self.command_history[-20:], 1):
                    console.print(f"  {i}. {hist_cmd}")
            else:
                console.print("[yellow]No command history[/yellow]")
            return True
        
        # Not a built-in command
        return False
    
    def generate_ai_command(self, user_input: str) -> Optional[str]:
        """Generate Windows command from natural language using AI."""
        try:
            system_prompt = f"""You are a Windows CMD expert. Current directory: {self.cwd}

Rules:
1. ONLY respond with valid Windows commands
2. Never use Linux commands
3. Use Windows equivalents: ls→dir, grep→findstr, etc.
4. Return ONLY the command, no explanations"""
            
            prompt = f'''{system_prompt}

Examples:
Input: "count lines in file.txt"
Output: find /c /v "" < file.txt

Input: "search for errors"
Output: findstr "error" *.log

Input: "{user_input}"
Output:'''
            
            response = self.model.generate_content(prompt)
            return response.text.strip('"\'\n `')
        except Exception as e:
            console.print(f"[red]AI Error: {e}[/red]")
            return None
    
    def execute_command(self, command: str) -> str:
        """Execute Windows command in current directory."""
        try:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                capture_output=True,
                text=True,
                cwd=self.cwd
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Error: {e.stderr.strip()}"
    
    def is_dangerous(self, command: str) -> bool:
        """Check if command is dangerous."""
        dangerous = ["rm", "del", "format", "diskpart", "shutdown", "reboot",
                    "del /s", "rd /s", "reg delete", "wmic", "netsh"]
        return any(d in command.lower() for d in dangerous)
    
    def run(self):
        """Main terminal loop."""
        # Welcome banner
        banner = Panel.fit(
            "[bold green]🤖 AI File Manager Terminal[/]\n"
            f"[dim]Current directory: {self.cwd}[/]\n"
            "[yellow]Type 'help' for commands or use natural language[/]",
            border_style="green"
        )
        console.print(banner)
        
        while True:
            try:
                # Show prompt with current directory
                dir_name = Path(self.cwd).name or self.cwd
                user_input = input(f"\n[{dir_name}]> ").strip()
                
                if not user_input:
                    continue
                
                # Exit commands
                if user_input.lower() in ['exit', 'quit']:
                    console.print("[yellow]Goodbye! 👋[/yellow]")
                    break
                
                # Add to history
                self.command_history.append(user_input)
                
                # Try built-in commands first
                if self.process_builtin_command(user_input):
                    continue
                
                # Use AI for natural language commands
                console.print("[dim]🤖 Generating command...[/dim]")
                command = self.generate_ai_command(user_input)
                
                if not command:
                    console.print("[red]Failed to generate command[/red]")
                    continue
                
                # Show command and confirm
                is_danger = self.is_dangerous(command)
                if is_danger:
                    console.print("[red]⚠️  WARNING: Potentially dangerous command[/red]")
                
                console.print(f"[yellow]>> {command}[/yellow]")
                confirm = input("Execute? [y/N]: ").lower() == 'y'
                
                if not confirm:
                    console.print("[yellow]Cancelled[/yellow]")
                    continue
                
                # Execute
                output = self.execute_command(command)
                if output:
                    console.print(f"[green]{output}[/green]")
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Use 'exit' to quit[/yellow]")
                continue
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
                continue


def main():
    """Entry point."""
    try:
        terminal = FileManagerTerminal()
        terminal.run()
    except Exception as e:
        console.print(f"[red]Fatal error: {e}[/red]")
        exit(1)


if __name__ == "__main__":
    main()
