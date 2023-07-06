##!/bin/bash
# exit when any command fails
set -e

export SRC_ROOT="$(pwd)/../../../"

echo "Running experiments on protein data"
## sh ./baseline/lr/protein.sh > protein.log
## sh ./adwin_with_z1_z2/lr/wetlab.sh > protein.log
sh ./z1_z2_only/lr/protein.sh > protein.log
