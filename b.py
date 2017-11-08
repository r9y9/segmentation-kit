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
from tqdm import trange


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


if __name__ == "__main__":
    in_dir = "/home/ryuichi/data/jsut_ver1"
    transcriptions = jsut.TranscriptionDataSource(
        in_dir, subsets=jsut.available_subsets).collect_files()
    wav_paths = jsut.WavFileDataSource(
        in_dir, subsets=jsut.available_subsets).collect_files()

    dst_dir = "jsut"

    c = 1
    tagger = MeCab.Tagger("-Oyomi")
    os.makedirs(dst_dir, exist_ok=True)
    for idx in trange(len(transcriptions)):
        text = transcriptions[idx]
        wav_path = wav_paths[idx]
        name = splitext(basename(wav_path))[0]

        dst_path = join(dst_dir, name + ".wav")

        # Copy
        p = Popen("cp {} {}".format(wav_path, dst_path),
                  stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
        p.wait()

        # Sox
        tmp_path = "/tmp/test.wav"
        p = Popen("sox {} -r 16000 {}".format(dst_path, tmp_path),
                  stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
        p.wait()

        # mv
        p = Popen("mv {} {}".format(tmp_path, dst_path),
                  stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
        p.wait()
