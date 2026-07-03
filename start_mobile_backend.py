import subprocess
import sys
import time

def install_and_run():
    print("Checking dependencies for Mobile API Tunnel...")
    try:
        import pyngrok
    except ImportError:
        print("Installing pyngrok...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyngrok"])

    from pyngrok import ngrok
    import uvicorn
    from threading import Thread
    from api import app

    def run_server():
        print("Starting local AI API on port 8000...")
        uvicorn.run(app, host="0.0.0.0", port=8000)

    # Start FastAPI in a background thread
    server_thread = Thread(target=run_server, daemon=True)
    server_thread.start()

    time.sleep(3) # Wait for server to boot

    print("\n" + "="*50)
    print("STARTING FLUTTERFLOW TUNNEL (LocalTunnel)")
    print("="*50)
    
    print("\nStarting LocalTunnel to expose port 8000...")
    print("Leave this window open!")
    print("="*50)
    
    try:
        # Use localtunnel via npx instead of ngrok (no auth required)
        subprocess.run(["npx", "localtunnel", "--port", "8000", "--subdomain", "whole-moments-make"], check=True, shell=True)
    except KeyboardInterrupt:
        print("\nShutting down tunnel...")

if __name__ == "__main__":
    install_and_run()
