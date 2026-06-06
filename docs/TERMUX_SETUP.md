# 📱 Termux/Mobile Setup Guide

This guide explains how to install and run **ApplyPilot** on an Android device using Termux.

## 1. Overview
ApplyPilot is an autonomous job application pipeline. While optimized for desktop/server environments, it can be run on mobile for job discovery, scoring, and tailoring.

## 2. Requirements
- **Device**: Android phone (8.0+) with 4GB+ RAM recommended.
- **App**: [Termux](https://f-droid.org/en/packages/com.termux/) (F-Droid version required).
- **Storage**: ~2GB free space.
- **Wake Lock**: Enabled in Termux notification to prevent Android from killing the process.

## 3. Installation Steps
Run these commands in Termux:

```bash
# Update system packages
pkg update && pkg upgrade -y

# Install core dependencies
pkg install git python python-pip -y
```

## 4. Repository Clone
```bash
git clone https://github.com/Cladius-Weinert/ApplyPilot.git
cd ApplyPilot
```

## 5. Virtual Environment Setup
```bash
# Create and activate environment
python -m venv .venv
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip
```

## 6. Dependency Installation
```bash
pip install .
```

## 7. .env Setup
Copy the example file and edit it with your keys:
```bash
cp .env.example .env
nano .env
```
*Note: Use a physical keyboard or Hacker's Keyboard for easier editing.*

## 8. Run Commands
```bash
# Verify installation
applypilot doctor

# Run discovery and tailoring
applypilot run
```

## 9. Browser & Playwright Limitations
- **Base Termux**: Default Playwright browser binaries do not support Android's ARM architecture directly.
- **Auto-Apply**: Stage 6 (`applypilot apply`) requires a browser. For mobile, this may require Chromium installed via `pkg install chromium` and additional environment configuration (like `BROWSER_PATH`), or running in a VNC/Desktop environment.
- **Recommendation**: Use mobile primarily for Stages 1-5 (Discovery, Scoring, Tailoring).

## 10. Common Errors
- **Permission Denied**: Run `termux-setup-storage` and grant permissions.
- **Package Failures**: Ensure you are using the F-Droid version of Termux; the Play Store version is outdated.
- **Memory Issues**: Large pandas operations or AI processing may crash on low-RAM devices.

## 11. Security Notes
- **Secrets**: Never commit your `.env` file.
- **Keys**: Store API keys in your device's secure vault if not using environment variables.

## 12. Troubleshooting
If `pip install` fails with build errors, install build tools:
```bash
pkg install clang make -y
```

## 13. Next Steps
Once your resumes are tailored, you can transfer them to a desktop for final submission or use a cloud-based rater if available.
