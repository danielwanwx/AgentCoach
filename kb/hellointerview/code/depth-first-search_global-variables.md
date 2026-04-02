# Passing Values Down and Helper Functions

> Source: https://www.hellointerview.com/learn/code/depth-first-search/global-variables
> Scraped: 2026-03-30



Depth-First Search
Passing Values Down and Helper Functions
In the Return Values section, we covered how return values allow us to solve binary tree problems from the "bottom-up".
In some cases, questions require us to pass information "down" from parents to child nodes, which we do via the parameters of our recursive function. If we need more parameters than the original function signature allows, then we need to introduce a helper function to help us recurse.
Let's look at an example of a question that requires a helper function.
DESCRIPTION (inspired by Leetcode.com)
Given the root node of a binary tree, write a function to find the number of "good nodes" in the tree. A node X in the tree is considered "good" if in the path from the root to the node X, there are no nodes with a value greater than X's value.
Example
Input:

4
2
1
3
7
6
9
Output:
3 # The good nodes are highlighted in green (4, 7, 9)
Node	Path	Is Good Node?	Explanation
4	[4]	Yes	The root node is a "good node" since there are no nodes with a value greater than 4 in the path from the root to the node.
2	[4, 2]	No	4 is greater than 2.
1	[4, 2, 1]	No	Both 4 and 2 are greater than 1.
3	[4, 2, 3]	No	4 is greater than 3.
7	[4, 7]	Yes	There are no nodes with a value greater than 7, so it is a "good node".
6	[4, 7, 6]	No	7 is greater than 6.
9	[4, 7, 9]	Yes	There are no nodes with a value greater than 9, so it is a "good node".
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
# class TreeNode:
#     def __init__(self, val: int, left: 'TreeNode' = None, right: 
'TreeNode' = None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def goodNodes(self, root: TreeNode) -> int:
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

Define the Return Value
If I'm at a node in the tree, what values do I need from my left and right children to calculate the number of good nodes in the subtree rooted at the current node?
I need to know the number of good nodes in my left subtree and the number of good nodes in my right subtree, which tells me that each recursive call should return the number of good nodes in the subtree rooted at the current node.
If I know those two values, then I can return the number of good nodes in my subtree by adding them together, and then adding 1 if the current node is a good node. We'll figure out how to tell if the current node is a good node next, but first let's figure out the base case.
Base Case
The number of good nodes in an empty tree is 0.
Extra Step: Determining if a Node is "Good"
In order to tell if a root node is "good", we need to know the maximum value of any node on the path starting from the original root of the tree to the current node. Since this is a value that must be passed down from parent nodes to children, we need to introduce a helper function that introduces an extra parameter max_, which represents the maximum value seen so far on the current path from the root.
To check if the current node is a good node, we compare the current node's value to max_. If the current node's value is greater than or equal to max_, then the current node is a good node, and we increment our count by 1.
Here's what the helper function looks like:
SOLUTION
Python
Language
def dfs(root, max_):
    # base case
    if root is None:
        return 0

    count = 0
    if root.val >= max_:
        # good node found, update count and max_
        count += 1
        max_ = root.val

    # recurse and pass down updated max_
    # to the left and right children
    left = dfs(root.left, max_)
    right = dfs(root.right, max_)           

    # return the number of good nodes in the
    # subtree rooted at the current node
    return count + left + right
In our main function, we can make the initial call to our helper function with max_ set to -infinity to kick off the recursion.
The animation below visualizes each step of the solution. Pay attention to how the max value seen so far on the current path from the root is passed down from parent to child nodes via the parameter in the helper function.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def goodNodes(root):
  def dfs(root, max_):
    if root is None:
        return 0
    
    count = 0
    if root.val >= max_:
      count += 1
      max_ = root.val
    
    left = dfs(root.left, max_)
    right = dfs(root.right, max_)
    return left + right + count

  return dfs(root, -float("inf"))
4
2
1
3
7
6
9

visible nodes in binary tree

0 / 37

1x
In this implementation, notice that the helper function dfs is defined within the body of the main goodNodes function. While not strictly necessary, we recommend this approach as it allows for a cleaner way to use global variables, which we cover below.
Questions involving root-to-leaf paths are common examples of where using helper functions are necessary, as we can use the helper function to introduce extra parameters that store the state of our current path.
Summary
Some questions require that nodes have values that are passed down to them via their parents. These values are passed via the parameters of the recursive function. If we need more values than the original function signature allows, then we need to introduce a helper function to help us recurse.
Global Variables
In some cases, using a global variable that all recursive calls access can simplify the code. Recalling the Good Nodes question from the previous section, Let's say that instead of returning only returning the count of all good nodes, we want to return a list of all good nodes in the tree.
To do so, we can initialize a single list that all recursive calls have access to, and append the current node to that list if it's visible:
SOLUTION
Python
Language

def goodNodes(root):
    nodes = []
    def dfs(root, max_):
        nonlocal nodes
        if root is None:
            return
        
        if root.val >= max_:
            max_ = root.val
            nodes.append(root)
        
        dfs(root.left, max_)
        dfs(root.right, max_)           

    dfs(root, -float('inf'))
    return nodes 
    
