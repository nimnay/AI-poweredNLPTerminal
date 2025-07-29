import ollama
from rich.console import Console

console = Console()

def ask_llama(prompt, model="gemma:2b"):
    try:
        response = ollama.generate(
            model=model,
            prompt=prompt,
            system=""
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
    Input: "show running processes"
    Output: "ps aux"

    Input: "{user_input}"
    Output:"""
    
    return ask_llama(prompt).strip()

if __name__ == "__main__":
    while True:
        user_input = input("> ")
        if user_input.lower() in ["exit", "quit"]:
            break
        command = interpret_command(user_input)
        print(f"Command: {command}")
