# Troubleshooting Guide

Solutions for common issues when using mgtinker/tools.

## Installation Issues

### Python 3 Not Found

**Problem:**
```
bash: python3: command not found
```

**Solution:**

Rocky 8.10/RHEL/Fedora:
```bash
sudo dnf install python3 python3-devel
python3 --version
```

Ubuntu/Debian:
```bash
sudo apt update
sudo apt install python3 python3-dev
python3 --version
```

macOS:
```bash
brew install python3
python3 --version
```

**Verify:** `python3 --version` should show 3.8 or higher.

---

### Git Not Installed

**Problem:**
```
bash: git: command not found
```

**Solution:**

Rocky 8.10/RHEL/Fedora:
```bash
sudo dnf install git
git --version
```

Ubuntu/Debian:
```bash
sudo apt install git
git --version
```

macOS:
```bash
brew install git
git --version
```

**Verify:** `git --version` should work.

---

### Permission Denied (setup.sh)

**Problem:**
```
bash: ./setup.sh: Permission denied
```

**Solution:**

Make script executable:
```bash
chmod +x python/setup.sh
bash python/setup.sh
```

Or run with bash directly:
```bash
bash python/setup.sh
```

---

### pip Installation Fails

**Problem:**
```
ERROR: Could not install packages due to an error
```

**Solution:**

Upgrade pip first:
```bash
python3 -m pip install --upgrade pip
```

Then try installation again:
```bash
python3 -m pip install -r requirements.txt
```

**Alternative - User installation:**
```bash
python3 -m pip install --user -r requirements.txt
```

**Alternative - Virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### Virtual Environment Activation Fails

**Problem:**
```
bash: venv/bin/activate: No such file or directory
```

**Solution:**

Recreate virtual environment:
```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate.bat  # Windows CMD
# or
.\venv\Scripts\Activate.ps1  # Windows PowerShell
```

Then install dependencies:
```bash
pip install -r requirements.txt
```

---

### Module Not Found After Installation

**Problem:**
```
ModuleNotFoundError: No module named 'gitlab'
```

**Solution:**

Verify dependencies:
```bash
python3 check_dependencies.py
```

Install missing packages:
```bash
python3 check_dependencies.py --auto-install
```

Or manually:
```bash
python3 -m pip install python-gitlab requests pyyaml toml
```

---

## Configuration Issues

### Config File Not Found

**Problem:**
```
Error: Config file not found: config.yaml
```

**Solution:**

Create config file:
```bash
python3 gitlab_service_analyzer.py --init-config config.yaml
```

Then edit:
```bash
nano config.yaml
```

Add your GitLab details.

---

### "Invalid token" Error

**Problem:**
```
Error: 401 Unauthorized - Invalid token
```

**Causes:**
1. Token copied incorrectly
2. Token expired
3. Token doesn't have required permissions
4. Extra spaces in token

**Solution:**

1. **Verify token value:**
   ```bash
   # Check for accidental spaces
   cat config.yaml | grep token
   ```

