from transformers import pipeline
from collections import defaultdict

class EmotionalIntelligenceModule:
    def __init__(self, hf_token, score_threshold=0.6):
        # Using a sentiment analysis model to detect emotional tone
        self.emotion_analyzer = pipeline(
            'sentiment-analysis',
            model='mrm8488/t5-base-finetuned-emotion',
            token=hf_token  # Handling token using the newer parameter name
        )
        self.user_emotional_state = defaultdict(list)  # Store emotional states over time
        self.score_threshold = score_threshold  # Minimum score confidence threshold for emotions

    def analyze_emotion(self, text):
        try:
            # Analyzing the user's input to detect emotions
            emotion_result = self.emotion_analyzer(text)
            if emotion_result and emotion_result[0]['score'] >= self.score_threshold:
                emotion = emotion_result[0]['label']
                score = emotion_result[0]['score']
                return emotion, score
            else:
                # If confidence is too low, fallback to "neutral"
                return "neutral", 1.0
        except Exception as e:
            return "neutral", 1.0  # Default to neutral if there's an issue

    def adjust_response(self, emotion, response, username=None):
        """
        Adjust Ella's response based on the detected emotion. Optionally includes user-specific responses.
        """
        adjusted_response = response
        if emotion == "joy":
            adjusted_response += " I'm glad you're feeling good!"
        elif emotion == "anger":
            adjusted_response = "I understand you're upset. Let's work through this."
        elif emotion == "sadness":
            adjusted_response = "I'm here for you. Would you like to talk about what's bothering you?"
        elif emotion == "fear":
            adjusted_response = "Don't worry, everything will be fine. I'm here to help."
        elif emotion == "surprise":
            adjusted_response = "Wow, something unexpected happened! How can I assist?"

        # Add user-specific customizations
        if username:
            adjusted_response += f" {username}, I'm always here if you need to talk."

        return adjusted_response

    def track_emotion(self, username, emotion):
        """
        Track emotional state of the user over time, avoiding consecutive duplicates.
        """
        if self.user_emotional_state[username]:
            last_emotion = self.user_emotional_state[username][-1]
            if last_emotion != emotion:
                self.user_emotional_state[username].append(emotion)
        else:
            self.user_emotional_state[username].append(emotion)

    def suggest_help_based_on_emotion(self, username):
        """
        Based on the emotional history of the user, suggest assistance.
        """
        if username not in self.user_emotional_state:
            return None

        emotions = self.user_emotional_state[username]
        sadness_count = emotions.count("sadness")
        anger_count = emotions.count("anger")
        fear_count = emotions.count("fear")

        # Suggest help based on a pattern of emotions
        if sadness_count > 2:
            return "It seems you've been feeling down lately. Maybe a comforting song or chat would help?"
        elif anger_count > 2:
            return "I see you've been upset recently. A relaxing activity or deep breathing could be helpful."
        elif fear_count > 2:
            return "It looks like you've been anxious. Do you want to try some calming techniques?"

        # Offer generic advice if no significant pattern is detected
        return None

    def get_emotional_history(self, username):
        """
        Return the emotional history of the user.
        """
        return self.user_emotional_state.get(username, [])