#!/usr/bin/env python3
"""
Simple startup script for the E-commerce Analytics Dashboard
"""

import os
import sys

def main():
    """Run the Flask application with proper configuration"""
    
    # Set environment variables
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_DEBUG'] = '1'
    
    # Check if required files exist
    required_files = [
        'dataset/customers.csv',
        'dataset/products.csv', 
        'dataset/transactions.csv'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("Error: Missing required data files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        print("\nPlease ensure all data files are in the dataset/ directory.")
        sys.exit(1)
    
    print("Starting E-commerce Analytics Dashboard...")
    print("Loading data files...")
    print("Initializing analytics modules...")
    print("Starting web server...")
    print()
    print("Dashboard will be available at: http://localhost:5000")
    print("Access from other devices: http://[your-ip]:5000")
    print()
    print("Press Ctrl+C to stop the server")
    print("-" * 60)
    
    # Import and run the Flask app
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5002)
    except KeyboardInterrupt:
        print("\nDashboard stopped. Thank you for using the Analytics Dashboard!")
    except Exception as e:
        print(f"Error starting the application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()