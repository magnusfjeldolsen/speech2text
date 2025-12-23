# Setup Guide - Speech to Text Dictation App

Complete setup instructions for Windows with VSCode.

## Prerequisites

### 1. Install Python
- Download Python 3.9 or higher from [python.org](https://www.python.org/downloads/)
- **Important**: During installation, check "Add Python to PATH"
- Verify installation:
  ```powershell
  python --version
  ```

### 2. Install Git (Optional, for version control)
- Download from [git-scm.com](https://git-scm.com/downloads)
- Or install via Chocolatey: `choco install git`

### 3. Install VSCode
- Download from [code.visualstudio.com](https://code.visualstudio.com/)

## Project Setup

### Option 1: Automated Setup (Recommended)

1. Open VSCode
2. Open this project folder (`File > Open Folder`)
3. Open the integrated terminal (`Terminal > New Terminal` or `` Ctrl+` ``)
4. Ensure PowerShell execution policy allows scripts:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
5. Run the setup script:
   ```powershell
   .\setup.ps1
   ```

The script will:
- Create a virtual environment in `venv/`
- Activate the virtual environment
- Upgrade pip
- Install all required dependencies from `requirements.txt`

### Option 2: Manual Setup

1. Open VSCode and open this project folder
2. Open the integrated terminal (`` Ctrl+` ``)
3. Create virtual environment:
   ```powershell
   python -m venv venv
   ```
4. Activate virtual environment:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

   If you get an execution policy error, run:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
   Then try activating again.

5. Upgrade pip:
   ```powershell
   python -m pip install --upgrade pip
   ```

6. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

## VSCode Configuration

### 1. Select Python Interpreter

1. Press `Ctrl+Shift+P` to open Command Palette
2. Type "Python: Select Interpreter"
3. Choose the interpreter from `.\venv\Scripts\python.exe`

### 2. Recommended Extensions

Install these VSCode extensions for better development experience:
- **Python** (by Microsoft) - Essential for Python development
- **Pylance** (by Microsoft) - Advanced Python language support

Install via:
1. Click the Extensions icon in the sidebar (or `Ctrl+Shift+X`)
2. Search for each extension
3. Click "Install"

## Running the Application

### From VSCode

1. Ensure virtual environment is activated (you should see `(venv)` in terminal)
2. Open `dictation_app.py`
3. Press `F5` to run with debugger, or:
4. In terminal, run:
   ```powershell
   python dictation_app.py
   ```

### From PowerShell (Outside VSCode)

1. Navigate to project directory:
   ```powershell
   cd C:\Python\speech2text\speech2text
   ```
2. Activate virtual environment:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
3. Run application:
   ```powershell
   python dictation_app.py
   ```

## Using the Application

1. **Select Language**: Choose "Norsk" or "English (US)" from dropdown
2. **Record**: Click "▶ Start" to begin recording
3. **Stop**: Click "■ Stopp" to stop recording and transcribe
4. **Clear**: Click "🗑 Tøm" to clear all transcribed text
5. **Transcribed text**:
   - Automatically copied to clipboard
   - Displayed in the text area
   - Each new recording appends on a new line
   - Scrollable for long transcriptions

## Troubleshooting

### "Python is not recognized"
- Python is not in your PATH
- Reinstall Python and check "Add Python to PATH"

### "Execution policy" error
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Virtual environment not activating
Try using forward slashes:
```powershell
./venv/Scripts/Activate.ps1
```

### "No module named xyz" errors
Ensure virtual environment is activated and reinstall:
```powershell
pip install -r requirements.txt
```

### Missing microphone permissions
- Windows Settings > Privacy > Microphone
- Enable microphone access for desktop apps

### First run downloads model
- The first time you run the app, Whisper downloads the "base" model (~140MB)
- This is normal and only happens once
- Model is cached for future runs

## Development Notes

### Dependencies
- `openai-whisper` - Speech recognition model
- `torch` - Deep learning framework (required by Whisper)
- `sounddevice` - Audio recording
- `numpy` - Audio data handling
- `scipy` - Audio file operations (optional, not used in current version)
- `pyperclip` - Clipboard operations

### Configuration
Edit `dictation_app.py` to change:
- `SAMPLE_RATE`: Audio sample rate (default: 16000)
- `MODEL_NAME`: Whisper model size - "tiny", "base", "small", "medium", "large"
  - Larger models are more accurate but slower
  - "base" is a good balance for real-time use

### No ffmpeg Required
This app passes audio directly to Whisper as NumPy arrays, bypassing the need for ffmpeg installation.

## Git Setup (Optional)

If you want to version control your project:

1. Initialize repository (if not already done):
   ```powershell
   git init
   ```

2. Add files:
   ```powershell
   git add .
   ```

3. Commit:
   ```powershell
   git commit -m "Initial commit"
   ```

4. Add remote and push:
   ```powershell
   git remote add origin <your-repo-url>
   git branch -M main
   git push -u origin main
   ```

Note: The `.gitignore` file already excludes `venv/` and other heavy files.
