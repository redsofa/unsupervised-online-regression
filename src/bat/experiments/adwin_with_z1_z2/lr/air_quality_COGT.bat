cd "%PROJ_ROOT%\src\python"

echo "Running ADWIN with Z1 Z2 experiment ..."

echo 'Launching Adaptive Model ...'
python main.py ^
    --raw_data_dir "%DATA_ROOT%" ^
    --output_dir "%WORK_ROOT%/adwin_with_z1_z2/lr/air_quality_COGT/%NOW%" ^
    --input_csv_file std_AirQualityUCI.csv ^
    --input_csv_param_file std_AirQualityUCI_COGT.params ^
    --output_predictions_file std_AirQualityUCI_COGT_predictions.csv ^
    --output_stats_file std_AirQualityUCI_COGT_stats.txt ^
    --working_data_points 120 ^
    --max_samples None ^
    --output_drifts_csv_file std_AirQualityUCI_COGT_drifts.csv ^
    --algorithm sklearn_linear_regression_model ^
    --drift_detector_config "{\"detector\": \"ADWIN\", \"required_feature_drifts\": 1, \"delta\": 0.1e-15}" ^
    --delta_threshold 0.1e-4 ^
    --is_baseline_run False ^
    --loglevel DEBUG

echo '...'
echo '...'

echo 'Adaptive Model Evaluation ...'
python .\evaluation\evaluate.py ^
    --output_dir "%WORK_ROOT%/adwin_with_z1_z2/lr/air_quality_COGT/%NOW%" ^
    --predictions_file std_AirQualityUCI_COGT_predictions.csv ^
    --stats_file std_AirQualityUCI_COGT_stats.txt

echo '...'
echo '...'

echo  'Plotting results ...'
python .\plotting\main.py ^
    --input_dir "%WORK_ROOT%/adwin_with_z1_z2/lr/air_quality_COGT/%NOW%" ^
    --output_dir "%WORK_ROOT%/adwin_with_z1_z2/lr/air_quality_COGT/%NOW%" ^
    --predictions_file std_AirQualityUCI_COGT_predictions.csv ^
    --drift_file std_AirQualityUCI_COGT_drifts.csv