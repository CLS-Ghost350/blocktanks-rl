import os

from sb3_plus import MultiOutputPPO, MultiOutputEnv

from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv
from stable_baselines3.common.evaluation import evaluate_policy

from BlocktanksEnv import BlocktanksEnv

import math

log_path = os.path.join("Training", "Logs")
model_path = os.path.join("Training", "SavedModels", "A")

#n_steps = 249

def create_env(seed):
    def init():
        env = BlocktanksEnv(seed=seed)
        env = MultiOutputEnv(env)
        return env

    return init


ENVS_NUM = 6

N_STEPS = 640

STEPS_PER_SAVE = N_STEPS * ENVS_NUM * 4 + 1

TOTAL_TIMESTEPS = int(100 * 1000 / STEPS_PER_SAVE) * STEPS_PER_SAVE + 1

# fps around 18 per env (108 total)

#env = BlocktanksEnv()
env = SubprocVecEnv([ create_env(seed) for seed in range(ENVS_NUM) ])

model = MultiOutputPPO("MultiOutputPolicy", env, verbose=1, n_steps=N_STEPS, tensorboard_log=log_path, learning_rate=lambda amountLeft: 0.0004 * amountLeft**2)

SAVES = int(TOTAL_TIMESTEPS / STEPS_PER_SAVE)
print("SAVES:", SAVES)

for i in range(SAVES):
    model.learn(total_timesteps=STEPS_PER_SAVE, log_interval=1)#1.75*1000*1000) #log_interval=100)
    model.save(model_path)
    print("Saved", i)