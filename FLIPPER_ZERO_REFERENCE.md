# Flipper Zero & Flipper Patcher - Complete Reference

## 🐬 Overview

Flipper Zero is a portable multi-tool device for pentesters and hardware hackers. This document contains all the information added to your JARVIS database.

---

## 📊 Database Statistics

- **System Info Entries**: 8
- **Knowledge Base Entries**: 16
- **Preferences**: 4
- **Total Flipper Data**: 28 entries

---

## 🔧 Hardware Specifications

| Component | Specification |
|-----------|---------------|
| **Processor** | STM32WB55 (Cortex-M4 + M0+) |
| **Display** | 128x64 monochrome LCD |
| **Battery** | 2000mAh Li-Po |
| **GPIO Pins** | 18 pins |
| **Storage** | Internal + microSD support |
| **Connectivity** | USB-C, Bluetooth, Sub-GHz, NFC, RFID, IR |

---

## 📡 Radio Capabilities

### Sub-GHz Radio
**Frequencies**: 
- 300-348 MHz
- 387-464 MHz  
- 779-928 MHz

**Common Uses**:
- Car key fobs (315/433/868/915 MHz)
- Garage door openers
- Weather stations
- Wireless doorbells
- Remote controls

**Range**: Up to 50-100 meters (depending on conditions)

### NFC (13.56 MHz)
**Supported Standards**:
- ISO14443A/B
- ISO15693
- FeliCa

**Supported Cards**:
- MIFARE Classic
- MIFARE Ultralight
- NTAG
- DESFire
- EMV (read-only)

**Functions**: Read, Write, Emulate, Clone

### RFID (125 kHz)
**Supported Types**:
- EM4100
- HID Prox
- Indala

**Functions**: Read, Write, Emulate

### Infrared
**Capabilities**:
- Universal remote control
- Learn mode (capture any IR signal)
- Universal remote library
- Custom signal creation

**Frequency**: 800-1000 nm wavelength

**Supported Devices**:
- TVs
- Air conditioners
- Audio systems
- Projectors
- Fans
- LED strips

---

## 💻 Software Features

### BadUSB
**Description**: Emulate USB keyboard/mouse for automated attacks

**Capabilities**:
- DuckyScript support
- Reverse shells
- Data exfiltration
- System reconnaissance
- Credential harvesting
- Persistence mechanisms

**Platforms**: Windows, Linux, macOS

**Storage**: Scripts stored in `/badusb/` folder on SD card

⚠️ **Use responsibly and legally!**

### GPIO (18 Pins)
**Protocols Supported**:
- UART
- SPI
- I2C
- 1-Wire

**Voltage**: 3.3V logic level

**Features**:
- Logic analyzer
- UART terminal
- SPI/I2C sniffer
- PWM output
- ADC input

**Use Cases**:
- Hardware debugging
- Firmware dumping
- IoT device analysis
- Arduino communication

### iButton
**Description**: Dallas/Maxim 1-Wire key system

**Functions**: Read, Write, Emulate

**Common Types**:
- DS1990A (read-only)
- DS1992-DS1996 (read/write memory)
- TM2004 (crypto)

**Use Cases**:
- Building access
- Elevator control
- Time tracking systems
- Vending machines

---

## 🔄 Firmware Options

### 1. Official Firmware
- ✅ Stable
- ✅ Regular updates
- ❌ Limited features
- 🎯 Best for: Beginners, legal compliance

### 2. Unleashed Firmware
- ✅ More features
- ✅ Removed restrictions
- ✅ Community-driven
- 🎯 Best for: Advanced users, more protocols

### 3. RogueMaster Firmware
- ✅ Maximum features
- ✅ Includes games
- ✅ Extra protocols
- 🎯 Best for: Power users, full capabilities

### 4. Xtreme Firmware
- ✅ Customizable
- ✅ Performance-focused
- 🎯 Best for: Custom configurations

**Update Methods**:
- qFlipper app (official)
- Web updater
- Manual SD card method

---

## 📁 File Structure (SD Card)

```
/badusb/          - BadUSB scripts
/subghz/          - Sub-GHz captures
/nfc/             - NFC dumps
/rfid/            - RFID dumps
/infrared/        - IR signals
/ibutton/         - iButton keys
/u2f/             - U2F keys
/apps/            - FAP applications
/apps_data/       - App data
/music_player/    - RTTTL ringtones
```

---

## 🛠️ Flipper Patcher

### Overview
Tool for modifying Flipper Zero firmware and applications.

### Features
- ✅ Custom firmware building
- ✅ App patching
- ✅ Resource modification
- ✅ Animation customization
- ✅ Icon editing
- ✅ Manifest editing

### Use Cases
- Remove region locks
- Add custom features
- Modify UI
- Enable hidden functions
- Create custom builds

### Installation
```bash
# Requires Python 3.8+
git clone https://github.com/flipper-patcher/flipper-patcher
cd flipper-patcher
pip install -r requirements.txt
```

### Basic Usage
```bash
python flipper_patcher.py --firmware <path> --patch <patch_file>
```

### Common Patches
- Region unlock
- Frequency expansion
- Feature enablement
- UI modifications

