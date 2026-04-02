# Return Values

> Source: https://www.hellointerview.com/learn/code/depth-first-search/return-values
> Scraped: 2026-03-30


Depth-First Search
Return Values
In the previous section, we learned how Depth-First Search traverses each node in a binary tree via a series of recursive calls. To solve binary tree interview problems, the next step is to have each recursive call to DFS return a value.
In this unit, we will:
Walkthrough an example to demonstrate how recursion and return values are used to solve binary tree problems with Depth-First Search.
Cover a general approach we can use to determine return values when faced with a binary tree problem.
Practice!
Recursion
This template is a starting point for solving binary tree problems with Depth-First Search, which takes the base implementation of DFS from the previous section and adds return values to each recursive call.
SOLUTION
Python
Language
def dfs(node):
    # base case
    if node is None:
        return some value
    
    ...
    
    left = dfs(node.left)
    right = dfs(node.right)
    return value based on left and right
To solve binary tree problems with DFS, we have to get used to solving problems recursively, which we do in the problem below:
Problem: Sum of Nodes
DESCRIPTION
Given a binary tree, use Depth-First Search to find the sum of all nodes in the tree.
Input

4
2
1
3
7
6
9
Output
4 + 2 + 1 + 3 + 7 + 6 + 9 = 32
Thinking Recursively
To solve this problem, let's start with an observation:
In the binary tree below, the sum of all nodes equals the value of the root node (4) + the sum of all nodes in the left subtree (6) + the sum of all nodes in the right subtree (22).
6
22
4
2
1
3
7
6
9
The sum of all the nodes in the binary tree is 4 + 6 + 22 = 32.
Note this applies to every subtree in the tree. The sum of the subtree rooted at Node(2) is equal to 2 + the sum of its left subtree (1) + the sum of its right subtree (3).
6
3
1
4
2
1
3
7
6
9
The sum of the right subtree 2 + 1 + 3 = 6. Recursion!
The subtrees rooted at the leaf nodes are equal to the value of the leaf nodes, since their left and right subtrees are empty.
In other words, if we know the sum of our left and right subtrees, then we know the sum of our subtree.
sum(node) = sum(node.left) + sum(node.right) + node.val
What we've done is expressed the solution to the problem recursively: in terms of smaller subproblems to the same problem (the sum of a tree in terms of its left and right subtrees).
So how can we leverage this observation to solve the problem? By using Depth-First Search!
Depth-First Search Approach
Let's recall a key point about Depth-First Search: when a recursive call to dfs on a subtree returns, execution returns to the parent of that subtree.
If each recursive call to dfs returns with the sum of its subtree, then the parent node will receive that value as the sum of either its left or right subtree. It can then use that value as part of its own subtree sum based on the recursive equation from above.
Here's how to visualize the steps of the Depth-First Search solution to this problem:
It starts by making recursive calls down the left subtree until reaching the first leaf node, Node(1):
VISUALIZATION
Full Screen
4
2
1
3
5
2

sum of nodes in binary tree

0 / 2

1x
Node(1) returns the sum of its subtree to its parent Node(2), which receives this value as the sum of its left subtree. 1/2
Node(2) then makes a recursive call to its right subtree, Node(3). 2/2
VISUALIZATION
Full Screen
4
2
1
3
5
2

0 / 2

1x
Node(3) returns the sum of its subtree to its parent, which receives this value as the sum of its right subtree. 1/9
Now, the parent node Node(2) can calculate the sum of its subtree, and return that value to its parent, Node(4). 2/9
This process continues until the root node receives the sum of both its left and right subtrees, and can calculate the sum of the entire tree. 3/9 to 9/9
VISUALIZATION
Full Screen
4
2
1
3
5
2

0 / 9

1x
Note how the answer "bubbles up" from the leaf nodes up to the parent nodes until we reach the root node, which is true of all binary tree problems that are solved with Depth-First Search.
Implementation
Now that we know that each recursive call should return the sum of its subtree, we can implement our solution:
The base cases are the subproblems we can solve directly (without making any recursive calls):
An empty subtree has a sum of 0.
The subtree rooted at a leaf node has a sum equal to the value of the leaf node.
Otherwise, we make recursive calls to get the sum of our left and right subtrees. We then return the sum of the left subtree, right subtree, and the current node's value.
SOLUTION
Python
Language
def dfs(node):
    # base case: empty subtree
    if node is None:
        return 0
    
    # base case: leaf node
    if node.left is None and node.right is None:
        return node.val
    
    left = dfs(node.left)
    right = dfs(node.right)
    return left + right + node.val
