# Fundamentals

> Source: https://www.hellointerview.com/learn/code/depth-first-search/fundamentals
> Scraped: 2026-03-30


Depth-First Search
Fundamentals
6:18
7 chapters • 2 interactive checkpoints
Depth-First Search (DFS) is an algorithm that is used to visit all nodes in a tree or graph-like data structure. We'll start by learning the order in which visits the nodes in a binary tree.
Binary Tree Properties
The top node of a binary tree is called the root. Each node in a binary tree can have at most two children, referred to as the left child and right child. A node that does not have any children is called a leaf node:
4
2
1
1
2
3
3
4
7
6
1
2
9
3
4
root
leaf nodes
left
right
Height of a Binary Tree
The height of a binary tree is the number of edges on the longest path between the root node and a leaf node. This is also known as the depth of the tree.
4
2
1
1
2
3
3
4
7
6
1
2
9
4
4
Balanced Binary Tree
A binary tree is balanced if the height of the left and right subtrees of every node differ by at most 1.
4
2
1
1
2
3
3
4
7
6
1
2
9
4
A balanced binary tree.
4
2
1
1
2
3
3
4
7
An unbalanced binary tree.
Complete Binary Tree
A binary tree is complete if every level, except possibly the last, is completely filled, and all nodes are as far left as possible. Complete binary trees are an important concept in heap data structures.
4
2
1
1
2
3
3
4
7
6
1
9
A complete binary tree.
A complete binary tree has a height of O(log(n)), where n is the number of nodes in the tree.
Binary Search Tree
A binary search tree (BST) is a binary tree where:
All nodes in the left subtree of the root have a value less than the root.
All nodes in the right subtree of the root have a value greater than the root.
The same property applies to all subtrees in the tree. This property allows for efficient search, insertion, and deletion of nodes in the tree.
4
2
1
3
7
6
9
A binary search tree. All nodes in the left subtree are less than 4, while all nodes in the right subtree are greater than 4.
Depth-First Search (DFS)
Depth-First Search is an algorithm used to traverse each node in a binary tree. It starts at the root node and tries to go "down" as far as possible until reaching a leaf node. When it reaches a leaf node, it "backtracks" to the parent node to explore the next path, which is animated below:
VISUALIZATION
Python
Language
Full Screen
def dfs(root):
    if root is None:
        return

    dfs(root.left)
    dfs(root.right)
    return
4
2
1
3
7

bare DFS traversal

0 / 32

1x
This "go deep as far as possible and then backtrack" behavior differentiates DFS from Breadth-First Search (BFS), which explores all the nodes at "level" before moving on to the next level.
Let's now look at the implementation of DFS on a binary tree. We'll pay special attention to the role that recursion and the call stack play in the algorithm.
Recursion And The Call Stack
Depth-First Search is typically implemented as a recursive function, or a function that calls itself within the body of the function.
SOLUTION
Python
Language
def dfs(node):
    # base case
    if not node:
        return

    dfs(node.left) # recursive call
    dfs(node.right) # recursive call
Working with any recursive function requires a good understanding of the call stack. The call stack is a stack-like data structure that keeps track of the function calls that are currently being executed.
Below, we'll visualize how the call stack grows and shrinks as we traverse a binary tree using DFS. In particular, we'll learn how the call stack allows DFS to backtrack.
Call Frame
The initial call to dfs is made on the root node of the binary tree. This creates a call frame (the left panel below), which contains the current line of code being executed and the variables that are local to the function call.
def dfs(node):
  if node is None:
    return

  dfs(node.left)
  dfs(node.right)
node: Node(4)
4
2
1
3
7
dfs
The current line of execution is highlighted in blue. The local variables are node: Node(4).
Pushing To The Call Stack
Since node is not None, the first step of our dfs function is to visit the left child of the root node by making a recursive call to dfs(node.left).
This pushes a new call frame onto the call stack, where node: Node(2). Execution begins at the first line of code in this new call frame.
VISUALIZATION
Python
Language
Full Screen
def dfs(node):
    if node is None:
        return

    dfs(node.left)
    dfs(node.right)
4
2
1
3
7

dfs

0 / 1

1x
Pushing a new call frame onto the call stack.
Base Case
As we make recursive calls to traverse down the tree, we keep pushing call frames onto the call stack until we reach our first base case, where node is None.
A base case is a condition that stops DFS from traversing down.
VISUALIZATION
Python
Language
Full Screen
def dfs(node):
    if node is None:
        return

    dfs(node.left)
    dfs(node.right)
node: Node(4)
def dfs(node):
    if node is None:
        return

    dfs(node.left)
    dfs(node.right)
node: Node(2)
4
2
1
3
7

0 / 2

1x
Traversing down until reaching a base case.
Backtracking
Here, we reach our first return statement. When the function returns, the call frame is popped off the call stack, and execution returns to the call frame that is now at the top of the call stack. This is backtracking!
After backtracking, we make a recursive call to dfs(node.right), which is another base case that returns immediately.
VISUALIZATION
Python
Language
Full Screen
def dfs(node):
    if node is None:
        return

    dfs(node.left)
    dfs(node.right)
