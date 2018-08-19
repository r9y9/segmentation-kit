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
    from params import in_dir, dst_dir
    from params import dataset, dataset_wav_kwargs, dataset_script_kwargs

    transcriptions = dataset.TranscriptionDataSource(
        in_dir, **dataset_script_kwargs).collect_files()
    wav_paths = dataset.WavFileDataSource(
        in_dir, **dataset_wav_kwargs).collect_files()

    for idx in trange(len(wav_paths)):
        wav_path = wav_paths[idx]
        name = splitext(basename(wav_path))[0]
        lab_path = join(dst_dir, name + ".lab")
        if not exists(lab_path):
            print(idx, "doesn't exist", lab_path)
            continue
        dst_path = wav_path.replace(".wav", ".lab")
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
