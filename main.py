import gym
import numpy as np
import time
from turtle_env import StayAwayFromCenterEnvironment, DontTouchTheWallEnvironment, HitThePointChallange, \
    VerticalMovementChallange
from turtle_agent import TurtleQTableAgent
from neural_nework_agent import NeuralNetworkAgent
import matplotlib.pyplot as plt

def main():
    env = HitThePointChallange()
    agent = NeuralNetworkAgent(env.observation_space, env.action_space)
    train_data = []
    DISPLAY_GAMES = 1000
    game_performance = []
    try:
        reward_history = []
        start_time = time.time()
        for game_index in range(100001):
            if game_index % DISPLAY_GAMES == 0:
                env.enable_draw()
            else:
                env.disable_draw()
            env.reset()
            total_reward = 0
            action = env.action_space.sample()
            previous_observation = None
            feedbacks = []
            for step_index in range(25):
                env.render()
                observation, reward, done, info = env.step(action)
                total_reward += reward
                if previous_observation:
                    feedbacks.append((previous_observation, action, observation, reward))
                if done:
                    break
                action = agent.act(observation)
                previous_observation = observation
            if len(feedbacks) > 128:
                agent.feedback(feedbacks)
            reward_history.append(total_reward)
            if game_index % 100 == 0:
                print(f'Round {game_index}, avg. reward: {np.average(reward_history)} (took {time.time() - start_time}s)')
                reward_history = []
                start_time = time.time()
            if game_index % DISPLAY_GAMES == 0:
                env.save_to_file(f'images/turtle_{game_index}.ps')
            game_performance.append(total_reward)
    except KeyboardInterrupt:
        print('Interrupted, showing graph')
    c = np.cumsum(np.insert(game_performance, 0, 0))
    performace_moving_avg = (c[100:] - c[:-100]) / float(100)
    plt.plot(performace_moving_avg)
    plt.show()


if __name__ == '__main__':
    main()