2. **Create new token:**
   - Go to: `https://your-gitlab.com/-/user_settings/personal_access_tokens`
   - Click "Add new token"
   - Name: `tools-analyzer`
   - Scopes: `api`, `read_api`, `read_repository`
   - Click "Create"
   - Copy token (immediately, won't be shown again)

3. **Update config:**
   ```bash
   nano config.yaml
   # Paste new token
   ```

4. **Test connection:**
   ```bash
   curl -H "PRIVATE-TOKEN: your_token" \
     https://your-gitlab.com/api/v4/user
   # Should return user info
   ```

---

### "Connection refused" Error

**Problem:**
```
Error: Failed to connect to GitLab at https://gitlab.example.com
Connection refused
```

**Solutions:**

1. **Check GitLab URL:**
   ```bash
   # Should be full HTTPS URL, no trailing slash
   https://gitlab.example.com    # Correct
   gitlab.example.com            # Wrong
   https://gitlab.example.com/   # Wrong (trailing slash)
   ```

2. **Verify network access:**
   ```bash
   curl https://your-gitlab.com
   # Should return GitLab login page
   ```

3. **Check firewall:**
   ```bash
   # Try direct connection
   telnet your-gitlab.com 443
   ```

4. **For self-hosted GitLab:**
   - Verify GitLab is running
   - Check firewall rules
   - Verify URL is correct

5. **Update config:**
   ```bash
   nano config.yaml
   # Fix gitlab.url
   ```

---

### No Projects Found

**Problem:**
```
No projects found
Proceeding with 0 repositories
```

**Causes:**
1. Wrong group ID
2. No access to projects
3. All projects are archived

**Solutions:**

1. **Verify group ID:**
   ```bash
   # Find group ID: https://your-gitlab.com/groups/YOUR-GROUP/-/settings/general
   # Look for "Group ID" field
   ```

   Update config:
   ```yaml
   gitlab:
     group_id: 123  # Correct group ID
   ```

2. **Try analyzing all projects:**
   ```yaml
   gitlab:
     group_id: null  # null means all projects
   ```

3. **Check token permissions:**
   - Token needs `api` or `read_api` scope
   - Token needs `read_repository` scope

4. **Verify project visibility:**
   - Private projects require personal access
   - Archived projects may be excluded

---

## Runtime Issues

### Analysis Takes Very Long

**Problem:**
```
Analyzing repositories... (20+ minutes)
```

**Solutions:**

1. **Skip code analysis (faster):**
   ```yaml
   analysis:
     analyze_code: false
     analyze_configs: true
   ```

2. **Enable parallel cloning:**
   ```yaml
   advanced:
     concurrent_clones: 4
   ```

3. **Skip large repositories:**
   ```yaml
   advanced:
     max_repo_size: 200    # MB
   ```

4. **Exclude specific projects:**
   ```yaml
   advanced:
     exclude_projects:
       - '^large-'
       - 'archive'
   ```

5. **Analyze specific group:**
   ```yaml
   gitlab:
     group_id: 42  # Instead of all projects
   ```

---

### Out of Disk Space

**Problem:**
```
Error: No space left on device
OSError: [Errno 28] No space left on device
```

**Solutions:**

1. **Clean previous temporary files:**
   ```bash
   rm -rf /tmp/gitlab_analysis
   ```

2. **Use different temp directory:**
   ```yaml
   temp_directory: '/mnt/large_disk/gitlab_analysis'
   ```

3. **Enable automatic cleanup:**
   ```yaml
   cleanup_after: true
   ```

4. **Skip large repos:**
   ```yaml
   advanced:
     max_repo_size: 100    # MB - reduce size limit
   ```

5. **Check available space:**
   ```bash
   df -h
   du -sh /tmp/
   ```

---

### Memory Issues

**Problem:**
```
MemoryError
Killed (out of memory)
```

**Solutions:**

1. **Reduce concurrent clones:**
   ```yaml
   advanced:
     concurrent_clones: 1
   ```

2. **Skip code analysis:**
   ```yaml
   analysis:
     analyze_code: false
   ```

3. **Analyze smaller group:**
   ```yaml
   gitlab:
     group_id: 42  # Smaller group
   ```

4. **Run with memory limit:**
   ```bash
   python3 -u gitlab_service_analyzer.py --config config.yaml
   # -u is unbuffered output for better monitoring
   ```

---

### Unicode/Encoding Errors

**Problem:**
```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0x...
```

**Solution:**

Ensure UTF-8 encoding:
```bash
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
python3 gitlab_service_analyzer.py --config config.yaml
```

For permanent fix, add to `~/.bashrc`:
```bash
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
```

---

## Output Issues

### Generated File is Empty

**Problem:**
```
architecture.md is 0 bytes or contains no content
```

**Solutions:**

1. **Check if analysis ran:**
   ```bash
   # Look for status messages
   tail -20 analyzer.log
   ```

2. **Verify projects were found:**
   - Run analysis again with verbose output
   - Check "Found X projects" message

3. **Check file permissions:**
   ```bash
   ls -la architecture.md
   chmod 644 architecture.md
   ```

4. **Run with debug logging:**
   ```yaml
   logging:
     level: 'DEBUG'
   ```

---

### No Connections Detected

**Problem:**
```
Total Connections: 0
```

**Causes:**
1. No services actually connect
2. Connection patterns not recognized
3. Code analysis disabled

**Solutions:**

1. **Enable code analysis:**
   ```yaml
   analysis:
     analyze_code: true
   ```

2. **Check code patterns:**
   Review detected files:
   ```bash
   python3 gitlab_service_analyzer.py --keep-repos
   # Check /tmp/gitlab_analysis/ for config files
   ```

3. **Review docker-compose files:**
   - Look for `depends_on` or `links` sections
   - Check environment variables for host references

4. **Verify regex patterns:**
   - Open `python/connectivity_analyzer.py`
   - Review patterns for your services
   - May need customization for unusual patterns

---

### JSON File Has Wrong Format

**Problem:**
```
JSON is invalid or missing data
```

**Solution:**

Verify JSON is valid:
```bash
python3 -m json.tool services.json
# Should output formatted JSON without errors
```

Regenerate:
```bash
python3 gitlab_service_analyzer.py --config config.yaml
```

---

## GitLab Connection Issues

### Self-Hosted GitLab Connection

**Problem:**
```
Can't connect to self-hosted GitLab instance
```

**Solutions:**

1. **Verify full URL:**
   ```yaml
   gitlab:
     url: 'https://gitlab.internal.company.com'  # Full URL
   ```

2. **Check SSL certificate:**
   For self-signed certificates (development only):
   ```bash
   # This will show certificate issues
   curl https://your-gitlab.url
   ```

   Workaround in code (not recommended for production):
   ```python
   import urllib3
   urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
   ```

3. **Check GitLab is running:**
   ```bash
   # From GitLab server
   sudo gitlab-ctl status
   ```

4. **Verify firewall:**
   ```bash
   # From client
   telnet gitlab.server.com 443
   ```

---

### Rate Limiting

**Problem:**
```
Error: 429 Too Many Requests
```

**Solution:**

GitLab rate-limits API requests. Wait and retry:
```bash
# Wait a few minutes
sleep 300

# Then retry
python3 gitlab_service_analyzer.py --config config.yaml
```

To reduce rate limiting:
```yaml
advanced:
  concurrent_clones: 1  # Reduce from 4 to 1
```

---

## Windows/WSL Issues

### Script Not Found on WSL

**Problem:**
```
bash: ./setup.sh: No such file or directory
```

**Solution:**

Use bash explicitly:
```bash
bash python/setup.sh
```

Or ensure line endings are Unix (LF), not Windows (CRLF):
```bash
dos2unix python/setup.sh
bash python/setup.sh
```

---

### Virtual Environment Activation on WSL

**Problem:**
```
bash: venv/bin/activate: Permission denied
```

**Solution:**

Ensure proper permissions:
```bash
chmod 755 venv/bin/activate
source venv/bin/activate
```

---

## Getting More Help

### Enable Debug Logging

```yaml
logging:
  level: 'DEBUG'
  file: 'analyzer.log'
```

Then review logs:
```bash
tail -100 analyzer.log
```

### Check Tool Versions

```bash
python3 --version
git --version
python3 -c "import gitlab; print(gitlab.__version__)"
python3 -c "import yaml; print(yaml.__version__)"
```

### Run with Verbose Output

Add to Python scripts:
```bash
python3 -u gitlab_service_analyzer.py --config config.yaml
# -u runs unbuffered for real-time output
```

### Manual Connection Test

```bash
# Test GitLab connection
curl -H "PRIVATE-TOKEN: your_token" \
  https://your-gitlab.com/api/v4/user

# Should return user information
```

### Still Stuck?

1. Review [README.md](../../python/README.md) in python directory
2. Check [Service Analyzer How-To](./SERVICE_ANALYZER_HOWTO.md)
3. Review [Configuration Reference](../references/CONFIGURATION.md)
4. Check GitLab official documentation
5. Create GitHub issue with error details

---

## Reporting Issues

When reporting a problem, include:

1. **Command you ran:**
   ```bash
   python3 gitlab_service_analyzer.py --config config.yaml
   ```

2. **Error message (full):**
   ```
   [paste complete error]
   ```

3. **Configuration (sanitized):**
   ```yaml
   # Remove sensitive data
   gitlab:
     url: 'https://your-gitlab.com'
     token: 'XXX'  # Don't share real token
     group_id: 123
   ```

4. **Environment:**
   ```bash
   python3 --version
   git --version
   uname -a
   ```

5. **Log file:**
   ```bash
   cat analyzer.log
   ```

This helps troubleshoot faster!
