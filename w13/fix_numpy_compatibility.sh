#!/bin/bash

# NumPy Compatibility Fix Script for NeuralProphet
# This script fixes the "np.NaN was removed in NumPy 2.0" error

echo "=================================="
echo "NumPy Compatibility Fix Script"
echo "=================================="
echo ""

# Check if conda is available
if command -v conda &> /dev/null; then
    echo "✓ Conda detected"

    # Check if neuralprophet environment exists
    if conda env list | grep -q "neuralprophet"; then
        echo "✓ neuralprophet environment found"
        echo ""
        echo "Activating neuralprophet environment..."

        # Note: In a script, we need to source conda
        eval "$(conda shell.bash hook)"
        conda activate neuralprophet

        echo "Current Python: $(which python)"
        echo "Current NumPy version: $(python -c 'import numpy; print(numpy.__version__)' 2>/dev/null || echo 'not installed')"
        echo ""

        echo "Fixing NumPy compatibility..."
        pip uninstall numpy -y
        pip install "numpy<2.0,>=1.24.0"

        echo ""
        echo "Verifying installation..."
        python -c "import numpy; print(f'✓ NumPy version: {numpy.__version__}')"

        echo ""
        echo "Testing NeuralProphet import..."
        python -c "from neuralprophet import NeuralProphet; print('✓ NeuralProphet imported successfully!')"

        echo ""
        echo "=================================="
        echo "✓ Fix completed successfully!"
        echo "=================================="
        echo ""
        echo "You can now run your notebook cells again."

    else
        echo "⚠ neuralprophet environment not found"
        echo ""
        echo "Available environments:"
        conda env list
        echo ""
        echo "Please activate the correct environment and run:"
        echo "  pip uninstall numpy -y"
        echo "  pip install 'numpy<2.0,>=1.24.0'"
    fi
else
    echo "⚠ Conda not found. Using system Python."
    echo ""
    echo "Installing compatible NumPy version..."
    pip uninstall numpy -y
    pip install "numpy<2.0,>=1.24.0"

    echo ""
    echo "Verifying installation..."
    python -c "import numpy; print(f'NumPy version: {numpy.__version__}')"

    echo ""
    echo "=================================="
    echo "Fix completed!"
    echo "=================================="
fi

echo ""
echo "For manual installation, see NUMPY_FIX.md for detailed instructions."
