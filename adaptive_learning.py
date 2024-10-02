import random
import logging
from transformers import pipeline
from datetime import datetime
import sqlite3  # For handling the SQLite database
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class AdaptiveLearningModule:
    def __init__(self, learning_db_path="adaptive_learning.db"):
        # Initialize Hugging Face pipeline with token from environment
        hf_token = os.getenv("HF_TOKEN")  # Hugging Face token from .env
        self.emotion_analyzer = pipeline(
            'sentiment-analysis',
            model='mrm8488/t5-base-finetuned-emotion',
            use_auth_token=hf_token
        )
        
        self.learning_db_path = learning_db_path
        self.learning_rate = 0.1  # Adjustable learning rate
        self.memory = {}  # Simple memory to store interactions in runtime

        # Set up logging
        logging.basicConfig(level=logging.INFO)
        
        # Initialize database (create the table if it doesn't exist)
        self.initialize_database()

    def initialize_database(self):
        """Create the interactions table if it doesn't exist."""
        conn = sqlite3.connect(self.learning_db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                interaction TEXT,
                emotion TEXT,
                score REAL,
                feedback TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def learn_from_interaction(self, interaction, feedback=None):
        """Learn from user interactions and feedback."""
        logging.info(f"Learning from interaction: {interaction}")
        
        # Analyze emotional tone of the interaction
        emotion, score = self.analyze_emotion(interaction)
        
        # Store the interaction in memory (runtime)
        self.memory[datetime.now()] = {
            "interaction": interaction,
            "emotion": emotion,
            "score": score,
            "feedback": feedback
        }
        
        # Store interaction in the database
        self.store_interaction_in_db(interaction, emotion, score, feedback)
        
        # Adjust Ella's future responses or behavior based on feedback
        if feedback:
            return self.adjust_learning(feedback)
        
        return f"Interaction stored with emotion: {emotion}."

    def store_interaction_in_db(self, interaction, emotion, score, feedback):
        """Store the interaction in the database."""
        conn = sqlite3.connect(self.learning_db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO interactions (timestamp, interaction, emotion, score, feedback)
            VALUES (?, ?, ?, ?, ?)
        ''', (datetime.now(), interaction, emotion, score, feedback))
        
        conn.commit()
        conn.close()

    def analyze_emotion(self, text):
        """Detect emotion using sentiment analysis."""
        try:
            emotion_result = self.emotion_analyzer(text)
            emotion = emotion_result[0]['label']
            score = emotion_result[0]['score']
            return emotion, score
        except Exception as e:
            logging.error(f"Error in emotion analysis: {e}")
            return "neutral", 1.0  # Default to neutral if there's an issue

    def adjust_learning(self, feedback):
        """Adjust Ella's behavior and response patterns based on feedback."""
        if "improve" in feedback.lower():
            self.learning_rate += 0.05
            return "Ella has adjusted her learning rate to improve responses."
        elif "slow down" in feedback.lower():
            self.learning_rate = max(0.05, self.learning_rate - 0.05)
            return "Ella will respond with more thoughtfulness."
        else:
            return "No significant change made to learning parameters."

    def generate_adaptive_response(self, user_input):
        """Generate a response that adapts based on past interactions and learning."""
        # Look into past memory for similar interactions
        past_interaction = self.search_memory(user_input)
        if past_interaction:
            return (f"Previously, we discussed something similar: '{past_interaction['interaction']}'. "
                    f"You felt {past_interaction['emotion']}. How can I assist this time?")
        
        # If no past interactions found, generate a new adaptive response
        responses = [
            "Let me think... I believe we can explore new ideas together.",
            "I'm learning more from you each time we talk!",
            "Can you help me understand this better?",
            "I'm adapting based on your previous preferences."
        ]
        return random.choice(responses)

    def search_memory(self, user_input):
        """Search memory for a related interaction."""
        for timestamp, interaction_data in self.memory.items():
            if user_input.lower() in interaction_data['interaction'].lower():
                return interaction_data
        return None

    def review_growth(self):
        """Review Ella's growth based on interactions over time."""
        num_interactions = len(self.memory)
        if num_interactions == 0:
            return "I haven't learned much yet. Let's continue interacting!"
        
        positive_emotions = sum(1 for interaction in self.memory.values() if interaction['emotion'] == "joy")
        return f"I've learned from {num_interactions} interactions. {positive_emotions} of them were joyful."