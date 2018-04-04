#!/bin/bash -e

  # Define script variables
  scriptDir=$(pwd)/$(dirname $0)
  execFile=${scriptDir}/src/kmeans.py
  appClasspath=${scriptDir}/src/
  appPythonpath=${scriptDir}/src/

  # Retrieve arguments
  jobDependency=$1
  numNodes=$2
  executionTime=$3
  tasksPerNode=$4
  tracing=$5

  # Leave application args on $@
  shift 5

  # Enqueue the application
  enqueue_compss \
    --job_dependency=$jobDependency \
    --num_nodes=$numNodes \
    --cpus_per_node=$tasksPerNode \
    --exec_time=$executionTime \
    --master_working_dir=. \
    --worker_working_dir=gpfs \
    --library_path=/gpfs/apps/MN3/INTEL/mkl/lib/intel64 \
    --tracing=$tracing \
    --classpath=$appClasspath \
    --pythonpath=$appPythonpath \
    --lang=python \
    -d \
    $execFile $@


######################################################
# APPLICATION EXECUTION EXAMPLE
# Call:
#       ./launch.sh jobDependency numNodes executionTime tasksPerNode tracing dataset_path numV dim k
#
# Example:
#       ./launch.sh None 2 5 16 false /path/to/dataset/ 16000 3 4
#
#  dataset_path = Path where the dataset is
#  numV = Number of points
#  dim = Number of dimensions
#  k = Number of centers