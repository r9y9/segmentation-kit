# coding: utf-8

"""16kHzの音声データを用意する"""

import os
from os.path import basename, join, splitext
from subprocess import PIPE, Popen

import numpy as np
from nnmnkwii.datasets import jsut
from tqdm import trange

if __name__ == "__main__":
    from params import dst_dir, in_dir, subsets

    wav_paths = jsut.WavFileDataSource(in_dir, subsets=subsets).collect_files()

    os.makedirs(dst_dir, exist_ok=True)
    for idx in trange(len(wav_paths)):
        wav_path = wav_paths[idx]
        name = splitext(basename(wav_path))[0]

        dst_path = join(dst_dir, name + ".wav")

        # Copy
        p = Popen(
            "cp {} {}".format(wav_path, dst_path),
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
            shell=True,
        )
        p.wait()

        # Sox
        tmp_path = "/tmp/test.wav"
        p = Popen(
            "sox {} -r 16000 {}".format(dst_path, tmp_path),
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
            shell=True,
        )
        p.wait()

        # mv
        p = Popen(
            "mv {} {}".format(tmp_path, dst_path),
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
            shell=True,
        )
        p.wait()
