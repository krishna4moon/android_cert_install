import subprocess
import socket
import sys

def adb_shell(command, device=None):
    """Execute ADB command on specific device"""
    cmd = ["adb"]
    if device:
        cmd.extend(["-s", device])
    cmd.extend(["shell", command])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()

def get_devices():
    """Get list of connected devices"""
    result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
    devices = []
    for line in result.stdout.split('\n')[1:]:
        if line.strip() and '\tdevice' in line:
            devices.append(line.split('\t')[0])
    return devices

def get_ipv4_address():
    """Get local IP address"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except:
        return None

def set_wifi_proxy(device, ip, port):
    """Set proxy on specific device"""
    commands = [
        f"settings put global http_proxy {ip}:{port}",
        f"settings put global global_http_proxy_host {ip}",
        f"settings put global global_http_proxy_port {port}"
    ]
    
    for cmd in commands:
        result = adb_shell(cmd, device)
        if "Exception" in result:
            return False
    return True

def clear_wifi_proxy(device):
    """Remove proxy settings"""
    commands = [
        "settings put global http_proxy :0",
        "settings put global global_http_proxy_host ''",
        "settings put global global_http_proxy_port ''"
    ]
    
    for cmd in commands:
        adb_shell(cmd, device)
    return True

def main():
    # Get computer IP
    ip = get_ipv4_address()
    if not ip:
        print("Error: Could not get IP address")
        return
    
    # Get connected devices
    devices = get_devices()
    if not devices:
        print("Error: No Android devices connected")
        return
    
    print(f"Found {len(devices)} device(s): {devices}")
    
    # Get user choice
    port = input("Enter proxy port (default 5492): ").strip() or "5492"
    action = input("Set (s) or Clear (c) proxy? ").strip().lower()
    
    for device in devices:
        if action == 's':
            if set_wifi_proxy(device, ip, port):
                print(f"[{device}] Proxy set to {ip}:{port}")
            else:
                print(f"[{device}] Failed to set proxy")
        elif action == 'c':
            if clear_wifi_proxy(device):
                print(f"[{device}] Proxy cleared")
            else:
                print(f"[{device}] Failed to clear proxy")

if __name__ == "__main__":
    main()