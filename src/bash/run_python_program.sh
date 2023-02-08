#!/bin/bash

# Command to start the Python program
python ../python/main.py \
    --input_file_name ../../datasets/small.csv \
    --stream_parameters ../../datasets/small.parameters \
    --buffer_size 10 \
    --max_samples 15 \
    --pre_train_size 5
