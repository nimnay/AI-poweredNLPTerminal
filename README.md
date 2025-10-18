# 🤖 AI-Powered NLP Terminal

A natural language interface for your Windows terminal powered by Google's Gemini AI. Control your computer, navigate files, and run programs using plain English commands.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

## ✨ Features

- **🗣️ Natural Language Processing**: Type commands in plain English
- **🔄 Real-Time Execution**: Commands run directly on your system with persistent directory navigation
- **🛡️ Safety First**: Automatic detection of dangerous commands with confirmation prompts
- **⚡ Direct Command Mode**: Bypass AI with `!` prefix for instant command execution
- **📁 Advanced File Management**: Visual file browser with search, tree view, and detailed info
- **💻 System Monitoring**: Real-time CPU, memory, and disk usage information
- **🎨 Rich UI**: Beautiful terminal output with colors and formatting
- **📚 Smart History**: Track command history and bookmarks

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Windows 10/11
- Google Gemini API key ([Get one free here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository**
   ```powershell
   git clone https://github.com/nimnay/AI-poweredNLPTerminal.git
   cd AI-poweredNLPTerminal
   ```

2. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Set up your API key**
   
   Copy the example environment file:
   ```powershell
   copy .env.example .env
   ```
   
   Edit `.env` and add your Gemini API key:
   ```
   GEMINI_API_KEY=your-actual-api-key-here
   ```

4. **Run the terminal**
   ```powershell
   python ai_terminal_assistant.py
   ```

## 📖 Usage

### Three Terminal Versions

#### 1. **ai_terminal_assistant.py** ⭐ (Recommended)
The main terminal with the best balance of features:
- Persistent directory navigation
- Auto-balances quotes in paths
- Direct command mode with `!` prefix
- Smart command generation
- Safety confirmations for dangerous operations

```powershell
python ai_terminal_assistant.py
```

#### 2. **ai_terminal.py**
Simpler version with confirmations for every command:
- Always asks before execution
- Good for learning and testing
- Includes fuzzy matching features

```powershell
python ai_terminal.py
```

#### 3. **file_manager_terminal.py**
Advanced file manager with built-in commands:
- Visual file browser
- Built-in commands (ls, tree, info, search)
- System monitoring dashboard
- Bookmarks and history tracking

```powershell
python file_manager_terminal.py
```

### Command Examples

#### Natural Language Commands

```bash
# Navigation
"show my files"
"go to desktop"
"go to my documents"
"go back up"
"go to CPSC 1010"

# File Operations
"create folder test"
"list all python files"
"delete old.txt"
"copy file.txt to backup.txt"
"show me all files modified today"

# System Information
"show disk usage"
"what's my current directory"
"list running processes"

# Program Execution
"run python script.py"
"execute test.py"
"open notepad"
```

#### Direct Commands (! prefix)

For faster execution, prefix any command with `!` to bypass AI:

```bash
!dir
!cd ..
!python script.py
!type file.txt
!ipconfig
```

#### Built-in Commands (file_manager_terminal.py)

```bash
ls              # List directory contents
tree            # Show directory tree
info file.txt   # Detailed file information
search *.py     # Search for files
sysinfo         # System information
diskinfo        # Disk usage
help            # Show help
exit            # Quit terminal
```

## 🛠️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your-api-key-here
```

Or set as a system environment variable:

```powershell
setx GEMINI_API_KEY "your-api-key-here"
```

### Customization

Edit the starting directory in any terminal script:

```python
def __init__(self):
    self.cwd = os.getcwd()  # Change this to your preferred starting directory
```

## 🔒 Safety Features

The terminal includes several safety mechanisms:

- **Dangerous Command Detection**: Automatically identifies potentially harmful commands
- **Confirmation Prompts**: Asks for explicit confirmation before executing dangerous operations
- **Command Preview**: Shows the translated command before execution
- **Quote Auto-Balancing**: Fixes unbalanced quotes in file paths

Dangerous keywords detected:
- `rm`, `del`, `format`, `diskpart`
- `shutdown`, `reboot`, `rmdir`
- `reg delete`, `wmic`, and more

## 📁 Project Structure

```
AI-poweredNLPTerminal/
├── ai_terminal_assistant.py     ⭐ Main terminal (recommended)
├── ai_terminal.py                Simple version with confirmations
├── file_manager_terminal.py      Advanced file manager
├── requirements.txt              Python dependencies
├── .env                          Your API key (not in git)
├── .env.example                  API key template
├── .gitignore                    Git ignore rules
├── LICENSE                       MIT License
├── README.md                     This file
├── PROJECT_SUMMARY.md            Project cleanup summary
├── QUICKSTART.md                 Quick reference guide
└── src/
    └── ai_terminal/
        ├── file_manager.py       File operations module
        └── system_monitor.py     System monitoring module
```

## 🐛 Troubleshooting

### Common Issues

**Problem:** `GEMINI_API_KEY not found`
```
Solution: Ensure .env file exists in project root and contains your API key
```

**Problem:** `Directory not found`
```
Solution: Use exact capitalization for folder names: "CPSC 1010" not "cpsc 1010"
```

**Problem:** Import errors with psutil
```
Solution: Install psutil: pip install psutil
```

**Problem:** Command not executing
```
Solution: Check if quotes are balanced in paths with spaces
         The terminal auto-fixes this in ai_terminal_assistant.py
```

### Getting Help

Type `help` in any terminal to see available commands and examples.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini AI** - For powering the natural language processing
- **Rich Library** - For beautiful terminal formatting
- **psutil** - For system monitoring capabilities

## 📧 Contact

Project Link: [https://github.com/nimnay/AI-poweredNLPTerminal](https://github.com/nimnay/AI-poweredNLPTerminal)

---

**⚠️ Important Notes:**

- This terminal executes real commands on your system. Always review commands before confirming execution.
- Keep your API key secure and never commit it to version control.
- The terminal respects your current directory and maintains state across commands.
- For folders with spaces, use exact names: `"My Folder"` not `"my folder"`

**💡 Pro Tips:**

- Use `!` prefix for commands you use frequently to bypass AI translation
- Type `help` to see all available features
- Check `QUICKSTART.md` for a quick reference guide
- The AI learns from context - be specific in your requests