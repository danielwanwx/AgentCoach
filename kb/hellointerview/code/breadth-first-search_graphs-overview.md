# Graphs Overview

> Source: https://www.hellointerview.com/learn/code/breadth-first-search/graphs-overview
> Scraped: 2026-03-30



Breadth-First Search
Graphs Overview
Like Depth-First Search, breadth-first search is also used to traverse graphs. In this section, we'll cover how to implement BFS on both adjacency lists and matrices, as well as the types of problems that are best solved using BFS.
Just like with depth-first search, the most important thing to remember when implementing BFS on a graph is to keep track of visited nodes to avoid infinite loops. If we try to enqueue a node that has already been visited, we should skip it instead of adding it to the queue.
BFS on an Adjacency List
To traverse a graph represented with an adjacency list with BFS:
Choose a starting node and add it to the queue (we start with the first node in the adjacency list Node "1" in the example below).
While the queue is not empty, remove the node at the front of the queue and add it to the set of visited nodes.
Add the children of the node to the back of the queue (if they haven't been visited yet).
Repeat steps 2 and 3 until the queue is empty.
The animation shows how BFS traverses the graph represented by:
SOLUTION
Python
Language
adjList = {
    "1": ["2", "4"],
    "2": ["1", "3"],
    "3": ["2", "4"],
    "4": ["1", "3", "5"],
    "5": ["4"]
}
VISUALIZATION
Python
Language
Full Screen
from collections import deque

def bfs(start):
  visited = set([start])
  queue = deque([start])

  while queue:
    node = queue.popleft()
    for neighbor in adjList[node]:
      if neighbor not in visited:
        visited.add(neighbor)
        queue.append(neighbor)

5
4
3
2
1

0 / 11

1x
BFS on an Matrix (2D Grid)
To traverse a graph represented as a matrix with BFS:
Choose a starting node and add it to the queue (we start with top left node in the example below).
While the queue is not empty, remove the node at the front of the queue and add it to the set of visited nodes.
Add the four neighbors of the node to the back of the queue (if they haven't been visited yet and are within the bounds of the matrix).
Repeat steps 2 and 3 until the queue is empty.
The animation shows how BFS traverses the graph represented by:
SOLUTION
Python
Language
matrix = [
    [0, 0, 0],
    [0, 1, 1],
    [0, 1, 0]
]
VISUALIZATION
Python
Language
Full Screen
from collections import deque

def bfs(grid):
  visited = set()
  # up, down, left, right
  directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

  queue = deque([(0, 0)])
  visited.add((0, 0))

  while queue:
    row, col = queue.popleft()

    # enqueue neighbors
    for dr, dc in directions:
      n_row = row + dr
      m_col = col + dc

      # check bounds and if neighbor is visited
      if 0 <= n_row < len(grid) \
                and 0 <= m_col < len(grid[0]) \
                and (n_row, m_col) not in visited:
        queue.append((n_row, m_col))
        visited.add((n_row, m_col))

0
0
0
0
1
1
0
1
0

0 / 20

1x
Nodes at a Level
Like binary trees, graphs can also have levels. In a graph, a level is defined as the number of edges between the root node and the current node, which is also known as the "distance" between the two nodes.
This is the primary use case of BFS in graphs: to solve questions that involve traversing the graph level-by-level, so we should be familiar with this pattern for both adjacency lists and matrices.
0
1
2
3
1
2
3
4
2
3
4
5
3
4
5
6
Nodes in a 2D-grid labeled with their distance from the top-left node.
2
1
2
1
0
Nodes in graph labeled with their distance from the top-left node (Node(0)).
And just like binary trees, the BFS algorithm can be extended to know when we have finished processing all nodes at a level. We can do this by adding a for-loop that iterates over the size of the queue at the beginning of each level.
Adjacency List Level-By-Level
SOLUTION
Python
Language
from collections import deque

def bfs_levels(graph, start):
    queue = deque([start])
    visited = set()
    visited.add(start)
    levels = []

    while queue:
        level_size = len(queue)
        current_level = []

        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        # IMPORTANT
        # we have finished processing all nodes at the current level
        levels.append(current_level)

    return levels
Matrix Level-By-Level
SOLUTION
Python
Language
from collections import deque

def bfs_level_by_level(matrix):
    rows, cols = len(matrix), len(matrix[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # start at the top-left corner
    queue = deque([(0, 0)])
    visited = set([(0, 0)])

    levels = []
    while queue:
        level_size = len(queue)
        current_level = []

        for _ in range(level_size):
            row, col = queue.popleft()
            current_level.append((row, col))
            for dr, dc in directions:
                r, c = row + dr, col + dc
                if 0 <= r < rows and 0 <= c < cols and (r, c) not in visited:
                    visited.add((r, c))
                    queue.append((r, c))

        # IMPORTANT
        # we have finished processing all nodes at this level
        levels.append(current_level)

    return levels
Shortest Path in a Graph
A consequence of the level-by-level nature of BFS traversal is that we can use it to find the shortest path between two nodes in a graph. Because BFS traverses the graph level-by-level, the first time we reach the destination node will be on the shortest path between the two nodes.
The animation below shows how BFS finds the shortest path between the top left node in the matrix and the first node with value "1":
VISUALIZATION
Full Screen
0
0
0
0
0
0
1
0
0
0
0
0
0
0
0
0

0 / 8

1x
Compare this to depth-first search, where the first path it encounters might not be the shortest path between two nodes:
VISUALIZATION
Full Screen
0
0
0
0
0
0
1
0
0
0
0
0
0
0
0
0

simple matrix DFS traversal

0 / 19

1x
To find the shortest path using DFS, we would have to explore all possible paths and then compare the lengths of each path to find the shortest one at the end. This makes BFS a better choice for any question that involves finding the shortest path between two nodes in a graph.

Mark as read

Next: Minimum Knight Moves

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

(12)

Comment
Anonymous
​
Sort By
Popular
Sort By
P
PassiveBlackChimpanzee437
Top 10%
• 1 year ago

this should be paid content, they are TOO good

17

Reply
Venkataramanan Venkateswaran
• 7 months ago

In the code for BFS on an Adjacency List and BFS on an Matrix (2D Grid), you use a list as a queue and do queue.pop(0). This will run in O(n) time. The better solution is to directly use a deque in python and do queue.popleft(). This will run in O(1) time.

6

Reply
L
Luiz
Premium
• 6 months ago

Also, if you are popping it from the end is a stack (LIFO - Last In First Out), not a queue (FIFO - First In First Out), no matter how your variable name misleads you... :)

1

Reply
Venkataramanan Venkateswaran
• 6 months ago

queue.popleft() pops from the front, not the end.

0

Reply
L
Luiz
Premium
• 6 months ago

Hi Venkata,
I am talking about his first code on the BFS on an Adjacency List way above. Below is the excerpt (it is clearly a pop, not a popleft :)):

def bfs(start):
visited = set([start])
queue = [start]

while queue:
node = queue.pop(0)
for neighbor in adjList[node]:
if neighbor not in visited:
visited.add(neighbor)
queue.append(neighbor)

0

Reply
Anh Minh Nguyễn Đoàn
• 3 months ago

that code use pop(0) => it will pop front but takes O(n) time

2

Reply
Faizan Patel
• 1 year ago

This Graph overview, previous page (Maximum Width of Binary Tree) and the next page (Minimum Knight move) are missing from the navigation menu on the sidebar under BFS. The menu directly jumps from Zigzag level order to Rotting Oranges problem.

2

Reply
SM
Sriharsha Madala
Premium
• 7 months ago

It would be helpful to add one more article on how we can backtrack in BFS to return that shortest path.

1

Reply
I
ImmediateBronzePartridge132
Premium
• 4 days ago

def bfs(start):

visited = set([start])

queue = [start]

while queue:

node = queue.pop(0)

for neighbor in adjList[node]:

  if neighbor not in visited:

    visited.add(neighbor)

    queue.append(neighbor)


Can this be updated to use a deque? For someone who is going through the problems in order it can be a little confusing as to why a list and pop are used instead of deque and popLeft

0

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

BFS on an Adjacency List

BFS on an Matrix (2D Grid)

Nodes at a Level

Adjacency List Level-By-Level

Matrix Level-By-Level

Shortest Path in a Graph
