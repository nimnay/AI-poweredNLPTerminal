"""
AI-powered Windows NLP Terminal
------------------------------

This script provides a natural language interface to the Windows command line using Google's Gemini API.

Features:
- Converts plain English instructions into valid Windows CMD commands using Gemini AI.
- Uses the rich library for styled terminal output.
- Detects and warns about potentially dangerous commands before execution.
- Asks for user confirmation before running any command.

Usage:
- Set your GEMINI_API_KEY environment variable
- Run the script and type your command in plain English.
- Type 'exit' or 'quit' to leave the terminal.
"""

# Import required libraries
import os  # For environment variables
import subprocess  # For running shell commands
import google.generativeai as genai  # For Gemini API
from rich.console import Console  # For styled terminal output
from pathlib import Path  # For file path handling

# Initialize the rich console for pretty printing
console = Console()

# Configure Gemini API - Load from .env file if exists
def load_api_key():
    # First check system environment variable
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        return api_key
    
    # Try to load from .env file
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

GEMINI_API_KEY = load_api_key()
if not GEMINI_API_KEY:
    console.print("[red]Error: GEMINI_API_KEY not found![/red]")
    console.print("[yellow]Either:[/yellow]")
    console.print("[yellow]1. Set it as environment variable: setx GEMINI_API_KEY \"your-api-key-here\"[/yellow]")
    console.print("[yellow]2. Or add it to .env file in the project directory[/yellow]")
    exit(1)

genai.configure(api_key=GEMINI_API_KEY)

# Use Gemini 2.5 Flash (latest stable model)
try:
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    console.print(f"[green]✓ Using Gemini 2.5 Flash[/green]")
except Exception as e:
    console.print(f"[red]Error initializing model: {e}[/red]")
    exit(1)


# Ask Gemini to convert a natural language prompt to a Windows CMD command
def ask_gemini(prompt):
    try:
        system_prompt = """You are a Windows CMD expert. Rules:
1. ONLY respond with valid Windows commands, don't output 'output:' or any explanation
2. Never use Linux commands
3. Use these equivalents:
   ls → dir /b
   grep → findstr
   wc -l → find /c /v ""
   chmod → icacls
   rm → del
4. Return ONLY the command, nothing else"""
        
        full_prompt = f"{system_prompt}\n\n{prompt}"
        response = model.generate_content(full_prompt)
        
        # Return the generated command, stripping extra quotes and newlines
        return response.text.strip('"\'\n `')
    except Exception as e:
        # Print error in red if something goes wrong
        console.print(f"[red]Error calling Gemini API: {e}[/red]")
        return None


# Prepare a prompt for Gemini with examples and the user's input
def interpret_command(user_input):
    prompt = f'''Convert to Windows CMD:
        Input: "count lines in file"
        Output: find /c /v "" < file.txt

        Input: "search for errors"
        Output: findstr "error" *.log

        Input: "{user_input}"
        Output:'''
    return ask_gemini(prompt)


# Execute the generated Windows command and return its output
def execute_command(command):
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        # Return the command output
        return result.stdout
    except subprocess.CalledProcessError as e:
        # Return error message if command fails
        return f"Error: {e.stderr.strip()}"

# Check if the command is potentially dangerous
def is_dangerous(command):
    # List of dangerous commands that could harm the system
    DANGEROUS = ["rm", "del", "format", "diskpart", "shutdown", "reboot","del /s", "rd /s", "reg delete",
        "wmic ", "netsh ", "vssadmin" ]
    # Check if any dangerous command is present in the input
    return any(d in command.lower() for d in DANGEROUS)

def confirm_execution(cmd):
    console.print(f"[yellow]>> {cmd}[/yellow]")
    return input("Execute? [y/N]: ").lower() == 'y'

# Main loop: interactively accept user input and process commands
if __name__ == "__main__":
    console.print("[bold green]Windows AI Terminal[/]")  # Welcome message
    while True:
        try:
            user_input = input("> ")  # Get user input
            if user_input.lower() in ["exit", "quit"]:
                break  # Exit on 'exit' or 'quit'

            command = interpret_command(user_input)  # Convert input to CMD command
            
            # Check if command generation failed
            if not command:
                console.print("[red]Failed to generate command. Please try again.[/red]")
                continue

            # Fallback: If a Linux command slips through, re-ask for Windows version
            if any(linux_cmd in command for linux_cmd in ["ls ", "grep ", "wc "]):
                command = interpret_command(f"Windows version of: {user_input}")
                if not command:
                    console.print("[red]Failed to generate Windows command.[/red]")
                    continue

            # Always ask for confirmation, but warn if dangerous
            if is_dangerous(command):
                console.print("[red]WARNING:[/] Potentially destructive command")
                if not confirm_execution(command):
                    continue
            else:
                if not confirm_execution(command):
                    continue

            output = execute_command(command)  # Run the command
            console.print(f"[green]{output}[/green]")  # Show the output
            
        except KeyboardInterrupt:
            console.print("\n[yellow]Use 'exit' or 'quit' to terminate[/yellow]")
            continue
        except Exception as e:
            console.print(f"[red]Unexpected error: {e}[/red]")