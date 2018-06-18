#!/bin/bash -e

  # Define script variables
  scriptDir=$(dirname $0)
  execFile=src/sort.py
  appClasspath=${scriptDir}/src/
  appPythonpath=${scriptDir}/src/

  # Retrieve arguments
  tracing=$1

  # Leave application args on $@
  shift 1

  # Enqueue the application
  runcompss \
    --tracing=$tracing \
    --classpath=$appClasspath \
    --pythonpath=$appPythonpath \
    --lang=python \
    $execFile $@


######################################################
# APPLICATION EXECUTION EXAMPLE
# Call:
#       ./run_local.sh tracing file numFrag numRange
#
# Example:
#       # Run the generator consider the output path for running
#       ./run_local.sh false /path/to/dataset/dataset.txt 5 600
#