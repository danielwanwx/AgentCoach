# Longest Univalue Path

> Source: https://www.hellointerview.com/learn/code/depth-first-search/longest-univalue-path
> Scraped: 2026-03-30



Depth-First Search
Longest Univalue Path
medium
DESCRIPTION (inspired by Leetcode.com)

Given the root of the binary tree, find the longest path where all nodes along the path have the same value. This path doesn't have to include the root node. Return the number of edges on that path, not the number of nodes.

Example 1:

1
4
4
4
5
5

Input:

[1,4,5,4,4,5]

Output: 2

Explanation: The longest path of the same value is the path [4,4,4], which has a total of 2 edges.

Example 2:

1
1
1
1
1
1
1

Input:

[1,1,1,1,1,1,1]

Output: 4

Explanation: The longest path of the same value is the path [1,1,1,1,1], which has a length of 4.

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
    def longestUnivaluePath(self, root: TreeNode) -> int:
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
We can solve this question using a Post-Order Traversal of the tree, using a similar approach to the Diameter of a Binary Tree problem.
We'll visit each node in the binary tree, and at each node, we'll calculate the length of the longest univalue path that is rooted at that node. We'll then return the longest of those paths at the end. In order to do this in one pass, we'll use a bottom-up approach, or Post-Order Traversal.
Calculating The Longest Univalue Path At A Node
The idea is to have each recursive call return the length of the longest univalue path that is rooted at the current node to its parent. This way, the parent can use the return values from its children to calculate the longest univalue path that passes through the current node.
Let's look at an example of how this works:
If the current node is a leaf node, then the longest univalue path rooted at those nodes is 0.
4
4
4
3
5
5
0
0
Both the leaf nodes shown above return 0 to its parent node.
Those values are received by the parent node, which uses them to calculate the longest univalue path that passes through its node.
The parent first checks if the value of the current node matches the value of its children. If it does, the parent can calculate the longest univalue path that passes through its node by adding 1 to the longest univalue path of its children.
4
4
4
3
5
5
Because the parent (4) has a value equal to its left child, the length of the longest univalue path through node 4 is 1.
The parent node now returns the length of the longest univalue path rooted through its node to its parent, and the process will continue until we have visited all nodes in the tree.
4
4
4
3
5
5
1
Let's visualize another example.
Starting from the leaf nodes:
4
4
4
4
5
5
0
0
Both the leaf nodes shown above return 0 to its parent node.
Node 4 receives those two values, and can extend the longest univalue path that passes through it by 2, since it has the same value as its left and right children.
4
4
4
4
5
5
Longest univalue path through 4: 2 + 0 + 0
Now, Node 4 returns the longest univalue path rooted at its node to its parent, which is only 1, as this is the only path that the parent can possibly extend in order to calculate its own longest univalue path.
4
4
4
4
5
5
1
Using the framework describe in the Overivew section:
Return Values
Each node returns the length of the longest univalue path rooted at its node to its parent.
Base Case
An empty node returns 0, as it does not have any univalue path rooted at its node.
Global Variables
Note that the problem is asking for the length of the longest univalue that goes through a node, not necessarily rooted at a node, which is a different value than what each recursive call returns from the return values.
This means we have to keep track of the longest univalue path that goes through a node, which is stored in a global variable max_length.
Extra Work
At each node, after receiving the return values from its children, we have to check if the node can extend the longest univalue path that goes through it by checking if the value of the node matches the value of its children. We can extend the longest univalue path by 1 for each child that has the same value as the node.
Then, we can update the global variable max_length with the length of the longest univalue path that goes through the current node.
Solution
SOLUTION
Python
Language
class Solution:
    def longestUnivaluePath(self, root):
        max_length = 0
        
        def dfs(node):
            nonlocal max_length
            if not node:
                return 0
            
            left_length = dfs(node.left)
            right_length = dfs(node.right)

            left_arrow = right_arrow = 0

            # check if children have the same value as the current node,
            # which means we can extend the univalue path by including the
            # current node
            if node.left and node.left.val == node.val:
                left_arrow = left_length + 1
            if node.right and node.right.val == node.val:
                right_arrow = right_length + 1

            # left_arrow + right_arrow is the length of the longest
            # univalue path that goes through the current node
            max_length = max(max_length, left_arrow + right_arrow)
            return max(left_arrow, right_arrow)
        
        dfs(root)
        return max_length
What is the time complexity of this solution?
1

O(n log n)

2

O(n)

3

O(n³)

4

O(N + Q)

Mark as read

Next: Graphs Overview

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

(19)

Comment
Anonymous
​
Sort By
Popular
Sort By
A
AdditionalAquamarineHalibut543
• 5 months ago

Would be good to have animation for this question as other questions

15

Reply
H
HolyBeigeDragon306
Premium
• 1 month ago

and use distinct colors if possible,

i.e. don't use dark and dark, and light and light.

