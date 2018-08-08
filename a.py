# coding: utf-8

"""Run OpenJTalk and convert texts to phone sequences"""

import numpy as np
import os
import sys
from nnmnkwii.datasets import jsut
from os.path import join, splitext, basename
from tqdm import trange
from pyopenjtalk import OpenJTalk


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


if __name__ == "__main__":
    from params import in_dir, dst_dir, subsets

    transcriptions = jsut.TranscriptionDataSource(
        in_dir, subsets=subsets).collect_files()
    wav_paths = jsut.WavFileDataSource(
        in_dir, subsets=subsets).collect_files()

    jtalk = OpenJTalk()

    os.makedirs(dst_dir, exist_ok=True)
    for idx in trange(len(transcriptions)):
        text = transcriptions[idx]
        wav_path = wav_paths[idx]
        name = splitext(basename(wav_path))[0]

        # Run openjtalk
        njd_results, labels = jtalk.run_frontend(text)
        phones = []
        for label in labels:
            phone = label.split("-")[1].split("+")[0]
            if phone == "sil":
                continue
            elif phone == "pau":
                phone = "sp"
            phones.append(phone)
        yomi = " ".join(phones).lower()

        # Phone mapping for julius
        spe = {
            # "by a": "b y a",
            "v": "b",  # julius doesn't care about it
            "cl": "q",
            " y e": " i e",
            # this is wrong but for now maybe it's fine for forced alignment
            "ty": "ch",
        }
        for k, v in spe.items():
            if k in yomi:
                yomi = yomi.replace(k, v)

        with open(join(dst_dir, name + ".openjtalk.lab"), "w") as f:
            for l in labels:
                f.write("{}\n".format(l))

        # Write to file
        with open(join(dst_dir, name + ".txt"), "w") as f:
            f.write(yomi)

    sys.exit(0)
