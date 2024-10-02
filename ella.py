import os
import logging
import json
import torch
import base64
import numpy as np
from collections import defaultdict
from transformers import pipeline, GPT2Tokenizer, GPT2LMHeadModel
from rl.algorithms import DeepQNetwork  # Using your actual implementation
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from ella_singing_module import EllaSingingModule  # Existing modules
from core.emotional_intelligence import EmotionalIntelligenceModule
from core.knowledge_graph import KnowledgeGraph
from config import settings

# Set up logging
logging.basicConfig(filename='advanced_ai.log', level=logging.INFO)

class EmotionalRLAgent:
    def __init__(self):
        self.agent = DeepQNetwork()  # Initialize your actual DeepQNetwork class
        self.emotions = ['joy', 'sadness', 'neutral', 'laughter']
        self.actions = ['tell_joke', 'play_music', 'offer_help']
    
    def get_state(self, user_emotion):
        """Convert user emotion into a numerical state."""
        return user_emotion  # Use user emotion directly as state
    
    def get_action(self, state):
        """Choose an action based on the current emotional state."""
        return self.agent.choose_action(state, self.actions)  # Use the available actions
    
    def reward_function(self, user_reaction):
        """Define a reward function based on user reaction."""
        if user_reaction in ['joy', 'laughter']:
            return 1
        elif user_reaction == 'sadness':
            return -1
        return 0
    
    def update(self, state, action, reward, next_state):
        """Update the agent's policy based on the experience."""
        self.agent.update_q_value(state, action, reward, next_state)
    
    def run(self, user_emotion, user_reaction):
        """Run the reinforcement learning loop."""
        state = self.get_state(user_emotion)
        action = self.get_action(state)
        reward = self.reward_function(user_reaction)
        next_state = self.get_state(user_reaction)
        self.update(state, action, reward, next_state)
        self.agent.reset_episode()  # Reset episode for decaying exploration


class EmotionalAnalysis:
    def __init__(self):
        self.analyzer = pipeline('sentiment-analysis')
    
    def analyze_emotion(self, user_input):
        result = self.analyzer(user_input)
        return result[0]['label'], result[0]['score']


class PersonalizedAI:
    def __init__(self, model_name='gpt2'):
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.model = GPT2LMHeadModel.from_pretrained(model_name)
    
    def generate_response(self, user_input, user_profile):
        prompt = f"{user_profile['name']} likes {user_profile['favorite_task']} and feels {user_profile['emotion']}. {user_input}"
        inputs = self.tokenizer.encode(prompt, return_tensors='pt')
        outputs = self.model.generate(inputs, max_length=150, num_return_sequences=1)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)


class AdvancedLearningModule:
    def __init__(self, profile_path='user_profiles.json', hf_token=None):
        self.profile_path = profile_path
        self.emotion_module = EmotionalIntelligenceModule(hf_token)
        self.user_profiles = self.load_user_profiles()
        self.emotion_analysis = EmotionalAnalysis()
        self.reinforcement_agent = EmotionalRLAgent()  # Initialize the EmotionalRLAgent
        self.personalized_ai = PersonalizedAI()

    def load_user_profiles(self):
        """Load user profiles from a JSON file."""
        if os.path.exists(self.profile_path):
            with open(self.profile_path, 'r') as file:
                return json.load(file)
        return defaultdict(lambda: {'preferences': {}, 'emotions': []})
    
    def save_user_profiles(self):
        """Save user profiles to a JSON file."""
        with open(self.profile_path, 'w') as file:
            json.dump(self.user_profiles, file)
    
    def update_profile(self, username, key, value):
        """Update user profile with a new piece of data."""
        self.user_profiles[username][key] = value
        self.save_user_profiles()
    
    def track_emotion(self, username, emotion):
        """Track user emotions to detect patterns and improve responses."""
        self.user_profiles[username]['emotions'].append(emotion)
        self.save_user_profiles()
    
    def personalize_response(self, username, user_input):
        """Generate a personalized response based on the user's profile."""
        profile = self.user_profiles[username]
        emotion, _ = self.emotion_analysis.analyze_emotion(user_input)
        profile['emotion'] = emotion
        self.track_emotion(username, emotion)
        
        return self.personalized_ai.generate_response(user_input, profile)
    
    def handle_reinforcement_learning(self, user_input, user_reaction, username):
        """Use reinforcement learning to adjust actions based on emotional feedback."""
        emotion, _ = self.emotion_analysis.analyze_emotion(user_input)
        self.reinforcement_agent.run(emotion, user_reaction)
        return self.reinforcement_agent.get_action(self.reinforcement_agent.get_state(emotion))


class AdvancedAssistantAI:
    def __init__(self):
        self.knowledge_graph = KnowledgeGraph(settings.KNOWLEDGE_GRAPH_DB)
        hf_token = settings.HF_TOKEN
        self.learning_module = AdvancedLearningModule(hf_token=hf_token)
        self.singing_module = EllaSingingModule()
        self.emotional_intelligence = EmotionalIntelligenceModule(hf_token=hf_token)

    def handle_user_input(self, username, user_input):
        """Handle user's commands and input intelligently."""
        try:
            # Detect emotion and personalize response
            response = self.learning_module.personalize_response(username, user_input)
            print(response)
            
            # Reinforcement learning based on user feedback
            feedback = self.get_user_feedback()
            self.learning_module.handle_reinforcement_learning(user_input, feedback, username)

        except Exception as e:
            logging.error(f"Error handling command: {str(e)}")
    
    def get_user_feedback(self):
        """Simulate getting user feedback after the AI action."""
        return 'joy'  # Simulated feedback

    def sing_song(self):
        """Make the assistant sing a song."""
        self.singing_module.sing_from_sd_card()


# Add the Ella class as a wrapper for the AdvancedAssistantAI
class Ella:
    def __init__(self):
        self.advanced_ai = AdvancedAssistantAI()

    def interact(self, username, user_input):
        """Interface method for interacting with Ella."""
        return self.advanced_ai.handle_user_input(username, user_input)

    def sing(self):
        """Interface method for singing."""
        return self.advanced_ai.sing_song()