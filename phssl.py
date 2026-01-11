import os
import subprocess
import sys
import time
from colorama import init, Fore, Style

# Initialize colorama for colored output
init()

# Function to check and install required library
def install_required_library(library):
    try:
        import importlib
        importlib.import_module(library)
    except ImportError:
        print(Fore.RED + f"Installing {library}..." + Style.RESET_ALL)
        subprocess.run([sys.executable, '-m', 'pip', 'install', library], check=True)
        print(Fore.GREEN + f"{library} installed successfully." + Style.RESET_ALL)

def check_adb_installed():
    """Check if ADB is installed and available in PATH"""
    try:
        subprocess.run(['adb', '--version'], capture_output=True, text=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(Fore.RED + "ADB is not installed or not in PATH. Please install Android SDK Platform Tools." + Style.RESET_ALL)
        return False

def check_adb_devices():
    try:
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True, check=True)
        if "List of devices attached" in result.stdout:
            devices = [line.strip() for line in result.stdout.split('\n')[1:] if line.strip()]
            connected_devices = [d for d in devices if not d.endswith('offline') and d != '']
            
            if connected_devices:
                print(Fore.GREEN + "Connected devices:" + Style.RESET_ALL)
                for device in connected_devices:
                    parts = device.split('\t')
                    if len(parts) >= 2:
                        print(Fore.CYAN + f"  • {parts[0]} ({parts[1]})" + Style.RESET_ALL)
                return True
            else:
                print(Fore.YELLOW + "No active devices found. Please connect your device via USB and enable USB debugging." + Style.RESET_ALL)
                return False
        return False
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"Error checking ADB devices: {e}" + Style.RESET_ALL)
        return False

def check_root_access():
    """Check if device has root access"""
    try:
        result = subprocess.run(['adb', 'shell', 'su', '-c', '"echo root_check"'], 
                              capture_output=True, text=True, timeout=5, shell=True)
        if "root_check" in result.stdout:
            return True
        else:
            # Try without su
            result = subprocess.run(['adb', 'shell', 'whoami'], 
                                  capture_output=True, text=True, timeout=5)
            return "root" in result.stdout
    except:
        return False

