Task: 
Write C++ code to generate random graph and count the number of connected components of the graph.

Solution:
In this task the graph is represented as an adjacency matrix. Then we count connected components using it. If two members are already a part of to different “groups”, then these groups are merged together. Nodes, that don’t belong to any “group”, are counted separately.