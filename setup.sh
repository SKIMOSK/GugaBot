#!/usr/bin/env bash
# GugaBot — quick setup script (Linux / macOS)
set -e

echo "=== GugaBot Setup ==="

# Create virtual environment if not present
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment…"
    python3 -m venv .venv
fi

source .venv/bin/activate
echo "Installing Python dependencies…"
pip install --upgrade pip -q
pip install -r requirements.txt

# Linux-specific audio fix
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo ""
    echo "Linux detected. If pyaudio fails to install, run:"
    echo "  sudo apt install python3-pyaudio portaudio19-dev"
    echo "  sudo apt install python3-xlib scrot  # for screenshot/PC control"
fi

echo ""
echo "=== Setup complete! ==="
echo "Run the app with:"
echo "  source .venv/bin/activate && python main.py"
