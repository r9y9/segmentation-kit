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

    err = 0
    tagger = MeCab.Tagger("-Oyomi")
    os.makedirs(dst_dir, exist_ok=True)
    for idx in trange(len(transcriptions)):
        text = transcriptions[idx]
        wav_path = wav_paths[idx]

        # Get yomi from normalized text
        yomi = jaconv.normalize(text)
        r = tagger.parse(yomi)[:-1]
        yomi = jaconv.kata2hira(r)
        if yomi[-1] in [".", ",", "、", "。", "！", "？", "!", "?"]:
            yomi = yomi[:-1]

        # fallback path, get yomi from unnormalized text
        if hasNumbers(yomi):
            r = tagger.parse(text)[:-1]
            yomi = jaconv.kata2hira(r)
            if yomi[-1] in [".", ",", "、", "。", "！", "？", "!", "?"]:
                yomi = yomi[:-1]

            if hasNumbers(yomi):
                err += 1
                print(idx, wav_path, yomi)

        # Insert short pose
        for c in [",", "、", ".", "。"]:
            yomi = yomi.replace(c, " sp ")

        # Remove
        for c in ["「", "」", "『", "』", "・"]:
            yomi = yomi.replace(c, "")

        # Write to file
        name = splitext(basename(wav_path))[0]
        with open(join(dst_dir, name + ".txt"), "w") as f:
            f.write(yomi)

    print(err)
