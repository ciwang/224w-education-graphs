def U_fold_graph(G, U_set):
    """
    G: Bipartite graph that we want to fold.
    U_set: Set containing all node ids in the left partition of G.
    """
    folded_G = snap.TUNGraph.New()
    
    # Add all nodes in U_set to G.
    for nid in U_set:
        folded_G.AddNode(nid)
        
    # Iterate through nodes in U_set and add edge between them if they have at least one common neighbor in G.
    # Becasue the graph is bipartite, the common neighbor must be in V.
    for N1 in G.Nodes():
        if (N1.GetId() not in U_set): continue # N1 not a disease node.
        for N2 in G.Nodes():
            if (N1.GetId() == N2.GetId()): continue # No self-loops.
            if (N2.GetId() not in U_set): continue # N2 not a disease node.
            if (snap.GetCmnNbrs(G, N1.GetId(), N2.GetId()) > 0):
                    folded_G.AddEdge(N1.GetId(), N2.GetId())
    return folded_G