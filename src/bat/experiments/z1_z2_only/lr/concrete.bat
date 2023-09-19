cd %PROJ_ROOT%/src/python

echo "Running L1 L2 only experiment ..."

echo 'Launching Adaptive Model ...'
python main.py ^
    --raw_data_dir "%DATA_ROOT%" ^
    --output_dir "%WORK_ROOT%"/z1_z2_only/lr/concrete/"%NOW%" ^
    --input_csv_file std_concrete_data.csv ^
    --input_csv_param_file std_concrete_data.params ^
    --output_predictions_file concrete_predictions.csv ^
    --output_stats_file concrete_stats.txt ^
    --working_data_points 120 ^
    --max_samples None ^
    --output_drifts_csv_file concrete_drifts.csv ^
    --algorithm sklearn_linear_regression_model ^
    --drift_detector_config "{\"detector\": \"NA\"}" ^
    --delta_threshold 0.3 ^
    --is_baseline_run False ^
    --loglevel DEBUG

echo '...'
echo '...'

echo 'Adaptive Model Evaluation ...'
# Command to stat the model evaluation
python .\evaluation\evaluate.py ^
    --output_dir "%WORK_ROOT%"/z1_z2_only/lr/concrete/"%NOW%" ^
    --predictions_file concrete_predictions.csv ^
    --stats_file concrete_stats.txt

echo '...'
echo '...'

echo  'Plotting results ...'
python .\plotting\main.py ^
    --input_dir "%WORK_ROOT%"/z1_z2_only/lr/concrete/"%NOW%" ^
    --output_dir "%WORK_ROOT%"/z1_z2_only/lr/concrete/"%NOW%" ^
    --predictions_file concrete_predictions.csv ^
    --drift_file concrete_drifts.csv
