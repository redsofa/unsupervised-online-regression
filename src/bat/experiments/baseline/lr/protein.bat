cd "%PROJ_ROOT%\src\python"

echo "Running baseline experiment ..."

echo 'Launching Adaptive Model ...'
python main.py ^
    --raw_data_dir "%DATA_ROOT%" ^
    --output_dir "%WORK_ROOT%/baseline/lr/protein/%NOW%" ^
    --input_csv_file std_CASP.csv ^
    --input_csv_param_file std_CASP.params ^
    --output_predictions_file protein_predictions.csv ^
    --output_stats_file protein_stats.txt ^
    --working_data_points 120 ^
    --max_samples None ^
    --output_drifts_csv_file protein_drifts.csv ^
    --algorithm sklearn_linear_regression_model ^
    --drift_detector_config "{\"detector\": \"NA\"}" ^
    --delta_threshold None ^
    --is_baseline_run True ^
    --loglevel DEBUG

echo '...'
echo '...'

echo 'Adaptive Model Evaluation ...'
python .\evaluation\evaluate.py ^
    --output_dir "%WORK_ROOT%/baseline/lr/protein/%NOW%" ^
    --predictions_file protein_predictions.csv ^
    --stats_file protein_stats.txt

echo '...'
echo '...'

echo  'Plotting results ...'
python .\plotting\main.py ^
    --input_dir "%WORK_ROOT%/baseline/lr/protein/%NOW%" ^
    --output_dir "%WORK_ROOT%/baseline/lr/protein/%NOW%" ^
    --predictions_file protein_predictions.csv ^
    --drift_file protein_drifts.csv
