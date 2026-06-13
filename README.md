# android_cert_install
# Kalla Billa🚀

A powerful Python suite for Android certificate management - convert DER certificates to PEM format and install them on rooted Android devices.

#install.bat one file is enough


![Kalla Billa Logo](https://img.shields.io/badge/Kalla-Billa-blue?style=for-the-badge) ![Python](https://img.shields.io/badge/python-3.6+-green?style=for-the-badge) ![License](https://img.shields.io/badge/license-MIT-orange?style=for-the-badge) ![Platform](https://img.shields.io/badge/platform-Android-lightgrey?style=for-the-badge)

## 📖 Overview

Kalla Billa Suite is a comprehensive toolkit designed for cybersecurity professionals, penetration testers, and Android developers who need to manage SSL/TLS certificates on Android devices. The suite provides a complete workflow for certificate conversion and installation on rooted Android devices.

## ✨ Features

### 🔧 Certificate Converter (`cert.py`)
- Convert `.der` certificate files to `.pem` format
- Automatic subject hash generation for Android system
- Interactive file selection menu
- Colorful terminal interface with random colors
- Seamless integration with installer

### 📱 Certificate Installer (`phssl.py`)
- Root detection and verification
- Automatic `/system` partition remount (read-write)
- Multiple installation methods for compatibility
- ADB device connectivity check
- Permission management (644 for system certificates)
- Device reboot option after installation

## 🚀 Quick Start

### Prerequisites
- Python 3.6 or higher
- ADB (Android Debug Bridge) installed
- Rooted Android device
- USB debugging enabled

### Installation
```bash
git clone https://github.com/yourusername/kalla-billa-suite.git
cd kalla-billa-suite
pip install colorama
```

### Basic Usage
```bash
python main.py
```

## 📋 Usage Guide

### Using the Main Suite
Run the main launcher for access to both tools:
```bash
python main.py
```

### Individual Tools

#### 1. Certificate Conversion
```bash
python cert.py
```
1. Select a `.der` file from the list
2. Script converts to `burp.pem`
3. Automatically generates Android hash name
4. Renames to `[hash].0` format

#### 2. Certificate Installation
```bash
python phssl.py
```
1. Connect rooted Android device via USB
2. Enable USB debugging
3. Run script and select "Install certificate"
4. Choose `.0` certificate file
5. Follow installation prompts

## 🎯 Workflow

1. **Export certificate** from Burp Suite/Charles Proxy as `.der`
2. **Convert certificate** using `cert.py`
3. **Install certificate** using `phssl.py`
4. **Reboot device** for changes to take effect

## 🛠️ Technical Details

### Supported Platforms
- Android 4.0+ (with root access)
- Tested on Android 7-13
- Windows/Linux/macOS

### File Structure
```
kalla-billa-suite/
├── main.py              # Main launcher
├── cert.py              # Certificate converter
├── phssl.py             # Certificate installer
├── requirements.txt     # Dependencies
├── README.md           # Documentation
└── LICENSE             # MIT License
```

### Certificate Locations
- System: `/system/etc/security/cacerts/`
- Permissions: `644` (rw-r--r--)

## 🔒 Security Notes

⚠️ **Important Security Considerations:**
- Requires **rooted Android device**
- Install only trusted certificates
- Backup original certificates first
- Use in controlled testing environments only
- Not for production devices

## 🐛 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| ADB not found | Install Android SDK Platform Tools |
| Device not detected | Enable USB debugging |
| Permission denied | Ensure device is rooted |
| Certificate not appearing | Reboot device |

### Debug Mode
```bash
python -m phssl.py 2>&1 | tee debug.log
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## ⚠️ Disclaimer

**FOR EDUCATIONAL AND AUTHORIZED TESTING PURPOSES ONLY**

This tool is intended for:
- Security professionals conducting authorized assessments
- Developers testing their own applications
- Educational purposes in controlled environments

The authors are not responsible for any misuse of this software.

---

**Made with ❤️ by Krishna**
