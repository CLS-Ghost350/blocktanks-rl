import os

from sb3_plus import MultiOutputPPO

from stable_baselines3.common.vec_env import DummyVecEnv, VecFrameStack

from keyboard import is_pressed

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
            keys = [ 1, 1 ]
            if is_pressed('w'): keys[0] += 1
            if is_pressed('s'): keys[0] -= 1
            if is_pressed('a'): keys[1] -= 1
            if is_pressed('d'): keys[1] += 1

            action = { "keys": keys }
        #action = [1,2]

        obs, reward, terminated, truncated, info = env.step(action)

        done = terminated or truncated

        #cv2.imshow("AI View", obs)
        #cv2.waitKey()
