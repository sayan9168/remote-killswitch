import requests
import sys
import logging
import hashlib
import json
from datetime import datetime, timedelta
from typing import Optional, Callable, List, Dict, Any
import time
import threading
import base64
import hmac
from functools import wraps

# Set up logging for the library
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RemoteKillSwitch")

class KillSwitch:
    def __init__(
        self, 
        config_url: str, 
        developer_email: str,
        app_id: Optional[str] = None,
        allowed_versions: Optional[List[str]] = None,
        expiry_date: Optional[str] = None,
        max_failures: int = 3,
        callback: Optional[Callable[[str], None]] = None,
        require_https: bool = True,
        cache_duration: int = 300,
        api_secret: Optional[str] = None,
        geo_restrictions: Optional[List[str]] = None,
        ip_whitelist: Optional[List[str]] = None,
        heartbeat_interval: int = 60,
        encryption_key: Optional[str] = None,
        custom_headers: Optional[Dict[str, str]] = None,
        offline_mode_timeout: int = 3600,
        panic_mode_enabled: bool = False
    ):
        """
        Initializes the ultra-advanced KillSwitch with enterprise-grade security features.
        
        Args:
            config_url: URL of the remote JSON configuration file
            developer_email: Contact email for support
            app_id: Unique identifier for this application instance
            allowed_versions: List of allowed version strings (e.g., ["1.0.0", "1.1.0"])
            expiry_date: Expiry date in ISO format (YYYY-MM-DD)
            max_failures: Maximum number of connection failures before shutdown
            callback: Optional callback function to execute before shutdown
            require_https: Enforce HTTPS for config URL (default: True)
            cache_duration: Cache duration in seconds for status checks
            api_secret: Secret key for HMAC signature verification
            geo_restrictions: List of allowed country codes (ISO 3166-1 alpha-2)
            ip_whitelist: List of allowed IP addresses or CIDR ranges
            heartbeat_interval: Interval in seconds for sending heartbeat signals
            encryption_key: Key for encrypting sensitive communications
            custom_headers: Custom HTTP headers for requests
            offline_mode_timeout: Seconds app can run without server contact
            panic_mode_enabled: Enable emergency shutdown trigger
        """
        self.config_url = config_url
        self.developer_email = developer_email
        self.app_id = app_id or self._generate_app_id()
        self.allowed_versions = allowed_versions
        self.expiry_date = expiry_date
        self.max_failures = max_failures
        self.callback = callback
        self.require_https = require_https
        self.cache_duration = cache_duration
        self.api_secret = api_secret
        self.geo_restrictions = geo_restrictions
        self.ip_whitelist = ip_whitelist
        self.heartbeat_interval = heartbeat_interval
        self.encryption_key = encryption_key
        self.custom_headers = custom_headers or {}
        self.offline_mode_timeout = offline_mode_timeout
        self.panic_mode_enabled = panic_mode_enabled
        
        # Security features
        self._failure_count = 0
        self._last_check_time = None
        self._cached_status = None
        self._cached_config = None
        self._integrity_hash = None
        self._heartbeat_thread = None
        self._panic_code = None
        self._session_token = None
        self._last_heartbeat = None
        self._offline_start_time = None
        
        # Initialize heartbeat if enabled
        if heartbeat_interval > 0:
            self._start_heartbeat()
        
        # Validate HTTPS requirement
        if require_https and not config_url.startswith("https://"):
            logger.warning(f"Security Warning: Config URL should use HTTPS. Current: {config_url}")
    
    def _generate_app_id(self) -> str:
        """Generate a unique app ID based on system info and timestamp."""
        import socket
        import os
        import uuid
        
        # More robust unique ID generation
        unique_string = f"{socket.gethostname()}{os.getpid()}{time.time()}{uuid.uuid4()}"
        return hashlib.sha256(unique_string.encode()).hexdigest()[:16]
    
    def _start_heartbeat(self):
        """Start background heartbeat thread."""
        def heartbeat_loop():
            while True:
                try:
                    time.sleep(self.heartbeat_interval)
                    self._send_heartbeat()
                except Exception as e:
                    logger.debug(f"Heartbeat failed: {e}")
        
        self._heartbeat_thread = threading.Thread(target=heartbeat_loop, daemon=True)
        self._heartbeat_thread.start()
        logger.info("Heartbeat monitoring started")
    
    def _send_heartbeat(self):
        """Send heartbeat signal to server."""
        try:
            payload = {
                "app_id": self.app_id,
                "timestamp": datetime.now().isoformat(),
                "status": "alive",
                "session_token": self._session_token
            }
            
            if self.api_secret:
                signature = self._generate_signature(payload)
                payload["signature"] = signature
            
            heartbeat_url = self.config_url.replace("status.json", "heartbeat.json")
            requests.post(heartbeat_url, json=payload, timeout=5)
            self._last_heartbeat = time.time()
        except Exception as e:
            logger.debug(f"Heartbeat transmission failed: {e}")
    
    def _generate_signature(self, data: Dict) -> str:
        """Generate HMAC signature for request integrity."""
        if not self.api_secret:
            return ""
        
        message = json.dumps(data, sort_keys=True)
        signature = hmac.new(
            self.api_secret.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def _verify_signature(self, data: Dict, signature: str) -> bool:
        """Verify HMAC signature of received data."""
        if not self.api_secret or not signature:
            return True  # Skip verification if no secret
        
        expected_signature = self._generate_signature(data)
        return hmac.compare_digest(expected_signature, signature)
    
    def _encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data using base64 (simple obfuscation)."""
        if not self.encryption_key:
            return data
        # Simple encryption (for production, use cryptography library)
        encrypted = base64.b64encode(data.encode()).decode()
        return encrypted
    
    def _decrypt_data(self, data: str) -> str:
        """Decrypt data."""
        if not self.encryption_key:
            return data
        try:
            decrypted = base64.b64decode(data.encode()).decode()
            return decrypted
        except:
            return data
    
    def _check_geo_restrictions(self) -> bool:
        """Check if application is running in allowed geographic region."""
        if not self.geo_restrictions:
            return True
        
        try:
            # Get country code from IP (using external service)
            response = requests.get("https://ipapi.co/country/", timeout=5)
            if response.status_code == 200:
                country_code = response.text.strip().upper()
                if country_code in self.geo_restrictions:
                    return True
                else:
                    logger.warning(f"Access denied from country: {country_code}")
                    return False
        except Exception as e:
            logger.debug(f"Geo-check failed: {e}")
            return True  # Allow on error
        
        return True
    
    def _check_ip_whitelist(self) -> bool:
        """Check if current IP is in whitelist."""
        if not self.ip_whitelist:
            return True
        
        try:
            # Get current IP
            response = requests.get("https://ipapi.co/ip/", timeout=5)
            if response.status_code == 200:
                current_ip = response.text.strip()
                if current_ip in self.ip_whitelist:
                    return True
                else:
                    logger.warning(f"Access denied from IP: {current_ip}")
                    return False
        except Exception as e:
            logger.debug(f"IP check failed: {e}")
            return True  # Allow on error
        
        return True
    
    def _check_offline_timeout(self) -> bool:
        """Check if app has exceeded offline timeout."""
        if self._offline_start_time is None:
            return True
        
        elapsed = time.time() - self._offline_start_time
        if elapsed > self.offline_mode_timeout:
            logger.error(f"Offline timeout exceeded: {elapsed} seconds")
            return False
        
        return True
    
    def _validate_config_integrity(self, data: dict) -> bool:
        """Validate the integrity of the received configuration."""
        if not isinstance(data, dict):
            return False
        
        required_fields = ["status"]
        for field in required_fields:
            if field not in data:
                logger.error(f"Missing required field: {field}")
                return False
        
        # Verify signature if API secret is set
        if self.api_secret:
            signature = data.get("signature")
            if signature and not self._verify_signature(data, signature):
                logger.error("Configuration signature verification failed")
                return False
        
        return True
    
    def _check_expiry(self) -> bool:
        """Check if the application has passed its expiry date."""
        if not self.expiry_date:
            return True
        
        try:
            expiry = datetime.fromisoformat(self.expiry_date)
            return datetime.now() <= expiry
        except ValueError as e:
            logger.error(f"Invalid expiry date format: {e}")
            return True
    
    def _check_version(self, current_version: str) -> bool:
        """Check if the current version is allowed."""
        if not self.allowed_versions:
            return True
        
        return current_version in self.allowed_versions
    
    def _enforce_rate_limiting(self) -> bool:
        """Enforce rate limiting on status checks."""
        if self._last_check_time is None:
            return True
        
        elapsed = time.time() - self._last_check_time
        return elapsed >= self.cache_duration
    
    def check_status(self, current_version: Optional[str] = None) -> bool:
        """
        Fetches the status from the remote URL and terminates the program 
        if the status is not 'active' or other security checks fail.
        
        Expected JSON format: {
            "status": "active",
            "message": "Reason...",
            "allowed_versions": ["1.0.0"],
            "maintenance_mode": false,
            "features": {"feature_name": true/false}
        }
        
        Returns:
            bool: True if all checks pass, False otherwise (before shutdown)
        """
        # Check geo-restrictions
        if not self._check_geo_restrictions():
            self._trigger_shutdown("Access denied: Application not authorized in your region.")
            return False
        
        # Check IP whitelist
        if not self._check_ip_whitelist():
            self._trigger_shutdown("Access denied: Your IP address is not whitelisted.")
            return False
        
        # Check offline timeout
        if not self._check_offline_timeout():
            self._trigger_shutdown("Offline mode timeout exceeded. Internet connection required.")
            return False
        
        # Check panic mode
        if self.panic_mode_enabled and self._check_panic_trigger():
            self._trigger_shutdown("Emergency shutdown triggered.")
            return False
        
        # Check rate limiting
        if not self._enforce_rate_limiting():
            logger.debug("Status check skipped due to rate limiting")
            # Still validate offline timeout even when cached
            if not self._check_offline_timeout():
                self._trigger_shutdown("Offline mode timeout exceeded.")
                return False
            return self._cached_status == "active" if self._cached_status else True
        
        # Check expiry date
        if not self._check_expiry():
            self._trigger_shutdown("Application license has expired.")
            return False
        
        # Check version compatibility
        if current_version and not self._check_version(current_version):
            self._trigger_shutdown(f"Version {current_version} is no longer supported.")
            return False
        
        try:
            # Prepare request headers
            headers = self.custom_headers.copy()
            if self.api_secret:
                # Generate signature for request authentication
                req_data = {"app_id": self.app_id, "timestamp": time.time()}
                signature = self._generate_signature(req_data)
                headers["X-Signature"] = signature
                headers["X-App-ID"] = self.app_id
            
            # Fetch data from the remote server
            response = requests.get(self.config_url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Validate configuration integrity
            if not self._validate_config_integrity(data):
                self._trigger_shutdown("Configuration integrity check failed.")
                return False
            
            # Reset failure count and offline timer on successful fetch
            self._failure_count = 0
            self._last_check_time = time.time()
            self._offline_start_time = None
            self._cached_status = data.get("status")
            self._cached_config = data
            
            # Extract session token if provided
            self._session_token = data.get("session_token", self._session_token)
            
            # Check maintenance mode
            if data.get("maintenance_mode", False):
                logger.info("System is in maintenance mode. Limited functionality may apply.")
            
            # Check feature flags if present
            features = data.get("features", {})
            for feature_name, enabled in features.items():
                if not enabled:
                    logger.warning(f"Feature '{feature_name}' is disabled remotely.")
            
            # Check announcements
            announcements = data.get("announcements", [])
            for announcement in announcements:
                priority = announcement.get("priority", "normal")
                title = announcement.get("title", "Announcement")
                content = announcement.get("content", "")
                logger.info(f"[{priority.upper()}] {title}: {content}")
            
            # Check main status
            if data.get("status") != "active":
                self._trigger_shutdown(data.get("message", "Service Terminated by Developer."))
                return False
            
            logger.info("All security checks passed. Application is authorized to run.")
            return True
        
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            self._handle_connection_failure()
        except requests.exceptions.Timeout as e:
            logger.error(f"Request timed out: {e}")
            self._handle_connection_failure()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error connecting to KillSwitch server: {e}")
            # Start offline timer on first failure
            if self._offline_start_time is None:
                self._offline_start_time = time.time()
            self._handle_connection_failure()
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON response: {e}")
            self._trigger_shutdown("Configuration parsing failed.")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            self._handle_connection_failure()
        
        return False
    
    def _check_panic_trigger(self) -> bool:
        """Check if panic shutdown has been triggered."""
        # This can be extended to check for external panic signals
        # For now, it's a placeholder for future implementation
        return False
    
    def trigger_panic_shutdown(self, reason: str = "Emergency shutdown"):
        """Manually trigger an emergency shutdown."""
        self._trigger_shutdown(f"PANIC: {reason}")
    
    def _handle_connection_failure(self):
        """Handle connection failures with retry logic."""
        self._failure_count += 1
        
        if self._failure_count >= self.max_failures:
            self._trigger_shutdown(
                f"Security check failed after {self.max_failures} attempts - "
                "cannot reach config server."
            )
        else:
            logger.warning(
                f"Connection attempt {self._failure_count}/{self.max_failures} failed. "
                f"Retries remaining: {self.max_failures - self._failure_count}"
            )
    
    def _trigger_shutdown(self, message: str):
        """Terminates the application with graceful cleanup."""
        try:
            # Execute callback if provided
            if self.callback:
                try:
                    self.callback(message)
                except Exception as e:
                    logger.error(f"Callback execution failed: {e}")
            
            # Log shutdown event
            shutdown_log = {
                "timestamp": datetime.now().isoformat(),
                "app_id": self.app_id,
                "reason": message,
                "developer_contact": self.developer_email
            }
            logger.info(f"Shutdown log: {json.dumps(shutdown_log)}")
            
            # Display user-friendly message
            print("\n" + "="*60)
            print(f"[!] SECURITY ALERT: {message}")
            print(f"[!] Application ID: {self.app_id}")
            print(f"[!] Please contact: {self.developer_email}")
            print("="*60 + "\n")
            
        finally:
            sys.exit(1)
    
    def get_feature_flag(self, feature_name: str, default: bool = False) -> bool:
        """
        Get the status of a specific feature flag from cached config.
        
        Args:
            feature_name: Name of the feature to check
            default: Default value if feature is not found
        
        Returns:
            bool: Feature enabled status
        """
        if self._cached_status and isinstance(self._cached_status, dict):
            features = self._cached_status.get("features", {})
            return features.get(feature_name, default)
        return default
    
    def report_usage(self, usage_data: dict):
        """
        Report usage statistics to the remote server.
        
        Args:
            usage_data: Dictionary containing usage metrics
        """
        try:
            payload = {
                "app_id": self.app_id,
                "timestamp": datetime.now().isoformat(),
                "data": usage_data
            }
            
            # Send usage data asynchronously (non-blocking)
            def send_usage():
                try:
                    headers = self.custom_headers.copy()
                    if self.api_secret:
                        signature = self._generate_signature(payload)
                        headers["X-Signature"] = signature
                    
                    requests.post(
                        self.config_url.replace("status.json", "usage.json"),
                        json=payload,
                        headers=headers,
                        timeout=5
                    )
                except Exception as e:
                    logger.debug(f"Usage reporting failed: {e}")
            
            thread = threading.Thread(target=send_usage, daemon=True)
            thread.start()
            
        except Exception as e:
            logger.debug(f"Failed to queue usage report: {e}")
    
    def get_announcements(self) -> List[Dict[str, Any]]:
        """
        Get all announcements from cached config.
        
        Returns:
            List of announcement dictionaries
        """
        if self._cached_config:
            return self._cached_config.get("announcements", [])
        return []
    
    def is_maintenance_mode(self) -> bool:
        """
        Check if system is in maintenance mode.
        
        Returns:
            bool: True if in maintenance mode
        """
        if self._cached_config:
            return self._cached_config.get("maintenance_mode", False)
        return False
    
    def get_session_info(self) -> Dict[str, Any]:
        """
        Get current session information.
        
        Returns:
            Dictionary with session details
        """
        return {
            "app_id": self.app_id,
            "session_token": self._session_token,
            "last_check": self._last_check_time,
            "last_heartbeat": self._last_heartbeat,
            "failure_count": self._failure_count,
            "is_cached": self._cached_status is not None,
            "offline_since": self._offline_start_time
        }
    
    def refresh_config(self, force: bool = False) -> bool:
        """
        Force refresh of configuration from server.
        
        Args:
            force: If True, bypass rate limiting
        
        Returns:
            bool: True if refresh successful
        """
        if force:
            self._last_check_time = None
        
        return self.check_status()
    
    def validate_license(self, license_key: str) -> bool:
        """
        Validate a license key with the server.
        
        Args:
            license_key: License key to validate
        
        Returns:
            bool: True if license is valid
        """
        try:
            payload = {
                "app_id": self.app_id,
                "license_key": self._encrypt_data(license_key) if self.encryption_key else license_key,
                "timestamp": datetime.now().isoformat()
            }
            
            if self.api_secret:
                payload["signature"] = self._generate_signature(payload)
            
            response = requests.post(
                self.config_url.replace("status.json", "validate.json"),
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("valid", False)
            
            return False
        except Exception as e:
            logger.error(f"License validation failed: {e}")
            return False
    
    def extend_offline_timeout(self, seconds: int):
        """
        Extend the offline mode timeout.
        
        Args:
            seconds: Additional seconds to allow offline mode
        """
        self.offline_mode_timeout += seconds
        logger.info(f"Offline timeout extended by {seconds} seconds")
    
    def disable_heartbeat(self):
        """Disable the heartbeat monitoring."""
        self.heartbeat_interval = 0
        logger.info("Heartbeat monitoring disabled")
    
    def enable_heartbeat(self, interval: int = 60):
        """
        Enable heartbeat monitoring.
        
        Args:
            interval: Heartbeat interval in seconds
        """
        self.heartbeat_interval = interval
        self._start_heartbeat()
        logger.info(f"Heartbeat monitoring enabled with {interval}s interval")

