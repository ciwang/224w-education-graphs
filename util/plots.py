import snap
import matplotlib.pyplot as plt
import numpy as np

from os import path
import sys

# YEAR = 2018
# BASE_PATH = "../data/academia.stackexchange.com/Years"
# USERID_NGRAM_TSV_PATH = path.join(BASE_PATH, "Userid_Ngram_Bipartite_Graph_%d.tsv") % YEAR
# POSTID_NGRAM_TSV_PATH = path.join(BASE_PATH, "Postid_Ngram_Bipartite_Graph_%d.tsv") % YEAR
# NGRAMID_DICT_PICKLE_PATH = path.join(BASE_PATH, "Ngramid_Dict_%d.pickle") % YEAR
# USERID_SET_PICKLE_PATH = path.join(BASE_PATH, "Userid_set_%d.pickle") % YEAR
# POSTID_SET_PICKLE_PATH = path.join(BASE_PATH, "Postid_set_%d.pickle") % YEAR
# USERID_NGRAM_FOLDED_GRAPH_PATH = path.join(BASE_PATH, "Userid_Ngram_Folded_Graph_%d.graph") % YEAR
# POSTID_FOLDED_GRAPH_PATH = path.join(BASE_PATH, "Postid_Folded_Graph_%d.graph") % YEAR

BASE_PATH = "../data/academia.stackexchange.com"
USERID_NGRAM_TSV_PATH = path.join(BASE_PATH, "Userid_Ngram_Bipartite_Graph.tsv")
POSTID_NGRAM_TSV_PATH = path.join(BASE_PATH, "Postid_Ngram_Bipartite_Graph.tsv")
NGRAMID_DICT_PICKLE_PATH = path.join(BASE_PATH, "Ngramid_Dict.pickle")
USERID_SET_PICKLE_PATH = path.join(BASE_PATH, "Userid_set.pickle")
POSTID_SET_PICKLE_PATH = path.join(BASE_PATH, "Postid_set.pickle")
USERID_NGRAM_FOLDED_GRAPH_PATH = path.join(BASE_PATH, "Userid_Ngram_Folded_Graph.graph")
POSTID_FOLDED_GRAPH_PATH = path.join(BASE_PATH, "Postid_Folded_Graph.graph")

# BASE_PATH = "../data/stats.stackexchange.com/Mixed"
# POST_TOP_NGRAM_PATH = path.join(BASE_PATH, "Posts-top_words.tsv")
# USERID_NGRAM_TSV_PATH = path.join(BASE_PATH, "ngram_graph_STATS_20k-Posts_11-top_uni&bigrams_nostem")
# POSTID_NGRAM_TSV_PATH = path.join(BASE_PATH, "postid_graph_STATS_20k-Posts_11-top_uni&bigrams_nostem")
# NGRAMID_DICT_PICKLE_PATH = path.join(BASE_PATH, "ngram_dict_STATS_20k-Posts_11-top_uni&bigrams_nostem")
# USERID_SET_PICKLE_PATH = path.join(BASE_PATH, "userid_set_STATS_20k-Posts_11-top_uni&bigrams_nostem")
# POSTID_SET_PICKLE_PATH = path.join(BASE_PATH, "postid_set_STATS_20k-Posts_11-top_uni&bigrams_nostem")
# USERID_NGRAM_FOLDED_GRAPH_PATH = path.join(BASE_PATH, "Userid_Ngram_Folded_Graph.graph")
# POSTID_FOLDED_GRAPH_PATH = path.join(BASE_PATH, "Postid_Folded_Graph.graph")

def getGraphFromFile(gfile):
    if gfile.endswith('.graph'):
        FIn = snap.TFIn(gfile)
        Network = snap.TUNGraph.Load(FIn)
    else:
        Network = snap.LoadEdgeList(snap.PUNGraph, gfile, 0, 1)
    return Network

def getNodeDegForPlot(Graph):
    """
    :param - Graph: snap.PUNGraph object representing an undirected graph

    return values:
    X: list of degrees
    Y: list of frequencies: Y[i] = fraction of nodes with degree X[i]
    """
    ############################################################################
    # TODO: Your code here!
    N = float(Graph.GetNodes())
    DegToCntV = snap.TIntPrV()
    snap.GetDegCnt(Graph, DegToCntV)
    X, Y = zip(*[(item.GetVal1(), item.GetVal2()/N) for item in DegToCntV])
    ############################################################################
    return X, Y

UserNgramGraph = getGraphFromFile(USERID_NGRAM_TSV_PATH)
x_ngram, y_ngram = getNodeDegForPlot(UserNgramGraph)
plt.plot(x_ngram, y_ngram, color = 'y', label = 'User <> Ngram Bipartite Graph')

NgramFoldedGraph = getGraphFromFile(USERID_NGRAM_FOLDED_GRAPH_PATH)
x_ngram_folded, y_ngram_folded = getNodeDegForPlot(NgramFoldedGraph)
plt.plot(x_ngram_folded, y_ngram_folded, linestyle = 'dashed', color = 'g', label = 'Folded Ngram Graph')

PostNgramGraph = getGraphFromFile(POSTID_NGRAM_TSV_PATH)
x_post, y_post = getNodeDegForPlot(PostNgramGraph)
plt.plot(x_post, y_post, color = 'm', label = 'Post <> Ngram Bipartite Graph')

PostFoldedGraph = getGraphFromFile(POSTID_FOLDED_GRAPH_PATH)
x_post_folded, y_post_folded = getNodeDegForPlot(PostFoldedGraph)
plt.plot(x_post_folded, y_post_folded, linestyle = 'dashed', color = 'r', label = 'Folded Post Graph')

plt.xlabel('Node Degree (log)')
plt.ylabel('Proportion of Nodes with a Given Degree (log)')
plt.title('Degree Distribution of Bipartite and Folded Graphs - Academia')
plt.legend()
plt.show()
