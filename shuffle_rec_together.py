import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
from pathlib import Path
import itertools

# import data
rec_together = np.load('rec_together.npy')

# observed mean
# SRR, d_max, d_bar, d_prop, v_max, v_bar, v_prop, H
obs_together = np.diagonal(rec_together[:, :, :30, 30:], axis1 = 2, axis2 = 3)

# shuffled means
n_itr = 20000
shuffle_together = np.empty((2, 8, n_itr, 30))  # session, vals, itr, pair
k = np.repeat(range(30), 2)     # fake pair ID
for itr in range(n_itr):
    np.random.shuffle(k)    # shuffle fake pair ID
    foo = np.empty((2, 8, 30))    # session, vals, pair
    for x in range(30):
        pair = np.where(k == x)[0].tolist()
        foo[:, :, x] = rec_together[:, :, pair[0], pair[1]]
    shuffle_together[:, :, itr, :] = foo

# compare
p_vals = pd.DataFrame()
p_val_s1 = []; p_val_s2 = []
for i in range(8):
    foo = np.mean(obs_together[:, i, :], axis = 1)          # observed mean
    bar = np.mean(shuffle_together[:, i, :, :], axis = 2)   # shuffled means

    right_s1 = np.sum(foo[0] < bar[0, :])
    left_s1 = np.sum(foo[0] > bar[0, :])
    p1 = (np.min([right_s1, left_s1]) * 2 + 1) / (n_itr + 1)
    p_val_s1.append(p1)

    right_s2 = np.sum(foo[1] < bar[1, :])
    left_s2 = np.sum(foo[1] > bar[1, :])
    p2 = (np.min([right_s2, left_s2]) * 2 + 1) / (n_itr + 1)
    p_val_s2.append(p2)

p_vals['session1'] = p_val_s1
p_vals['session2'] = p_val_s2
p_vals.index = ['SRR', 'd_max', 'd_bar', 'd_prop', 'v_max', 'v_bar', 'v_prop', 'H']
