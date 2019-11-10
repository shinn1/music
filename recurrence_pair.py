import os
import pandas as pd
import numpy as np
import time
from pathlib import Path

# import functions for recurrence analysis
home = str(Path.home())
os.chdir(home + '/Google Drive/music_project/codes_python')
from recurrence_functions import symbolize, TErec, MIrec

# directory of amplitude files
os.chdir(home + '/Google Drive/music_project/data_processed/wav data (0.15 s)')

# list of file names
## first 30 is player 1, second 30 is player 2
file_s1 = []
file_s2 = []
for p in range(30):
    file_s1.append('Trial' + str(p+1).zfill(2) + 'p1s1.csv')
    file_s2.append('Trial' + str(p+1).zfill(2) + 'p1s2.csv')
for q in range(30):
    file_s1.append('Trial' + str(q+1).zfill(2) + 'p2s1.csv')
    file_s2.append('Trial' + str(q+1).zfill(2) + 'p2s2.csv')

# empty array to store data
## session, values (jointSRR, MI, TE), player i, player j
rec_pair = np.empty((2, 3, 60, 60))

# m-history
m = 3

# start
start = time.time()
for i in range(60):
    for j in range(60):
        #session 1
        data1 = pd.read_csv(file_s1[i])
        data2 = pd.read_csv(file_s1[j])
        foo1 = data1['amplitude']
        foo2 = data2['amplitude']
        symbol_foo1 = symbolize(foo1, m)
        symbol_foo2 = symbolize(foo2, m)
        val1 = MIrec(symbol_foo1, symbol_foo2, m)     # jointSRR, recurrence MI
        val2 = TErec(symbol_foo1, symbol_foo2, m)     # recurrence TE(i->j)
        rec_pair[0,:,i, j] = [val1[0], val1[1], val2]

        #session 2
        data1 = pd.read_csv(file_s2[i])
        data2 = pd.read_csv(file_s2[j])
        foo1 = data1['amplitude']
        foo2 = data2['amplitude']
        symbol_foo1 = symbolize(foo1, m)
        symbol_foo2 = symbolize(foo2, m)
        val1 = MIrec(symbol_foo1, symbol_foo2, m)
        val2 = TErec(symbol_foo1, symbol_foo2, m)
        rec_pair[1,:,i, j] = [val1[0], val1[1], val2]

        # print progress
        if np.mod(60*i+j+1,10)==0:
            elapsed = int((time.time() - start)/60)
            print(60*i+j+1, 'out of', len(file_s1) * len(file_s2), 'done.', elapsed, 'min elasped.')

# save
os.chdir(home + '/Google Drive/music_project/data_processed')
np.save('rec_pair_m3.npy', rec_pair)
