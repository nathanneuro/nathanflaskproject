# Random walk
# Bernoulli / Binomial Distribution
# started project at 11am on Oct 29th
# As crow flies - take length of line (hypotenuse of triangle) formed
# from (0,0) to (x,y)
# length = sqrt((x**2)+(y**2))

#from scipy import stats
import numpy as np
import itertools
np.set_printoptions(precision=9)
import math
import timeit
from functools import partial
from multiprocessing import Pool


#Parameters

#n = 10  # Steps
#p1 = 0.5 # Probability of vertical or horizontal
#p2 = 0.5 # Probability of success (towards target)
#goal = 3 # How far is the threshold as crow flies?
# length = ((x**2) + (y**2))**0.5 # radius length from 0,0
# q = 100 # trials for simulation

#p = 0.5 # For 1D


# math.factorial(x)
#def walk_1D(n, p, goal):
#    k = np.arange(goal,n + 1)  # Number of successes needed if 1D
#    binomial = stats.binom.pmf(k, n, p)
#    print(binomial, k)
#    print(sum(binomial))
#    print(format(sum(binomial), '.10g'))
#    return sum(binomial)


def walk_sim_peak(params):
    job_start_time = timeit.default_timer()
    cross = 0
    move_tot = 0
    run_tot = [0, 0, 0, 0, 0]
    trials = params[0]
    n = params[1]
    goal = params[2]
    for t in range(trials):
        x = 0
        y = 0
        # print("Trial #", t+1)
        for i in range(n):
            move = np.random.randint(0,4)
            # print("Move rand int: ", move, " for step number ", i+1)
            if move == 0:
                x = x - 1
            elif move == 1:
                x = x + 1
            elif move == 2:
                y = y - 1
            elif move == 3:
                y = y + 1
            #else:
            #    print("Error. Wrong Move direction.")
            # print("(", x, ", ", y, ")")
        if ((x**2 + y**2)**0.5) >= goal:
            cross = cross + 1
            # print("Cross! ", cross)
            move_tot = move_tot + (i+1)
    #print("Crosses: ", cross, " Total trials: ", trials, " p = ", cross/trials, "Move avg:", move_tot/trials)
    run_tot[0] = run_tot[0] + cross  # crosses
    run_tot[1] = run_tot[1] + trials  # trials
    run_tot[2] = run_tot[0] / run_tot[1]  # crosses/trials
    run_tot[3] = run_tot[3] + move_tot  # moves total
    run_tot[4] = timeit.default_timer() - job_start_time  # job time elapsed

    return (run_tot)


# def parallel_attribute(f): # this would let it take a func with multiple params
# Assumes f has one argument unless using partial (confused so not using for now)

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
    repetitions = (10**4)*50  # trials to repeat over
    n = 10  # steps to take
    goal = 3  # boundary to cross
    params = [repetitions, n, goal]
    jobs = [] # list of jobs (param inputs) to run through function
    jobruns = range(5)  # times to repeat same entire job
    
    for j in jobruns:
        jobs.append(params)
    
    results = easy_parallize(walk_sim_peak, jobs)
    
    for run_tot in results:
        print("Crosses: ", run_tot[0], "Trials: ", run_tot[1], " p = ", run_tot[2], "Move Avg:", (run_tot[3]/run_tot[1]), "\nTime elapsed for job: ", run_tot[4], " secs")
        
    print("Total time elapsed for all jobs: ", timeit.default_timer() - total_start_time, " secs")


def walk_pmf_add(n, p1, p2, goal):
    count_pairs = n + 1
    cuml_prob = 0
    print(count_pairs, " Total Count Pairs")
    for pair in range(count_pairs):
        x_count = count_pairs-(pair+1)
        y_count = pair
        print("Count Pair: #", x_count, "x, #", y_count, "y")
        prob_mass = 0
        #function here
        if x_count % 2 == 1:
            x_list = list(range(x_count + 1))
        else:
            x_list = list(range(0, x_count + 1, 2))
        if y_count % 2 == 1:
            y_list = list(range(y_count + 1))
        else:
            y_list = list(range(0, y_count + 1, 2))
        print("X list: ", x_list, "Y list", y_list)
        for y in y_list:
            for x in x_list:
                if ((x**2 + y**2)**0.5) >= goal:
                    # print ("x", x, "and y", y)
                    # remember that "losses" count too, so two-tailed
                    # multiplying by binompmf by 2 > 1 tot p nonsensical
                    binom_x = stats.binom.pmf(x, x_count, p2)
                    binom_y = stats.binom.pmf(y, y_count, p2)
                    prob_mass = prob_mass + (binom_x * binom_y)
        
        binom_count = stats.binom.pmf(x_count, n, p1)
        print("Binom of Count_x: ", binom_count)
        print("Probability Mass: ", prob_mass)
        cuml_prob = cuml_prob + (prob_mass * binom_count)
        print("Cumulative Probability: ", cuml_prob)

    return cuml_prob




# print("Cumulative Probability in Total: ", walk_pmf_add(n, p1, p2, goal))

# w = walk_1D(n, p, goal)


#def walkendpoint(n, p1, q, p2):
  #  count_x = sum(np.random.binomial(n, p1, q))
  #  count_y = n - count_x
  #  x_total = 0
  #  y_total = 0
  #  for x in xrange(count_x):
  #      horizontal = sum(np.random.binomial(1, p2, 1) #zero for -1, 1 for +1
        #if horizontal == 0:
        #    x_total = x_total - 1
        #else:
        #    x_total = x_total + 1
    #for y in xrange(count_y):
    #    vertical = sum(np.random.binomial(1, p2, 1) #zero for -1, 1 for +1
    #    if vertical == 0:
    #        y_total = y_total - 1
    #    else:
    #        y_total = y_total + 1
    #return (x_total, y_total)

    
#endarray = []
#endarray.append(walkendpoint(n, p1, q, p2))



# since i'm confused, I'll try a simulation
def ends(walks=1000, n=10, dimensions=2):
    return sum(np.random.random_integers(12,1,(n,walks,dimensions)))

#simX, simY = np.transpose(ends(10, 10, 2))
# lengths = np.prod(ends(10, 10, 2), axis=1) as alternate form
#lengths = ((simX**2) + (simY**2))**0.5
# ** for exponent, .5 for square root
#goal = 10
#probpass = ((lengths >= goal).sum())/len(lengths)
#print(simX, simY, lengths)
#print(probpass)

if __name__ == '__main__':
   main()
