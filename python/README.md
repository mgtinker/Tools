# Python Tools for Service Architecture Analysis

Tools for analyzing GitLab repositories and documenting service-to-service connections in containerized environments.

## Overview

This toolkit helps you understand the architecture and connectivity of microservices running in Docker/Kubernetes by:

1. **Crawling GitLab repositories** - Clones and analyzes your project repos
2. **Analyzing configurations** - Parses docker-compose.yml, Dockerfile, Kubernetes manifests
3. **Code analysis** - Scans application code for service references and connections
4. **Generating documentation** - Creates comprehensive architecture diagrams and connection maps

## Tools

### 1. `gitlab_service_analyzer.py` - Main Service Analyzer

Crawls GitLab repositories and generates architecture documentation.

#### Features
- Analyzes docker-compose, Dockerfile, and Kubernetes manifests
- Scans code for HTTP APIs, database connections, message queues
- Generates markdown documentation with connection matrices
- Creates JSON summary of services
- Configurable via YAML file

#### Quick Start

```bash
# 1. Check dependencies
python3 check_dependencies.py --auto-install

# 2. Create configuration
python3 gitlab_service_analyzer.py --init-config config.yaml

# 3. Edit config with your GitLab credentials
# nano config.yaml

# 4. Run analysis
python3 gitlab_service_analyzer.py --config config.yaml

# 5. Review output
cat architecture.md
```

#### Configuration

See `config.example.yaml` for all options. Key settings:

```yaml
gitlab:
  url: https://gitlab.example.com
  token: YOUR_PERSONAL_ACCESS_TOKEN
  group_id: null  # Optional: specific group ID

output:
  markdown_file: architecture.md
  json_file: services.json
```

#### Usage

```bash
# Generate with default config
python3 gitlab_service_analyzer.py

# Use custom config file
python3 gitlab_service_analyzer.py --config my_config.yaml

# Analyze specific group
python3 gitlab_service_analyzer.py --group-id 42

# Keep cloned repos for inspection
python3 gitlab_service_analyzer.py --keep-repos

# Specify output file
python3 gitlab_service_analyzer.py --output my_architecture.md
```

#### Output

Generates:

1. **architecture.md** - Comprehensive documentation including:
   - Service overview by repository
   - Detailed connection diagrams
   - Connection matrix showing all service relationships
   - Service metadata (image, language, ports)

2. **services.json** - JSON summary for programmatic use:
   ```json
   {
     "service_name": {
       "repo": "repository",
       "image": "image:tag",
       "language": "python",
       "ports": ["8080"],
       "connections": 5
     }
   }
   ```

#### Connection Types Detected

- **http** - HTTP/REST API calls
- **grpc** - gRPC communication
- **database** - PostgreSQL, MySQL, MongoDB
- **redis** - Redis cache connections
- **message_queue** - Kafka, RabbitMQ, AMQP
- **dependency** - Docker-compose depends_on
- **environment** - Environment variable references
- **network** - Docker network links
- **k8s_env** - Kubernetes environment configs

### 2. `check_dependencies.py` - Dependency Manager

Verifies and installs required Python packages.

#### Usage

```bash
# Check which dependencies are installed
python3 check_dependencies.py

# Auto-install missing packages
python3 check_dependencies.py --auto-install

# Use custom requirements file
python3 check_dependencies.py --requirements my_requirements.txt

# Auto-install with custom file
python3 check_dependencies.py --auto-install --requirements my_requirements.txt
```

#### Features
- Checks for installed packages
- Handles package name variations (hyphens/underscores)
- Auto-installs missing dependencies
- Supports standard requirements.txt format
- Clear status output

### 3. `setup_tools.py` - Environment Setup

Prepares Python environment for Rocky 8.10 (or other Linux systems).

#### Usage

```bash
# Full setup (checks Python, creates venv, installs deps)
python3 setup_tools.py

# Or manually:
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
```

#### What It Does
- Verifies Python 3.8+ installed
- Creates virtual environment
- Installs dependencies from requirements.txt
- Provides activation instructions

### 4. `connectivity_analyzer.py` - Core Analysis Module

Low-level module that handles parsing and analysis. Used by main analyzer, but can be used standalone.

```python
from connectivity_analyzer import (
    Service, ServiceConnection, DockerComposeAnalyzer,
    CodeAnalyzer
)

# Parse docker-compose
compose_content = open('docker-compose.yml').read()
connections = DockerComposeAnalyzer.analyze(compose_content, 'my-service', 'my-repo')
```

## Requirements

### System Requirements
- Python 3.8 or higher
- Git (for cloning repositories)
- 500MB+ disk space (for temporary repo clones)
- Network access to GitLab

### Python Dependencies

