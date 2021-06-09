from scipy import stats
import scikit_posthocs as sp
import numpy as np

# RF p2000 accuracy over different sampling methods
group1 = [0.741,0.704,0.790,0.773,0.756,0.747,0.731,0.778,0.759,0.689]
group2 = [0.629,0.676,0.689,0.687,0.667,0.623,0.642,0.719,0.647,0.565]
group3 = [0.523,0.701,0.790,0.761,0.578,0.502,0.608,0.736,0.537,0.525]

#perform Friedman Test
friedman = stats.friedmanchisquare(group1, group2, group3)
print(friedman)

#combine three groups into one array
data = np.array([group1, group2, group3])

#perform Nemenyi post-hoc test
nemenyi=sp.posthoc_nemenyi_friedman(data.T)
print (nemenyi)