def remount_system_as_rw():
    """Attempt to remount /system as read-write"""
    print(Fore.YELLOW + "Attempting to remount /system as read-write..." + Style.RESET_ALL)
    
    # Method 1: adb remount
    try:
        result = subprocess.run(['adb', 'remount'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(Fore.GREEN + "Successfully remounted /system using 'adb remount'" + Style.RESET_ALL)
            return True
    except:
        pass
    
    # Method 2: Using adb shell with su
    try:
        commands = [
            'mount -o rw,remount /system',
            'mount -o rw,remount /',
            'mount -o remount,rw /system'
        ]
        
        for cmd in commands:
            try:
                result = subprocess.run(f'adb shell su -c "{cmd}"', 
                                      capture_output=True, text=True, timeout=10, shell=True)
                if result.returncode == 0:
                    print(Fore.GREEN + f"Successfully remounted /system using: {cmd}" + Style.RESET_ALL)
                    return True
            except:
                # Try without shell=True
                result = subprocess.run(['adb', 'shell', 'su', '-c', cmd], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    print(Fore.GREEN + f"Successfully remounted /system using: {cmd}" + Style.RESET_ALL)
                    return True
    except:
        pass
    
    print(Fore.RED + "Failed to remount /system as read-write" + Style.RESET_ALL)
    return False

def list_files_with_numbers(files):
    print(Fore.GREEN + f"\nAvailable certificate files (.0 format):" + Style.RESET_ALL)
    for i, file in enumerate(files, start=1):
        print(Fore.CYAN + f"{i}. {file}" + Style.RESET_ALL)

def select_file(files):
    while True:
        selection = input(Fore.YELLOW + f"\nEnter the number (1-{len(files)}) of the file to install: " + Style.RESET_ALL)
        if selection.isdigit() and 1 <= int(selection) <= len(files):
            return files[int(selection) - 1]
        else:
            print(Fore.RED + f"Invalid selection. Please enter a number between 1 and {len(files)}" + Style.RESET_ALL)

def check_system_cacerts_exists():
    """Check if /system/etc/security/cacerts directory exists"""
    try:
        result = subprocess.run(['adb', 'shell', 'ls', '/system/etc/security/cacerts'], 
                              capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except:
        return False

def execute_shell_command(command):
    """Execute a shell command with proper quoting"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
        return result
    except subprocess.TimeoutExpired:
        return subprocess.CompletedProcess(command, 1, "", "Command timed out")

def main():
    try:
        install_required_library('colorama')
        
        # Banner
        print(Fore.GREEN + ">>===========================================<<")
        print("||                                           ||")
        print("||  _  __     _ _         ____  _ _ _        ||")
        print("|| | |/ /__ _| | | __ _  | __ )(_) | | __ _  ||")
        print("|| | ' // _` | | |/ _` | |  _ \| | | |/ _` | ||")
        print("|| | . \ (_| | | | (_| | | |_) | | | | (_| | ||")
        print("|| |_|\_\__,_|_|_|\__,_| |____/|_|_|_|\__,_| ||")
        print("||                                           ||")
        print(">>===========================================<<" + Style.RESET_ALL)
        
        # Check if ADB is installed
        if not check_adb_installed():
            input(Fore.RED + "\nPress Enter to exit..." + Style.RESET_ALL)
            return
        
        while True:
            print(Fore.YELLOW + "\n" + "="*50 + Style.RESET_ALL)
            print(Fore.CYAN + "1. Check if device is connected" + Style.RESET_ALL)
            print(Fore.CYAN + "2. Install certificate" + Style.RESET_ALL)
            print(Fore.CYAN + "3. Exit" + Style.RESET_ALL)
            choice = input(Fore.YELLOW + "\nSelect option (1-3): " + Style.RESET_ALL)
            
            if choice == '1':
                check_adb_devices()
                continue
            elif choice == '2':
                if not check_adb_devices():
                    print(Fore.RED + "\nPlease connect a device first!" + Style.RESET_ALL)
                    continue
                
                # Check for .0 files
                files = [file for file in os.listdir() if file.endswith(".0")]
                if not files:
                    print(Fore.RED + "\nNo .0 certificate files found in current directory." + Style.RESET_ALL)
                    print(Fore.YELLOW + "Please place certificate files (.0 format) in the same directory as this script." + Style.RESET_ALL)
                    continue
                
                list_files_with_numbers(files)
                selected_file = select_file(files)
                
                # Ask for confirmation
                print(Fore.YELLOW + f"\nYou selected: {selected_file}" + Style.RESET_ALL)
                confirm = input(Fore.YELLOW + "Proceed with installation? (yes/no): " + Style.RESET_ALL)
                if confirm.lower() not in ['yes', 'y']:
                    print(Fore.YELLOW + "Installation cancelled." + Style.RESET_ALL)
                    continue
                
                # Step 1: Check root access
                print(Fore.YELLOW + "\n[1/7] Checking root access..." + Style.RESET_ALL)
                if not check_root_access():
                    print(Fore.RED + "Device does not have root access!" + Style.RESET_ALL)
                    print(Fore.YELLOW + "This operation requires root permissions. Continuing anyway..." + Style.RESET_ALL)
                
                # Step 2: Remount system as read-write FIRST
                print(Fore.YELLOW + "[2/7] Preparing system partition..." + Style.RESET_ALL)
                if not remount_system_as_rw():
                    print(Fore.YELLOW + "Trying to continue without remount..." + Style.RESET_ALL)
                
                # Step 3: Check if cacerts directory exists
                print(Fore.YELLOW + "[3/7] Checking cacerts directory..." + Style.RESET_ALL)
                if not check_system_cacerts_exists():
                    print(Fore.YELLOW + "Creating cacerts directory..." + Style.RESET_ALL)
                    # Create directory with proper permissions
                    mkdir_result = execute_shell_command('adb shell "su -c \'mkdir -p /system/etc/security/cacerts\'"')
                    if mkdir_result.returncode != 0:
                        print(Fore.YELLOW + "Trying alternative method to create directory..." + Style.RESET_ALL)
                        execute_shell_command('adb shell mkdir -p /system/etc/security/cacerts')
                
                # Step 4: Push file directly to system location (alternative method)
                print(Fore.YELLOW + "[4/7] Pushing certificate to system..." + Style.RESET_ALL)
                
                # Method 1: Try direct push to system (if remount worked)
                system_path = f"/system/etc/security/cacerts/{selected_file}"
                push_direct = subprocess.run(['adb', 'push', selected_file, system_path], 
                                           capture_output=True, text=True)
                
                if push_direct.returncode != 0:
                    print(Fore.YELLOW + "Direct push failed, trying alternative method..." + Style.RESET_ALL)
                    
                    # Method 2: Push to temp and copy with proper shell command
                    temp_path = f"/data/local/tmp/{selected_file}"
                    push_temp = subprocess.run(['adb', 'push', selected_file, temp_path], 
                                             capture_output=True, text=True)
                    
                    if push_temp.returncode != 0:
                        print(Fore.RED + f"Failed to push file: {push_temp.stderr}" + Style.RESET_ALL)
                        continue
                    
                    print(Fore.GREEN + f"✓ File pushed to {temp_path}" + Style.RESET_ALL)
                    
                    # Step 5: Copy using dd command (more reliable)
                    print(Fore.YELLOW + "[5/7] Copying to system location..." + Style.RESET_ALL)
                    
                    # Using dd command which handles binary files better
                    copy_cmd = f'adb shell "su -c \\"dd if={temp_path} of={system_path} 2>/dev/null\\""'
                    copy_result = execute_shell_command(copy_cmd)
                    
                    if copy_result.returncode != 0:
                        # Try cat command
                        print(Fore.YELLOW + "Trying cat command..." + Style.RESET_ALL)
                        copy_cmd = f'adb shell "su -c \\"cat {temp_path} > {system_path}\\""'
                        copy_result = execute_shell_command(copy_cmd)
                    
                    if copy_result.returncode != 0:
                        # Try simple cp command
                        print(Fore.YELLOW + "Trying cp command..." + Style.RESET_ALL)
                        copy_cmd = f'adb shell cp {temp_path} {system_path}'
                        copy_result = execute_shell_command(copy_cmd)
                    
                    if copy_result.returncode != 0:
                        print(Fore.RED + f"Failed to copy file to system: {copy_result.stderr}" + Style.RESET_ALL)
                        
                        # Try one more method - use adb shell in interactive mode
                        print(Fore.YELLOW + "Trying interactive shell method..." + Style.RESET_ALL)
                        try:
                            # Create a script file
                            with open('temp_script.sh', 'w') as f:
                                f.write(f'''#!/system/bin/sh
su -c "cat {temp_path} > {system_path}"
exit
''')
                            
                            subprocess.run(['adb', 'push', 'temp_script.sh', '/data/local/tmp/temp_script.sh'])
                            subprocess.run(['adb', 'shell', 'chmod', '755', '/data/local/tmp/temp_script.sh'])
                            script_result = subprocess.run(['adb', 'shell', '/data/local/tmp/temp_script.sh'], 
                                                         capture_output=True, text=True)
                            os.remove('temp_script.sh')
                            subprocess.run(['adb', 'shell', 'rm', '/data/local/tmp/temp_script.sh'])
                            
                            if script_result.returncode != 0:
                                raise Exception("Script method failed")
                        except:
                            print(Fore.RED + "All copy methods failed!" + Style.RESET_ALL)
                            continue
                    
                    # Clean up temp file
                    subprocess.run(['adb', 'shell', 'rm', temp_path], capture_output=True, text=True)
                else:
                    print(Fore.GREEN + f"✓ Certificate pushed directly to system" + Style.RESET_ALL)
                
                # Step 6: Set permissions
                print(Fore.YELLOW + "[6/7] Setting permissions..." + Style.RESET_ALL)
                chmod_cmd = f'adb shell "su -c \\"chmod 644 {system_path}\\""'
                chmod_result = execute_shell_command(chmod_cmd)
                
                if chmod_result.returncode == 0:
                    print(Fore.GREEN + "✓ Permissions set correctly" + Style.RESET_ALL)
                else:
                    # Try without su
                    subprocess.run(['adb', 'shell', 'chmod', '644', system_path], capture_output=True, text=True)
                    print(Fore.YELLOW + "✓ Permissions set (alternative method)" + Style.RESET_ALL)
                
                # Step 7: Verify file exists
                print(Fore.YELLOW + "[7/7] Verifying installation..." + Style.RESET_ALL)
                verify_result = subprocess.run(['adb', 'shell', 'ls', '-la', system_path], 
                                             capture_output=True, text=True)
                
                if verify_result.returncode == 0 and selected_file in verify_result.stdout:
                    print(Fore.GREEN + f"✓ Certificate successfully installed at: {system_path}" + Style.RESET_ALL)
                    print(Fore.GREEN + f"✓ File details:\n{verify_result.stdout}" + Style.RESET_ALL)
                else:
                    print(Fore.YELLOW + "⚠ Installation completed but verification failed" + Style.RESET_ALL)
                
                # Ask about reboot
                reboot_choice = input(Fore.YELLOW + "\nReboot device now? (yes/no): " + Style.RESET_ALL)
                
                if reboot_choice.lower() in ['yes', 'y']:
                    print(Fore.YELLOW + "Rebooting device..." + Style.RESET_ALL)
                    subprocess.run(['adb', 'reboot'], capture_output=True, text=True)
                    print(Fore.GREEN + "Device is rebooting. You're all done!" + Style.RESET_ALL)
                    time.sleep(2)
                else:
                    print(Fore.YELLOW + "Please reboot your device manually for changes to take effect." + Style.RESET_ALL)
                
                break
                
            elif choice == '3':
                print(Fore.YELLOW + "Goodbye!" + Style.RESET_ALL)
                break
            else:
                print(Fore.RED + "Invalid option. Please try again." + Style.RESET_ALL)
                
    except KeyboardInterrupt:
        print(Fore.RED + "\n\nOperation cancelled by user." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"\nAn unexpected error occurred: {str(e)}" + Style.RESET_ALL)
        import traceback
        traceback.print_exc()
    finally:
        input(Fore.YELLOW + "\nPress Enter to exit..." + Style.RESET_ALL)

if __name__ == "__main__":
    main()