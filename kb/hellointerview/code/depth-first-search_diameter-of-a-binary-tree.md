# Diameter of a Binary Tree

> Source: https://www.hellointerview.com/learn/code/depth-first-search/diameter-of-a-binary-tree
> Scraped: 2026-03-30



Depth-First Search
Diameter of a Binary Tree
easy
DESCRIPTION (inspired by Leetcode.com)

Given the root of a binary tree, write a recursive function to find the diameter of the tree. The diameter of a binary tree is the length of the longest path (# of edges) between any two nodes in a tree. This path may or may not pass through the root.

Example 1:

3
9
1
5
4
2

Input:

[3, 9, 2, 1, 4, null, null, null, 5]

Output: 4 (The longest path is 5 -> 1 -> 9 -> 3 -> 2) for a total of 4 edges

Example 2:

3
9
1
2
4
3

Input:

[3, 9, null, 1, 4, null, null, 2, null, 3]


Output: 4 (The longest path is 2 -> 1 -> 9 -> 4 -> 3) for a total of 4 edges

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
    def maxDiameter(self, root: TreeNode) -> int:
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
The diameter of a binary tree is equal to longest path between any two nodes in the tree. So we want to use depth-first search to visit each node, and at each node we'll calculate the length of the longest path that passes through that node. At the end, we'll return the maximum of those lengths.
Now, let's breakdown how to calculate the longest path that passes through a node in the tree. As shown in the diagram below, the longest path that passes through a node is equal to the maximum depth of the nodes' left subtree + the maximum depth of the nodes' right subtree, where the depth of a subtree is the number of nodes on the longest path from the root of that subtree to a leaf node.
3
9
1
5
4
2
The length of the longest path going through the root node in the tree above is 4.
3
9
1
5
4
2
Which is equal to the maximum depth of the left subtree (3) + the maximum depth of the right subtree (1).
So at each node, we want to find the max depth of our left and right subtrees, and use that to calculate the length of the longest path that passes through that node. With that in mind, we can solve this problem using the framework described in the Overview section:
Return Values
If I'm at a node in the tree, what values do I need from my left and right children to calculate the diameter of the subtree rooted at the current node?
As we broke down above, to calculate the diameter, we need:
The max depth of the left subtree.
The max depth of the right subtree.
This tells us that each recursive call should return the max depth of the subtree rooted at the current node. So in the body of the recursive function, I'll make recursive calls to the current node's left and right children, and then return the max depth of the current subtree as 1 + max(left, right) to the parent.
Before returning, I should add those values together to get the diameter of the tree rooted at the current node. I can then compare that value to a global variable max_, and update max_ if necessary.
(See the Global Variables section below for more details on why this is necessary).
SOLUTION
Python
Language
# get the max depth of the left and right subtrees
left = dfs(node.left)
right = dfs(node.right)

# update the maximum diameter of the tree
max_ = max(max_, left + right)

# return the max depth of the current subtree
return 1 + max(left, right)
Base Case
The max depth of an empty tree is 0.
Global Variables
Each recursive call returns the max depth of the subtree rooted at the current node, but the question is asking for the diameter of the tree. Since these two values are different, we can use a global variable max_ to store the maximum diameter of the tree, and update it as necessary in each recursive call.
Using a global variable allows us to avoid using multiple return values in our recursive function, or having to pass the maximum diameter value as a parameter from the parent to the child.
Helper Function
We don't need to pass values from the parent to the child to solve this problem. However, since we are using a global variable to store the maximum diameter of the tree, we should define max_ inside the body of our main function, and then introduce a helper function to perform the recursive calls. This keeps the max_ variable protected, as no code outside of the main function can access it.
Inside the main function, we can initiate the call to the helper function, passing in the root of the tree as an argument. We return the value of max_ after the recursive helper function has finished executing.
Solution
SOLUTION
Python
Language
class Solution:
    def diameterOfBinaryTree(self, root):
        max_ = 0
        def dfs(node):
            nonlocal max_
            # base case
            if not node:
                return 0

            # get the max depth of the left and right subtrees
            left = dfs(node.left)
            right = dfs(node.right)
            
            # update the maximum diameter of the tree
            max_ = max(max_, left + right)
            
            # return the max depth of the current subtree
            return 1 + max(left, right)
        
        dfs(root)
        return max_
Animated Solution
nums
​
|
nums
list of integers
Try these examples:
Single
Skewed
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def diameterOfBinaryTree(root):
    max_ = 0
    def dfs(node):
        nonlocal max_
        if not node:
            return 0

        left = dfs(node.left)
        right = dfs(node.right)
        max_ = max(max_, left + right)
        return max(left, right) + 1

    dfs(root)
    return max_
3
9
1
5
4
2

diameter of binary tree

0 / 34

1x
What is the time complexity of this solution?
1

O(n log n)

2

O(log m * n)

3

O(n)

4

O(V + E)

Mark as read

Next: Path Sum II

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

(14)

Comment
Anonymous
​
Sort By
Popular
Sort By
Abhay Singh
Top 1%
• 1 year ago

Java Solution:

class Solution {
    
    class Node {
        int NTL; // node to leaf path (Height)
        int LTL; // leaf to leaf path (Diameter)
        
        Node(int ntl, int ltl) {
            this.NTL = ntl;
            this.LTL = ltl;
        }
    }
    
    public Node solve(TreeNode root) {
        if (root == null) return new Node(-1, -1);
        
        Node leftNode = solve(root.left);
        Node rightNode = solve(root.right);
        
        int curNTL = Math.max(leftNode.NTL, rightNode.NTL) + 1;
        int curLTL = Math.max(leftNode.NTL + rightNode.NTL + 2, Math.max(leftNode.LTL, rightNode.LTL));
        
        return new Node(curNTL, curLTL);
    }
    
    public int diameterOfBinaryTree(TreeNode root) {
        return solve(root).LTL;
    }
}
Show More

4

Reply
I
InterestingCoffeeCapybara976
• 1 year ago

Can you please explain the difference between Max Depth and Max Height of a Binary Tree?

From my understanding :
-> Max height would be the total number of edges between root and ending node of the longest path

-> Max Depth would be the total number of nodes from root to ending node of the longest path

Do correct me if I as wrong.

1

Reply
Feng Xia
Premium
• 2 months ago
• edited 2 months ago

The depth of a node is the number of edges from the node to the tree's root node.
A root node will have a depth of 0.

The height of a node is the number of edges on the longest path from the node to a leaf.
A leaf node will have a height of 0.

source: https://stackoverflow.com/questions/2603692/what-is-the-difference-between-depth-and-height-in-a-tree

1

Reply
L
LexicalBronzeWolverine167
Premium
• 2 months ago
def maxDiameter(self, root: TreeNode):
        def traverse(root):
            if not root:
                return 0
            
            left = traverse(root.left)
            right = traverse(root.right)

            self.max_diameter = max(self.max_diameter, left + right)

            return max(left, right) + 1
        
        self.max_diameter = 0
        traverse(root)

        return self.max_diameter

0

Reply
Satya Dasara
Premium
• 2 months ago
• edited 2 months ago

Here the trick is for current node we add left + right + 1 (to include current node)
To pass up in recursion call we return max(left, right)

Also we get total number of nodes for largest diameter
Number of edges will be number of nodes - 1

class Solution:
    def maxDiameter(self, root: TreeNode):
        # Your code goes here
        ans = 0

        def dfs(node):
            if not node:
                return 0
            

            left = dfs(node.left)
            right = dfs(node.right)
            curr_length = 1 + left + right
            nonlocal ans
            ans = max(ans, curr_length)

            return 1 + max(left, right)
        
        dfs(root)

        return ans - 1 if ans else 0
Show More

0

Reply
Stanley Lin
• 1 month ago

why did you have to add 1 to current length when you would have to delete it at the end?

2

Reply
kolade afeez
Premium
• 5 months ago
public class Solution {
        int longestRoot = 0;
        int longestSide = 0;
          int diameter = 0;
    public int DiameterOfBinaryTree(TreeNode root) {
        // approach-- get count of both side of a parent
        //     --- get value of sum of both branch
        // move up-- sum of the max side count + other side max branch
        // and repeat..

        DFS(root);
        
        // var result = Math.Max(longestRoot, longestSide) - 1;
        // if(result < 0)
        //     return 0;
        // else 
        //     return result;

        return diameter;

    }

    public int DFS(TreeNode root)
    {
        if(root == null)
            return 0;

        // if(root.left == null && root.right == null)
        // {
        //     return 1;
        // }

        var left = DFS(root.left);
        var right = DFS(root.right);

        // longestRoot = Math.Max(longestRoot, (left + right + 1));
        // longestSide = Math.Max(Math.Max(left, right), longestSide);

        diameter = Math.Max(diameter, left + right);

        // Return height of current subtree
        return Math.Max(left, right) + 1;
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

Solution

Animated Solution

