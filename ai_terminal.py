# Import required libraries
import ollama  # For AI-powered command generation
import subprocess  # For running shell commands
from rich.console import Console  # For styled terminal output

# Initialize the rich console for pretty printing
console = Console()
llmmodel = "llama3"


# Ask the Llama model to convert a natural language prompt to a Windows CMD command
def ask_llama(prompt, model=llmmodel):
    try:
        response = ollama.generate(
            model=model,
            prompt=prompt,
            system="""You are a Windows CMD expert. Rules:
            1. ONLY respond with valid Windows commands, dont output 'output:'
            2. Never use Linux commands
            3. Use these equivalents:
            ls → dir /b
            grep → findstr
            wc -l → find /c /v ""
            chmod → icacls
            rm → del""",
            stream=False
        )
        # Return the generated command, stripping extra quotes and newlines
        return response["response"].strip('"\'\n ')
    except Exception as e:
        # Print error in red if something goes wrong
        console.print(f"[red]Error: {e}[/red]")
        return None


# Prepare a prompt for the Llama model with examples and the user's input
def interpret_command(user_input):
    prompt = f'''Convert to Windows CMD:
        Input: "count lines in file"
        Output: find /c /v "" < file.txt

        Input: "search for errors"
        Output: findstr "error" *.log

        Input: "{user_input}"
        Output:'''''
    return ask_llama(prompt)


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

            # Fallback: If a Linux command slips through, re-ask for Windows version
            if any(linux_cmd in command for linux_cmd in ["ls ", "grep ", "wc "]):
                command = interpret_command(f"Windows version of: {user_input}")
            

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