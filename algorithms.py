import random
from collections import defaultdict
import numpy as np

class DeepQNetwork:
    def __init__(self):
        self.q_table = defaultdict(lambda: defaultdict(float))  # State-action value function
        self.learning_rate = 0.1
        self.discount_factor = 0.95
        self.exploration_rate = 1.0
        self.exploration_decay = 0.99
        self.min_exploration_rate = 0.01  # Added minimum exploration rate
        self.alpha_decay = 0.995  # For dynamic learning rate decay
        self.episode_rewards = []  # Track rewards per episode

    def choose_action(self, state, available_actions):
        """Choose action using an epsilon-greedy approach with a dynamic exploration rate."""
        if random.random() < self.exploration_rate:
            return random.choice(available_actions)  # Explore
        return max(self.q_table[state], key=self.q_table[state].get, default=random.choice(available_actions))  # Exploit

    def update_q_value(self, state, action, reward, next_state):
        """Update Q-value based on temporal difference learning."""
        best_next_action = max(self.q_table[next_state], key=self.q_table[next_state].get, default=None)
        td_target = reward + (self.discount_factor * self.q_table[next_state][best_next_action]) if best_next_action else reward
        td_error = td_target - self.q_table[state][action]
        self.q_table[state][action] += self.learning_rate * td_error  # Update the Q-value

    def decay_exploration(self):
        """Decay exploration rate over time, ensuring a minimum exploration rate."""
        self.exploration_rate = max(self.min_exploration_rate, self.exploration_rate * self.exploration_decay)

    def dynamic_learning_rate_decay(self):
        """Decay the learning rate over time to converge more effectively."""
        self.learning_rate *= self.alpha_decay

    def track_episode_rewards(self, total_reward):
        """Track the cumulative reward for an episode."""
        self.episode_rewards.append(total_reward)

    def reset_episode(self):
        """Reset for a new episode and decay exploration rate."""
        self.decay_exploration()
        self.dynamic_learning_rate_decay()

    def get_average_reward(self, window_size=100):
        """Calculate the average reward over a specified window of episodes."""
        if len(self.episode_rewards) < window_size:
            return np.mean(self.episode_rewards)
        return np.mean(self.episode_rewards[-window_size:])