import os
import pandas as pd
import numpy as np
import time
from pathlib import Path

# import functions for recurrence analysis
from recurrence_functions import symbolize, recurrence

# import sound amplitude data
data = pd.read_csv('amplitude.csv')

file_s1 = []; file_s2 = []
for p in range(30):
    s1 = data.loc[(data['session']==1) & (data['pair']==p) & (data['player']==1)]['amplitude']
    s2 = data.loc[(data['session']==2) & (data['pair']==p) & (data['player']==1)]['amplitude']
    file_s1.append(np.array(s1))
    file_s2.append(np.array(s2))
for q in range(30):
    s1 = data.loc[(data['session']==1) & (data['pair']==q) & (data['player']==2)]['amplitude']
    s2 = data.loc[(data['session']==2) & (data['pair']==q) & (data['player']==2)]['amplitude']
    file_s1.append(np.array(s1))
    file_s2.append(np.array(s2))

# an empty array to store data
## session, values (SRR, d_max, d_bar, d_prop, v_max, v_bar, v_prop, H),
## player i, player j
rec_together = np.empty((2, 8, 60, 60))

# m-history
m = 3

# start
start = time.time()
for i in range(60):
    for j in range(60):
        #session 1
        foo1 = file_s1[i]
        foo2 = file_s2[j]
        foo = foo1 + foo2
        symbol_foo = symbolize(foo, m)
        rec_together[0,:,i,j] = recurrence(symbol_foo, m)

        #session 2
        foo1 = file_s2[i]
        foo2 = file_s2[j]
        foo = foo1 + foo2
        symbol_foo = symbolize(foo, m)
        rec_together[1,:,i,j] = recurrence(symbol_foo, m)

        # print progress
        if np.mod(60*i+j+1,10)==0:
            elapsed = int((time.time() - start)/60)
            print(60*i+j+1, 'out of', 3600, 'done.', elapsed, 'min elasped.')

# save
np.save('rec_together.npy', rec_together)
