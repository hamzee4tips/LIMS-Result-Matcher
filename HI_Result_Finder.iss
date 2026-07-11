#define MyAppName "HI Result Finder"
#define MyAppVersion "3.0.1"
#define MyAppPublisher "Hamza Isah"
#define MyAppURL "https://github.com/hamzee4tips"
#define MyAppExeName "HI Result Finder.exe"

[Setup]
AppId={{7E29D88F-93F9-4B35-91F0-7F9B3A5B2101}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

DefaultDirName={autopf}\HI Result Finder
DefaultGroupName=HI Result Finder

OutputDir=release
OutputBaseFilename=HI_Result_Finder_v3.0.1_Setup

Compression=lzma
SolidCompression=yes

WizardStyle=modern

DisableProgramGroupPage=yes

PrivilegesRequired=admin

SetupIconFile=assets\icons\hi_result_finder.ico

UninstallDisplayIcon={app}\HI Result Finder.exe

ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a Desktop shortcut"; GroupDescription: "Additional Icons:"; Flags: unchecked

[Files]

Source: "dist\HI Result Finder\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]

Name: "{group}\HI Result Finder"; Filename: "{app}\HI Result Finder.exe"

Name: "{autodesktop}\HI Result Finder"; Filename: "{app}\HI Result Finder.exe"; Tasks: desktopicon

[Run]

[Run]
Filename: "{app}\HI Result Finder.exe"; \
WorkingDir: "{app}"; \
Description: "Launch HI Result Finder"; \
Flags: nowait postinstall skipifsilent