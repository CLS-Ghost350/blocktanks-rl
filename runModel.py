import os
import math

from sb3_plus import MultiOutputPPO

from stable_baselines3.common.vec_env import DummyVecEnv, VecFrameStack
from gym.spaces import MultiDiscrete, Box, Dict
from keyboard import is_pressed
from pygame import mouse

from BlocktanksEnv import BlocktanksEnv

manual = True

env = BlocktanksEnv(render=True,seed=2)

if not manual:
    model_path = os.path.abspath(os.path.join("Training", "SavedModels", "A"))
    #model_path = os.path.abspath(os.path.join("Models", "PPO1"))

    #env = DummyVecEnv([ lambda: env ])
    #env = VecFrameStack(env, 4, channels_order='last')
    model = MultiOutputPPO.load(model_path)

episodes = 5

import cv2

for episode in range(1, episodes + 1):
    obs, _ = env.reset()
    done = False

    while not done:
        #env.render()

        if not manual:
            action, _states = model.predict(obs)
            print(action)

        else:
            # Key Actions
            keys = [ 1, 1 ]
            if is_pressed('w'): keys[0] += 1
            if is_pressed('s'): keys[0] -= 1
            if is_pressed('a'): keys[1] -= 1
            if is_pressed('d'): keys[1] += 1

            # Mouse Actions
            mouse_clicked = 1 if mouse.get_pressed()[0] else 0 #Returns 1 if clicked, 0 otherwise

            # Angle Calculations based on Mouse Positions
            player = env.game.player
            mouse_pos = mouse.get_pos()

            x_diff = mouse_pos[0] - player.x
            y_diff = mouse_pos[1] - player.y
            angle = math.atan(x_diff/y_diff) #I have no idea why this is the case

            action = { "keys": keys, "isShooting" : mouse_clicked, "angle": angle}
        #action = [1,2]

        obs, reward, terminated, truncated, info = env.step(action)

        done = terminated or truncated

        #cv2.imshow("AI View", obs)
        #cv2.waitKey()
