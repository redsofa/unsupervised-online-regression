##!/bin/bash
# exit when any command fails
set -e

NOW=$( date "+%Y_%m_%d__%H_%M_%S" )
cd ${SRC_ROOT}/src/python

echo 'Launching Adaptive Model ...'
# Command to start the model
python main.py \
    --raw_data_dir ~/data/usup_reg/raw/synth \
    --output_dir ~/data/usup_reg/work/no_retrain/svr/synth/$NOW \
    --input_csv_file synth.csv \
    --input_csv_param_file synth.params \
    --output_predictions_file online_synth_predictions.csv \
    --output_drifts_csv_file online_synth_drifts.csv \
    --output_stats_file online_synth_stats.txt \
    --algorithm sklearn_svr_regression_model \
    --train_samples 100 \
    --test_samples 20

echo '\n'

echo 'Adaptive Model Evaluation'
# Command to stat the model evaluation
python evaluate.py \
    --output_dir ~/data/usup_reg/work/no_retrain/svr/synth/$NOW \
    --predictions_file online_synth_predictions.csv \
    --drift_file online_synth_drifts.csv \
    --stats_file online_synth_stats.txt \
    --plot_file online_synth.png \
    --plot_drifts False


echo '\n'

echo 'Launching baseline regression model'
# Command to start model
python baselines/linear_regression.py \
    --raw_data_dir ~/data/usup_reg/raw/synth \
    --output_dir ~/data/usup_reg/work/no_retrain/svr/synth/$NOW \
    --input_csv_file synth.csv \
    --output_predictions_file baseline_synth_predictions.csv \
    --output_stats_file baseline_synth_stats.txt \
    --train_samples 100 \
    --test_samples 20 \
    --x_col_indices 0,1,2,3\
    --y_col_index 4

echo '\n'

echo 'Launching baseline regression model evaluation'
# Command to stat the model evaluation
python evaluate.py \
    --output_dir ~/data/usup_reg/work/no_retrain/svr/synth/$NOW \
    --predictions_file baseline_synth_predictions.csv \
    --drift_file online_synth_drifts.csv \
    --stats_file baseline_synth_stats.txt \
    --plot_file baseline_synth.png \
    --plot_drifts False
