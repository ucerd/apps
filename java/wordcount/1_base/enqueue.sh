#!/bin/bash -e

workingDir=gpfs
numNodes=2
execTime=60

enqueue_compss -d --worker_working_dir=$workingDir --num_nodes=$numNodes --log_level=debug --exec_time=$execTime --appdir=$PWD wordcount.uniqueFile.Wordcount ~/singleFileDataset/data.txt ~/singleFileDataset/outputfolder/ result.txt 1024000


