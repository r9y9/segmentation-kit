import numpy as np
import os
from nnmnkwii.datasets import jsut

import librosa
import librosa.display
from matplotlib import pyplot as plt
import MeCab
import jaconv

from nnmnkwii.datasets import jsut
from os.path import join, splitext, basename

from subprocess import Popen, PIPE


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


if __name__ == "__main__":
    in_dir = "/home/ryuichi/data/jsut_ver1"
    transcriptions = jsut.TranscriptionDataSource(
        in_dir, subsets=jsut.available_subsets).collect_files()
    wav_paths = jsut.WavFileDataSource(
        in_dir, subsets=jsut.available_subsets).collect_files()

    dst_dir = "jsut"

    c = 0
    tagger = MeCab.Tagger("-Oyomi")
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

    print(c)
