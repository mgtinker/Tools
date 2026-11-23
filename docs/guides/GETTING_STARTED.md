# Getting Started with mgtinker/tools

A quick introduction to the tools repository and its main features.

## What Are These Tools?

The mgtinker/tools repository contains utility scripts designed to help you understand and document your microservice architecture, particularly for services running in Docker and Kubernetes.

**Main capability:** Analyze GitLab repositories and automatically generate documentation showing how your services connect and communicate.

## 5-Minute Quick Start

### 1. Check What You Need
```bash
python3 --version    # Need 3.8 or higher
git --version        # Need git
```

### 2. Clone the Repository
```bash
git clone https://github.com/mgtinker/Tools.git
cd tools
```

### 3. Set Up (Rocky 8.10 WSL or Linux)
```bash
cd python
bash setup.sh
```

### 4. Configure
```bash
nano config.yaml
```
Add your GitLab details:
- GitLab URL (e.g., `https://gitlab.example.com`)
- Personal access token from GitLab
- Optional: specific group ID to analyze

### 5. Run Analysis
```bash
python3 gitlab_service_analyzer.py --config config.yaml
```

### 6. Review Results
```bash
cat architecture.md
```

Done! You now have documentation of your service architecture.

## Understanding the Tools

### The Main Tool: GitLab Service Analyzer

**What it does:**
- Connects to your GitLab instance
- Clones all your repository code
- Analyzes configuration files (docker-compose, Dockerfile, etc)
- Scans code for service references
- Generates markdown documentation

**What you get:**
- `architecture.md` - Complete service architecture documentation
- `services.json` - JSON data for tools/dashboards
- Understanding of how your services connect

### Supporting Tools

**check_dependencies.py**
- Verifies Python packages are installed
- Can auto-install missing packages
- Useful when setup.sh isn't available

**setup.sh & setup_tools.py**
- Prepare your environment
- Create virtual environment
- Install dependencies
- Generate configuration templates

## Common Scenarios

### Scenario 1: "I want to document my service architecture"

1. Create GitLab token: https://your-gitlab.com/-/user_settings/personal_access_tokens
2. Run: `bash python/setup.sh`
3. Edit `python/config.yaml` with your token
4. Run: `python3 python/gitlab_service_analyzer.py --config python/config.yaml`
5. Share `architecture.md` with your team

**Time:** ~5-10 minutes (depending on repository size)

### Scenario 2: "I need to set up on a new machine"

1. Clone: `git clone https://github.com/mgtinker/Tools.git`
2. Navigate: `cd tools/python`
3. Setup: `bash setup.sh`
4. Configure: `nano config.yaml`
5. Run: `python3 gitlab_service_analyzer.py --config config.yaml`

**Time:** ~15 minutes (includes dependency installation)

### Scenario 3: "I want to analyze only a specific group"

Edit `config.yaml`:
```yaml
gitlab:
  group_id: 123  # Set to your group ID
```

Then run as normal.

### Scenario 4: "I already have dependencies installed"

Skip setup:
```bash
python3 gitlab_service_analyzer.py --init-config config.yaml
nano config.yaml
python3 gitlab_service_analyzer.py --config config.yaml
```

## What Gets Analyzed

The tools look for:

**Configuration Files:**
- `docker-compose.yml` - Container orchestration
- `Dockerfile` - Container images and metadata
- `kubernetes.yaml` - Kubernetes deployments

**Code Patterns:**
- HTTP API calls (requests library, fetch, curl)
- Database connections (PostgreSQL, MySQL, MongoDB)
- Message queues (Kafka, RabbitMQ)
- Cache connections (Redis)
- Environment variable references

**Connection Types Found:**
- Service-to-service HTTP calls
- Database connections
- Message queue connections
- Docker links and dependencies
- Kubernetes configuration references

## Understanding the Output

### architecture.md

The markdown file contains:

```markdown
# Service Architecture Documentation

## Service Overview
Lists all discovered services organized by repository

## Service Connections
Shows how services connect to each other:
  gateway-service → auth-service (http)
  gateway-service → postgres-db (postgresql)
  auth-service → redis-cache (redis)

## Connection Matrix
ASCII table showing all connections at a glance
```

### services.json

JSON data for integration with other tools:
```json
{
  "auth-service": {
    "repo": "auth-services",
    "image": "python:3.11-slim",
    "language": "python",
    "ports": ["8080"],
    "connections": 3
  }
}
```

## Next Steps

**New to these tools?**
→ Read [Installation Guide](./guides/INSTALLATION.md) for detailed setup

**Want to use the analyzer?**
→ Read [Service Analyzer How-To](./guides/SERVICE_ANALYZER_HOWTO.md)

**Running into issues?**
→ See [Troubleshooting Guide](./guides/TROUBLESHOOTING.md)

**Need command reference?**
→ See [Tool Reference](./references/TOOL_REFERENCE.md)

## Frequently Asked Questions

**Q: Do I need admin access to GitLab?**
A: No, just a personal access token with read permissions.

**Q: How long does analysis take?**
A: Depends on repository size. Usually 2-5 minutes per 10 repos.

**Q: Can I analyze only specific projects?**
A: Yes, set `group_id` in config.yaml or exclude patterns.

**Q: What if my GitLab is self-hosted?**
A: Set the full URL in config: `https://my-gitlab.company.com`

**Q: Does it modify my repositories?**
A: No, it only reads configuration and code files.

**Q: Can I keep the cloned repositories?**
A: Yes, use `--keep-repos` flag to prevent cleanup.

**Q: What if analysis fails?**
A: See [Troubleshooting Guide](./guides/TROUBLESHOOTING.md) for common issues.

## Important Notes

💡 **Tip:** Keep your config.yaml in a safe location (don't commit to git)

⚠️ **Warning:** Your GitLab token is sensitive. Treat it like a password.

✨ **Hint:** The first run is slower as it clones all repos. Subsequent runs can be faster if you use `--keep-repos`.

## Keyboard Shortcuts (During Analysis)

No interactive mode - analysis runs to completion.
To stop early: `Ctrl+C`

## Getting Help

1. **Installation issues?** → See [Installation Guide](./guides/INSTALLATION.md)
2. **Configuration questions?** → See [Configuration Reference](./references/CONFIGURATION.md)
3. **Need examples?** → See [Examples](./examples/)
4. **Still stuck?** → See [Troubleshooting](./guides/TROUBLESHOOTING.md)

---

Ready? Start with [Installation Guide](./guides/INSTALLATION.md) or jump to [Service Analyzer How-To](./guides/SERVICE_ANALYZER_HOWTO.md).
