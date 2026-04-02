# Graph Valid Tree

> Source: https://www.hellointerview.com/learn/code/depth-first-search/graph-valid-tree
> Scraped: 2026-03-30


medium
DESCRIPTION (inspired by Lintcode.com)

You are given an integer n and a list of undirected edges where each entry in the list is a pair of integers representing an edge between nodes 0 and n - 1. You have to write a function to check whether these edges make up a valid tree.

There will be no duplicate edges in the edges list. (i.e. [0, 1] and [1, 0] will not appear together in the list).

Input:

n = 4 
edges = [[0, 1], [2, 3]]
3
2
1
0

Output:

false # the graph is not connected.
CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def graph_valid_tree(self, n: int, edges: List[List[int]]) -> bool:
        # Your code goes here
        pass
Results

AI Feedback

Past Submissions

Reset
View Answer
Run

Run your code to see results here

Have suggestions or found something wrong?

Explanation
In order for a graph to be a valid tree, it must satisfy the following conditions:
The graph must contain no cycles.
There should be a single connected component - if we start from any node, we should be able to reach all other nodes.
We can use a depth-first search to check for these conditions. We'll start by converting the list of edges into an adjacency list. This allows us to easily find the neighbors of any node, which is required by the depth-first search algorithm.
We'll walkthrough how this solution determines that a graph with a cycle is not a valid tree when n = 5 and edges = [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]], which forms the following graph:
4
3
2
1
0
VISUALIZATION
Python
Language
Full Screen
def validTree(n, edges):
  adj_list = [[] for _ in range(n)]
  for u, v in edges:
    adj_list[u].append(v)
    adj_list[v].append(u)

  # Use DFS to check if the graph is a valid tree
  visited = [False] * n
  if hasCycle(adj_list, 0, visited, -1):
    return False

  return all(visited)

def hasCycle(adj_list, node, visited, parent):
  visited[node] = True
  for neighbor in adj_list[node]:
    if visited[neighbor] and parent != neighbor:
      return True
    elif not visited[neighbor] and \
        hasCycle(adj_list, neighbor, visited, node):
      return True
  return False
[0, 1]
[1, 2]
[2, 3]
[1, 3]
[1, 4]

graph valid tree

0 / 6

1x
Building the adjacency list.
Depth-First Search
Next, we use a recursive function hasCycle to check for cycles in the graph. Each call to hasCycle returns true if there is a cycle connected to the input node. The function first marks the current node as visited, then recursively visits all its neighbors using depth-first search, checking for cycles. To keep track of the nodes we've visited already, we use a boolean array visited.
VISUALIZATION
Python
Language
Full Screen
def validTree(n, edges):
  adj_list = [[] for _ in range(n)]
  for u, v in edges:
    adj_list[u].append(v)
    adj_list[v].append(u)

  # Use DFS to check if the graph is a valid tree
  visited = [False] * n
  if hasCycle(adj_list, 0, visited, -1):
    return False

  return all(visited)

def hasCycle(adj_list, node, visited, parent):
  visited[node] = True
  for neighbor in adj_list[node]:
    if visited[neighbor] and parent != neighbor:
      return True
    elif not visited[neighbor] and \
        hasCycle(adj_list, neighbor, visited, node):
      return True
  return False
[0, 1]
[1, 2]
[2, 3]
[1, 3]
[1, 4]
[u, v]
node
0:
1
1:
0
2
3
4
2:
1
3
3:
2
1
4:
1

build adjacency list

0 / 5

1x
Recursively calling `hasCycle`
Detecting a Cycle
If at any point during our search, we encounter a node that we've already visited and is not the parent of the current node, then we've found a cycle. We return true to indicate that the graph is not a valid tree, which causes the depth-first search to terminate early, until the main function returns false.
VISUALIZATION
Python
Language
Full Screen
def validTree(n, edges):
  adj_list = [[] for _ in range(n)]
  for u, v in edges:
    adj_list[u].append(v)
    adj_list[v].append(u)

  # Use DFS to check if the graph is a valid tree
  visited = [False] * n
  if hasCycle(adj_list, 0, visited, -1):
    return False

  return all(visited)

def hasCycle(adj_list, node, visited, parent):
  visited[node] = True
  for neighbor in adj_list[node]:
    if visited[neighbor] and parent != neighbor:
      return True
    elif not visited[neighbor] and \
        hasCycle(adj_list, neighbor, visited, node):
      return True
  return False
def hasCycle(adj_list, node, visited, parent):
  visited[node] = True
  for neighbor in adj_list[node]:
    if visited[neighbor] and parent != neighbor:
      return True
    elif not visited[neighbor] and \
        hasCycle(adj_list, neighbor, visited, node):
      return True
  return False
def hasCycle(adj_list, node, visited, parent):
  visited[node] = True
  for neighbor in adj_list[node]:
    if visited[neighbor] and parent != neighbor:
      return True
    elif not visited[neighbor] and \
        hasCycle(adj_list, neighbor, visited, node):
      return True
  return False
def hasCycle(adj_list, node, visited, parent):
  visited[node] = True
  for neighbor in adj_list[node]:
    if visited[neighbor] and parent != neighbor:
      return True
    elif not visited[neighbor] and \
        hasCycle(adj_list, neighbor, visited, node):
      return True
  return False
