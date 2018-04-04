#!/usr/bin/python
# -*- coding: utf-8 -*-
from pycompss.api.task import task
from pycompss.api.parameter import *
from pycompss.api.constraint import constraint
from scipy import linalg, random
import numpy as np
import ctypes

@constraint (ComputingUnits="${ComputingUnits}")
@task(returns=list)
def createBlock(BSIZE, MKLProc, diag):
    import os
    os.environ["MKL_NUM_THREADS"]=str(MKLProc)
    block = np.array(np.random.random((BSIZE, BSIZE)), dtype=np.double,copy=False)
    mb = np.matrix(block, dtype=np.double, copy=False)
    mb = mb + np.transpose(mb)
    if diag:
        mb = mb + 2*BSIZE*np.eye(BSIZE)
    return mb

def genMatrix(MKLProc):
    for i in range(MSIZE):
        A.append([])
        for j in range(MSIZE):
            A[i].append([])
    for i in range(MSIZE):
        mb = createBlock(BSIZE, MKLProc, True)
        A[i][i]=mb
        for j in range(i+1,MSIZE):
            mb = createBlock(BSIZE, MKLProc, False)
            A[i][j]=mb
            A[j][i]=mb


@constraint(ComputingUnits="${ComputingUnits}")
@task(returns=np.ndarray)
def potrf(A, MKLProc):
    from scipy.linalg.lapack import dpotrf
    import os
    os.environ['MKL_NUM_THREADS']=str(MKLProc)
    A = dpotrf(A, lower=True)[0]
    return A

@constraint(ComputingUnits="${ComputingUnits}")
@task(returns=np.ndarray)
def solve_triangular(A, B, MKLProc):
    from scipy.linalg import solve_triangular
    from numpy import transpose
    import os
    os.environ['MKL_NUM_THREADS']=str(MKLProc)
    B = transpose(B)
    B = solve_triangular(A, B, lower=True)  # , trans='T'
    B = transpose(B)
    return B

@constraint(ComputingUnits="${ComputingUnits}")
@task(returns=np.ndarray)
def gemm(alpha, A, B, C, beta, MKLProc):
    from scipy.linalg.blas import dgemm
    from numpy import transpose
    import os
    os.environ['MKL_NUM_THREADS']=str(MKLProc)
    B = transpose(B)
    C = dgemm(alpha, A, B, c=C, beta=beta)
    return C

@constraint(ComputingUnits="${ComputingUnits}")
@task(returns=np.ndarray)
def syrk(A, B, MKLProc):
    from scipy.linalg.blas import dsyrk
    import os
    os.environ['MKL_NUM_THREADS']=str(MKLProc)
    alpha = -1.0
    beta = 1.0
    B = dsyrk(alpha, A, c=B, beta=beta, lower=True)
    return B

def cholesky_blocked(A):
    import os
    cont = 0
    for k in range(MSIZE):
        # Diagonal block factorization
        A[k][k] = potrf(A[k][k], mkl_threads)
        cont += 1
        # Triangular systems
        for i in range(k+1, MSIZE):
            A[i][k] = solve_triangular(A[k][k], A[i][k], mkl_threads)
            A[k][i] = np.zeros((BSIZE,BSIZE))
            cont += 1

        # update trailing matrix
        for i in range(k+1, MSIZE):
            for j in range(i, MSIZE):
                A[j][i] = gemm(-1.0, A[j][k], A[i][k], A[j][i], 1.0, mkl_threads)
                cont += 1
            #A[j][i] = syrk(A[j][k], A[j][i], mkl_threads)
            cont += 1

    print "Number of tasks: {}".format(cont)
    return A

def joinMatrix(A):
    joinMat=np.matrix([[]])
    for i in range(0,len(A)):
        currRow=A[i][0]
        for j in range(1,len(A[i])):
            currRow=np.bmat([[currRow,A[i][j]]])
        if i == 0:
            joinMat = currRow
        else:
            joinMat = np.bmat([[joinMat],[currRow]])
    return np.matrix(joinMat)

def cholesky():
    import time
    import sys
    import os
    import copy
    from scipy.linalg.blas import dgemm
    from pycompss.api.api import compss_barrier
    from pycompss.api.api import compss_wait_on
    MSIZE = int(sys.argv[1])
    BSIZE = int(sys.argv[2])
    mkl_threads = int(sys.argv[3])

    # Generate de matrix
    startTime = time.time()

    # Generate supermatrix
    A = []
    res = []

    genMatrix(mkl_threads)
    compss_barrier()
    initTime = time.time() - startTime

    startDecompTime = time.time()

    res = cholesky_blocked(A)

    compss_barrier()

    decompTime = time.time() - startDecompTime
    totalTime = decompTime + initTime


    print "---------- PARAMS ----------"
    print "MSIZE:{}".format(MSIZE)
    print "BSIZE:{}".format(BSIZE)

    print "initT:{}".format(initTime)
    print "decompT:{}".format(decompTime)
    print "totalTime:{}".format(totalTime)

    print "----------------------------"

if __name__ == "__main__":
    cholesky()