from simulation.model.agent import Agent
from simulation.model.prey import Prey
from simulation.config import config
from simulation.statistics_logger.statistics_logger import StatisticsLogger


class Hunter(Agent):

    def __init__(self, environment, id):
        super().__init__(config.PREY_MAX_AGE, environment, id)
        self.energy_level = config.HUNTER_START_ENERGY
        self.energy_to_reproduce = config.HUNTER_ENERGY_TO_REPRODUCE
        self.energy_per_eaten_prey = config.HUNTER_ENERGY_PER_PREY_EATEN

        StatisticsLogger.log_new_hunter()

    def move_agent(self):
        super().move_agent()

    def should_reproduce(self):
        if self.energy_level >= self.energy_to_reproduce:
            self.reproduce()

    def reproduce(self):
        self.energy_level -= self.energy_to_reproduce
        self.environment.add_agent(
            Hunter(environment=self.environment, id="hunter_" + str(StatisticsLogger.hunters_amount)))
        StatisticsLogger.log_new_hunter()

    def should_die(self):
        if self.age >= self.get_max_age() or self.energy_level <= 0:
            return True
        return False

    def die(self):
        self.alive = False
        StatisticsLogger.log_dead_hunter()

    def can_eat(self):
        for agent in self.environment.agent_list:
            if isinstance(agent, Prey):
                if self.near_other_agent(agent):
                    self.eat(agent)

    def eat(self, prey_to_eat):
        self.energy_level += self.energy_per_eaten_prey
        self.environment.remove_agent(prey_to_eat)
        StatisticsLogger.log_eaten_prey()

    def get_class(self):
        return Hunter

    def step(self):
        if self.should_die():
            self.die()
        else:
            self.move_agent()
            self.should_reproduce()
            self.can_eat()

        self.energy_level -= 1
        self.age += 1

    # UP = 0, DOWN = 1, LEFT = 2, RIGHT = 3, REPRODUCE = 4
    def step_env(self, action):
        if action == 0:
            if self.check_window_size(self.x_pos, self.y_pos - 1):
                self.y_pos -= 1
        elif action == 1:
            if self.check_window_size(self.x_pos, self.y_pos + 1):
                self.y_pos += 1
        elif action == 2:
            if self.check_window_size(self.x_pos - 1, self.y_pos):
                self.x_pos -= 1
        elif action == 3:
            if self.check_window_size(self.x_pos + 1, self.y_pos):
                self.x_pos += 1
        elif action == 4:
            if self.energy_level >= self.energy_to_reproduce:
                self.reproduce()

        self.can_eat()

        self.energy_level -= 1
        self.age += 1

        if self.should_die():
            self.die()

        rel_x, rel_y = self.rel_post_closest_agent()

        return self.age, self.energy_level, rel_x, rel_y
