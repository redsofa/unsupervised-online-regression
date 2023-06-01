##!/bin/bash
# exit when any command fails
set -e

export SRC_ROOT="$(pwd)/../../../"

sh ./uci_wine.sh
sh ./uci_energy.sh
