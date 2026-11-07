#define AppName "THE LAST ORDER"
#define AppVersion "1.0.0"
#define AppPublisher "Game-TLO"
#define GameRoot "Z:\\workspaces\\Game-TLO"
#define SetupOutputDir "Z:\\workspaces\\Game-TLO\\build\\installer-output"

[Setup]
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
DefaultDirName={commonpf64}\The Last Order
DefaultGroupName={#AppName}
UninstallDisplayIcon={app}\TheLastOrder.exe
OutputDir={#SetupOutputDir}
OutputBaseFilename=TheLastOrder_Setup
Compression=lzma
SolidCompression=yes
PrivilegesRequired=lowest
WizardStyle=modern
UsePreviousAppDir=no
AppCopyright=(c) 2026 {#AppPublisher}

[Files]
Source: "{#GameRoot}\dist\TheLastOrder.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#GameRoot}\README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#GameRoot}\assets\TheLastOrder.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Play THE LAST ORDER"; Filename: "{app}\TheLastOrder.exe"; WorkingDir: "{app}"; IconFilename: "{app}\TheLastOrder.ico"
Name: "{group}\Uninstall THE LAST ORDER"; Filename: "{uninstallexe}"
Name: "{commondesktop}\THE LAST ORDER"; Filename: "{app}\TheLastOrder.exe"; WorkingDir: "{app}"; IconFilename: "{app}\TheLastOrder.ico"

[Run]
Filename: "{app}\TheLastOrder.exe"; Description: "Launch THE LAST ORDER"; Flags: nowait postinstall skipifsilent
