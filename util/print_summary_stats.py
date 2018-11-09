import snap
import matplotlib.pyplot as plt
import numpy as np

from pathlib import Path
import sys

gfile = sys.argv[1]
print('Printing summary stats for file at:', gfile)

if gfile.endswith('.tsv'):
    Network = snap.LoadEdgeList(snap.PUNGraph, gfile, 0, 1)
elif gfile.endswith('.graph'):
    FIn = snap.TFIn(gfile)
    Network = snap.TUNGraph.Load(FIn)
else:
    print('Error: file type not supported')
    exit()

snap.PrintInfo(Network)
print('Edges:', snap.CntUniqUndirEdges(Network))

# for directed graphs, should be same for undir
DegToCntV = snap.TIntPrV()
snap.GetInDegCnt(Network, DegToCntV)
print('Nodes with deg > 10', sum([item.GetVal2() for item in DegToCntV if item.GetVal1() > 10]))

# Nodes = snap.TIntFltH()
# Edges = snap.TIntPrFltH()
# snap.GetBetweennessCentr(Network, Nodes, Edges, 0.1)

ClustCoeff = snap.GetClustCf(Network, 10000)
print('Clustering coeff', ClustCoeff)