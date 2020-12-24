from random import uniform
from simulation.model.agent import Agent
from simulation.config import config
from simulation.statistics_logger.statistics_logger import StatisticsLogger

class Prey(Agent):

    def __init__(self, environment, id):
        super().__init__(config.PREY_MAX_AGE, environment, id)
        self.prey_birt_rate = config.PREY_BIRTH_RATE

        StatisticsLogger.log_new_prey()

    def move_agent(self):
        super().move_agent()

    def should_reproduce(self):
        if uniform(0, 1) < self.prey_birt_rate:
            self.reproduce()

    def reproduce(self):
        self.environment.add_agent(Prey(environment=self.environment, id ="prey_" + str(StatisticsLogger.preys_amount)))
        StatisticsLogger.log_new_prey()

    def should_die(self):
        if self.age >= self.get_max_age():
            return True
        return False

    def die(self):
        self.alive = False
        StatisticsLogger.log_dead_prey()

    def get_class(self):
        return Prey

    def step(self):
        if self.should_die():
            self.die()
        else:
            self.move_agent()
            self.should_reproduce()
        self.age += 1


    # UP = 0, DOWN = 1, LEFT = 2, RIGHT = 3
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

        self.age += 1

        rel_x, rel_y = self.rel_post_closest_agent()
        obs = [self.age, rel_x, rel_y, self.alive]

        return obs
