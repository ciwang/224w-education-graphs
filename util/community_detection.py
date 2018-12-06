import snap
from os import path
import pickle
import collections
import numpy as np
from tqdm import tqdm
import pandas as pd

BASE_PATH = "../data/stats.stackexchange.com/Mixed"
FOLDED_NGRAM_GRAPH_PATH = path.join(BASE_PATH, "Userid_Ngram_Folded_Graph.graph")
FOLDED_POSTID_GRAPH_PATH = path.join(BASE_PATH, "Postid_Folded_Graph.graph")
NGRAM_DICT_PICKLE = path.join(BASE_PATH, "Bigramid_Dict")
POSTID_PICKLE = path.join(BASE_PATH, "STATS_20k-Posts_11-top_uni&bigrams_nostem.pickle")
POST_TOP_NGRAM_PATH = path.join(BASE_PATH, "STATS_20k-Posts_11-top_uni&bigrams_nostem.tsv")

def get_modularity(G, community_dict):
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

def load_top_ngram_df(topwords_path):
    # Load csv containing the top words.
    posts_df = pd.read_csv(topwords_path, sep = "\t", usecols =
                           ["Id", "OwnerUserId", "TopWord1", "TopWord2", "TopWord3", "TopWord4", "TopWord5"])

    # Clean dataframe.
    posts_df = posts_df.dropna()
    posts_df = posts_df.rename(columns={
            "Id": "post_id", "OwnerUserId": "user_id"})
    posts_df["user_id"] = posts_df["user_id"].astype(np.int64)
    posts_df["post_id"] = posts_df["post_id"].astype(np.int64)
    posts_df = posts_df[posts_df["user_id"] > 0]
    posts_df = posts_df[posts_df["post_id"] > 0]

    return posts_df

def add_communities_post_df(post_df, best_comm_map, postid_dict):
    # Iterate over rows and add each community to each row.
    community_array = []
    for index, row in post_df.iterrows():
        user_id = row["post_id"]
        A_id = postid_dict.get(user_id, -1)
        if (A_id < 0):
            community_array.append(-1)
        else:
            community_array.append(best_comm_map[A_id])
    post_df.loc[:,'Community'] = community_array

    return post_df

##########################################################################

f_in = snap.TFIn(FOLDED_POSTID_GRAPH_PATH)
post_graph = snap.TUNGraph.Load(f_in)
print "nodes", post_graph.GetNodes()
print "edges", post_graph.GetEdges()

COMMUNITIES_PATH = path.join(BASE_PATH, 'postid-communities-with-postbodies.txt')
COMMUNITIES_VEC_PATH = path.join(BASE_PATH, 'postid-communities.vector')

# remove degree-1 nodes
assert snap.CntSelfEdges(post_graph) == 0
snap.DelDegKNodes(post_graph, 1, 1)

comm_vec = snap.TCnComV()
modularity = snap.CommunityCNM(post_graph, comm_vec)

f_out = snap.TFOut(COMMUNITIES_VEC_PATH)
comm_vec.Save(f_out)
f_out.Flush()

f_in = snap.TFIn(COMMUNITIES_VEC_PATH)
comm_vec = snap.TCnComV()
comm_vec.Load(f_in)

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
    # alt_modularity = get_modularity(post_graph, community_dict)
    # f.write("Alternate modularity of the network (sanity check) is {}".format(alt_modularity))

postid_dict2 = collections.defaultdict(int)
for node in community_dict:
    postid_dict2[node] = node

posts_df = load_top_ngram_df(POST_TOP_NGRAM_PATH)
add_communities_post_df(posts_df, community_dict, postid_dict2)

print posts_df