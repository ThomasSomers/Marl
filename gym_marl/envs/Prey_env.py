import gym
import numpy as np
from ray.rllib import MultiAgentEnv
from simulation.config import config
from simulation.environment import Environment
from simulation.model.prey import Prey


class Prey_Environment_v0(gym.Env, MultiAgentEnv):

    def __init__(self):
        self.action_space = gym.spaces.Discrete(4)
        self.observation_space = gym.spaces.Box(
            low=np.array([0, - config.SCREEN_WIDTH, -config.SCREEN_HEIGHT], dtype=np.float32), high=np.array(
                [config.PREY_MAX_AGE, config.SCREEN_WIDTH, config.SCREEN_HEIGHT], dtype=np.float32),
            shape=(3,))

        self.world = Environment()

    def reset(self):
        self.world.reset()

        return self.world.get_prey_obs()

    def step(self, action: dict):
        obs_dict = {}
        reward_dict = {}
        done_dict = {}

        all_done = False

        temp_agent_list = list(self.world.get_agent_list())

        if self.world.get_preys_amount() > 0:
            for agent in temp_agent_list:
                if isinstance(agent, Prey):
                    agent.step_env(action[agent.get_id()])
                else:
                    agent.step()
        else:
            all_done = True

        temp_agent_list = list(self.world.get_agent_list())

        for agent in temp_agent_list:
            if isinstance(agent, Prey):
                obs_dict[agent.get_id()] = np.array(agent.get_obs())
                rewardx, rewardy = agent.rel_post_closest_agent()
                reward_dict[agent.get_id()] = ((abs(rewardx) + abs(rewardy)) / (config.SCREEN_WIDTH))*config.PREY_DISTANCE_REWARD_SCALE
                done_dict[agent.get_id()] = not agent.get_alive()

                if not agent.get_alive():
                    self.world.remove_agent(agent)

        if self.world.get_hunters_amount() == 0:
            all_done = True

        done_dict['__all__'] = all_done

        return obs_dict, reward_dict, done_dict, {}