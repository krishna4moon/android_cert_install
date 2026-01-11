import os
import subprocess
import shutil
import random
import sys
import time
from colorama import init, Fore, Style

init()

logo = f"""
{random.choice([Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN])}>>===========================================<<
||                                           ||
||  _  __     _ _         ____  _ _ _        ||
|| | |/ /__ _| | | __ _  | __ )(_) | | __ _  ||
|| | ' // _` | | |/ _` | |  _ \| | | |/ _` | ||
|| | . \ (_| | | | (_| | | |_) | | | | (_| | ||
|| |_|\_\__,_|_|_|\__,_| |____/|_|_|_|\__,_| ||
||                                           ||
>>===========================================<<{Style.RESET_ALL}
"""

def install_required_library(library):
    try:
        import importlib
        importlib.import_module(library)
    except ImportError:
        print(Fore.RED + f"Installing {library}..." + Style.RESET_ALL)
        subprocess.run([sys.executable, '-m', 'pip', 'install', library], check=True)
        print(Fore.GREEN + f"{library} installed successfully." + Style.RESET_ALL)

def display_menu():
    print(f"\n{Fore.YELLOW}{'='*50}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{' '*18}MAIN MENU{' '*18}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'='*50}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}1. Convert DER to PEM (cert.py){Style.RESET_ALL}")
    print(f"{Fore.GREEN}2. Install Certificate (phssl.py){Style.RESET_ALL}")
    print(f"{Fore.RED}0. Exit{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'-'*50}{Style.RESET_ALL}")

def run_cert_py():
    try:
        subprocess.run([sys.executable, 'cert.py'])
    except FileNotFoundError:
        print(f"{Fore.RED}cert.py not found!{Style.RESET_ALL}")

def run_phssl_py():
    try:
        subprocess.run([sys.executable, 'phssl.py'])
    except FileNotFoundError:
        print(f"{Fore.RED}phssl.py not found!{Style.RESET_ALL}")

def print_welcome():
    print(f"{Fore.MAGENTA}{'*'*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{' '*15}WELCOME TO KALLA BILLA SUITE{' '*15}{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}{'*'*60}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Version: 1.0 | Author: Kalla Billa Team{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Tools:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  • cert.py: Convert DER certificates to PEM format{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  • phssl.py: Install certificates on Android devices{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}{'*'*60}{Style.RESET_ALL}\n")

def check_requirements():
    required_files = ['cert.py', 'phssl.py']
    missing = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)
    
    if missing:
        print(f"{Fore.RED}Missing required files:{Style.RESET_ALL}")
        for file in missing:
            print(f"  • {file}")
        print(f"{Fore.YELLOW}Please ensure all files are in the same directory.{Style.RESET_ALL}")
        return False
    return True

def main():
    try:
        install_required_library('colorama')
        
        print(logo)
        print_welcome()
        
        if not check_requirements():
            print(f"{Fore.RED}Cannot proceed. Required files are missing.{Style.RESET_ALL}")
            input(f"{Fore.YELLOW}Press Enter to exit...{Style.RESET_ALL}")
            return
        
        while True:
            display_menu()
            choice = input(f"{Fore.CYAN}Select option (0-2): {Style.RESET_ALL}")
            
            if choice == "1":
                print(f"{Fore.YELLOW}Launching Certificate Converter...{Style.RESET_ALL}")
                time.sleep(1)
                run_cert_py()
            elif choice == "2":
                print(f"{Fore.YELLOW}Launching Certificate Installer...{Style.RESET_ALL}")
                time.sleep(1)
                run_phssl_py()
            elif choice == "0":
                print(f"{Fore.GREEN}Thank you for using Kalla Billa Suite!{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Goodbye! 👋{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.RED}Invalid option! Please select 0, 1, or 2.{Style.RESET_ALL}")
            
            input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
    
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Operation cancelled by user.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Goodbye!{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}An unexpected error occurred: {str(e)}{Style.RESET_ALL}")
    finally:
        if 'choice' not in locals() or choice != "0":
            input(f"{Fore.YELLOW}Press Enter to exit...{Style.RESET_ALL}")

if __name__ == "__main__":
    main()