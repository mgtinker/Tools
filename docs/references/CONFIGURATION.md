# Configuration Reference

Complete reference for all configuration options in mgtinker/tools.

## Overview

Configuration is handled via YAML files for the GitLab Service Analyzer.

**Default file:** `config.yaml`
**Example file:** `config.example.yaml`

## Configuration Sections

1. [GitLab Connection](#gitlab-connection)
2. [Output Files](#output-files)
3. [Analysis Options](#analysis-options)
4. [Temporary Files](#temporary-files)
5. [Advanced Options](#advanced-options)
6. [Logging](#logging)

---

## GitLab Connection

Configure your GitLab instance connection.

### Required Settings

```yaml
gitlab:
  url: 'https://gitlab.example.com'
  token: 'glpat-xxxxxxxxxxxx'
```

### Optional Settings

```yaml
gitlab:
  url: 'https://gitlab.example.com'
  token: 'glpat-xxxxxxxxxxxx'
  group_id: null  # null = all projects, number = specific group
```

### Options Reference

#### `url` (required)
- **Type:** String
- **Format:** Full HTTPS URL
- **Examples:**
  - `'https://gitlab.com'` (GitLab cloud)
  - `'https://gitlab.example.com'` (self-hosted)
  - `'https://gitlab.internal.company.com'` (internal)
- **Notes:**
  - Must include `https://`
  - Should NOT have trailing slash
  - Self-hosted URL must be reachable from your network

#### `token` (required)
- **Type:** String
- **Format:** GitLab personal access token
- **Example:** `'glpat-aBcDeFgHiJkLmNoP'`
- **Notes:**
  - Create at: `https://your-gitlab.com/-/user_settings/personal_access_tokens`
  - Required scopes: `api`, `read_api`, `read_repository`
  - Treat as sensitive - don't commit to git
  - Don't share publicly

#### `group_id` (optional)
- **Type:** Number or null
- **Default:** `null`
- **Examples:**
  - `null` - Analyze all accessible projects
  - `42` - Analyze only group with ID 42
- **Notes:**
  - Find group ID: `https://your-gitlab.com/groups/YOUR-GROUP/-/settings/general`
  - Useful to limit analysis to specific team
  - Significantly speeds up analysis on large instances

### Examples

**Analyze all projects:**
```yaml
gitlab:
  url: 'https://gitlab.com'
  token: 'glpat-your-token'
  group_id: null
```

**Analyze specific group:**
```yaml
gitlab:
  url: 'https://gitlab.com'
  token: 'glpat-your-token'
  group_id: 123
```

**Self-hosted GitLab:**
```yaml
gitlab:
  url: 'https://gitlab.internal.company.com'
  token: 'glpat-company-token'
  group_id: 1
```

---

## Output Files

Configure where analysis results are written.

```yaml
output:
  markdown_file: 'architecture.md'
  json_file: 'services.json'
```

### Options Reference

#### `markdown_file` (required)
- **Type:** String
- **Default:** `'architecture.md'`
- **Format:** File path (relative or absolute)
- **Examples:**
  - `'architecture.md'` (current directory)
  - `'/home/user/docs/architecture.md'` (absolute path)
  - `'./output/arch.md'` (relative path)
- **Notes:**
  - Overwrites existing file
  - Can be overridden with `--output` command-line flag
  - Should end with `.md` extension

#### `json_file` (optional)
- **Type:** String
- **Default:** `'services.json'`
- **Format:** File path
- **Examples:**
  - `'services.json'`
  - `'/tmp/services_backup.json'`
- **Notes:**
  - Skipped if not specified
  - Useful for tool integration
  - Machine-readable format

### Examples

**Default output:**
```yaml
output:
  markdown_file: 'architecture.md'
  json_file: 'services.json'
```

**Custom locations:**
```yaml
output:
  markdown_file: '/home/user/projects/docs/service_arch.md'
  json_file: '/home/user/projects/data/services.json'
```

**Markdown only:**
```yaml
output:
  markdown_file: 'architecture.md'
  # json_file: omitted
```

---

## Analysis Options

Control what gets analyzed and how.

```yaml
analysis:
  analyze_configs: true
  analyze_code: true
  code_patterns:
    - '*.py'
    - '*.js'
    - '.env'
  connection_types:
    - http
    - database
    - message_queue
```

### Options Reference

#### `analyze_configs` (optional)
- **Type:** Boolean
- **Default:** `true`
- **Examples:**
  - `true` - Analyze docker-compose, Dockerfile, Kubernetes
  - `false` - Skip config analysis
- **Notes:**
  - Relatively fast
  - Recommended to keep enabled
  - Finds container orchestration relationships

#### `analyze_code` (optional)
- **Type:** Boolean
- **Default:** `true`
- **Examples:**
  - `true` - Scan code files for connections
  - `false` - Skip code analysis
- **Notes:**
  - Can be slow on large codebases
  - Finds HTTP APIs, databases, etc.
  - Set to `false` for faster analysis

#### `code_patterns` (optional)
- **Type:** Array of strings
- **Default:** `['*.py', '*.js', '*.ts', '*.go', '.env*']`
- **Examples:**
  ```yaml
  code_patterns:
    - '*.py'          # Python files
    - '*.js'          # JavaScript files
    - '*.ts'          # TypeScript files
    - '*.go'          # Go files
    - '*.java'        # Java files
    - '.env'          # Environment files
    - '*.conf'        # Config files
    - '*.yaml'        # YAML files
  ```
- **Notes:**
  - Use glob patterns
  - Add more for comprehensive scanning
  - Add fewer for faster analysis

#### `connection_types` (optional)
- **Type:** Array of strings
- **Default:** All types
- **Examples:**
  ```yaml
  connection_types:
    - http              # HTTP/REST APIs
    - grpc              # gRPC services
    - database          # Generic databases
    - postgresql        # PostgreSQL specific
    - mysql             # MySQL specific
    - mongodb           # MongoDB specific
    - redis             # Redis cache
    - message_queue     # Message queues (Kafka, RabbitMQ)
    - dependency        # Docker Compose depends_on
    - environment       # Environment variables
    - network           # Docker network links
    - k8s_env           # Kubernetes env configs
  ```
- **Notes:**
  - Filters what connections are reported
  - Subset to focus on specific types
  - Useful for large analyses

### Examples

**Complete analysis (default):**
```yaml
analysis:
  analyze_configs: true
  analyze_code: true
  code_patterns:
    - '*.py'
    - '*.js'
    - '*.ts'
    - '*.go'
    - '.env*'
  connection_types:
    - http
    - database
    - message_queue
```

**Fast analysis (config only):**
```yaml
analysis:
  analyze_configs: true
  analyze_code: false
```

**Code only (no container configs):**
```yaml
analysis:
  analyze_configs: false
  analyze_code: true
  code_patterns:
    - '*.py'
    - '*.js'
```

**Specific languages:**
```yaml
analysis:
  analyze_configs: true
  analyze_code: true
  code_patterns:
    - '*.py'
    - '*.go'
```

---

## Temporary Files

Control how temporary repository clones are handled.

```yaml
temp_directory: '/tmp/gitlab_analysis'
cleanup_after: true
```

### Options Reference

#### `temp_directory` (optional)
- **Type:** String
- **Default:** `'/tmp/gitlab_analysis'`
- **Format:** File path (must exist or be creatable)
- **Examples:**
  - `'/tmp/gitlab_analysis'` (default)
  - `/mnt/large_disk/gitlab_analysis` (different disk)
  - `/home/user/temp_analysis` (home directory)
- **Notes:**
  - Repositories cloned here temporarily
  - Should have 500MB+ free space
  - Use different disk if running out of space

#### `cleanup_after` (optional)
- **Type:** Boolean
- **Default:** `true`
- **Examples:**
  - `true` - Delete clones after analysis (default)
  - `false` - Keep clones for inspection
- **Notes:**
  - Use `false` for debugging
  - Use `true` for production (saves disk)
  - Can override with `--keep-repos` flag

### Examples

**Default cleanup:**
```yaml
temp_directory: '/tmp/gitlab_analysis'
cleanup_after: true
```

**Keep for inspection:**
```yaml
temp_directory: '/tmp/gitlab_analysis'
cleanup_after: false
```

**Large disk:**
```yaml
temp_directory: '/mnt/large_disk/gitlab_analysis'
cleanup_after: true
```

---

## Advanced Options

Fine-tune performance and behavior.

```yaml
advanced:
  max_repo_size: 500
  clone_timeout: 300
  concurrent_clones: 1
  exclude_projects: []
  include_projects: []
```

### Options Reference

#### `max_repo_size` (optional)
- **Type:** Number
- **Default:** `500` (MB)
- **Examples:**
  - `500` - Skip repos larger than 500MB
  - `200` - Skip repos larger than 200MB
  - `1000` - Allow up to 1GB
- **Notes:**
  - Skips very large repositories
  - Saves time and disk space
  - Set to 0 to disable

#### `clone_timeout` (optional)
- **Type:** Number
- **Default:** `300` (seconds)
- **Examples:**
  - `300` - 5 minute timeout
  - `600` - 10 minute timeout
  - `60` - 1 minute timeout
- **Notes:**
  - Timeout for git clone operations
  - Increase for slow networks

#### `concurrent_clones` (optional)
- **Type:** Number
- **Default:** `1`
- **Examples:**
  - `1` - Sequential cloning (safe)
  - `4` - 4 concurrent clones (faster)
  - `8` - 8 concurrent clones (risk of overload)
- **Notes:**
  - Higher = faster but higher resource usage
  - Start with 1, increase cautiously
  - Balance with network/disk I/O

#### `exclude_projects` (optional)
- **Type:** Array of strings (regex patterns)
- **Default:** `[]`
- **Examples:**
  ```yaml
  exclude_projects:
    - '^archived-'      # Projects starting with 'archived-'
    - '^test-'          # Projects starting with 'test-'
    - 'deprecated'      # Contains 'deprecated'
    - '\.old$'          # Ends with '.old'
  ```
- **Notes:**
  - Regex patterns (use `^` and `$` for exact match)
  - Skips matching projects
  - Useful to ignore old/archived projects

#### `include_projects` (optional)
- **Type:** Array of strings (regex patterns)
- **Default:** `[]` (all projects)
- **Examples:**
  ```yaml
  include_projects:
    - '^services/'      # Only projects under 'services/'
    - 'production'      # Only production projects
    - '^api-'           # Only projects starting with 'api-'
  ```
- **Notes:**
  - Whitelist - only matches are included
  - Overrides `exclude_projects`
  - Empty = include all

### Examples

**Default (no filtering):**
```yaml
advanced:
  max_repo_size: 500
  clone_timeout: 300
  concurrent_clones: 1
```

**Faster cloning:**
```yaml
advanced:
  max_repo_size: 500
  concurrent_clones: 4
```

**Small repos only:**
```yaml
advanced:
  max_repo_size: 100
  exclude_projects:
    - '^large-'
    - 'archive'
```

**Specific projects:**
```yaml
advanced:
  include_projects:
    - '^services/'
    - 'production'
```

---

## Logging

Configure output logging and debugging.

```yaml
logging:
  level: 'INFO'
  file: 'analyzer.log'
```

### Options Reference

#### `level` (optional)
- **Type:** String
- **Default:** `'INFO'`
- **Options:**
  - `'DEBUG'` - Very verbose, all details
  - `'INFO'` - Standard output
  - `'WARNING'` - Only warnings
  - `'ERROR'` - Only errors
- **Examples:**
  - `'DEBUG'` - Use for troubleshooting
  - `'INFO'` - Standard operation
  - `'ERROR'` - Production (quiet)
- **Notes:**
  - Higher = more output
  - Use DEBUG for troubleshooting

#### `file` (optional)
- **Type:** String
- **Default:** `'analyzer.log'`
- **Format:** File path
- **Examples:**
  - `'analyzer.log'` (current directory)
  - `'/var/log/analyzer.log'` (system log)
  - `'/tmp/debug.log'` (temp location)
- **Notes:**
  - Log file location
  - Appends to existing file
  - Useful for review after run

### Examples

**Standard operation:**
```yaml
logging:
  level: 'INFO'
  file: 'analyzer.log'
```

**Debug mode:**
```yaml
logging:
  level: 'DEBUG'
  file: 'debug.log'
```

**Quiet mode:**
```yaml
logging:
  level: 'WARNING'
  file: 'analyzer.log'
```

---

## Complete Examples

### Minimal Configuration

```yaml
gitlab:
  url: 'https://gitlab.com'
  token: 'glpat-your-token'

output:
  markdown_file: 'architecture.md'
```

### Standard Configuration

```yaml
gitlab:
  url: 'https://gitlab.com'
  token: 'glpat-your-token'
  group_id: null

output:
  markdown_file: 'architecture.md'
  json_file: 'services.json'

analysis:
  analyze_configs: true
  analyze_code: true

temp_directory: '/tmp/gitlab_analysis'
cleanup_after: true
```

### Production Configuration

```yaml
gitlab:
  url: 'https://gitlab.internal.company.com'
  token: 'glpat-prod-token'
  group_id: 1

output:
  markdown_file: '/home/analyst/docs/architecture.md'
  json_file: '/home/analyst/data/services.json'

analysis:
  analyze_configs: true
  analyze_code: true
  code_patterns:
    - '*.py'
    - '*.js'
    - '*.ts'

temp_directory: '/mnt/data/gitlab_analysis'
cleanup_after: true

advanced:
  max_repo_size: 500
  concurrent_clones: 4
  exclude_projects:
    - '^archived-'
    - 'deprecated'

logging:
  level: 'INFO'
  file: '/var/log/gitlab_analyzer.log'
```

### High-Performance Configuration

```yaml
gitlab:
  url: 'https://gitlab.com'
  token: 'glpat-your-token'
  group_id: 42

output:
  markdown_file: 'architecture.md'

analysis:
  analyze_configs: true
  analyze_code: false  # Skip code for speed

advanced:
  max_repo_size: 200
  concurrent_clones: 8
  exclude_projects:
    - '^test-'
    - '^temp-'

cleanup_after: true
```

---

## Validation

Configuration is validated on startup. Common errors:

| Error | Fix |
|-------|-----|
| `Config file not found` | Check file path and name |
| `GitLab URL invalid` | Use format: `https://gitlab.com` |
| `Token required` | Add personal access token |
| `Invalid group_id` | Use number or `null` |
| `Invalid temp directory` | Ensure path is writable |

---

## Tips

1. **Start simple** - Use default options, add complexity as needed
2. **Keep secrets safe** - Never commit `config.yaml` with real token
3. **Use group_id** - Significantly speeds up large instances
4. **Monitor disk space** - Set `cleanup_after: true` for production
5. **Enable debugging** - Use `DEBUG` level only when needed
6. **Document changes** - Comment why you modified defaults

---

## See Also

- [Service Analyzer How-To](../guides/SERVICE_ANALYZER_HOWTO.md) - Usage guide
- [Tool Reference](./TOOL_REFERENCE.md) - Commands and options
- [Troubleshooting](../guides/TROUBLESHOOTING.md) - Problem solving
