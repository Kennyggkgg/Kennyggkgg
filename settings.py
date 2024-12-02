import os

# Hugging Face API Token
HF_TOKEN = "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"  # Replace with your actual Hugging Face token

# Knowledge Graph Database Configuration
KNOWLEDGE_GRAPH_DB = "knowledge_graph.db"  # Path to your knowledge graph database file

# Logging Configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
        'verbose': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
        'simple': {
            'format': '%(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'app.log',  # Log file for general application logs
            'formatter': 'standard',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        '': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Email Configuration for Alerts
EMAIL_SETTINGS = {
    'sender': 's2251584249@gmail.com',           # Your email address
    'receiver': 'darkphoenixlord101@gmail.com',      # Email to receive alerts
    'password': 'Jesus is my saviour',           # Email password (consider using environment variables for security)
}

# Camera and Voice Settings
CAMERA_SETTINGS = {
    'monitoring_enabled': True,                  # Enable or disable camera monitoring
    'resolution': '1080p',                       # Camera resolution settings
}

VOICE_SETTINGS = {
    'language': 'en-US',                         # Default language for voice interface
    'gender': 'female',                          # Gender voice preference
}

# Intrusion Detection Settings
INTRUSION_DETECTION_SETTINGS = {
    'detection_enabled': True,                   # Enable or disable intrusion detection
    'sensitivity': 'high',                       # Sensitivity level for detecting intrusions
}

# File Paths
FILE_PATHS = {
    'ella_commands': os.path.join(os.path.dirname(__file__), 'ella_commands.py'),  # Path to Ella's command file
}

# Feature Flags
FEATURE_FLAGS = {
    'enable_singing_module': True,               # Feature flag to enable the singing module
    'enable_dynamic_expansion': True,            # Feature flag for dynamic expansion features
}

# Other Configuration Variables
OTHER_SETTINGS = {
    'max_learning_attempts': 5,                  # Maximum attempts for learning new knowledge
    'response_length': 50,                        # Default length for generated responses
}

# Use this function to load environment variables if needed
def load_env_variables():
    from dotenv import load_dotenv
    load_dotenv()

# Optional: Load environment variables
load_env_variables()