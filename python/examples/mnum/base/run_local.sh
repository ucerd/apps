#!/bin/bash -e

  # Define script variables
  scriptDir=$(pwd)/$(dirname $0)
  execFile=${scriptDir}/src/mnum.py
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
#       ./run_local.sh tracing num precision
#
# Example:
#       ./run_local.sh false 16 4096
#
