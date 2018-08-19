#!/bin/bash

for s in fujitou tsuchiya uemura
do
    for e in normal happy angry
    do
        cat << EOS > params.py
# coding: utf-8
from os.path import join, expanduser
from nnmnkwii.datasets import jsut, voice_statistics

dataset = voice_statistics
dataset_script_kwargs = {"column": "yomi"}
dataset_wav_kwargs = {"speakers": ["$s"], "emotions": ["$e"]}

in_dir = join(expanduser("~"), "data/voice-statistics/")
dst_dir = "outputs_{}_{}".format(dataset_wav_kwargs["speakers"][0], dataset_wav_kwargs["emotions"][0])
EOS
        cat params.py
        ./run.sh
    done
done
