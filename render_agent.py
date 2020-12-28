import ray
import json
import gym
import numpy as np
from ray.tune.registry import register_env

from gym_marl.envs.hunter_env import HunterEnvironment_v0

from ray import tune
from ray.rllib.models import ModelCatalog
from dqn import DQNTrainer, DQNModel

if __name__ == "__main__":

    # Settings
    folder = "/home/thomas/ray_results/DQNAlgorithm/DQNAlgorithm_hunter-v0_a2081_00000_0_2020-12-28_09-21-06"
    select_env="hunter-v0"
    register_env(select_env, lambda config: HunterEnvironment_v0())
    checkpoint = 221
    num_episodes = 1

    # Def env
    env = gym.make(select_env)
    print(folder + "/params.json")

    ray.init()
    ModelCatalog.register_custom_model("DQNModel", DQNModel)

    # Load config
    with open(folder + "/params.json") as json_file:
        config = json.load(json_file)
    trainer = DQNTrainer(env=select_env,config=config)

    # Restore checkpoint
    trainer.restore(folder + "/checkpoint_{}/checkpoint-{}".format(checkpoint, checkpoint))


    avg_reward = 0
    for episode in range(num_episodes):
        step = 0
        total_reward = 0
        done = False
        observation = env.reset()

        while not done:
            step += 1
            env.render()
            print(observation)
            action, _, _ = trainer.get_policy().compute_actions([observation], [])
            observation, reward, done, info = env.step(action[0])
            total_reward += reward
        print("episode {} received reward {} after {} steps".format(episode, total_reward, step))
        avg_reward += total_reward
    print('avg reward after {} episodes {}'.format(avg_reward/num_episodes , num_episodes))
    env.close()
    del trainer
