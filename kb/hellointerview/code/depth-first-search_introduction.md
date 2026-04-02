# Introduction

> Source: https://www.hellointerview.com/learn/code/depth-first-search/introduction
> Scraped: 2026-03-30


Depth-First Search
Introduction
Depth-First Search (DFS) is a traversal algorithm for trees and graphs. It's called "depth-first" because it explores as far down a path as possible before backtracking to try another path. This makes DFS incredibly versatile, and it's arguably the most important algorithm to master for coding interviews.
dfs(node)
    if node == null
        return
    
    visit(node)
    dfs(node.left)
    dfs(node.right)
A
1
B
C
D
E
F
G
Watch how DFS goes all the way down the left side (A → B → D) before backtracking to visit E, then finally exploring C's subtree. This "go deep, then backtrack" behavior is what separates DFS from Breadth-First Search, which explores all nodes at one level before moving to the next. We will explore DFS in-depth in upcoming lessons.
Basic DFS Pattern
At its core, DFS follows this simple pattern:
dfs(node)
    if node is null
        return
    
    // process the current node
    
    dfs(node.left)
    dfs(node.right)
For graphs, you also need to track visited nodes to avoid infinite loops:
dfs(node, visited)
    if node in visited
        return
    
    visited.add(node)
    
    for neighbor in node.neighbors
        dfs(neighbor, visited)
Module Overview
This module teaches you how to solve coding interview questions using depth-first search. It's divided into two main sections:
Binary Trees
We start with DFS on binary trees because they're the simplest structure to work with. Trees have no cycles, so you don't need to track visited nodes. You'll learn:
How the call stack enables backtracking
How to use return values to aggregate information from subtrees
Common patterns like finding depth, validating structure, and path problems
Graphs
Graph problems add complexity: you need to handle cycles, different representations (adjacency lists and matrices), and sometimes disconnected components. You'll practice:
DFS on adjacency list representations
DFS on 2D matrix grids
Patterns like connected components, boundary traversal, and cycle detection
After completing this module, continue to Breadth-First Search and Backtracking. Understanding when to use DFS vs BFS is critical. In short: use DFS when you need to explore all paths or find any valid solution, use BFS when you need the shortest path or level-by-level traversal.
Common DFS Problem Patterns
You'll encounter a few recurring patterns in DFS problems. Recognizing these patterns quickly will help you identify the right approach during interviews.
Counting Connected Components
One of the most common DFS applications is counting distinct groups or regions in a grid or graph. Think of it as "flood filling" each region and counting how many times you had to start a new fill.
Take this grid where 1 represents land and 0 represents water. The goal is to count distinct islands (groups of connected 1s):
[0, 1, 0, 0, 0, 0]
[0, 1, 1, 0, 1, 0]
[0, 0, 0, 1, 1, 0]
[1, 1, 0, 0, 0, 1]
[1, 1, 0, 0, 0, 1]
The answer is 4 because there are four separate islands.
The approach works like this: scan every cell in the grid from top-left to bottom-right. When you hit an unvisited 1, you've found a new island, so increment your count. Then run DFS to "flood" that entire island, marking every connected 1 as visited (typically by setting it to 0). When DFS returns, that island is fully consumed and won't be counted again.
Watch the visualization below to see this in action. Notice how DFS explores deeply in one direction before backtracking, and how the count variable only increases when we discover an entirely new island.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def count_islands(grid):
    rows, cols = len(grid), len(grid[0])
    visited = set()
    count = 0
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def dfs(r, c):
        if (r, c) in visited:
            return
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return
        if grid[r][c] != 1:
            return
        visited.add((r, c))
        for dr, dc in directions:
            dfs(r + dr, c + dc)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1 and (r, c) not in visited:
                dfs(r, c)
                count += 1

    return count
0
1
2
3
4
0
1
2
3
4
5
0
1
0
0
0
0
0
1
1
0
1
0
0
0
0
1
1
0
1
1
0
0
0
1
1
1
0
0
0
1
Variables
position
(-, -)
row
-
col
-
count
0
Start
Visited

