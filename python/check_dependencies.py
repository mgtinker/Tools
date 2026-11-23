#!/usr/bin/env python3
"""
Verify and install Python dependencies for tools.

Usage:
    python3 check_dependencies.py [--auto-install] [--requirements FILE]

Options:
    --auto-install      Automatically install missing packages
    --requirements FILE  Path to requirements file (default: requirements.txt)
"""

import sys
import subprocess
import importlib.util
from pathlib import Path
import argparse


def parse_requirements(req_file):
    """Parse requirements.txt format."""
    requirements = {}
    try:
        with open(req_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                # Handle version specifiers (>=, ==, <=, ~=, etc.)
                for op in ['>=', '<=', '==', '!=', '~=', '>', '<']:
                    if op in line:
                        pkg, version = line.split(op, 1)
                        requirements[pkg.strip()] = (op + version.strip(), line)
                        break
                else:
                    requirements[line] = (None, line)
    except FileNotFoundError:
        print(f"Error: Requirements file '{req_file}' not found")
        return None
    return requirements


def check_package_installed(package_name):
    """Check if a package is installed."""
    # Handle package names with hyphens/underscores
    import_name = package_name.replace('-', '_')
    spec = importlib.util.find_spec(import_name)
    return spec is not None


def install_package(package_spec):
    """Install a package using pip."""
    try:
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'install', '--quiet', package_spec],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True
    except subprocess.CalledProcessError:
        return False


def main():
    parser = argparse.ArgumentParser(description='Verify Python dependencies')
    parser.add_argument('--auto-install', action='store_true',
                        help='Automatically install missing packages')
    parser.add_argument('--requirements', default='requirements.txt',
                        help='Path to requirements file')
    args = parser.parse_args()

    req_file = Path(args.requirements)
    if not req_file.exists():
        # Try relative to this script
        script_dir = Path(__file__).parent
        req_file = script_dir / args.requirements

    requirements = parse_requirements(str(req_file))
    if requirements is None:
        return 1

    print(f"Checking dependencies from {req_file}...\n")

    missing = []
    installed = []

    for package, (version_spec, full_spec) in requirements.items():
        if check_package_installed(package):
            installed.append(package)
            print(f"✓ {package}")
        else:
            missing.append((package, full_spec))
            print(f"✗ {package} - NOT INSTALLED")

    print(f"\n--- Summary ---")
    print(f"Installed: {len(installed)}")
    print(f"Missing: {len(missing)}")

    if missing:
        if args.auto_install:
            print(f"\nInstalling {len(missing)} missing package(s)...")
            failed = []
            for package, spec in missing:
                print(f"  Installing {package}...", end=' ')
                if install_package(spec):
                    print("✓")
                else:
                    print("✗ FAILED")
                    failed.append(package)

            if failed:
                print(f"\nFailed to install: {', '.join(failed)}")
                print("Try running manually:")
                print(f"  python3 -m pip install {' '.join([spec for _, spec in [m for m in missing if m[0] in failed]])}")
                return 1
            else:
                print("\nAll dependencies installed successfully!")
                return 0
        else:
            print("\nTo install missing dependencies, run:")
            print(f"  python3 {Path(__file__).name} --auto-install")
            print("\nOr manually:")
            print(f"  python3 -m pip install {' '.join([spec for _, spec in missing])}")
            return 1

    print("\nAll dependencies satisfied!")
    return 0


if __name__ == '__main__':
    sys.exit(main())
