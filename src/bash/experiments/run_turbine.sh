##!/bin/bash
# exit when any command fails
set -e

export NOW=$( date "+%Y_%m_%d__%H_%M_%S" )
export PROJ_ROOT="$(pwd)/../../../"
export DATA_ROOT=~/data/usup_reg/raw/uci/turbine
export WORK_ROOT=~/data/usup_reg/work


# echo "Running experiments on turbine data TEY prediction"

# mkdir -p ${WORK_ROOT}/baseline/lr/turbine_TEY/${NOW}
# sh ./baseline/lr/turbine_TEY.sh &> ${WORK_ROOT}/baseline/lr/turbine_TEY/${NOW}/turbine_TEY.log

# mkdir -p ${WORK_ROOT}/adwin_with_z1_z2/lr/turbine_TEY/${NOW}
# sh ./adwin_with_z1_z2/lr/turbine_TEY.sh &> ${WORK_ROOT}/adwin_with_z1_z2/lr/turbine_TEY/${NOW}/urbine_TEY_adwin_with_z1_z2.log

# mkdir -p ${WORK_ROOT}/z1_z2_only/lr/turbine_TEY/${NOW}
# sh ./z1_z2_only/lr/turbine_TEY.sh &> ${WORK_ROOT}/z1_z2_only/lr/turbine_TEY/${NOW}/turbine_TEY_z1_z2_only.log



echo "Running experiments on turbine data CO prediction"

mkdir -p ${WORK_ROOT}/baseline/lr/turbine_CO/${NOW}
sh ./baseline/lr/turbine_CO.sh &> ${WORK_ROOT}/baseline/lr/turbine_CO/${NOW}/turbine_CO_baseline.log

mkdir -p ${WORK_ROOT}/adwin_with_z1_z2/lr/turbine_CO/${NOW}
sh ./adwin_with_z1_z2/lr/turbine_CO.sh &> ${WORK_ROOT}/adwin_with_z1_z2/lr/turbine_CO/${NOW}/turbine_CO_adwin_with_z1_z2.log

mkdir -p ${WORK_ROOT}/z1_z2_only/lr/turbine_CO/${NOW}
sh ./z1_z2_only/lr/turbine_CO.sh &> ${WORK_ROOT}/z1_z2_only/lr/turbine_CO/${NOW}/turbine_CO_z1_z2_only.log


#
#echo "Running experiments on turbine data NOX prediction"
#sh ./baseline/lr/turbine_NOX.sh &> turbine_NOX_baseline.log
#sh ./adwin_with_z1_z2/lr/turbine_NOX.sh &> turbine_NOX_adwin_with_z1_z2.log
#sh ./z1_z2_only/lr/turbine_NOX.sh &> turbine_NOX_z1_z2_only.log
