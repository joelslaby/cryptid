import dill
import matplotlib.pyplot as plt
import numpy as np

class Data():
   pass

with open('map_data.pk', 'rb') as file:
    d = dill.load(file)

# print([len(x) for x in d.good_hexes])
nbr_good = np.array([len(x) for x in d.good_hexes])
# nbr_good_norm = nbr_good/max(nbr_good)
combo_time = np.array(d.combo_time)
combo_norm = combo_time/max(combo_time)

plt.figure()
# plt.semilogy(d.player_nbrs, nbr_good)
plt.plot(d.player_nbrs, combo_norm)
plt.xlim(3,19)
plt.show()