node: Node(4)
def dfs(node):
    if node is None:
        return

    dfs(node.left)
    dfs(node.right)
node: Node(2)
def dfs(node):
    if node is None:
        return

    dfs(node.left)
    dfs(node.right)
node: Node(1)
def dfs(node):
    if node is None:
        return

    dfs(node.left)
    dfs(node.right)
node: None
4
2
1
3
7
None

0 / 3

1x
Backtracking to the parent node.
Backtracking (Continued)
At this point, we have finished visiting all the nodes in the left and right subtrees of the current node Node(1). The current call frame is popped off the call stack, and we backtrack to the parent node Node(2), which then makes a recursive call to dfs(node.right).
This process continues until we have visited all the nodes in the binary tree.
VISUALIZATION
Python
Language
Full Screen
def dfs(node):
    if node is None:
        return

    dfs(node.left)
    dfs(node.right)
node: Node(4)
def dfs(node):
    if node is None:
        return

    dfs(node.left)
    dfs(node.right)
node: Node(2)
def dfs(node):
    if node is None:
        return

    dfs(node.left)
    dfs(node.right)
node: Node(1)
4
2
1
3
7

0 / 15

1x
Traversing the entire binary tree.
Time and Space Complexity
If there a N nodes in a binary tree, then a depth-first search based solution will visit each node exactly once.
Time Complexity:
Find the work done per recursive call, and multiply it by N. All of the examples (aside from the merging lists example) perform a constant amount of work per recursive call, so the time complexity is O(N).
Space Complexity:
The memory that each recursive call occupies on the call stack is part of the space complexity of a problem. In depth-first search problems, a recursive call is made for each node in the tree, so the space complexity is at least O(N). This is in addition to the amount of space required for each recursive call itself, which differs from problem to problem.
Summary
Depth-First Search visits every node in a binary tree by going "down" as far as possible before backtracking to visit the nodes on the next path.
Depth-First Search is typically implemented as a recursive function. It visits new nodes in the tree by making recursive calls. When a recursive call is made, a new call frame is pushed onto the call stack.
Backtracking occurs whenever a recursive call returns. The call frame is popped off the call stack, and execution returns to the next call frame on the call stack.
Another key insight is that whenever a recursive function returns, we have finished visiting all nodes in the left and right subtrees of the current node. This leads us to Return Values, which is the first unit in solving binary tree problems with DFS.

Mark as read

Next: Return Values

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

(28)

Comment
Anonymous
​
Sort By
Popular
Sort By
C
caly.yang
Top 10%
• 1 year ago

Hi, I think the space complexity for DFS should be O(h), where h is the height of the tree, because it should count only the maximum space needed at a given point in time, versus the total space used.

25

Reply
MM
Minnie Mouse
Top 5%
• 6 months ago

This would be true for a balanced binary tree but consider an unbalanced binary tree which only has left nodes and visually looks like a linked list. In that case, the call stack would grow proportionally to n, the number of nodes. For a balanced binary tree, the call stack would grow proportionally to log_2(N), the height of the tree. So, in the worst case, DFS uses O(N) memory. The article should say "the space complexity is at [most] O(N)".

10

Reply
MM
Minnie Mouse
Top 5%
• 6 months ago

Upon reviewing my comment, you are right. When the tree is balanced, h = log_2(N), and when the tree is a linked list, h = N. So both O(h) and O(N) are correct. I think it just comes down to a preference of describing the complexity in terms of the size of the input rather than in terms of a property of the input.

5

Reply
Bhavik Shah
Premium
• 6 months ago

I agree, the space complexity is O(h) which is height of the tree. Every time we go up in tree, we pop from stack before moving on to another right subtree

1

Reply
Haris Osmanagić
Premium
• 3 months ago

I believe that's not true. Complexity refers to the total amount of a resource used (time or space, just checked Wikipedia). So, if we're visiting each node once, then the complexity is O(n).

It's similar to lists: if you need to go over each element in a list, then the complexity is O(n) t00.

0

Reply
M
MeltedAmberPiranha299
Top 10%
• 3 months ago

I think it is true, the space is occupied by the call stack. The call stack is only as tall as the height of the binary tree. For example, in a complete binary tree, you have way more nodes than you do in actual height, but the call stack will only have a maximum height of O(h). More specifically, think about what happens at the return statement during the base case.

0

Reply
C
ConvincingBronzePtarmigan296
• 1 year ago

Isn't the height of the binary tree 3 in the very first example?

12

Reply
I
InterestingAmethystFowl390
Premium
• 1 year ago

Great content!

Could you please correct the visualization for 'Height of a Binary Tree' section? Shouldn't the depth be 3 instead of 4 as there are only 3 edges from the root to leftmost leaf node.

7

Reply
dib
Premium
• 1 year ago

Thanks for creating such an awesome content!! Is it possible for you to add few problems on Binary Search?

4

Reply
Jimmy Zhang
Top 5%
• 1 year ago

Here it is! https://www.hellointerview.com/learn/code/binary-search/overview

3

Reply
M
muigaiunaka
Premium
• 8 months ago

there is a "π" next to "leaf node:π" above

3

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Binary Tree Properties

Depth-First Search (DFS)

Time and Space Complexity

Summary
