# Topological Sort

> Source: https://www.hellointerview.com/learn/code/graphs/topological-sort
> Scraped: 2026-03-30

Topological Sort
5:24
8 chapters • 1 interactive checkpoints
Pre-Requisite: Depth-First Search, Breadth-First Search
When working with graphs, make sure you first practice using Depth-First Search (DFS) and Breadth-First Search (BFS) to solve coding interview questions, as they are the most common graph algorithms you'll encounter.
This section covers Topological Sort, an important but less common graph algorithm.
Topological sort takes a directed acyclic graph (DAG) and turns it into a linear ordering of nodes such that the directed edges only point forward, from left-to-right:
2
3
4
1
0
1
0
3
2
4
A graph (left) and its topological sort (right)
In more formal terms, a topological sort is a linear ordering of vertices such that for every directed edge u -> v, vertex u comes before vertex v in the ordering.
A given graph may have more than one valid topological sorts. We'll look at one algorithm for finding a topological sort - Kahn's Algorithm, which uses the concept of indegrees.
Indegrees
Each node in a graph has an indegree, which is the number of incoming edges to that node.
2
3
4
1
0
0
1
2
1
1
The indegree is shown next to each node.
Calculate Indegrees
List of Edges
If our graph is given to us as list of edges, we can calculate the indegree of each node by iterating through the edges and incrementing the indegree of the destination node.
DESCRIPTION
You are given a graph with n nodes, where each node has an integer value from 0 to n - 1.
The graph is represent by a list of edges, where edges[i] = [u, v] is a directed edge from node u to node v. Write a function to calculate the indegree of each node in the graph.
Example
Input:
edges = [(0, 1), (1, 2), (1, 3), (3, 2), (3, 4)]
n = 5
2
3
4
1
0
Output:
[0, 1, 2, 1, 1]
Note that we can output the indegrees as an array because the nodes are numbered from 0 to n - 1. (We can look up the indegree of node i at index i in the array.) If the nodes were numbered differently, we would need a dictionary to map each node to its indegree.
SOLUTION
Python
Language
def indegree(n, edges): 
    indegree = [0] * n
    for u, v in edges:
        indegree[v] += 1
    return indegree
Adjacency List
If our graph is given to us as an adjacency list, we can calculate the indegree of each node by iterating through the neighbors of each node and incrementing their indegree.
DESCRIPTION
You are given a graph with n nodes, where each node has an integer value from 0 to n - 1.
The graph is represent by an adjacency list, where each node i is mapped to a list of nodes that have a directed edge from node i to them. Write a function to calculate the indegree of each node in the graph.
Example
Input:
edges = {0: [1], 1: [2, 3], 2: [], 3: [2, 4], 4: []}
n = 5
2
3
4
1
0
Output:
[0, 1, 2, 1, 1]
SOLUTION
Python
Language
def indegree(adj_list, n):
    indegree = [0] * n
    for u in adj_list:
        # increment the indegree of each neighbor of u
        for v in adj_list[u]:
            indegree[v] += 1
Kahn's Algorithm
Kahn's algorithm is a form of Breadth-First Search in which nodes with lower indegrees are placed on the queue before nodes with higher indegrees.
The algorithm is as follows:
Calculate the indegree of each node.
Add all nodes with an indegree of 0 to a queue.
While the queue is not empty:
Dequeue the first node from the queue and add it to the topological order.
For each neighbor of the node, decrement its indegree by 1. If the neighbor's indegree is now 0, add it to the queue.
Return the topological order.
Walkthrough
We'll walkthrough how the algorithm works for the graph given by the adjacency list below:
    adjList = {    
        0: [1, 3],    
        1: [2],
        2: [],
        3: [1, 4, 5],
        4: [5],
        5: []
    }    
0
1
2
3
4
5
Step 1:
Calculate the indegree of each node.
0
0
1
2
2
1
3
1
4
1
5
2
The indegree is shown next to each node.
Step 2:
Add all nodes with an indegree of 0 to the queue.
0
0
1
2
2
1
3
1
4
1
5
2
queue
[0]
Step 3:
While the queue is not empty:
Deque the first node from the queue and add it to the topological sort.
VISUALIZATION
Full Screen
0
0
1
2
2
1
3
1
4
1
5
2
order
[]
queue
[0]

