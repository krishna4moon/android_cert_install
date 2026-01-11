import os
import subprocess
import shutil
import random
from colorama import init, Fore, Style
import colorama

# Initialize colorama for colored output
init()

# ASCII art for "Kalla Billa" logo
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

# Function to list .der files in the current directory
def list_der_files():
    der_files = [file for file in os.listdir() if file.endswith(".der")]
    if not der_files:
        raise FileNotFoundError(f"{Fore.RED}No .der files found in the directory{Style.RESET_ALL}")
    print(f"{random.choice([Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN])}Available .der files:{Style.RESET_ALL}")
    for i, file in enumerate(der_files, start=1):
        print(f"{random.choice([Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN])}{i}. {file}{Style.RESET_ALL}")
    return der_files

# Function to select a file and convert it to .pem
def convert_to_pem(selected_index, der_files):
    if 1 <= selected_index <= len(der_files):
        selected_file = der_files[selected_index - 1]
        pem_file = "burp.pem"
        try:
            # Remove burp.pem if it exists
            if os.path.exists(pem_file):
                os.remove(pem_file)
            # Convert .der to .pem
            subprocess.run(['openssl', 'x509', '-inform', 'DER', '-in', selected_file, '-out', pem_file], check=True)
            print(f"{random.choice([Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN])}{selected_file} converted to {pem_file}{Style.RESET_ALL}")
            return pem_file
        except subprocess.CalledProcessError:
            raise RuntimeError(f"{Fore.RED}Failed to convert {selected_file} to {pem_file}{Style.RESET_ALL}")
    else:
        raise ValueError(f"{Fore.RED}Invalid selection{Style.RESET_ALL}")

# Function to print subject hash and certificate
def print_subject_hash_and_certificate(pem_file):
    try:
        # Run openssl x509 command and capture output
        result = subprocess.run(['openssl', 'x509', '-inform', 'PEM', '-subject_hash_old', '-in', pem_file], capture_output=True, text=True, check=True)
        # Extract the first line
        output_lines = result.stdout.split('\n')
        if len(output_lines) > 0:
            new_hash = output_lines[0]
            print(f"{random.choice([Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN])}First line: {new_hash}{Style.RESET_ALL}")
            # Print the entire certificate
            print(f"{random.choice([Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN])}Certificate:{Style.RESET_ALL}")
            print(result.stdout)
            return new_hash
        else:
            print("No output")
    except subprocess.CalledProcessError:
        raise RuntimeError(f"{Fore.RED}Failed to print subject hash and certificate for {pem_file}{Style.RESET_ALL}")

# Function to move burp.pem to new_hash.0
def move_pem_to_hash(pem_file, new_hash):
    try:
        shutil.move(pem_file, f"{new_hash}.0")
        print(f"{random.choice([Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN])}{pem_file} moved to {new_hash}.0{Style.RESET_ALL}")
    except Exception as e:
        raise RuntimeError(f"{Fore.RED}Failed to move {pem_file} to {new_hash}.0: {e}{Style.RESET_ALL}")

# Function to handle the menu after the file is moved
def handle_menu():
    print(f"{random.choice([Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN])}Options:{Style.RESET_ALL}")
    print(f"{random.choice([Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN])}1. Go back{Style.RESET_ALL}")
    print(f"{random.choice([Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN])}2. Run next script (phssl.py){Style.RESET_ALL}")
    print(f"{random.choice([Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN])}0. Exit{Style.RESET_ALL}")
    choice = input(f"{random.choice([Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN])}Enter your choice: {Style.RESET_ALL}")
    return choice

# Main function
def main():
    print(logo)
    try:
        der_files = list_der_files()
        selected_index = int(input(f"{random.choice([Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN])}Enter the serial number of the file you want to convert: {Style.RESET_ALL}"))
        pem_file = convert_to_pem(selected_index, der_files)
        new_hash = print_subject_hash_and_certificate(pem_file)
        move_pem_to_hash(pem_file, new_hash)
        
        while True:
            choice = handle_menu()
            if choice == "1":
                break
            elif choice == "2":
                # Run phssl.py script
                subprocess.run(['python', 'phssl.py'])
            elif choice == "0":
                print(f"{random.choice([Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN])}Exiting...{Style.RESET_ALL}")
                break
            else:
                print(f"{random.choice([Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN])}Invalid choice. Please try again.{Style.RESET_ALL}")
    except FileNotFoundError as e:
        print(e)
    except ValueError as e:
        print(e)
    except RuntimeError as e:
        print(e)
    except KeyboardInterrupt:
        print(f"{Fore.RED}\nYou killed a kalla bila!{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}An unexpected error occurred: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
