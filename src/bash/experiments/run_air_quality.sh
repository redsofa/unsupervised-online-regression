##!/bin/bash
# exit when any command fails
set -e

export NOW=$( date "+%Y_%m_%d__%H_%M_%S" )
export PROJ_ROOT="$(pwd)/../../../"
export DATA_ROOT=~/data/usup_reg/raw/uci/air_quality
export WORK_ROOT=~/data/usup_reg/work


echo "Running experiments on air_quality data COGT prediction"

mkdir -p ${WORK_ROOT}/baseline/lr/air_quality_COGT/${NOW}
sh ./baseline/lr/air_quality_COGT.sh &> ${WORK_ROOT}/baseline/lr/air_quality_COGT/${NOW}/air_quality_COGT_baseline.log

# mkdir -p ${WORK_ROOT}/adwin_with_z1_z2lr/air_quality_COGT/${NOW}
# sh ./adwin_with_z1_z2/lr/air_quality_COGT.sh &> ${WORK_ROOT}/adwin_with_z1_z2lr/air_quality_COGT/${NOW}/air_quality_COGT_adwin_with_z1_z2.log

# mkdir -p ${WORK_ROOT}/z1_z2_only/air_quality_COGT/${NOW}
# sh ./z1_z2_only/lr/air_quality_COGT.sh &> ${WORK_ROOT}/z1_z2_only/air_quality_COGT/${NOW}/air_quality_COGT_z1_z2_only.log



# echo "Running experiments on air_quality data NO2 prediction"
# 
# mkdir -p ${WORK_ROOT}/baseline/lr/air_quality_NO2/${NOW}
# sh ./baseline/lr/air_quality_NO2.sh &> ${WORK_ROOT}/baseline/lr/air_quality_NO2/${NOW}/air_quality_NO2_baseline.log

# mkdir -p ${WORK_ROOT}/adwin_with_z1_z2/lr/air_quality_NO2/${NOW}
# sh ./adwin_with_z1_z2/lr/air_quality_NO2.sh &> ${WORK_ROOT}/adwin_with_z1_z2/lr/air_quality_NO2/${NOW}/air_quality_NO2_adwin_with_z1_z2.log
# 
# mkdir -p ${WORK_ROOT}/z1_z2_only/lr/air_quality_NO2/${NOW}
# sh ./z1_z2_only/lr/air_quality_NO2.sh &> ${WORK_ROOT}/z1_z2_only/lr/air_quality_NO2/${NOW}/air_quality_NO2_z1_z2_only.log
# 
# 
# 
# echo "Running experiments on air_quality data NMHCGT prediction"
# 
# mkdir -p ${WORK_ROOT}/baseline/lr/air_quality_NMHCGT/${NOW}
# sh ./baseline/lr/air_quality_NMHCGT.sh &> ${WORK_ROOT}/baseline/lr/air_quality_NMHCGT/${NOW}/air_quality_NMHCGT_baseline.log
# 
# mkdir -p ${WORK_ROOT}/adwin_with_z1_z2/lr/air_quality_NMHCGT/${NOW}
# sh ./adwin_with_z1_z2/lr/air_quality_NMHCGT.sh &> ${WORK_ROOT}/adwin_with_z1_z2/lr/air_quality_NMHCGT/${NOW}/air_quality_NMHCGT_adwin_with_z1_z2.log
# 
# mkdir -p ${WORK_ROOT}/z1_z2_only/lr/air_quality_NMHCGT/${NOW}
# sh ./z1_z2_only/lr/air_quality_NMHCGT.sh &> ${WORK_ROOT}/z1_z2_only/lr/air_quality_NMHCGT/${NOW}/air_quality_NMHCGT_z1_z2_only.log
