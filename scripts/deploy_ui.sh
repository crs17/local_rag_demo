#!/bin/bash
set -e  # Exit on error

# Check if chat-ui directory already exists
if [ -d "chat-ui" ]; then
    echo "chat-ui directory already exists. Skipping creation."
    cd chat-ui
else
    echo "Creating chat-ui application..."
    # Use -Y to skip all prompts and use defaults
    # --package-manager pnpm to use pnpm (default is yarn)
    # --install-deps true to auto-install (this is the default, but explicit is clearer)
    npx create-agent-chat-app@latest -Y --project-name chat-ui --package-manager pnpm
    cd chat-ui
    echo "Installing dependencies..."
    # Install
    pnpm install

fi

