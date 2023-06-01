##!/bin/bash
# exit when any command fails
set -e

NOW=$( date "+%Y_%m_%d__%H_%M_%S" )
cd ${SRC_ROOT}/src/python

echo 'Launching Adaptive Model ...'
# Command to start the model
python main.py \
    --raw_data_dir ~/data/usup_reg/raw/synth \
    --output_dir ~/data/usup_reg/work/kswin/rf/synth/$NOW \
    --input_csv_file synth.csv \
    --input_csv_param_file synth.params \
    --output_predictions_file online_synth_predictions.csv \
    --output_drifts_csv_file online_synth_drifts.csv \
    --output_stats_file online_synth_stats.txt \
    --algorithm sklearn_randomforest_regression_model \
    --train_samples 100 \
    --test_samples 20 \
    --drift_detector KSWIN

echo '\n'

echo 'Adaptive Model Evaluation'
# Command to stat the model evaluation
python evaluate.py \
    --output_dir ~/data/usup_reg/work/kswin/rf/synth/$NOW \
    --predictions_file online_synth_predictions.csv \
    --drift_file online_synth_drifts.csv \
    --stats_file online_synth_stats.txt \
    --plot_file online_synth.png \
    --plot_drifts True
