# Random walk
# Bernoulli / Binomial Distribution
# started project at 11am on Oct 29th

from scipy import stats
import numpy as np

n = 10  # Steps
p = 0.5  # Probability of success (towards target)
k = np.arange(0,n + 1)  # Number of successes
binomial = stats.binom.pmf(k, n, p)
print(binomial)
