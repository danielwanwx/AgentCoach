# Graphs Overview | Hello Interview

> Source: https://www.hellointerview.com/learn/code/depth-first-search/graphs-overview
> Scraped: 2026-03-30



Graphs
Depth-First Search is also used to solve interview questions involving graphs.
During the coding interview, graphs are typically represented in two ways: as an adjacency list or as a matrix. So to best prepare for the coding interview, you should be very comfortable with implementing basic DFS on both types of graphs (meaning you can can write the code quickly, and without errors). From there, it's a matter of practicing enough graph questions to get a feel for the types of questions you might encounter.
When working with DFS on a graph, the most important thing to remember is to keep track of the visited nodes as you traverse, since graphs (unlike trees) can contain cycles.
Graph Basics
Graphs consist of nodes (also frequently referred to as vertices), and edges that connect the nodes.
4
3
2
1
0
node
edge
Nodes that are connected to each other via an edge are known as the neighbors of that node. Being able to quickly find the neighbors of a node is crucial when working with graph traversal algorithms.
4
3
2
1
0
neighbor
neighbor
neighbor
neighbor
Nodes 0, 2, 3, 4 are all neighbors of node 1.
A graph can contain cycles. A cycle is a path that starts and ends at the same node.
4
3
2
1
0
cycle
Graphs can also have connected and disconnected components. A connected graph is a graph where there is a path between every pair of nodes. (A tree is a connected graph with no cycles.)
4
3
2
1
A connected graph where there is a path between every pair of nodes.
4
3
2
1
A tree is a connected graph with no cycles.
A disconnected graph is a graph where there are at least two nodes that are not connected to each other by a path. In the example below, nodes 1, 2, 3, 4, 5, and 6 all belong to the same graph, but nodes 5 and 6 are disconnected from nodes 1 - 4. The nodes that are connected to each other are commonly referred to as a connected component, in which case there are 2:
6
5
4
3
2
1
Nodes 1, 2, 3, and 4 are connected, while nodes 5 and 6 are connected. The entire graph (consisting of nodes 1 - 6) is disconnected.
Finally, graphs can be either directed or undirected. In a directed graph, edges between nodes only go in one direction. In an undirected graph, edges between nodes go in both directions. For the most part, the graphs that you will encounter during the coding interview will be undirected.
4
3
2
1
0
A graph with directed edges.

Mark as read

Next: Adjacency List

How would you rate the quality of this article?

0.5 Stars
1 Star
1.5 Stars
2 Stars
2.5 Stars
3 Stars
3.5 Stars
4 Stars
4.5 Stars
5 Stars
Empty

