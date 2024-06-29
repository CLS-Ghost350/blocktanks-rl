import os
from SimpleEnv.BlocktanksEnv import BlocktanksEnv
from stable_baselines3 import A2C, PPO
from stable_baselines3.common.vec_env import DummyVecEnv, VecFrameStack
from gym.spaces import MultiDiscrete, Box, Dict
from keyboard import is_pressed

manual = True

model_path = os.path.abspath(os.path.join("Training", "SavedModels", "A"))
#model_path = os.path.abspath(os.path.join("Models", "PPO1"))

env = BlocktanksEnv(render=True,seed=2)

#env = DummyVecEnv([ lambda: env ])
#env = VecFrameStack(env, 4, channels_order='last')
#model = PPO.load(model_path)

episodes = 5

import cv2

for episode in range(1, episodes + 1):
    obs = env.reset()
    done = False

    while not done:
        #env.render()

        if not manual:
            action, _states = model.predict(obs)
            print(action)

        else:
            action = Dict({ "keys": [1, 1]})
            if is_pressed('w'): action[0] += 1
            if is_pressed('s'): action[0] -= 1
            if is_pressed('a'): action[1] -= 1
            if is_pressed('d'): action[1] += 1
        #action = [1,2]

        obs, reward, done, info = env.step(action)

        #cv2.imshow("AI View", obs)
        #cv2.waitKey()
