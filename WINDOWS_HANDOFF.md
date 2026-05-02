# Flint Windows Handoff

This project is authored on macOS, but you can package a Windows installer on Windows with Cursor.

## 1) Share all code to your Windows Cursor

Recommended: use GitHub.

On Mac:

```bash
cd /Users/henrymarcais/Documents
git init
git add lang.py build_app.sh make_icon.py push_update.sh build_windows.ps1 requirements-windows.txt installer/flint.iss WINDOWS_HANDOFF.md
git commit -m "Prepare Flint cross-platform packaging files"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/flint.git
git push -u origin main
```

On Windows:

```powershell
git clone https://github.com/YOUR_USERNAME/flint.git
cd flint
```

## 2) Build Windows app bundle (.exe + folder)

From PowerShell in the project root:

```powershell
.\build_windows.ps1 -Clean
```

Result:

- `dist\Flint\Flint.exe`

Optional icon:

- Add `Flint.ico` in project root before building.

## 3) Build Windows installer (.exe installer)

Install [Inno Setup](https://jrsoftware.org/isinfo.php), then:

1. Open `installer\flint.iss`
2. Click **Build** in Inno Setup
3. Output installer appears in `dist-installer\Flint-Setup.exe`

## Important note about auto-update

Current Flint auto-update edits `lang.py` directly. In packaged Windows EXEs, that direct self-edit path may not behave the same as macOS script mode.

If Windows auto-update is required, choose one of these:

1. **Installer-based updates only** (simplest): publish a new installer each release.
2. Add a Windows-specific updater that replaces files in the install directory.
3. Change updater to fetch/replace a separate script file in `%LOCALAPPDATA%\Flint\`.

For now, packaging works; just treat auto-update as "needs Windows-specific implementation."
