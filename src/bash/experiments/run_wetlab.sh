##!/bin/bash
# exit when any command fails
set -e

export SRC_ROOT="$(pwd)/../../../"

echo "Running experiments on wetlab data"
sh ./adwin/lr/wetlab.sh
#sh ./kswin/lr/wetlab.sh
##sh ./pagehinkley/lr/wetlab.sh
##sh ./retrain_every/lr/wetlab.sh
##sh ./no_retrain/lr/wetlab.sh

sh ./adwin/rf/wetlab.sh
##sh ./kswin/rf/wetlab.sh
##sh ./pagehinkley/rf/wetlab.sh
##sh ./retrain_every/rf/wetlab.sh
##sh ./no_retrain/rf/wetlab.sh

sh ./adwin/svr/wetlab.sh
##sh ./kswin/svr/wetlab.sh
##sh ./pagehinkley/svr/wetlab.sh
##sh ./retrain_every/svr/wetlab.sh
##sh ./no_retrain/svr/wetlab.sh
