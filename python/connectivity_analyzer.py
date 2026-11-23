"""
Service connectivity analyzer for Docker/Kubernetes environments.

Analyzes configuration files and code to understand service-to-service connections.
"""

import re
from typing import Dict, List, Set, Tuple
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class ServiceConnection:
    """Represents a connection between services."""
    source_service: str
    target_service: str
    connection_type: str  # 'http', 'grpc', 'database', 'message_queue', 'env_var', etc.
    protocol: str = ''
    port: str = ''
    path: str = ''  # file path where connection was found
    context: str = ''  # context snippet from the file


@dataclass
class Service:
    """Represents a service/container."""
    name: str
    repo_name: str
    image: str = ''
    ports: List[str] = field(default_factory=list)
    environment: Dict[str, str] = field(default_factory=dict)
    volumes: List[str] = field(default_factory=list)
    connections: List[ServiceConnection] = field(default_factory=list)
    language: str = ''
    root_path: Path = None


class DockerComposeAnalyzer:
    """Analyzes docker-compose files."""

    @staticmethod
    def analyze(content: str, service_name: str, repo_name: str) -> List[ServiceConnection]:
        """Extract service connections from docker-compose.yml content."""
        connections = []

        # Parse environment variables for service references
        env_pattern = r'(?:^|[\s])([A-Z_]+)(?:_HOST|_URL|_ADDR)=\s*([^\s\n]+)'
        for match in re.finditer(env_pattern, content, re.MULTILINE):
            env_var, url = match.groups()
            # Try to extract service name from URL
            service_ref = extract_hostname(url)
            if service_ref and service_ref != service_name:
                connections.append(ServiceConnection(
                    source_service=service_name,
                    target_service=service_ref,
                    connection_type='environment',
                    path='docker-compose.yml',
                    context=url
                ))

        # Find depends_on references
        depends_pattern = r'depends_on:\s*((?:[^\n]*\n)*?)\n(?=\S|\Z)'
        for match in re.finditer(depends_pattern, content):
            deps_block = match.group(1)
            service_refs = re.findall(r'-\s*(\w+)', deps_block)
            for ref in service_refs:
                if ref != service_name:
                    connections.append(ServiceConnection(
                        source_service=service_name,
                        target_service=ref,
                        connection_type='dependency',
                        path='docker-compose.yml',
                        context='depends_on'
                    ))

        # Find network references
        network_pattern = r'(?:links|networks):\s*((?:[^\n]*\n)*?)\n(?=\S|\Z)'
        for match in re.finditer(network_pattern, content):
            block = match.group(1)
            services = re.findall(r'-\s*(\w+)', block)
            for svc in services:
                if svc != service_name:
                    connections.append(ServiceConnection(
                        source_service=service_name,
                        target_service=svc,
                        connection_type='network',
                        path='docker-compose.yml',
                        context='links/networks'
                    ))

        return connections


class DockerfileAnalyzer:
    """Analyzes Dockerfile for service information."""

    @staticmethod
    def analyze(content: str, service_name: str) -> Dict[str, str]:
        """Extract metadata from Dockerfile."""
        metadata = {
            'base_image': '',
            'language': '',
            'exposed_ports': []
        }

        # Find FROM line
        from_match = re.search(r'^FROM\s+(\S+)', content, re.MULTILINE)
        if from_match:
            base_image = from_match.group(1)
            metadata['base_image'] = base_image
            # Guess language from base image
            if 'python' in base_image:
                metadata['language'] = 'python'
            elif 'node' in base_image or 'npm' in base_image:
                metadata['language'] = 'javascript'
            elif 'java' in base_image:
                metadata['language'] = 'java'
            elif 'go' in base_image:
                metadata['language'] = 'go'

        # Find exposed ports
        expose_pattern = r'^EXPOSE\s+(\d+)'
        for match in re.finditer(expose_pattern, content, re.MULTILINE):
            metadata['exposed_ports'].append(match.group(1))

        return metadata


