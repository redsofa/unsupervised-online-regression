##!/bin/bash
# exit when any command fails
set -e

echo 'Launching Model ...'
# Command to start the model
python ../../python/main.py \
    --raw_data_dir ~/data/usup_reg/raw/uci/turbine \
    --output_dir ~/data/usup_reg/work/uci/turbine \
    --input_csv_file gt_2015.csv \
    --input_csv_param_file gt_2015.params \
    --output_predictions_file gt_2015_predictions.csv \
    --output_stats_file gt_2015_stats.txt \
    --train_samples 100 \
    --test_samples 40 \
    --buffer_size 40 \
    --delta_threshold 2
    #--delta_threshold 1e-10

echo '\n'

echo 'Model Evaluation'
# Command to stat the model evaluation
python ../../python/evaluate.py \
    --output_dir ~/data/usup_reg/work/uci/turbine \
    --predictions_file gt_2015_predictions.csv \
    --stats_file gt_2015_stats.txt \
    --plot_file gt_2015.png
