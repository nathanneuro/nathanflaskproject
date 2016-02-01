import numpy as np
import itertools
import math
import timeit
from functools import partial
from multiprocessing import Pool
from statistics import mean, stdev
from decimal import *

def draw_card(params):
    n = params[0]
    trials = params[1]
    total_score_of_trials = 0
    # dictionary of card values
    dict_card_values = {0:1, 1:2, 2:4, 3:8, 4:16, 5:32, 6:64}
    trial_scores = list()

    for j in range(trials):
        card_drawn = 0
        card_value = 0
        total = 0
        
        while total < n:
            card_drawn = np.random.randint(0, high = 7)
            card_value = dict_card_values[card_drawn]
            total += card_value

        trial_scores.append(total - n)

    trial_scores = np.array(trial_scores)
    score_mean = np.mean(trial_scores, dtype=np.float64)
    score_SD = np.std(trial_scores, dtype=np.float64)
    job_result = np.array([score_mean, score_SD])
    return job_result




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
    # Precision Options
    #np.set_printoptions(precision=10)
    #np.set_printoptions(formatter={'float': '{:.9f}'.format})
    getcontext().prec = 9
    # Parameters
    repetitions = (10**5)*2  # trials to repeat over
    n = 21  # steps to take
    # choice variable for expansion of function
    params = [n, repetitions]
    jobs = [] # list of jobs (param inputs) to run through function
    job_runs = 5  # times to repeat same entire job
    
    for j in range(job_runs):
        jobs.append(params)
    
    job_set_total = [0,0]
    master_total = [0,0]
    job_counter = 0
    all_means = []
    all_stdevs = []
    while job_counter <= 500:
        #results = easy_parallize(draw_card, jobs)
        #for job_result in results:
        #print("Job #", i, "Mean= ", '{:.9f}'.format(job_result[0]), ", SD= ", '{:.9f}'.format(job_result[1]))
        for task in range(job_runs):
            results = draw_card(params)
            #all_means.extend(item[0] for item in results)
            #all_stdevs.extend(item[1] for item in results)
            all_means.append(results[0])
            all_stdevs.append(results[1])
        job_counter += job_runs
        if not job_counter % 20:
            # results[-1][0], results[-1][1]
            print("Jobs: ", job_counter, results[0], results[1], Decimal(mean(all_means)), Decimal(mean(all_stdevs)))
        if (Decimal(mean(all_means[:-1])) == Decimal(mean(all_means))) and (Decimal(mean(all_stdevs[:-1])) == Decimal(mean(all_stdevs))):
            print("Success!")
            break
        #print("Success!", "Jobs total:", job_counter, "Mean= ", '{:.9f}'.format(master_total[0]), ", SD= ", '{:.9f}'.format(master_total[1]))
    print(job_counter, Decimal(mean(all_means)), Decimal(mean(all_stdevs)))

    print("Total time elapsed for all jobs: ", timeit.default_timer() - total_start_time, " secs")

if __name__ == '__main__':
   main()
