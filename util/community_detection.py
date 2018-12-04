import snap
from os import path
import pickle
import collections
import numpy as np
from tqdm import tqdm

BASE_PATH = "../data/stats.stackexchange.com/Mixed"
FOLDED_NGRAM_GRAPH_PATH = path.join(BASE_PATH, "Userid_Ngram_Folded_Graph.graph")
FOLDED_POSTID_GRAPH_PATH = path.join(BASE_PATH, "Postid_Folded_Graph.graph")
NGRAM_DICT_PICKLE = path.join(BASE_PATH, "Bigramid_Dict")
POSTID_PICKLE = path.join(BASE_PATH, "STATS_20k-Posts_11-top_uni&bigrams_nostem.pickle")

def get_modularity(G, community_dict):
    '''
    This function might be useful to compute the modularity of a given cut
    defined by two sets S and neg_S. We would normally require sets S and neg_S
    to be disjoint and to include all nodes in Graph.

    - community_dict: maps node id to community
    '''
    ##########################################################################
    two_M = G.GetEdges() * 2.0
    mod_sum = 0.0
    for NI in tqdm(G.Nodes()):
        NI_id = NI.GetId()
        for NJ in G.Nodes():
            NJ_id = NJ.GetId()
            if (community_dict[NI_id] == community_dict[NJ_id]):
                mod_sum += G.IsEdge(NI_id, NJ_id) - ((NI.GetDeg() * NJ.GetDeg()) / two_M)
    modularity = mod_sum / two_M
    return modularity
    ##########################################################################

f_in = snap.TFIn(FOLDED_POSTID_GRAPH_PATH)
post_graph = snap.TUNGraph.Load(f_in)
print "nodes", post_graph.GetNodes()
print "edges", post_graph.GetEdges()

# f_in = snap.TFIn(FOLDED_NGRAM_GRAPH_PATH)
# ngram_graph = snap.TUNGraph.Load(f_in)
# print "nodes", ngram_graph.GetNodes()
# print "edges", ngram_graph.GetEdges()

COMMUNITIES_PATH = path.join(BASE_PATH, 'postid-communities-with-postbodies.txt')
COMMUNITIES_VEC_PATH = path.join(BASE_PATH, 'postid-communities.vector')

# CNM
assert snap.CntSelfEdges(post_graph) == 0
modularity = 0.441618294539

comm_vec = snap.TCnComV()

modularity = snap.CommunityCNM(post_graph, comm_vec)

f_out = snap.TFOut(COMMUNITIES_VEC_PATH)
comm_vec.Save(f_out)
f_out.Flush()

f_in = snap.TFIn(COMMUNITIES_VEC_PATH)
comm_vec = snap.TCnComV()
comm_vec.Load(f_in)

# print "communities", len(comm_vec)

# pickle_file = open(NGRAM_DICT_PICKLE, 'rb')
# ngram_dict = pickle.load(pickle_file)
# inverted_dict = dict([[v,k] for k,v in ngram_dict.items()])

# with open(COMMUNITIES_PATH, 'w') as f:
#     for i, comm in enumerate(comm_vec):
#         f.write("#####Community {}#####\n".format(i))
#         for node in comm:
#             f.write(inverted_dict[node] + '\n')
#     f.write("The modularity of the network is {}".format(modularity))

print "communities", len(comm_vec)

pickle_file = open(POSTID_PICKLE, 'rb')
postid_dict = pickle.load(pickle_file)

community_dict = collections.defaultdict(int)

with open(COMMUNITIES_PATH, 'w') as f:
    for i, comm in enumerate(comm_vec):
        f.write("#####Community {}#####\n".format(i))
        community = snap.TIntV()
        for node in comm:
            community.Add(node)
            f.write("Node {}: {}\n".format(node, postid_dict[node]))
            community_dict[node] = i
        f.write('Community {}, nodes: {} modularity: {}\n\n'.format(i, len(comm), snap.GetModularity(post_graph, community, post_graph.GetEdges())))
    f.write("The modularity of the network is {}\n".format(modularity))
    alt_modularity = get_modularity(post_graph, community_dict)
    f.write("Alternate modularity of the network (sanity check) is {}".format(alt_modularity))