##!/bin/bash
# exit when any command fails
set -e

export SRC_ROOT="$(pwd)/../../../"

echo "Running experiments on synthetic data"
#sh ./adwin/lr/synth.sh
#sh ./kswin/lr/synth.sh
#sh ./pagehinkley/lr/synth.sh
#sh ./retrain_every/lr/synth.sh
sh ./no_retrain/lr/synth.sh

## sh ./adwin/rf/synth.sh
## sh ./kswin/rf/synth.sh
## sh ./pagehinkley/rf/synth.sh
## sh ./retrain_every/rf/synth.sh
## sh ./no_retrain/rf/synth.sh

## sh ./adwin/svr/synth.sh
## sh ./kswin/svr/synth.sh
## sh ./pagehinkley/svr/synth.sh
## sh ./retrain_every/svr/synth.sh
## sh ./no_retrain/svr/synth.sh



echo "Running experiments on City of Fredericton air quality data"
#sh ./adwin/lr/fred_aq.sh
#sh ./kswin/lr/fred_aq.sh
#sh ./pagehinkley/lr/fred_aq.sh
#sh ./retrain_every/lr/fred_aq.sh
sh ./no_retrain/lr/fred_aq.sh

## sh ./adwin/rf/fred_aq.sh
## sh ./kswin/rf/fred_aq.sh
## sh ./pagehinkley/rf/fred_aq.sh
## sh ./retrain_every/rf/fred_aq.sh
## sh ./no_retrain/rf/fred_aq.sh

## sh ./adwin/svr/fred_aq.sh
## sh ./kswin/svr/fred_aq.sh
## sh ./pagehinkley/svr/fred_aq.sh
## sh ./retrain_every/svr/fred_aq.sh
## sh ./no_retrain/svr/fred_aq.sh



echo "Running experiments on UCI wine data"
#sh ./adwin/lr/uci_wine.sh
#sh ./kswin/lr/uci_wine.sh
#sh ./pagehinkley/lr/uci_wine.sh
#sh ./retrain_every/lr/uci_wine.sh
sh ./no_retrain/lr/uci_wine.sh

## sh ./adwin/rf/uci_wine.sh
## sh ./kswin/rf/uci_wine.sh
## sh ./pagehinkley/rf/uci_wine.sh
## sh ./retrain_every/rf/uci_wine.sh
## sh ./no_retrain/rf/uci_wine.sh

## sh ./adwin/svr/uci_wine.sh
## sh ./kswin/svr/uci_wine.sh
## sh ./pagehinkley/svr/uci_wine.sh
## sh ./retrain_every/svr/uci_wine.sh
## sh ./no_retrain/svr/uci_wine.sh



echo "Running experiments on UCI protein data"
#sh ./adwin/lr/uci_protein.sh
#sh ./kswin/lr/uci_protein.sh
#sh ./pagehinkley/lr/uci_protein.sh
#sh ./retrain_every/lr/uci_protein.sh
## sh ./no_retrain/lr/uci_protein.sh

## sh ./adwin/rf/uci_protein.sh
## sh ./kswin/rf/uci_protein.sh
## sh ./pagehinkley/rf/uci_protein.sh
## sh ./retrain_every/rf/uci_protein.sh
## sh ./no_retrain/rf/uci_protein.sh

## sh ./adwin/svr/uci_protein.sh
## sh ./kswin/svr/uci_protein.sh
## sh ./pagehinkley/svr/uci_protein.sh
## sh ./retrain_every/svr/uci_protein.sh
## sh ./no_retrain/svr/uci_protein.sh



echo "Running experiments on UCI std_turbine data"
#sh ./adwin/lr/uci_std_turbine.sh
#sh ./kswin/lr/uci_std_turbine.sh
#sh ./pagehinkley/lr/uci_std_turbine.sh
#sh ./retrain_every/lr/uci_std_turbine.sh
## sh ./no_retrain/lr/uci_std_turbine.sh

## sh ./adwin/rf/uci_std_turbine.sh
## sh ./kswin/rf/uci_std_turbine.sh
## sh ./pagehinkley/rf/uci_std_turbine.sh
## sh ./retrain_every/rf/uci_std_turbine.sh
## sh ./no_retrain/rf/uci_std_turbine.sh

## sh ./adwin/svr/uci_std_turbine.sh
## sh ./kswin/svr/uci_std_turbine.sh
## sh ./pagehinkley/svr/uci_std_turbine.sh
## sh ./retrain_every/svr/uci_std_turbine.sh
## sh ./no_retrain/svr/uci_std_turbine.sh



echo "Running experiments on UCI energy data"
#sh ./adwin/lr/uci_energy.sh
#sh ./kswin/lr/uci_energy.sh
#sh ./pagehinkley/lr/uci_energy.sh
#sh ./retrain_every/lr/uci_energy.sh
## sh ./no_retrain/lr/uci_energy.sh

## sh ./adwin/rf/uci_energy.sh
## sh ./kswin/rf/uci_energy.sh
## sh ./pagehinkley/rf/uci_energy.sh
## sh ./retrain_every/rf/uci_energy.sh
## sh ./no_retrain/rf/uci_energy.sh

## sh ./adwin/svr/uci_energy.sh
## sh ./kswin/svr/uci_energy.sh
## sh ./pagehinkley/svr/uci_energy.sh
## sh ./retrain_every/svr/uci_energy.sh
## sh ./no_retrain/svr/uci_energy.sh



echo "Running experiments on UCI parkinsons data"
#sh ./adwin/lr/uci_parkinsons.sh
#sh ./kswin/lr/uci_parkinsons.sh
#sh ./pagehinkley/lr/uci_parkinsons.sh
#sh ./retrain_every/lr/uci_parkinsons.sh
## sh ./no_retrain/lr/uci_parkinsons.sh

## sh ./adwin/rf/uci_parkinsons.sh
## sh ./kswin/rf/uci_parkinsons.sh
## sh ./pagehinkley/rf/uci_parkinsons.sh
## sh ./retrain_every/rf/uci_parkinsons.sh
## sh ./no_retrain/rf/uci_parkinsons.sh

## sh ./adwin/svr/uci_parkinsons.sh
## sh ./kswin/svr/uci_parkinsons.sh
## sh ./pagehinkley/svr/uci_parkinsons.sh
## sh ./retrain_every/svr/uci_parkinsons.sh
## sh ./no_retrain/svr/uci_parkinsons.sh
