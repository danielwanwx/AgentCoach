# Copy Graph

> Source: https://www.hellointerview.com/learn/code/depth-first-search/copy-graph
> Scraped: 2026-03-30


Copy Graph
easy
DESCRIPTION

Given a reference to a variable node which is part of an undirected, connected graph, write a function to return a copy of the graph as an adjacency list in dictionary form. The keys of the adjacency list are the values of the nodes, and the values are the neighbors of the nodes.

node is an instance of the following class, where neighbors is a list of references to other nodes in the graph (also of type IntGraphNode):

class IntGraphNode:
    def __init__(self, value = 0, neighbors = None):
    self.value = value
    self.neighbors = neighbors if neighbors is not None else []

Example 1:

Input:

node = IntGraphNode(1, [IntGraphNode(2), IntGraphNode(3)])
3
2
1

Output:

>>> copy_graph(node)
{1: [2, 3], 2: [1], 3: [1]}

Example 2: Input:

n1 = IntGraphNode(1)
n2 = IntGraphNode(2)
n3 = IntGraphNode(3)
n4 = IntGraphNode(4)

n1.neighbors = [n2, n4]
n2.neighbors = [n1, n3]
n3.neighbors = [n2, n4]
n4.neighbors = [n1, n3]
4
3
2
1

Output:

>>> copy_graph(n1)
{1: [2, 4], 2: [1, 3], 3: [2, 4], 4: [1, 3]}
CODE EDITOR
Python
​
Full Screen
1
2
3
4
5
6
7
8
9
10
11
from typing import Dict, List
# class IntGraphNode:
#     def __init__(self, value, id, neighbors):
#         self.value = value
#         self.id = id
#         self.neighbors = neighbors
class Solution:
    def copy_graph(self, node: IntGraphNode) -> Dict[int, List[int]]:
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
This solution uses depth-first search to traverse each node in the original graph. We can define a recursive helper function dfs that takes in an input node to help us perform the DFS traversal.
At each node, we:
Add the value of the node as a key in the adjacency list, and a list of its neighbor's values as the value in the dictionary.
Recursively call the dfs function on each neighbor of the node.
The adjacency list also helps us keep track of visited nodes. If we call dfs on a node that has already been added to the adjacency list, this means we have already visited the node, so we can return right away before making any more recursive calls.
SOLUTION
Python
Language
# class IntGraphNode:
#     value: int
#     id: int
#     neighbors: List[IntGraphNode]

def copy_graph(node):
  adj_list = {}

  def dfs(node):
    if node.value in adj_list:
      return
   
    adj_list[node.value] = [n.value for n in node.neighbors]
    for neighbor in node.neighbors:
      dfs(neighbor)

  if node:
    dfs(node)

  return adj_list
We can now take a closer look at the solution by visualizing each step as it traverses the graph below:
3
2
1
0
Initialization
The first step is to initialize adj_list as an empty dictionary. We will return this dictionary at the end, after the depth-first search traversal is complete. We then define the recursive helper function dfs that takes a node as input, and make the initial call to dfs with the input node.
VISUALIZATION
Python
Language
Full Screen
# class IntGraphNode:
#     value: int
#     id: int
#     neighbors: List[IntGraphNode]

def copy_graph(node):
  adj_list = {}

  def dfs(node):
    if node.value in adj_list:
      return
   
    adj_list[node.value] = [n.value for n in node.neighbors]
    for neighbor in node.neighbors:
      dfs(neighbor)

  if node:
    dfs(node)

  return adj_list
3
2
1
0

copy graph

0 / 2

1x
Defining both adj_list and the helper dfs function inside the main function ensures us that:
each call to the recursive function can access adj_list directly
the scope of adj_list is limited to the main function, which means that other parts of the code cannot modify it.
Depth-First Search
When the dfs function is called with a node, it first checks if the node is already present in the adj_list dictionary. If it isn't, it adds the node to the dictionary. The key is the value of the node, and the value is a list of the values of each of the node's neighbors.
VISUALIZATION
Python
Language
Full Screen
# class IntGraphNode:
#     value: int
#     id: int
#     neighbors: List[IntGraphNode]

def copy_graph(node):
  adj_list = {}

  def dfs(node):
    if node.value in adj_list:
      return
   
    adj_list[node.value] = [n.value for n in node.neighbors]
    for neighbor in node.neighbors:
      dfs(neighbor)

  if node:
    dfs(node)

  return adj_list
def dfs(node):
  if node.value in adj_list:
    return

  adj_list[node.value] = [n.value for n in node.neighbors]
  for neighbor in node.neighbors:
    dfs(neighbor)
3
2
1
0
adj_list
{}

recursive call

0 / 1

1x
Then, it recursively calls dfs on each neighbor of the original node.
VISUALIZATION
Python
Language
Full Screen
# class IntGraphNode:
#     value: int
#     id: int
#     neighbors: List[IntGraphNode]

def copy_graph(node):
  adj_list = {}

  def dfs(node):
    if node.value in adj_list:
      return
   
    adj_list[node.value] = [n.value for n in node.neighbors]
    for neighbor in node.neighbors:
      dfs(neighbor)

  if node:
    dfs(node)

  return adj_list
def dfs(node):
  if node.value in adj_list:
    return

  adj_list[node.value] = [n.value for n in node.neighbors]
  for neighbor in node.neighbors:
    dfs(neighbor)
