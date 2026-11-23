#!/usr/bin/env python3
"""
GitLab Repository Service Architecture Analyzer

Crawls GitLab repositories and analyzes service-to-service connections
to generate architecture documentation.

Usage:
    python3 gitlab_service_analyzer.py --config config.yaml

Requirements:
    - See requirements.txt for Python dependencies
    - GitLab API access token (personal or group token)
"""

import sys
import json
import yaml
import argparse
import tempfile
from pathlib import Path
from typing import Dict, List, Set, Tuple
import subprocess
from dataclasses import asdict
from datetime import datetime

try:
    import gitlab
    import requests
except ImportError:
    print("Error: Required packages not installed.")
    print("Run: python3 check_dependencies.py --auto-install")
    sys.exit(1)

from connectivity_analyzer import (
    Service, ServiceConnection, DockerComposeAnalyzer,
    DockerfileAnalyzer, KubernetesAnalyzer, CodeAnalyzer
)


class GitLabAnalyzer:
    """Analyzes GitLab projects and services."""

    def __init__(self, gitlab_url: str, token: str, group_id: str = None):
        """Initialize GitLab connection."""
        self.gl = gitlab.Gitlab(gitlab_url, private_token=token, api_version=4)
        self.group_id = group_id
        self.repos_cache = {}

    def get_projects(self) -> List:
        """Get list of projects to analyze."""
        try:
            if self.group_id:
                group = self.gl.groups.get(self.group_id)
                projects = group.projects.list(all=True)
            else:
                projects = self.gl.projects.list(all=True, visibility='private')
            return projects
        except Exception as e:
            print(f"Error fetching projects: {e}")
            return []

    def clone_repo(self, project, temp_dir: Path) -> Path:
        """Clone repository to temp directory."""
        try:
            repo_path = temp_dir / project.name
            if repo_path.exists():
                return repo_path

            print(f"  Cloning {project.name}...", end=' ', flush=True)
            subprocess.run(
                ['git', 'clone', '--depth', '1', project.http_url_to_repo, str(repo_path)],
                capture_output=True,
                timeout=60,
                check=True
            )
            print("✓")
            return repo_path
        except Exception as e:
            print(f"✗ Error: {e}")
            return None


