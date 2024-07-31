import os

from stable_baselines3 import PPO

from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv, VecNormalize
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.callbacks import CheckpointCallback

from stable_baselines3.common.monitor import Monitor

from BlocktanksEnv import BlocktanksEnv

import math

from constants import HyperParameters as Hp, LearningParameters as Lp

log_path = os.path.join("Training", "Logs")
model_path = os.path.join("Training", "SavedModels", "final")

def create_env(seed):
    def init():
        env = Monitor(BlocktanksEnv(seed=seed))
        return env

    return init

if __name__ == "__main__":
    #env = BlocktanksEnv()
    env = SubprocVecEnv([ create_env(seed) for seed in range(Lp.N_ENVS) ])
    env = VecNormalize(env, norm_obs=False, norm_reward=True)

    checkpoint_callback = CheckpointCallback(
        save_freq=Lp.SAVE_FREQ,
        save_path="./Training/SavedModels/",
        name_prefix="rl_model",
        save_replay_buffer=True,
        save_vecnormalize=True,
    )

    model = PPO(
        "CnnPolicy", 
        env, 
        verbose=1, 
        tensorboard_log=log_path, 
        learning_rate=Hp.LEARNING_RATE,
        n_steps=Hp.N_STEPS,
        batch_size=Hp.BATCH_SIZE,
        gamma=Hp.GAMMA
    )

    model.learn(
        log_interval=Lp.LOG_INTERVAL_STEPS // (Lp.N_ENVS * Hp.N_STEPS),
        total_timesteps=Lp.TOTAL_TIMESTEPS,
        callback=checkpoint_callback
    )


    model.save(model_path)