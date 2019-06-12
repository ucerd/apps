#!/bin/bash

  # Clean job files
  find . -type f -name 'compss-*.out' -delete
  find . -type f -name 'compss-*.err' -delete

  # Clean temp files
  find . -type f -name '*.sh~' -delete
  find . -type f -name '*.py~' -delete

  # Clean python compiled files
  find . -type f -name '*.pyc' -delete

  # Clean trace files
  find . -type f -name '*tar.gz' -delete

  # Remove temporal dataset
  find . -type f -name 'file*.txt' -delete
  find . -type d -name 'dataset_*' -delete