def hasCycle(adj_list, node, visited, parent):
  visited[node] = True
  for neighbor in adj_list[node]:
    if visited[neighbor] and parent != neighbor:
      return True
    elif not visited[neighbor] and \
        hasCycle(adj_list, neighbor, visited, node):
      return True
  return False
[0, 1]
[1, 2]
[2, 3]
[1, 3]
[1, 4]
[u, v]
node
0:
1
1:
0
2
3
4
2:
1
3
3:
2
1
4:
1
node
parent
neighbor
visited
T
T
T
T
F
node: 3
parent: 2

iterate over neighbors

0 / 5

1x
The node `1` has already been visited and is not the parent of the current node `3`.
If no cycle is found, then we have to make sure there is a single connected component. We do this by checking if all nodes have been visited. If so, the graph is a valid tree and we return true. If not, then the graph is not a valid tree and we return false.
Animated Solution
edges
​
|
edges
list of nodes [start, end]
n
​
|
n
integer
Try these examples:
Valid Tree
Cycle
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def validTree(n, edges):
  adj_list = [[] for _ in range(n)]
  for u, v in edges:
    adj_list[u].append(v)
    adj_list[v].append(u)

  # Use DFS to check if the graph is a valid tree
  visited = [False] * n
  if hasCycle(adj_list, 0, visited, -1):
    return False

  return all(visited)

def hasCycle(adj_list, node, visited, parent):
  visited[node] = True
  for neighbor in adj_list[node]:
    if visited[neighbor] and parent != neighbor:
      return True
    elif not visited[neighbor] and \
        hasCycle(adj_list, neighbor, visited, node):
      return True
  return False
[0, 1]
[1, 2]
[2, 3]
[1, 3]
[1, 4]

graph valid tree

0 / 27

1x
Complexity Analysis
For this problem, let n be the number of nodes and e be the number of edges.
What is the time complexity of this solution?
1

O(2ⁿ)

2

O(n + e)

3

O(m * n * 4^L)

4

O(m * n)

Mark as read

Next: Matrices

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

(30)

Comment
Anonymous
​
Sort By
Popular
Sort By
R
RadicalAquaBedbug232
Top 10%
• 1 year ago

Looks like same as: https://leetcode.com/problems/graph-valid-tree/description/

(to use leetcode in all links)

14

Reply
Nisarg B
• 8 months ago

its premium only

4

Reply
Shannon Monasco
• 1 year ago

There is an assumption built into your visited List that node values:

are unique
are contiguous for [0, n)

I imagine these are intended to be true but they are not called out in the given.

10

Reply
S
SubjectiveIndigoSkink289
• 4 months ago

Implied by your 2nd statement, but also that a -1 node doesn't exist. i.e. the initial value for parent

0

Reply
B
berkob
• 1 year ago

Is test case #2 valid?
n: 2, edges: [[0,1],[1,0]]

Am I misunderstanding the following constraint?
“There will be no duplicate edges in the edges list. (i.e. [0, 1] and [1, 0] will not appear together in the list).”

6

Reply
Mike Perez
• 3 months ago
def validTree(n, edges):
    # Mathematical property: A tree with 'n' nodes MUST have exactly 'n - 1' edges.
    # If it has more, there is a cycle. If it has fewer, it is disconnected.
    if len(edges) != n - 1:
        return False

    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
        
    # Use a set to keep track of visited nodes to avoid infinite loops.
    visited = set()

    def dfs(node):
        # Mark the current node as visited.
        visited.add(node)
        
        # Explore all neighbors of the current node.
        for neighbor in adj[node]:
            if neighbor not in visited:
                dfs(neighbor)
  
    dfs(0)
    
    # If we visited all 'n' nodes, it means the graph is connected.
    # Because we already checked that edges == n - 1, connectivity guarantees no cycles.
    return len(visited) == n
Show More

5

Reply
Satya Dasara
Premium
• 2 months ago

Two condition for a tree to be valid:

No cycles
Only one connected component

While checking for cycle in DFS make sure you exclude parent from cycle check to prevent false cycle flag
Take one node and do DFS to visit all nodes
If length of visited != n then it means more than one connected component
In other words there are nodes not present in visited

from collections import defaultdict

class Solution:
    def graph_valid_tree(self, n: int, edges: List[List[int]]):
        graph = defaultdict(list)

        for edge in edges:
            a, b = edge
            graph[a].append(b)
            graph[b].append(a)
        
        visited = set()
        cycle = False

        def dfs(node, parent):
            if node is None:
                return
            
            nonlocal visited
            nonlocal graph
            nonlocal cycle

            visited.add(node)

            for nei in graph[node]:
                if nei not in visited:
                    dfs(nei, node)
                # Important to check for parent to prevent false cycle detection
                elif nei != parent:
                    cycle = True
            
            return
        
        dfs(0, -1)
        
        if cycle:
            return False

        for node in range(n):
            if node not in visited:
                return False
        
        return True
Show More

1

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

Depth-First Search

Detecting a Cycle

Animated Solution

Complexity Analysis
