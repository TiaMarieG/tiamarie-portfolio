#!/bin/bash

# Exit on any error
set -e

# Configurable variables
PROJECT_DIR="$HOME/tiamarie-portfolio"
VENV_DIR="$PROJECT_DIR/python3-virtualenv"
TMUX_SESSION_NAME="flask-server"

echo "==> Killing any running tmux sessions..."
tmux kill-server || true

echo "==> Entering project directory..."
cd "$PROJECT_DIR"

echo "==> Fetching and resetting latest changes from GitHub..."
git fetch
git reset origin/main --hard

echo "==> Activating virtualenv and installing dependencies..."
source "$VENV_DIR/bin/activate"
pip install -r requirements.txt
deactivate

echo "==> Launching Flask in a detached tmux session..."
tmux new-session -d -s "$TMUX_SESSION_NAME" bash -c "
cd \"$PROJECT_DIR\"
source \"$VENV_DIR/bin/activate\"
flask run --host=0.0.0.0 --port=5000
"

echo "==> ✅ Site deployed and running in tmux session '$TMUX_SESSION_NAME'."
