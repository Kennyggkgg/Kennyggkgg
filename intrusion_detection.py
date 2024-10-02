import os

class IntrusionDetectionSystem:
    def __init__(self, log_file_path):
        self.log_file_path = log_file_path

    def detect_intrusion(self):
        if os.path.exists(self.log_file_path):
            with open(self.log_file_path, 'r') as log_file:
                for line in log_file.readlines():
                    if self.is_intrusion_detected(line):
                        print(f"Intrusion detected: {line}")
                        return True
        return False

    def is_intrusion_detected(self, log_line):
        suspicious_patterns = ["Failed login", "Access denied", "Error code 404"]
        for pattern in suspicious_patterns:
            if pattern in log_line:
                return True
        return False