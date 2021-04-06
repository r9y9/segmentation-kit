# coding: utf-8

import os
from os.path import basename, join, splitext
from subprocess import PIPE, Popen

import numpy as np
from nnmnkwii.datasets import jsut


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

    c = 0
    os.makedirs(dst_dir, exist_ok=True)
    for idx, (text, wav_path) in enumerate(zip(transcriptions, wav_paths)):
        name = splitext(basename(wav_path))[0]

        text2 = true_prons[name]["text_level2"]
        if text != text2:
            text = text2

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
                        #                        import ipdb

                        #                        ipdb.set_trace()
                        print(name, "Somethihng vad!")

    print("Failed number of utterances:", c)
