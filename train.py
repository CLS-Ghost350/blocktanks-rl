import os

from sb3_plus import MultiOutputPPO

from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv
from stable_baselines3.common.evaluation import evaluate_policy

from BlocktanksEnv import BlocktanksEnv

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
    env = BlocktanksEnv()
    #env = SubprocVecEnv([ create_env(seed) for seed in range(envs_num) ])

    model = MultiOutputPPO("MultiOutputPolicy", env, verbose=1, tensorboard_log=log_path, learning_rate=lambda amountLeft: 0.0004 * amountLeft**2)#, learning_rate=0.5)#, n_steps=3500)

    model.learn(total_timesteps=150)#1.75*1000*1000) #log_interval=100)
    model.save(model_path)