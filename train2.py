import os
from SimpleEnv.BlocktanksGame import BlocktanksEnv
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv
from stable_baselines3.common.evaluation import evaluate_policy

import math

log_path = os.path.join("Training", "Logs")
model_path = os.path.join("Training", "SavedModels", "A")

#n_steps = 249

def create_env(seed):
    def init():
        return BlocktanksEnv(seed=seed)

    return init

envs_num = 6

if __name__ == "__main__":
    #env = BlocktanksEnv()
    env = SubprocVecEnv([ create_env(seed) for seed in range(envs_num) ])

    model = PPO.load(model_path, env=env, learning_rate=0.0001)

    model.learn(total_timesteps=2*1000*1000) #log_interval=100)
    model.save(model_path)