##!/bin/bash
# exit when any command fails
set -e

NOW=$( date "+%Y_%m_%d__%H_%M_%S" )

echo 'Launching Adaptive Model ...'
# Command to start the model
python ../../python/main.py \
    --raw_data_dir ~/data/usup_reg/raw/synth \
    --output_dir ~/data/usup_reg/work/synth/$NOW \
    --input_csv_file synth.csv \
    --input_csv_param_file synth.params \
    --output_predictions_file synth_online_predictions.csv \
    --output_drifts_csv_file synth_online_drifts.csv \
    --output_stats_file synth_online_stats.txt \
    --train_samples 100 \
    --test_samples 20 \
    --buffer_size 100 \
    --delta_threshold 0.001
    #--delta_threshold 3

echo '\n'

echo 'Adaptive Model Evaluation'
# Command to stat the model evaluation
python ../../python/evaluate.py \
    --output_dir ~/data/usup_reg/work/synth/$NOW \
    --predictions_file synth_online_predictions.csv \
    --drift_file synth_online_drifts.csv \
    --stats_file synth_online_stats.txt \
    --plot_file synth_online.png


echo '\n'

echo 'Launching baseline regression batch model'
# Command to start model
python ../../python/baselines/linear_regression.py \
    --raw_data_dir ~/data/usup_reg/raw/synth \
    --output_dir ~/data/usup_reg/work/synth/$NOW \
    --input_csv_file synth.csv \
    --output_predictions_file synth_batch_predictions.csv \
    --output_stats_file synth_batch_stats.txt \
    --train_samples 100 \
    --test_samples 20 \
    --x_col_indices 0,1,2,3\
    --y_col_index 4 

echo '\n'

echo 'Launching baseline batch Model Evaluation'
# Command to stat the model evaluation
python ../../python/evaluate.py \
    --output_dir ~/data/usup_reg/work/synth/$NOW \
    --predictions_file synth_batch_predictions.csv \
    --drift_file synth_online_drifts.csv \
    --stats_file synth_batch_stats.txt \
    --plot_file synth_batch.png
