##!/bin/bash
# exit when any command fails
set -e

NOW=$( date "+%Y_%m_%d__%H_%M_%S" )
cd ${SRC_ROOT}/src/python

echo 'Launching Adaptive Model ...'
# Command to start the model
python main.py \
    --raw_data_dir ~/data/usup_reg/raw/uci/air_quality \
    --output_dir ~/data/usup_reg/work/adwin_with_z1_z2/lr/air_quality/$NOW \
    --input_csv_file std_AirQualityUCI.csv \
    --input_csv_param_file std_AirQualityUCI_NO2.params \
    --output_predictions_file std_AirQualityUCI_NO2_predictions.csv \
    --output_stats_file std_AirQualityUCI_NO2_stats.txt \
    --working_data_points 120 \
    --max_samples None \
    --output_drifts_csv_file std_AirQualityUCI_NO2_drifts.csv \
    --algorithm sklearn_linear_regression_model \
    --drift_detector_config '{"detector": "ADWIN", "required_feature_drifts": 1, "delta": 0.1e-15}' \
    --delta_threshold 0.1e-4 \
    --is_baseline_run False \
    --loglevel DEBUG

echo '\n'

echo 'Adaptive Model Evaluation'
# Command to stat the model evaluation
python evaluate.py \
    --output_dir ~/data/usup_reg/work/adwin_with_z1_z2/lr/air_quality/$NOW \
    --predictions_file std_AirQualityUCI_NO2_predictions.csv \
    --drift_file std_AirQualityUCI_NO2_drifts.csv \
    --stats_file std_AirQualityUCI_NO2_stats.txt \
    --plot_file std_AirQualityUCI_NO2.png \
    --plot_drifts True
