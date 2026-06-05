# 🚀 SETUP GUIDE - Financial Intelligence Dashboard

Complete installation and configuration guide for the Financial Analytics Dashboard with Forecasting & Scenario Analysis.

---

## TABLE OF CONTENTS

1. [System Requirements](#system-requirements)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Running the Dashboard](#running-the-dashboard)
6. [Using Your Data](#using-your-data)
7. [Troubleshooting](#troubleshooting)
8. [Deployment](#deployment)
9. [Verification Checklist](#verification-checklist)

---

## SYSTEM REQUIREMENTS

### Minimum Requirements
- **Operating System:** Windows 10+, macOS 10.14+, Linux (Ubuntu 18.04+)
- **Python:** 3.8 or higher
- **RAM:** 2GB minimum (4GB recommended)
- **Disk Space:** 500MB free space
- **Internet:** Required for cloud deployment (optional)

### Recommended Setup
- **Python:** 3.10 or higher
- **RAM:** 4GB or more
- **Disk Space:** 1GB
- **Browser:** Chrome, Firefox, Safari, or Edge (latest version)

### Check Your Current Setup

```bash
# Check Python version
python --version

# Should show 3.8 or higher
# Example output: Python 3.10.5
```

---

## PREREQUISITES

### 1. Install Python (If Needed)

#### Windows
1. Go to https://www.python.org/downloads/
2. Click "Download Python 3.10" (or latest)
3. Run installer
4. **IMPORTANT:** Check "Add Python to PATH"
5. Click "Install Now"
6. Verify installation:
   ```bash
   python --version
   ```

#### macOS
**Option A: Using Homebrew (Recommended)**
```bash
# Install Homebrew if needed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python3

# Verify
python3 --version
```

**Option B: Using Official Installer**
1. Go to https://www.python.org/downloads/
2. Download macOS installer
3. Run installer
4. Follow prompts

#### Linux (Ubuntu/Debian)
```bash
# Update package manager
sudo apt-get update

# Install Python
sudo apt-get install python3 python3-pip python3-venv

# Verify
