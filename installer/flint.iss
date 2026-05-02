; Inno Setup script for Flint (Windows)
; Build prerequisite:
;   - Run build_windows.ps1 first
;   - Confirm dist\Flint\Flint.exe exists

#define MyAppName "Flint"
#define MyAppVersion "0.1.2"
#define MyAppPublisher "Henry Marcais"
#define MyAppExeName "Flint.exe"

[Setup]
AppId={{8D8C0F57-5C8F-4D10-95A8-3046559E5AF3}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputDir=..\dist-installer
OutputBaseFilename=Flint-Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "..\dist\Flint\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

[Dirs]
; Match app behavior: default project folder in Documents\flint
Name: "{userdocs}\flint"

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
