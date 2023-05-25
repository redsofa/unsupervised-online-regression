##!/bin/bash
# exit when any command fails
set -e

export SRC_ROOT="$(pwd)/../../../"

#echo "Running experiments on synthetic data"
#sh ./adwin/lr/synth.sh
#sh ./kswin/lr/synth.sh
#sh ./pagehinkley/lr/synth.sh
#sh ./retrain_every/lr/synth.sh

#echo "Running experiments on City of Fredericton air quality data"
#sh ./adwin/lr/fred_aq.sh
#sh ./kswin/lr/fred_aq.sh
#sh ./pagehinkley/lr/fred_aq.sh
#sh ./retrain_every/lr/fred_aq.sh

#echo "Running experiments on UCI wine data"
#sh ./adwin/lr/uci_wine.sh
#sh ./kswin/lr/uci_wine.sh
#sh ./pagehinkley/lr/uci_wine.sh
#sh ./retrain_every/lr/uci_wine.sh

#echo "Running experiments on UCI protein data"
sh ./adwin/lr/uci_protein.sh
#sh ./kswin/lr/uci_protein.sh
#sh ./pagehinkley/lr/uci_protein.sh
#sh ./retrain_every/lr/uci_protein.sh