Was a bit difficult to see the visuals on the graphs imo

1

Reply
Abhay Singh
Top 1%
• 1 year ago

Java Solution:

class Solution {

    class Node {
        int NTL; // node to leaf path (Height)
        int LTL; // leaf to leaf path (Diameter)
        int maxPathLen;
        
        Node(int ntl, int ltl, int maxPathLen) {
            this.NTL = ntl;
            this.LTL = ltl;
            this.maxPathLen = maxPathLen;
        }
    }

    public Node solve(TreeNode root) {
        if (root == null) return new Node(-1, -1, 0);
        
        Node leftNode = solve(root.left);
        Node rightNode = solve(root.right);
        
        int curNTL = 0;
        if(root.left!=null && root.val == root.left.val) curNTL = Math.max(leftNode.NTL + 1, curNTL);
        if(root.right!=null && root.val == root.right.val) curNTL = Math.max(curNTL, rightNode.NTL + 1);

        int curLTL = Math.max(leftNode.LTL, rightNode.LTL);
        if(root.left!=null && root.val == root.left.val && root.right!=null && root.val == root.right.val){
            curLTL = Math.max(leftNode.NTL + rightNode.NTL + 2, curLTL);
        }

        int curMaxPathLen = Math.max(Math.max(curNTL, curLTL), Math.max(leftNode.maxPathLen, rightNode.maxPathLen));
        
        return new Node(curNTL, curLTL, curMaxPathLen);
    }

    public int longestUnivaluePath(TreeNode root) {
        return solve(root).maxPathLen;
    }
}
Show More

5

Reply
Somdip Se
Premium
• 1 month ago

This article is great. Suggesting some improvements like below -

We are recursing first (postorder) :-
int leftLength = dfs(root.left);
int rightLength = dfs(root.right);

If left child exists and has the same value as root. You can extend that path by 1 edge.
if (root.left != null && root.left.val == root.val) {
leftArrow = leftLength + 1;
}
If values don’t match → path is broken → arrow = 0.

maxLength = Math.max(maxLength, leftArrow + rightArrow);
Above means - A path can pass through this node. Going left ← root → right.
That gives a longer path than either side alone.
This path cannot be extended upward, so we only store it globally.

return Math.max(leftArrow, rightArrow);
Above is because a parent node can only extend one continuous path.
We can't branch upward. So we return best single-direction path.

Show More

2

Reply
W
WillowyBlushCephalopod239
Premium
• 2 months ago

Python Solution:
The idea is that the dfs function returns the number of edges that can be made back to the parent. We pass the parents node into the dfs function and have the children nodes check if its value is equal to its parent.

If a child's val is equal to its parents val, that means an edge can be made. If not, we return a 0, indicating that an edge cannot be formed with that child.

# class TreeNode:
#     def __init__(self, val: int, left: 'TreeNode' = None, right: 'TreeNode' = None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def longestUnivaluePath(self, root: TreeNode):
        ans = 0 
        def dfs(root, parent):
            nonlocal ans
            if not root:
                return 0

            left = dfs(root.left, root)
            right = dfs(root.right, root)
            ans = max(ans, left+right)
            
            return 1 + max(left, right) if root.val == parent.val else 0

        dfs(root, TreeNode(val=0))
        return ans

Show More

2

Reply
E
ElegantAquaMouse760
• 5 days ago
• edited 5 days ago

awesome but further modification would be removing the Dummy Tree node, as that might get misinterpreted, and adding an if-else condition in the end, like below to isolate the parent of the root node:

def longestUnivaluePath( root: Optional[TreeNode]) -> int:
    def solve(node, parent= None):
        if not node:
            return 0
        left_val = solve(node.left, node)
        right_val = solve(node.right, node)
        nonlocal maxCount
        maxCount = max(right_val + left_val, maxCount)
        
        if parent and node.val == parent.val:
            return max(left_val, right_val) + 1 
        else:
            return 0

    maxCount = 0
    solve(root)
    return maxCount
Show More

0

Reply
Daksh Gargas
Premium
• 22 days ago

Go Lang

// type TreeNode struct {
//     Val   int
//     Left  *TreeNode
//     Right *TreeNode
// }

func longestUnivaluePath(root *TreeNode) int {
    if root == nil { return 0 }
    
    longestPath := 0

    var dfs func(node *TreeNode, parentVal int) int
    dfs = func(node *TreeNode, parentVal int) int {
        if node == nil { return 0 }
        left := dfs(node.Left, node.Val)
        right := dfs(node.Right, node.Val)
        count := left + right
        if count > longestPath { longestPath = count }
        if node.Val == parentVal { 
            if left > right {
                return left + 1
            } else {
                return right + 1
            }
         }
        return 0
    }
    
    dfs(root, root.Val)
    return longestPath
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

Calculating the Longest Univalue Path at a Node

Solution

