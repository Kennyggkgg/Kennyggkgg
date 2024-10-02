import requests
import json
import logging
from config.config import API_KEYS
from core.resource_management import FMController

# This is the function that interfaces with the FM signal system
def control_fm_signal(action):
    if action == "start":
        if FMController.start_fm_signal():
            return "FM signal started successfully."
        else:
            return "Failed to start FM signal."
    elif action == "stop":
        if FMController.stop_fm_signal():
            return "FM signal stopped successfully."
        else:
            return "Failed to stop FM signal."
    else:
        return "Unknown action for FM signal control."


class APITaskHandler:
    def __init__(self):
        self.api_keys = API_KEYS

    def fetch_weather(self, location):
        """Fetch weather data using an external weather API."""
        try:
            url = f"http://api.weatherapi.com/v1/current.json?key={self.api_keys['weather']}&q={location}"
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                logging.error(f"Failed to fetch weather data: {response.status_code}")
                return None
        except Exception as e:
            logging.error(f"Error fetching weather data: {str(e)}")
            return None

    def get_news(self, topic="technology"):
        """Fetch news based on the topic from an external news API."""
        try:
            url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={self.api_keys['news']}"
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                logging.error(f"Failed to fetch news: {response.status_code}")
                return None
        except Exception as e:
            logging.error(f"Error fetching news: {str(e)}")
            return None

    def send_email(self, recipient, subject, body):
        """Send an email using an email API."""
        try:
            url = f"https://api.mailgun.net/v3/{self.api_keys['mailgun_domain']}/messages"
            auth = ('api', self.api_keys['mailgun'])
            data = {
                "from": f"Ella AI <ella@{self.api_keys['mailgun_domain']}>",
                "to": [recipient],
                "subject": subject,
                "text": body
            }
            response = requests.post(url, auth=auth, data=data)
            if response.status_code == 200:
                return response.json()
            else:
                logging.error(f"Failed to send email: {response.status_code}")
                return None
        except Exception as e:
            logging.error(f"Error sending email: {str(e)}")
            return None

    def control_smart_home(self, device_id, command):
        """Control a smart home device using an external API."""
        try:
            url = f"http://smarthomeapi.com/devices/{device_id}/commands"
            headers = {
                "Authorization": f"Bearer {self.api_keys['smarthome']}",
                "Content-Type": "application/json"
            }
            data = json.dumps({"command": command})
            response = requests.post(url, headers=headers, data=data)
            if response.status_code == 200:
                return response.json()
            else:
                logging.error(f"Failed to control smart home device: {response.status_code}")
                return None
        except Exception as e:
            logging.error(f"Error controlling smart home device: {str(e)}")
            return None

    def fetch_stock_price(self, symbol):
        """Fetch stock price data using an external financial API."""
        try:
            url = f"https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={self.api_keys['stock']}"
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                logging.error(f"Failed to fetch stock data: {response.status_code}")
                return None
        except Exception as e:
            logging.error(f"Error fetching stock data: {str(e)}")
            return None