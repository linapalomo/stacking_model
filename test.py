
import numpy as np
import json
from numpy.random import default_rng


LU_prob = np.random.dirichlet(np.ones(3), size=1).tolist()[0]
LU0, LU1, LU2 = [int(prob * 100) for prob in LU_prob]


n_plots = 200
LU0_parcels = int(n_plots * LU0 / 100)
LU1_parcels = int(n_plots * LU1 / 100)
LU2_parcels = int(n_plots * LU2 / 100)


LU_distribution = {
    "LU0": LU0_parcels,
    "LU1": LU1_parcels,
    "LU2": LU2_parcels
}

with open("LU_distribution.json", "w") as f:
    json.dump(LU_distribution, f)


print(f'Percentage of LU0: {LU0}%, number of cells: {LU0_parcels}')
print(f'Percentage of LU1: {LU1}%, number of cells: {LU1_parcels}')
print(f'Percentage of LU2: {LU2}%, number of cells: {LU2_parcels}')
print(LU0, LU1, LU2)
