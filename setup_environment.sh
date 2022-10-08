#!bin/bash

# create enviroment using Miniconda (or Anaconda)
conda create -n continual_clip python=3.8
conda activate continual_clip

# install pytorch
pip install torch==1.8.2 torchvision==0.9.2 torchaudio==0.8.2 \
    --extra-index-url https://download.pytorch.org/whl/lts/1.8/cu111

# install other dependencies
pip install -r requirements.txt

# install CLIP
pip install git+https://github.com/openai/CLIP.git

