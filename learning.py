from transformers import pipeline, logging as hf_logging
from core.knowledge_graph import KnowledgeGraph
from config import settings  # Import settings for hf_token
import logging
import requests

logging.basicConfig(filename='learning.log', level=logging.INFO)
hf_logging.set_verbosity_error()  # Suppresses HF model loading warnings

class LearningModule:
    def __init__(self, db_path):
        self.knowledge_graph = KnowledgeGraph(db_path)
        self.hf_token = settings.HF_TOKEN  # Fetching the token from settings

        # Validate HF token
        if not self._validate_hf_token(self.hf_token):
            raise ValueError("Invalid Hugging Face token provided.")

        # Initialize models
        self.knowledge_model = pipeline('zero-shot-classification', use_auth_token=self.hf_token)
        self.nlp_model = pipeline('text-generation', model='gpt2', use_auth_token=self.hf_token)

    def _validate_hf_token(self, hf_token):
        """Validates the Hugging Face token by making a request to the HF API."""
        headers = {"Authorization": f"Bearer {hf_token}"}
        response = requests.get("https://huggingface.co/api/whoami", headers=headers)
        
        if response.status_code == 200:
            logging.info("Hugging Face token validated successfully.")
            return True
        else:
            logging.error(f"Failed to validate HF token: {response.status_code}")
            return False

    def learn(self, text):
        """Learn new knowledge by classifying text and storing it in the knowledge graph."""
        try:
            result = self.knowledge_model(text, candidate_labels=["knowledge", "information", "task"])
            concept = result['labels'][0]
            data = text
            self.knowledge_graph.store_knowledge(concept, [], data)
            logging.info(f"Learned new knowledge: {concept}")
        except Exception as e:
            logging.error(f"Error learning new knowledge: {str(e)}")

    def generate_response(self, text):
        """Generate a natural language response based on input text."""
        try:
            response = self.nlp_model(text, max_length=50)
            return response[0]['generated_text']
        except Exception as e:
            logging.error(f"Error generating response: {str(e)}")
            return "I'm sorry, I couldn't process that."