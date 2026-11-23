# Installation Guide

Detailed setup instructions for different platforms and scenarios.

## System Requirements

### Minimum Requirements
- **Python:** 3.8 or higher
- **Git:** Any recent version
- **Disk Space:** 500MB+ for temporary files
- **Network:** Access to your GitLab instance

### Supported Platforms
- ✓ Linux (Rocky 8.10+, Ubuntu 20.04+, Debian 11+)
- ✓ WSL2 (Windows Subsystem for Linux)
- ✓ macOS (Intel and Apple Silicon)
- ✓ Docker containers

## Installation Paths

### Quick Start (Recommended for Most Users)

**For Rocky 8.10 WSL or Linux:**

```bash
# 1. Clone repository
git clone https://github.com/mgtinker/Tools.git
cd tools

# 2. Run setup script
cd python
bash setup.sh

# 3. Configure
nano config.yaml
# Add: GitLab URL, token, group_id (optional)

# 4. Activate (if using venv)
source venv/bin/activate  # Created by setup.sh

# 5. Run
python3 gitlab_service_analyzer.py --config config.yaml
```

**Time:** ~5-10 minutes

---

## Detailed Setup by Platform

### Rocky 8.10 WSL

#### Prerequisites Check
```bash
python3 --version    # Should be 3.8+
git --version
```

#### If Python Not Installed
```bash
sudo dnf update -y
sudo dnf install -y python3 python3-devel python3-pip git
```

#### Full Installation
```bash
# Clone repo
git clone https://github.com/mgtinker/Tools.git
cd tools/python

# Run automated setup
bash setup.sh

# Edit config
nano config.yaml

# Test
python3 gitlab_service_analyzer.py --init-config test.yaml
```

### Ubuntu / Debian Linux

```bash
# Update package lists
sudo apt update

# Install Python and git
sudo apt install -y python3 python3-dev python3-pip git

# Clone repo
git clone https://github.com/mgtinker/Tools.git
cd tools/python

# Run setup
bash setup.sh
```

### macOS

```bash
# Using Homebrew (if not installed: https://brew.sh)
brew install python3 git

# Clone repo
git clone https://github.com/mgtinker/Tools.git
cd tools/python

# Run setup
bash setup.sh
```

### Docker Container

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install git
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Clone repo
RUN git clone https://github.com/mgtinker/Tools.git .

WORKDIR /app/python

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Default command
CMD ["python3", "gitlab_service_analyzer.py", "--help"]
```

Build and run:
```bash
docker build -t tools-analyzer .
docker run -it -v $(pwd):/output tools-analyzer \
  python3 gitlab_service_analyzer.py --output /output/architecture.md
```

---

## Manual Installation (Advanced)

If you prefer not to use `setup.sh`:

### Step 1: Clone Repository
```bash
git clone https://github.com/mgtinker/Tools.git
cd tools/python
```

### Step 2: Create Virtual Environment (Optional but Recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

**Or** use the dependency checker:
```bash
python3 check_dependencies.py --auto-install
```

### Step 4: Verify Installation
```bash
python3 -c "import gitlab; import yaml; print('OK')"
```

### Step 5: Create Configuration
```bash
python3 gitlab_service_analyzer.py --init-config config.yaml
```

### Step 6: Configure
```bash
nano config.yaml
# Edit and add:
# - gitlab.url: https://your-gitlab.com
# - gitlab.token: YOUR_TOKEN
# - gitlab.group_id: (optional)
```

### Step 7: Test
```bash
python3 gitlab_service_analyzer.py --config config.yaml
```

---

## Installing Dependencies

### Standard Installation
```bash
python3 -m pip install -r requirements.txt
```

### Specific Packages
```bash
python3 -m pip install requests>=2.31.0
python3 -m pip install python-gitlab>=3.15.0
python3 -m pip install pyyaml>=6.0
python3 -m pip install toml>=0.10.2
```

### Using check_dependencies.py
```bash
# Check status
python3 check_dependencies.py

# Auto-install
python3 check_dependencies.py --auto-install

