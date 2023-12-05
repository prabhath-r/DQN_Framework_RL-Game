# file to configure settings for the DQN agent and environment
# this acts file to manage the hyperparameters that decide the performance of our RL agent

# GAME_ENV = 'Breakout'
# GAME_ENV = 'ChromeDino'

GAME_ENV = None #placeholder
STATE_SIZE = (1, 80, 80)  # image state size (channels, height, width)

GAMMA = 0.99  # discount factor
EPSILON = 1.0  # starting value of epsilon for the epsilon-greedy policy
EPSILON_MIN = 0.01  # Minimum value of epsilon as learning progress
EPSILON_DECAY = 0.995  # factor per episode for decreasing epsilon
LEARNING_RATE = 0.001  # learning rate
MEMORY_SIZE = 1000000  # replay buffer size
BATCH_SIZE = 32  # training batch size

NUM_EPISODES = 10000
