#!bin/bash

# for imagenet-100 dataset; 10 classes/task
# python main.py \
#     --config-path configs/class \
#     --config-name cifar100_10-10.yaml \
#     dataset_root="../datasets/" \
#     class_order="class_orders/cifar100.yaml"

# for imagenet-1000 dataset; 100 classes/task
# python main.py \
#     --config-path configs/class \
#     --config-name imagenet1000_100-100.yaml \
#     dataset_root="../datasets/" \
#     class_order="class_orders/imagenet1000.yaml"

python main.py \
    --config-path configs/domain \
    --config-name core50.yaml \
    dataset_root="../datasets/" 