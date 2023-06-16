##!/bin/bash
# exit when any command fails
set -e

export SRC_ROOT="$(pwd)/../../../"

echo "Running experiments on wetlab data"
## sh ./baseline/lr/wetlab.sh > baseline.log
## sh ./adwin_with_z1_z2/lr/wetlab.sh > adwin_with_z1_z2.log
sh ./z1_z2_only/lr/wetlab.sh > z1_z2_only.log
