
class StatisticsLogger:
    preys_amount = 0
    hunters_amount = 0
    preys_reproduced = 0
    hunters_reproduced = 0
    preys_died = 0
    hunters_died = 0
    preys_eaten = 0
    steps_amount = 0


    @staticmethod
    def log_new_prey():
        StatisticsLogger.preys_amount += 1

    @staticmethod
    def log_new_hunter():
        StatisticsLogger.hunters_amount += 1

    @staticmethod
    def log_reproduce_prey():
        StatisticsLogger.preys_reproduced += 1

    @staticmethod
    def log_reproduce_hunter():
        StatisticsLogger.hunters_reproduced += 1

    @staticmethod
    def log_dead_prey():
        StatisticsLogger.preys_amount -= 1

    @staticmethod
    def log_dead_hunter():
        StatisticsLogger.hunters_amount -= 1

    @staticmethod
    def log_eaten_prey():
        StatisticsLogger.preys_amount -= 1
        StatisticsLogger.preys_eaten += 1

    @staticmethod
    def log_step():
        StatisticsLogger.steps_amount += 1

    @staticmethod
    def reset():
        StatisticsLogger.preys_amount = 0
        StatisticsLogger.hunters_amount = 0
        StatisticsLogger.preys_reproduced = 0
        StatisticsLogger.hunters_reproduced = 0
        StatisticsLogger.preys_died = 0
        StatisticsLogger.hunters_died = 0
        StatisticsLogger.preys_eaten = 0
        StatisticsLogger.steps_amount = 0








