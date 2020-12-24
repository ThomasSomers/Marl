import gym
import numpy as np
from simulation.config import config
from simulation.environment import Environment
from simulation.model.hunter import Hunter
from ray.rllib.env.multi_agent_env import MultiAgentEnv


class HunterEnvironment_v0(gym.Env, MultiAgentEnv):

    def __init__(self):
        # UP = 0, DOWN = 1, LEFT = 2, RIGHT = 3, REPRODUCE_IF_POSSIBLE = 4
        self.action_space = gym.spaces.Discrete(5)

        # Age, Energy, Relative x closest prey, Relative y closest prey
        self.observation_space = gym.spaces.Box(
            low=np.array([0, 0, - config.SCREEN_WIDTH, -config.SCREEN_HEIGHT], dtype=np.float32), high=np.array(
                [config.HUNTER_MAX_AGE, float('inf'), config.SCREEN_WIDTH, config.SCREEN_HEIGHT], dtype=np.float32),
            shape=(4,))

        self.world = Environment()

    def reset(self):
        self.world.reset()

        return self.world.get_hunter_obs()

    def step(self, action: dict):

        print(str(action))
        for agent in self.world.get_agent_list():
            if isinstance(agent, Hunter):
                print(agent.get_id() + " " + str(agent.get_alive()))

        obs_dict = {}
        reward_dict = {}
        done_dict = {}

        all_done = False

        iterable_agent_list = self.world.get_agent_list()

        if self.world.get_hunters_amount() > 0:
            for agent in iterable_agent_list:
                if isinstance(agent, Hunter):
                    obs = np.array(agent.step_env(action[agent.get_id()]))
                    obs_dict[agent.get_id()] = obs
                    reward_dict[agent.get_id()] = 0
                    done_dict[agent.get_id()] = not agent.get_alive()

                    if not agent.get_alive():
                        self.world.remove_agent(agent)
                else:
                    agent.step()
        else:
            all_done = True

        done_dict['__all__'] = all_done

        return obs_dict, reward_dict, done_dict, {}
