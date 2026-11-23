# Tools Documentation

Complete guides for using the mgtinker/tools repository and its utilities.

## Table of Contents

1. **[Getting Started](./guides/GETTING_STARTED.md)** - Quick start for all tools
2. **[Installation Guide](./guides/INSTALLATION.md)** - Setup instructions for different systems
3. **[Service Analyzer How-To](./guides/SERVICE_ANALYZER_HOWTO.md)** - Using the GitLab analyzer
4. **[Configuration Reference](./references/CONFIGURATION.md)** - Detailed config options
5. **[Tool Reference](./references/TOOL_REFERENCE.md)** - Command reference for all tools
6. **[Examples](./examples/)** - Real-world examples and use cases
7. **[Troubleshooting](./guides/TROUBLESHOOTING.md)** - Common issues and solutions
8. **[API Reference](./api/)** - Python API documentation

## Quick Links by Tool

### Python Service Analyzer
- **Purpose:** Analyze GitLab repositories and document service architecture
- **Main Script:** `python/gitlab_service_analyzer.py`
- **Quick Start:** See [Service Analyzer How-To](./guides/SERVICE_ANALYZER_HOWTO.md)
- **Docs:** `python/README.md`

### Dependency Checker
- **Purpose:** Verify and install Python dependencies
- **Script:** `python/check_dependencies.py`
- **Usage:** See [Tool Reference](./references/TOOL_REFERENCE.md#check_dependencies)

### Setup Tools
- **Purpose:** Configure Python environment
- **Scripts:** `python/setup.sh`, `python/setup_tools.py`
- **Quick Setup:** See [Installation Guide](./guides/INSTALLATION.md)

## Documentation Structure

```
docs/
├── README.md                  (this file)
├── guides/                    How-to guides and tutorials
│   ├── GETTING_STARTED.md
│   ├── INSTALLATION.md
│   ├── SERVICE_ANALYZER_HOWTO.md
│   └── TROUBLESHOOTING.md
├── references/                Technical reference docs
│   ├── CONFIGURATION.md
│   └── TOOL_REFERENCE.md
├── examples/                  Example configurations and outputs
│   ├── sample_config.yaml
│   ├── sample_output.md
│   └── README.md
└── api/                       API documentation
    └── connectivity_analyzer.md
```

## Common Tasks

### I want to analyze my GitLab services
→ See [Service Analyzer How-To](./guides/SERVICE_ANALYZER_HOWTO.md)

### I need to set up on Rocky 8.10 WSL
→ See [Installation Guide](./guides/INSTALLATION.md)

### I need to understand the config file
→ See [Configuration Reference](./references/CONFIGURATION.md)

### Something isn't working
→ See [Troubleshooting](./guides/TROUBLESHOOTING.md)

### I need all available commands
→ See [Tool Reference](./references/TOOL_REFERENCE.md)

### I want to extend the tools
→ See [API Reference](./api/connectivity_analyzer.md)

## Getting Help

1. **Read the relevant guide** in `docs/guides/`
2. **Check examples** in `docs/examples/`
3. **Review the reference** in `docs/references/`
4. **Check troubleshooting** for known issues
5. **Review tool README files** in their directories

## For Different Audiences

### For Users (New to the Tools)
1. Start: [Getting Started](./guides/GETTING_STARTED.md)
2. Setup: [Installation Guide](./guides/INSTALLATION.md)
3. Use: [Service Analyzer How-To](./guides/SERVICE_ANALYZER_HOWTO.md)

### For Administrators (Managing Deployment)
1. Review: [Installation Guide](./guides/INSTALLATION.md)
2. Configure: [Configuration Reference](./references/CONFIGURATION.md)
3. Troubleshoot: [Troubleshooting Guide](./guides/TROUBLESHOOTING.md)

### For Developers (Extending Tools)
1. Understand: [API Reference](./api/connectivity_analyzer.md)
2. Review: [Examples](./examples/)
3. See: Tool source code with inline comments

### For Documentation/Architecture Teams
1. Learn: [Service Analyzer How-To](./guides/SERVICE_ANALYZER_HOWTO.md)
2. Review: [Example Outputs](./examples/sample_output.md)
3. Configure: [Configuration Reference](./references/CONFIGURATION.md)

## Contributing to Documentation

When adding new tools:
1. Add tool to appropriate category directory
2. Create README.md in tool directory
3. Add section to `Tool Reference`
4. Add setup instructions to `Installation Guide`
5. Add example to `examples/`
6. Add troubleshooting tips if applicable

## Document Conventions

- **CLI commands:** Use `code blocks` with `$` prompt
- **Configuration:** Show YAML format
- **Output:** Show expected results
- **Warnings:** Use `⚠️` symbol
- **Notes:** Use `💡` symbol
- **Tips:** Use `✨` symbol

## Version Information

- **Last Updated:** 2026-11-23
- **Tools Version:** 1.0
- **Documentation Version:** 1.0

See [CHANGELOG.md](../CHANGELOG.md) for version history.
