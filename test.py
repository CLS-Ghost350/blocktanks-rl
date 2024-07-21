import os

from stable_baselines3 import PPO

model_path = os.path.abspath(os.path.join("Training", "SavedModels", "A"))
model = PPO.load(model_path)
