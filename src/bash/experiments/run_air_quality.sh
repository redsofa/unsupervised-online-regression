##!/bin/bash
# exit when any command fails
set -e

export SRC_ROOT="$(pwd)/../../../"

echo "Running experiments on air_quality data COGT prediction"
sh ./baseline/lr/air_quality_COGT.sh > air_quality_COGT_baseline.log
## sh ./adwin_with_z1_z2/lr/air_quality_COGT.sh > air_quality_COGT_adwin_with_z1_z2.log
sh ./z1_z2_only/lr/air_quality_COGT.sh > air_quality_COGT_z1_z2_only.log


