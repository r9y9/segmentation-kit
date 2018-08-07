# coding: utf-8

import numpy as np
import os
from nnmnkwii.datasets import jsut
from os.path import join, exists, splitext, basename
from tqdm import trange
from shutil import copyfile
import sys


def wavesurfer_to_hts(lab_path, openjtalk_lab_path):
    lab = ""
    with open(openjtalk_lab_path) as f:
        jlines = f.readlines()
    with open(lab_path) as f:
        lines = f.readlines()
    assert len(jlines) == len(lines)
    for idx, line in enumerate(lines):
        s, e, l = line.split()
        s, e = float(s) * 1e7, float(e) * 1e7
        s, e = int(s), int(e)
        l = jlines[idx].split()[-1]
        lab += "{} {} {}\n".format(s, e, l)
    with open(lab_path, "w") as f:
        f.write(lab)


if __name__ == "__main__":
    from params import in_dir, dst_dir, subsets

    transcriptions = jsut.TranscriptionDataSource(
        in_dir, subsets=subsets).collect_files()
    wav_paths = jsut.WavFileDataSource(
        in_dir, subsets=subsets).collect_files()

    for subset in subsets:
        wav_paths = jsut.WavFileDataSource(in_dir, subsets=[subset]).collect_files()
        save_dir = join(in_dir, subset, "lab")
        os.makedirs(save_dir, exist_ok=True)
        for idx in trange(len(wav_paths)):
            wav_path = wav_paths[idx]
            name = splitext(basename(wav_path))[0]
            lab_path = join(dst_dir, name + ".lab")
            if not exists(lab_path):
                print(idx, "doesn't exist", lab_path)
                continue
            dst_path = join(save_dir, name + ".lab")
            # segment_julius outpus 0-sized label if error happens
            filesize = os.stat(lab_path).st_size
            if filesize > 0:
                openjtalk_lab_path = join(dst_dir, name + ".openjtalk.lab")
                assert exists(openjtalk_lab_path)
                copyfile(lab_path, dst_path)
                wavesurfer_to_hts(dst_path, openjtalk_lab_path)
            else:
                print(idx, "filesize zeo", lab_path)

    sys.exit(0)
