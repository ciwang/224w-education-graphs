import snap
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle
from tqdm import tqdm

import sys
from os import path

BASE_PATH = "../data/stats.stackexchange.com/Mixed"
USERID_NGRAM_TSV_PATH = path.join(BASE_PATH, "ngram_graph_STATS_20k-Posts_11-top_uni&bigrams_nostem")
NGRAMID_DICT_PICKLE_PATH = path.join(BASE_PATH, "ngram_dict_STATS_20k-Posts_11-top_uni&bigrams_nostem")
HITS_SAVE_PATH = path.join(BASE_PATH, "userid_ngram_hits.csv")

# BASE_PATH = "../data/academia.stackexchange.com/Years"
# USERID_NGRAM_TSV_PATH = path.join(BASE_PATH, "Userid_Ngram_Bipartite_Graph_2018.tsv")
# NGRAMID_DICT_PICKLE_PATH = path.join(BASE_PATH, "Ngramid_Dict_2018.pickle")
# HITS_SAVE_PATH = path.join(BASE_PATH, "userid_ngram_hits.csv")
# BASE_PATH = "../data/academia.stackexchange.com"
# USERID_NGRAM_TSV_PATH = path.join(BASE_PATH, "Userid_Ngram_Bipartite_Graph.tsv")
# NGRAMID_DICT_PICKLE_PATH = path.join(BASE_PATH, "Ngramid_Dict.pickle")
# HITS_SAVE_PATH = path.join(BASE_PATH, "userid_ngram_hits.csv")

Network = snap.LoadEdgeList(snap.PUNGraph, USERID_NGRAM_TSV_PATH)
ngramid_dict = pickle.load(open(NGRAMID_DICT_PICKLE_PATH, "rb"))
idngram_dict = {v: k for k, v in ngramid_dict.iteritems()}

def printTop20(ht):
    ht.SortByDat(False)
    it = ht.BegI()
    i = 0
    while not it.IsEnd() and i < 20:
        print it.GetKey(), idngram_dict.get(it.GetKey(), '--user--'), it.GetDat()
        it.Next()
        i += 1

PRankH = snap.TIntFltH()
snap.GetPageRank(Network, PRankH)
print '\nTop 20 nodes (PageRank)'
printTop20(PRankH)

NIdHubH = snap.TIntFltH()
NIdAuthH = snap.TIntFltH()
snap.GetHits(Network, NIdHubH, NIdAuthH)
print '\nTop 20 nodes (Hubs)'
printTop20(NIdHubH)
print '\nTop 20 nodes (Auths)'
printTop20(NIdAuthH)

df = pd.DataFrame()
df['id'] = [n.GetId() for n in Network.Nodes()]
df['pr'] = [PRankH[ni] for ni in df['id']]
df['hub'] = [NIdHubH[ni] for ni in df['id']]
df['auth'] = [NIdAuthH[ni] for ni in df['id']]
df.to_csv(HITS_SAVE_PATH, index=False)
