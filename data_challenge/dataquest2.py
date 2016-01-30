import numpy as np
import itertools
np.set_printoptions(precision=9)
import math
import timeit
from functools import partial
from multiprocessing import Pool

def draw_card(n, trials):
    total_score_of_trials = 0

    for j in range(trials):
        card_drawn = 0
        card_value = 0
        total = 0
        trial_scores = list()
        # dictionary of card values
        dict_card_values = {0:1, 1:2, 2:4, 3:8, 4:16, 5:32, 6:64}
        while total < range(n):
            card_drawn = np.random.randint(0,7)
            card_value = dict_card_values[card_drawn]
            total += card_value
        trial_scores.append(total - n)
    trial_scores = np.array(trial_scores)
    score_mean = np.mean(trials_scores, dtype=np.float64)
    score_SD = np.std(trial_scores, dtype=np.float64)
    return score_mean, score_SD




def easy_parallize(f, sequence):
    pool = Pool(processes=2) # Defaults to num of processors (2) if unspecified
    result = pool.map(f, sequence) # e.g. (function, jobs)
    cleaned = [x for x in result if not x is None]
    # cleaned = asarray(cleaned)
    # not optimal but safe
    pool.close()
    pool.join()
    return cleaned

    # return partial(easy_parallize, f) 

def main():
    total_start_time = timeit.default_timer()
    # Parameters
    repetitions = (10**2)*1  # trials to repeat over
    n = 21  # steps to take
    # choice variable for 
    params = [n, repetitions]
    jobs = [] # list of jobs (param inputs) to run through function
    jobruns = range(1)  # times to repeat same entire job
    
    for j in jobruns:
        jobs.append(params)
    
    results = easy_parallize(draw_card, jobs)
    
    print("Mean= ", results[0], ", SD= ", results[1])
            
    print("Total time elapsed for all jobs: ", timeit.default_timer() - total_start_time, " secs")


