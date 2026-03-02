from killswitch import KillSwitch
import time

# 1. URL of your remote JSON config file (e.g., GitHub Gist raw URL)
# The file should contain: {"status": "active", "message": "..."}
MY_CONTROL_LINK = "https://gist.githubusercontent.com/sayan9168/269e8a32c214ea9d3b1b998432034898/raw/0b1a904ecb33bf207ed83bab82279328bf99f379/status.json"

# 2. Initialize the KillSwitch
guardian = KillSwitch(
    config_url=MY_CONTROL_LINK, 
    developer_email="sm6881164@gmail.com"
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
  
