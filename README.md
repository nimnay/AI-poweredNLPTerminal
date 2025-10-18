# AI-poweredNLPTerminal

## Description
An AI-powered terminal that converts natural language into executable Windows CMD commands using Google's Gemini API.

## Features
- Natural language to Windows CMD command conversion
- Gemini AI-powered command generation
- Command execution with safety checks
- Dangerous command detection and warnings
- Colorized output with Rich library

## Prerequisites
- Python 3.10+
- Google Gemini API key

## Installation
```bash
# Get your Gemini API key from https://makersuite.google.com/app/apikey

# Set up Python environment
python -m venv venv
.\venv\Scripts\activate   # Windows

# Install dependencies
pip install google-generativeai rich
```

## Setup
```bash
# Set your Gemini API key as an environment variable
setx GEMINI_API_KEY "your-api-key-here"

# Restart your terminal for the environment variable to take effect
```

## Usage
```bash
python ai_terminal.py
```

Then type your commands in natural language:
- "list all files in current directory"
- "find all python files"
- "count lines in ai_terminal.py"
- "search for TODO in all files"

Type `exit` or `quit` to close the terminal.

## Safety Features
- All commands require user confirmation before execution
- Dangerous commands (del, format, shutdown, etc.) show a red warning
- Commands are displayed before execution for review