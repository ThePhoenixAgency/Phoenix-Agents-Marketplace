#!/bin/bash
# Command: extract-function
# Created: 2026-02-18
set -euo pipefail
echo "=== Extract Function Helper ==="
echo ""
echo "Usage: Select the code to extract, then:"
echo ""
echo "1. Identify the inputs (variables used from outer scope)"
echo "2. Identify the outputs (what the extracted code returns)"
echo "3. Create the function with inputs as parameters"
echo "4. Replace the original code with the function call"
echo "5. Run tests to verify behavior is preserved"
echo ""
echo "Checklist:"
echo "  - [ ] Function has a descriptive name"
echo "  - [ ] Parameters are minimal"
echo "  - [ ] Return type is clear"
echo "  - [ ] Tests still pass"
