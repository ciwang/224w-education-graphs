def get_modularity(G, community_dict):
    '''
    This function might be useful to compute the modularity of a given cut
    defined by two sets S and neg_S. We would normally require sets S and neg_S
    to be disjoint and to include all nodes in Graph.
    
    - community_dict: maps node id to community
    '''
    ##########################################################################
    two_M = G.GetEdges() * 2
    mod_sum = 0
    for NI in G.Nodes():
        NI_id = NI.GetId()
        for NJ in G.Nodes():
            NJ_id = NJ.GetId()
            if (community_dict[NI_id] == community_dict[NJ_id]):
                mod_sum += G.IsEdge(NI_id, NJ_id) - ((NI.GetDeg() * NJ.GetDeg()) / two_M)
    modularity = mod_sum / two_M
    return modularity
    ##########################################################################