class RepositoryAnalyzer:
    """Analyzes a repository for services and connections."""

    CONFIG_FILES = {
        'docker-compose.yml': DockerComposeAnalyzer,
        'docker-compose.yaml': DockerComposeAnalyzer,
        'Dockerfile': DockerfileAnalyzer,
        'k8s.yaml': KubernetesAnalyzer,
        'k8s.yml': KubernetesAnalyzer,
        'kubernetes.yaml': KubernetesAnalyzer,
        'kubernetes.yml': KubernetesAnalyzer,
    }

    CODE_FILES = [
        '*.py', '*.js', '*.ts', '*.go', '*.java', '*.rb',
        '.env*', '*.conf', '*.config'
    ]

    def __init__(self, repo_path: Path, repo_name: str):
        """Initialize repository analyzer."""
        self.repo_path = repo_path
        self.repo_name = repo_name
        self.services: Dict[str, Service] = {}
        self.connections: List[ServiceConnection] = []

    def analyze(self) -> Tuple[Dict[str, Service], List[ServiceConnection]]:
        """Analyze repository for services."""
        print(f"  Analyzing {self.repo_name}...", end=' ', flush=True)

        try:
            self._analyze_configs()
            self._analyze_code()
            print("✓")
        except Exception as e:
            print(f"✗ Error: {e}")

        return self.services, self.connections

    def _analyze_configs(self):
        """Analyze configuration files."""
        for config_file, analyzer_class in self.CONFIG_FILES.items():
            config_path = self.repo_path / config_file
            if config_path.exists():
                try:
                    with open(config_path, 'r') as f:
                        content = f.read()

                    if analyzer_class == DockerComposeAnalyzer:
                        self._analyze_docker_compose(content, config_path)
                    elif analyzer_class == DockerfileAnalyzer:
                        self._analyze_dockerfile(content, config_path)
                    elif analyzer_class == KubernetesAnalyzer:
                        self._analyze_kubernetes(content, config_path)
                except Exception as e:
                    pass

    def _analyze_docker_compose(self, content: str, config_path: Path):
        """Extract services from docker-compose.yml."""
        try:
            import yaml
            compose = yaml.safe_load(content)
            if not compose or 'services' not in compose:
                return

            for service_name, service_config in compose['services'].items():
                if service_name not in self.services:
                    self.services[service_name] = Service(
                        name=service_name,
                        repo_name=self.repo_name,
                        root_path=self.repo_path
                    )

                svc = self.services[service_name]
                svc.image = service_config.get('image', '')
                svc.ports = service_config.get('ports', [])
                svc.environment = service_config.get('environment', {})
                svc.volumes = service_config.get('volumes', [])

                # Extract connections
                connections = DockerComposeAnalyzer.analyze(content, service_name, self.repo_name)
                self.connections.extend(connections)
                svc.connections.extend(connections)
        except Exception:
            pass

    def _analyze_dockerfile(self, content: str, config_path: Path):
        """Extract metadata from Dockerfile."""
        service_name = self.repo_name
        if service_name not in self.services:
            self.services[service_name] = Service(
                name=service_name,
                repo_name=self.repo_name,
                root_path=self.repo_path
            )

        metadata = DockerfileAnalyzer.analyze(content, service_name)
        svc = self.services[service_name]
        svc.image = metadata.get('base_image', '')
        svc.language = metadata.get('language', '')

    def _analyze_kubernetes(self, content: str, config_path: Path):
        """Extract from Kubernetes manifests."""
        # K8s manifests can define multiple resources
        try:
            import yaml
            docs = yaml.safe_load_all(content)
            for doc in docs:
                if not doc:
                    continue
                metadata = doc.get('metadata', {})
                service_name = metadata.get('name', 'unknown')

                if service_name not in self.services:
                    self.services[service_name] = Service(
                        name=service_name,
                        repo_name=self.repo_name,
                        root_path=self.repo_path
                    )

                connections = KubernetesAnalyzer.analyze(content, service_name)
                self.connections.extend(connections)
                self.services[service_name].connections.extend(connections)
        except Exception:
            pass

    def _analyze_code(self):
        """Analyze code files for service references."""
        for service_name in self.services:
            code_patterns = [
                '*.py', '*.js', '*.ts', '*.go', '*.java', '.env*', '*.conf'
            ]
            for pattern in code_patterns:
                for code_file in self.repo_path.glob(f'**/{pattern}'):
                    if any(x in str(code_file) for x in ['.git', 'node_modules', '.env']):
                        continue
                    connections = CodeAnalyzer.analyze_file(code_file, service_name)
                    self.connections.extend(connections)
                    self.services[service_name].connections.extend(connections)


