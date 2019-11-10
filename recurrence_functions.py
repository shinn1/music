# functions for recurrence analysis
import numpy as np
import pandas as pd
import itertools
import os
from find_runs import find_runs

#___________________________________________________________
#
# symbolize
def symbolize(xx, mm):
    perm = list(itertools.permutations(range(mm)))
    sx = []
    for i in range(len(xx) - mm):
        aa = xx[i:(i + mm)]
        sx.append(np.where([np.array_equal(np.argsort(aa), perm[p]) for p in range(len(perm))])[0].tolist())
    sx = np.array([x[0] for x in sx])

    return sx



#___________________________________________________________
#
# surrogate symbolic time series x on y
def surrogate(sx, sy, mm):
    perm = list(itertools.permutations(range(mm)))
    sxx = sx.copy()
    for n in range(len(perm)):
        idx = np.where(sy == n)[0]
        shuffled = np.random.permutation(sxx[idx])
        np.put(sxx, idx, shuffled)

    return sxx



#___________________________________________________________
#
# recurrence metrics
# returns SRR, d_max, d_bar, D, v_max, v_bar, V, H
def recurrence(sx, mm):
    perm = list(itertools.permutations(range(mm)))
    count = np.zeros(len(perm), dtype = int)    # reccurrence for each symbol (t < s)
    for t in range(len(sx) - 1):
        for s in range(t + 1, len(sx)):
            if(sx[t] == sx[s]):
                count[sx[t]] = count[sx[t]] + 1

    # recurrence rate
    SRR = np.sum(count) * 2 / (len(sx)**2 - len(sx))

    # vertical elements
    vertical = []
    for t in range(len(sx) - 1):
        sxx = sx[(t+1):]
        foo = sxx - np.array(sx[t])    # vertical
        bar = [sxx[i] if foo[i] == 0 else -1 for i in range(foo.size)]
        runs = find_runs(bar)
        nruns = runs[2][np.where(runs[0] > -1)]
        vertical.extend(nruns.tolist())

    unique, counts = np.unique(vertical, return_counts = True)
    V = pd.DataFrame(np.asarray((unique, counts)).T, columns = ['v', 'n'])
    V_sub = V.drop(V.index[0])  # drop the row with length 1
    v_max = np.max(V_sub['v'])
    v_bar = np.sum(V_sub['v'] * V_sub['n']) / np.sum(V_sub['n'])
    v_prop = np.sum(V_sub['v'] * V_sub['n']) / np.sum(V['v'] * V['n'])

    # diagonal elements
    diagonal = []
    for delta in range(1, len(sx) - 1):
        foo = sx - np.roll(sx, -delta)    # diagonal
        foo = foo[:-delta]
        bar = [sx[i] if foo[i] == 0 else -1 for i in range(foo.size)]
        runs = find_runs(bar)
        nruns = runs[2][np.where(runs[0] > -1)]
        diagonal.extend(nruns.tolist())

    unique, counts = np.unique(diagonal, return_counts = True)
    D = pd.DataFrame(np.asarray((unique, counts)).T, columns = ['d', 'n'])
    D_sub = D.drop(D.index[0])  # drop the row with length 1
    d_max = np.max(D_sub['d'])
    d_bar = np.sum(D_sub['d'] * D_sub['n']) / np.sum(D_sub['n'])
    d_prop = np.sum(D_sub['d'] * D_sub['n']) / np.sum(D['d'] * D['n'])

    # entropy of reccurrence
    p = [0 if count[c] == 0 else count[c] / np.sum(count) * np.log2(count[c] / np.sum(count)) for c in range(len(perm))]

    H = -np.sum(p)

    return SRR, v_max, v_bar, v_prop, d_max, d_bar, d_prop, H



#___________________________________________________________
#
# function to get joint SRR and recurrence MI

def MIrec(sx, sy, mm):

    perm = list(itertools.permutations(range(mm)))
    # recurrence of the combination of symbols
    combn = [p for p in itertools.product(range(len(perm)), repeat = 2)]
    times = list(itertools.combinations(range(len(sx)), 2))
    foo = [[sx[ts[0]], sy[ts[0]]] for ts in times]
    bar = [[sx[ts[1]], sy[ts[1]]] for ts in times]
    baz = np.all(np.array(foo) == np.array(bar), axis = 1)
    idx = list(itertools.compress(range(len(baz)), baz))
    idx2 = [np.argwhere(np.all(np.array(combn) == foo[i], axis = 1))[0][0] for i in idx]
    unique, counts = np.unique(idx2, return_counts = True)
    count = pd.Series(counts)
    count.index = unique

    # joint recurrence rate
    df = pd.DataFrame(combn, columns = ['x', 'y'])
    df['count'] = count
    df = df.fillna(0)

    jointSRR = np.sum(df['count']) / (len(sx) ** 2 - len(sx))

    # mutual information
    p = np.empty(len(combn))
    for i in range(df.shape[0]):
        px = np.sum(df.loc[df['x'] == df.iloc[i,0]]['count']) / np.sum(df['count'])
        py = np.sum(df.loc[df['y'] == df.iloc[i,1]]['count']) / np.sum(df['count'])
        pxy = df.iloc[i, 2] / np.sum(df['count'])

        if pxy == 0 or px == 0 or py == 0:
            p[i] = 0
        else:
            p[i] = pxy * np.log2(pxy / (px * py))

    return jointSRR, np.sum(p)



#___________________________________________________________
#
# function to get reccurrence TE from sy to sx (m-history)

def TErec(sy, sx, mm):
    perm = list(itertools.permutations(range(mm)))

    sxplus = sx[1:]
    sx = sx[:-1]
    sy = sy[:-1]

    # count recurrence of the combination of symbols
    combn = [p for p in itertools.product(range(len(perm)), repeat = 3)]
    times = list(itertools.combinations(range(len(sx)), 2))
    foo = [[sxplus[ts[0]], sx[ts[0]], sy[ts[0]]] for ts in times]
    bar = [[sxplus[ts[1]], sx[ts[1]], sy[ts[1]]] for ts in times]
    baz = np.all(np.array(foo) == np.array(bar), axis = 1)
    idx = list(itertools.compress(range(len(baz)), baz))
    idx2 = [np.argwhere(np.all(np.array(combn) == foo[i], axis=1))[0][0] for i in idx]
    unique, counts = np.unique(idx2, return_counts = True)
    count = pd.Series(counts)
    count.index = unique

    # transfer entropy from y to x
    df = pd.DataFrame(combn, columns = ['xplus', 'x', 'y'])
    df['count'] = count
    df = df.fillna(0)

    p = np.empty(len(combn))
    for i in range(df.shape[0]):

        px = np.sum(df.loc[df['x'] == df.iloc[i,1]]['count']) / np.sum(df['count'])
        pxy = np.sum(df.loc[(df['x'] == df.iloc[i,1]) & (df['y'] == df.iloc[i,2])]['count']) / np.sum(df['count'])
        pxplusx = np.sum(df.loc[(df['xplus'] == df.iloc[i,0]) & (df['x'] == df.iloc[i,1])]['count']) / np.sum(df['count'])
        pxplusxy = df.iloc[i, 3] / np.sum(df['count'])

        if px == 0 or pxy == 0 or pxplusx ==0 or pxplusxy==0:
            p[i] = 0
        else:
            p[i] = pxplusxy * np.log2((pxplusxy / pxy) / (pxplusx/ px))

    return np.sum(p)
