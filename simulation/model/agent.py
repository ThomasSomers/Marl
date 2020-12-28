import random
from simulation.config import config

class Agent:

    def __init__(self, max_age, environment, id):
        self.age = 0
        self.max_age = max_age
        self.environment = environment
        self.id = id
        self.alive = True

        self.x_pos = random.randint(0, config.SCREEN_WIDTH)
        self.y_pos = random.randint(0, config.SCREEN_HEIGHT)

    def get_age(self):
        return self.age

    def get_max_age(self):
        return self.max_age

    def get_x_pos(self):
        return self.x_pos

    def get_y_pos(self):
        return self.y_pos

    def get_alive(self):
        return self.alive

    def check_window_size(self, x, y):
        if (x > 0 and
                (x + config.AGENT_SIZE) < config.SCREEN_WIDTH and
                y > 0 and
                (y + config.AGENT_SIZE) < config.SCREEN_HEIGHT):
            return True
        else:
            return False

    def move_agent(self):
        # UP = 0, DOWN = 1, LEFT = 2, RIGHT = 3
        random_direction = random.randint(0, 3)

        if random_direction == 0:
            if self.check_window_size(self.x_pos, self.y_pos + 1):
                self.y_pos += 1
        elif random_direction == 1:
            if self.check_window_size(self.x_pos, self.y_pos - 1):
                self.y_pos -= 1
        elif random_direction == 2:
            if self.check_window_size(self.x_pos - 1, self.y_pos):
                self.x_pos -= 1
        elif random_direction == 3:
            if self.check_window_size(self.x_pos + 1, self.y_pos):
                self.x_pos += 1

    def should_reproduce(self):
        pass

    def reproduce(self):
        pass

    def get_obs(self):
        pass

    def should_die(self):
        pass

    def step(self):
        pass

    def get_id(self):
        return self.id

    def step_env(self, action):
        pass

    # ClassToFind: Hunter, Prey
    def rel_post_closest_agent(self):
        tmp_distance = float('inf')

        tmp_x = float('inf')
        tmp_y = float('inf')

        for agent in self.environment.agent_list:
            if not isinstance(agent, self.__class__):
                x_diff = agent.get_x_pos() - self.get_x_pos()
                y_diff = agent.get_y_pos() - self.get_y_pos()
                distance = ((x_diff ** 2) + (y_diff ** 2)) ** 0.5
                if distance < tmp_distance:
                    tmp_distance = distance
                    tmp_x = x_diff
                    tmp_y = y_diff

        if tmp_x == float('inf') and tmp_y == float('inf'):
            tmp_x = config.SCREEN_WIDTH
            tmp_y = config.SCREEN_HEIGHT

        return tmp_x, tmp_y

    def die(self):
        pass

    def get_class(self):
        pass

    def near_other_agent(self, agent):
        if (self.get_x_pos() <= agent.get_x_pos() + config.AGENT_SIZE and
                self.get_x_pos() + config.AGENT_SIZE >= agent.get_x_pos() and
                self.get_y_pos() <= agent.get_y_pos() + config.AGENT_SIZE and
                self.get_y_pos() + config.AGENT_SIZE >= agent.get_y_pos() and
                self.get_x_pos() != agent.get_x_pos() and
                self.get_y_pos() != agent.get_y_pos()
        ):
            return True
        return False
