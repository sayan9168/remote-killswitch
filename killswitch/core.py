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
        self.config_url = https://gist.githubusercontent.com/sayan9168/269e8a32c214ea9d3b1b998432034898/raw/0b1a904ecb33bf207ed83bab82279328bf99f379/status.json
        self.developer_email = sm6881164@gmail.com

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
