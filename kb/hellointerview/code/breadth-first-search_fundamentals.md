# Breadth-First Search Fundamentals

> Source: https://www.hellointerview.com/learn/code/breadth-first-search/fundamentals
> Scraped: 2026-03-30

Breadth-First Search Fundamentals
5:21
7 chapters • 2 interactive checkpoints
BFS is a level-by-level traversal algorithm. It starts at the root node of the binary tree and visits all nodes at the current level before moving to the next level of the tree.
VISUALIZATION
Python
Language
Full Screen
def bfs(root):
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        curr_node = queue.popleft()
        result.append(curr_node.val)
        
        if curr_node.left:
            queue.append(curr_node.left)
        if curr_node.right:
            queue.append(curr_node.right)

    return result
4
2
1
3
7
6
9

breadth-first search

0 / 15

1x
The order in which BFS visits the nodes in a binary tree.
BFS Procedure
BFS uses a queue to keep track of the nodes it needs to visit, and follows these steps:
Start at the root node and add it to the queue.
While the queue is not empty, remove the node at the front of the queue and visit it.
Add the children of the node to the back queue.
Repeat steps 2 and 3 until the queue is empty, which means you've processed all nodes in the tree.
Queues in Python
In Python, you can use the deque class from the collections module to create a queue.
The deque class provides an append method to add elements to the end of the queue and a popleft method to remove elements from the front of the queue, both of which run in O(1) time.
Implementation
Below is a basic implementation of BFS on a binary tree. The result list stores the nodes in the order in which they are visited.
VISUALIZATION
Python
Language
Full Screen
def bfs(root):
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        curr_node = queue.popleft()
        result.append(curr_node.val)
        
        if curr_node.left:
            queue.append(curr_node.left)
        if curr_node.right:
            queue.append(curr_node.right)

    return result
4
2
1
3
7
6
9

breadth-first search

0 / 15

1x
Summary
BFS is a traversal algorithm that visits all nodes at a particular level before moving to the next level.
BFS uses a queue to keep track of the nodes it needs to visit.
Processing Levels
The distinguishing feature of BFS is that it visits all nodes at a particular level before moving onto the nodes at the next level.
Compared to depth-first search, BFS makes it much easier to tell when we have finished processing all nodes at a particular level. This makes it a natural candidate for questions that ask something about the nodes at each level, which is shown below in the Level-Order Traversal algorithm.
DESCRIPTION
Given a binary tree, return the level-order traversal of its nodes' values. (i.e., from left to right, level by level).
Input

4
2
1
3
7
6
9
Output
[[4], [2, 7], [1, 3, 6, 9]]
We can extend our basic BFS algorithm to calculate the number of nodes at each level by adding a for-loop that iterates over the size of the queue at the beginning of each level.
Each time the for-loop runs, we add the current node to the current_level list.
When the for-loop finishes, we have finished processing all nodes at that level, and we can add the current_level list to the result list. We can reset the current_level list to an empty list to prepare for the next level.
SOLUTION
Python
Language
from collections import deque
    
def level_order(root):
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        # number of nodes at the current level
        level_size = len(queue)
        current_level = []
        
        for _ in range(level_size):
            curr = queue.popleft()
            current_level.append(curr.val)
            
            if curr.left:
                queue.append(curr.left)
            if curr.right:
                queue.append(curr.right)
        
        # IMPORTANT
        # we have finished processing all nodes at the current level
        result.append(current_level)
        
    return result
To help you visualize how this algorithm works, the diagram below shows the state of the queue after we have finished processing the 2nd level of the tree.
Notice that queue contains the nodes at the 3rd level of the tree, [1, 3, 6, 9]. When we enter the next iteration of the while loop, the for loop will run 4 times to process these nodes.
from collections import deque
    
def level_order(root):
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        # number of nodes at current level
        level_size = len(queue)
        current_level = []
        
        for _ in range(level_size):
            curr = queue.popleft()
            current_level.append(curr.val)
            
            if curr.left:
                queue.append(curr.left)
            if curr.right:
                queue.append(curr.right)
        
        # IMPORTANT
        # we have finished processing all
        # nodes at the current level
        result.append(current_level)
        
    return result
4
2
1
3
7
6
9
queue
[1,3,6,9]
[1,3,6]
current_level
[2,7]
result
[[4]]
The state of the aglorithm after we have finished processing the nodes at the 2nd level of the tree.
Using a for-loop to iterate over the nodes at each level is such a common pattern that it is the version of BFS on binary trees you need to know for interviews. The practice problems we will look at next all use this version of BFS.
What is the time complexity of this solution?
1

O(n)

2

O(n log n)

3

O(4ⁿ)

4

O(n²)

Mark as read

Next: Level Order Sum

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

(3)

Comment
Anonymous
SW
• 8 months ago

Leetcode https://leetcode.com/problems/binary-tree-level-order-traversal/description/

5

Reply
M
ManagingBlueMockingbird521
Premium
• 10 months ago

This is great! You can also achieve level order using two queues current next and next level. Something like this

def run_level_order(root):
    if root is None:
        return

    queue_current = deque()
    queue_next = deque()
    queue_current.append(root)
    result = []
    current_level = []
    while queue_current:
        node = queue_current.popleft()
        current_level.append(node.value)
        print (node.value, end=", ")
        if node.left:
            queue_next.append(node.left)
        if node.right:
            queue_next.append(node.right)

        if not queue_current:
            queue_current = queue_next
            print ("\n")
            queue_next = deque()
            result.append(current_level)
            current_level = []

    print (result)
    print ("Done..")

Show More

1

Reply
Mickey Mouse
• 1 year ago

Awesome content!

1

Reply
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Processing Levels