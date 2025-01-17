'''
using Q-Learning reinf. learning to build tunk agent
'''

import numpy as np
import random

# Parameters
alpha = 0.1  # Learning rate
gamma = 0.9  # Discount factor
epsilon = 0.1  # Exploration rate
num_episodes = 1000

# Initialize Q-Table
state_space_size = 100  # Adjust based on game complexity
action_space_size = 5   # Draw Deck, Draw Discard, Drop, Knock, Spread
Q = np.zeros((state_space_size, action_space_size))

# Simulate the game
for episode in range(num_episodes):
    state = get_initial_state()  # Define this based on your game
    done = False
    
    while not done:
        # Choose action
        if random.uniform(0, 1) < epsilon:
            action = random.choice(range(action_space_size))  # Explore
        else:
            action = np.argmax(Q[state])  # Exploit
        
        # Perform action and observe outcome
        next_state, reward, done = step(state, action)  # Define step function
        
        # Update Q-Table
        Q[state, action] = Q[state, action] + alpha * (reward + gamma * np.max(Q[next_state]) - Q[state, action])
        
        state = next_state

# Evaluate the trained agent
evaluate_agent(Q)