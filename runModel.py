import os
import math

from sb3_plus import MultiOutputPPO

from stable_baselines3.common.vec_env import DummyVecEnv, VecFrameStack
from gymnasium.spaces import MultiDiscrete, Box, Dict
from keyboard import is_pressed
from pygame import mouse

from BlocktanksEnv import BlocktanksEnv, BlocktanksGame

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
            # Mouse Actions
            mouse_clicked = 1 if mouse.get_pressed()[0] else 0 #Returns 1 if clicked, 0 otherwise

            # Key Actions
            keys = [ 1, 1, mouse_clicked ]
            if is_pressed('w'): keys[0] += 1
            if is_pressed('s'): keys[0] -= 1
            if is_pressed('a'): keys[1] -= 1
            if is_pressed('d'): keys[1] += 1


            # Angle Calculations based on Mouse Positions
            centerX = BlocktanksGame.WINDOW_SIZE[0] / 2
            centerY = BlocktanksGame.WINDOW_SIZE[1] / 2

            mouse_pos = mouse.get_pos()

            #print(mouse_pos, (centerX, centerY))

            angle = math.atan2(mouse_pos[1] - centerY, mouse_pos[0] - centerX) 

            action = { "keys": keys, "angle": angle}
        #action = [1,2]

        obs, reward, terminated, truncated, info = env.step(action)

        done = terminated or truncated

        #cv2.imshow("AI View", obs)
        #cv2.waitKey()
