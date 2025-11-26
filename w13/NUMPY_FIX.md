# NumPy Compatibility Fix for NeuralProphet

## Problem
The error `AttributeError: 'np.NaN' was removed in the NumPy 2.0 release` occurs because NeuralProphet is not yet fully compatible with NumPy 2.0.

## Root Cause
- NumPy 2.0 removed `np.NaN` in favor of `np.nan`
- NeuralProphet library still uses the deprecated `np.NaN`
- This causes the prediction method to fail

## Solution
Downgrade NumPy to a version < 2.0 while maintaining compatibility with other packages.

## Steps to Fix

### Option 1: Using pip (Recommended for conda environment)

1. **Activate your neuralprophet conda environment:**
   ```bash
   conda activate neuralprophet
   ```

2. **Uninstall the current NumPy version:**
   ```bash
   pip uninstall numpy -y
   ```

3. **Install a compatible NumPy version:**
   ```bash
   pip install "numpy<2.0,>=1.24.0"
   ```

4. **Verify the installation:**
   ```bash
   python -c "import numpy; print(f'NumPy version: {numpy.__version__}')"
   ```

5. **Reinstall or update NeuralProphet (optional, but recommended):**
   ```bash
   pip install --upgrade neuralprophet
   ```

### Option 2: Using requirements.txt

1. **Activate your neuralprophet conda environment:**
   ```bash
   conda activate neuralprophet
   ```

2. **Install from requirements.txt:**
   ```bash
   pip install -r requirements.txt --force-reinstall numpy
   ```

### Option 3: Using conda

1. **Install NumPy 1.26.x using conda:**
   ```bash
   conda activate neuralprophet
   conda install numpy=1.26.4 -y
   ```

## Verification

After applying the fix, run this test in Python:

```python
import numpy as np
from neuralprophet import NeuralProphet

print(f"NumPy version: {np.__version__}")
print(f"NeuralProphet imported successfully!")

# Test if np.nan works (should work)
test_value = np.nan
print(f"np.nan works: {test_value}")
```

## Expected Result
- NumPy version should be < 2.0 (e.g., 1.26.4 or 1.24.3)
- NeuralProphet should import without errors
- Your model.predict() calls should work correctly

## Updated requirements.txt
The `requirements.txt` file has been updated to include:
```
numpy<2.0,>=1.24.0
neuralprophet>=0.7.0
```

## Additional Notes
- This is a temporary fix until NeuralProphet releases a version fully compatible with NumPy 2.0
- Monitor the [NeuralProphet GitHub repository](https://github.com/ourownstory/neural_prophet) for updates
- Once NeuralProphet is updated to support NumPy 2.0, you can upgrade both packages

## Alternative: Wait for NeuralProphet Update
If you prefer to wait for an official fix:
- Check for NeuralProphet updates: `pip install --upgrade neuralprophet`
- The NeuralProphet team is aware of NumPy 2.0 compatibility issues
- A fix may be available in newer versions

## Troubleshooting

### If you still get errors after downgrading:
1. Completely remove and reinstall:
   ```bash
   pip uninstall numpy neuralprophet pytorch-lightning torch -y
   pip install "numpy<2.0" neuralprophet
   ```

### If other packages conflict:
- Some packages may require NumPy 2.0. In this case, create a separate conda environment:
  ```bash
  conda create -n neuralprophet_env python=3.10 "numpy<2.0" pandas matplotlib scikit-learn
  conda activate neuralprophet_env
  pip install neuralprophet
  ```

## References
- [NumPy 2.0 Migration Guide](https://numpy.org/devdocs/numpy_2_0_migration_guide.html)
- [NeuralProphet GitHub Issues](https://github.com/ourownstory/neural_prophet/issues)
