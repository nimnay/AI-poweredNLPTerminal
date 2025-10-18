# 🤖 AI-Powered NLP Terminal# 🤖 AI-Powered File Manager Terminal



> Transform natural language into Windows commands using Google's Gemini AI. Navigate your computer, manage files, and execute programs by simply describing what you want to do in plain English.> A comprehensive file management system combining AI-powered natural language commands with powerful built-in file operations and system monitoring.



## ✨ Features[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

- **Natural Language Commands** - Type what you want in plain English

- **Persistent Navigation** - Directory changes persist across commands## 🌟 Description

- **Real Command Execution** - Runs actual commands on your file system

- **Safety Layer** - Confirms dangerous commands before executionTransform how you manage files and navigate your computer! This AI-powered terminal provides:

- **Direct Command Mode** - Use `!` prefix to bypass AI for direct execution- **Natural Language Interface**: Describe what you want, AI generates the command

- **Smart Quoting** - Automatically handles file/folder names with spaces- **Visual File Browser**: Beautiful, detailed directory listings and tree views

- **Built-in File Operations**: Copy, move, delete, search without typing complex commands

## 🚀 Quick Start- **System Monitoring**: Check disk space, processes, network, system info

- **Smart Navigation**: Bookmarks, command history, directory jumping

### 1. Installation- **Safety First**: All dangerous operations require confirmation



```powershell## ✨ Features

# Clone the repository

git clone https://github.com/nimnay/AI-poweredNLPTerminal.git### 🧠 AI-Powered Commands

cd AI-poweredNLPTerminal- Converts plain English to Windows CMD commands using Google Gemini

- Context-aware: knows your current directory

# Install dependencies- Smart fallbacks for Linux-style commands

pip install -r requirements.txt

```### 📁 File Management

- **Visual Browser**: Detailed file listings with sizes, dates, types

### 2. API Key Setup- **Tree View**: Hierarchical directory structure

- **File Operations**: Copy, move, rename, delete with confirmations

Create a `.env` file in the project root:- **Search**: Find files by pattern with recursive search

- **Preview**: View file contents directly in terminal

```env

GEMINI_API_KEY=your-api-key-here### 💻 System Information

```- Real-time system stats (CPU, RAM, disk)

- Process monitoring

**Get your Gemini API key:** https://makersuite.google.com/app/apikey- Network interface information

- Environment variables browser

### 3. Run the Terminal- Disk usage for all drives



```powershell### 🎯 Productivity

python ai_terminal_assistant.py- **Bookmarks**: Save and jump to favorite directories

```- **Command History**: Track and replay commands

- **Smart Navigation**: cd, pwd, and quick directory jumps

## 📖 Usage- **Batch Operations**: Execute multiple commands efficiently



### Natural Language Commands## 📦 Prerequisites



Just type what you want in plain English:- Python 3.10 or higher

