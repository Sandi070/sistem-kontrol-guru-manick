#!/usr/bin/env python3
import os
import subprocess
import sys
import time

def main():
    print("=== Railway Deployment Debug ===")
    
    # Print environment info
    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    print(f"PORT environment: {os.environ.get('PORT', 'NOT SET')}")
    print(f"DATABASE_URL: {'SET' if os.environ.get('DATABASE_URL') else 'NOT SET'}")
    
    # Get port from environment or use default
    port = os.environ.get('PORT', '8000')
    
    # Validate port
    try:
        port_int = int(port)
        if port_int < 1 or port_int > 65535:
            raise ValueError("Port out of range")
    except ValueError:
        print(f"Invalid port: {port}, using default 8000")
        port = '8000'
    
    print(f"Using port: {port}")
    
    # Test if app.py can be imported
    try:
        print("Testing app import...")
        import app
        print("✅ App imported successfully")
    except Exception as e:
        print(f"❌ Error importing app: {e}")
        sys.exit(1)
    
    # Build gunicorn command
    cmd = [
        'gunicorn',
        'app:app',
        '--bind', f'0.0.0.0:{port}',
        '--workers', '1',
        '--timeout', '120',
        '--access-logfile', '-',
        '--error-logfile', '-',
        '--log-level', 'debug'
    ]
    
    print(f"Starting application on port {port}")
    print(f"Command: {' '.join(cmd)}")
    
    # Give some time for database to be ready
    if os.environ.get('DATABASE_URL'):
        print("Waiting 5 seconds for database...")
        time.sleep(5)
    
    # Run gunicorn
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting application: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("Application stopped by user")
        sys.exit(0)

if __name__ == '__main__':
    main()