class ArchitectureDocGenerator:
    """Generates architecture documentation in Markdown."""

    def __init__(self, services: Dict[str, Service], connections: List[ServiceConnection]):
        """Initialize documentation generator."""
        self.services = services
        self.connections = connections
        self.repos = {}  # Group services by repo

        for service in services.values():
            if service.repo_name not in self.repos:
                self.repos[service.repo_name] = []
            self.repos[service.repo_name].append(service)

    def generate(self) -> str:
        """Generate architecture documentation."""
        doc = []

        # Header
        doc.append("# Service Architecture Documentation\n")
        doc.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        doc.append("")

        # Table of contents
        doc.append("## Table of Contents\n")
        doc.append("1. [Service Overview](#service-overview)")
        doc.append("2. [Service Connections](#service-connections)")
        doc.append("3. [Repositories](#repositories)")
        doc.append("4. [Connection Matrix](#connection-matrix)")
        doc.append("")

        # Service Overview
        doc.append("## Service Overview\n")
        doc.append(f"Total Services: {len(self.services)}")
        doc.append(f"Total Repositories: {len(self.repos)}")
        doc.append(f"Total Connections: {len(self.connections)}\n")

        # Service list
        doc.append("### Services by Repository\n")
        for repo_name, services in sorted(self.repos.items()):
            doc.append(f"#### {repo_name}\n")
            for service in sorted(services, key=lambda s: s.name):
                doc.append(f"- **{service.name}**")
                if service.image:
                    doc.append(f"  - Image: `{service.image}`")
                if service.language:
                    doc.append(f"  - Language: {service.language}")
                if service.ports:
                    doc.append(f"  - Ports: {', '.join(map(str, service.ports))}")
            doc.append("")

        # Connections Overview
        doc.append("## Service Connections\n")
        if not self.connections:
            doc.append("No connections detected.\n")
        else:
            doc.append("### Connection Summary\n")
            conn_types = {}
            for conn in self.connections:
                conn_type = conn.connection_type
                conn_types[conn_type] = conn_types.get(conn_type, 0) + 1

            for conn_type, count in sorted(conn_types.items()):
                doc.append(f"- **{conn_type}**: {count} connections")
            doc.append("")

            # Detailed connections
            doc.append("### Detailed Connections\n")
            current_source = None
            for conn in sorted(self.connections, key=lambda c: (c.source_service, c.target_service)):
                if conn.source_service != current_source:
                    current_source = conn.source_service
                    doc.append(f"\n#### {conn.source_service}\n")

                target = conn.target_service
                conn_type = conn.connection_type
                doc.append(f"- **→ {target}** ({conn_type})")
                if conn.port:
                    doc.append(f"  - Port: {conn.port}")
                if conn.protocol:
                    doc.append(f"  - Protocol: {conn.protocol}")
                if conn.path:
                    doc.append(f"  - Found in: `{conn.path}`")
            doc.append("")

        # Repositories
        doc.append("## Repositories\n")
        for repo_name, services in sorted(self.repos.items()):
            doc.append(f"### {repo_name}\n")
            doc.append(f"Services: {len(services)}\n")
            doc.append(f"- {', '.join(sorted([s.name for s in services]))}\n")

        # Connection Matrix
        doc.append("## Connection Matrix\n")
        doc.append("```\n")
        all_services = sorted(set(s.name for s in self.services.values()))
        matrix = self._build_connection_matrix()

        # Header
        doc.append("       " + "  ".join(f"{s:8}" for s in all_services))
        doc.append("".join("-" * 80))

        # Rows
        for source in all_services:
            row = f"{source:6} "
            for target in all_services:
                key = (source, target)
                count = matrix.get(key, 0)
                if count > 0:
                    row += f"{count:8} "
                else:
                    row += "  -     "
            doc.append(row)

        doc.append("```\n")

        return "\n".join(doc)

    def _build_connection_matrix(self) -> Dict[Tuple[str, str], int]:
        """Build connection count matrix."""
        matrix = {}
        for conn in self.connections:
            key = (conn.source_service, conn.target_service)
            matrix[key] = matrix.get(key, 0) + 1
        return matrix


def load_config(config_file: Path) -> Dict:
    """Load configuration from YAML file."""
    with open(config_file, 'r') as f:
        return yaml.safe_load(f)


def create_default_config(config_file: Path):
    """Create a default configuration file."""
    default_config = {
        'gitlab': {
            'url': 'https://gitlab.example.com',
            'token': 'YOUR_GITLAB_TOKEN',
            'group_id': None,  # Optional: specific group ID to analyze
        },
        'output': {
            'markdown_file': 'architecture.md',
            'json_file': 'services.json',
        },
        'analysis': {
            'analyze_code': True,
            'analyze_configs': True,
            'code_patterns': ['*.py', '*.js', '*.ts', '*.go', '.env*'],
            'connection_types': [
                'http', 'grpc', 'database', 'message_queue',
                'dependency', 'environment', 'network'
            ],
        },
        'temp_directory': '/tmp/gitlab_analysis',
        'cleanup_after': True,
    }

    with open(config_file, 'w') as f:
        yaml.dump(default_config, f, default_flow_style=False)
    print(f"Created default configuration: {config_file}")
    print("Please update with your GitLab credentials and run again.")


