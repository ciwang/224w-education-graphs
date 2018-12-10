import snap
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from operator import itemgetter
import pickle
from tqdm import tqdm

from pathlib import Path
import sys

# gfile = sys.argv[1]
# print('Printing summary stats for file at:', gfile)

# if gfile.endswith('.tsv'):
#     Network = snap.LoadEdgeList(snap.PUNGraph, gfile, 0, 1)
# elif gfile.endswith('.graph'):
#     FIn = snap.TFIn(gfile)
#     Network = snap.TUNGraph.Load(FIn)
# else:
#     print('Error: file type not supported')
#     exit()

GRAPH_PATH='../data/academia.stackexchange.com/Userid_Ngram_Folded_Graph.graph'
NGRAMID_DICT_PICKLE_PATH='../data/academia.stackexchange.com/Ngramid_Dict.pickle'

FIn = snap.TFIn(GRAPH_PATH)
Network = snap.TUNGraph.Load(FIn)
ngramid_dict = pickle.load(open(NGRAMID_DICT_PICKLE_PATH, "rb"))
idngram_dict = {v: k for k, v in ngramid_dict.iteritems()}

CENTRALITY_SAVE_PATH='../data/academia.stackexchange.com/node_centrality.csv'

PageRanks = snap.TIntFltH()
print "Calculating page rank"
snap.GetPageRank(Network, PageRanks)
pr_list = []
for ni in PageRanks:
    pr_list.append([ni, idngram_dict[ni], PageRanks[ni]])
cent_df = pd.DataFrame(pr_list, columns=['id', 'value', 'pr_score'])
cent_df.to_csv(CENTRALITY_SAVE_PATH, index=False)

cent_df = pd.read_csv(CENTRALITY_SAVE_PATH)
print "Calculating harmonic centrality"
nids = [n.GetId() for n in Network.Nodes()]
pathlens = {}
hm_list = []
for ni in tqdm(nids):
    hm = 0
    for nj in tqdm(nids):
        path = pathlens.get((nj,ni))
        if not path:
            path = snap.GetShortPath(Network, ni, nj)
            pathlens[(ni, nj)] = path
        if path > 0:
            hm += 1.0/path
    hm_list.append([ni, hm])
hm_df = pd.DataFrame(bt_list, columns=['id', 'hm_score'])
cent_df = cent_df.merge(hm_df, on='id')
cent_df.to_csv(CENTRALITY_SAVE_PATH, index=False)

cent_df = pd.read_csv(CENTRALITY_SAVE_PATH)
BetweenNodes = snap.TIntFltH()
BetweenEdges = snap.TIntPrFltH()
print "Calculating betweenness centrality"
snap.GetBetweennessCentr(Network, BetweenNodes, BetweenEdges, 0.1)
bt_list = []
for ni in BetweenNodes:
    bt_list.append([ni, BetweenNodes[ni]])
bt_df = pd.DataFrame(bt_list, columns=['id', 'bt_score'])
cent_df = cent_df.merge(bt_df, on='id')
cent_df.to_csv(CENTRALITY_SAVE_PATH, index=False)

