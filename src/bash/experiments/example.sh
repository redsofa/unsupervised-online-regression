#!/bin/bash

# Command to start the Python program
python ../../python/main.py \
    --input_stream_file ../../../datasets/small.csv \
    --stream_parameter_file ../../../datasets/small.parameters \
    --train_samples 8 \
    --test_samples 2 \
    --buffer_size 10 \
    --delta_threshold 5