enqueue nodes with indegree 0

0 / 1

1x
Decrement the indegree of each neighbor of the node. If this results in a neighbor having an indegree of 0, add it to the queue.
VISUALIZATION
Full Screen
0
0
1
2
2
1
3
1
4
1
5
2
order
[0]
queue
[]

dequeue and add node 0 to topological sort

0 / 1

1x
We have fully processed node 1, so now repeat the process of dequeuing and decrementing indegrees for the next node in the queue until the queue is empty.
VISUALIZATION
Full Screen
0
0
1
1
2
1
3
0
4
1
5
2
order
[0]
queue
[3]

decrement indegree of neighbors

0 / 8

1x
Step 4:
Return the topological order.
VISUALIZATION
Full Screen
0
0
1
0
2
0
3
0
4
0
5
0
order
[0, 3, 1, 4, 2, 5]
queue
[]

dequeue and add node 5 to topological sort

0 / 1

1x
Solution
SOLUTION
Python
Language
from collections import deque

def topological_sort(adj_list, n):

  # calculate indegree of each node
  indegree = [0] * n
  for u in adj_list:
      for v in adj_list[u]:
          indegree[v] += 1

  # enqueue nodes with indegree 0
  queue = deque([u for u in range(n) if indegree[u] == 0])

  order = []
  while queue:
      u = queue.popleft()
      order.append(u)
      
      for v in adj_list.get(u, []):
          indegree[v] -= 1
          if indegree[v] == 0:
              queue.append(v)

  return order if len(order) == n else []
What is the time complexity of this solution?
1

O(V + E)

2

O(n³)

3

O(n * logn)

4

O(x * y)

Mark as read

Next: Course Schedule

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
Comments

(18)

Comment
Anonymous
​
Sort By
Popular
Sort By
A
AcceptableFuchsiaFrog410
Top 5%
• 1 year ago

This is amazing, could you make a page on Dijkstra's algo?

39

Reply
xiaoxiao liu
Premium
• 2 months ago

they actually made it!!

1

Reply
K
kapild.fb
Premium
• 10 months ago

This is an interesting approach that uses in-degree to perform topological sorting via BFS. In the CVL algorithm book that I’ve read, the topological sort is done using DFS, where nodes are added to a stack in the order they finish. You might consider trying that as an alternative approach

5

Reply
Sayan Sarkar
Top 10%
• 7 months ago

True, This is the first time I am seeing about using BFS for topological sorting.

1

Reply
S
SubjectiveIndigoSkink289
• 4 months ago

Wow, I had never seen this before. Great explanation! Minor nit and opportunity for improvement:

While the following statement is factual:

Topological sort takes a directed acyclic graph (DAG) and turns it into a linear ordering of nodes such that the directed edges only point forward, from left-to-right:

It's a bit abstract and hard to digest for people seeing this for the first time. The first question that popped up in my mind was, "But why would I want to use this?" So I asked Claude.ai:

The key insight is that a topological sort essentially "flattens" a partial ordering (represented by the DAG) into a total ordering (a sequence) while preserving all the dependency constraints. Note that topological sorts are not unique - a DAG may have multiple valid topological orderings.

It also gave concrete use cases, which was helpful. (scheduling, dependency resolution, package management, etc.)

4

Reply
S
SubjectiveIndigoSkink289
• 4 months ago

Would also be nice to explain the significance of when the length of the topological sort is not equal to the number of vertices. (i.e. that a cycle exists)

1

Reply
H
HighGrayPorcupine484
Premium
• 2 months ago

Should this page be called "Topological Sort"? There's already a Graphs Overview page under DFS

1

Reply
whm
Premium
• 2 months ago

Should this page called "Topological Sort"? there's already a "Graphs" Overview page under DFS

1

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Indegrees

Kahn's Algorithm

Walkthrough