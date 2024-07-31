class HyperParameters:
    N_STEPS = 32 #256 #2048 
    # equal to what's normally called the batch size; the number of steps before an update to the networks
    # set to episode length or amount of steps it 

    LEARNING_RATE = lambda amountLeft: 0.0004 * amountLeft**2

    GAMMA = 0.99

    BATCH_SIZE = 16 #32 #64 # actually the mini-batch size

class LearningParameters:
    TOTAL_TIMESTEPS = 600 * 1000 # fps around 18 per env (108 total)  - actually 87? - seems to converge to 70
    N_ENVS = 6

    SAVE_FREQ = 60000
    SAVE_FREQ = max(SAVE_FREQ // N_ENVS, 1)

    LOG_INTERVAL_STEPS = 10 * 1000