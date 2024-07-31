import os
import math

from stable_baselines3 import PPO

from stable_baselines3.common.vec_env import DummyVecEnv, VecFrameStack
from gymnasium.spaces import MultiDiscrete, Box
from keyboard import is_pressed
from pygame import mouse

from BlocktanksEnv import BlocktanksEnv, BlocktanksGame

manual = False

env = BlocktanksEnv(render=True)

if not manual:
    model_path = os.path.abspath(os.path.join("Training", "SavedModels", "rl_model_180000_steps")) #"final"))
    #model_path = os.path.abspath(os.path.join("Models", "PPO1"))

    #env = DummyVecEnv([ lambda: env ])
    #env = VecFrameStack(env, 4, channels_order='last')
    model = PPO.load(model_path)

episodes = 5

import cv2

mouse_clicked_last = False

for episode in range(1, episodes + 1):
    obs, _ = env.reset()
    done = False

    steps = 0
    totalReward = 0

    while not done:
        #env.render()

        if not manual:
            action, _states = model.predict(obs)

        else:
            # Key Actions
            action = [ 1, 1, 0, 0 ]
            if is_pressed('w'): action[0] += 1
            if is_pressed('s'): action[0] -= 1
            if is_pressed('a'): action[1] -= 1
            if is_pressed('d'): action[1] += 1

            if mouse.get_pressed()[0]:
                if not mouse_clicked_last:
                    action[2] = 1
                    mouse_clicked_last = True
            else: mouse_clicked_last = False

            # Angle Calculations based on Mouse Positions
            centerX = BlocktanksGame.WINDOW_SIZE[0] / 2
            centerY = BlocktanksGame.WINDOW_SIZE[1] / 2

            mouse_pos = mouse.get_pos()

            #print(mouse_pos, (centerX, centerY))

            angle = (math.atan2(mouse_pos[1] - centerY, mouse_pos[0] - centerX) + 2*math.pi) % (2*math.pi)
            action[3] = round(angle / (2*math.pi) * BlocktanksEnv.ANGLES) % BlocktanksEnv.ANGLES
    
        #action = [1,2]

        print(action)

        obs, reward, terminated, truncated, info = env.step(action)

        #if reward != 0:
        #print(reward)

        totalReward += reward

        done = terminated or truncated

        #cv2.imshow("AI View", obs)
        #cv2.waitKey()

        steps += 1
        #print(steps) # around 100-200 steps per episode

    print("total reward:", totalReward)
