# Tools

A collection of utility scripts and automation tools for managing development projects.

## Overview

This repository contains reusable scripts across multiple languages and technologies:

- **Python**: General-purpose scripting and automation (including service architecture analyzer)
- **TCL**: EDA tool automation and hardware design workflows
- **Make**: Build systems and task orchestration
- **Shell**: System-level operations and integration
- **Other**: Miscellaneous tools in other languages

## Quick Start

**New to the tools?** Start here:
1. Read [Getting Started](./docs/guides/GETTING_STARTED.md) for quick overview
2. Follow [Installation Guide](./docs/guides/INSTALLATION.md) for setup
3. Check [Service Analyzer How-To](./docs/guides/SERVICE_ANALYZER_HOWTO.md) for usage

**Need help?** See [Documentation](./docs/README.md) for complete guides and references.

## Directory Structure

```
tools/
├── docs/                    Complete documentation
│   ├── guides/              How-to guides and tutorials
│   ├── references/          Technical reference
│   └── examples/            Example configurations
├── python/                  Python utilities
│   ├── gitlab_service_analyzer.py     Service crawler
│   ├── connectivity_analyzer.py       Analysis engine
│   ├── check_dependencies.py          Dependency manager
│   ├── setup.sh                       Quick setup
│   └── README.md                      Tool documentation
├── tcl/                     TCL scripts
├── make/                    Makefiles
├── shell/                   Shell scripts
└── other/                   Other tools
```

## Main Tools

### Python - GitLab Service Architecture Analyzer

Crawls GitLab repositories and generates documentation of service connections.

**Key Features:**
- Analyzes docker-compose, Dockerfile, Kubernetes manifests
- Scans code for HTTP APIs, databases, message queues
- Generates markdown documentation with connection matrices
- Outputs JSON summaries for tool integration

**Quick Start:**
```bash
cd python
bash setup.sh                                  # Setup
python3 gitlab_service_analyzer.py --init-config config.yaml  # Create config
nano config.yaml                               # Add GitLab token
python3 gitlab_service_analyzer.py --config config.yaml      # Run analysis
cat architecture.md                            # Review output
```

**Documentation:** See [docs/guides/SERVICE_ANALYZER_HOWTO.md](./docs/guides/SERVICE_ANALYZER_HOWTO.md)

## Documentation

Complete documentation is in the `docs/` folder:

### For Users
- **Getting Started**: [5-minute quick start](./docs/guides/GETTING_STARTED.md)
- **Installation**: [Setup for different platforms](./docs/guides/INSTALLATION.md)
- **Service Analyzer Guide**: [Complete usage documentation](./docs/guides/SERVICE_ANALYZER_HOWTO.md)
- **Troubleshooting**: [Solutions for common issues](./docs/guides/TROUBLESHOOTING.md)

### For Reference
- **Tool Commands**: [Command line reference](./docs/references/TOOL_REFERENCE.md)
- **Configuration**: [All configuration options](./docs/references/CONFIGURATION.md)
- **Examples**: [Real-world use cases](./docs/examples/)

## System Requirements

- **Python:** 3.8 or higher
- **Git:** Any recent version
- **Disk Space:** 500MB+ for analysis
- **Network:** Access to your GitLab instance

## Installation

### Rocky 8.10 WSL / Linux

```bash
git clone https://github.com/mgtinker/Tools.git
cd tools/python
bash setup.sh
nano config.yaml   # Add GitLab token
python3 gitlab_service_analyzer.py --config config.yaml
```

### macOS

```bash
brew install python3 git
git clone https://github.com/mgtinker/Tools.git
cd tools/python
bash setup.sh
```

**More details:** See [Installation Guide](./docs/guides/INSTALLATION.md)

## Usage Examples

### Analyze All Projects
```bash
python3 gitlab_service_analyzer.py --config config.yaml
```

### Analyze Specific Group
```bash
python3 gitlab_service_analyzer.py --group-id 42
```

### Fast Analysis (Config Only)
```bash
# Edit config.yaml: set analyze_code: false
python3 gitlab_service_analyzer.py --config config.yaml
```

**More examples:** See [Examples](./docs/examples/)

## Configuration

Create `config.yaml` with:

```yaml
gitlab:
  url: 'https://gitlab.example.com'
  token: 'glpat-your-token'
  group_id: null

output:
  markdown_file: 'architecture.md'

analysis:
  analyze_code: true
  analyze_configs: true
```

**Detailed reference:** See [Configuration Reference](./docs/references/CONFIGURATION.md)

## Output

### architecture.md
Markdown file with:
- Service overview by repository
- Detailed connection diagrams
- Connection type statistics
- Service-to-service matrix

### services.json
JSON summary for integration with other tools

## Getting Help

1. **Quick questions?** → [Getting Started](./docs/guides/GETTING_STARTED.md)
2. **Setup issues?** → [Installation Guide](./docs/guides/INSTALLATION.md)
3. **Usage questions?** → [Service Analyzer How-To](./docs/guides/SERVICE_ANALYZER_HOWTO.md)
4. **Troubleshooting?** → [Troubleshooting Guide](./docs/guides/TROUBLESHOOTING.md)
5. **Command reference?** → [Tool Reference](./docs/references/TOOL_REFERENCE.md)

## Contributing

When adding new tools:
1. Create tool in appropriate directory (python/, tcl/, etc)
2. Add README.md documenting the tool
3. Update docs with tool information
4. Add examples to docs/examples/

## License

This repository is licensed under the **Commons Clause + MIT License** with custom commercial restrictions.

**Summary:**
- ✅ **Non-Commercial Use**: Free for educational, personal, and open-source projects
- ✅ **Internal Tools**: Free to use within your organization (not sold/offered externally)
- ❌ **Commercial Use**: Requires a Commercial License Agreement (selling, building services, derivatives)

**Learn more:**
- **Quick Reference**: See [COMMERCIAL_USE.md](./COMMERCIAL_USE.md) for allowed/restricted activities
- **Full Legal Terms**: See [LICENSE](./LICENSE) for complete legal text
- **Commercial Inquiry**: Open a GitHub Issue titled "Commercial License Inquiry"

## Support

- **Documentation:** [docs/](./docs/README.md)
- **Issues:** Check [Troubleshooting Guide](./docs/guides/TROUBLESHOOTING.md)
- **Repository:** https://github.com/mgtinker/Tools
