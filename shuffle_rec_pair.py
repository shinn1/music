import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
from pathlib import Path

# import data
home = str(Path.home())
os.chdir(home + '/Google Drive/music_project/data_processed/')

rec_pair = np.load('rec_pair_m3.npy')

obs_pair1 = np.diagonal(rec_pair[:, :, :30, 30:], axis1 = 2, axis2 = 3) # SRR, MI, TE12
obs_pair2 = np.diagonal(rec_pair[:, 2, 30:, :30], axis1 = 1, axis2 = 2) # TE21
obs_pair2 = np.expand_dims(obs_pair2, axis = 1)
obs_pair = np.concatenate((obs_pair1, obs_pair2), axis = 1)     # session, vals (SRR, MI, TE12, TE21), pair



#__________________________________________________
#
# compare an observed mean against shuffled means

n_itr = 20000
shuffle_pair = np.empty((2, 4, n_itr, 30))  # session, vals (jointSRR, MI, TE12, TE21), itr, pair
k = np.repeat(range(30), 2)     # fake pair ID
for itr in range(n_itr):
    np.random.shuffle(k)    # shuffle fake pair ID
    foo = np.empty((2, 4, 30))    # session, vals (jointSRR, MI, TE12, TE21), pair
    for x in range(30):
        pair = np.where(k == x)[0].tolist()
        foo[:, :3, x] = rec_pair[:, :, pair[0], pair[1]]
        foo[:, 3, x] = rec_pair[:, 2, pair[1], pair[0]]
    shuffle_pair[:, :, itr, :] = foo

np.save('obs_pair.npy', obs_pair)
np.save('shuffle_pair.npy', shuffle_pair)

#____________________________
# p-value
p_s1 = []; p_s2 = []
## jointSRR (session 1)
foo = np.mean(obs_pair[0, 0, :])                  # observed mean
bar = np.mean(shuffle_pair[0, 0, :, :], axis = 1) # shuffled means
right = np.sum(foo < bar)
p_s1.append((right + 1) / (n_itr + 1))

## jointSRR (session 2)
foo = np.mean(obs_pair[1, 0, :])
bar = np.mean(shuffle_pair[1, 0, :, :], axis = 1)
right = np.sum(foo < bar)
p_s2.append((right + 1) / (n_itr + 1))

## MI (session 1)
foo = np.mean(obs_pair[0, 1, :])
bar = np.mean(shuffle_pair[0, 1, :, :], axis = 1)
right = np.sum(foo < bar)
p_s1.append((right + 1) / (n_itr + 1))

## MI (session 2)
foo = np.mean(obs_pair[1, 1, :])
bar = np.mean(shuffle_pair[1, 1, :, :], axis = 1)
right = np.sum(foo < bar)
p_s2.append((right + 1) / (n_itr + 1))

## TE (session 1)
foo = np.mean(obs_pair[0, 2:4, :])
bar = np.mean(shuffle_pair[0, 2:4, :, :], axis = 2).flatten()
right = np.sum(foo < bar)
p_s1.append((right + 1) / (n_itr + 1))

## TE (session 2)
foo = np.mean(obs_pair[1, 2:4, :])
bar = np.mean(shuffle_pair[1, 2:4, :, :], axis = 2).flatten()
right = np.sum(foo < bar)
p_s2.append((right + 1) / (n_itr + 1))

# save
p_vals = pd.DataFrame()
p_vals['session 1'] = p_s1
p_vals['session 2'] = p_s2
p_vals.index = ['jointSRR', 'MI', 'TE']
os.chdir(home + '/Google Drive/music_project/data_processed')
p_vals.to_csv('p_vals_pair.csv')
