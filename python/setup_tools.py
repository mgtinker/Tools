#!/usr/bin/env python3
"""
Deployment and setup helper for tools in Rocky 8.10 WSL environment.

Handles:
- Python version verification
- Virtualenv setup
- Dependency installation
- Environment configuration
"""

import sys
import subprocess
import os
from pathlib import Path


def check_python_version(min_version=(3, 8)):
    """Verify Python version meets requirements."""
    if sys.version_info < min_version:
        print(f"Error: Python {min_version[0]}.{min_version[1]}+ required")
        print(f"Current: Python {sys.version_info.major}.{sys.version_info.minor}")
        return False
    return True


def check_command(cmd):
    """Check if command is available."""
    try:
        subprocess.run(['which', cmd], capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def run_command(cmd, description):
    """Run command and report status."""
    print(f"{description}...", end=' ', flush=True)
    try:
        subprocess.run(cmd, shell=True, check=True, capture_output=True)
        print("✓")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error: {e}")
        return False


def setup_venv(venv_path='venv'):
    """Setup Python virtual environment."""
    venv = Path(venv_path)
    if venv.exists():
        print(f"Virtual environment already exists: {venv}")
        return True

    print(f"Creating virtual environment: {venv}")
    if not run_command(f'{sys.executable} -m venv {venv}', "Creating venv"):
        return False

    return True


def install_requirements(requirements_file='requirements.txt', venv_path='venv'):
    """Install Python dependencies."""
    if not Path(requirements_file).exists():
        print(f"Warning: {requirements_file} not found")
        return False

    venv = Path(venv_path)
    if not venv.exists():
        print(f"Error: Virtual environment not found: {venv}")
        return False

    # Determine pip path
    if sys.platform == 'win32':
        pip_path = venv / 'Scripts' / 'pip.exe'
    else:
        pip_path = venv / 'bin' / 'pip'

    cmd = f'{pip_path} install -r {requirements_file}'
    return run_command(cmd, "Installing requirements")


def main():
    print("=== Python Tools Setup Helper ===\n")

    # Check Python
    if not check_python_version():
        return 1

    print(f"Python: {sys.version_info.major}.{sys.version_info.minor}")

    # Check required commands
    required = ['git']
    for cmd in required:
        if not check_command(cmd):
            print(f"Warning: {cmd} not found in PATH")

    # Create venv
    if not setup_venv():
        return 1

    # Install dependencies
    if not install_requirements():
        return 1

    print("\n=== Setup Complete ===")
    print("\nTo activate virtual environment:")
    print("  source venv/bin/activate  # Linux/WSL")
    print("  .\\venv\\Scripts\\activate.bat  # Windows CMD")
    print("  .\\venv\\Scripts\\Activate.ps1  # Windows PowerShell")

    return 0


if __name__ == '__main__':
    sys.exit(main())