### Output
Modified firmware `.dfu` file

### Flashing
- qFlipper
- dfu-util

⚠️ **Always backup original firmware!**

---

## 📱 Apps & Plugins

### App Types
- Built-in apps
- External apps (.fap files)
- Plugins

### Popular Apps
- 🎮 Snake game
- 🎮 Tetris
- 🎵 Music player
- 🔐 TOTP generator
- 📡 WiFi scanner (with ESP32)
- 📍 GPS (with module)
- 📊 Spectrum analyzer
- 🔊 Signal generator
- 💻 UART terminal
- ⌨️ USB keyboard

### Installation
1. Copy `.fap` files to `/apps/` on SD card
2. Or use qFlipper app manager

---

## 📡 Sub-GHz Protocols

### Supported Protocols
- Princeton
- KeeLoq
- Star Line
- Nice FLO
- Came
- Faac SLH
- Somfy Telis
- Somfy Keytis
- Chamberlain
- Linear
- Megacode
- Security+
- BFT Mitto
- Holtek
- Marantec
- Mastercode
- Firefly

### Functions
- Read RAW
- Decode
- Save
- Emulate
- Brute force (some protocols)

---

## 💻 CLI Commands

### Access
- Screen serial terminal
- qFlipper CLI
- USB serial connection

### Common Commands
```bash
storage         # Manage files
gpio            # Control GPIO
rfid            # RFID operations
nfc             # NFC operations
subghz          # Sub-GHz radio
ir              # Infrared
bt              # Bluetooth
power           # Battery info
led             # Control LED
vibro           # Vibration motor
speaker         # Sound control
```

---

## ⚖️ Legal & Security

### ✅ LEGAL USES
- Personal device testing
- Security research (authorized)
- Educational purposes
- Home automation
- Hardware development
- Devices you own

### ❌ ILLEGAL ACTIVITIES
- Cloning access cards without permission
- Car key attacks on vehicles you don't own
- Unauthorized network access
- Payment card fraud
- Breaking into systems without authorization

### 📋 Important Notes
- Only test on devices you own or have written permission to test
- Know your local laws regarding radio frequencies
- Some frequencies are restricted by region
- Security testing requires authorization
- Unauthorized access is illegal in most jurisdictions

---

## 🌐 Resources

### Official
- **Website**: flipperzero.one
- **Documentation**: docs.flipperzero.one
- **Forum**: forum.flipperzero.one

### GitHub
- **Official**: github.com/flipperdevices
- **Community**: github.com/UberGuidoZ/Flipper

### Communities
- Reddit: r/flipperzero
- Discord servers
- Telegram groups

### Tools
- **qFlipper**: Official desktop app
- **Flipper Mobile App**: iOS/Android
- **Web updater**: Online firmware updater
- **Python CLI**: Command-line tools

### Databases
- Sub-GHz signal database
- IR remote database
- NFC card database

---

## 🎯 Quick Reference

### Frequencies by Region

| Region | Allowed Frequencies |
|--------|-------------------|
| **USA** | 315 MHz, 433 MHz, 915 MHz |
| **Europe** | 433 MHz, 868 MHz |
| **Asia** | 433 MHz, 315 MHz |

⚠️ **Always check local regulations!**

### Common Use Cases

| Task | Module | Frequency/Protocol |
|------|--------|-------------------|
| Car key fob | Sub-GHz | 315/433/868/915 MHz |
| Garage door | Sub-GHz | 300-400 MHz |
| Access card | RFID/NFC | 125 kHz / 13.56 MHz |
| TV remote | Infrared | 800-1000 nm |
| Building key | iButton | 1-Wire |
| USB attack | BadUSB | DuckyScript |

---

## 📝 JARVIS Integration

### Query Examples

Ask JARVIS:
```
"What frequencies does Flipper Zero support?"
"How do I use BadUSB on Flipper Zero?"
"What's the difference between Unleashed and RogueMaster?"
"How do I clone an RFID card?"
"What is Flipper Patcher?"
"Show me Flipper Zero GPIO capabilities"
"What apps are available for Flipper Zero?"
```

### Database Location
All Flipper Zero information is stored in:
- `system_info` table (hardware specs)
- `knowledge_base` table (detailed information)
- `user_preferences` table (settings)

### View Flipper Data
```bash
python view_flipper_data.py
```

### Add More Data
```bash
python add_flipper_zero.py
```

---

## 🔄 Updates

**Last Updated**: May 4, 2026  
**Database Version**: 2.0  
**Flipper Data Entries**: 28

---

## ⚠️ Disclaimer

This information is provided for educational and authorized security testing purposes only. Always:
- Obtain proper authorization before testing
- Follow local laws and regulations
- Use responsibly and ethically
- Respect privacy and property rights

**Unauthorized access to computer systems and networks is illegal.**

---

## 📞 Support

For questions about:
- **Flipper Zero device**: Official forum and documentation
- **JARVIS database**: Run `python view_database.py`
- **Adding data**: Run `python add_flipper_zero.py`

---

**🐬 Happy Flipping! (Legally and Responsibly)**
