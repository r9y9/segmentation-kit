# coding: utf-8

import numpy as np
import os
import MeCab
import jaconv

from nnmnkwii.datasets import jsut
from os.path import join, splitext, basename

from subprocess import Popen, PIPE


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


if __name__ == "__main__":
    from params import in_dir, dst_dir, subsets

    transcriptions = jsut.TranscriptionDataSource(
        in_dir, subsets=subsets).collect_files()
    wav_paths = jsut.WavFileDataSource(
        in_dir, subsets=subsets).collect_files()

    c = 0
    os.makedirs(dst_dir, exist_ok=True)
    for idx, (text, wav_path) in enumerate(zip(transcriptions, wav_paths)):
        name = splitext(basename(wav_path))[0]

        label_path = join(dst_dir, name + ".lab")
        with open(label_path) as f:
            lines = f.readlines()
            if len(lines) == 0:
                with open(join(dst_dir, name + ".txt")) as ff:
                    print(idx, label_path, text, ff.readlines())
                c += 1
            else:
                openjtalk_label_path = join(dst_dir, name + ".openjtalk.lab")
                with open(openjtalk_label_path) as of:
                    jlines = of.readlines()
                    if len(lines) != len(jlines):
                        print("Somethihng vad!")

    print("Failed number of utterances:", c)
