#!/bin/sh
# Install Elixir in WSL
set -e

echo "Installing Erlang and Elixir in WSL..."

# Update package list
sudo apt-get update

# Install Erlang and Elixir
sudo apt-get install -y erlang elixir

# Verify installation
echo ""
echo "Installed versions:"
elixir --version
echo ""
echo "Elixir installed successfully!"
