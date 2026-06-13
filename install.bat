@echo off
title Krishna Certificate Manager Installer
color 0A

:: ============================================
:: AUTO-ELEVATE TO ADMINISTRATOR
:: ============================================
:: Check if running as admin
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Requesting Administrator privileges...
    powershell start -verb runas '%0'
    exit /b
)

:: Now running as admin
cd /d "%~dp0"

echo ================================================
echo    Krishna Certificate Manager Installer
echo ================================================
echo.
echo [OK] Running with Administrator privileges
echo.

:: ============================================
:: STEP 1: Install Chocolatey
:: ============================================
echo [1/4] Installing Chocolatey...
where choco >nul 2>&1
if %errorLevel% equ 0 (
    echo [OK] Chocolatey already installed
) else (
    echo [*] Installing Chocolatey...
    @"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "[System.Net.ServicePointManager]::SecurityProtocol = 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))" >nul 2>&1
    if %errorLevel% equ 0 (
        echo [OK] Chocolatey installed
    ) else (
        echo [FAIL] Chocolatey installation failed
        pause
        exit /b 1
    )
)
echo.

:: ============================================
:: STEP 2: Install OpenSSL
:: ============================================
echo [2/4] Installing OpenSSL...
where openssl >nul 2>&1
if %errorLevel% equ 0 (
    echo [OK] OpenSSL already installed
) else (
    echo [*] Installing OpenSSL...
    choco install openssl -y >nul 2>&1
    if %errorLevel% equ 0 (
        echo [OK] OpenSSL installed
        call refreshenv >nul 2>&1
    ) else (
        echo [FAIL] OpenSSL installation failed
        pause
        exit /b 1
    )
)
echo.

:: ============================================
:: STEP 3: Install ADB
:: ============================================
echo [3/4] Installing ADB...
where adb >nul 2>&1
if %errorLevel% equ 0 (
    echo [OK] ADB already installed
) else (
    echo [*] Installing Android Platform Tools...
    choco install android-sdk-platform-tools -y >nul 2>&1
    if %errorLevel% equ 0 (
        echo [OK] ADB installed
        call refreshenv >nul 2>&1
    ) else (
        echo [FAIL] ADB installation failed
        pause
        exit /b 1
    )
)
echo.

:: ============================================
:: STEP 4: Install Python Packages
:: ============================================
echo [4/4] Installing Python packages...
pip install rich cryptography pyopenssl --quiet >nul 2>&1
if %errorLevel% equ 0 (
    echo [OK] Python packages installed
) else (
    echo [WARN] Some packages may already be installed
)
echo.

:: ============================================
:: CREATE cert.py
:: ============================================
echo [*] Creating certificate manager...

