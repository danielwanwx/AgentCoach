# Maximum Depth of Binary Tree

> Source: https://www.hellointerview.com/learn/code/depth-first-search/maximum-depth-of-binary-tree
> Scraped: 2026-03-30


Depth-First Search
Maximum Depth of Binary Tree
easy
DESCRIPTION (inspired by Leetcode.com)

Given the root of a binary tree, write a recursive function to find its maximum depth, where maximum depth is defined as the number of nodes along the longest path from the root node down to a leaf node.

Example 1:

4
2
1
8
7
6
9

Input:

[4, 2, 7, 1, null, 6, 9, null, 8, null, null, null, null, null, null]

Output: 4 (The 4 nodes along the longest path are shown in bold)

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
    def maxDepth(self, root: TreeNode) -> int:
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
If I'm at a node in the tree, what values do I need from my left and right children to calculate the max depth of the current subtree?
the maximum depth of the left subtree.
the maximum depth of the right subtree.
This tells me that each recursive call should return the maximum depth of the subtree rooted at the current node.
So in the body of the recursive function, I'll make recursive calls to the current node's left and right children to get their max depths. Once I have those values, then the maximum depth of the subtree rooted at the current node is 1 (for the current node) + the maximum of the left and right depths. So, each node should return max(left, right) + 1 to its parent.
Base Case
The max depth of an empty tree is 0.
Helper Function
We don't need to pass values from the parent to the child to solve this problem, so we don't need to introduce a helper function.
Global Variables
Each recursive call returns the maximum depth of the subtree rooted at the current code, which matches the answer to the problem, so we don't need to use any global variables.
Solution
SOLUTION
Python
Language
class Solution:
    def maxDepth(self, root):
        if root is None:
            return 0

        # get the maximum depth of the left and right subtrees
        left = self.maxDepth(root.left)
        right = self.maxDepth(root.right)
        return max(left, right) + 1
Animated Solution
nums
​
|
nums
list of integers
Try these examples:
Single
Deeper
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def maxDepth(root):
    if root is None:
        return 0

    left = maxDepth(root.left)
    right = maxDepth(root.right)
    return max(left, right) + 1


4
2
1
3
7
6
9
stack

max depth of binary tree

0 / 29

1x
What is the time complexity of this solution?
1

O(n)

2

O(x * y)

3

O(n * logn)

4

O(2ⁿ)

Mark as read

Next: Path Sum

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

(17)

Comment
Anonymous
​
Sort By
Popular
Sort By
santhosh joruka
• 1 year ago

Space Complexity as explained above does not seem to be reasonable as the call frames would not exceed the height of the tree. Shouldn't it be O(h) where h is the height of the tree?

11

Reply
Anthony Yip
Premium
• 11 months ago

O(h) only applies if it's a balanced tree. If the tree is very skewed (like a linked list), then the worse case scenario would be O(n)

14

Reply
MM
Minnie Mouse
Top 5%
• 6 months ago

O(h) does apply because in the case of a balanced tree, h = log_2(N), and in the case of a linked list presenting tree, h = N. So either O(h) or O(N) is technically correct. Although, I personally prefer O(N) because I find it clearer to describe the complexity in terms of the size of the input, rather than a property of the input such as height, exactly because of the confusions happening above this comment lol.

1

Reply
C
CorrectScarletConstrictor796
Premium
• 11 months ago

I was thinking exactly the same when I was reading it.

0

Reply
Abhay Singh
Top 1%
• 1 year ago

Java Solution:

class Solution {
    public int maxDepth(TreeNode root) {
        if(root == null) return 0;

        return 1 + Math.max(maxDepth(root.left), maxDepth(root.right));
    }
}

9

Reply
K
KeenSilverBobolink836
Premium
• 1 year ago

Using Stack:

class Solution:
    def maxDepth(self, root):
        if root is None:
            return 0

        curr = [(root, 1)]
        max_depth = 0

        while curr:
            n, d = curr.pop()

            max_depth = max(max_depth, d)

            if n.left:
                curr.append([n.left, d+1])
            
            if n.right:
                curr.append([n.right, d+1])
            
        return max_depth
Show More

1

Reply
B
BrilliantPeachElk753
Premium
• 21 days ago

CPP solution

int maxDepth(TreeNode* root) {
        if(!root) return 0;
        return 1 + max(maxDepth(root->left), maxDepth(root->right));
    }

0

Reply
Mohammad kilani
Premium
• 22 days ago
• edited 22 days ago

I do not see an Overview section for DFS. Is this statement incorrect or outdated?
"We can solve this problem using the framework established in the Overview section."

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