See `requirements.txt`:
```
requests>=2.31.0
python-gitlab>=3.15.0
pyyaml>=6.0
toml>=0.10.2
```

Install with:
```bash
python3 -m pip install -r requirements.txt
```

Or use the dependency checker:
```bash
python3 check_dependencies.py --auto-install
```

## Installation for Rocky 8.10 WSL

```bash
# 1. Update system
sudo dnf update -y

# 2. Install Python and git
sudo dnf install -y python3 python3-devel git

# 3. Verify installation
python3 --version
git --version

# 4. Clone/setup tools
cd /path/to/tools/python

# 5. Setup environment
python3 setup_tools.py

# 6. Activate venv
source venv/bin/activate

# 7. Run analyzer
python3 gitlab_service_analyzer.py --init-config config.yaml
# ... edit config.yaml with your GitLab token
python3 gitlab_service_analyzer.py --config config.yaml
```

## GitLab Setup

### Create Personal Access Token

1. Go to: https://your-gitlab.com/-/user_settings/personal_access_tokens
2. Create token with scopes:
   - `api` - Full API access
   - `read_api` - Read-only API access
   - `read_repository` - Read repository contents

### For Group Analysis

1. Find group ID: https://your-gitlab.com/groups/your-group/-/settings/general
2. Set in config.yaml:
   ```yaml
   gitlab:
     group_id: 123
   ```

## Troubleshooting

### "Module not found" errors
```bash
python3 check_dependencies.py --auto-install
```

### GitLab connection fails
- Verify token is valid: `https://your-gitlab.com/-/user_settings/personal_access_tokens`
- Check permissions: token needs `api` or `read_api` scope
- Verify URL format: `https://your-gitlab.com` (no trailing slash)

### Slow cloning
- Increase `concurrent_clones` in config (default: 1)
- Reduce repository size limit or exclude large repos
- Use `--keep-repos` to avoid re-cloning

### Out of disk space
- Reduce `temp_directory` or use a larger partition
- Delete previous temp directories: `rm -rf /tmp/gitlab_analysis`
- Reduce repository size limit in config

### Code analysis misses connections
- Review generated files for patterns
- Check `config.example.yaml` for supported file patterns
- Modify `connectivity_analyzer.py` patterns for custom formats

## Example Workflow

```bash
# 1. Setup on new WSL instance
python3 setup_tools.py
source venv/bin/activate

# 2. Create configuration
python3 gitlab_service_analyzer.py --init-config config.yaml

# 3. Add GitLab token to config
nano config.yaml

# 4. Run initial analysis
python3 gitlab_service_analyzer.py --keep-repos

# 5. Review architecture documentation
cat architecture.md

# 6. Future runs (repos already cloned)
python3 gitlab_service_analyzer.py

# 7. Share documentation
cp architecture.md ~/Dropbox/  # or git commit
```

## Output Examples

### Architecture Markdown

```markdown
# Service Architecture Documentation

## Service Overview
- Total Services: 12
- Total Repositories: 4
- Total Connections: 23

## Services by Repository

#### api-gateway
- **gateway-svc**
  - Image: `python:3.11-slim`
  - Language: python
  - Ports: 8080

#### auth-service
- **auth-svc**
  - Image: `python:3.11-slim`
  - Language: python

## Service Connections

#### gateway-svc
- **→ auth-svc** (http)
  - Found in: `gateway/client.py`
- **→ postgres-db** (postgresql)
  - Found in: `gateway/models.py`
```

### Connection Matrix

```
       auth-svc api-svc db-svc
auth-svc      -      -      1
api-svc       1      -      1
gateway       2      1      1
```

## Advanced Usage

### Custom Connection Patterns

Edit `connectivity_analyzer.py` to add custom patterns:

```python
class CodeAnalyzer:
    CUSTOM_PATTERNS = [
        r'my_service\.connect\((["\']([^"\']+)["\'])\)',
    ]
```

### Programmatic Access

```python
from pathlib import Path
from connectivity_analyzer import RepositoryAnalyzer

repo = RepositoryAnalyzer(Path('/path/to/repo'), 'my-repo')
services, connections = repo.analyze()

for conn in connections:
    print(f"{conn.source_service} -> {conn.target_service}: {conn.connection_type}")
```

## Notes

- Analysis is read-only; no modifications to repositories
- Temporary clones deleted by default (use `--keep-repos` to retain)
- Large repositories may take time; consider excluding in config
- Markdown output is suitable for Confluence/GitHub wikis
- JSON output integrates with other tools/dashboards

## Contributing

To improve pattern detection:

1. Add test repositories with specific patterns
2. Update regex patterns in `connectivity_analyzer.py`
3. Test with `python3 gitlab_service_analyzer.py --keep-repos`
4. Document patterns added

## License

See repository LICENSE file.
