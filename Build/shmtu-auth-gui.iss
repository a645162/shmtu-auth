; -- shmtu-auth-gui.iss --

[Setup]
AppName=shmtu-auth
AppVersion=2.0.0
WizardStyle=modern
DefaultDirName={autopf}\shmtu-auth
; Since no icons will be created in "{group}", we don't need the wizard
; to ask for a Start Menu folder name:
DisableProgramGroupPage=yes
UninstallDisplayIcon={app}\shmtu_auth_windows_gui.exe

Compression=none
;Compression=lzma2
;SolidCompression=yes

OutputDir=Output\inno
OutputBaseFilename=setup-shmtu-auth-gui

[Files]
Source: "shmtu_auth_windows_gui\shmtu_auth_windows_gui\*"; DestDir: "{app}"; Flags: recursesubdirs
; Source: "..\LICENSE"; DestDir: "{app}"; Flags: isreadme

[Icons]
Name: "{autoprograms}\shmtu-auth"; Filename: "{app}\shmtu_auth_windows_gui.exe"
Name: "{autodesktop}\shmtu-auth"; Filename: "{app}\shmtu_auth_windows_gui.exe"
