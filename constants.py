class HyperParameters:
    N_STEPS = 2048
    LEARNING_RATE = 0.0003#lambda amountLeft: 0.0004 * amountLeft**2

    GAMMA = 0.99

class LearningParameters:
    TOTAL_TIMESTEPS = 60 * 1000 # fps around 18 per env (108 total)
    N_ENVS = 6

    SAVE_FREQ = 12000
    SAVE_FREQ = max(SAVE_FREQ // N_ENVS, 1)