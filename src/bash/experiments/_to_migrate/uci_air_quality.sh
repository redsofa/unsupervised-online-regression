##!/bin/bash
# exit when any command fails
set -e

NOW=$( date "+%Y_%m_%d__%H_%M_%S" )

echo 'Launching Adaptive Model ...'
# Command to start the model
python ../../python/main.py \
    --raw_data_dir ~/data/usup_reg/raw/uci/air_quality \
    --output_dir ~/data/usup_reg/work/uci/air_quality/$NOW \
    --input_csv_file KNN_UCI.csv \
    --input_csv_param_file KNN_UCI.params \
    --output_predictions_file KNN_UCI_online_predictions.csv \
    --output_drifts_csv_file KNN_UCI_online_drifts.csv \
    --output_stats_file KNN_UCI_online_stats.txt \
    --train_samples 100 \
    --test_samples 20 \
    --buffer_size 100 \
    --delta_threshold 0.001
    #--delta_threshold 3

echo '\n'

echo 'Adaptive Model Evaluation'
# Command to stat the model evaluation
python ../../python/evaluate.py \
    --output_dir ~/data/usup_reg/work/uci/air_quality/$NOW \
    --predictions_file KNN_UCI_online_predictions.csv \
    --drift_file KNN_UCI_online_drifts.csv \
    --stats_file KNN_UCI_online_stats.txt \
    --plot_file KNN_UCI_online.png


echo '\n'

echo 'Launching baseline regression batch model'
# Command to start model
python ../../python/baselines/linear_regression.py \
    --raw_data_dir ~/data/usup_reg/raw/uci/air_quality \
    --output_dir ~/data/usup_reg/work/uci/air_quality/$NOW \
    --input_csv_file KNN_UCI.csv \
    --output_predictions_file KNN_UCI_batch_predictions.csv \
    --output_stats_file KNN_UCI_batch_stats.txt \
    --train_samples 100 \
    --test_samples 20 \
    --x_col_indices 0,1,2,3,4,5,6,7,8,9,10,11,12\
    --y_col_index 13

echo '\n'

echo 'Launching baseline batch Model Evaluation'
# Command to stat the model evaluation
python ../../python/evaluate.py \
    --output_dir ~/data/usup_reg/work/uci/air_quality/$NOW \
    --predictions_file KNN_UCI_batch_predictions.csv \
    --drift_file KNN_UCI_online_drifts.csv \
    --stats_file KNN_UCI_batch_stats.txt \
    --plot_file KNN_UCI_batch.png
