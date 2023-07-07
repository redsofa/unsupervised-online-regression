##!/bin/bash
# exit when any command fails
set -e

export SRC_ROOT="$(pwd)/../../../"

echo "Running experiments on turbine data TEY prediction"
sh ./baseline/lr/turbine_TEY.sh > turbine_TEY_baseline.log
## sh ./adwin_with_z1_z2/lr/turbine_TEY.sh > turbine_TEY_adwin_with_z1_z2.log
sh ./z1_z2_only/lr/turbine_TEY.sh > turbine_TEY_z1_z2_only.log

echo "Running experiments on turbine data CO prediction"
sh ./baseline/lr/turbine_CO.sh > turbine_CO_baseline.log
## sh ./adwin_with_z1_z2/lr/turbine_CO.sh > turbine_CO_adwin_with_z1_z2.log
sh ./z1_z2_only/lr/turbine_CO.sh > turbine_CO_z1_z2_only.log

echo "Running experiments on turbine data NOX prediction"
sh ./baseline/lr/turbine_NOX.sh > turbine_NOX_baseline.log
## sh ./adwin_with_z1_z2/lr/turbine_NOX.sh > turbine_NOX_adwin_with_z1_z2.log
sh ./z1_z2_only/lr/turbine_NOX.sh > turbine_NOX_z1_z2_only.log
