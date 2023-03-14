##!/bin/bash
# exit when any command fails
set -e

echo 'Launching Model ...'
# Command to start the model
python ../../python/main.py \
    --raw_data_dir ~/data/usup_reg/raw/uci/parkinsons \
    --output_dir ~/data/usup_reg/work/uci/parkinsons \
    --input_csv_file parkinsons_updrs.data \
    --input_csv_param_file parkinsons_updrs.params \
    --output_predictions_file parkinsons_updrs_predictions.csv \
    --output_stats_file parkinsons_updrs_stats.txt \
    --train_samples 500 \
    --test_samples 100 \
    --buffer_size 100 \
    --delta_threshold 4
    #--delta_threshold 1e-10

echo '\n'

echo 'Model Evaluation'
# Command to stat the model evaluation
python ../../python/evaluate.py \
    --output_dir ~/data/usup_reg/work/uci/parkinsons \
    --predictions_file parkinsons_updrs_predictions.csv \
    --stats_file parkinsons_updrs_stats.txt \
    --plot_file parkinsons_updrs.png
