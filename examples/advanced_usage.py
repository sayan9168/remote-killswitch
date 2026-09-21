from killswitch import KillSwitch
import time
import json

# ============================================================================
# ADVANCED USAGE EXAMPLE - Remote KillSwitch with Enhanced Features
# ============================================================================

# 1. URL of your remote JSON config file (e.g., GitHub Gist raw URL)
MY_CONTROL_LINK = "https://gist.githubusercontent.com/sayan9168/269e8a32c214ea9d3b1b998432034898/raw/0b1a904ecb33bf207ed83bab82279328bf99f379/status.json"

# 2. Define a callback function for graceful shutdown
def on_shutdown_callback(reason: str):
    """Called before the application shuts down."""
    print(f"\n[*] Preparing for shutdown...")
    print(f"[*] Reason: {reason}")
    # Save state, close connections, cleanup resources, etc.
    # Example: save_user_data(), close_database(), etc.

# 3. Initialize the advanced KillSwitch with enhanced security features
guardian = KillSwitch(
    config_url=MY_CONTROL_LINK,
    developer_email="sm6881164@gmail.com",
    
    # Advanced Features:
    app_id="my-app-001",                    # Unique identifier for this instance
    allowed_versions=["1.0.0", "1.1.0"],   # Version control
    expiry_date="2026-12-31",              # License expiry date (YYYY-MM-DD)
    max_failures=3,                        # Max connection failures before shutdown
    callback=on_shutdown_callback,         # Graceful shutdown callback
    require_https=True,                    # Enforce HTTPS for security
    cache_duration=300                     # Cache status for 5 minutes
)

def main():
    print("="*60)
    print("REMOTE KILLSWITCH - ADVANCED DEMO")
    print("="*60)
    
    # Get current app version
    APP_VERSION = "1.0.0"
    
    # Check status with version validation
    print("\n[1] Performing initial security check...")
    guardian.check_status(current_version=APP_VERSION)
    
    print("[✓] Application is authorized to run!")
    
    # Simulate application work with periodic checks
    print("\n[2] Starting application loop with periodic checks...")
    
    for i in range(10):
        # Do some work
        print(f"   Working... iteration {i+1}/10")
        time.sleep(1)
        
        # Periodic status check every 3 iterations
        if (i + 1) % 3 == 0:
            print(f"   [Checking status at iteration {i+1}...]")
            guardian.check_status()
    
    # Demo: Feature flags
    print("\n[3] Checking feature flags...")
    premium_feature = guardian.get_feature_flag("premium_feature", default=False)
    beta_feature = guardian.get_feature_flag("beta_feature", default=False)
    
    print(f"   Premium Feature Enabled: {premium_feature}")
    print(f"   Beta Feature Enabled: {beta_feature}")
    
    if premium_feature:
        print("   → Unlocking premium content...")
    else:
        print("   → Premium content locked.")
    
    # Demo: Usage reporting
    print("\n[4] Reporting usage statistics...")
    usage_data = {
        "session_duration": 30,  # seconds
        "actions_performed": 10,
        "features_used": ["core", "advanced"],
        "user_type": "demo"
    }
    guardian.report_usage(usage_data)
    print("   ✓ Usage data queued for reporting")
    
    print("\n[5] Application completed successfully!")
    print("="*60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] User interrupted execution. Exiting gracefully...")
    except Exception as e:
        print(f"\n[!] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
