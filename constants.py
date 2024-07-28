class HyperParameters:
    N_STEPS = 128
    LEARNING_RATE = lambda amountLeft: 0.0004 * amountLeft**2

class LearningParameters:
    TOTAL_TIMESTEPS = 2 * 1000 * 1000 # fps around 18 per env (108 total)
    N_ENVS = 6

    SAVE_FREQ = 12000
    SAVE_FREQ = max(SAVE_FREQ // N_ENVS, 1)