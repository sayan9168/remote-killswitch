# Remote-KillSwitch 🛡️

A powerful Python library to remotely control and protect your code execution with advanced security features. Ideal for freelancers, developers, and businesses who need to maintain control over their software distribution and licensing.

## Features ✨

### Core Features
- **Remote Control:** Activate/deactivate your scripts from anywhere via JSON configuration
- **Easy Integration:** Add protection in just 3 lines of code
- **Custom Messages:** Display personalized messages when access is revoked

### Advanced Security Features 🔒
- **Version Control:** Restrict execution to specific app versions
- **License Expiry:** Set expiration dates for time-limited access
- **Feature Flags:** Remotely enable/disable specific features
- **Graceful Shutdown:** Execute cleanup callbacks before termination
- **Connection Retry Logic:** Configurable failure tolerance
- **Rate Limiting:** Cache status checks to reduce API calls
- **HTTPS Enforcement:** Ensure secure communication
- **Usage Analytics:** Track application usage metrics
- **Maintenance Mode:** Temporarily limit functionality during updates
- **Unique App ID:** Identify individual installations

## Installation 📦
```bash
pip install requests
```

## Quick Start 🚀

### Basic Usage (3 lines)
```python
from killswitch import KillSwitch

guardian = KillSwitch(config_url="YOUR_JSON_URL", developer_email="your@email.com")
guardian.check_status()
```

### Advanced Usage with All Features
```python
from killswitch import KillSwitch

def cleanup(reason):
    print(f"Cleaning up before shutdown: {reason}")

guardian = KillSwitch(
    config_url="https://your-server.com/status.json",
    developer_email="support@example.com",
    app_id="my-app-001",                    # Unique instance ID
    allowed_versions=["1.0.0", "1.1.0"],   # Version control
    expiry_date="2025-12-31",              # License expiry
    max_failures=3,                        # Retry attempts
    callback=cleanup,                      # Shutdown callback
    require_https=True,                    # Enforce HTTPS
    cache_duration=300,                    # Cache for 5 minutes
    # Enterprise Features
    api_secret="your-secret-key",          # HMAC authentication
    geo_restrictions=["US", "BD", "IN"],   # Country restrictions
    ip_whitelist=["192.168.1.1"],          # IP whitelist
    heartbeat_interval=60,                 # Heartbeat every 60s
    encryption_key="encrypt-key",          # Data encryption
    custom_headers={"X-API-Key": "key"},   # Custom headers
    offline_mode_timeout=7200,             # 2 hours offline allowed
    panic_mode_enabled=True                # Emergency shutdown
)

# Check status with version validation
guardian.check_status(current_version="1.0.0")

# Use feature flags
if guardian.get_feature_flag("premium_feature"):
    unlock_premium_content()

# Report usage analytics
guardian.report_usage({
    "session_duration": 120,
    "actions_performed": 45
})

# Get session information
session = guardian.get_session_info()
print(f"Session: {session}")

# Check announcements
for announcement in guardian.get_announcements():
    print(f"{announcement['title']}: {announcement['content']}")

# Validate license
if guardian.validate_license("LICENSE-KEY"):
    print("License valid!")
```

## Configuration File Format 📋

Your remote JSON file should follow this structure:

```json
{
  "status": "active",
  "message": "All systems operational",
  "allowed_versions": ["1.0.0", "1.1.0"],
  "maintenance_mode": false,
  "features": {
    "premium_feature": true,
    "beta_feature": false,
    "experimental_api": true
  },
  "announcements": [
    {
      "title": "Update Available",
      "content": "Version 2.0 is now available",
      "priority": "high"
    }
  ]
}
```

### Configuration Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | Must be `"active"` for app to run |
| `message` | string | Custom message shown on shutdown |
| `allowed_versions` | array | List of permitted version strings |
| `maintenance_mode` | boolean | Enable maintenance mode |
| `features` | object | Feature flags for remote control |
| `announcements` | array | Messages to display to users |

