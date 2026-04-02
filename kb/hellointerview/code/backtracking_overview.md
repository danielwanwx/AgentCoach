# Backtracking Overview

> Source: https://www.hellointerview.com/learn/code/backtracking/overview
> Scraped: 2026-03-30

Backtracking Overview
5:37
8 chapters • 1 interactive checkpoints
Pre-Requisite: Depth-First Search
Backtracking algorithms use Depth-First Search to search all possible paths for a solution to a path. The animation below shows how a backtracking algorithm finds the word "HELLO" using cells that are adjacent to each other in a 2D-grid.
The algorithm starts with "H" and explores all possible word paths by adding adjacent cells to the current word. As soon as the current word doesn't match "HELLO", the algorithm backtracks to the previous cell and tries the next path.
VISUALIZATION
Full Screen
H
M
O
I
E
L
L
P
T
K
C
A

word search backtracking

0 / 11

2x
This example demonstrates key characteristics of backtracking algorithms:
It finds a solution for the problem by exploring all possible paths.
It "backtracks" to the previous path as soon as the current path doesn't lead to a solution.
Let's now look at an example of how to use Depth-First Search to solve backtracking problems.
Example: Path Sum
DESCRIPTION
Given a binary tree where all nodes have positive, integer values and a target sum, find all root-to-leaf paths where the sum of the values along the path equals the given sum.
Example:
Target: 7
4
7
1
3
2
6
1
Output:
[[4, 2, 1]]
4
7
1
3
2
6
1
This problem is a good backtracking candidate because it requires exploring all root-to-leaf paths to see if they sum to the given target.
The animation below visualizes the different paths the backtracking algorithm explores on the binary tree below with target = 11:
VISUALIZATION
Full Screen
4
2
1
2
5
8
4
3
2
3
2
8

path sum backtracking

0 / 13

1x
Pay attention to step 2 / 4, in which we stop exploring the path before reaching the leaf node because the sum of the path exceeds the target sum. This is known as "pruning".
Backtracking Solution
To implement this algorithm, we'll use depth-first search to explore all possible root-to-leaf paths.
We define a helper function backtrack that performs the depth-first search. backtrack takes the current node, the current path, and the current sum as arguments.
Each recursive call of backtrack explores the current node by adding the node's value to the path and incrementing the total sum.
If the current node is a leaf node, we check if the total sum equals the target sum. If it does, we add the path to the result list. We then backtrack to the previous node in the tree.
Otherwise, it makes recursive calls to explore the left and right children of the current node.
SOLUTION
Python
Language
def pathSum(root, target):
    def backtrack(node, path, total):
        if not node:
            return
        
        path.append(node.val)
        total += node.val

        # KEY STEP 2
        # current sum exceeds target
        # so pop to remove the current node from the path
        # return to backtrack to previous node on the call stack
        if total > target:
            path.pop()
            return
        
        if not node.left and not node.right:
            # add the path to the result
            # note we have to make a copy (path[:]) of the path
            # since future recursive calls modify path
            if total == target:
                result.append(path[:])
        else:
            backtrack(node.left, path, total)
            backtrack(node.right, path, total)

        # KEY STEP 1
        # we have finished exploring all paths containing the current node
        # so pop to remove the current node from the path
        # return to backtrack to previous node on the call stack.
        path.pop()

    result = [] 
    backtrack(root, [], 0)
    return result
Key Steps
The key to understanding backtracking algorithms is to understand what happens when a recursive call returns.
KEY STEP 1: Backtracking
The animation below shows how the algorithm "backtracks" after processing the first leaf node (Node 2 at the bottom left of the tree).
Step 1:
The function first adds the value of the leaf node to the path and increments the total of the path.
Step 2:
Since we're at a leaf node, the function checks if the current sum equals the target sum. It doesn't here, the function first pops the leaf node from the path list before the function call returns and backtracks to the previous node in the tree.
Step 3:
The next function on the call stack then resumes and explores its right child (Node 5).
VISUALIZATION
Python
Language
Full Screen
def pathSum(root, target):
    result = []
    backtrack(root, [], 0)
    return result
def backtrack(node, path, total):
    if not node:
        return
        
    path.append(node.val)
    total += node.val

    if total > target:
        path.pop()
        return

    if not node.left and not node.right:
        if total == target:
            result.append(path[:])
    else:
        backtrack(node.left, path, total)
        backtrack(node.right, path, total)
    path.pop()
total: 4
path: [4]
def backtrack(node, path, total):
    if not node:
        return
        
    path.append(node.val)
    total += node.val

    if total > target:
        path.pop()
        return

    if not node.left and not node.right:
        if total == target:
            result.append(path[:])
    else:
        backtrack(node.left, path, total)
        backtrack(node.right, path, total)
    path.pop()
total: 6
path: [4,2]
def backtrack(node, path, total):
    if not node:
        return
        
    path.append(node.val)
    total += node.val

    if total > target:
        path.pop()
        return

    if not node.left and not node.right:
        if total == target:
            result.append(path[:])
    else:
        backtrack(node.left, path, total)
        backtrack(node.right, path, total)
    path.pop()