def main():
    parser = argparse.ArgumentParser(
        description='Analyze GitLab service architecture and connections',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create default config
  python3 gitlab_service_analyzer.py --init-config config.yaml

  # Analyze with config
  python3 gitlab_service_analyzer.py --config config.yaml

  # Analyze specific group
  python3 gitlab_service_analyzer.py --config config.yaml --group-id 42
        """
    )

    parser.add_argument('--config', type=Path, default='config.yaml',
                        help='Configuration file (default: config.yaml)')
    parser.add_argument('--init-config', action='store_true',
                        help='Create default configuration file')
    parser.add_argument('--output', type=Path, help='Output markdown file')
    parser.add_argument('--group-id', help='GitLab group ID to analyze')
    parser.add_argument('--keep-repos', action='store_true',
                        help='Keep cloned repos instead of deleting')

    args = parser.parse_args()

    # Handle config initialization
    if args.init_config:
        create_default_config(args.config)
        return 0

    # Load configuration
    if not args.config.exists():
        print(f"Error: Config file not found: {args.config}")
        print(f"Run: python3 {sys.argv[0]} --init-config {args.config}")
        return 1

    config = load_config(args.config)

    # Validate config
    if not config.get('gitlab', {}).get('token') or config['gitlab']['token'] == 'YOUR_GITLAB_TOKEN':
        print("Error: GitLab token not configured")
        print(f"Edit {args.config} and set your GitLab token")
        return 1

    # Override config with CLI args
    if args.group_id:
        config['gitlab']['group_id'] = args.group_id
    if args.output:
        config['output']['markdown_file'] = str(args.output)

    print(f"\n=== GitLab Service Architecture Analyzer ===\n")
    print(f"GitLab: {config['gitlab']['url']}")
    print(f"Group: {config['gitlab'].get('group_id', 'All projects')}\n")

    # Initialize analyzers
    gl_analyzer = GitLabAnalyzer(
        config['gitlab']['url'],
        config['gitlab']['token'],
        config['gitlab'].get('group_id')
    )

    # Get projects
    print("Fetching projects...")
    projects = gl_analyzer.get_projects()
    if not projects:
        print("No projects found")
        return 1
    print(f"Found {len(projects)} project(s)\n")

    # Create temp directory
    temp_dir = Path(config.get('temp_directory', '/tmp/gitlab_analysis'))
    temp_dir.mkdir(parents=True, exist_ok=True)

    all_services = {}
    all_connections = []

    # Analyze each repository
    print("Analyzing repositories:")
    for project in projects:
        repo_path = gl_analyzer.clone_repo(project, temp_dir)
        if repo_path:
            analyzer = RepositoryAnalyzer(repo_path, project.name)
            services, connections = analyzer.analyze()
            all_services.update(services)
            all_connections.extend(connections)

    print(f"\nAnalysis complete:")
    print(f"  Services found: {len(all_services)}")
    print(f"  Connections detected: {len(all_connections)}\n")

    # Generate documentation
    print("Generating documentation...")
    doc_gen = ArchitectureDocGenerator(all_services, all_connections)
    markdown_doc = doc_gen.generate()

    # Write output
    output_file = Path(config['output']['markdown_file'])
    with open(output_file, 'w') as f:
        f.write(markdown_doc)
    print(f"✓ Markdown documentation: {output_file}")

    # Optional: Write JSON
    if 'json_file' in config['output']:
        services_json = {
            name: {
                'repo': svc.repo_name,
                'image': svc.image,
                'language': svc.language,
                'ports': svc.ports,
                'connections': len(svc.connections),
            }
            for name, svc in all_services.items()
        }
        json_file = Path(config['output']['json_file'])
        with open(json_file, 'w') as f:
            json.dump(services_json, f, indent=2)
        print(f"✓ JSON summary: {json_file}")

    # Cleanup
    if not args.keep_repos and config.get('cleanup_after', True):
        print(f"\nCleaning up temporary files...")
        import shutil
        shutil.rmtree(temp_dir)
        print("✓ Cleaned up")

    print(f"\nDone!")
    return 0


if __name__ == '__main__':
    sys.exit(main())
