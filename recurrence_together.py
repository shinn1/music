import os
import pandas as pd
import numpy as np
import time
from pathlib import Path

# import functions for recurrence analysis
home = str(Path.home())
os.chdir(home + '/Google Drive/music_project/codes_python')
from recurrence_functions import symbolize, recurrence

# directory of amplitude files
os.chdir(home + '/Google Drive/music_project/data_processed/wav data (0.15 s)')

# a list of file names
file_s1 = []; file_s2 = []
for p in range(30):
    file_s1.append('Trial' + str(p+1).zfill(2) + 'p1s1.csv')
    file_s2.append('Trial' + str(p+1).zfill(2) + 'p1s2.csv')
for q in range(30):
    file_s1.append('Trial' + str(q+1).zfill(2) + 'p2s1.csv')
    file_s2.append('Trial' + str(q+1).zfill(2) + 'p2s2.csv')

# an empty array to store data
## session, values (SRR, v_max, v_bar, v_prop, d_max, d_bar, d_prop, H),
## player i, player j
rec_together = np.empty((2, 8, 60, 60))

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
        foo = foo1 + foo2
        symbol_foo = symbolize(foo, m)
        rec_together[0,:,i,j] = recurrence(symbol_foo, m)

        #session 2
        data1 = pd.read_csv(file_s2[i])
        data2 = pd.read_csv(file_s2[j])
        foo1 = data1['amplitude']
        foo2 = data2['amplitude']
        foo = foo1 + foo2
        symbol_foo = symbolize(foo, m)
        rec_together[1,:,i,j] = recurrence(symbol_foo, m)

        # print progress
        if np.mod(60*i+j+1,10)==0:
            elapsed = int((time.time() - start)/60)
            print(60*i+j+1, 'out of', 3600, 'done.', elapsed, 'min elasped.')

# save
os.chdir(home + '/Google Drive/music_project/data_processed')
np.save('rec_together_m3.npy', rec_together)
