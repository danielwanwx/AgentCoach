# Breadth-First Search Introduction | Hello Interview

> Source: https://www.hellointerview.com/learn/code/breadth-first-search/introduction
> Scraped: 2026-03-30



Breadth First Search
Breadth-First Search (BFS) is a level-by-level traversal algorithm for trees and graphs. Unlike DFS which dives deep into one path before backtracking, BFS explores all nodes at the current level before moving to the next level. This makes BFS the go-to algorithm when you need shortest paths or level-order processing.
bfs(root)
    queue = [root]
    
    while queue not empty
        node = queue.pop()
        visit(node)
        queue.add(node.left)
        queue.add(node.right)
A
1
B
C
D
E
F
G
Watch how BFS visits the tree level by level: first A, then B and C (level 2), then D, E, F, and G (level 3). The queue ensures nodes are processed in the order they were discovered, creating this breadth-first behavior. We will explore BFS in-depth in upcoming lessons.
This module teaches you how to solve coding interview questions using breadth-first search by focusing on questions that are best solved using BFS rather than Depth-First Search. It's divided into 2 sections:
Binary Trees
We start by learning how breadth-first search traverses the nodes in a binary tree, which will teach us the fundamentals of the algorithm. We then look at practice problems that are best solved using BFS.
Graphs
We then look at the two most common ways graphs are represented during the coding interview, and how to traverse both representations with BFS. Then we work through problems that give us practice with the different types of graph problems that are best solved using BFS.

Mark as read

Next: Breadth-First Search Fundamentals

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
Dez Dezsson
Premium
• 8 months ago

Please fix the link pointing to Graphs Overview

15

Reply
S
sulattphone
• 1 year ago

Are we missing a page similar to this for DFS? On the left navigation menu, there's no introduction or overview under DFS and just jumps right into Graphs. So there's no DFS information for Binary Trees like this page has for BFS.

2

Reply
retr0
• 1 year ago

Make sure to check the 'introduction' subsection in the left navigation menu. The right menu takes you directly to exercises.
https://www.hellointerview.com/learn/code/depth-first-search/introduction

0

Reply
Kartik Khunda
• 1 year ago

Yeah I am also seeing the same. Hoping they would fix it asap

0

Reply
K
KnowledgeSeeker
Premium
• 1 month ago

Can you add Java and python implementation ?

0

Reply

Shivam Chauhan

Admin
• 1 month ago

Hey, as stated in the article the implementations and deep dives are in next lessons BFS Fundamentals

1

Reply
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Breadth First Search

Binary Trees

Graphs