Solving Problems with Recursion
When solving a binary tree problem with recursion, the first step is to figure out the return value of each recursive call. In the problem above, each recursive call returned the sum of the subtree rooted at the current node.
To determine what the return value should be for a different problem, imagine you're at a node in the tree and ask yourself: "What information do I need from my left and right subtrees to solve the problem for my subtree?"
Problem
Find the maximum value in a binary tree
Explanation
If I'm at a node in the tree, what values do I need from my left and right subtrees to find the maximum value for my subtree?
I need to know the maximum value in my left subtree, and the maximum value in my right subtree. The maximum value in my subtree is the maximum of those two values and the value of my node.
3
9
4
2
1
3
7
9
The maximum value in the tree above is equal to max(3, 4, 9) = 9
This tells me that each recursive call should return the maximum value in the subtree rooted at the current node.
In code, I'll get the max values of my left and right subtrees via recursive calls, and the return statement of each recursive function becomes:
SOLUTION
Python
Language
def maxValue(node):
    ... 

    left = maxValue(node.left)
    right = maxValue(node.right)
    return max(left, right, node.val)
Finally, we need to add our base case, which are the subproblems we can solve directly:
An empty subtree has a maximum value of negative infinity.
The subtree rooted at a leaf node has a maximum value equal to the value of the leaf node.
SOLUTION
Python
Language
def maxValue(node):
    if node is None:
        return float('-inf')
    
    if node.left is None and node.right is None:
        return node.val

    left = maxValue(node.left)
    right = maxValue(node.right)
    return max(left, right, node.val)
Common Mistakes
Returns Value
Not being able to clearly define what each recursive call returns in terms of the node it is called on. This leads to incorrect return values, particulary in the base cases.
Base Cases
Make sure that the return value of the base case and the return value of the recursive case are of the same type. A common mistake is to return None for the base case and an integer in the recursive case.

Mark as read

Next: Maximum Depth of Binary Tree

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

(13)

Comment
Anonymous
​
Sort By
Popular
Sort By
P
PrincipalCoralOctopus997
Top 5%
• 1 year ago

whats the point of

if node.left is None and node.right is None:
    return node.val

because

if node is None:
    return float('-inf')

is all you need cus it handles cases of empty subtree AND where subtree rooted at leaf node so its simpler to just do

def maxValue(node):
    if node is None:
        return float('-inf')

    left = maxValue(node.left)
    right = maxValue(node.right)
    return max(left, right, node.val)
Show More

23

Reply
Jimmy Zhang
Top 5%
• 1 year ago

yeah you're right! its not necessary, but you can think of it is a minor optimization since it saves a few recursive calls

19

Reply
Gen Lauer
Premium
• 10 months ago

Thanks for confirming it.

1

Reply
Divya Saini
Premium
• 25 days ago

I was wondering the same, thanks!

0

Reply
Gen Lauer
Premium
• 10 months ago

It seems to me in the code below, we do not need the base code for leaf node. " If node is None: return 0" will take care of it automatically, is that correct?

def dfs(node):
    # base case: empty subtree
    if node is None:
        return 0
    
    # base case: leaf node
    if node.left is None and node.right is None:
        return node.val
    
    left = dfs(node.left)
    right = dfs(node.right)
    return left + right + node.val

3

Reply
P
PeacefulApricotWallaby562
Premium
• 9 months ago

'return 0' is applicable when we know the input contains only +ve integers. Negative infinity takes care of the +ve and -ve integers.

2

Reply
0
0106kwh
• 9 months ago

When the tree is empty, this special case will give 0 directly

0

Reply
0
0106kwh
• 9 months ago

Hi dude, i guess we are on the same path, wanna learn it together?

0

Reply
Yves Sy
Premium
• 6 months ago

Typo on the caption of one of the diagrams "The sum of the right subtree 2 + 1 + 3 = 6. Recursion!" -> should be left subtree

1

Reply
nailyk
Premium
• 2 months ago
• edited 2 months ago

note: the "On This Page" section is broken for this page, it refers to the "Introduction" page (edit: same issue for other pages under the Depth-First Search section)

0

Reply
Haris Osmanagić
Premium
• 3 months ago

DFS is slightly more understandable to me if I do this:

void dfs(TreeNode node) {
    if (node.isLeafNode()) {
        return;
    }

   if (node.left != null) {
            dfs(node.left);
        }

    if (node.right != null) {
        dfs(node.right);
    }
}

It checks if a node has a child node, and only if it does, it calls dfs on it.

This code runs only on actual nodes, and I don't need to think about what should be the return values for non-existing nodes.

0

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Recursion

Problem: Sum of Nodes

Depth-First Search Approach

Implementation

Solving Problems with Recursion

Common Mistakes
