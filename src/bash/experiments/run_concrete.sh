##!/bin/bash
# exit when any command fails
set -e

export SRC_ROOT="$(pwd)/../../../"

echo "Running experiments on concrete data"
sh ./baseline/lr/concrete.sh > concrete_baseline.log
sh ./adwin_with_z1_z2/lr/concrete.sh > concrete_adwin_with_z1_z2.log
sh ./z1_z2_only/lr/concrete.sh > concrete_z1_z2_only.log
