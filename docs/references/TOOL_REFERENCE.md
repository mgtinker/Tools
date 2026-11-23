# Tool Reference

Complete command and option reference for all mgtinker/tools utilities.

## Table of Contents

1. [gitlab_service_analyzer.py](#gitlab_service_analyzerpy)
2. [check_dependencies.py](#check_dependenciespy)
3. [setup.sh](#setupsh)
4. [setup_tools.py](#setup_toolspy)

---

## gitlab_service_analyzer.py

Main GitLab repository analyzer - crawls repos and generates architecture documentation.

### Location
```
tools/python/gitlab_service_analyzer.py
```

### Usage
```bash
python3 gitlab_service_analyzer.py [OPTIONS]
```

### Options

| Option | Argument | Description | Example |
|--------|----------|-------------|---------|
| `--help` | None | Show help message | `python3 gitlab_service_analyzer.py --help` |
| `--config` | FILE | Path to config file | `--config config.yaml` |
| `--init-config` | FILE | Create default config | `--init-config config.yaml` |
| `--output` | FILE | Output markdown file | `--output arch.md` |
| `--group-id` | ID | Analyze specific group | `--group-id 42` |
| `--keep-repos` | None | Keep cloned repos | `--keep-repos` |

### Examples

```bash
# Show help
python3 gitlab_service_analyzer.py --help

# Create config file
python3 gitlab_service_analyzer.py --init-config config.yaml

# Analyze with config
python3 gitlab_service_analyzer.py --config config.yaml

# Analyze specific group
python3 gitlab_service_analyzer.py --config config.yaml --group-id 123

# Custom output location
python3 gitlab_service_analyzer.py \
  --config config.yaml \
  --output /home/user/my_architecture.md

# Keep cloned repositories
python3 gitlab_service_analyzer.py \
  --config config.yaml \
  --keep-repos

# Multiple options
python3 gitlab_service_analyzer.py \
  --config production.yaml \
  --group-id 42 \
  --output /tmp/prod_arch.md \
  --keep-repos
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error (see message) |
| 2 | Invalid arguments |

### Output Files

| File | Description |
|------|-------------|
| `architecture.md` | Markdown documentation (default name) |
| `services.json` | JSON service summary (if configured) |
| `analyzer.log` | Debug log (if logging enabled) |

### Configuration File

Required config items:
```yaml
gitlab:
  url: 'https://gitlab.example.com'
  token: 'glpat-your-token'
  group_id: null  # or specific group ID

output:
  markdown_file: 'architecture.md'
  json_file: 'services.json'
```

See [Configuration Reference](./CONFIGURATION.md) for all options.

### Exit Messages

**Success:**
```
Done!
✓ Markdown documentation: architecture.md
✓ JSON summary: services.json
```

**Common Errors:**
```
Error: Config file not found
Error: GitLab token not configured
No projects found
```

---

## check_dependencies.py

Verifies and installs Python package dependencies.

### Location
```
tools/python/check_dependencies.py
```

### Usage
```bash
python3 check_dependencies.py [OPTIONS]
```

### Options

| Option | Argument | Description |
|--------|----------|-------------|
| `--auto-install` | None | Auto-install missing packages |
| `--requirements` | FILE | Path to requirements file |
| `--help` | None | Show help |

### Examples

```bash
# Check dependency status
python3 check_dependencies.py

# Auto-install missing packages
python3 check_dependencies.py --auto-install

# Check custom requirements file
python3 check_dependencies.py --requirements my_requirements.txt

# Auto-install with custom file
python3 check_dependencies.py \
  --auto-install \
  --requirements my_requirements.txt
```

### Output

**All satisfied:**
```
Checking dependencies from requirements.txt...
✓ requests
✓ python-gitlab
✓ pyyaml
✓ toml

--- Summary ---
Installed: 4
Missing: 0

All dependencies satisfied!
```

**Missing packages:**
```
Checking dependencies from requirements.txt...
✓ requests
✗ python-gitlab - NOT INSTALLED
✓ pyyaml
✗ toml - NOT INSTALLED

--- Summary ---
Installed: 2
Missing: 2

To install missing dependencies, run:
  python3 check_dependencies.py --auto-install
```

**After auto-install:**
```
Installing 2 missing package(s)...
  Installing python-gitlab... ✓
  Installing toml... ✓

All dependencies installed successfully!
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All dependencies satisfied |
| 1 | Missing dependencies |

### Supported Formats

Supports standard requirements.txt format:
```
requests>=2.31.0
python-gitlab>=3.15.0
pyyaml>=6.0
toml>=0.10.2
```

Also accepts:
- `==` (exact version)
- `<=` (less than)
- `>=` (greater than)
- `~=` (compatible version)
- No version specifier (any version)

---

## setup.sh

Quick setup script for Rocky 8.10 WSL and Linux systems.

### Location
```
tools/python/setup.sh
```

### Usage
```bash
bash setup.sh [CONFIG_FILE]
```

### Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `CONFIG_FILE` | Config file name | `config.yaml` |

### Examples

```bash
# Default setup
bash setup.sh

# With custom config file
bash setup.sh my_config.yaml
```

### What It Does

1. Checks Python 3 installed
2. Checks git installed
3. Verifies/installs Python dependencies
4. Creates default config if needed
5. Provides activation instructions

### Output

**Successful setup:**
```
=== GitLab Service Analyzer - Rocky 8.10 Setup ===

✓ Python 3.11.0
✓ Git installed
Checking Python dependencies...
Installing missing dependencies...

=== Setup Complete ===

To activate virtual environment:
  source venv/bin/activate
```

**Config needs setup:**
```
⚠️  IMPORTANT: Edit config.yaml and add your GitLab token:
   1. Go to: https://your-gitlab.com/-/user_settings/personal_access_tokens
   2. Create token with 'api', 'read_api', 'read_repository' scopes
   3. Copy token value into config.yaml
   4. Run: python3 gitlab_service_analyzer.py --config config.yaml
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Setup complete or config needs update |
| 1 | Error during setup |

### After Setup

```bash
# Activate virtual environment
source venv/bin/activate

# Verify installation
python3 check_dependencies.py

# Create config
python3 gitlab_service_analyzer.py --init-config config.yaml

# Edit config
nano config.yaml

# Run analysis
python3 gitlab_service_analyzer.py --config config.yaml
```

---

## setup_tools.py

Manual environment setup script for custom configurations.

### Location
```
tools/python/setup_tools.py
```

### Usage
```bash
python3 setup_tools.py
```

### Options

No command-line options. Script is interactive.

### What It Does

1. Verifies Python 3.8+ installed
2. Checks required commands (git)
3. Creates virtual environment
4. Installs dependencies from requirements.txt
5. Provides activation instructions

### Output

**Success:**
```
=== Python Tools Setup Helper ===

Python: 3.11
Installing requirements...
✓ Installing requirements

=== Setup Complete ===

To activate virtual environment:
  source venv/bin/activate  # Linux/WSL
```

### Virtual Environment Location

Default: `venv/` in current directory

After running:
```
venv/
├── bin/           # Linux/macOS executables
├── Scripts/       # Windows executables
└── lib/           # Python libraries
```

### Manual Steps (Without setup.sh)

```bash
# Create venv
python3 -m venv venv

# Activate
source venv/bin/activate      # Linux/macOS
# or
venv\Scripts\activate.bat      # Windows CMD
# or
.\venv\Scripts\Activate.ps1    # Windows PowerShell

# Install dependencies
pip install -r requirements.txt

# Verify
python3 check_dependencies.py
```

---

## Command Summary Table

| Tool | Purpose | Main Command | Key Option |
|------|---------|--------------|-----------|
| `gitlab_service_analyzer.py` | Analyze repos | `python3 gitlab_service_analyzer.py` | `--config FILE` |
| `check_dependencies.py` | Check packages | `python3 check_dependencies.py` | `--auto-install` |
| `setup.sh` | Quick setup | `bash setup.sh` | `CONFIG_FILE` |
| `setup_tools.py` | Manual setup | `python3 setup_tools.py` | (interactive) |

---

## Common Workflows

### Complete Setup to Analysis

```bash
# 1. Enter tools directory
cd tools/python

# 2. Quick setup
bash setup.sh

# 3. Configure
nano config.yaml
# Add GitLab URL and token

# 4. Run analysis
python3 gitlab_service_analyzer.py --config config.yaml

# 5. Review results
cat architecture.md
```

### Manual Setup

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Check dependencies
python3 check_dependencies.py --auto-install

# 3. Create config
python3 gitlab_service_analyzer.py --init-config config.yaml

# 4. Configure and analyze
nano config.yaml
python3 gitlab_service_analyzer.py --config config.yaml
```

### Analyze Multiple Groups

```bash
# Group 1
python3 gitlab_service_analyzer.py \
  --config config.yaml \
  --group-id 42 \
  --output group_42_arch.md

# Group 2
python3 gitlab_service_analyzer.py \
  --config config.yaml \
  --group-id 99 \
  --output group_99_arch.md
```

### Debug Mode

```bash
# Enable debug logging in config.yaml
logging:
  level: 'DEBUG'
  file: 'analyzer.log'

# Run analysis
python3 gitlab_service_analyzer.py --config config.yaml

# Review logs
tail -100 analyzer.log
```

---

## Environment Variables

No specific environment variables required, but standard Python ones work:

| Variable | Purpose | Example |
|----------|---------|---------|
| `PYTHONPATH` | Python module path | `PYTHONPATH=/path/to/tools python3 script.py` |
| `LANG` | Character encoding | `export LANG=en_US.UTF-8` |
| `LC_ALL` | Locale settings | `export LC_ALL=en_US.UTF-8` |

---

## Configuration Files

### requirements.txt

Standard pip requirements format:
```
requests>=2.31.0
python-gitlab>=3.15.0
pyyaml>=6.0
toml>=0.10.2
```

### config.yaml

Tool configuration (YAML format):
```yaml
gitlab:
  url: 'https://gitlab.example.com'
  token: 'glpat-your-token'
  group_id: null

output:
  markdown_file: 'architecture.md'
  json_file: 'services.json'
```

See [Configuration Reference](./CONFIGURATION.md) for complete options.

---

## File Locations

| File | Location | Purpose |
|------|----------|---------|
| Main analyzer | `python/gitlab_service_analyzer.py` | Service crawler |
| Core module | `python/connectivity_analyzer.py` | Analysis engine |
| Dependency check | `python/check_dependencies.py` | Package manager |
| Setup script | `python/setup.sh` | Quick setup |
| Setup tool | `python/setup_tools.py` | Manual setup |
| Requirements | `python/requirements.txt` | Dependencies |
| Config example | `python/config.example.yaml` | Template |
| Main README | `python/README.md` | Documentation |

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Ctrl+C` | Stop running script |
| `Ctrl+D` | End input (EOF) |

No interactive menu - scripts run to completion.

---

## See Also

- [Configuration Reference](./CONFIGURATION.md) - Detailed config options
- [Service Analyzer How-To](../guides/SERVICE_ANALYZER_HOWTO.md) - Usage guide
- [Installation Guide](../guides/INSTALLATION.md) - Setup instructions
- [Troubleshooting Guide](../guides/TROUBLESHOOTING.md) - Problem solutions
