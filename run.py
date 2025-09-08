

#!/usr/bin/env python3
"""
Main entry point for the Mood Movie Recommender application.
This script provides a convenient way to run the application with proper configuration.
"""

import uvicorn
import os
from dotenv import load_dotenv

def main():
    """Main function to run the application"""
    
    # Load environment variables
    load_dotenv()
    
    # Get configuration from environment variables
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    
    print("🎬 Starting Mood Movie Recommender...")
    print(f"📍 Server will be available at: http://{host}:{port}")
    print(f"📚 API Documentation: http://{host}:{port}/docs")
    print(f"🔧 Debug mode: {'ON' if debug else 'OFF'}")
    print("=" * 50)
    
    # Run the application
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info" if not debug else "debug"
    )

if __name__ == "__main__":
    main()



