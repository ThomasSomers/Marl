from simulation.config import config
from simulation.model.prey import Prey
from simulation.model.hunter import Hunter
from simulation.statistics_logger.statistics_logger import StatisticsLogger
import numpy as np

class Environment():

    def __init__(self):
        self.agent_list = []

        self.seed()

    def seed(self):
        for i in range(config.START_AMOUNT_PREYS):
            self.add_agent(Prey(environment=self, id="prey_" + str(StatisticsLogger.preys_amount)))

        for j in range(config.START_AMOUNT_HUNTERS):
            self.add_agent(Hunter(environment=self, id= "hunter_" + str(StatisticsLogger.hunters_amount)))


    def add_agent(self, agent):
        self.agent_list.append(agent)

    def remove_agent(self, agent):
        self.agent_list.remove(agent)

    def get_agent_list(self):
        return self.agent_list

    def set_agent_list(self, agent_list):
        self.agent_list = agent_list

    def get_hunters_amount(self):
        counter = 0

        for agent in self.agent_list:
            if isinstance(agent, Hunter):
                counter += 1
        return counter

    def get_preys_amount(self):
        counter = 0

        for agent in self.agent_list:
            if isinstance(agent, Prey):
                counter += 1
        return counter

    def reset(self):
        StatisticsLogger.reset()
        self.agent_list = []

        self.seed()

    def get_hunter_obs(self):
        obs = {}

        for agent in self.agent_list:
            if isinstance(agent, Hunter):
                rel_x, rel_y = agent.rel_post_closest_agent()
                obs[agent.get_id()] = np.array([agent.age, agent.energy_level, rel_x, rel_y ])


        return obs

    def get_prey_obs(self):
        obs = {}

        for agent in self.agent_list:
            if isinstance(agent,Prey):
                rel_x, rel_y = agent.rel_post_closest_agent()
                obs[agent.get_id()] = np.array([agent.age, rel_x, rel_y])
        return obs



