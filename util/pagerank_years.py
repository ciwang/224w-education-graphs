import snap
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from operator import itemgetter
import pickle

from os import path
import sys

BASE_PATH = "../data/academia.stackexchange.com/Years"
NGRAMID_DICT_PICKLE_PATH = path.join(BASE_PATH, "Ngramid_Dict_%d.pickle")
USERID_NGRAM_FOLDED_GRAPH_PATH = path.join(BASE_PATH, "Userid_Ngram_Folded_Graph_%d.graph")
SAVE_PATH='../data/academia.stackexchange.com/Years/pagerank_years.csv'

def score_page_rank(year):
    graph_path = USERID_NGRAM_FOLDED_GRAPH_PATH % year
    dict_path = NGRAMID_DICT_PICKLE_PATH % year

    FIn = snap.TFIn(graph_path)
    Network = snap.TUNGraph.Load(FIn)
    ngramid_dict = pickle.load(open(dict_path, "rb"))
    idngram_dict = {v: k for k, v in ngramid_dict.iteritems()}

    PageRanks = snap.TIntFltH()
    print "Calculating page rank for", graph_path
    snap.GetPageRank(Network, PageRanks)
    pr_list = []
    for ni in PageRanks:
        pr_list.append([idngram_dict[ni], PageRanks[ni]])
    df = pd.DataFrame(pr_list, columns=['value', 'pr_score_%d'%year])
    
    if path.exists(SAVE_PATH):
        all_df = pd.read_csv(SAVE_PATH)
        df = all_df.merge(df, on='value', how='outer')
    df.to_csv(SAVE_PATH, index=False)

for year in range(2011, 2019):
    score_page_rank(year)
