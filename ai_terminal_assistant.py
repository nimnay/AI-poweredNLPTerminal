"""
AI-Powered Terminal Assistant
-----------------------------

A natural language terminal that executes real commands on your system.
Navigate your computer, manage files, and run programs using plain English.

Features:
- Natural language command translation via Gemini AI
- Real terminal execution with persistent directory changes
- Safety confirmations for destructive commands
- Direct command passthrough with ! prefix
- Full system access and navigation
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Optional, Tuple, List
from difflib import SequenceMatcher

import google.generativeai as genai
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()


class AITerminalAssistant:
    """
    AI-powered terminal that translates natural language to shell commands
    and executes them on your real file system.
    """
    
    def __init__(self):
        """Initialize the AI terminal assistant."""
        self.cwd = os.getcwd()  # Real current working directory
        self.command_history = []
        self.setup_gemini()
        
    def setup_gemini(self):
        """Configure Gemini AI model."""
        api_key = self.load_api_key()
        if not api_key:
            console.print("[red]Error: GEMINI_API_KEY not found![/red]")
            console.print("[yellow]Set it in .env file or as environment variable[/yellow]")
            sys.exit(1)
        
        genai.configure(api_key=api_key)
        try:
            self.model = genai.GenerativeModel('models/gemini-2.5-flash')
            console.print(f"[dim]✓ AI model ready[/dim]")
        except Exception as e:
            console.print(f"[red]Error initializing AI: {e}[/red]")
            sys.exit(1)
    
    def load_api_key(self) -> Optional[str]:
        """Load API key from environment or .env file."""
        # Check environment variable first
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            return api_key
        
        
        # Try .env file
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
    
    def get_prompt(self) -> str:
        """Get the terminal prompt showing current directory."""
        # Show home directory as ~ for brevity
        display_cwd = self.cwd.replace(str(Path.home()), '~')
        return f"[bold cyan]{display_cwd}$[/bold cyan] "
    
    def is_dangerous_command(self, command: str) -> bool:
        """Check if a command is potentially destructive."""
        dangerous_keywords = [
            'rm ', 'del ', 'format', 'diskpart', 'shutdown', 'reboot',
            'rmdir', 'rd ', 'deltree', 'erase', 'reg delete', 'wmic'
        ]
        cmd_lower = command.lower()
        return any(keyword in cmd_lower for keyword in dangerous_keywords)
    
    def fuzzy_match(self, query: str, candidates: List[str], threshold: float = 0.6) -> List[Tuple[str, float]]:
        """
        Find candidates that fuzzy match the query string.
        
        Args:
            query: The search string
            candidates: List of strings to search through
            threshold: Minimum similarity score (0-1)
            
        Returns:
            List of (candidate, score) tuples sorted by score
        """
        matches = []
        query_lower = query.lower()
        
        for candidate in candidates:
            candidate_lower = candidate.lower()
            
            # Exact match gets highest score
            if query_lower == candidate_lower:
                matches.append((candidate, 1.0))
                continue
            
            # Contains match gets high score
            if query_lower in candidate_lower:
                score = 0.9 * (len(query) / len(candidate))
                matches.append((candidate, score))
                continue
            
            # Sequence matcher for fuzzy matching
            ratio = SequenceMatcher(None, query_lower, candidate_lower).ratio()
            if ratio >= threshold:
                matches.append((candidate, ratio))
        
        # Sort by score (highest first)
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches
    
    def find_files_fuzzy(self, query: str, search_dir: Optional[str] = None) -> List[str]:
        """
        Find files/folders that fuzzy match the query.
        
        Args:
            query: The search string (can be misspelled)
            search_dir: Directory to search in (defaults to cwd)
            
        Returns:
            List of matching file/folder paths
        """
        search_path = Path(search_dir or self.cwd)
        
        if not search_path.exists():
            return []
        
        try:
            # Get all items in directory
            all_items = [item.name for item in search_path.iterdir()]
            
            # Fuzzy match against query
            matches = self.fuzzy_match(query, all_items, threshold=0.5)
            
            # Return full paths of top matches
            return [str(search_path / match[0]) for match in matches[:5]]
        except (PermissionError, OSError):
            return []
    
    def expand_fuzzy_paths(self, command: str) -> str:
        """
        DISABLED: Return command as-is without fuzzy matching.
        
        Args:
            command: Shell command
            
        Returns:
            Command unchanged (fuzzy matching disabled)
        """
        # Fuzzy matching disabled - return command as-is
        return command
    
    def translate_to_command(self, user_input: str) -> Optional[str]:
        """
        Use AI to translate natural language into a shell command.
        
        Args:
            user_input: Natural language input from user
            
        Returns:
            Shell command string or None if translation fails
        """
        try:
            system_prompt = f"""You are a Windows CMD/PowerShell expert assistant. Current directory: {self.cwd}

