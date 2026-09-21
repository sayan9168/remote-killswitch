"""
Ultra-Advanced KillSwitch Example
Demonstrates all enterprise-grade features
"""

from killswitch import KillSwitch
import time

def cleanup_callback(reason):
    """Graceful shutdown callback"""
    print(f"\n[CLEANUP] Saving data before shutdown: {reason}")
    # Save important data, close connections, etc.

def main():
    # Initialize with ALL advanced features
    guardian = KillSwitch(
        config_url="https://your-server.com/status.json",
        developer_email="support@example.com",
        app_id="enterprise-app-001",
        allowed_versions=["1.0.0", "1.1.0", "2.0.0"],
        expiry_date="2026-12-31",
        max_failures=5,
        callback=cleanup_callback,
        require_https=True,
        cache_duration=300,
        # NEW ADVANCED FEATURES:
        api_secret="your-secret-key-here",           # HMAC signature verification
        geo_restrictions=["US", "BD", "IN"],         # Allow only specific countries
        ip_whitelist=["192.168.1.1", "10.0.0.0/24"], # Whitelist specific IPs
        heartbeat_interval=60,                        # Send heartbeat every 60s
        encryption_key="encryption-key",              # Encrypt sensitive data
        custom_headers={"X-API-Key": "your-api-key"}, # Custom HTTP headers
        offline_mode_timeout=7200,                    # Allow 2 hours offline
        panic_mode_enabled=True                       # Enable emergency shutdown
    )
    
    # Check status with version validation
    print("Checking system status...")
    guardian.check_status(current_version="1.1.0")
    
    # Get session information
    session_info = guardian.get_session_info()
    print(f"\nSession Info: {session_info}")
    
    # Check feature flags
    if guardian.get_feature_flag("premium_feature", default=False):
        print("\n✓ Premium feature unlocked!")
        # unlock_premium_content()
    
    if guardian.get_feature_flag("beta_feature", default=False):
        print("✓ Beta feature enabled!")
        # enable_beta_features()
    
    # Check maintenance mode
    if guardian.is_maintenance_mode():
        print("\n⚠ System is in maintenance mode")
        # Show maintenance message to users
    
    # Get announcements
    announcements = guardian.get_announcements()
    for announcement in announcements:
        priority = announcement.get('priority', 'normal')
        title = announcement.get('title', 'Announcement')
        content = announcement.get('content', '')
        print(f"\n[{priority.upper()}] {title}: {content}")
    
    # Report usage analytics
    guardian.report_usage({
        "session_duration": 120,
        "actions_performed": 45,
        "user_id": "user123",
        "features_used": ["feature1", "feature2"]
    })
    
    # Validate license key (if needed)
    # license_valid = guardian.validate_license("LICENSE-KEY-HERE")
    # if license_valid:
    #     print("✓ License validated successfully")
    
    # Force refresh configuration
    # guardian.refresh_config(force=True)
    
    # Extend offline timeout if needed
    # guardian.extend_offline_timeout(3600)  # Add 1 hour
    
    # Emergency shutdown (if security breach detected)
    # guardian.trigger_panic_shutdown("Security breach detected")
    
    print("\n✓ All systems operational - Application running normally")
    
    # Main application loop
    while True:
        try:
            # Your application logic here
            print("Working...", end="\r")
            time.sleep(1)
        except KeyboardInterrupt:
            print("\n\nApplication stopped by user")
            break

if __name__ == "__main__":
    main()
