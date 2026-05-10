; =======================================================================
; EVRENSEL SETUP ŞABLONU
; Her yeni projede SADECE bu "PROJE AYARLARI" bölümünü değiştir.
; Alt kısımdaki kodlara dokunmana gerek yoktur.
; =======================================================================

#define MyAppName "ChiperNora"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Neuron Solution"
#define MyAppURL "https://www.tuakpina.com/"
#define MyAppExeName "ChiperNora.exe"

; BURASI ÇOK ÖNEMLİ: PyInstaller'ın ürettiği klasörün adı
#define MyBuildDir "dist\ChiperNora"

; Eğer setup ikonun yoksa bu satırın başına noktalı virgül (;) koyarak kapatabilirsin
#define MySetupIcon "icons\setup.ico"

[Setup]
; KRİTİK UYARI: Her yepyeni projede Inno Setup menüsünden "Tools -> Generate GUID" 
; tıklayarak aşağıdaki AppId kısmına o yeni projeye özel yeni bir kod yapıştır. 
; Aksi takdirde Windows, farklı projelerini birbirinin güncellemesi sanır!
AppId={{BURAYA-YENİ-BİR-GUID-YAPIŞTIR}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

; Programın kurulacağı varsayılan klasör (Program Files \ Proje Adı)
DefaultDirName={autopf}\{#MyAppName}
UninstallDisplayIcon={app}\{#MyAppExeName}

; Mimari Ayarları
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
DisableProgramGroupPage=yes
PrivilegesRequired=lowest

; Çıktı Ayarları (Setup dosyasını script'in çalıştığı yere kaydeder)
OutputDir=.
OutputBaseFilename=ChiperNora Setup
SetupIconFile={#MySetupIcon}
SolidCompression=yes
WizardStyle=modern windows11

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "turkish"; MessagesFile: "compiler:Languages\Turkish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; 1. Önce sadece EXE dosyasını alır
Source: "{#MyBuildDir}\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

; 2. Sonra EXE'nin yanındaki tüm alt klasörleri (_internal vb.) ve dosyaları kopyalar
Source: "{#MyBuildDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOT: Sistem dosyaları paylaşımlıysa "ignoreversion" bayrağını dikkatli kullanın.

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent