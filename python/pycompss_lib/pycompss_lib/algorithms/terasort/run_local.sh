#!/bin/bash -e

  # Define script directory for relative calls
  scriptDir=$(pwd)

  # Set common arguments
  numFragments=10
  numEntries=100
  tracing=false

  # Set arguments
  appArgs="${numFragments} ${numEntries}"

  # Execute specific version launch
  cd base
  # cdbasebase_oo
  ./run_local.sh $tracing $appArgs
  cd ..