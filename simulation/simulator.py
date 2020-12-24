from simulation.environment import Environment
from simulation.statistics_logger.statistics_logger import StatisticsLogger
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pygame
from simulation.model.prey import Prey
from simulation.config import config

x = []
yHunter = []
yPrey = []

blue = (0, 0, 255)
red = (255, 0, 0)


class Simulator:

    def __init__(self):
        self.env = Environment()
        pygame.init()

        self.gameDisplay = pygame.display.set_mode(
            (config.SCREEN_HEIGHT * config.PYGAME_SCALE, config.SCREEN_WIDTH * config.PYGAME_SCALE))
        pygame.display.set_caption("Predator/prey simulation")

    def start_simulation(self):
        ani = FuncAnimation(plt.gcf(), animate)

        while len(self.env.get_agent_list()) > 0:
            self.gameDisplay.fill((0, 0, 0))
            for agent in self.env.get_agent_list():
                agent.step()

                if agent.alive == False:
                    self.env.remove_agent(agent)

                if isinstance(agent, Prey):
                    pygame.draw.rect(self.gameDisplay, blue, (
                    agent.get_x_pos() * config.PYGAME_SCALE, agent.get_y_pos() * config.PYGAME_SCALE,
                    config.AGENT_SIZE * config.PYGAME_SCALE, config.AGENT_SIZE * config.PYGAME_SCALE))
                else:
                    pygame.draw.rect(self.gameDisplay, red, (
                    agent.get_x_pos() * config.PYGAME_SCALE, agent.get_y_pos() * config.PYGAME_SCALE,
                    config.AGENT_SIZE * config.PYGAME_SCALE, config.AGENT_SIZE * config.PYGAME_SCALE))

            StatisticsLogger.log_step()

            plt.tight_layout()
            plt.draw()
            plt.pause(0.001)

            pygame.display.update()

        pygame.quit()
        quit()

    def reset(self):
        self.env.reset()

    def get_env(self):
        return self.env


def animate(i):
    x.append(StatisticsLogger.steps_amount)
    yHunter.append(StatisticsLogger.hunters_amount)
    yPrey.append(StatisticsLogger.preys_amount)

    plt.cla()
    plt.plot(x, yHunter, label='# hunters')
    plt.plot(x, yPrey, label='# preys')
    plt.legend(loc='upper left')
    plt.tight_layout()
