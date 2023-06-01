##!/bin/bash
# exit when any command fails
set -e

export SRC_ROOT="$(pwd)/../../../"

sh ./uci_wine.sh
sh ./uci_energy.sh
sh ./uci_parkinsons.sh
sh ./uci_protein.sh
sh ./fred_aq.sh
sh ./synth.sh
