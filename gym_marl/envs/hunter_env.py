import gym
import numpy as np
from simulation.config import config
from simulation.environment import Environment
from simulation.model.hunter import Hunter
from simulation.model.prey import Prey
from ray.rllib.env.multi_agent_env import MultiAgentEnv

import pygame

blue = (0, 0, 255)
red = (255, 0, 0)


class HunterEnvironment_v0(gym.Env, MultiAgentEnv):

    def __init__(self):
        # UP = 0, DOWN = 1, LEFT = 2, RIGHT = 3, REPRODUCE_IF_POSSIBLE = 4
        self.action_space = gym.spaces.Discrete(5)

        # Age, Energy, Relative x closest prey, Relative y closest prey
        self.observation_space = gym.spaces.Box(
            low=np.array([0, 0, - config.SCREEN_WIDTH, -config.SCREEN_HEIGHT], dtype=np.float32), high=np.array(
                [config.HUNTER_MAX_AGE, float('inf'), config.SCREEN_WIDTH, config.SCREEN_HEIGHT]))

        self.world = Environment()

        pygame.init()
        self.gameDisplay = pygame.display.set_mode(
            (config.SCREEN_HEIGHT * config.PYGAME_SCALE, config.SCREEN_WIDTH * config.PYGAME_SCALE))
        pygame.display.set_caption("Predator/prey simulation")

    def reset(self):
        self.world.reset()

        return self.world.get_hunter_obs()

    def step(self, action: dict):
        obs_dict = {}
        reward_dict = {}
        done_dict = {}

        all_done = False

        iterable_agent_list = list(self.world.get_agent_list())

        if self.world.get_hunters_amount() > 0:
            for agent in iterable_agent_list:
                if isinstance(agent, Hunter):
                    agent.step_env(action[agent.get_id()])
                else:
                    agent.step()
        else:
            all_done = True

        iterable_agent_list = list(self.world.get_agent_list())

        for agent in iterable_agent_list:
            if isinstance(agent,Hunter):
                obs_dict[agent.get_id()] = np.array(agent.get_obs())
                #reward_dict[agent.get_id()] = (self.world.get_hunters_amount()) * config.TEAM_REWARD_SCALE + (agent.get_energy_level() * config.ENERGY_REWARD_SCALE )
                reward_dict[agent.get_id()] = self.world.get_hunters_amount()
                done_dict[agent.get_id()] = not agent.get_alive()

                if not agent.get_alive():
                    self.world.remove_agent(agent)


        done_dict['__all__'] = all_done

        return obs_dict, reward_dict, done_dict, {}

    #def render(self, mode='human'):
    #    self.gameDisplay.fill((0, 0, 0))
#
    #    for agent in self.env.get_agent_list():
#
    #        if isinstance(agent, Prey):
    #            pygame.draw.rect(self.gameDisplay, blue, (
    #                agent.get_x_pos() * config.PYGAME_SCALE, agent.get_y_pos() * config.PYGAME_SCALE,
    #                config.AGENT_SIZE * config.PYGAME_SCALE, config.AGENT_SIZE * config.PYGAME_SCALE))
    #        else:
    #            pygame.draw.rect(self.gameDisplay, red, (
    #                agent.get_x_pos() * config.PYGAME_SCALE, agent.get_y_pos() * config.PYGAME_SCALE,
    #                config.AGENT_SIZE * config.PYGAME_SCALE, config.AGENT_SIZE * config.PYGAME_SCALE))
#
    #    pygame.display.update()