Your job: Convert natural language to Windows shell commands.

Rules:
1. Return ONLY the command, no explanations
2. Use Windows commands (dir, cd, copy, move, del, etc.)
3. For PowerShell features, use PowerShell syntax
4. Use full paths when ambiguous, relative paths when clear
5. If user says "my documents", use {Path.home() / 'Documents'}
6. If user says "home", use {Path.home()}
7. Chain commands with && when needed
8. Return "cd <path>" for directory changes
9. Use EXACT folder/file names as user types them
10. ALWAYS wrap paths with spaces in double quotes: cd "CPSC 1010"
11. Ensure quotes are properly closed - every opening quote needs a closing quote

Examples:
Input: "show my documents folder"
Output: cd {Path.home() / 'Documents'} && dir

Input: "list all python files"
Output: dir *.py /s /b

Input: "go to desktop"
Output: cd {Path.home() / 'Desktop'}

Input: "go to CPSC 1010"
Output: cd "CPSC 1010"

Input: "go to My Folder Name"
Output: cd "My Folder Name"

Input: "show current folder"
Output: dir

Input: "find files modified today"
Output: forfiles /P . /D +0

Input: "delete temp.txt"
Output: del temp.txt

Now translate: "{user_input}"
Command:"""
            
            response = self.model.generate_content(system_prompt)
            command = response.text.strip()
            
            # Remove markdown code blocks if present
            if command.startswith('```') and command.endswith('```'):
                command = command.strip('`')
                # Remove language identifier if present (e.g., ```bash or ```cmd)
                if '\n' in command:
                    lines = command.split('\n')
                    command = '\n'.join(lines[1:-1]) if len(lines) > 2 else command
                command = command.strip()
            
            # Remove common prefixes that AI might add
            if command.lower().startswith('output:'):
                command = command[7:].strip()
            if command.lower().startswith('command:'):
                command = command[8:].strip()
            
            # Remove single backticks at start/end only (not quotes!)
            if command.startswith('`') and command.endswith('`'):
                command = command.strip('`')
            
            # Fix unbalanced quotes - if odd number of quotes, add closing quote
            quote_count = command.count('"')
            if quote_count % 2 != 0:
                command = command + '"'
                console.print("[dim]💡 Fixed unbalanced quotes[/dim]")
            
            # Apply fuzzy file matching to the command (currently disabled)
            command = self.expand_fuzzy_paths(command)
            
            return command.strip()
            
        except Exception as e:
            console.print(f"[red]AI Error: {e}[/red]")
            return None
    
    def execute_command(self, command: str) -> Tuple[bool, str]:
        """
        Execute a shell command in the current working directory.
        
        Args:
            command: Shell command to execute
            
        Returns:
            Tuple of (success: bool, output: str)
        """
        try:
            # Check for cd command to update our working directory
            if command.strip().startswith('cd '):
                target = command.strip()[3:].strip()
                return self.change_directory(target)
            
            # Handle chained cd commands (cd X && Y)
            if ' && ' in command and 'cd ' in command.split('&&')[0]:
                parts = command.split('&&')
                cd_part = parts[0].strip()
                rest = ' && '.join(parts[1:]).strip()
                
                # Execute cd first
                success, msg = self.execute_command(cd_part)
                if not success:
                    return False, msg
                
                # Execute rest
                return self.execute_command(rest)
            
            # Execute the command in the current working directory
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=self.cwd
            )
            
            output = result.stdout if result.stdout else result.stderr
            success = result.returncode == 0
            
            return success, output.strip()
            
        except Exception as e:
            return False, f"Execution error: {str(e)}"
    
    def change_directory(self, target: str) -> Tuple[bool, str]:
        """
        Change the current working directory.
        
        Args:
            target: Target directory path
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            # Expand ~ and environment variables
            target = os.path.expanduser(target)
            target = os.path.expandvars(target)
            
            # Handle relative paths
            if not os.path.isabs(target):
                target = os.path.join(self.cwd, target)
            
            # Normalize the path
            target = os.path.normpath(target)
            
            # Check if directory exists
            if not os.path.isdir(target):
                return False, f"Directory not found: {target}"
            
            # Change directory
            os.chdir(target)
            self.cwd = os.getcwd()
            
            return True, f"Changed to: {self.cwd}"
            
        except PermissionError:
            return False, f"Permission denied: {target}"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def process_input(self, user_input: str) -> bool:
        """
        Process user input and execute appropriate action.
        
        Args:
            user_input: Raw user input
            
        Returns:
            True to continue, False to exit
        """
        user_input = user_input.strip()
        
        # Empty input
        if not user_input:
            return True
        
        # Exit commands
        if user_input.lower() in ['exit', 'quit', 'q']:
            console.print("[yellow]Goodbye! 👋[/yellow]")
            return False
        
        # Help command
        if user_input.lower() in ['help', '?']:
            self.show_help()
            return True
        
        # Direct command execution with ! prefix (bypass AI)
        if user_input.startswith('!'):
            command = user_input[1:].strip()
            console.print(f"[dim]Executing: {command}[/dim]")
            success, output = self.execute_command(command)
            
            if output:
                console.print(output)
            
            return True
        
        # Translate natural language to command using AI
        console.print("[dim]🤖 Translating...[/dim]")
        command = self.translate_to_command(user_input)
        
        if not command:
            console.print("[red]Could not translate command[/red]")
            return True
        
        # Show the generated command
        console.print(f"[yellow]→ {command}[/yellow]")
        
        # Check if dangerous and require confirmation
        if self.is_dangerous_command(command):
            console.print("[red]⚠️  DANGEROUS COMMAND[/red]")
            confirm = Prompt.ask("Execute this command?", choices=["y", "n"], default="n")
            if confirm != 'y':
                console.print("[yellow]Cancelled[/yellow]")
                return True
        
        # Execute the command
        success, output = self.execute_command(command)
        
        # Show output
        if output:
            if success:
                console.print(output)
            else:
                console.print(f"[red]{output}[/red]")
        
        # Add to history
        self.command_history.append({
            'input': user_input,
            'command': command,
            'success': success
        })
        
        return True
    
    def show_help(self):
        """Display help information."""
        help_text = """
[bold cyan]AI Terminal Assistant - Help[/bold cyan]

[bold]Usage:[/bold]
  • Type natural language commands: "show my documents"
  • Prefix with ! for direct execution: "!dir"
  • Type 'exit' or 'quit' to leave
  • Use exact file/folder names as they appear on your system

[bold]Examples:[/bold]
  [green]"show my documents folder"[/green]     → cd ~/Documents && dir
  [green]"list all python files"[/green]        → dir *.py /s /b
  [green]"go to desktop"[/green]                → cd ~/Desktop
  [green]"go to CPSC 1010"[/green]              → cd "CPSC 1010"
  [green]"create folder test"[/green]           → mkdir test
  [green]"show README.md"[/green]               → type README.md

[bold]Direct Commands:[/bold]
  [cyan]!dir /w[/cyan]           Windows directory listing
  [cyan]!cd ..[/cyan]            Go up one directory
  [cyan]!type file.txt[/cyan]    Show file content

[bold]Special:[/bold]
  [yellow]help, ?[/yellow]       Show this help
  [yellow]exit, quit[/yellow]    Exit the terminal

[bold red]⚠️  Safety:[/bold red]
  Destructive commands (rm, del, format) require confirmation.
  This executes REAL commands on your REAL file system!
  
[bold yellow]💡 Tip:[/bold yellow]
  Type folder/file names exactly as they appear.
  The AI will handle spaces and special characters automatically.
        """
        console.print(Panel(help_text, border_style="cyan"))
    
    def run(self):
        """Main terminal loop."""
        # Welcome banner
        console.print(Panel.fit(
            "[bold green]🤖 AI Terminal Assistant[/bold green]\n"
            f"[dim]Starting in: {self.cwd}[/dim]\n"
            "[yellow]Type 'help' for usage or use natural language[/yellow]",
            border_style="green"
        ))
        
        # Main loop
        while True:
            try:
                # Show prompt and get input
                prompt = self.get_prompt()
                user_input = Prompt.ask(prompt)
                
                # Process input
                if not self.process_input(user_input):
                    break
                    
            except KeyboardInterrupt:
                console.print("\n[yellow]Use 'exit' to quit[/yellow]")
                continue
            except EOFError:
                console.print("\n[yellow]Goodbye! 👋[/yellow]")
                break
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
                continue


def main():
    """Entry point for the AI terminal assistant."""
    try:
        terminal = AITerminalAssistant()
        terminal.run()
    except KeyboardInterrupt:
        console.print("\n[yellow]Goodbye! 👋[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[red]Fatal error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
