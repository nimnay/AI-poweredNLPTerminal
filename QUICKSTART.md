# 🚀 Quick Reference

## Setup (One Time)

```powershell
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create .env file
copy .env.example .env

# 3. Edit .env and add your Gemini API key
notepad .env
```

## Run

```powershell
python ai_terminal_assistant.py
```

## Commands

### Natural Language
```
"show my files"
"go to desktop"
"create folder test"
"list all python files"
"delete old.txt"
"go to CPSC 1010"
```

### Direct Mode (! prefix)
```
!dir
!cd ..
!python script.py
!type file.txt
```

### Built-in
```
help    # Show help
exit    # Quit terminal
```

## Tips

✅ **Use exact folder names:** `go to "CPSC 1010"` (with correct capitalization)
✅ **Spaces handled automatically:** Just type the folder name as-is
✅ **Direct commands for speed:** `!dir` faster than "list files"
✅ **Safety first:** Dangerous commands require confirmation

## Common Examples

```bash
# Navigation
go to my documents
go back up
go to C:\Windows

# Files
show all files
create folder myproject
copy file.txt to backup.txt
delete temp.txt

# Programs
run python script.py
execute test.py
open notepad
```

## Troubleshooting

**Problem:** "GEMINI_API_KEY not found"
**Solution:** Check `.env` file exists and has your key

**Problem:** "Directory not found"
**Solution:** Use exact capitalization: `"CPSC 1010"` not `"cpsc 1010"`

**Problem:** Quote issues
**Solution:** Terminal auto-fixes unbalanced quotes

---

💡 **Pro Tip:** Type `help` in the terminal for full documentation!
