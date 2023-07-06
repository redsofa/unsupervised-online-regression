##!/bin/bash
# exit when any command fails
set -e

export SRC_ROOT="$(pwd)/../../../"

echo "Running experiments on diabetes data"
sh ./baseline/lr/diabetes.sh > diabetes.log
