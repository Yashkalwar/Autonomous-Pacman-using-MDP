# Autonomous-Pacman-using-MDP
An autonomous Pacman implementation utilizing Markov Decision Processes (MDP) to enable intelligent navigation and decision-making. This project helps Pacman maximize rewards and avoid ghosts by making optimal moves based on the current state of the game environment.

# Pacman MDP Implementation

An autonomous Pacman agent utilizing Markov Decision Processes (MDP) to intelligently navigate mazes, maximize rewards, and avoid ghosts. This project applies reinforcement learning techniques to enable Pacman to make optimal decisions based on the current state of the game environment.

## Features

- **MDP-Based Decision Making**: Implements value iteration to calculate the utility of each state and determine the best action.
- **Dynamic Reward System**: Assigns rewards for different game elements, such as food, capsules, ghosts, and empty spaces.
- **Ghost Avoidance and Chasing**: Adjusts behavior based on ghost states, avoiding active ghosts and pursuing scared ones.
- **Probabilistic Movement**: Considers stochastic outcomes by modeling possible movements and their probabilities.
- **Adaptive Strategy**: Updates utilities and rewards in real-time based on the evolving game state.

## Getting Started

### Prerequisites

- Python 2.7
- Pacman AI projects from [UC Berkeley's AI Pacman](http://ai.berkeley.edu/project_overview.html)

## How It Works

- **Initialization**

  - The agent identifies walls, food, capsules, and initializes the game grid.
  - Rewards are assigned to different grid positions based on the presence of game elements.
  - This is how small and medium grid looks.


![image](https://github.com/user-attachments/assets/940d26ad-6137-4a04-a440-4698745cbe42)




![image](https://github.com/user-attachments/assets/f7f60ffc-4e99-458b-8d3b-be75a4129274)


- **Value Iteration**

  - Performs value iteration using the Bellman equation:
    \[
    U(s) = R(s) + \gamma \max_a \sum_{s'} P(s'|s,a) U(s')
    \]
  - Calculates the utility of each state over a number of iterations to account for future rewards.

- **Action Selection**

  - At each decision point, the agent:
    - Predicts possible next positions based on legal actions.
    - Calculates the expected utility for each action.
    - Incorporates factors like proximity to food and ghosts.
    - Selects the action with the highest expected utility.

- **Reward Updates**

  - Dynamically updates the reward grid considering:
    - **Food**: Positive reward to encourage consumption.
    - **Capsules**: Higher positive reward due to the power-up effect.
    - **Ghosts**: Negative reward to avoid active ghosts.
    - **Scared Ghosts**: Positive reward to chase and capture.
    - **Empty Spaces**: Small negative reward to encourage efficiency.

- **Ghost Handling**

  - Creates a "danger zone" around active ghosts, increasing the negative reward the closer Pacman is to a ghost.
  - Adjusts strategy when ghosts are scared, allowing Pacman to pursue them safely.

## Configuration Parameters

- `FOOD_REWARD`: Reward for consuming food pellets (e.g., `370.0`).
- `EMPTY_REWARD`: Penalty for empty moves to encourage efficiency (e.g., `-0.9`).
- `GHOST_REWARD`: Penalty for being close to an active ghost (e.g., `-500.0`).
- `CAPSULE_REWARD`: Reward for consuming a power capsule (e.g., `800.0`).
- `SCARED_GHOST_REWARD`: Reward for capturing a scared ghost (e.g., `5000.0`).
- `discount`: Discount factor for future rewards in value iteration (e.g., `0.85`).
- `iteration_count`: Number of iterations for value iteration to converge (e.g., `15`).

## Project Structure

- `MDPAgent.py`: Main agent implementing the MDP logic.
- `README.md`: Project documentation.
- Additional files and folders as required by the Pacman framework.

## References

This project was inspired by and references several implementations and explanations:

1. **Markovian Pac-Man by Prateek Mishra**

   [Markovian Pac-Man Medium Article](https://prateek-mishra.medium.com/markovian-pac-man-8dd212c5a35c)

2. **Markov Decision Process Value Iteration by Ngao7**

   [Value Iteration Medium Article](https://medium.com/@ngao7/markov-decision-process-value-iteration-2d161d50a6ff)

3. **Udacity Pacman Problem Explanation**

   [Pacman Problem Video](https://youtu.be/3DxXFWsHpvU)

4. **CSE573 Pacman MDP**

   [CSE573 Pacman MDP Assignment](https://courses.cs.washington.edu/courses/cse573/17wi/pacman/ps3/mdp.html)

5. **Eamansour's Pacman MDP Agent**

   [Eamansour's GitHub Repository](https://github.com/eamansour/pacman/blob/main/mdpAgents.py)

6. **DarrenSandhu's Pacman MDP Implementation**

   [DarrenSandhu's GitHub Repository](https://github.com/DarrenSandhu/Pacman-Markov-Decision-Process)

## License

This project is based on the Pacman AI projects developed at UC Berkeley.

**Attribution Information:**

The Pacman AI projects were developed at UC Berkeley. The core projects and autograders were primarily created by John DeNero and Dan Klein. Student side autograding was added by Brad Miller, Nick Hay, and Pieter Abbeel.

## Author

**Yash Kalwar**

- MSc Artificial Intelligence
