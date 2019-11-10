import os
import pandas as pd
import numpy as np
import time
from pathlib import Path

# import functions for recurrence analysis
from recurrence_functions import symbolize, TErec, MIrec

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
        foo1 = file_s1[i]
        foo2 = file_s1[j]
        symbol_foo1 = symbolize(foo1, m)
        symbol_foo2 = symbolize(foo2, m)
        val1 = MIrec(symbol_foo1, symbol_foo2, m)     # jointSRR, recurrence MI
        val2 = TErec(symbol_foo1, symbol_foo2, m)     # recurrence TE(i->j)
        rec_pair[0,:,i, j] = [val1[0], val1[1], val2]

        #session 2
        foo1 = file_s2[i]
        foo2 = file_s2[j]
        symbol_foo1 = symbolize(foo1, m)
        symbol_foo2 = symbolize(foo2, m)
        val1 = MIrec(symbol_foo1, symbol_foo2, m)
        val2 = TErec(symbol_foo1, symbol_foo2, m)
        rec_pair[1,:,i, j] = [val1[0], val1[1], val2]

        # print progress
        if np.mod(60*i+j+1,10)==0:
            elapsed = int((time.time() - start)/60)
            print(60*i+j+1, 'out of', len(file_s1) * len(file_s2), 'done.', elapsed, 'min elasped.')

