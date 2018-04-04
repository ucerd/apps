#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Code for:
# Chapter 20: Practically Trivial Parallel Data Processing in a Neuroscience Laboratory
# M. Denker, B. Wiebelt, D. Fliegner, M. Diesmann, A. Morrison
# In: Analaysis of Parallel Spike Trains (2010) S. Gruen and S. Rotter (eds). Springer Series in Computational Neuroscience 7
# http://www.spiketrain-analysis.org
#
# Listing 20.1
#
# Copyright 2010 Michael Denker, B. Wiebelt, D. Fliegner, M. Diesmann, A. Morrison
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#

from numpy import *
import cPickle as pickle
from pycompss.api.task import task
from pycompss.api.parameter import *

# Analysis params
maxlag = 200
num_surrs = 20  # 1000

# Experiment Params
num_neurons = 100
num_secs = 10
num_bins = num_secs * 1000


@task(cc_original=INOUT, cc_surrs=INOUT, priority=True)
def gather(result, cc_original, cc_surrs, start, end):
    cc_original[start:end, :] = result[0]
    cc_surrs[start:end, :, :] = result[1]


@task(returns=list)
def cc_surrogate_range(fspikes, start, end, seed):
    random.seed(seed)
    f = open(fspikes, 'r')
    spikes = pickle.load(f)
    f.close()

    my_cc_orig = zeros((end - start, 2 * maxlag + 1))
    my_cc_surrs = zeros((end - start, 2 * maxlag + 1, num_surrs))
    idxrange = range(num_bins - maxlag, num_bins + maxlag + 1)
    surrs_ij = zeros((num_surrs, 2 * maxlag + 1))
    idx = row = 0
    # for all pairs ni,nj such that nj > ni
    for ni in range(num_neurons - 1):
        for nj in range(ni + 1, num_neurons):
            if idx < start:
                idx += 1
                continue
            elif idx < end:
                spike_i = spikes[ni, :]
                spike_j = spikes[nj, :]
                my_cc_orig[row, :] = correlate(spike_i, spike_j, "full")[idxrange]

                num_spikes_i = sum(spike_i)
                num_spikes_j = sum(spike_j)
                for surrogate in range(num_surrs):
                    surr_i = zeros(num_bins)
                    surr_i[random.random_integers(0, num_bins - 1, num_spikes_i)] = 1
                    surr_j = zeros(num_bins)
                    surr_j[random.random_integers(0, num_bins - 1, num_spikes_j)] = 1
                    surrs_ij[surrogate, :] = correlate(surr_i, surr_j, "full")[idxrange]

                # save point-wise 5% and 95% values of sorted surrogate ccs
                surrs_ij_sorted = sort(surrs_ij, axis=0)
                my_cc_surrs[row, :, 0] = surrs_ij_sorted[round(num_surrs * 0.95), :]
                my_cc_surrs[row, :, 1] = surrs_ij_sorted[round(num_surrs * 0.05), :]
                idx += 1
                row += 1
            else:
                return [my_cc_orig, my_cc_surrs]

    return [my_cc_orig, my_cc_surrs]


if __name__ == '__main__':
    import sys

    fragments = int(sys.argv[1])
    fspikes = sys.argv[2]

    # pre-allocate result variables
    num_ccs = (num_neurons ** 2 - num_neurons) / 2
    cc_orig = zeros((num_ccs, 2 * maxlag + 1))
    cc_surrs = zeros((num_ccs, 2 * maxlag + 1, num_surrs))
    step = num_ccs / fragments
    seed = 2398645
    delta = 1782324

    idxs = [s for s in xrange(0, num_ccs, step)]
    idxs += [num_ccs]

    # for all pairs ni,nj such that nj > ni
    for i in range(1, len(idxs)):
        result = cc_surrogate_range(fspikes, idxs[i - 1], idxs[i], seed)
        gather(result, cc_orig, cc_surrs, idxs[i - 1], idxs[i])
        seed += delta

    # wait and save results
    from pycompss.api.api import compss_wait_on
    cc_orig = compss_wait_on(cc_orig)
    cc_surrs = compss_wait_on(cc_surrs)
    f = open('result_cc_originals.dat', 'w')
    pickle.dump(cc_orig, f)
    f.close()
    f = open('result_cc_surrogates.dat', 'w')
    pickle.dump(cc_surrs, f)
    f.close()
