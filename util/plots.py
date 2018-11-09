import snap
import matplotlib.pyplot as plt
import numpy as np

from os import path
import sys

BASE_PATH = "../data/academia.stackexchange.com"
POST_TOP_NGRAM_PATH = path.join(BASE_PATH, "Posts-top_words.tsv")
USERID_NGRAM_TSV_PATH = path.join(BASE_PATH, "Userid_Ngram_Bipartite_Graph.tsv")
POSTID_NGRAM_TSV_PATH = path.join(BASE_PATH, "Postid_Ngram_Bipartite_Graph.tsv")
NGRAMID_DICT_PICKLE_PATH = path.join(BASE_PATH, "Ngramid_Dict.pickle")
USERID_SET_PICKLE_PATH = path.join(BASE_PATH, "Userid_set.pickle")
POSTID_SET_PICKLE_PATH = path.join(BASE_PATH, "Postid_set.pickle")
USERID_FOLDED_GRAPH_PATH = path.join(BASE_PATH, "Userid_Folded_Graph.graph")
POSTID_FOLDED_GRAPH_PATH = path.join(BASE_PATH, "Postid_Folded_Graph.graph")
USERID_NGRAM_FOLDED_GRAPH_PATH = path.join(BASE_PATH, "Userid_Ngram_Folded_Graph.graph")
POSTID_NGRAM_FOLDED_GRAPH_PATH = path.join(BASE_PATH, "Postid_Ngram_Folded_Graph.graph")

def getGraphFromFile(gfile):
    if gfile.endswith('.tsv'):
        Network = snap.LoadEdgeList(snap.PUNGraph, gfile, 0, 1)
    elif gfile.endswith('.graph'):
        FIn = snap.TFIn(gfile)
        Network = snap.TUNGraph.Load(FIn)
    else:
        print('Error: file type not supported')
        return None
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
plt.loglog(x_ngram, y_ngram, color = 'y', label = 'User <> Ngram Bipartite Graph')

NgramFoldedGraph = getGraphFromFile(USERID_NGRAM_FOLDED_GRAPH_PATH)
x_ngram_folded, y_ngram_folded = getNodeDegForPlot(NgramFoldedGraph)
plt.loglog(x_ngram_folded, y_ngram_folded, linestyle = 'dashed', color = 'g', label = 'Folded Ngram Graph')

PostNgramGraph = getGraphFromFile(POSTID_NGRAM_TSV_PATH)
x_post, y_post = getNodeDegForPlot(PostNgramGraph)
plt.loglog(x_post, y_post, color = 'm', label = 'Post <> Ngram Bipartite Graph')

PostFoldedGraph = getGraphFromFile(POSTID_FOLDED_GRAPH_PATH)
x_post_folded, y_post_folded = getNodeDegForPlot(PostFoldedGraph)
plt.loglog(x_post_folded, y_post_folded, linestyle = 'dashed', color = 'r', label = 'Folded Post Graph')

plt.xlabel('Node Degree (log)')
plt.ylabel('Proportion of Nodes with a Given Degree (log)')
plt.title('Degree Distribution of Bipartite and Folded Graphs - Posts')
plt.legend()
plt.show()
