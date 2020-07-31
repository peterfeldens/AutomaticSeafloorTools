#!/usr/bin/env bash
CUDA_VISIBLE_DEVICES=0 python main.py \
    --output_dir /Users/peter/Work/boulderdetection/data/interim/super_resolution/BalticSeaValidation/UHR/valid_UHR_pad32_model20000 \
    --summary_dir = /Users/peter/Work/  \
    --mode inference \
    --is_training False \
    --task SRResnet \
    --batch_size 16 \
    --input_dir_LR /Users/peter/Work/boulderdetection/data/interim/super_resolution/BalticSeaValidation/HR/valid_100pixels_padded32 \
    --num_resblock 16 \
    --perceptual_mode MSE \
    --pre_trained_model True \
    --checkpoint /Users/peter/Work/boulderdetection/models/super_resolution/Baltic_Sea_x2_30crop/model-20000
