# Path Sum II

> Source: https://www.hellointerview.com/learn/code/depth-first-search/path-sum-2
> Scraped: 2026-03-30




Depth-First Search
Path Sum II
medium
DESCRIPTION (inspired by Leetcode.com)

Given the root of a binary tree and an integer target, write a recursive function to find all root-to-leaf paths where the sum of all the values along the path sum to target.

Example 1:

1
2
4
7
4
5
1

Input:

[1,2,4,4,7,5,1]
target = 10

Output:

[[1,2,7],[1,4,5]] # [[1,4,5],[1,2,7]] is also accepted.

The paths are 1 -> 2 -> 7 and 1 -> 4 -> 5

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
    def pathSum(self, root: TreeNode, target: int) -> List[List[int]]:
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
This problem is an extension of the Path Sum problem. In this problem, we are asked to return a list of all root-to-leaf paths where the sum of the nodes in the path equals a given target sum.
This is an example of a question which benefits from using a global variable that all recursive calls have access to store the list of all root-to-leaf paths that match the target sum.
Return Values
In this case question, we don't need our recursive calls to return any values. Instead, we use depth-first search to traverse each root-to-leaf path in the tree, while maintaining the state of the current path via parameters to the recursive call.
Base Case
We can stop recursing when our tree is empty.
Extra Work
At each node, we need to add the value of the node to the current path.
Whenever we are at a leaf node, we can check if the value of the current node matches the target. If it does, we can add the current path to the global list of paths.
Helper Function
Parent nodes need to pass two pieces of information down to their children:
The remaining target sum
The values along the current path (starting from the root).
These values must be passed down as parameters of the recursive call, so we need to introduce a helper function to help us recurse.
Global Variables
We will use a global variable to store the root-to-leaf paths that match the given target. This allows us to avoid having to return path arrays up the recursion stack and simplifies collecting all valid paths.
SOLUTION
Python
Language
def dfs(node, target, path):
    # base case
    if not node:
        return

    # append current value to the path
    path.append(node.val)
    if not node.left and not node.right:
        if node.val == target:
            result.append(path[:])

    dfs(node.left, target - node.val, path)
    dfs(node.right, target - node.val, path)

    # when our code reaches here, are done exploring all
    # the root-to-leaf paths that go through the current node.
    # pop the current value from the path to prepare for the next path
    path.pop()
Global Variables
We can use a single global variable that all recursive calls have access to store the list of paths that add up to the target sum.
Solution
SOLUTION
Python
Language
class Solution:
    def pathSum(self, root, target):
        def dfs(node, target, path):
            # base case
            if not node:
                return

            # append current value to the path
            path.append(node.val)
            if not node.left and not node.right:
                if node.val == target:
                    result.append(path[:])

            dfs(node.left, target - node.val, path)
            dfs(node.right, target - node.val, path)

            # when our code reaches here, are done exploring all
            # the root-to-leaf paths that go through the current node.
            # pop the current value from the path to prepare for the next path
            path.pop()

        result = []
        dfs(root, target, [])
        return result
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
def pathSum(root, target):
  def dfs(node, target, path):
    if not node:
      return
    
    path.append(node.val)
    if not node.left and not node.right:
      if node.val == target:
        result.append(path[:])
    
    dfs(node.left, target - node.val, path)
    dfs(node.right, target - node.val, path)
    path.pop()

  result = []
  dfs(root, target, [])
  return result
1
2
4
7
4
5
1

path sum II

0 / 41

1x
What is the time complexity of this solution?
1

O(1)

2

O(n²)

3

O(n * logn)

4

O(n)

Mark as read

Next: Longest Univalue Path

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
Yan
• 1 year ago

The runtime should be O(n^2), cause need to do n times of copy array path[:] operation,  worst case is O(n) of copy for unbalanced tree

10

Reply
W
WittyWhiteBovid129
Premium
• 7 months ago

Would it not be O(n*logn) since path can have a max of O(logn) length (height of the tree)

I guess if the tree is skewed then it would O(n^2)

0

Reply
BeffJezos
Premium
• 2 months ago

If the tree is skewed, there's at most O(2N) work done, so it's O(N) if all values are unique.

O(N^2) is the case wehre the tree is just full of nodes of value of 0, and the target is 0 with a skewed tree.

0

Reply
Mahsa Aghajani
Premium
• 7 months ago

In the first code snippet in the section "Explanation", the return statement is wrong in the condition:
if not node.left and not node.right:
if node.val == target:
result.append(path[:])
return

The code part in section "Solution" does not have this return statement either.

4

Reply
Aneesh Mysore
• 10 months ago

In one of the code snippets this is written:

if node.val == target:
    result.append(path[:])
    return

And then in the solution the return statement is removed. The return should not be there

4

Reply
kaivalya apte
Premium
• 6 months ago

The solution must return an int[][] and not a List<List<Integer>> solution must be corrected.

return result.stream()
.map(l -> l.stream().mapToInt(Integer::intValue).toArray())
.toArray(int[][]::new);

3

Reply
B
Brandredo
Premium
• 7 months ago

In the first solution of the helper function where it says "Global Variable" there's a typo. The code contains a return statement which would break the code.

// append current value to the path
path.add(node.val);
if (node.val == target) {
            result.add(new ArrayList<>(path));
            return;
}

1

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

