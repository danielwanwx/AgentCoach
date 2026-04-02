# Calculate Tilt

> Source: https://www.hellointerview.com/learn/code/depth-first-search/calculate-tilt
> Scraped: 2026-03-30



Depth-First Search
Calculate Tilt
easy
DESCRIPTION (inspired by Leetcode.com)

Given the root node of a binary tree, write a recursive function to return the sum of all node tilts in the tree.

The tilt of a node is calculated as the absolute difference between the sum of all values in its left subtree and the sum of all values in its right subtree. For nodes that are missing a left child, right child, or both, treat the missing subtree as having a sum of 0.

For example, a leaf node has a tilt of 0 because both its left and right subtrees are empty (sum = 0), so the absolute difference is |0 - 0| = 0.

Example 1:

5
1
3

Input:

[5, 1, 3]

Output:

2

The leaf nodes 1, 3 have tilts of 0 (their left and right subtrees are empty)

The root node 5 has a tilt of |1 - 3| = 2

Example 2:

4
2
1
3
7
6
9

Input:

[4, 2, 7, 1, 3, 6, 9]

Output:

21

The leaf nodes 1, 3, 6, 9 have tilts of 0 (their left and right subtrees are empty)

Node 2 has a tilt of |1 - 3| = 2 Node 7 has a tilt of |6 - 9| = 3 Node 4 has a tilt of |6 - 22] = 16

2 + 3 + 16 = 21

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
    def calculateTilt(self, root: TreeNode) -> int:
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
We can solve this problem using the framework established in the Overview section.
Return Values
If I'm at a node in the tree, what values do I need to calculate the tilt of the subtree rooted at that node?
The sum of the values in the left subtree.
The sum of the values in the right subtree.
This tells me that each recursive call should return the sum of the values in the subtree rooted at the current node. So in the body of the recursive function, I'll make recursive calls to the current node's left and right children, and then add the value of the current node to return the sum of the current subtree.
Before returning the sum of the current subtree, I'll also need to calculate the tilt of the current subtree. I can calculate the tilt of the current subtree as abs(left - right), and add that a global variable tilt that stores the total tilt of the tree. (see the Global Variables section for more details on why this is necessary).
SOLUTION
Python
Language

# get the sum of current node's left and right subtrees
left = dfs(node.left)
right = dfs(node.right)

# calculate tilt of current subtree and add it to the global tilt variable
tilt += abs(left - right)

# return the sum of the current subtree
return left + right + node.val
Base Case
The tilt of an empty tree is 0.
Global Variables
Note that the problem is asking for the total tilt of the tree, but each recursive call returns the sum of the nodes in the subtree rooted at a given node. Since these two values are different, we can use a global variable tilt to store the total tilt of the tree. This allows us to avoid using multiple return values in our recursive function, or having to pass the total tilt value from the parent to the child.
Helper Function
We don't need to pass values from the parent to the child to solve this problem. However, since we are using a global variable to store the total tilt of the tree, we should define tilt inside the body of our main function, and then introduce a helper function to perform the recursive calls. This way, no code outside of the main function will have access to the tilt variable.
Inside the main function, we can initiate the call to the helper function, passing in the root of the tree as an argument. We return the value of tilt after the recursive helper function has finished executing.
Solution
SOLUTION
Python
Language
class Solution:
    def findTilt(self, root: TreeNode) -> int:
        tilt = 0

       # define a helper function to perform the recursive calls 
       # this ensures that the tilt variable is not accessible outside of the main function
        def dfs(node):
            nonlocal tilt
            # base case
            if not node:
                return 0

            # get the sum of the current node's left and right subtrees
            left = dfs(node.left)
            right = dfs(node.right)

            # calculate tilt of current subtree, and add it to the global tilt variable
            tilt += abs(left - right)

            # return the sum of the current subtree
            return left + right + node.val

       # initiate the call to the helper function 
        dfs(root)
        return tilt
What is the time complexity of this solution?
1

O(n!)

2

O(1)

3

O(2ⁿ)

4

O(n)

Mark as read

Next: Diameter of a Binary Tree

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

(11)

Comment
Anonymous
​
Sort By
Popular
Sort By
F
FavouriteMagentaWarbler627
• 11 months ago

This is not a great problem from leetcode, very poorly written.

8

Reply
S
SubjectiveIndigoSkink289
• 4 months ago

Agree! This statement was difficult to parse: If a node has an empty left or subtree, the sum of the empty subtree is 0.

0

Reply
Abhay Singh
Top 1%
• 1 year ago

Java Solution:

class Solution {

    class Info{
        int nodeTilt;
        int nodeSum;

        Info(int nodeTilt, int nodeSum){
            this.nodeTilt = nodeTilt;
            this.nodeSum = nodeSum;
        }
    }

    public Info solve(TreeNode root){
        if(root == null) return new Info(0, 0);

        Info lc = solve(root.left);
        Info rc = solve(root.right);

        int curTilt = Math.abs(lc.nodeSum - rc.nodeSum);
        return new Info(curTilt + lc.nodeTilt + rc.nodeTilt, root.val + lc.nodeSum + rc.nodeSum);
    }

    public int findTilt(TreeNode root) {
        return solve(root).nodeTilt;
    }
}
Show More

3

Reply
Shannon Monasco
• 1 year ago

Can you supply us with the Node class so we know it has left, right and val?

2

Reply
Du Zheng
• 1 year ago

You could refer the TreeNode class in provided leetcode link https://leetcode.com/problems/binary-tree-tilt/

0

Reply
L
LexicalBronzeWolverine167
Premium
• 2 months ago
def traverse(root):
            if not root:
                return 0
            
            left = traverse(root.left)
            right = traverse(root.right)

            self.tilt += abs(left - right)

            return left + right + root.val

        self.tilt = 0
        traverse(root)

        return self.tilt

0

Reply
Satya Dasara
Premium
• 2 months ago

This problem needs to be understood properly before coding.
We are doing 2 things:

Return sums of all left and right subchildren and current node value
Adding tilt at each level to global variable ans
class Solution:
    def calculateTilt(self, root: TreeNode):
        
        ans = 0

        def dfs(node):
            nonlocal ans

            if not node:
                return 0
            
            left =  dfs(node.left)
            right = dfs(node.right)
            diff = abs(right - left)
            ans += diff

            return node.val + left + right
        
        dfs(root)

        return ans
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

