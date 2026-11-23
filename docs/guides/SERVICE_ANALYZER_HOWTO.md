# Service Analyzer How-To Guide

Complete guide to using the GitLab Service Architecture Analyzer.

## Overview

The GitLab Service Analyzer crawls your GitLab repositories and generates comprehensive documentation showing how your microservices connect and communicate.

**Main Entry Point:** `python/gitlab_service_analyzer.py`

## What It Does

The analyzer:
1. Connects to your GitLab instance
2. Clones all repositories you have access to
3. Analyzes configuration files (docker-compose, Dockerfile, Kubernetes)
4. Scans code for service references and connections
5. Generates markdown documentation and JSON summaries

**Result:** A complete map of your service architecture with connection details.

## Before You Start

### Requirements
- GitLab instance (self-hosted or cloud)
- Personal access token with read permissions
- Python 3.8+
- 500MB+ disk space (for temporary clones)

### Create GitLab Token

1. Go to: `https://your-gitlab.com/-/user_settings/personal_access_tokens`
2. Click "Add new token"
3. Set name: `tools-analyzer` or similar
4. Select scopes:
   - `api` - Full API access
   - `read_api` - Read-only API
   - `read_repository` - Repository contents
5. Click "Create"
6. Copy the token (you won't see it again!)

## Basic Usage

### Quick Start (5 minutes)

```bash
# 1. Navigate to tools
cd tools/python

# 2. Create configuration file
python3 gitlab_service_analyzer.py --init-config config.yaml

# 3. Edit configuration
nano config.yaml
# Add: GitLab URL and token

# 4. Run analysis
python3 gitlab_service_analyzer.py --config config.yaml

# 5. Review output
cat architecture.md
```

### Minimal Configuration

Create `config.yaml`:
```yaml
gitlab:
  url: 'https://gitlab.example.com'
  token: 'glpat-xxxxxxxxxxxx'
  group_id: null

output:
  markdown_file: 'architecture.md'
  json_file: 'services.json'

analysis:
  analyze_code: true
  analyze_configs: true

temp_directory: '/tmp/gitlab_analysis'
cleanup_after: true
```

Then run:
```bash
python3 gitlab_service_analyzer.py --config config.yaml
```

## Common Scenarios

### Scenario 1: Analyze Entire GitLab Instance

Configuration:
```yaml
gitlab:
  url: 'https://gitlab.example.com'
  token: 'glpat-xxxxxxxxxxxx'
  group_id: null  # null = all accessible projects
```

Run:
```bash
python3 gitlab_service_analyzer.py --config config.yaml
```

**Result:** Analyzes all projects you have access to.

---

### Scenario 2: Analyze Specific Group Only

Configuration:
```yaml
gitlab:
  url: 'https://gitlab.example.com'
  token: 'glpat-xxxxxxxxxxxx'
  group_id: 42  # Set to your group ID
```

**To find your group ID:**
1. Go to: `https://your-gitlab.com/groups/your-group-name/-/settings/general`
2. Look for "Group ID" on the page
3. Add to config

Run:
```bash
python3 gitlab_service_analyzer.py --config config.yaml
```

**Result:** Only analyzes projects in that group.

---

### Scenario 3: Analyze with Custom Output Location

```bash
python3 gitlab_service_analyzer.py \
  --config config.yaml \
  --output /home/user/docs/my_architecture.md
```

**Result:** Saves markdown to custom location.

---

### Scenario 4: Keep Cloned Repositories for Inspection

```bash
python3 gitlab_service_analyzer.py \
  --config config.yaml \
  --keep-repos
```

**Result:** Repositories stay in `/tmp/gitlab_analysis/` for review.

Then explore:
```bash
ls /tmp/gitlab_analysis/
# See all cloned repositories
```

---

### Scenario 5: Analyze Specific Group and Keep Repos

```bash
python3 gitlab_service_analyzer.py \
  --config config.yaml \
  --group-id 123 \
  --keep-repos
```

**Result:** Analyzes group 123 and keeps cloned repos.

---

## Advanced Configuration

### Full Configuration Example

```yaml
# GitLab Connection
gitlab:
  url: 'https://gitlab.example.com'
  token: 'glpat-your-token-here'
  group_id: null                # null for all, number for specific group

# Output Files
output:
  markdown_file: 'architecture.md'
  json_file: 'services.json'

# Analysis Options
analysis:
  # Analyze configuration files
  analyze_configs: true
  
  # Analyze code files
  analyze_code: true
  
  # File patterns to scan
  code_patterns:
    - '*.py'
    - '*.js'
    - '*.ts'
    - '*.go'
    - '.env'
    - '*.conf'
  
  # Connection types to find
  connection_types:
    - http
    - grpc
    - database
    - message_queue
    - dependency
    - environment
    - network

# Temporary Files
temp_directory: '/tmp/gitlab_analysis'
cleanup_after: true          # Delete clones after analysis

# Advanced (Optional)
advanced:
  max_repo_size: 500         # MB - skip larger repos
  clone_timeout: 300         # seconds
  concurrent_clones: 1       # increase for parallel cloning
  exclude_projects: []       # regex patterns to skip
  include_projects: []       # only analyze these (overrides exclude)

# Logging
logging:
  level: 'INFO'              # DEBUG, INFO, WARNING, ERROR
  file: 'analyzer.log'
```

### Customize File Patterns

Scan additional file types:
```yaml
analysis:
  code_patterns:
    - '*.py'
    - '*.js'
    - '*.java'
    - '*.rb'
    - '*.go'
    - '*.rs'
    - '*.yml'
    - '*.yaml'
    - '.env*'
```

### Exclude Specific Projects

Skip archived or non-service projects:
```yaml
advanced:
  exclude_projects:
    - '^archived-'
    - '^test-'
    - 'deprecated'
```

### Include Only Specific Projects

Analyze only production services:
```yaml
advanced:
  include_projects:
    - '^services/'
    - 'production'
```

---

## Understanding the Output

### architecture.md Structure

The generated markdown contains several sections:

#### 1. Service Overview
```markdown
## Service Overview

Total Services: 12
Total Repositories: 4
Total Connections: 23

### Services by Repository

#### auth-services
- **auth-svc**
  - Image: `python:3.11-slim`
  - Language: python
  - Ports: 8080
```

Shows all discovered services organized by repository.

#### 2. Service Connections
```markdown
## Service Connections

### auth-svc
- **→ database** (postgresql)
  - Found in: `src/models/user.py`
- **→ redis-cache** (redis)
  - Found in: `config/redis.yaml`
```

Lists how each service connects to others with file locations.

#### 3. Connection Matrix
```markdown
## Connection Matrix
```
       auth-svc api-svc db-svc
auth-svc      -      -      1
api-svc       1      -      1
gateway       2      1      1
```

Shows all connections at a glance.

---

### services.json Structure

```json
{
  "auth-service": {
    "repo": "auth-services",
    "image": "python:3.11-slim",
    "language": "python",
    "ports": ["8080"],
    "connections": 3
  },
  "api-gateway": {
    "repo": "gateway",
    "image": "node:18-alpine",
    "language": "javascript",
    "ports": ["3000"],
    "connections": 5
  }
}
```

Machine-readable format for integration with other tools.

---

## Command Reference

### Full Command Syntax
```bash
python3 gitlab_service_analyzer.py [OPTIONS]
```

### Options

| Option | Description | Example |
|--------|-------------|---------|
| `--config FILE` | Config file path | `--config config.yaml` |
| `--init-config` | Create default config | `--init-config` |
| `--output FILE` | Output markdown file | `--output arch.md` |
| `--group-id ID` | Analyze specific group | `--group-id 42` |
| `--keep-repos` | Don't delete clones | `--keep-repos` |
| `--help` | Show help message | `--help` |

### Examples

```bash
# Create config and exit
python3 gitlab_service_analyzer.py --init-config config.yaml

# Analyze with default config
python3 gitlab_service_analyzer.py

# Analyze with custom config
python3 gitlab_service_analyzer.py --config my_config.yaml

# Analyze specific group
python3 gitlab_service_analyzer.py --group-id 123

# Custom output location
python3 gitlab_service_analyzer.py \
  --output /home/user/architecture.md

# Keep repos for inspection
python3 gitlab_service_analyzer.py --keep-repos

# Combine multiple options
python3 gitlab_service_analyzer.py \
  --config production.yaml \
  --group-id 42 \
  --output /home/user/prod_architecture.md \
  --keep-repos
```

---

## Tips and Tricks

### Faster Analysis (Skip Code Scanning)

If you only need config-level connections:
```yaml
analysis:
  analyze_code: false
  analyze_configs: true
```

Saves significant time on large codebases.

### Parallel Cloning

For faster cloning (use with caution):
```yaml
advanced:
  concurrent_clones: 4
```

Increases network usage but runs faster.

### Skip Large Repositories

Avoid massive repos that slow analysis:
```yaml
advanced:
  max_repo_size: 200    # MB - skip if larger
  exclude_projects:
    - '^large-'
    - 'archive'
```

### Custom Temporary Directory

Use different disk if running out of space:
```yaml
temp_directory: '/mnt/large_disk/gitlab_analysis'
```

### Analyze Multiple Times

After first run, skip cleanup to speed up reruns:
```yaml
cleanup_after: false
```

Then manually clean:
```bash
rm -rf /tmp/gitlab_analysis
```

### Debug Mode

Enable logging:
```yaml
logging:
  level: 'DEBUG'
  file: 'analyzer.log'
```

Then review: `tail -f analyzer.log`

---

## Troubleshooting

### "Connection refused" Error

**Problem:** Can't connect to GitLab
```
Error: Failed to connect to GitLab
```

**Solutions:**
1. Check GitLab URL is correct (with https://)
2. Verify network access to GitLab
3. Test token validity at: `https://your-gitlab.com/api/v4/user`

### "Invalid token" Error

**Problem:** Token rejected
```
Error: 401 Unauthorized
```

**Solutions:**
1. Verify token is copied correctly (no extra spaces)
2. Check token hasn't expired
3. Verify scopes: api, read_api, read_repository
4. Create new token if needed

### "No projects found" Error

**Problem:** Analyzer finds zero projects
```
No projects found
```

**Solutions:**
1. Verify GitLab group_id is correct
2. Check you have access to projects
3. Try without group_id (analyze all projects)
4. Verify token has sufficient permissions

### Slow Performance

**Problem:** Analysis takes very long
```
Analyzing repositories... (taking too long)
```

**Solutions:**
1. Enable concurrent cloning: `concurrent_clones: 4`
2. Disable code analysis: `analyze_code: false`
3. Skip large repos: `max_repo_size: 200`
4. Analyze specific group instead of all projects

### Disk Space Issues

**Problem:** Out of disk space
```
Error: No space left on device
```

**Solutions:**
1. Use different temp directory (larger disk)
2. Enable cleanup: `cleanup_after: true`
3. Use `--keep-repos false` explicitly
4. Manually clean: `rm -rf /tmp/gitlab_analysis`

### PyYAML Import Error

**Problem:** YAML library missing
```
ModuleNotFoundError: No module named 'yaml'
```

**Solutions:**
```bash
python3 check_dependencies.py --auto-install
# or
pip install pyyaml
```

---

## Sharing Results

### Generate Documentation
```bash
python3 gitlab_service_analyzer.py --config config.yaml
# Creates architecture.md
```

### Share with Team
```bash
# Git repository
cp architecture.md /path/to/wiki/docs/
git add docs/architecture.md
git commit -m "Update service architecture"
git push

# Confluence/Wiki
# Copy content of architecture.md to wiki page

# Email
# Attach architecture.md or send with git link
```

### Integration Examples

**Include in CI/CD Pipeline:**
```bash
# Generate before deployment
python3 gitlab_service_analyzer.py --config config.yaml

# Commit if changed
if [ -f architecture.md ]; then
  git add architecture.md
  git commit -m "Auto-generated architecture docs"
  git push
fi
```

**Use JSON for Dashboard:**
```bash
# Generate JSON
python3 gitlab_service_analyzer.py --config config.yaml

# Parse with jq
jq '.[] | select(.language == "python")' services.json
```

---

## Next Steps

- **Review Output:** See `architecture.md` and `services.json`
- **Share Documentation:** Use markdown with your team
- **Schedule Analysis:** Set up regular runs (e.g., weekly)
- **Extend Tools:** See [API Reference](../api/connectivity_analyzer.md)
- **Troubleshoot:** See [Troubleshooting Guide](./TROUBLESHOOTING.md)

---

## Related Documentation

- [Installation Guide](./INSTALLATION.md) - Setup instructions
- [Configuration Reference](../references/CONFIGURATION.md) - All config options
- [Tool Reference](../references/TOOL_REFERENCE.md) - Command reference
- [Troubleshooting](./TROUBLESHOOTING.md) - Common issues
- [API Reference](../api/connectivity_analyzer.md) - Python API
