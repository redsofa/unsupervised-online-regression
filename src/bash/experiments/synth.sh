##!/bin/bash
# exit when any command fails
set -e

NOW=$( date "+%Y_%m_%d__%H_%M_%S" )

echo 'Launching Model ...'
# Command to start the model
python ../../python/main.py \
    --raw_data_dir ~/data/usup_reg/raw/synth \
    --output_dir ~/data/usup_reg/work/synth/$NOW \
    --input_csv_file synth.csv \
    --input_csv_param_file synth.params \
    --output_predictions_file synth_predictions.csv \
    --output_drifts_csv_file synth_drifts.csv \
    --output_stats_file synth_stats.txt \
    --train_samples 100 \
    --test_samples 40 \
    --buffer_size 40 \
    --delta_threshold 0.2
    #--delta_threshold 3

echo '\n'

echo 'Model Evaluation'
# Command to stat the model evaluation
python ../../python/evaluate.py \
    --output_dir ~/data/usup_reg/work/synth/$NOW \
    --predictions_file synth_predictions.csv \
    --drift_file synth_drifts.csv \
    --stats_file synth_stats.txt \
    --plot_file synth.png