3
2
1
0
adj_list
{0: [1]}

add to adj_list

0 / 5

1x
Recursive call to `dfs`
When dfs is called on a node that is already present in adj_list, it returns immediately without making any more recursive calls, which helps us avoid infinite loops in the graph. After returning, the function continues to the next neighbor of the current node.
VISUALIZATION
Python
Language
Full Screen
# class IntGraphNode:
#     value: int
#     id: int
#     neighbors: List[IntGraphNode]

def copy_graph(node):
  adj_list = {}

  def dfs(node):
    if node.value in adj_list:
      return
   
    adj_list[node.value] = [n.value for n in node.neighbors]
    for neighbor in node.neighbors:
      dfs(neighbor)

  if node:
    dfs(node)

  return adj_list
def dfs(node):
  if node.value in adj_list:
    return

  adj_list[node.value] = [n.value for n in node.neighbors]
  for neighbor in node.neighbors:
    dfs(neighbor)
def dfs(node):
  if node.value in adj_list:
    return

  adj_list[node.value] = [n.value for n in node.neighbors]
  for neighbor in node.neighbors:
    dfs(neighbor)
def dfs(node):
  if node.value in adj_list:
    return

  adj_list[node.value] = [n.value for n in node.neighbors]
  for neighbor in node.neighbors:
    dfs(neighbor)
3
2
1
0
adj_list
{0: [1], 1: [0,2]}

recursive call

0 / 2

1x
Returning from a previously visited node.
This process continues until all nodes in the original graph have been visited and added to the adj_list dictionary.
Animated Solution
adjList
​
|
adjList
list of neighbors
Try these examples:
Single
Two Nodes
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
# class IntGraphNode:
#     value: int
#     id: int
#     neighbors: List[IntGraphNode]

def copy_graph(node):
  adj_list = {}

  def dfs(node):
    if node.value in adj_list:
      return
   
    adj_list[node.value] = [n.value for n in node.neighbors]
    for neighbor in node.neighbors:
      dfs(neighbor)

  if node:
    dfs(node)

  return adj_list
3
2
1
0

copy graph

0 / 26

1x
What is the time complexity of this solution?
1

O(2ⁿ)

2

O(N + M)

3

O(1)

4

O(n * logn)

Mark as read

Next: Graph Valid Tree

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

(25)

Comment
Anonymous
​
Sort By
Popular
Sort By
E
ExperiencedAmethystConstrictor277
Top 10%
• 1 year ago

I'm a bit confused about the requirement here. It seems to me this problem is asking for creating a deep copy for each node in the original graph, and then converting that copied graph into an adjacency list. But the given solution did not create a deep copy for each node, instead it  just converted the graph from a node-based structure to an adjacency list. Did i misunderstand the requirement?

21

Reply
Abhay Singh
Top 1%
• 1 year ago

Java Solution:

class Solution {

    public Node dfs(Node node, Map<Node, Node> mp){
        if(node == null) return null;

        Node newNode = new Node();
        newNode.val = node.val;

        mp.put(node, newNode);

        for(Node neighbor : node.neighbors){
            if(mp.get(neighbor) == null){
                Node newNeighbor = dfs(neighbor, mp);

                newNeighbor.neighbors.add(newNode); // 2 added 1 

                mp.put(neighbor, newNeighbor);
            }else{
                Node newNeighbor = mp.get(neighbor);

                newNeighbor.neighbors.add(newNode); // 1 added 2
            }
        }

        return newNode;
    }

    public Node cloneGraph(Node node) {
        Map<Node,Node> mp = new HashMap<>();

        return dfs(node, mp);
    }
}
Show More

4

Reply
M
MathematicalRedWombat488
Premium
• 4 months ago

This is medium difficulty problem not easy one.

3

Reply
V
Valentino
• 4 months ago

I think there is no Leetcode counterpart to this problem. The link they provided sends us to Clone Graph, which is indeed a Medium problem but also a different one.

2

Reply
H
hkim85
• 1 year ago

some of this page says cloneGraph while others say copy_graph

1

Reply
Joyce Wambui
Premium
• 1 year ago

yeah I've seen that too. The question on leetcode is clone graph but this one is copy graph

4

Reply
V
Valentino
• 4 months ago

They are not the same

0

Reply
B
Binary.Beast
Premium
• 2 days ago
• edited 2 days ago

In the above solution, you are accumulating all edges first(effectively visiting all neighbours first) and then going to depth from there. This is more like a BFS. We can complete this one for loop in pure DFS fashion.


public class Solution {
   Map<Integer, List<Integer>> copyNodes = new HashMap<>();

   public Map<Integer, List<Integer>> copy_graph(IntGraphNode node) {
       copyNodes.clear();
       if (node == null) return copyNodes;
       dfsHelper(node, new HashSet<>());
       // could have used copyNodes key for tracking visited nodes
       return copyNodes;
   }

   private void dfsHelper(IntGraphNode current, Set<IntGraphNode> visited) {
       if (visited.contains(current)) return;
       visited.add(current);

       List<Integer> nodeNeighbours = new ArrayList<>();
       copyNodes.put(current.value, nodeNeighbours);

       for (IntGraphNode neighbor : current.neighbors) {
           nodeNeighbours.add(neighbor.value);
           dfsHelper(neighbor, visited);
       }
   }
}

Show More

0

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

Initialization

Depth-First Search

Animated Solution
