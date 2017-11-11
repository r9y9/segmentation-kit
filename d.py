# coding: utf-8

import numpy as np
import os
from nnmnkwii.datasets import jsut
from os.path import join, exists, splitext, basename
from tqdm import trange
from shutil import copyfile
import sys


def wavesurfer_to_hts(lab_path):
    lab = ""
    with open(lab_path) as f:
        for line in f:
            s, e, l = line.split()
            s, e = float(s) * 1e7, float(e) * 1e7
            s, e = int(s), int(e)
            lab += "{} {} {}\n".format(s, e, l)
    with open(lab_path, "w") as f:
        f.write(lab)


if __name__ == "__main__":
    from params import in_dir, dst_dir
    transcriptions = jsut.TranscriptionDataSource(
        in_dir, subsets=jsut.available_subsets).collect_files()
    wav_paths = jsut.WavFileDataSource(
        in_dir, subsets=jsut.available_subsets).collect_files()

    for subset in jsut.available_subsets:
        wav_paths = jsut.WavFileDataSource(in_dir, subsets=[subset]).collect_files()
        dst_dir = join(in_dir, subset, "lab")
        os.makedirs(dst_dir, exist_ok=True)
        for idx in trange(len(wav_paths)):
            wav_path = wav_paths[idx]
            name = splitext(basename(wav_path))[0]
            lab_path = join(dst_dir, name + ".lab")
            if not exists(lab_path):
                continue
            dst_path = join(dst_dir, name + ".lab")
            # segment_julius outpus 0-sized label if error happens
            filesize = os.stat(lab_path).st_size
            if filesize > 0:
                copyfile(lab_path, dst_path)
                wavesurfer_to_hts(dst_path)

    sys.exit(0)