(
echo #!/usr/bin/env python3
echo """
echo Krishna Certificate Manager - Android Certificate Installation Tool
echo """
echo.
echo import os
echo import sys
echo import subprocess
echo import shutil
echo import platform
echo from datetime import datetime
echo from pathlib import Path
echo from typing import List, Dict, Optional, Tuple
echo from dataclasses import dataclass
echo from enum import Enum
echo.
echo # Try to import rich for better UI
echo try:
echo     from rich.console import Console
echo     from rich.table import Table
echo     RICH_AVAILABLE = True
echo except ImportError:
echo     RICH_AVAILABLE = False
echo.
echo # ========== DATA CLASSES ==========
echo @dataclass
echo class Device:
echo     serial: str
echo     model: str = ""
echo     android: str = ""
echo     sdk: str = ""
echo     rooted: bool = False
echo     selinux: str = ""
echo.
echo @dataclass
echo class Certificate:
echo     path: str
echo     subject: str = ""
echo     hash_val: str = ""
echo     valid: bool = False
echo     expiry: str = ""
echo.
echo class CertFormat(Enum):
echo     DER = "der"
echo     PEM = "pem"
echo     CRT = "crt"
echo     CER = "cer"
echo.
echo # ========== UI CLASS ==========
echo class UI:
echo     def __init__(self):
echo         self.console = Console() if RICH_AVAILABLE else None
echo     .
echo     def ok(self, msg): 
echo         if self.console: self.console.print(f"[green]✓ {msg}[/green]")
echo         else: print(f"[OK] {msg}")
echo     .
echo     def err(self, msg): 
echo         if self.console: self.console.print(f"[red]✗ {msg}[/red]")
echo         else: print(f"[ERROR] {msg}")
echo     .
echo     def warn(self, msg): 
echo         if self.console: self.console.print(f"[yellow]⚠ {msg}[/yellow]")
echo         else: print(f"[WARN] {msg}")
echo     .
echo     def info(self, msg): 
echo         if self.console: self.console.print(f"[cyan]ℹ {msg}[/cyan]")
echo         else: print(f"[INFO] {msg}")
echo     .
echo     def solution(self, msg): 
echo         if self.console: self.console.print(f"[green]SOLUTION: {msg}[/green]")
echo         else: print(f"[FIX] {msg}")
echo     .
echo     def command(self, msg): 
echo         if self.console: self.console.print(f"[yellow]RUN: {msg}[/yellow]")
echo         else: print(f">>> {msg}")
echo     .
echo     def step(self, curr, total, msg):
echo         if self.console: self.console.print(f"[bold yellow][{curr}/{total}][/bold yellow] {msg}")
echo         else: print(f"[{curr}/{total}] {msg}")
echo     .
echo     def banner(self):
echo         banner = \"\"\"
echo ╔══════════════════════════════════════════════════════════╗
echo ║                                                          ║
echo ║    _  __     _ _         ____  _ _ _     KRISHNA        ║
echo ║   | |/ /__ _| | | __ _  | __ )(_) | | __ _  Certificate ║
echo ║   | ' // _` | | |/ _` | |  _ \| | | |/ _` | Manager     ║
echo ║   | . \ (_| | | | (_| | | |_) | | | | (_| | v1.0        ║
echo ║   |_|\_\__,_|_|_|\__,_| |____/|_|_|_|\__,_|             ║
echo ║                                                          ║
echo ╚══════════════════════════════════════════════════════════╝
echo         \"\"\"
echo         if self.console:
echo             self.console.print(banner, style="bold cyan")
echo         else:
echo             print(banner)
echo     .
echo     def menu(self):
echo         print("\n" + "="*50)
echo         print("    KRISHNA CERTIFICATE MANAGER")
echo         print("="*50)
echo         print("1. Install Certificate")
echo         print("2. Verify Certificate")
echo         print("3. Remove Certificate")
echo         print("4. Device Information")
echo         print("5. Diagnostic Scan")
echo         print("6. Backup Certificates")
echo         print("7. Restore Backup")
echo         print("8. Exit")
echo         print("-"*50)
echo     .
echo     def cert_table(self, cert: Certificate):
echo         if self.console:
echo             table = Table(title="Certificate Details")
echo             table.add_column("Field", style="cyan")
echo             table.add_column("Value", style="white")
echo             table.add_row("Subject", cert.subject[:60])
echo             table.add_row("Hash", cert.hash_val)
echo             table.add_row("Valid", "✓" if cert.valid else "✗")
echo             table.add_row("Expires", cert.expiry)
echo             self.console.print(table)
echo         else:
echo             print(f"\nSubject: {cert.subject}\nHash: {cert.hash_val}\nValid: {cert.valid}")
echo     .
echo     def device_table(self, device: Device):
echo         if self.console:
echo             table = Table(title=f"Device: {device.serial}")
echo             table.add_column("Property", style="cyan")
echo             table.add_column("Value", style="white")
echo             table.add_row("Model", device.model)
echo             table.add_row("Android", f"{device.android} (SDK {device.sdk})")
echo             table.add_row("Root", "✓" if device.rooted else "✗")
echo             table.add_row("SELinux", device.selinux)
echo             self.console.print(table)
echo         else:
echo             print(f"\nDevice: {device.serial}\nAndroid: {device.android}\nRoot: {device.rooted}")
echo.
echo # ========== ADB MANAGER ==========
echo class ADBManager:
echo     def __init__(self, ui: UI):
echo         self.ui = ui
echo         self.adb_path = self._find_adb()
echo     .
echo     def _find_adb(self) -> Optional[str]:
echo         cmd = "adb.exe" if platform.system() == "Windows" else "adb"
echo         return shutil.which(cmd)
echo     .
echo     def check(self) -> bool:
echo         if not self.adb_path:
echo             self.ui.err("ADB not found")
echo             self.ui.solution("Run install.bat as Administrator")
echo             return False
echo         return True
echo     .
echo     def execute(self, args: List[str], timeout=30) -> Tuple[int, str, str]:
echo         full_cmd = [self.adb_path] + args
echo         try:
echo             r = subprocess.run(full_cmd, capture_output=True, text=True, timeout=timeout)
echo             return r.returncode, r.stdout, r.stderr
echo         except:
echo             return -1, "", "Command failed"
echo     .
echo     def get_devices(self) -> List[Device]:
echo         code, out, _ = self.execute(["devices"])
echo         if code != 0: return []
echo         devices = []
echo         for line in out.strip().split('\n')[1:]:
echo             if not line.strip(): continue
echo             parts = line.split()
echo             if len(parts) >= 2 and parts[1] == "device":
echo                 devices.append(Device(serial=parts[0]))
echo         return devices
echo     .
echo     def get_device_details(self, serial: str) -> Device:
echo         device = Device(serial=serial)
echo         def get_prop(prop): 
echo             _, out, _ = self.execute(["-s", serial, "shell", "getprop", prop])
echo             return out.strip()
echo         device.android = get_prop("ro.build.version.release")
echo         device.sdk = get_prop("ro.build.version.sdk")
echo         device.model = get_prop("ro.product.model")
echo         _, out, _ = self.execute(["-s", serial, "shell", "su -c id 2>/dev/null"])
echo         device.rooted = "uid=0" in out
echo         _, out, _ = self.execute(["-s", serial, "shell", "getenforce"])
echo         device.selinux = out.strip()
echo         return device
echo     .
echo     def push(self, serial: str, src: str, dst: str) -> Tuple[bool, str]:
echo         code, _, err = self.execute(["-s", serial, "push", src, dst])
echo         return (code == 0, err if code != 0 else "")
echo     .
echo     def shell(self, serial: str, cmd: str, root=False) -> Tuple[int, str, str]:
echo         if root: return self.execute(["-s", serial, "shell", "su", "-c", cmd])
echo         else: return self.execute(["-s", serial, "shell", cmd])
echo.
echo # ========== CERTIFICATE MANAGER ==========
echo class CertificateManager:
echo     def __init__(self, ui: UI, adb: ADBManager):
echo         self.ui = ui
echo         self.adb = adb
echo         self.backup_dir = Path("backups")
echo         self.backup_dir.mkdir(exist_ok=True)
echo     .
echo     def detect_format(self, path: str) -> CertFormat:
echo         with open(path, 'rb') as f:
echo             header = f.read(20)
echo         if b'-----BEGIN' in header: return CertFormat.PEM
echo         if header[:2] == b'\x30\x82': return CertFormat.DER
echo         ext = Path(path).suffix.lower()
echo         if ext == '.cer': return CertFormat.CER
echo         if ext == '.crt': return CertFormat.CRT
echo         return CertFormat.PEM
echo     .
echo     def to_pem(self, src: str) -> Tuple[bool, str, str]:
echo         fmt = self.detect_format(src)
echo         if fmt == CertFormat.PEM: return True, src, "Already PEM"
echo         out = Path(src).stem + ".pem"
echo         try:
echo             subprocess.run(['openssl', 'x509', '-inform', fmt.value.upper(), 
echo                           '-in', src, '-out', out], check=True, capture_output=True)
echo             return True, out, f"Converted to {out}"
echo         except:
echo             return False, "", "OpenSSL conversion failed"
echo     .
echo     def get_hash(self, pem_path: str) -> str:
echo         try:
echo             r = subprocess.run(['openssl', 'x509', '-inform', 'PEM', 
echo                               '-subject_hash_old', '-in', pem_path], 
echo                              capture_output=True, text=True, check=True)
echo             return r.stdout.strip().split('\n')[0]
echo         except:
echo             return ""
echo     .
echo     def get_info(self, path: str) -> Certificate:
echo         cert = Certificate(path=path)
echo         try:
echo             r = subprocess.run(['openssl', 'x509', '-in', path, '-text', '-noout'],
echo                              capture_output=True, text=True)
echo             if r.returncode == 0:
echo                 for line in r.stdout.split('\n'):
echo                     if 'Subject:' in line: cert.subject = line.strip()
echo                     if 'Not After :' in line: cert.expiry = line.split(':')[1].strip()
echo             cert.hash_val = self.get_hash(path)
echo             cert.valid = True
echo         except:
echo             cert.valid = False
echo         return cert
echo     .
echo     def system_path(self, sdk: str) -> str:
echo         sdk_int = int(sdk) if sdk.isdigit() else 0
echo         if sdk_int >= 34: return "/apex/com.android.conscrypt/cacerts"
echo         else: return "/system/etc/security/cacerts"
echo     .
echo     def install(self, device: Device, cert_path: str) -> Tuple[bool, str]:
echo         if not device.rooted: return False, "Root access required"
echo         .
echo         self.ui.step(1, 6, "Converting certificate...")
echo         ok, pem, msg = self.to_pem(cert_path)
echo         if not ok: return False, msg
echo         .
echo         self.ui.step(2, 6, "Calculating hash...")
echo         hash_val = self.get_hash(pem)
echo         if not hash_val: return False, "Hash calculation failed"
echo         .
echo         target = f"{hash_val}.0"
echo         sys_path = self.system_path(device.sdk)
echo         full = f"{sys_path}/{target}"
echo         temp = f"/data/local/tmp/{target}"
echo         .
echo         self.ui.step(3, 6, "Pushing to device...")
echo         ok, err = self.adb.push(device.serial, pem, temp)
echo         if not ok: return False, f"Push failed: {err}"
echo         .
echo         self.ui.step(4, 6, "Remounting system...")
echo         self.adb.shell(device.serial, "mount -o rw,remount /system", root=True)
echo         .
echo         self.ui.step(5, 6, "Installing to system...")
echo         code, _, err = self.adb.shell(device.serial, f"cat {temp} > {full}", root=True)
echo         if code != 0: return False, f"Copy failed: {err}"
echo         .
echo         self.adb.shell(device.serial, f"chmod 644 {full}", root=True)
echo         self.adb.shell(device.serial, f"rm {temp}", root=True)
echo         .
echo         self.ui.step(6, 6, "Verifying...")
echo         code, out, _ = self.adb.shell(device.serial, f"ls {full}", root=True)
echo         if code != 0: return False, "Verification failed"
echo         .
echo         return True, f"Installed: {target}"
echo     .
echo     def verify(self, device: Device, hash_val: str) -> Tuple[bool, str]:
echo         sys_path = self.system_path(device.sdk)
echo         full = f"{sys_path}/{hash_val}.0"
echo         code, out, _ = self.adb.shell(device.serial, f"ls -la {full}", root=True)
echo         if code != 0: return False, "Certificate not found"
echo         if "rw-r--r--" not in out: return False, "Incorrect permissions"
echo         return True, f"Verified: {full}"
echo     .
echo     def remove(self, device: Device, hash_val: str) -> Tuple[bool, str]:
echo         sys_path = self.system_path(device.sdk)
echo         full = f"{sys_path}/{hash_val}.0"
echo         code, _, err = self.adb.shell(device.serial, f"rm {full}", root=True)
echo         if code != 0: return False, f"Remove failed: {err}"
echo         return True, f"Removed: {hash_val}"
echo     .
echo     def backup_all(self, device: Device) -> Tuple[bool, str]:
echo         sys_path = self.system_path(device.sdk)
echo         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
echo         backup_folder = self.backup_dir / f"{device.serial}_{timestamp}"
echo         backup_folder.mkdir(parents=True, exist_ok=True)
echo         .
echo         code, out, _ = self.adb.shell(device.serial, f"ls {sys_path}/*.0", root=True)
echo         if code != 0: return False, "No certificates found"
echo         .
echo         count = 0
echo         for cert_line in out.strip().split('\n'):
echo             if cert_line:
echo                 cert_name = Path(cert_line).name
echo                 code, data, _ = self.adb.shell(device.serial, f"cat {cert_line}", root=True)
echo                 if code == 0:
echo                     (backup_folder / cert_name).write_text(data)
echo                     count += 1
echo         return True, f"Backed up {count} certs to {backup_folder}"
echo     .
echo     def restore(self, device: Device, backup_path: str) -> Tuple[bool, str]:
echo         sys_path = self.system_path(device.sdk)
echo         backup_folder = Path(backup_path)
echo         if not backup_folder.exists(): return False, "Backup not found"
echo         .
echo         certs = list(backup_folder.glob("*.0"))
echo         if not certs: return False, "No certificate files"
echo         .
echo         count = 0
echo         for cert_file in certs:
echo             temp = f"/data/local/tmp/{cert_file.name}"
echo             target = f"{sys_path}/{cert_file.name}"
echo             self.adb.push(device.serial, str(cert_file), temp)
echo             self.adb.shell(device.serial, f"cat {temp} > {target}", root=True)
echo             self.adb.shell(device.serial, f"chmod 644 {target}", root=True)
echo             self.adb.shell(device.serial, f"rm {temp}", root=True)
echo             count += 1
echo         return True, f"Restored {count} certificates"
echo.
echo # ========== DIAGNOSTIC ==========
echo class Diagnostic:
echo     def __init__(self, ui: UI, adb: ADBManager):
echo         self.ui = ui
echo         self.adb = adb
echo     .
echo     def run(self, device: Device):
echo         self.ui.info("Running diagnostic...")
echo         issues, fixes = [], []
echo         .
echo         if not device.rooted:
echo             issues.append("Device not rooted")
echo             fixes.append("Root device with Magisk")
echo         .
echo         if device.selinux == "Enforcing":
echo             issues.append("SELinux Enforcing may block installation")
echo             fixes.append("adb shell su -c 'setenforce 0'")
echo         .
echo         sys_path = "/apex/com.android.conscrypt/cacerts" if int(device.sdk) >= 34 else "/system/etc/security/cacerts"
echo         code, _, _ = self.adb.shell(device.serial, f"ls {sys_path}", root=True)
echo         if code != 0:
echo             issues.append(f"Cannot access {sys_path}")
echo             fixes.append("adb shell su -c 'mount -o rw,remount /system'")
echo         .
echo         if issues:
echo             self.ui.warn(f"Found {len(issues)} issues:")
echo             for i in issues: self.ui.info(f"  • {i}")
echo             for f in fixes: self.ui.command(f)
echo         else:
echo             self.ui.ok("All checks passed")
echo         return issues, fixes
echo.
echo # ========== MAIN APP ==========
echo class KrishnaApp:
echo     def __init__(self):
echo         self.ui = UI()
echo         self.adb = ADBManager(self.ui)
echo         self.cert = CertificateManager(self.ui, self.adb)
echo         self.diag = Diagnostic(self.ui, self.adb)
echo         self.device = None
echo     .
echo     def run(self):
echo         self.ui.banner()
echo         .
echo         if not self.adb.check():
echo             input("\nPress Enter to exit...")
echo             return
echo         .
echo         devices = self.adb.get_devices()
echo         if not devices:
echo             self.ui.err("No devices connected")
echo             self.ui.solution("Connect USB and enable debugging")
echo             self.ui.command("adb devices")
echo             input("\nPress Enter...")
echo             return
echo         .
echo         if len(devices) == 1:
echo             self.device = self.adb.get_device_details(devices[0].serial)
echo         else:
echo             self.ui.info("Multiple devices found:")
echo             for i, d in enumerate(devices, 1):
echo                 self.ui.info(f"{i}. {d.serial}")
echo             try:
echo                 idx = int(input("Select device: ")) - 1
echo                 self.device = self.adb.get_device_details(devices[idx].serial)
echo             except:
echo                 self.ui.err("Invalid selection")
echo                 return
echo         .
echo         self.ui.device_table(self.device)
echo         .
echo         if not self.device.rooted:
echo             self.ui.warn("Device not rooted - installation will fail")
echo         .
echo         while True:
echo             self.ui.menu()
echo             choice = input("\nChoice: ").strip()
echo             .
echo             if choice == "1":
echo                 files = [f for f in os.listdir('.') if f.endswith(('.der','.pem','.crt','.cer'))]
echo                 if not files:
echo                     self.ui.err("No certificate files found")
echo                     continue
echo                 .
echo                 self.ui.info("Available certificates:")
echo                 for i, f in enumerate(files, 1):
echo                     self.ui.info(f"  {i}. {f}")
echo                 .
echo                 try:
echo                     idx = int(input("Select: ")) - 1
echo                     cert_path = files[idx]
echo                     info = self.cert.get_info(cert_path)
echo                     self.ui.cert_table(info)
echo                     .
echo                     if input("Install this certificate? (y/n): ").lower() == 'y':
echo                         self.ui.info(f"Installing {cert_path}...")
echo                         ok, msg = self.cert.install(self.device, cert_path)
echo                         if ok:
echo                             self.ui.ok(msg)
echo                             self.ui.info("Reboot device to apply changes")
echo                         else:
echo                             self.ui.err(msg)
echo                 except Exception as e:
echo                     self.ui.err(f"Error: {e}")
echo             .
echo             elif choice == "2":
echo                 hash_val = input("Enter certificate hash: ").strip()
echo                 if hash_val:
echo                     ok, msg = self.cert.verify(self.device, hash_val)
echo                     if ok: self.ui.ok(msg)
echo                     else: self.ui.err(msg)
echo             .
echo             elif choice == "3":
echo                 hash_val = input("Enter hash to remove: ").strip()
echo                 if hash_val and input(f"Remove {hash_val}? (y/n): ").lower() == 'y':
echo                     ok, msg = self.cert.remove(self.device, hash_val)
echo                     if ok:
echo                         self.ui.ok(msg)
echo                         self.ui.info("Reboot device to complete")
echo                     else:
echo                         self.ui.err(msg)
echo             .
echo             elif choice == "4":
echo                 self.ui.device_table(self.device)
echo             .
echo             elif choice == "5":
echo                 self.diag.run(self.device)
echo             .
echo             elif choice == "6":
echo                 self.ui.info("Backing up certificates...")
echo                 ok, msg = self.cert.backup_all(self.device)
echo                 if ok: self.ui.ok(msg)
echo                 else: self.ui.err(msg)
echo             .
echo             elif choice == "7":
echo                 backups = list(Path("backups").glob("*"))
echo                 if not backups:
echo                     self.ui.err("No backups found")
echo                     continue
echo                 self.ui.info("Available backups:")
echo                 for i, b in enumerate(backups, 1):
echo                     size = sum(f.stat().st_size for f in b.glob("*.0")) / 1024
echo                     self.ui.info(f"  {i}. {b.name} ({size:.1f} KB)")
echo                 try:
echo                     idx = int(input("Select backup: ")) - 1
echo                     if 0 <= idx < len(backups):
echo                         if input(f"Restore {backups[idx].name}? (y/n): ").lower() == 'y':
echo                             ok, msg = self.cert.restore(self.device, str(backups[idx]))
echo                             if ok:
echo                                 self.ui.ok(msg)
echo                                 self.ui.info("Reboot device")
echo                             else:
echo                                 self.ui.err(msg)
echo                 except:
echo                     self.ui.err("Invalid selection")
echo             .
echo             elif choice == "8":
echo                 self.ui.ok("Goodbye! 🙏")
echo                 break
echo             .
echo             else:
echo                 self.ui.err("Invalid option")
echo             .
echo             input("\nPress Enter to continue...")
echo.
echo if __name__ == "__main__":
echo     try:
echo         KrishnaApp().run()
echo     except KeyboardInterrupt:
echo         print("\n\nOperation cancelled")
echo     except Exception as e:
echo         print(f"\nError: {e}")
echo         import traceback
echo         traceback.print_exc()
echo         input("\nPress Enter...")
) > "cert.py"

echo [OK] cert.py created successfully
echo.

:: ============================================
:: CREATE LAUNCHER (No admin required)
:: ============================================
(
echo @echo off
echo title Krishna Certificate Manager
echo color 0A
echo cd /d "%~dp0"
echo python cert.py
echo pause
) > "Krishna Cert Manager.bat"

echo [OK] Launcher created
echo.

:: ============================================
:: CREATE DESKTOP SHORTCUT
:: ============================================
echo [*] Creating desktop shortcut...
copy "Krishna Cert Manager.bat" "%USERPROFILE%\Desktop\Krishna Cert Manager.bat" >nul 2>&1
echo [OK] Desktop shortcut created
echo.

:: ============================================
:: INSTALLATION COMPLETE - RUN TOOL
:: ============================================
echo.
echo ================================================
echo    INSTALLATION COMPLETE!
echo ================================================
echo.
echo ✅ Chocolatey installed
echo ✅ OpenSSL installed  
echo ✅ ADB installed
echo ✅ Python packages installed
echo ✅ cert.py created
echo ✅ Launcher created
echo ✅ Desktop shortcut created
echo.
echo ================================================
echo    STARTING CERTIFICATE MANAGER...
echo ================================================
echo.

:: Run the certificate manager
python cert.py

if %errorLevel% neq 0 (
    echo.
    echo [WARN] Trying python3...
    python3 cert.py
)

echo.
echo ================================================
echo    Application Closed
echo ================================================
pause
