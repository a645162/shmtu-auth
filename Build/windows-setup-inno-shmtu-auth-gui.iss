; -- windows-setup-inno-shmtu-auth-gui.iss --
; Author: Haomin Kong
; https://github.com/a645162/shmtu-auth

[Setup]
AppName=shmtu-auth
AppVersion=2.0.0
WizardStyle=modern
AppId={{E35937B9-C38B-4212-8DE5-AB269E484371}
DefaultDirName={pf}\shmtu-auth

; Since no icons will be created in "{group}", we don't need the wizard
; to ask for a Start Menu folder name:
DisableProgramGroupPage=yes
UninstallDisplayIcon={uninstallexe}

; File compression
; Compression=none
SolidCompression=yes

; Setup EXE output path
OutputDir=Output\Windows\INNO
OutputBaseFilename=setup-inno-shmtu-auth-gui

SetupIconFile=..\Assets\Icon\icons\Icon.ico
DisableWelcomePage=False
ShowTasksTreeLines=True
ShowLanguageDialog=no
; DisableDirPage=no

AppPublisher=Haomin Kong
AppPublisherURL=https://github.com/a645162
AppSupportURL=https://github.com/a645162/shmtu-auth
AppUpdatesURL=https://github.com/a645162/shmtu-auth

VersionInfoVersion=2.0.0
VersionInfoCompany=Haomin Kong
VersionInfoDescription=Shanghai Maritime University Edu network auto login.
VersionInfoProductName=shmtu-auth
VersionInfoCopyright=Only for study use!
VersionInfoProductVersion=020000
VersionInfoProductTextVersion=2.0.0
VersionInfoOriginalFileName=setup-inno-shmtu-auth-gui.exe

WizardSmallImageFile=..\Assets\Icon\32.bmp

LicenseFile=..\shmtu-auth-GUI-License.txt

ArchitecturesInstallIn64BitMode=x64
MinVersion=0,6.2

[Files]
Source: "Output\Windows\shmtu_auth_windows_gui\shmtu_auth_windows_gui\*"; \
	DestDir: "{app}"; \
	Flags: recursesubdirs

Source: "GPLv3.txt"; \
	DestDir: "{app}"; \
	Flags: isreadme

[Icons]
Name: "{autoprograms}\shmtu-auth"; \
	Filename: "{app}\shmtu_auth_windows_gui.exe"

Name: "{autodesktop}\shmtu-auth"; \
	Filename: "{app}\shmtu_auth_windows_gui.exe"

; {userdesktop} {commondesktop}
Name: "{commondesktop}\shmtu-auth"; \
	Filename: "{app}\shmtu_auth_windows_gui.exe"; \
	WorkingDir: "{app}"; \
	Tasks: DesktopIcon

[Tasks]
Name: "DesktopIcon"; Description: "Create desktop shortcut"

[Run]
Filename: "{app}\shmtu_auth_windows_gui.exe"; \
	Description: "Directly run program"; \
	Flags: postinstall nowait
