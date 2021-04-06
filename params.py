# coding: utf-8
from os.path import expanduser, join

from nnmnkwii.datasets import jsut

in_dir = join(expanduser("~"), "data/jsut_ver1.1")
dst_dir = "jsut"
subsets = jsut.available_subsets
subsets = ["basic5000"]
