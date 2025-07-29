# AI Terminal

## Description
An AI-powered terminal that converts natural language into executable bash commands using locally-hosted Ollama models.

## Features
- Natural language to bash command conversion
- Self-hosted AI (Ollama)
- Command execution with safety checks
- Command history tracking
- Colorized output

## Prerequisites
- Python 3.10+
- Ollama installed
- LLM model downloaded (default: llama3)

## Installation
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull model
ollama pull llama3

# Set up Python environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# Install dependencies
pip install ollama rich