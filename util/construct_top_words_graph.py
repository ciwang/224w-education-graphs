
# coding: utf-8

# In[ ]:


import re
import numpy as np
import pandas as pd
import numbers
import pickle
import snap
from os import path
from tqdm import tqdm


# In[6]:


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


# # ### Load top words from posts.

# # In[3]:


# num_top_words = 5


# # In[22]:


# top_word_columns = ["TopWord%d" % i for i in xrange(1, num_top_words+1)]


# # In[17]:


# def load_top_ngram_df(topwords_path):
#     """
#     TODO
#     """
#     # Load csv containing the top words.
#     posts_df = pd.read_csv(topwords_path, sep = "\t", usecols = 
#                            ["Id", "OwnerUserId", "TopWord1", "TopWord2", "TopWord3", "TopWord4", "TopWord5"])
    
#     # Clean dataframe.
#     posts_df = posts_df.dropna()
#     posts_df = posts_df.rename(columns={"Id": "post_id", "OwnerUserId": "user_id"})
#     posts_df["user_id"] = posts_df["user_id"].astype(np.int64)
#     posts_df["post_id"] = posts_df["post_id"].astype(np.int64)
#     posts_df = posts_df[posts_df["user_id"] > 0]
#     posts_df = posts_df[posts_df["post_id"] > 0]

#     return posts_df


# # In[23]:


# def get_top_ngram_set(posts_df):
#     top_ngram_set = set()
#     for col in top_word_columns:
#         top_ngram_set.update(posts_df[col].values)
#     return top_ngram_set


# # In[24]:


# posts_df = load_top_ngram_df(POST_TOP_NGRAM_PATH)


# # In[25]:


# top_ngram_set = get_top_ngram_set(posts_df)


# # In[26]:


# print "Number of n-grams:", len(top_ngram_set)


# # ### Construct User-Id to Ngram and Post-Id to Ngram Graphs.

# # In[12]:


# def create_ngram_id_dict(top_ngram_set, init_index):
#     """
#     Create dictionary mapping n-gram to an integer index greater than or equal to init_index.
#     """    
#     # Create dictinonary that maps n-gram to its id.
#     ngram_id_dict = dict()
#     curr_index = init_index
#     for ngram in top_ngram_set:
#         ngram_id_dict[ngram] = curr_index
#         curr_index += 1
    
#     return ngram_id_dict


# # In[36]:


# def create_graph_dfs(top_ngram_set, posts_df):
#     """
#     Create user-id to n-gram and post-id to n-gram graph. The graphs will be stored as a Pandas dataframe.
#         Each row of the dataframe contains an edge of the graph. The dataframe can be written out as a tsv
#         to be read in as a Snap graph.
#     Returns:
#         Tuple (userid_ngram_df, postid_ngram_df, ngram_id_dict, user_id_set, post_id_set). ngramid_dict is
#         a dictionary mapping ngram to its assigned id value. userid_set is a set containing the user id nodes
#         that are included in the user-id graph. postid_set is a containing the post id nodes that
#         are included in teh post-id graph.
#     """
#     # Create n-gram dict.
#     max_post_id = max(posts_df["post_id"].values)
#     max_user_id = max(posts_df["user_id"].values)
#     ngram_id_dict = create_ngram_id_dict(top_ngram_set, max(max_post_id, max_user_id) + 1)
    
#     # Create dataframes storing the edges in the graphs.
#     user_id_nodes = []
#     post_id_nodes = []
#     ngram_id_nodes = []
#     for _, row in posts_df.iterrows():
#         user_id = row["user_id"]
#         post_id = row["post_id"]
#         top_ngrams = list(row[top_word_columns])        
#         if ((user_id < 0) or (post_id) < 0): continue
#         for ngram, ngram_id in ngram_id_dict.items():
#             if ngram in top_ngrams:
#                 ngram_id_nodes.append(ngram_id)
#                 user_id_nodes.append(user_id)
#                 post_id_nodes.append(post_id)
      
