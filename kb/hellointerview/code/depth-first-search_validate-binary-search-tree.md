# Validate Binary Search Tree

> Source: https://www.hellointerview.com/learn/code/depth-first-search/validate-binary-search-tree
> Scraped: 2026-03-30



Depth-First Search
Validate Binary Search Tree
medium
DESCRIPTION (inspired by Leetcode.com)

Given the root of a binary tree, determine if it is a valid binary search tree (BST).

A tree is a BST if the following conditions are met:

Every node on the left subtree has a value less than the value of the current node.
Every node on the right subtree has a value greater than the value of the current node.
The left and right subtrees must also be valid BSTs.

Example 1:

2
1
4

Input:

[2,1,4]

Output: true

Example 2:

4
1
5
3
6

Input:

[4,1,5,null,null,3,6]

Output: false. 3 is the the root node's right subtree, but it is less than the root node 4.

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
    def validateBST(self, root: TreeNode) -> bool:
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
Let's think about what it means for a binary tree to be a valid binary search tree. For a binary tree to be a valid binary search tree, the following conditions must be true:
Every node in the left subtree of the root node must have a value less than the value of the root node.
Every node in the right subtree of the root node must have a value greater than the value of the root node.
This definition is true for every subtree in the node.
We can use that definition to validate a binary search tree by having parents pass values down to their children. Let's say we are validating this binary search tree:
4
2
1
3
7
6
9
Based on the definition of a valid binary search tree, any value in the left subtree must be less than 4, but there is no limit to how small the values are.
So we can pass max = 4 and min = -inf to the left child as a range of valid values of the left subtree.
4
2
1
3
7
6
9
max: 4
min: -inf
From there, for the subtree rooted at node 2:
The max value of any node in the left subtree 2 is 2, and the min value is still -inf.
4
2
1
3
7
6
9
max: 2
min: -inf
Any value in the right subtree must be greater than the 2, but also less than 4 (the value of the root node). So we can pass max = 4 and min = 2 to the right child as a range of valid values of the right subtree.
4
2
1
3
7
6
9
max: 4
min: 2
We can visit each node in the tree, and have the parent pass down the range of valid values to their children in this fashion. If the current node's value falls outside of the valid range, we can return False immediately. If we reach the empty subtree, this means that we have not yet found an invalid node yet, and we can return True.
Return Values
If I'm at a node in the tree, what values do I need from my left and right children to tell if the current subtree is a valid binary search tree?
The current subtree is a valid binary search tree if:
The left subtree is a valid binary search tree.
The right subtree is a valid binary search tree.
And the value of the current node falls within the valid range.
This tells me that each recursive call should return a boolean value indicating whether the current subtree is a valid binary search tree.
Base Case
An empty tree is a valid binary search tree.
Extra Work
The work that we need to do at each node is to check if the current node's value falls within the valid range. If it doesn't we can return False immediately.
Helper Functions
Since we need to pass the minimum and maximum values down to their children, we need to introduce a helper function to keep track of these values.
This helper function will introduce two parameters, min_ and max_, which represent the range of values that the current subtree's nodes can take on. The helper function will return a boolean value indicating whether the current subtree is a valid binary search tree.
When we recurse to our left child, we:
Pass the current node's value as the new max_ value, since the left child's value must be less than the current node's value. min_ remains the same.
When we recurse to our right child, we:
Pass the current node's value as the new min_ value, since the right child's value must be greater than the current node's value. max_ remains the same.
Global Variables
The return value of the helper function matches the answer to the problem, so we don't need to use any global variables.
Solution
SOLUTION
Python
Language
class Solution:
    def validateBST(self, root):
        def dfs(node, min_, max_):
            # base case
            if node is None:
                return True

            # check if the current node's value is within the valid range
            if node.val <= min_ or node.val >= max_:
                return False

            return dfs(node.left, min_, node.val) and dfs(node.right, node.val, max_)

        return dfs(root, float('-inf'), float('inf'))
What is the time complexity of this solution?
1

