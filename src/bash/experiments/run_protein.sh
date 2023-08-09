##!/bin/bash
# exit when any command fails
set -e

export NOW=$( date "+%Y_%m_%d__%H_%M_%S" )
export PROJ_ROOT="$(pwd)/../../../"
export DATA_ROOT=~/data/usup_reg/raw/uci/protein
export WORK_ROOT=~/data/usup_reg/work
 

echo "Running experiments on protein data ... "

mkdir -p ${WORK_ROOT}/baseline/lr/protein/${NOW} 
sh ./baseline/lr/protein.sh &> ${WORK_ROOT}/baseline/lr/protein/${NOW}/protein_baseline.log

mkdir -p ${WORK_ROOT}/z1_z2_only/lr/protein/${NOW} 
sh ./z1_z2_only/lr/protein.sh &> ${WORK_ROOT}/z1_z2_only/lr/protein/${NOW}/protein_z1_z2_only.log

mkdir -p ${WORK_ROOT}/adwin_with_z1_z2/lr/protein/${NOW}
sh ./adwin_with_z1_z2/lr/protein.sh &> ${WORK_ROOT}/adwin_with_z1_z2/lr/protein/${NOW}/protein_adwin_with_z1_z2.log
