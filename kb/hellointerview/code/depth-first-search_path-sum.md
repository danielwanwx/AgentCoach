# Path Sum

> Source: https://www.hellointerview.com/learn/code/depth-first-search/path-sum
> Scraped: 2026-03-30



Depth-First Search
Path Sum
easy
DESCRIPTION (inspired by Leetcode.com)

Given the root of a binary tree and an integer target, write a recursive function to determine if the tree has a root-to-leaf path where all the values along that path sum to the target.

Example 1:

4
2
1
3
7
6
9

Input:

[4, 2, 7, 1, 3, 6, 9]
target = 17 

Output: true (the path is 4 -> 7 -> 6)

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
target = 13

Output: false

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
    def pathSum(self, root: TreeNode, target: int) -> bool:
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
If I'm at a node in the tree, what values do I need from my child to tell if there's a path from the root to a leaf that sums to the target?
In order for there to be a path from the root to a leaf that sums to the target, there must be a path from either the left or right child to a leaf that sums to target - node.val.
This tells us that each recursive call should return True if there's a path from the current node to a leaf that sums to the current target, and False otherwise. In the body, we'll make recursive calls to the current node's left and right children, passing in target - node.val for the current target. If either of those calls returns True, then we should return True to the parent.
Base Case
If our current node is None, then our subtree is empty and there's no path from the current node to a leaf that sums to the target.
If our current node is a leaf node, then we check if the target is equal to the leaf node's value. If it is, then there's a path from the current node to a leaf that sums to the target.
Helper Functions
We need to pass the current target down from parent to children nodes, but this is included in the function signature of the main function, so we don't need to introduce a helper function.
Global Variables
The return value of each recursive call matches the answer to the problem, so we don't need to use any global variables.
Solution
SOLUTION
Python
Language
class Solution:
    def pathSum(self, root, target):
        if root is None:
            return False
       
        # if we reach a leaf node, check if the target is equal to the leaf node's value
        if not root.left and not root.right:
            return target == root.val

        target -= root.val
        
        # check if there's a path from the current node to a leaf that sums to target
        return self.pathSum(root.left, target) or self.pathSum(root.right, target)
Animated Solution
nums
​
|
nums
list of integers
target
​
|
target
integer
Try these examples:
Path Found
No Path
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def hasPathSum(root, target):
  if not root:
    return False

  if not root.left and not root.right:
    return target == root.val

  left = hasPathSum(root.left, target - root.val)
  right = hasPathSum(root.right, target - root.val)
  return left or right
target: 13


4
2
1
3
7
6
9

path sum

0 / 13

1x
What is the time complexity of this solution?
1

O(m * n)

2

O(m * n * 4^L)

3

O(n)

4

O(log n)

Mark as read

Next: Passing Values Down and Helper Functions

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

(22)

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

    public boolean solve(TreeNode root, int sum, int targetSum){
        if(root == null) return false;
        if(sum == targetSum){
            if(root.left==null && root.right==null) return true;
        }

        if(root.left!=null && solve(root.left, sum+root.left.val, targetSum)){
            return true;
        }

        if(root.right!=null && solve(root.right, sum+root.right.val, targetSum)){
            return true;
        }

        return false;
    }

    public boolean hasPathSum(TreeNode root, int targetSum) {
        if(root == null) return false;
        
        return solve(root, root.val, targetSum);
    }
}
Show More

3

Reply
Kamrun Nahar Liza
• 1 year ago

Finally, I think I got recursion, such great visuals, framework, and explanation! One thing tho, for targetSum 17 in this call stack visual, it should early return on the path 4 -> 7 -> 6 right?(because of the short circuit of or logic). But the visual shows it goes on to the right child regardless.

2

Reply
Jimmy Zhang
Top 5%
• 1 year ago

Hey really good question!

The visual doesn't show the most optimized version of the code. I have it making the call to the right child regardless because it was simpler to implement that way.

The most optimized version of the code should short circuit as you mentioned. For that the return statement would be:

retrun hasPathSum(root.left, target - root.val) or hasPathSum(root.right, target - root.val)

So the or statement for root.left short circuits before making the recursive call to root.right.

Hope that helps! Let me know if you have any other questions

3

Reply
Kamrun Nahar Liza
• 1 year ago

Oh I see it now haha, thank you for your reply as it clarified my confusion and solidified that I understood the concepts. I am looking at the code again, it's the version that calculated all the left, then right, stored in variables left and right, and after that, the return left or right statement got executed. So, yeah, it explored all the possible paths before or logic.

0

Reply
manohar chowdary
Premium
• 6 days ago

finding base case was tricky

0

Reply
F
ForeignBronzeFelidae167
Premium
• 14 days ago
• edited 14 days ago
public Boolean pathSum(TreeNode root, Integer target) { 
        return root == null ? false : 
             ((root.left==null && root.right==null && target-root.val==0) ? true :  
                  pathSum(root.left, target-root.val) || pathSum(root.right, target-root.val));
    }

0

Reply
C
CheerfulVioletWhitefish604
• 1 month ago

quite a few times if you implement the AI feedback, it will:

tell you the implemented has a flaw and should revert back to other. ex: mutating target vs passing decrementing in the recursive call
suggest a very different approach from provided solution, ex: DFS vs BFS

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

