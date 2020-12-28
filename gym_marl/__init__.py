from gym.envs.registration import register

# register(
#     id="hunter-v0",
#     entry_point="gym_marl.envs:HunterEnvironment_v0",
# )

register(
    id="prey-v0",
    entry_point="gym_marl.envs:Prey_Environment_v0",
    max_episode_steps = 200000
)
