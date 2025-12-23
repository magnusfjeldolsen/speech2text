# Building a Standalone Executable

This guide explains how to create a single-file executable of the Speech to Text app using PyInstaller.

## Prerequisites

Ensure you have completed the setup in [SETUP.md](SETUP.md) and your virtual environment is activated.

## Step 1: Install PyInstaller

PyInstaller is already included in `requirements.txt`. If you haven't installed it yet:

```powershell
pip install pyinstaller
```

Or reinstall all requirements:

```powershell
pip install -r requirements.txt
```

## Step 2: Build the Executable

### Basic Build (Recommended for Testing)

From your project directory with the virtual environment activated:

```powershell
pyinstaller --onefile --windowed dictation_app.py
```

**Flags explained:**
- `--onefile` - Creates a single executable file instead of a folder with dependencies
- `--windowed` - Hides the console window (GUI-only app)

### Advanced Build with Custom Options

For better control and smaller file size:

```powershell
pyinstaller --onefile --windowed --name "SpeechToText" --icon=app.ico --clean dictation_app.py
```

**Additional flags:**
- `--name "SpeechToText"` - Custom executable name
- `--icon=app.ico` - Custom icon (if you have an .ico file)
- `--clean` - Clean PyInstaller cache before building

### Build with Hidden Imports (If Needed)

If the basic build has issues with missing modules:

```powershell
pyinstaller --onefile --windowed --hidden-import=whisper --hidden-import=sounddevice --hidden-import=tkinter dictation_app.py
```

## Step 3: Locate the Executable

After the build completes:

1. The executable will be in the `dist/` folder
2. The file will be named `dictation_app.exe` (or your custom name)
3. You can move this file anywhere and run it independently

```
project/
├── dist/
│   └── dictation_app.exe    <- Your standalone executable
├── build/                    <- Build artifacts (can be deleted)
├── dictation_app.spec        <- PyInstaller spec file (can be customized)
└── ...
```

## Step 4: Test the Executable

1. Navigate to the `dist/` folder
2. Double-click `dictation_app.exe` to run
3. Test all features:
   - Recording with Space bar
   - Stopping and transcription
   - Clear with Delete key
   - Language switching

## Important Notes

### First Run Model Download

The first time the executable runs, it will download the Whisper model (~140MB). This is normal and happens automatically. The model is cached in:

```
C:\Users\<YourUsername>\.cache\whisper
```

Subsequent runs will use the cached model.

### File Size

The executable will be large (200-500MB) because it includes:
- Python interpreter
- PyTorch libraries
- Whisper model loader
- All dependencies

This is normal for PyInstaller applications with ML dependencies.

### Antivirus Warnings

Some antivirus software may flag PyInstaller executables as suspicious. This is a false positive. To resolve:

1. Add the executable to your antivirus exclusion list
2. Or build on the target machine to avoid issues

## Troubleshooting

### Build Fails with "Module not found"

Add missing modules explicitly:

```powershell
pyinstaller --onefile --windowed --hidden-import=<module_name> dictation_app.py
```

### Executable Won't Start

1. Try running from command line to see errors:
   ```powershell
   cd dist
   .\dictation_app.exe
   ```

2. Remove the `--windowed` flag to see console output:
   ```powershell
   pyinstaller --onefile dictation_app.py
   ```

### "Failed to execute script" Error

This usually means a dependency is missing. Try:

```powershell
pyinstaller --onefile --windowed --collect-all whisper --collect-all torch dictation_app.py
```

### Executable is Too Large

The large size is expected due to PyTorch. To reduce size slightly:

1. Use the "tiny" or "small" Whisper model in the code
2. Use `--exclude-module` for unused packages (advanced)

## Distribution

To share your executable:

1. Zip the `dictation_app.exe` file
2. Include a README noting:
   - First run downloads the Whisper model (~140MB)
   - Requires microphone permissions
   - Windows Defender may need approval

3. Optionally include the model cache to avoid first-run download:
   - Copy `C:\Users\<YourUsername>\.cache\whisper` folder
   - Users should place it in their own cache location

## Advanced: Customizing the Build

### Creating a Custom .spec File

For advanced customization, edit the generated `.spec` file:

1. Run PyInstaller once to generate the .spec file
2. Edit `dictation_app.spec`
3. Rebuild using the spec file:
   ```powershell
   pyinstaller dictation_app.spec
   ```

### Example .spec Customization

Add to `dictation_app.spec` to include data files:

```python
datas=[
    ('README.md', '.'),
],
```

## Clean Up

After building, you can delete:

```powershell
Remove-Item -Recurse -Force build
Remove-Item dictation_app.spec
```

Keep the `dist/` folder with your executable.

## Alternative: Directory Build

If the single-file build has issues, create a folder distribution instead:

```powershell
pyinstaller --windowed dictation_app.py
```

This creates a `dist/dictation_app/` folder with the executable and all dependencies. The folder is larger but sometimes more reliable.

## Summary

**Quick build command:**
```powershell
pyinstaller --onefile --windowed --name "SpeechToText" dictation_app.py
```

**Output location:**
```
dist/SpeechToText.exe
```

**Next steps:**
- Test the executable thoroughly
- Distribute to users
- Remember users need microphone access on first run
