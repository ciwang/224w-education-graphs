import re
import numpy as np
import pandas as pd
import numbers
import pickle
import snap
from os import path
from tqdm import tqdm

# BASE_PATH = "../data/academia.stackexchange.com/Years"
# USERID_NGRAM_TSV_PATH = path.join(BASE_PATH, "Userid_Ngram_Bipartite_Graph.tsv")
# POSTID_NGRAM_TSV_PATH = path.join(BASE_PATH, "Postid_Ngram_Bipartite_Graph.tsv")
# NGRAMID_DICT_PICKLE_PATH = path.join(BASE_PATH, "Ngramid_Dict.pickle")
# USERID_SET_PICKLE_PATH = path.join(BASE_PATH, "Userid_set.pickle")
# POSTID_SET_PICKLE_PATH = path.join(BASE_PATH, "Postid_set.pickle")
# USERID_NGRAM_FOLDED_GRAPH_PATH = path.join(BASE_PATH, "Userid_Ngram_Folded_Graph.graph")
# POSTID_FOLDED_GRAPH_PATH = path.join(BASE_PATH, "Postid_Folded_Graph.graph")
BASE_PATH = "../data/stats.stackexchange.com/Mixed"
USERID_NGRAM_TSV_PATH = path.join(BASE_PATH, "ngram_graph_STATS_20k-Posts_11-top_uni&bigrams_nostem")
POSTID_NGRAM_TSV_PATH = path.join(BASE_PATH, "postid_graph_STATS_20k-Posts_11-top_uni&bigrams_nostem")
NGRAMID_DICT_PICKLE_PATH = path.join(BASE_PATH, "ngram_dict_STATS_20k-Posts_11-top_uni&bigrams_nostem")
USERID_SET_PICKLE_PATH = path.join(BASE_PATH, "userid_set_STATS_20k-Posts_11-top_uni&bigrams_nostem")
POSTID_SET_PICKLE_PATH = path.join(BASE_PATH, "postid_set_STATS_20k-Posts_11-top_uni&bigrams_nostem")
USERID_NGRAM_FOLDED_GRAPH_PATH = path.join(BASE_PATH, "Userid_Ngram_Folded_Graph.graph")
POSTID_FOLDED_GRAPH_PATH = path.join(BASE_PATH, "Postid_Folded_Graph.graph")

def get_neighbor_set(Graph, NId):
    Node = Graph.GetNI(NId)
    return set([Node.GetNbrNId(i) for i in range(Node.GetDeg())])

def U_fold_graph(G, U_set):
    """
    G: Bipartite graph that we want to fold.
    U_set: Set containing all node ids in the left partition of G. These will be the nodes that are kept
        in the fold
    """
    folded_G = snap.TUNGraph.New()
    
    # Add all nodes in U_set to G.
    for nid in U_set:
        folded_G.AddNode(nid)
        
    # Iterate through nodes in U_set and add edge between them if they have at least one common neighbor in G.
    # Becasue the graph is bipartite, the common neighbor must be in V.
    print "iterating through nodes ...."
    for U1 in tqdm(U_set):
        for V in get_neighbor_set(G, U1):
            for U2 in get_neighbor_set(G, V):
                if U1 != U2 and not folded_G.IsEdge(U1, U2):
                    folded_G.AddEdge(U1, U2)
    return folded_G

def save_graph(graph, path):
    FOut = snap.TFOut(path)
    graph.Save(FOut)
    print 'graph saved to %s' % path
    FOut.Flush()

def fold_and_save_graphs(suffix=()):
    # Load the graphs in SNAP.
    userid_ngram_bipartite_graph = snap.LoadEdgeList(snap.PUNGraph, USERID_NGRAM_TSV_PATH % suffix, 0, 1)
    postid_ngram_bipartite_graph = snap.LoadEdgeList(snap.PUNGraph, POSTID_NGRAM_TSV_PATH % suffix, 0, 1)

    # Load pickled datastructures.
    ngramid_dict = pickle.load(open(NGRAMID_DICT_PICKLE_PATH % suffix, "rb"))
    userid_set = pickle.load(open(USERID_SET_PICKLE_PATH % suffix, "rb"))
    postid_set = pickle.load(open(POSTID_SET_PICKLE_PATH % suffix, "rb"))

    postid_graph = U_fold_graph(postid_ngram_bipartite_graph, postid_set)
    save_graph(postid_graph, POSTID_FOLDED_GRAPH_PATH % suffix)

    userid_ngram_graph = U_fold_graph(userid_ngram_bipartite_graph, ngramid_dict.values())
    save_graph(userid_ngram_graph, USERID_NGRAM_FOLDED_GRAPH_PATH % suffix)    

if __name__ == "__main__":
    # fold academia
    # for year in range(2011, 2019):
    #     fold_and_save_graphs('_%d' % year)
    #     print "Done folding year", year

    # fold normal
    fold_and_save_graphs()
