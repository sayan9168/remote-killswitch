from killswitch import KillSwitch
import time

# 1. URL of your remote JSON config file (e.g., GitHub Gist raw URL)
# The file should contain: {"status": "active", "message": "..."}
MY_CONTROL_LINK = "https://gist.githubusercontent.com/sayan9168/YOUR_GIST_ID/raw/status.json"

# 2. Initialize the KillSwitch
guardian = KillSwitch(
    config_url=MY_CONTROL_LINK, 
    developer_email="sayan@example.com"
)

def main():
    print("Initializing application...")
    
    # 3. Check status immediately upon startup
    guardian.check_status()
    
    print("Application is running successfully...")
    
    # Simulate work
    for i in range(5):
        print(f"Doing work... {i+1}")
        time.sleep(1)
    
    print("Work finished.")

if __name__ == "__main__":
    main()
  
