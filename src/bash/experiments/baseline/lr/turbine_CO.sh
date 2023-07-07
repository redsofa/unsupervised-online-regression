##!/bin/bash
# exit when any command fails
set -e

NOW=$( date "+%Y_%m_%d__%H_%M_%S" )
cd ${SRC_ROOT}/src/python

echo 'Launching Adaptive Model ...'
# Command to start the model
python main.py \
    --raw_data_dir ~/data/usup_reg/raw/uci/turbine \
    --output_dir ~/data/usup_reg/work/baseline/lr/turbine/$NOW \
    --input_csv_file std_gt_all.csv \
    --input_csv_param_file std_gt_all_CO.params \
    --output_predictions_file std_gt_all_CO_predictions.csv \
    --output_stats_file std_gt_all_CO_stats.txt \
    --working_data_points 120 \
    --max_samples None \
    --output_drifts_csv_file std_gt_all_CO_drifts.csv \
    --algorithm sklearn_linear_regression_model \
    --drift_detector_config '{"detector": "NA"}' \
    --delta_threshold None \
    --is_baseline_run True \
    --loglevel DEBUG

echo '\n'

echo 'Adaptive Model Evaluation'
# Command to stat the model evaluation
python evaluate.py \
    --output_dir ~/data/usup_reg/work/baseline/lr/turbine/$NOW \
    --predictions_file std_gt_all_CO_predictions.csv \
    --drift_file std_gt_all_CO_drifts.csv \
    --stats_file std_gt_all_CO_stats.txt \
    --plot_file std_gt_all_CO.png \
    --plot_drifts False