O(n)

2

O(4^L)

3

O(1)

4

O(n²)

Mark as read

Next: Calculate Tilt

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
Abhay Singh
Top 1%
• 1 year ago

Java Solution:

class Solution {

    class Info{
        boolean isBST;
        long minValue;
        long maxValue;

        Info(boolean isBST, long minValue, long maxValue){
            this.isBST = isBST;
            this.minValue = minValue;
            this.maxValue = maxValue;
        } 
    }

    public Info solve(TreeNode root){
        if(root == null) return new Info(true, Long.MAX_VALUE, Long.MIN_VALUE);

        Info lc = solve(root.left);
        Info rc = solve(root.right);

        long curMin = Math.min(root.val, Math.min(lc.minValue, rc.minValue));
        long curMax = Math.max(root.val, Math.max(lc.maxValue, rc.maxValue));

        boolean curBST = true;
        if(lc.isBST == false || rc.isBST == false || root.val <= lc.maxValue || root.val >= rc.minValue){
            curBST = false;
        }

        return new Info(curBST, curMin, curMax);
    }

    public boolean isValidBST(TreeNode root) {
        return solve(root).isBST;
    }
}
Show More

4

Reply
Pankaj Kapoor
Premium
• 1 month ago

how about just do inorder traversal and check with prev each time.

1

Reply
R
raphael.licha2
Premium
• 5 months ago

Just for the record, I think the first phrase of the problem description is unnecessary (Given the root of a binary, write a recursive function to determine if it is a valid binary search tree). It would make the description more concise and accurate.

1

Reply
S
SubjectiveIndigoSkink289
• 4 months ago

Yes, I find the writing in the coding descriptions sometimes confusing too!

0

Reply

Shivam Chauhan

Admin
• 4 months ago

Thanks for this, we have rectified this and would be live in next release.

0

Reply
M
ModestAquaWildfowl918
Premium
• 15 days ago

Alternative solution only using return values

public class Solution {
    public Boolean validateBST(TreeNode root) {
        return validateBSTHelper(root).valid;
    }

    private TreeResult validateBSTHelper(TreeNode node) {
        if (node == null) {
            return new TreeResult(true, Long.MAX_VALUE, Long.MIN_VALUE);
        }

        TreeResult leftResult = validateBSTHelper(node.left);
        TreeResult rightResult = validateBSTHelper(node.right);

        if (!leftResult.valid || !rightResult.valid) {
            return new TreeResult(false, Long.MAX_VALUE, Long.MIN_VALUE);
        }

        final Boolean isValid =
            leftResult.max < node.val &&
            node.val < rightResult.min;

        return new TreeResult(isValid, Math.min(node.val, leftResult.min), Math.max(node.val, rightResult.max));
    }

    private class TreeResult {
        private boolean valid;
        private long min;
        private long max;

        TreeResult(boolean valid, long min, long max) {
            this.valid = valid;
            this.max = max;
            this.min = min;
        }
    }
}
Show More

0

Reply
Tarundeep Singh
Premium
• 19 days ago
• edited 19 days ago

Test cases are weak even Wrong answer are getting passed. Please correct them
class RT{
int max;
int min;
Boolean isBst;
RT(){
}
}
public class Solution {
public Boolean validateBST(TreeNode root) {
RT rt = validate(root);
return rt.isBst;
}
public RT validate(TreeNode root){
RT rt = new RT();
rt.isBst = true;
if(root == null){
rt.max = Integer.MIN_VALUE;
rt.min = Integer.MAX_VALUE;
return rt;
}
RT left = validate(root.left);
RT right = validate(root.right);
rt.min = Math.min(root.val, left.min);
rt.max = Math.max(root.val, right.max);
if(!left.isBst || !right.isBst || (root.val <= left.max || root.val >= right.min)){
rt.isBst = false;
return rt;
}
return rt;
}
}
above must pass but below ones condition replaced in above also passes
if(root.val < left.max || root.val >= right.min) :: here not checked if left and right tree were bst

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