Initialize count = 0. Scan the grid to find islands.

0 / 60

1x
DFS marks each island as visited, preventing double-counting
The outer loop finds new islands; the DFS consumes each one so we don't count it twice. This pattern applies to any "count distinct regions" problem, whether it's islands, rooms in a building, or connected components in a graph.
Boundary DFS
Some problems ask you to find cells that are connected to the edge of a grid, i.e. all connected cells which are on boundary of the matrix. The naive way is to check every cell and finding "can this cell reach the boundary?" But that's inefficient.
The trick is to flip the question: instead of checking if each cell can reach the border, start from the border and see which cells can be reached from this boundary cell. Run DFS from each relevant cell on the boundary, and everything you visit is "connected to the edge."
VISUALIZATION
Hide Code
Python
Language
Full Screen
def find_boundary_connected(grid):
    rows, cols = len(grid), len(grid[0])
    visited = set()
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def dfs(r, c):
        if (r, c) in visited:
            return
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return
        if grid[r][c] != 1:
            return
        visited.add((r, c))
        for dr, dc in directions:
            dfs(r + dr, c + dc)

    # Start DFS from boundary cells with value 1
    for r in range(rows):
        if grid[r][0] == 1: dfs(r, 0)
        if grid[r][cols-1] == 1: dfs(r, cols-1)
    for c in range(cols):
        if grid[0][c] == 1: dfs(0, c)
        if grid[rows-1][c] == 1: dfs(rows-1, c)
0
1
2
3
4
5
0
1
2
3
4
5
0
1
0
0
1
0
0
1
1
0
1
0
0
0
1
0
1
0
0
1
0
0
1
1
0
1
1
0
1
1
1
0
0
0
0
0
Variables
position
(-, -)
row
-
col
-
Start
Visited

Boundary DFS: Start from edges of the grid to find all land connected to boundaries.

0 / 34

1x
DFS starts from the boundary and marks everything connected to it
This pattern appears in problems like "Surrounded Regions" and "Pacific Atlantic Water Flow." The key insight is always the same: start from the boundary and work inward.
When to Use DFS
DFS excels when you need to:
Explore all possible paths (like finding all solutions or any valid solution)
Traverse hierarchical structures (trees, nested data)
Find connected components in graphs or grids
Detect cycles in graphs
Process nodes in a specific order (pre-order, in-order, post-order)
If you need the shortest path in an unweighted graph, use BFS instead. DFS finds a path, not necessarily the shortest one.

Mark as read

Next: Fundamentals

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

(6)

Comment
Anonymous
L
LowTomatoBarracuda499
Premium
• 2 months ago

In the Connected Components example, visualization seem to be incorrect. The code is following rows -> cols, but visualization is showing in cols -> rows. Validate step 8.

4

Reply
M
MeaningfulSapphireSailfish421
Premium
• 2 months ago
• edited 2 months ago

+1 looks like both the visualizations are incorrect!

1

Reply

Shivam Chauhan

Admin
• 2 months ago

Hey, the visualizations are actually moving across row -> cols. It is skipping the 0 or visited nodes and is focusing on traversing the dfs path. But, feedback taken and we have updated the visualization to show the full trace. Will be live soon in next release!

1

Reply
nailyk
Premium
• 2 months ago

in visualisation 1, the implementation of dfs function is missing

1

Reply
S
SimpleRoseRabbit195
• 1 month ago

we

nit: Typo: "be"

0

Reply
M
malinibhandaru
Premium
• 2 months ago

Moving "visited.add(r,c)"  before the "if (grid[r][c] != 1" would save a few more steps.

0

Reply
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Basic DFS Pattern

Module Overview

Binary Trees

Graphs

Common DFS Problem Patterns

Counting Connected Components

Boundary DFS

When to Use DFS
