import ollama
from rich.console import Console

console = Console()

def ask_llama(prompt, model="llama3"):
    try:
        response = ollama.generate(
            model=model,
            prompt=prompt,
            system="You are a Linux terminal expert. " \
            "Respond ONLY with valid bash commands.",
            stream=False
        )
        return response["response"]
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        return None
    
def interpret_command(user_input):
    prompt = f"""Convert this natural language command to a bash command.
    Respond ONLY with the command itself, no explanations.test_prompt

    Examples:
    Input: "show files"
    Output: "ls -la"

    Input: "{user_input}"
    Output:"""
    
    return ask_llama(prompt)

if __name__ == "__main__":
    console.print("[bold green]AI Terminal[/] (type 'exit' to quit)")
    while True:
        user_input = input("> ")
        if user_input.lower() in ["exit", "quit"]:
            break
            
        command = interpret_command(user_input)
        console.print(f"[yellow]>> {command}[/yellow]")

