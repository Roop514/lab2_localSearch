from gymnasium.envs.classic_control.cartpole import CartPoleEnv
from agent import CartPoleAgent
import numpy as np
np.set_printoptions(precision=2)


def test_agent(parameters, render=False):
    """
    This function tests a CartPoleAgent with the given weights.
    The agent is tested over 10 episodes, and the total number of steps achieved is returned.
    """

    max_steps_per_episode = 500
    cumulative_reward = 0

    for rep in range(10):
        agent = CartPoleAgent(parameters)
        env = CartPoleEnv(render_mode="human" if render else None)
        

        observation, info = env.reset()

        for step in range(max_steps_per_episode):
            action = agent.get_action(observation)
            observation, reward, terminated, truncated, info = env.step(action)
            cumulative_reward += reward
            if terminated or truncated:
                break

    print(f'tested parameters: {parameters}, cumulative reward: {cumulative_reward}')
    return cumulative_reward



# watch how an agent with randomly-initialized parameters does:
#test_agent(parameters=np.random.uniform(-1, 1, size=5), render=True)


# Write a search to find the best parameters for the CartPoleAgent.

def hill_climbing(parameters, step_size=1.0, num_iterations=40):
    """
     One hill-climbing run: starts from 'parameters' and taes num_iterations' random steps, 
     keeping any neighbour that inproves on the current best.

    """ 
    current_parameters = parameters
    current_reward = test_agent(current_parameters)

    rewards = [current_reward]
    
    
    for step in range (num_iterations):
        neighbour = current_parameters + np.random.uniform(-step_size, step_size, 5)
        neighbour_reward = test_agent(neighbour)
        
        rewards.append(neighbour_reward)
        
        if neighbour_reward > current_reward:
            current_parameters = neighbour
            current_reward = neighbour_reward


    return current_parameters, current_reward, rewards   
def hill_climbing_with_restarts(num_restarts=5, step_size=1.0, num_interations=40):
    """
    Runs hill_climbing multiple times from different random starting points,
    and keeps the best result found across all restarts. This avoids getting
    stuck in a single bad region of parameter space.

    """
    best_parameters = None
    best_reward = -1
    all_rewards = []


    for restart in range(num_restarts):
        start = np.random.uniform(-1, 1, size=5)
        parameters, reward, rewards = hill_climbing(start, step_size, num_iterations)


        all_rewards.extend(rewards)

        if reward > best_reward:
            best_parameters = parameters
            best_reward = rewward

    return best_parameters, best_reward, all_rewards


best_parameters, best_reward, rewards = hill_climbing_with_restarts(num_restarts=5, step_size=1.0, num_interations=40)

print(best_parameters)
print(best_reward)




        
   