## API Reference 📖

### KillSwitch Class

#### Constructor Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `config_url` | str | required | URL to remote JSON config |
| `developer_email` | str | required | Contact email for support |
| `app_id` | str | auto-generated | Unique identifier for this instance |
| `allowed_versions` | List[str] | None | List of allowed versions |
| `expiry_date` | str | None | Expiry date in YYYY-MM-DD format |
| `max_failures` | int | 3 | Max connection failures before shutdown |
| `callback` | Callable | None | Function to call before shutdown |
| `require_https` | bool | True | Enforce HTTPS for config URL |
| `cache_duration` | int | 300 | Seconds to cache status checks |
| `api_secret` | str | None | HMAC signature verification key |
| `geo_restrictions` | List[str] | None | Allowed country codes (e.g., ["US", "BD"]) |
| `ip_whitelist` | List[str] | None | Allowed IP addresses/CIDR ranges |
| `heartbeat_interval` | int | 60 | Heartbeat signal interval in seconds |
| `encryption_key` | str | None | Key for data encryption |
| `custom_headers` | Dict | None | Custom HTTP headers |
| `offline_mode_timeout` | int | 3600 | Max seconds without server contact |
| `panic_mode_enabled` | bool | False | Enable emergency shutdown trigger |

#### Methods

##### `check_status(current_version=None)`
Performs all security checks and terminates if any fail.

```python
guardian.check_status(current_version="1.0.0")
```

##### `get_feature_flag(feature_name, default=False)`
Get the status of a specific feature flag.

```python
if guardian.get_feature_flag("premium_feature"):
    enable_premium_features()
```

##### `report_usage(usage_data)`
Send usage analytics to the server (non-blocking).

```python
guardian.report_usage({
    "user_actions": 50,
    "session_length": 300
})
```

##### `get_announcements()`
Get all active announcements from the server.

```python
for announcement in guardian.get_announcements():
    print(f"{announcement['title']}: {announcement['content']}")
```

##### `is_maintenance_mode()`
Check if system is currently in maintenance mode.

```python
if guardian.is_maintenance_mode():
    show_maintenance_screen()
```

##### `get_session_info()`
Get detailed session information.

```python
info = guardian.get_session_info()
print(f"App ID: {info['app_id']}")
print(f"Failures: {info['failure_count']}")
```

##### `validate_license(license_key)`
Validate a license key with the server.

```python
if guardian.validate_license("LICENSE-KEY"):
    enable_full_features()
```

##### `trigger_panic_shutdown(reason)`
Manually trigger emergency shutdown.

```python
guardian.trigger_panic_shutdown("Security breach detected")
```

##### `refresh_config(force=False)`
Force refresh configuration from server.

```python
guardian.refresh_config(force=True)
```

## Examples 💡

Check the `/examples` directory for complete working examples:
- `basic_usage.py` - Simple 3-line integration
- `advanced_usage.py` - Full-featured implementation

## Security Best Practices 🔐

1. **Always use HTTPS** for your configuration URL
2. **Set appropriate cache durations** to balance performance and control
3. **Implement graceful shutdown callbacks** to clean up resources
4. **Use version control** to phase out old clients gradually
5. **Monitor usage analytics** to detect unusual patterns

## Hosting Your Config File 🌐

You can host your JSON configuration file on:
- GitHub Gist (raw URL)
- Your own web server
- AWS S3 / Google Cloud Storage
- Any static file hosting service

Example GitHub Gist raw URL:
```
https://gist.githubusercontent.com/username/gist-id/raw/status.json
```

## Error Handling ⚠️

The library handles various error scenarios:
- Network timeouts
- Invalid JSON responses
- HTTP errors (4xx, 5xx)
- Missing configuration fields
- Connection failures with retry logic

## License 📄

MIT License - See LICENSE file for details

## Support 📧

For issues and questions, please contact the developer email configured in your KillSwitch instance.
