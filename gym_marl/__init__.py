from gym.envs.registration import  register

register(
    id="hunter-v0",
    entry_point="gym_marl.envs:HunterEnvironment_v0",
)
