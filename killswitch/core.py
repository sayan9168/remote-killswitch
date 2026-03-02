import requests
import sys
import logging

# Set up logging for the library
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RemoteKillSwitch")

class KillSwitch:
    def __init__(self, config_url: str, developer_email: str):
        """
        Initializes the KillSwitch with the remote config URL and developer email.
        """
        self.config_url = config_url
        self.developer_email = developer_email

    def check_status(self):
        """
        Fetches the status from the remote URL and terminates the program 
        if the status is not 'active'.
        
        Expected JSON format: {"status": "active", "message": "Reason..."}
        """
        try:
            # Fetch data from the remote server
            response = requests.get(self.config_url, timeout=10)
            data = response.json()

            if data.get("status") != "active":
                self._trigger_shutdown(data.get("message", "Service Terminated by Developer."))
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error connecting to KillSwitch server: {e}")
            # Optional: Decide if the app should shut down if the server is unreachable
            # self._trigger_shutdown("Security check failed - cannot reach config server.")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")

    def _trigger_shutdown(self, message):
        """Terminates the application immediately."""
        print(f"\n[!] SECURITY ALERT: {message}")
        print(f"[!] Please contact: {self.developer_email}")
        sys.exit(1) # Exits the program