#     userid_ngram_df = pd.DataFrame({"user_id": user_id_nodes, "ngram_id": ngram_id_nodes})
#     postid_ngram_df = pd.DataFrame({"post_id": post_id_nodes, "ngram_id": ngram_id_nodes})
#     return userid_ngram_df, postid_ngram_df, ngram_id_dict, set(user_id_nodes), set(post_id_nodes)


# # In[37]:


# # Construct graphs stored in dataframes.
# userid_ngram_df, postid_ngram_df, ngramid_dict, userid_set, postid_set = create_graph_dfs(top_ngram_set, posts_df)


# # In[38]:


# # Write graphs as tsv files that can be read as a Snap graph.
# userid_ngram_df.to_csv(USERID_NGRAM_TSV_PATH, sep="\t", header=False, index=False)
# postid_ngram_df.to_csv(POSTID_NGRAM_TSV_PATH, sep="\t", header=False, index=False)


# # In[39]:


# # Pickle to store ngramid_dict, userid_set, postid_set.
# pickle_out = open(NGRAMID_DICT_PICKLE_PATH,"wb")
# pickle.dump(ngramid_dict, pickle_out)
# pickle_out.close()

# pickle_out = open(USERID_SET_PICKLE_PATH,"wb")
# pickle.dump(userid_set, pickle_out)
# pickle_out.close()

# pickle_out = open(POSTID_SET_PICKLE_PATH,"wb")
# pickle.dump(postid_set, pickle_out)
# pickle_out.close()


# # ### Fold Bipartite Graphs to create User-id and Post-id Graphs

# # In[40]:


# # Load the graphs in SNAP.
userid_ngram_bipartite_graph = snap.LoadEdgeList(snap.PUNGraph, USERID_NGRAM_TSV_PATH, 0, 1)
postid_ngram_bipartite_graph = snap.LoadEdgeList(snap.PUNGraph, POSTID_NGRAM_TSV_PATH, 0, 1)


# # In[44]:


# # Load pickled datastructures.
ngramid_dict = pickle.load(open(NGRAMID_DICT_PICKLE_PATH, "rb"))
userid_set = pickle.load(open(USERID_SET_PICKLE_PATH, "rb"))
postid_set = pickle.load(open(POSTID_SET_PICKLE_PATH, "rb"))


# # In[42]:


# # Basic userid ngram bipartite graph statistics.
# print "Nodes", userid_ngram_bipartite_graph.GetNodes()
# print "Edges", userid_ngram_bipartite_graph.GetEdges()


# # In[43]:


# # Basic userid ngram bipartite graph statistics.
# print "Nodes", postid_ngram_bipartite_graph.GetNodes()
# print "Edges", postid_ngram_bipartite_graph.GetEdges()


# # In[45]:

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
    # for N1 in tqdm(G.Nodes(), total=G.GetNodes()):
    #     if (N1.GetId() not in U_set): continue # N1 not a disease node.
    #     for N2 in G.Nodes():
    #         if (N1.GetId() == N2.GetId()): continue # No self-loops.
    #         if (N2.GetId() not in U_set): continue # N2 not a disease node.
    #         if (snap.GetCmnNbrs(G, N1.GetId(), N2.GetId()) > 0):
    #                 folded_G.AddEdge(N1.GetId(), N2.GetId())
    return folded_G


# # Graph containing post nodes.

# # In[47]:


# Fold to create post graph.
postid_graph = U_fold_graph(postid_ngram_bipartite_graph, postid_set)


# In[49]:


# Save created post graph.
FOut = snap.TFOut(POSTID_FOLDED_GRAPH_PATH)
postid_graph.Save(FOut)
FOut.Flush()


# Graph containing n-gram nodes folded from user graph.

# In[ ]:


# # Fold to n-gram graph from the user graph.
# userid_ngram_graph = U_fold_graph(userid_ngram_bipartite_graph, ngramid_dict.values())


# # In[ ]:


# # Save created user n-gram  graph.
# FOut = snap.TFOut(USERID_NGRAM_FOLDED_GRAPH_PATH)
# userid_ngram_graph.Save(FOut)
# FOut.Flush()