class KubernetesAnalyzer:
    """Analyzes Kubernetes manifests for service connections."""

    @staticmethod
    def analyze(content: str, service_name: str) -> List[ServiceConnection]:
        """Extract connections from K8s manifests."""
        connections = []

        # Find environment variables
        env_pattern = r'name:\s*([A-Z_]+).*?value:\s*["\']?([^\s\n"\']+)'
        for match in re.finditer(env_pattern, content, re.DOTALL):
            env_name, env_value = match.groups()
            if any(x in env_name for x in ['HOST', 'URL', 'ADDR', 'SERVER']):
                target = extract_hostname(env_value)
                if target and target != service_name:
                    connections.append(ServiceConnection(
                        source_service=service_name,
                        target_service=target,
                        connection_type='k8s_env',
                        context=env_value,
                        path='kubernetes manifest'
                    ))

        return connections


class CodeAnalyzer:
    """Analyzes application code for service connections."""

    # HTTP client patterns
    HTTP_PATTERNS = [
        r'(?:requests|httpx|urllib)\.(?:get|post|put|delete)\s*\(\s*["\']([^"\']+)',
        r'http(?:s)?://(?:\$|{)?(?:process\.env\.)?([A-Z_]+)(?:})?(?:[/:\)])',
        r'(?:scheme|base_url|api_url)\s*[:=]\s*["\']([^"\']+)',
        r'(?:HOST|URL|ADDR)\s*=\s*["\']?([^\s\n"\']+)',
    ]

    DATABASE_PATTERNS = [
        r'(?:postgres|mysql|mongodb|redis)://(?:.*@)?([^\s/:]+)',
        r'["\']?(?:DB_HOST|REDIS_HOST|DB_URL)["\']?\s*[:=]\s*["\']?([^\s\n"\']+)',
    ]

    MESSAGE_QUEUE_PATTERNS = [
        r'(?:rabbitmq|kafka|amqp)://(?:.*@)?([^\s/:]+)',
        r'["\']?(?:MQ_HOST|KAFKA_HOST|AMQP_HOST)["\']?\s*[:=]\s*["\']?([^\s\n"\']+)',
    ]

    @classmethod
    def analyze_file(cls, file_path: Path, service_name: str) -> List[ServiceConnection]:
        """Analyze a single code file."""
        connections = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception:
            return connections

        # Check HTTP connections
        for pattern in cls.HTTP_PATTERNS:
            for match in re.finditer(pattern, content):
                url = match.group(1)
                target = extract_hostname(url)
                if target and target != service_name:
                    connections.append(ServiceConnection(
                        source_service=service_name,
                        target_service=target,
                        connection_type='http',
                        path=str(file_path),
                        context=url
                    ))

        # Check database connections
        for pattern in cls.DATABASE_PATTERNS:
            for match in re.finditer(pattern, content):
                target = match.group(1)
                if target and target != 'localhost' and len(target) > 2:
                    conn_type = 'database'
                    if 'postgres' in content[max(0, match.start()-20):match.end()]:
                        conn_type = 'postgresql'
                    elif 'mysql' in content[max(0, match.start()-20):match.end()]:
                        conn_type = 'mysql'
                    connections.append(ServiceConnection(
                        source_service=service_name,
                        target_service=target,
                        connection_type=conn_type,
                        path=str(file_path),
                        context=match.group(0)
                    ))

        # Check message queues
        for pattern in cls.MESSAGE_QUEUE_PATTERNS:
            for match in re.finditer(pattern, content):
                target = match.group(1)
                if target and target != 'localhost' and len(target) > 2:
                    connections.append(ServiceConnection(
                        source_service=service_name,
                        target_service=target,
                        connection_type='message_queue',
                        path=str(file_path),
                        context=match.group(0)
                    ))

        return connections


def extract_hostname(url: str) -> str:
    """Extract hostname from URL, env variable reference, or service name."""
    if not url:
        return ''

    url = url.strip('\'"')

    # Handle env var references
    env_match = re.search(r'\$\{?([A-Z_]+)\}?', url)
    if env_match:
        return env_match.group(1)

    # Extract hostname from full URL
    if '://' in url:
        url = url.split('://', 1)[1]
    if '/' in url:
        url = url.split('/', 1)[0]
    if ':' in url:
        url = url.split(':', 1)[0]
    if '@' in url:
        url = url.split('@', 1)[1]

    # Return if it looks like a hostname/service name
    url = url.strip()
    if url and url not in ('localhost', '127.0.0.1', '0.0.0.0', 'db', 'cache'):
        return url

    return ''
