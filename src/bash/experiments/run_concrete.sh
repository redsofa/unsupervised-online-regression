##!/bin/bash
# exit when any command fails
set -e

export NOW=$( date "+%Y_%m_%d__%H_%M_%S" )
export PROJ_ROOT="$(pwd)/../../../"
export DATA_ROOT=~/data/usup_reg/raw/uci/concrete
export WORK_ROOT=~/data/usup_reg/work


echo "Running experiments on concrete data"

mkdir -p ${WORK_ROOT}/baseline/lr/concrete/${NOW} 
sh ./baseline/lr/concrete.sh &> ${WORK_ROOT}/baseline/lr/concrete/${NOW}/concrete_baseline.log

mkdir -p ${WORK_ROOT}/adwin_with_z1_z2/lr/concrete/${NOW} 
sh ./adwin_with_z1_z2/lr/concrete.sh &> ${WORK_ROOT}/adwin_with_z1_z2/lr/concrete/${NOW}/concrete_adwin_with_z1_z2.log

mkdir -p ${WORK_ROOT}/z1_z2_only/lr/concrete/${NOW} 
sh ./z1_z2_only/lr/concrete.sh &> ${WORK_ROOT}/z1_z2_only/lr/concrete/${NOW}/concrete_z1_z2_only.log
