#!/usr/bin/python
# -*- coding: utf-8 -*-
from pycompss.api.task import task
from pycompss.api.parameter import *


@task(returns=dict)
def cluster_points_partial(XPath, mu, ind):
    import pickle
    import numpy as np
    f = open(XPath, 'r')
    XP = pickle.load(f)
    f.close()
    dic = {}
    for x in enumerate(XP):
        bestmukey = min([(i[0], np.linalg.norm(x[1] - mu[i[0]]))
                         for i in enumerate(mu)], key=lambda t: t[1])[0]
        if bestmukey not in dic:
            dic[bestmukey] = [x[0] + ind]
        else:
            dic[bestmukey].append(x[0] + ind)
    return dic


@task(returns=dict)
def partial_sum(XPath, clusters, ind):
    import pickle
    import numpy as np
    f = open(XPath, 'r')
    XP = pickle.load(f)
    f.close()
    p = [(i, [(XP[j - ind]) for j in clusters[i]]) for i in clusters]
    dic = {}
    for i, l in p:
        dic[i] = (len(l), np.sum(l, axis=0))
    return dic


@task(returns=list)
def reduceCenters(partialResult):
    centers = {}
    for l in partialResult:
        for key in l:
            if key not in centers:
                centers[key] = l[key]
            else:
                centers[key] = (
                    centers[key][0] + l[key][0], centers[key][1] + l[key][1])

    return [centers[c][1] / centers[c][0] for c in centers]


@task(a=INOUT, returns=dict)
def reduceCentersTask(a,b):
    for key in b:
        if key not in a:
            a[key] = b[key]
        else:
            a[key] = (a[key][0] + b[key][0], a[key][1] + b[key][1])
    return a


def has_converged(mu, oldmu, epsilon, iter, maxIterations):
    print "iter: " + str(iter)
    print "maxIterations: " + str(maxIterations)
    if oldmu != []:
        if iter < maxIterations:
            aux = [np.linalg.norm(oldmu[i] - mu[i]) for i in range(len(mu))]
            distancia = sum(aux)
            if distancia < epsilon * epsilon:
                print "Distancia_T: " + str(distancia)
                return True
            else:
                print "Distancia_F: " + str(distancia)
                return False
        else:
            # detencion pq se ha alcanzado el maximo de iteraciones
            return True


def distance(p, X):
    import numpy as np
    return min([np.linalg.norm(p-x) for x in X])


@task(returns=list)
def cost(Ypath, C):
    import pickle
    f = open(Ypath, 'r')
    Y = pickle.load(f)
    f.close()
    return sum([distance(x, C)**2 for x in Y])


@task(returns=list)
def probabilities(Xpath, C, l, phi, n):
    import random
    import pickle
    import numpy as np
    random.seed(5)
    f = open(Xpath, 'r')
    X = pickle.load(f)
    f.close()
    p = [(l*distance(x, C)**2)/phi for x in X]
    p /= sum(p)
    idx = np.random.choice(n, l, p=p)
    #idx = [i if p[i] > round(random.uniform(0.0, 1.0), 4) else -1 for i in idx]
    #idx = filter(lambda x: x != -1, idx)
    newC = [X[idx][0] for i in idx]
    return newC


def init_parallel(X, k, initSteps, l, frag, n):
    from pycompss.api.api import compss_wait_on
    import random
    import pickle
    random.seed(5)
    ind = random.randint(0, frag-1)
    f = open(X[ind], 'r')
    XP = pickle.load(f)
    f.close()

    C = random.sample(XP, 1)

    psi = [cost(x, C) for x in X]
    psi = compss_wait_on(psi)
    #psi = [item for sublist in psi for item in sublist]
    phi = sum(psi)

    for i in range(initSteps):
        '''calculate p'''
        c = [probabilities(x, C, l, phi, n/numFrag) for x in X]
        c = compss_wait_on(c)
        C.extend([item for sublist in c for item in sublist])
        '''cost distributed'''
        psi = [cost(x, C) for x in X]
        psi = compss_wait_on(psi)
        #psi = [item for sublist in psi for item in sublist]
        phi = sum(psi)

    f2 = open('/gpfs/projects/bsc19/COMPSs_APPS/kmeans/python/1.0_spark/src/data/centers.txt', 'w')
    pickle.dump(C, f2)
    f2.close()

    '''pick k centers'''
    result = kmeans_frag(len(C), ['/gpfs/projects/bsc19/COMPSs_APPS/kmeans/python/1.0_spark/src/data/centers.txt'], k, 1e-4, initSteps, 1, 'random')
    return result[1]


