#!/bin/bash

# Command to start the Python program
python ../python/main.py \
    --input_stream_file ~/data/UCI/pp_gas_emission/gt_2015.csv \
    --stream_parameter_file ~/data/UCI/pp_gas_emission/gt_2015.params \
    --train_samples 2000 \
    --test_samples 400 \
    --buffer_size 2400 \
    --delta_threshold 5
