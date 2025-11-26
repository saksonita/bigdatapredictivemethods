#!/usr/bin/env python
"""
NumPy Compatibility Fix Script for NeuralProphet
This script fixes the "np.NaN was removed in NumPy 2.0" error
"""

import subprocess
import sys
import os

def run_command(command, description=""):
    """Run a shell command and return the result"""
    if description:
        print(f"\n{description}")

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return False

def check_numpy_version():
    """Check current NumPy version"""
    try:
        import numpy
        return numpy.__version__
    except ImportError:
        return None

def check_neuralprophet():
    """Check if NeuralProphet is available"""
    try:
        import neuralprophet
        return True
    except ImportError:
        return False

def main():
    print("=" * 50)
    print("NumPy Compatibility Fix Script")
    print("=" * 50)
    print()

    # Check current NumPy version
    current_numpy = check_numpy_version()
    if current_numpy:
        print(f"Current NumPy version: {current_numpy}")
        if current_numpy.startswith("2."):
            print("⚠ NumPy 2.0+ detected - needs downgrade")
        else:
            print("✓ NumPy version is compatible")
    else:
        print("NumPy not installed")

    print()
    print("Checking Python environment...")
    print(f"Python: {sys.executable}")
    print(f"Python version: {sys.version.split()[0]}")
    print()

    # Ask user for confirmation
    response = input("Do you want to fix the NumPy compatibility issue? (yes/no): ").lower()
    if response not in ['yes', 'y']:
        print("Aborted by user.")
        return

    print("\n" + "=" * 50)
    print("Starting fix process...")
    print("=" * 50)

    # Step 1: Uninstall current NumPy
    print("\n[1/4] Uninstalling current NumPy version...")
    run_command(f"{sys.executable} -m pip uninstall numpy -y", "Removing NumPy...")

    # Step 2: Install compatible NumPy
    print("\n[2/4] Installing compatible NumPy version (<2.0)...")
    success = run_command(
        f"{sys.executable} -m pip install 'numpy<2.0,>=1.24.0'",
        "Installing NumPy 1.x..."
    )

    if not success:
        print("\n❌ Failed to install NumPy. Please try manually:")
        print(f"   {sys.executable} -m pip install 'numpy<2.0,>=1.24.0'")
        return

    # Step 3: Verify NumPy installation
    print("\n[3/4] Verifying NumPy installation...")
    new_numpy = check_numpy_version()
    if new_numpy:
        print(f"✓ NumPy version: {new_numpy}")
        if new_numpy.startswith("2."):
            print("⚠ Warning: NumPy 2.0+ is still installed. The fix may not work.")
        else:
            print("✓ NumPy version is now compatible!")
    else:
        print("❌ NumPy verification failed")
        return

    # Step 4: Verify NeuralProphet
    print("\n[4/4] Verifying NeuralProphet...")
    if check_neuralprophet():
        print("✓ NeuralProphet imported successfully!")
    else:
        print("⚠ NeuralProphet not found. Installing...")
        run_command(f"{sys.executable} -m pip install neuralprophet", "Installing NeuralProphet...")
        if check_neuralprophet():
            print("✓ NeuralProphet installed successfully!")
        else:
            print("❌ Failed to install NeuralProphet")

    # Final summary
    print("\n" + "=" * 50)
    print("Fix completed!")
    print("=" * 50)
    print("\nYou can now run your notebook cells again.")
    print("If you still encounter errors, see NUMPY_FIX.md for more options.")
    print()

    # Test script
    print("Running quick compatibility test...")
    try:
        import numpy as np
        from neuralprophet import NeuralProphet

        print(f"✓ NumPy {np.__version__} - OK")
        print(f"✓ NeuralProphet - OK")
        print(f"✓ np.nan works: {np.nan}")
        print("\n✓ All compatibility tests passed!")
    except Exception as e:
        print(f"\n⚠ Compatibility test failed: {e}")
        print("Please check NUMPY_FIX.md for troubleshooting steps.")

if __name__ == "__main__":
    main()
