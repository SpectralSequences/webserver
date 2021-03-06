import json
import os
import pathlib

from spectralsequence_chart import SpectralSequenceChart
import ext

def read_file(path):
    return pathlib.Path(path).read_text()

def read_json_file(path):
    return json.loads(read_file(path))

def add_to_namespace(repl_namespace, obj):
    name = obj.__name__.split(".")[-1]
    repl_namespace[name] = obj

def add_stuff_to_repl_namespace(repl_namespace):
    to_add = [
        read_file, read_json_file,
        ext, ext.algebra, ext.module, ext.fp, ext.fp.FpVector,
        ext.algebra.AdemAlgebra, ext.algebra.MilnorAlgebra,
        ext.module.FDModule,
        # ext.resolution.Resolution,
        SpectralSequenceChart,
    ]
    for name in to_add:
        add_to_namespace(repl_namespace, name)