- Google Gemini API key ([Get one free](https://makersuite.google.com/app/apikey))

```bash- Windows OS (currently optimized for Windows)

~\Documents$ : show my files

🤖 Translating...## 🚀 Quick Start

→ dir

[shows directory listing]### 1. Installation



~\Documents$ : go to desktop```bash

🤖 Translating...# Clone the repository

→ cd C:\Users\YourName\Desktopgit clone https://github.com/nimnay/AI-poweredNLPTerminal.git

Changed to: C:\Users\YourName\Desktopcd AI-poweredNLPTerminal



~\Desktop$ : create folder myproject# Create virtual environment

🤖 Translating...python -m venv .venv

→ mkdir myproject.\.venv\Scripts\activate

[creates folder]

# Install dependencies

~\Desktop$ : list all python filespip install -r requirements.txt

🤖 Translating...```

→ dir *.py /s /b

[lists all .py files recursively]### 2. Configure API Key

```

**Option A: Environment Variable**

### Direct Command Mode```bash

setx GEMINI_API_KEY "your-api-key-here"

Prefix commands with `!` to execute without AI translation:# Restart terminal after setting

```

```bash

~\Projects$ : !dir /w**Option B: .env File**

[executes dir /w immediately]```bash

# Create .env file in project root

~\Projects$ : !cd ..echo GEMINI_API_KEY=your-api-key-here > .env

[goes up one directory]```



~\Projects$ : !python script.py### 3. Run the Terminal

[runs Python script directly]

``````bash

python file_manager_terminal.py

### Built-in Commands```



```bash## 📖 Usage Guide

help, ?       # Show help information

exit, quit    # Exit the terminal### Built-in Commands (No AI, Instant)

```

#### Navigation & Viewing

## 💡 Example Commands```bash

ls                    # List directory (detailed)

### Navigationls simple             # Simple list view

tree                  # Directory tree structure

```tree 3                # Tree with depth 3

"go to my documents"cd <path>             # Change directory

"show desktop folder"  cd ..                 # Go up one level

"navigate to C:\Windows"pwd                   # Print working directory

"go up one level"```

"go to CPSC 1010"           # Handles spaces automatically

```#### File Information

```bash

### File Operationsinfo <file>           # Detailed file information

preview <file>        # Preview text file (first 20 lines)

```preview <file> 50     # Preview 50 lines

"list all files"```

"show python files"

"find text files"#### File Operations

"create folder test"```bash

"copy file.txt to backup.txt"copy <src> <dst>      # Copy file/directory

"delete old.txt"move <src> <dst>      # Move/rename

"rename temp to final"delete <path>         # Delete (with confirmation)

```mkdir <path>          # Create directory

search <pattern>      # Find files matching pattern

### Informationsearch *.py           # Find all Python files

```

```

"show current directory"#### System Information

"list files with details"```bash

"show disk space"sysinfo               # Complete system information

"what files are here"disk                  # Disk usage for all drives

```processes             # Top 20 processes

processes 50          # Top 50 processes

### Running Programsnetwork               # Network interfaces and stats

env                   # All environment variables

```env PATH              # Filter by name

"run python script.py"```

"execute test.py"

"open notepad"#### Bookmarks & History

``````bash

bookmark myproject    # Bookmark current directory

## 🛡️ Safety Featuresbookmarks             # List all bookmarks

jump myproject        # Jump to bookmarked directory

### Dangerous Command Detectionhistory               # Show command history

```

Commands that could harm your system require explicit confirmation:

#### Utilities

```bash```bash

~\Documents$ : delete important.txthelp                  # Show all commands

🤖 Translating...clear                 # Clear screen

→ del important.txtexit / quit           # Exit terminal

⚠️  DANGEROUS COMMAND```

Execute this command? [y/n] (n): _

```### Natural Language Commands (AI-Powered)



**Protected operations:**For any other input, the AI will convert your natural language to Windows commands:

- File/folder deletion (`del`, `rmdir`)

- Disk operations (`format`, `diskpart`)```bash

- System commands (`shutdown`, `reboot`)"find all python files in subdirectories"

- Registry modifications (`reg delete`)"show me files larger than 1MB"

"count lines in main.py"

### Command Preview"search for TODO in all files"

"list files modified today"

Every command is shown before execution:"show me the largest files"

```

```bash

~\Documents$ : create folder test**Note**: All AI-generated commands show a preview and require confirmation before execution.

🤖 Translating...

→ mkdir test## 🎨 Example Session

[command executes automatically for safe operations]

``````

🤖 AI File Manager Terminal

## 🎯 How It WorksCurrent directory: C:\Projects

Type 'help' for commands or use natural language

```

Your Input → Gemini AI → Windows Command → Real Execution → Output[Projects]> ls

```📁 C:\Projects

┏━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓

1. **You type** in natural language: "show my documents"┃ Type ┃ Name            ┃ Size    ┃ Modified        ┃

2. **AI translates** to Windows command: `cd C:\Users\Name\Documents && dir`┡━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩

3. **System executes** the actual command on your file system│ DIR  │ 📁 MyApp        │         │ 2025-10-17 14:30│

4. **Output displayed** with styled formatting│ DIR  │ 📁 Website      │         │ 2025-10-16 09:15│

│ FILE │ 📄 README.md    │ 2.3 KB  │ 2025-10-17 11:20│

## 📁 Project Structure└──────┴─────────────────┴─────────┴─────────────────┘



```[Projects]> cd MyApp

AI-poweredNLPTerminal/

├── ai_terminal_assistant.py    # Main terminal (recommended)[MyApp]> "find all python files"

├── ai_terminal.py               # Simple version with confirmations🤖 Generating command...

├── file_manager_terminal.py    # Advanced file manager version>> dir *.py /s /b

├── requirements.txt             # Python dependenciesExecute? [y/N]: y

├── .env                         # API key configurationC:\Projects\MyApp\main.py

├── README.md                    # This fileC:\Projects\MyApp\utils.py

└── src/C:\Projects\MyApp\config.py

    └── ai_terminal/

        ├── file_manager.py      # File operations module[MyApp]> bookmark myapp

        └── system_monitor.py    # System monitoring module✓ Bookmarked C:\Projects\MyApp as 'myapp'

```

[MyApp]> sysinfo

### Which File to Use?💻 System Information

┌────────────┬──────────────────────────────┐

- **`ai_terminal_assistant.py`** ⭐ **RECOMMENDED**│ OS         │ Windows 11                   │

  - Persistent directory navigation│ CPU Usage  │ 15.2%                        │

  - Natural language interface│ RAM Usage  │ 45.8%                        │

  - Direct command mode with `!`└────────────┴──────────────────────────────┘

  - Best for general use```



- **`ai_terminal.py`**## 🛡️ Safety Features

  - Simple version

  - Always requires confirmation- ✅ **User Confirmation**: Every command requires explicit confirmation

  - Good for learning/experimenting- ⚠️ **Danger Detection**: Warns about destructive commands (del, format, shutdown)

- 🔍 **Command Preview**: See the actual command before execution

- **`file_manager_terminal.py`**- 📋 **Command History**: Track what's been executed

  - Advanced file manager- 🚫 **Validation**: Checks for invalid paths and permissions

  - Built-in commands (ls, tree, info)

  - System monitoring features## 🔧 Configuration

  - Best for power users

### Environment Variables

## 🔧 Configuration

| Variable | Description | Required |

### API Key Options|----------|-------------|----------|

| `GEMINI_API_KEY` | Google Gemini API key | Yes |

**Option 1: `.env` file** (Recommended)

```env### Bookmarks

GEMINI_API_KEY=your-api-key-here

```Bookmarks are automatically saved to `~/.ai_terminal_bookmarks` and persist across sessions.



**Option 2: Environment Variable**## 📁 Project Structure

```powershell

setx GEMINI_API_KEY "your-api-key-here"```

# Restart terminal after settingAI-poweredNLPTerminal/

```├── file_manager_terminal.py    # Main enhanced terminal

├── ai_terminal.py               # Original simple terminal

### Starting Directory├── src/

│   └── ai_terminal/

The terminal starts in the directory where you run it:│       ├── file_manager.py      # File operations & browsing

│       └── system_monitor.py    # System information

```powershell├── requirements.txt             # Python dependencies

# Start in Documents├── .env.example                 # Example environment file

cd C:\Users\YourName\Documents├── .gitignore                   # Git ignore rules

python ai_terminal_assistant.py└── README.md                    # This file

```

# Start in Projects- All commands require user confirmation before execution

cd C:\Projects- Dangerous commands (del, format, shutdown, etc.) show a red warning

python ai_terminal_assistant.py- Commands are displayed before execution for review
```

## 📋 Requirements

- Python 3.10 or higher
- Windows OS (uses Windows CMD commands)
- Google Gemini API key (free tier available)

### Dependencies

```
google-generativeai>=0.8.3
rich>=13.0.0
psutil>=5.9.0
```

Install with:
```powershell
pip install -r requirements.txt
```

## ⚠️ Important Notes

### This is a REAL Terminal

- **Commands execute on your actual system**
- **File changes are permanent** (no undo)
- **You have your normal user permissions**
- **No sandboxing or virtualization**

### Best Practices

✅ **DO:**
- Start in a safe directory (like Documents or a test folder)
- Review dangerous commands before confirming
- Use `!` prefix for critical commands you want exact control over
- Keep your API key secure (don't commit `.env` to git)

❌ **DON'T:**
- Run without understanding what commands do
- Execute system-level operations without review
- Share your API key publicly
- Use for irreversible system operations without backup

## 🆚 Comparison with Standard Terminal

| Feature | Standard Terminal | AI Terminal |
|---------|------------------|-------------|
| Input | Exact command syntax | Natural language |
| Learning Curve | High (memorize commands) | Low (just describe) |
| Typos | Command fails | AI interprets |
| File Spaces | Manual quoting required | Auto-handled |
| Safety | No warnings | Dangerous command detection |
| Preview | Shows command before execution | Shows command before execution |

## 🐛 Troubleshooting

### "GEMINI_API_KEY not found"
- Ensure `.env` file exists in project root
- Check file contains: `GEMINI_API_KEY=your-key`
- No quotes around the key value
- File is named exactly `.env` (not `.env.txt`)

### "Directory not found"
- Check folder name spelling and capitalization
- Use exact names: `go to "CPSC 1010"` (with proper capitalization)
- Try absolute path: `go to C:\Users\Name\Folder`

### "Permission denied"
- Some folders require administrator access
- Right-click terminal and "Run as administrator"
- Check folder permissions in Windows

### AI generates wrong command
- Be more specific in your request
- Use direct mode: `!dir` instead of "list files"
- Check that you're in the right directory

### Quote issues with folder names
- The terminal auto-balances quotes
- Use exact folder names as they appear on disk
- If issues persist, use direct mode: `!cd "folder name"`

## 🤝 Contributing

This is a personal project, but suggestions and improvements are welcome!

1. Fork the repository
2. Create your feature branch
3. Test your changes
4. Submit a pull request

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- **Google Gemini API** - AI-powered command translation
- **Rich Library** - Beautiful terminal output
- **Python Community** - Amazing tools and libraries

## 📞 Support

Having issues? Here's how to get help:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review your `.env` file setup
3. Verify your Gemini API key is valid
4. Open an issue on GitHub

## 🎓 Learn More

- [Google Gemini API Documentation](https://ai.google.dev/docs)
- [Windows Command Reference](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/windows-commands)
- [Rich Library Documentation](https://rich.readthedocs.io/)

---

**Made with ❤️ for making terminals more human-friendly**

```powershell
python ai_terminal_assistant.py
```

🚀 Start controlling your computer with natural language today!
