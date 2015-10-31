# Random walk
# Bernoulli / Binomial Distribution
# started project at 11am on Oct 29th
# As crow flies - take length of line (hypotenuse of triangle) formed
# from (0,0) to (x,y)
# length = sqrt((x**2)+(y**2))
# prob of a && b = a*b


from scipy import stats
import numpy as np
import itertools
np.set_printoptions(precision=9)

n = 60  # Steps
p1 = 0.5 # Probability of vertical or horizontal
p2 = 0.5 # Probability of success (towards target)
goal = 10 # How far is the threshold as crow flies?
# length = ((x**2) + (y**2))**0.5 # radius length from 0,0
# q = 100 # trials

def walk_1D(n, p1, p2, goal):
    k = np.arange(goal,n + 1)  # Number of successes needed if 1D
    binomial = stats.binom.pmf(k, n, p)
    print(binomial, k)
    print(sum(binomial))
    return print(format(sum(binomial), '.10g'))


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
                    print ("x", x, "and y", y)
                    binom_x = stats.binom.pmf(x, x_count, p2)
                    binom_y = stats.binom.pmf(y, y_count, p2)
                    prob_mass = prob_mass + (binom_x * binom_y)
        
        binom_count = stats.binom.pmf(x_count, n, p1)
        print("Binom of Count_x: ", binom_count)
        print("Probability Mass: ", prob_mass)
        cuml_prob = cuml_prob + (prob_mass * binom_count)
        print("Cumulative Probability: ", cuml_prob)

    return cuml_prob




print("Cumulative Probability in Total: ", walk_pmf_add(n, p1, p2, goal))








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

