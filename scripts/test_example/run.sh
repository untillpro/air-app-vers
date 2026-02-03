#!/usr/bin/env bash
# Script to run validation on the test_example
# This demonstrates how to use validate.py with example data

set -Eeuo pipefail

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Get the scripts directory (from test_example to scripts)
SCRIPTS_DIR="$(cd "$SCRIPT_DIR/../../scripts" && pwd)"

# Change to the example directory
cd "$SCRIPT_DIR"

echo "Running validation on test_example..."
echo "Working directory: $(pwd)"
echo ""

# Run the validation script
python "$SCRIPTS_DIR/validate.py"

