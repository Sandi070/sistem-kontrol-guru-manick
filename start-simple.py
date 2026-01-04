#!/usr/bin/env python3
import os
import sys

def main():
    print("=== Simple Flask Start ===")
    
    # Print environment info
    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    print(f"PORT environment: {os.environ.get('PORT', 'NOT SET')}")
    print(f"DATABASE_URL: {'SET' if os.environ.get('DATABASE_URL') else 'NOT SET'}")
    
    # Get port
    port = int(os.environ.get('PORT', 8000))
    print(f"Using port: {port}")
    
    # Import and run Flask app directly
    try:
        print("Importing app...")
        from app import app
        print("✅ App imported successfully")
        
        print(f"Starting Flask development server on 0.0.0.0:{port}")
        app.run(host='0.0.0.0', port=port, debug=False)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()