total: 7
path: [4,2,1]
def backtrack(node, path, total):
    if not node:
        return
        
    path.append(node.val)
    total += node.val

    if total > target:
        path.pop()
        return

    if not node.left and not node.right:
        if total == target:
            result.append(path[:])
    else:
        backtrack(node.left, path, total)
        backtrack(node.right, path, total)
    path.pop()
total: 7
path: [4,2,1]
4
2
1
2
5
8
4
3
2
3
2
8
result
[]

recursive call

0 / 3

1x
Key Step 2: Pruning
The animation below shows how the algorithm "prunes" paths when the current sum exceeds the target sum at Node 8.
Step 1:
The function first adds the value of the current node to the path and increments the total of the path.
Step 2:
The function checks if the current sum exceeds the target sum. It does here, so the function immediately pops the current node from the path list before the function call returns and backtracks to the previous node in the tree.
Step 3:
The next function on the call stack then resumes (Node 2). Since all paths containing Node 2 have been explored, the function pops Node 2 from the path and backtracks to the previous node in the tree.
VISUALIZATION
Python
Language
Full Screen
def pathSum(root, target):
    result = []
    backtrack(root, [], 0)
    return result
def backtrack(node, path, total):
    if not node:
        return
        
    path.append(node.val)
    total += node.val

    if total > target:
        path.pop()
        return

    if not node.left and not node.right:
        if total == target:
            result.append(path[:])
    else:
        backtrack(node.left, path, total)
        backtrack(node.right, path, total)
    path.pop()
total: 4
path: [4]
def backtrack(node, path, total):
    if not node:
        return
        
    path.append(node.val)
    total += node.val

    if total > target:
        path.pop()
        return

    if not node.left and not node.right:
        if total == target:
            result.append(path[:])
    else:
        backtrack(node.left, path, total)
        backtrack(node.right, path, total)
    path.pop()
total: 6
path: [4,2]
def backtrack(node, path, total):
    if not node:
        return
        
    path.append(node.val)
    total += node.val

    if total > target:
        path.pop()
        return

    if not node.left and not node.right:
        if total == target:
            result.append(path[:])
    else:
        backtrack(node.left, path, total)
        backtrack(node.right, path, total)
    path.pop()
total: 6
path: [4,2]
4
2
1
2
5
8
4
3
2
3
2
8
result
[]

recursive call

0 / 3

1x
Key Takeaways
Returning from a function corresponds to backtracking to the previous node in the tree.
Since we use a single list to store the current path across all recursive calls, before returning, we have to pop the current node from that path to backtrack.
Time And Space Complexity
Time Complexity: O(n2), where n is the number of nodes in the binary tree. The backtrack function is called once for each node in the tree. Each call takes O(n) time in the worst case to copy the path to the result list, resulting in a total time complexity of O(n2).
Space Complexity: O(n2), where n is the number of nodes in the binary tree. This is dominated by the size of the result list, which can contain up to O(n) paths, each of which can contain up to O(n) nodes.
Summary
The above algorithm is a good example of a backtracking algorithm because:
It explores all possible root-to-leaf paths in the binary tree to find the paths that sum to the target sum.
Whenever we reach a leaf node, we backtrack to the previous node in the tree to explore the next path.
It "prunes" paths by returning immediately when the sum exceeds the target sum.

Mark as read

Next: Word Search

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

(23)

Comment
Anonymous
​
Sort By
Popular
Sort By
Chenshu Zhou
• 1 year ago

The path has length log(n), so the time complexity is O(nlogn) to be precise.

15

Reply
J
JudicialTomatoCaribou448
Premium
• 3 months ago

The path is only O(logN) for a balanced tree. For a degenerate tree, it is O(N). The math does still point to O(NlogN) though:

For a complete, balanced tree, there are roughly N/2 leaves => O(N) . Each path will be roughly O(logN) length, so it will take O(NlogN) time for to copy all O(logN) length paths at the O(N) leaf nodes.

For a degenerate tree, there is one leaf => O(1). The single path is of length O(N). So total time is O(N).

This, in the worst case, time complexity is O(NlogN)

4

Reply
Michael Sanchez
• 11 months ago

I would agree. And it's not a matter of exact precision - the difference between O(n log n) and O(n2) is huge.

4

Reply
revanth Reddy katanguri
Premium
• 8 months ago

Solution assumes that there are only Positive integers. Pruning logic fails if negative numbers are present in the tree.

9

Reply
Daniel Mai
Premium
• 1 month ago

exactly, great catch!

0

Reply
Wil
• 1 year ago

The interactive illustrations here are so helpful and really have made this so much easier to understand for me. Thank you!

9

Reply
Atif Mansoor
Premium
• 6 months ago

If you want to add this problem to your LeetCode total, it's 113. Path Sum II.
The 112. Path Sum problem is a simpler DFS variation without the state tracking.

4

Reply
R
RetiredHarlequinHarrier460
Premium
• 9 months ago

Doesn't the space for the result not count towards the space complexity? In that case there would be O(n) space complexity, since that is the size of the call stack in the worse case of an unbalanced tree where the height is equal to the number of nodes (ie linked list), and O(n) is also max size of the list of path nodes.

3

Reply
H
HomelyPurpleParakeet420
Premium
• 2 months ago

Space complexity is O(nb) because at worst case we have every node on the call stack and each node had stored its path O(n) resulting in O(nn) space complexity.

0

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Example: Path Sum

Backtracking Solution

Key Steps

Summary