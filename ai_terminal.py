import ollama
from rich.console import Console

console = Console()

def ask_llama(prompt, model="gemma:2b"):
    try:
        response = ollama.generate(
            model=model,
            prompt=prompt,
            stream=False
        )
        return response["response"]
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        return None
    
if __name__ == "__main__":
    test_prompt = "Convert to bash command: list files"
    result = ask_llama(test_prompt)
    console.print(f"[green]LLM Response:[/green] {result}")