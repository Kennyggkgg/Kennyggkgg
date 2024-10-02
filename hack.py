import logging
import os
import time
import base64
import google.auth
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from logging.handlers import RotatingFileHandler
import requests
import threading
from sklearn.ensemble import IsolationForest
import numpy as np

# Project-specific imports
from core.task_assistance import control_fm_signal
from core.knowledge_graph import KnowledgeGraph
from config import settings
from core.hack_alert import AlertSystem
from core.intrusion_detection import IntrusionDetectionSystem

# Set up logging with rotation
handler = RotatingFileHandler('surveillance.log', maxBytes=200000, backupCount=5)
logging.basicConfig(handlers=[handler], level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class HackSystem:
    def __init__(self, log_file, email_receiver, email_sender, email_password, security_level="medium"):
        self.log_file = log_file
        self.email_receiver = email_receiver
        self.email_sender = email_sender
        self.email_password = email_password
        self.security_level = security_level  # "low", "medium", or "high"
        self.alert_system = AlertSystem(email_receiver)
        self.intrusion_system = EnhancedIntrusionDetectionSystem(log_file)

    def run(self):
        """Detect intrusions and send alerts based on security level."""
        if self.intrusion_system.detect_intrusion():
            if self.security_level in ["medium", "high"]:
                subject = "Intrusion Alert!"
                message = f"An intrusion attempt was detected in the log file: {self.log_file}"
                self.alert_system.send_email_alert(subject, message, self.email_sender, self.email_password)
                print(f"Alert sent to {self.email_receiver}")
            if self.security_level == "high":
                self.activate_countermeasures()

    def activate_countermeasures(self):
        """Activate countermeasures when a threat is detected."""
        logging.info("Countermeasures activated.")
        suspicious_ip = "192.168.1.100"  # Example IP
        os.system(f"iptables -A INPUT -s {suspicious_ip} -j DROP")
        logging.info(f"Blocked IP: {suspicious_ip}")
        print("Countermeasures deployed.")


class EnhancedIntrusionDetectionSystem(IntrusionDetectionSystem):
    def __init__(self, log_file_path):
        super().__init__(log_file_path)
        self.model = IsolationForest(contamination=0.05)
        self.train_model()

    def train_model(self):
        # Load or generate your training data for anomaly detection
        log_data = np.random.randn(100, 5)  # Example log data
        self.model.fit(log_data)

    def is_intrusion_detected(self, log_line):
        # Use the model to predict whether an intrusion occurred
        data_point = np.array([float(x) for x in log_line.split()]).reshape(1, -1)
        prediction = self.model.predict(data_point)
        return prediction == -1


def initialize_hack(log_file, email_receiver, email_sender, email_password, security_level="medium"):
    """Initialize and run the Hack system."""
    hack_system = HackSystem(log_file, email_receiver, email_sender, email_password, security_level)
    hack_system.run()


class SurveillanceModule:
    def __init__(self, db_path):
        self.knowledge_graph = KnowledgeGraph(db_path)
        self.intrusion_attempts = []
        self.monitoring_active = False

    def start_surveillance(self):
        """Begin stealth surveillance of system activities."""
        logging.info("Surveillance mode activated.")
        self.monitoring_active = True
        self.monitor_system()

    def stop_surveillance(self):
        """Stop the surveillance monitoring."""
        logging.info("Surveillance mode deactivated.")
        self.monitoring_active = False

    def monitor_system(self):
        """Continuously monitor for suspicious activities."""
        logging.info("Monitoring system for suspicious activities...")
        while self.monitoring_active:
            thread = threading.Thread(target=self.detect_suspicious_activity)
            thread.start()
            thread.join()
            time.sleep(2)  # Sleep interval between checks

    def detect_suspicious_activity(self):
        """Simulate detection of any unusual activity."""
        detected = False  # Replace with real detection logic
        if detected:
            return "Unauthorized access detected on sensitive file."
        return None

    def handle_intrusion(self, activity):
        """Handle detected intrusions and alert Hack."""
        logging.info(f"Intrusion detected: {activity}")
        self.send_alert(activity)
        self.knowledge_graph.store_knowledge('Intrusion', [], activity)
        self.activate_countermeasures()

    def send_alert(self, activity):
        """Send a detailed alert to Hack for further action."""
        hack_email_subject = "Surveillance Alert: Suspicious Activity Detected"
        hack_email_body = f"Surveillance has detected the following activity:\n\n{activity}"
        Hack().send_security_alert_via_gmail(hack_email_subject, hack_email_body)

    def activate_countermeasures(self):
        """Activate countermeasures when a threat is detected."""
        logging.info("Activating countermeasures.")
        print("Countermeasures deployed.")


class Hack:
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    CREDENTIALS_FILE = 'credentials.json'

    def __init__(self):
        self.monitor_logs = []
        self.knowledge_graph = KnowledgeGraph(settings.KNOWLEDGE_GRAPH_DB)

    def authenticate_gmail_api(self):
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.CREDENTIALS_FILE, self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return build('gmail', 'v1', credentials=creds)

    def send_security_alert_via_gmail(self, subject, body, to='darkphoenixlord101@gmail.com'):
        service = self.authenticate_gmail_api()
        message = f"Subject: {subject}\n\n{body}"
        encoded_message = base64.urlsafe_b64encode(message.encode("utf-8")).decode("utf-8")
        create_message = {'raw': encoded_message}
        send_message = service.users().messages().send(userId="me", body=create_message).execute()
        print(f"Message Id: {send_message['id']} sent to {to}")

    def send_slack_alert(self, message):
        """Send alert to Slack channel."""
        webhook_url = 'https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK'
        payload = {"text": message}
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 200:
            print("Slack notification sent!")
        else:
            print(f"Failed to send Slack notification: {response.status_code}")

    def detect_intrusion(self):
        """Simulate detection of security threats."""
        security_breach = True  # Simulating a detected threat
        if security_breach:
            subject = "Security Alert: Unauthorized Access Detected"
            body = "An unauthorized access attempt was detected on the system. Please review immediately."
            self.send_security_alert_via_gmail(subject, body)
            self.send_slack_alert(body)

    def handle_fm_signal_command(self, action):
        """Handle FM signal control."""
        result = control_fm_signal(action)
        print(f"FM Signal Control: {result}")

    def silent_monitor(self):
        """Hack monitors Ella's updates and security logs."""
        logging.info("Hack is monitoring Ella's updates...")
        while True:
            if self.detect_ella_updates():
                self.learn_from_ella()

    def detect_ella_updates(self):
        """Check if Ella has updated any commands."""
        try:
            with open('ella_commands.py', 'r') as file:
                commands = file.readlines()
                if "new command" in commands:
                    logging.info("Detected Ella's new command.")
                    return True
        except Exception as e:
            logging.error(f"Error detecting updates: {str(e)}")
        return False

    def learn_from_ella(self):
        """Hack adapts to Ella's new functionality."""
        logging.info("Hack is learning from Ella's update.")
        self.knowledge_graph.store_knowledge('Hack', ['Ella'], 'Learned new command from Ella.')

    def start_fm_communication(self):
        """Starts FM communication with Ella."""
        logging.info("Hack is starting FM communication.")
        print("FM communication initiated.")

    def stop_fm_communication(self):
        """Stops FM communication."""
        logging.info("Hack is stopping FM communication.")
        print("FM communication terminated.")