def init_random(X, k):
    import random
    import pickle
    random.seed(5)
    ind = random.randint(0, len(X)-1)
    f = open(X[ind], 'r')
    XP = pickle.load(f)
    f.close()
    return random.sample(XP, k)

 
def init(X, k, mode, numFrag, numV, initIter=5):
    if mode == "kmeans++||":
        return init_parallel(X, k, initIter, k, numFrag, numV)
    else:
        return init_random(X, k)


def kmeans_frag(numV, X, k, epsilon, maxIterations, numFrag, initMode):
    from pycompss.api.api import compss_wait_on
    import time
    mu = init(X, k, initMode, numFrag, numV)
    oldmu = []
    n = 0
    size = int(numV / numFrag)
    startTime = time.time()
    while not has_converged(mu, oldmu, epsilon, n, maxIterations):
        oldmu = mu
        clusters = [cluster_points_partial(
            X[f], mu, f * size) for f in range(numFrag)]
        partialResult = [partial_sum(
            X[f], clusters[f], f * size) for f in range(numFrag)]

        #partialResult = compss_wait_on(partialResult)

        #mu = reduceCenters(partialResult)
        mu = reduce(reduceCentersTask,partialResult)
        mu = compss_wait_on(mu)
        mu = [mu[c][1]/mu[c][0] for c in mu]
        n += 1
    print "Kmeans Time(s)"
    print time.time()-startTime
    return (n, mu)

if __name__ == "__main__":
    import sys
    import time
    import numpy as np
    import os
    numV = int(sys.argv[1])
    dim = int(sys.argv[2])
    k = int(sys.argv[3])
    numFrag = int(sys.argv[4])
    initMode = sys.argv[5]
    path = sys.argv[6]

    #X = []
    #for file in os.listdir(path):
    #    X.append(path+'/'+file)
    #X = ['/gpfs/projects/bsc19/COMPSs_APPS/kmeans/python/1.0_spark/src/data/N600_K3_d3_0.txt', '/gpfs/projects/bsc19/COMPSs_APPS/kmeans/python/1.0_spark/src/data/N600_K3_d3_1.txt']
    X = ['/gpfs/projects/bsc19/COMPSs_APPS/kmeans/data/spark/N10000000_K100_d1000_100.txt','/gpfs/projects/bsc19/COMPSs_APPS/kmeans/data/spark/N10000000_K100_d1000_101.txt','/gpfs/projects/bsc19/COMPSs_APPS/kmeans/data/spark/N10000000_K100_d1000_102.txt','/gpfs/projects/bsc19/COMPSs_APPS/kmeans/data/spark/N10000000_K100_d1000_103.txt','/gpfs/projects/bsc19/COMPSs_APPS/kmeans/data/spark/N10000000_K100_d1000_104.txt','/gpfs/projects/bsc19/COMPSs_APPS/kmeans/data/spark/N10000000_K100_d1000_105.txt','/gpfs/projects/bsc19/COMPSs_APPS/kmeans/data/spark/N10000000_K100_d1000_106.txt','/gpfs/projects/bsc19/COMPSs_APPS/kmeans/data/spark/N10000000_K100_d1000_107.txt','/gpfs/projects/bsc19/COMPSs_APPS/kmeans/data/spark/N10000000_K100_d1000_108.txt','/gpfs/projects/bsc19/COMPSs_APPS/kmeans/data/spark/N10000000_K100_d1000_109.txt','/gpfs/projects/bsc19/COMPSs_APPS/kmeans/data/spark/N10000000_K100_d1000_110.txt','/gpfs/projects/bsc19/COMPSs_APPS/kmeans/data/spark/N10000000_K100_d1000_111.txt','/gpfs/projects/bsc19/COMPSs_APPS/kmeans/data/spark/N10000000_K100_d1000_112.txt','/gpfs/projects/bsc19/COMPSs_APPS/kmeans/data/spark/N10000000_K100_d1000_113.txt','/gpfs/projects/bsc19/COMPSs_APPS/kmeans/data/spark/N10000000_K100_d1000_114.txt','/gpfs/projects/bsc19/COMPSs_APPS/kmeans/data/spark/N10000000_K100_d1000_115.txt']
    startTime = time.time()
    result = kmeans_frag(numV, X, k, 1e-4, 10, numFrag, initMode)
    print "Ellapsed Time(s)"
    print time.time()-startTime