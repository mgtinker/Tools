# Examples

Real-world examples and use cases for mgtinker/tools.

## Table of Contents

1. [Configuration Examples](#configuration-examples)
2. [Output Examples](#output-examples)
3. [Use Cases](#use-cases)

## Configuration Examples

### Example 1: Analyze All GitLab Cloud Projects

**Scenario:** You have GitLab.com account with multiple projects

**Configuration:**
```yaml
# config_cloud.yaml
gitlab:
  url: 'https://gitlab.com'
  token: 'glpat-your-gitlab-com-token'
  group_id: null  # Analyze all projects

output:
  markdown_file: 'architecture.md'
  json_file: 'services.json'

analysis:
  analyze_configs: true
  analyze_code: true

cleanup_after: true
```

**Command:**
```bash
python3 gitlab_service_analyzer.py --config config_cloud.yaml
```

**Result:** Documents all your services across all GitLab projects.

---

### Example 2: Analyze Company Self-Hosted GitLab

**Scenario:** Company has private GitLab with multiple teams/groups

**Configuration:**
```yaml
# config_company.yaml
gitlab:
  url: 'https://gitlab.internal.company.com'
  token: 'glpat-company-token'
  group_id: null

output:
  markdown_file: 'company_architecture.md'

analysis:
  analyze_configs: true
  analyze_code: true

temp_directory: '/mnt/ssd/gitlab_analysis'
cleanup_after: true

advanced:
  concurrent_clones: 4
  exclude_projects:
    - '^archived-'
    - '^example-'

logging:
  level: 'INFO'
  file: 'company_analysis.log'
```

**Command:**
```bash
python3 gitlab_service_analyzer.py --config config_company.yaml
```

---

### Example 3: Analyze Specific Team/Group

**Scenario:** You only need backend services architecture

**Configuration:**
```yaml
# config_backend.yaml
gitlab:
  url: 'https://gitlab.com'
  token: 'glpat-your-token'
  group_id: 123  # Backend team group ID

output:
  markdown_file: 'backend_architecture.md'

analysis:
  analyze_configs: true
  analyze_code: true
  code_patterns:
    - '*.py'
    - '*.go'
    - '*.rs'

cleanup_after: true
```

**Command:**
```bash
python3 gitlab_service_analyzer.py --config config_backend.yaml
```

**Result:** Only backend services documented.

---

### Example 4: Fast Analysis (Config Only)

**Scenario:** You need quick results without deep code scanning

**Configuration:**
```yaml
# config_fast.yaml
gitlab:
  url: 'https://gitlab.com'
  token: 'glpat-your-token'

output:
  markdown_file: 'quick_architecture.md'

analysis:
  analyze_configs: true
  analyze_code: false  # Skip code scanning

cleanup_after: true
```

**Command:**
```bash
python3 gitlab_service_analyzer.py --config config_fast.yaml
```

**Result:** 10x faster, but only config-level connections.

---

### Example 5: Production Analysis with Logging

**Scenario:** Running analysis in production environment

**Configuration:**
```yaml
# config_production.yaml
gitlab:
  url: 'https://gitlab.internal.company.com'
  token: 'glpat-prod-token'
  group_id: 1

output:
  markdown_file: '/srv/docs/architecture.md'
  json_file: '/srv/data/services.json'

analysis:
  analyze_configs: true
  analyze_code: true

temp_directory: '/mnt/ssd/analysis'
cleanup_after: true

advanced:
  max_repo_size: 500
  concurrent_clones: 4
  exclude_projects:
    - '^archived-'
    - '^test-'

logging:
  level: 'WARNING'  # Quiet in production
  file: '/var/log/gitlab_analyzer.log'
```

**Command:**
```bash
python3 gitlab_service_analyzer.py --config config_production.yaml
```

---

## Output Examples

### Example: Generated architecture.md

```markdown
# Service Architecture Documentation

Generated: 2024-11-23 10:30:45

## Table of Contents

1. [Service Overview](#service-overview)
2. [Service Connections](#service-connections)
3. [Repositories](#repositories)
4. [Connection Matrix](#connection-matrix)

## Service Overview

Total Services: 8
Total Repositories: 3
Total Connections: 12

### Services by Repository

#### auth-services
- **auth-service**
  - Image: `python:3.11-slim`
  - Language: python
  - Ports: 8080

#### api-gateway
- **gateway-service**
  - Image: `node:18-alpine`
  - Language: javascript
  - Ports: 3000

#### database-services
- **postgres-primary**
  - Image: `postgres:15-alpine`

## Service Connections

### Detailed Connections

#### auth-service
- **→ postgres-primary** (postgresql)
  - Found in: `src/database.py`
- **→ redis-cache** (redis)
  - Found in: `config/cache.yaml`

#### gateway-service
- **→ auth-service** (http)
  - Found in: `src/auth.js`
- **→ api-service** (http)
  - Found in: `src/routing.js`

#### api-service
- **→ postgres-primary** (postgresql)
  - Found in: `models/database.go`
- **→ message-queue** (message_queue)
  - Found in: `config/kafka.yaml`

## Connection Matrix

```
              auth  gateway  api  postgres  redis  queue
auth             -       -    -       1      1      -
gateway          1       -    1       -      -      -
api              -       1    -       1      -      1
postgres         -       -    -       -      -      -
redis            -       -    -       -      -      -
queue            -       -    -       -      -      -
```

## Repositories

### auth-services
Services: 1
- auth-service

### api-gateway
Services: 2
- gateway-service
- api-service

### database-services
Services: 1
- postgres-primary
```

---

### Example: Generated services.json

```json
{
  "auth-service": {
    "repo": "auth-services",
    "image": "python:3.11-slim",
    "language": "python",
    "ports": ["8080"],
    "connections": 2
  },
  "gateway-service": {
    "repo": "api-gateway",
    "image": "node:18-alpine",
    "language": "javascript",
    "ports": ["3000"],
    "connections": 2
  },
  "api-service": {
    "repo": "api-gateway",
    "image": "go:1.21-alpine",
    "language": "go",
    "ports": ["5000"],
    "connections": 3
  },
  "postgres-primary": {
    "repo": "database-services",
    "image": "postgres:15-alpine",
    "language": "sql",
    "ports": ["5432"],
    "connections": 2
  },
  "redis-cache": {
    "repo": "cache-services",
    "image": "redis:7-alpine",
    "language": "none",
    "ports": ["6379"],
    "connections": 1
  }
}
```

---

## Use Cases

### Use Case 1: Documenting New Architecture

**Goal:** Document your new microservices architecture

**Steps:**
1. Create personal access token on GitLab
2. Copy `config.example.yaml` to `my_config.yaml`
3. Update with your GitLab URL and token
4. Run: `python3 gitlab_service_analyzer.py --config my_config.yaml`
5. Share `architecture.md` with team
6. Store in wiki/documentation system

**Benefits:**
- Automatic documentation
- Always up-to-date
- Clear view of connections
- Easy to share

---

### Use Case 2: Onboarding New Team Members

**Goal:** Help new developers understand system architecture

**Steps:**
1. Generate `architecture.md` from latest code
2. Add explanatory notes
3. Share as part of onboarding
4. Provides context for microservices
5. Shows service dependencies

**Benefits:**
- Faster onboarding
- Clear service map
- Reduces questions
- Living documentation

---

### Use Case 3: Architecture Review

**Goal:** Audit existing services before refactoring

**Steps:**
1. Run analyzer on current codebase
2. Review generated `architecture.md`
3. Identify heavily-connected services
4. Find bottlenecks
5. Plan refactoring

**Example output review:**
```
# High-connection services (refactor candidates)
- gateway-service: 5 connections
- auth-service: 4 connections
- api-service: 3 connections

# Could benefit from:
- API gateway consolidation
- Shared library extraction
- Event-driven architecture
```

---

### Use Case 4: CI/CD Pipeline Integration

**Goal:** Automatically update documentation on each commit

**Script:**
```bash
#!/bin/bash
# .gitlab-ci.yml or similar

generate_docs:
  stage: post
  script:
    - cd tools/python
    - python3 gitlab_service_analyzer.py --config config.yaml
    - cp architecture.md ../../docs/
  artifacts:
    paths:
      - docs/architecture.md
  only:
    - main
```

**Benefits:**
- Docs always current
- Automatic updates
- Catch service changes
- Audit trail

---

### Use Case 5: Multi-Group Analysis

**Goal:** Generate separate docs for each team

**Script:**
```bash
#!/bin/bash

# Backend team
python3 gitlab_service_analyzer.py \
  --config config.yaml \
  --group-id 42 \
  --output backend_arch.md

# Frontend team
python3 gitlab_service_analyzer.py \
  --config config.yaml \
  --group-id 99 \
  --output frontend_arch.md

# Infra team
python3 gitlab_service_analyzer.py \
  --config config.yaml \
  --group-id 101 \
  --output infra_arch.md
```

**Result:** Separate documentation per team.

---

### Use Case 6: Performance Analysis

**Goal:** Identify performance issues by analyzing connections

**Analysis:**
```
# Services with many connections might be:
- Bottlenecks
- Single points of failure
- Candidates for caching
- Load balancing targets

# Example:
postgres-primary: 7 connections
  ← Potential bottleneck
  ← Consider read replicas
  ← Cache frequently accessed data
```

---

## Tips for Success

### 1. First Run - Start Simple
```bash
# Create default config
python3 gitlab_service_analyzer.py --init-config config.yaml

# Edit with your token
nano config.yaml

# Run with keep-repos to inspect results
python3 gitlab_service_analyzer.py \
  --config config.yaml \
  --keep-repos
```

### 2. Review Generated Files
```bash
# Check markdown
cat architecture.md | head -50

# Check JSON
python3 -m json.tool services.json | head -20

# Inspect cloned repos
ls -la /tmp/gitlab_analysis/
```

### 3. Customize for Your Needs

**Too many connections?**
```yaml
analysis:
  analyze_code: false  # Skip code, use configs only
```

**Too slow?**
```yaml
advanced:
  max_repo_size: 200
  concurrent_clones: 4
```

**Wrong projects?**
```yaml
advanced:
  include_projects:
    - '^services/'  # Only production
```

### 4. Schedule Regular Runs

```bash
# Add to crontab (weekly)
0 2 * * 0 cd /path/to/tools/python && \
  python3 gitlab_service_analyzer.py --config config.yaml
```

### 5. Version Control

```bash
# Track changes in git
git add architecture.md
git commit -m "Update service architecture docs"
git push
```

---

## See Also

- [Service Analyzer How-To](../guides/SERVICE_ANALYZER_HOWTO.md)
- [Configuration Reference](../references/CONFIGURATION.md)
- [Tool Reference](../references/TOOL_REFERENCE.md)