Note that there are no return values in the recursive function. We use depth-first search to traverse each node in the tree, and at each node, we check if the node is visible. If it is, we append it to the global list of visible nodes.
Since the "global variable" nodes is declared within the body of the main goodNodes function, it's not truly global - only the recursive dfs function has access to it. This is preferred, as it protects the variable from being accidentally modified by code outside of the goodNodes function.
Although something like that most likely won't happen in the context of an interview, it's a good bit of knowledge that you can mention during your interview to demonstrate your understanding of scope.
Alternative Approach 1
Compare that approach to the following, where each recursive call returns a list of visible nodes in its subtree, and the parent node combines them to return the final list of visible nodes:
SOLUTION
Python
Language
def goodNodes(root):
    def dfs(root, max_):
        if root is None:
            return []
        
        result = []
        if root.val >= max_:
            max_ = root.val
            result.append(root)
        
        left = dfs(root.left, max_)
        right = dfs(root.right, max_)           
        return result + left + right

    return dfs(root, -float('inf'))
While this approach avoids a global variable, it has a one major drawback: it requires us to merge lists returned by each subtree at each node into a new list in every call, which adds both time and space complexity. In the worst case, when every node in the tree is visible, we end up copying up to N nodes at each of the N nodes in the tree, resulting in a time complexity of O(n2).
Alternative Approach 2
Another alternative approach is to pass a single list of visible nodes as an extra parameter to the recursive function and update it as we recurse. While this is more time and space efficient than merging lists, it is cumbersome and error-prone, as we need to both pass the list down to each recursive call, and correctly return it to the parent node.
SOLUTION
Python
Language
def goodNodes(root):
    def dfs(root, max_, nodes):
        if root is None:
            return nodes
        
        if root.val >= max_:
            max_ = root.val
            nodes.append(root)
        
        left = dfs(root.left, max_, nodes)
        # need to pass the result from the
        # left to the right subtree
        right = dfs(root.right, max_, left)
        return right
    return dfs(root, -float('inf'), [])
For these reasons, global variables are preferred whenever we need to collect values in a list as we traverse the binary tree. Global variables are also useful when the return values of each recursive function differs from what the question is asking. We'll cover a few such examples in the practice problems.
What is the time complexity of this solution?
1

O(m * n)

2

O(n)

3

O(n * logn)

4

O(n!)

Mark as read

Next: Validate Binary Search Tree

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

(21)

Comment
Anonymous
​
Sort By
Popular
Sort By
Kamrun Nahar Liza
• 1 year ago

'In depth-first search problems, a recursive call is made for each node in the tree, so the space complexity is at least O(N)' - I think the space complexity is O(h), which in the worst case can be O(n) if the binary tree is skewed and O(logn) for a balanced binary tree, because in a given moment, the call stack will hold call frames equal to the height of the tree. Please correct me if I got this wrong or confirm if my thoughts are right. AND, TYSM again because I started with DFS in this course and finally recursion clicked!!! I struggled to come up with recursive solutions or my head would hurt lol but these lessons are so well written!

9

Reply
Jimmy Zhang
Top 5%
• 1 year ago

Yeah you understand it correctly!

The space taken up by the call stack is O(h) where h is the height of the tree. In the worst case (for a skewed tree like you said), h = N, so worst case is O(N).

I say "at least" because the body of each recursive function call might be allocating more memory as well, which we have to take into account.

Really happy to hear this material helped you understand recursion :)

0

Reply
Bhavik Shah
Premium
• 6 months ago

I say "at least" because the body of each recursive function call might be allocating more memory as well, which we have to take into account.

Actually we don't have to take this into account in big O calculation. big O calculation should involve only those variables which increases with the increase of input. In this situation the input is number of nodes in tree N, all the other memory allocation are constants (i.e. they do not increase with increase with increase in number of nodes in tree). So if you have a 100 arguments to function the space complexity is O(height of tree * 100) = O(height of tree)

This is my understanding of big O

1

Reply
Alessandro Laurato
• 2 months ago
• edited 2 months ago
 return dfs(root, -float("inf"))

I think

 return dfs(root, root.val)

is more intuitive also for other programming language and correct

3

Reply
Youssef Biaz
Premium
• 3 days ago

[5,3,8,1,4,7,9] is a broken test case in this. On LeetCode, the expected return value for this test case is 3 (which is the correct answer--the only good nodes are 5, 8, and 9). But on here, for some reason the expected return value is 4, which causes a failure even on the suggested solution.

1

Reply
Y
yogeetha.sundaram
Premium
• 8 months ago

https://www.hellointerview.com/learn/code/depth-first-search/global-variables - This page is also empty
Both Return Values and Global variables are important foundational pieces that could be super helpful when these broken links/ pages are fixed

1

Reply
Y
yogeetha.sundaram
Premium
• 8 months ago

This seems to be fixed now. Thanks

1

Reply
I
InnovativeCyanAntelope719
Top 5%
• 11 months ago

In general, global variables are frowned upon.

def goodNodes(root: TreeNode) -> list[TreeNode]:
    nodes = []

    def dfs(node: TreeNode, path_max: float, nodes_list: list[TreeNode]):
        if node is None:
            return

        new_max_for_children = path_max
        if node.val >= path_max:
            nodes_list.append(node)
            new_max_for_children = node.val

        dfs(node.left, new_max_for_children, nodes_list)
        dfs(node.right, new_max_for_children, nodes_list)

    if root:
        dfs(root, -float('inf'), nodes)

    return nodes
Show More

1

Reply
S
SubjectiveIndigoSkink289
• 4 months ago

I like this much better. I also prefer your naming convention for the node parameter to dfs() since it clearly indicates that you're traversing a node, not the root.

0

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Global Variables

