#!/bin/bash

# Uninstall all existing packages
pip freeze | cut -d "@" -f1 | xargs pip uninstall -y --no-input --break-system-packages

# Upgrade pip and install pipreqs
pip install --upgrade pip
pip install pipreqs --break-system-packages

# Generate requirements.txt
pipreqs . --force

# Install the new requirements
pip install -r requirements.txt --no-cache-dir --no-input --break-system-packages

echo "Deployment completed successfully."