# Custom requirements file
python3 check_dependencies.py --requirements my_requirements.txt
```

---

## Post-Installation

### Verify Setup
```bash
cd tools/python
python3 gitlab_service_analyzer.py --help
```

Should show:
```
usage: gitlab_service_analyzer.py [-h] [--config CONFIG] ...
```

### Create Configuration
```bash
python3 gitlab_service_analyzer.py --init-config config.yaml
```

This creates a template with:
```yaml
gitlab:
  url: 'https://gitlab.example.com'
  token: 'YOUR_GITLAB_TOKEN'
  group_id: null
...
```

### Get GitLab Token

1. Go to: `https://your-gitlab.com/-/user_settings/personal_access_tokens`
2. Click "Add new token"
3. Enter name: "tools-analyzer"
4. Select scopes:
   - `api` (Full API access)
   - `read_api` (Read API)
   - `read_repository` (Repository access)
5. Click "Create personal access token"
6. Copy the token value

### Update Configuration
```bash
nano config.yaml
```

Replace:
```yaml
gitlab:
  url: 'https://your-gitlab.com'  # Your GitLab URL
  token: 'glpat-xxxxxxxxxxxx'     # Your token
  group_id: null                   # Optional: group ID
```

---

## Virtual Environment (Optional)

### Why Use Virtual Environment?
- Isolates project dependencies
- Prevents conflicts with system packages
- Easy cleanup (just delete the directory)

### Create Virtual Environment
```bash
python3 -m venv venv
```

### Activate Virtual Environment

**Linux/macOS:**
```bash
source venv/bin/activate
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Docker:**
```bash
# Not needed in Docker - dependencies installed globally
```

### Your Prompt Changes
```
(venv) user@machine:~/tools/python$
```

### Install Dependencies (In Virtual Environment)
```bash
pip install -r requirements.txt
```

### Deactivate Virtual Environment
```bash
deactivate
```

---

## Upgrade Installation

### Update Repository
```bash
cd tools
git pull origin main
```

### Update Dependencies
```bash
cd python
pip install --upgrade -r requirements.txt
```

### Or Full Fresh Install
```bash
# Backup current config
cp python/config.yaml python/config.yaml.backup

# Remove old venv (if used)
rm -rf python/venv

# Fresh install
cd python
bash setup.sh
```

---

## Troubleshooting Installation

### Python 3 Not Found
```bash
# Check installed versions
python3 --version
python --version

# Install if missing
sudo dnf install python3     # Rocky/RHEL/Fedora
sudo apt install python3     # Ubuntu/Debian
brew install python3         # macOS
```

### Git Not Found
```bash
sudo dnf install git         # Rocky/RHEL/Fedora
sudo apt install git         # Ubuntu/Debian
brew install git             # macOS
```

### Pip Installation Fails
```bash
# Try alternative method
python3 -m pip install --upgrade pip

# Install with --user flag
python3 -m pip install --user -r requirements.txt
```

### Permission Denied
```bash
# Use user installation
python3 -m pip install --user -r requirements.txt

# Or use virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Virtual Environment Issues
```bash
# Delete and recreate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### PyYAML Import Error
```bash
# Install development headers
sudo dnf install python3-devel
sudo apt install python3-dev

# Reinstall pyyaml
pip install --force-reinstall pyyaml
```

---

## Verification Checklist

After installation, verify:

- [ ] Python 3.8+ installed: `python3 --version`
- [ ] Git installed: `git --version`
- [ ] Repository cloned: `ls ~/tools/`
- [ ] Dependencies installed: `python3 check_dependencies.py`
- [ ] Config created: `ls python/config.yaml`
- [ ] GitLab token added to config
- [ ] Can run help: `python3 gitlab_service_analyzer.py --help`

---

## Next Steps

After successful installation:

1. **Configure:** Add your GitLab token to `config.yaml`
2. **Test:** Run with `--init-config` to verify setup
3. **Analyze:** Run full analysis with `--config config.yaml`
4. **Review:** Check generated `architecture.md`

See [Service Analyzer How-To](./SERVICE_ANALYZER_HOWTO.md) for detailed usage.

---

## Getting Help

- **Installation issue?** → Check [Troubleshooting](./TROUBLESHOOTING.md)
- **Can't find Python?** → See "Python 3 Not Found" section above
- **Dependencies failing?** → See "Pip Installation Fails" section above
- **Still stuck?** → Review the tool README: `python/README.md`
