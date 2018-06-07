#!/bin/bash -e

  # Define script directory for relative calls
  scriptDir=$(dirname $0)

  # Set common arguments
  jobDependency=None
  numNodes=2
  executionTime=30
  tasksPerNode=16
  tracing=false
  
  # Set arguments
  appArgs="1024 data/spikes.dat"

  # Execute specifcversion launch  
  ${scriptDir}/base/launch.sh $jobDependency $numNodes $executionTime $tasksPerNode $tracing $appArgs
