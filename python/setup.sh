#!/usr/bin/env bash
# Quick start script for GitLab service analyzer on Rocky 8.10 WSL

set -e

echo "=== GitLab Service Analyzer - Rocky 8.10 Setup ==="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Installing Python 3..."
    sudo dnf install -y python3 python3-devel 2>/dev/null
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✓ Python $PYTHON_VERSION"

# Check git
if ! command -v git &> /dev/null; then
    echo "Installing git..."
    sudo dnf install -y git 2>/dev/null
fi
echo "✓ Git installed"

# Check requirements file exists
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REQUIREMENTS_FILE="$SCRIPT_DIR/requirements.txt"

if [ ! -f "$REQUIREMENTS_FILE" ]; then
    echo "Error: requirements.txt not found in $SCRIPT_DIR"
    exit 1
fi

# Check dependencies
echo ""
echo "Checking Python dependencies..."
python3 "$SCRIPT_DIR/check_dependencies.py" || {
    echo ""
    echo "Installing missing dependencies..."
    python3 "$SCRIPT_DIR/check_dependencies.py" --auto-install || {
        echo "Warning: Some dependencies failed to install."
        echo "Try manually: python3 -m pip install -r $REQUIREMENTS_FILE"
    }
}

# Create config if needed
CONFIG_FILE="${1:-config.yaml}"
if [ ! -f "$CONFIG_FILE" ]; then
    echo ""
    echo "Creating configuration file: $CONFIG_FILE"
    python3 "$SCRIPT_DIR/gitlab_service_analyzer.py" --init-config --config "$CONFIG_FILE"
    
    echo ""
    echo "⚠️  IMPORTANT: Edit $CONFIG_FILE and add your GitLab token:"
    echo "   1. Go to: https://your-gitlab.com/-/user_settings/personal_access_tokens"
    echo "   2. Create token with 'api', 'read_api', 'read_repository' scopes"
    echo "   3. Copy token value into $CONFIG_FILE"
    echo "   4. Run: python3 gitlab_service_analyzer.py --config $CONFIG_FILE"
    exit 0
fi

# Config exists, ready to run
echo ""
echo "=== Setup Complete ==="
echo ""
echo "To analyze your services:"
echo "  python3 gitlab_service_analyzer.py --config $CONFIG_FILE"
echo ""
echo "For more options:"
echo "  python3 gitlab_service_analyzer.py --help"
