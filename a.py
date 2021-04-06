# coding: utf-8

"""Run OpenJTalk and convert texts to phone sequences"""

import os
import sys
from os.path import basename, join, splitext

import numpy as np
import pyopenjtalk
from nnmnkwii.datasets import jsut
from tqdm import trange


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


def load_saru_lab():
    import yaml

    with open("/home/ryuichi/sp/jsut-label/text_kana/basic5000.yaml") as f:
        d = yaml.safe_load(f)
    return d


if __name__ == "__main__":
    from params import dst_dir, in_dir, subsets

    transcriptions = jsut.TranscriptionDataSource(
        in_dir, subsets=subsets
    ).collect_files()
    wav_paths = jsut.WavFileDataSource(in_dir, subsets=subsets).collect_files()

    true_prons = load_saru_lab()

    cnt = 0
    wrong_pr = 0

    os.makedirs(dst_dir, exist_ok=True)
    for idx in trange(len(transcriptions)):
        text = transcriptions[idx]
        wav_path = wav_paths[idx]
        name = splitext(basename(wav_path))[0]

        text2 = true_prons[name]["text_level2"]
        if text != text2:
            cnt += 1
            text = text2

        # Run openjtalk
        njd_results, labels = pyopenjtalk.run_frontend(text)
        phones = []
        for label in labels:
            phone = label.split("-")[1].split("+")[0]
            if phone == "sil":
                continue
            elif phone == "pau":
                phone = "sp"
            phones.append(phone)
        yomi = " ".join(phones).lower()

        # Check
        phone_level3 = (
            true_prons[name]["phone_level3"]
            .replace("-", " ")
            .lower()
            .replace(" pau ", " ")
        )
        ps = pyopenjtalk.g2p(text).lower().replace(" pau ", " ")
        if ps != phone_level3:
            wrong_pr += 1

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

    print(f"{cnt} wrong texts")
    print(f"{wrong_pr} wrong pronunciations")
    sys.exit(0)
