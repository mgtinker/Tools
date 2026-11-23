# Tools Repository Context

A collection of utility scripts and automation tools designed to aid in managing and working on other development projects.

## Repository Structure

### `/python`
Python scripts for general-purpose development utilities and project management tasks.
- Use for data processing, file manipulation, and cross-platform scripting
- Examples: build helpers, project scaffolding, automation scripts

### `/tcl`
TCL scripts, commonly used for EDA tool automation (e.g., Vivado, design tools).
- Examples: synthesis scripts, simulation automation, design flow integration

### `/make`
Makefile-based build systems and task automation.
- Use for building projects, running test suites, and orchestrating complex workflows
- Can include both standalone Makefiles and supplementary build support scripts

### `/shell`
Shell scripts (bash, sh, zsh) for system-level operations and cross-tool integration.
- Examples: environment setup, batch processing, CI/CD integration scripts

### `/other`
Miscellaneous tools and scripts that don't fit other categories.
- Perl, Ruby, Node.js, or other language-based tools
- Configuration files and templates

## Usage

Each subdirectory should contain:
- **Scripts**: Properly organized with clear naming conventions
- **README.md** (optional): Usage instructions specific to that category
- **Dependencies**: Listed in comments or a requirements file (e.g., `requirements.txt` for Python)

## Contributing

- Include shebang lines for executable scripts (e.g., `#!/usr/bin/env python3`)
- Add descriptive comments and usage documentation
- Ensure scripts are portable and handle dependencies gracefully
- Include error handling and informative error messages

## Current Tools

### Python - Service Architecture Analyzer

Located in `/python/`, this toolkit analyzes GitLab repositories to document microservice architecture and connections:

**Main Components:**
- `gitlab_service_analyzer.py` - Crawls GitLab repos and generates architecture documentation
- `connectivity_analyzer.py` - Core analysis engine for configs and code
- `check_dependencies.py` - Verifies/installs Python packages
- `setup_tools.py` - Environment setup helper
- `setup.sh` - Quick start script for Rocky 8.10 WSL

**Features:**
- Analyzes docker-compose, Dockerfile, Kubernetes manifests
- Scans code for HTTP APIs, database connections, message queues
- Generates markdown documentation with connection matrices
- Detects: HTTP/REST, gRPC, Databases, Message Queues, etc.

**Quick Start:**
```bash
cd python
bash setup.sh                    # First-time setup
python3 gitlab_service_analyzer.py --init-config config.yaml
# Edit config.yaml with GitLab token
python3 gitlab_service_analyzer.py --config config.yaml
cat architecture.md              # Review output
```

See `/python/README.md` for complete documentation.

## Notes

- Tools should be designed for reusability across projects
- Documentation should include dependencies and system requirements
- Consider cross-platform compatibility where applicable
- All Python tools work on Rocky 8.10 and other Linux distributions
