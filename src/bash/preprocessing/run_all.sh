##!/bin/bash
# exit when any command fails
set -e

export SRC_ROOT="$(pwd)/../../../"

# Imputation
#
# sh uci_air_quality_impute.sh

# Standardization 
#
# sh ./uci_turbine.sh
# sh ./uci_protein.sh
# sh ./uci_concrete.sh
sh ./uci_air_quality_std.sh
