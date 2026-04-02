# Maximum Width of Binary Tree

> Source: https://www.hellointerview.com/learn/code/breadth-first-search/maximum-width-of-binary-tree
> Scraped: 2026-03-30


Given the root of a binary tree, write a function to find its maximum width. Each level of the binary tree has a width, which is the number of nodes between the leftmost and rightmost nodes at that level, including the null nodes between them. The function should return the maximum width of the binary tree.

Example 1:

Input:

[4, 2, 7, 1, null, null, 9]
max_width = 4
4
2
1
7
9
null
null
1
2
3
4

Output: 4

Example 2:

Input:

[4, 2, 7, 1]
4
2
1
3
3
6
7
6
9
7
9
3
1
max_width = 2

Output: 2

The third level only has one node, which means the width of that level is one.

Example 3:

Input:

[4,2,7,1,null,6,9,7,null,null,1,1,null]
4
2
1
7
null
3
3
6
7
6
9
7
9
1
3
null
null
null
null
1
max_width = 7
2
3
4
5
1
6
7

Output: 7

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
    def maxWidth(self, root: TreeNode) -> int:
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
Since width is something that is calculated at each level of the binary tree, we should recognize that a level-order breadth-first traversal of the binary tree is the most straightforward way to solve this problem. If we calculate the width at each level, then the max width is just the largest of those values.
Calculating Width
Let's now breakdown how to calculate the width at each level of the binary tree. The width at each level is the number of nodes between the right-most and left-most nodes at that level.
Position Of Nodes
In order to calculate the width at each level, we need to assign each node a "position" value, which represents the position of the node at that level (starting at 0). The diagram below labels the positions of each node in a binary tree:
4
2
1
7
9
null
null
0
1
0
3
1
2
0
The positions of the nodes at each level are labeled in gray
The key insight here is that if we know the position of our node, then we can also calculate the position of both of our children. If our position is p, then our left child's position is 2 * p and our right child's position is 2 * p + 1:
With this in mind, we can extend BFS to also keep track of each node's position. Each time we add a node to the queue, we'll also add its position. Then, each time we pop a node from the queue, we'll have its position, which we can use to calculate the positions of its children, which get added to the queue.
Then, the width at each level is the position of the node minus the position of the leftmost node plus one. The rightmost node is the last node in the queue at each level, and the leftmost node is the first node in the queue at each level.
SOLUTION
Python
Language
class Solution:
    def maxWidth(self, root: TreeNode) -> List[int]:
        if not root:
            return 0

        # enqueue the root node with position 0
        queue = deque([(root, 0)])
        max_ = 0

        while queue:
            level_size = len(queue)

            # leftPos is the position of the leftmost node at the current level
            _, leftPos = queue[0]
            rightPos = -1

            for i in range(level_size):
                node, pos = queue.popleft()

                # update rightPos to the position of the rightmost node
                # when we reach the last node in the level
                if i == level_size - 1:
                    rightPos = pos

                # add the children to the queue with their positions
                if node.left:
                    queue.append((node.left, 2 * pos))
                if node.right:
                    queue.append((node.right, 2 * pos + 1))
            
            # rightPos - leftPos + 1 is the width of the current level 
            max_ = max(max_, rightPos - leftPos + 1)

        return max_
What is the time complexity of this solution?
1

O(n)

2

O(N + Q)

3

O(2ⁿ)

4

O(n²)

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

(15)

Comment
Anonymous
​
Sort By
Popular
Sort By
H
HeavyAmaranthCephalopod183
Premium
• 1 year ago

Thank you for the awesome content. This has been really helpful in my learning so far.

This article seems to be missing from the sidebar. Also the "Next" links to sections that are not included in the sidebar.

7

Reply
retr0
• 1 year ago

Indeed. Still needs fix.

0

Reply
MM
Minnie Mouse
Top 5%
• 6 months ago

For the Python solution, we don't need to iterate through the current level to get the rightmost Node:

_, rightPos = queue[-1]

This will get you the rightmost Node.

6

Reply
A
artem.pushkin
Premium
• 5 months ago

If we assign position numbers to all virtual nodes in a level, below level 30 or so we run into integer overflow. One test case in Leetcode catches this, the tree is a single branch running down the right edge for over 1800 levels. To counter this, we can ensure that the leftmost node in a level always has position 0. Here's the solution in C#.

public class Solution {
    public int WidthOfBinaryTree(TreeNode root) {
        int max = 0;
        Queue<(TreeNode, int)> q = new();
        q.Enqueue((root, 0));

        while (q.Count > 0) {
            int levelSize = q.Count;

            // The leftmost node in the level should have position 0.
            // This prevents int overflow in deep trees.
            int leftOffset = -1; 
            int rightPos = -1;

            for (int i = 0; i < levelSize; i++) {
                (TreeNode node, int position) = q.Dequeue();
                rightPos = position;

                if (node.left != null) {
                    if (leftOffset < 0) leftOffset = position * 2;
                    q.Enqueue((node.left, position * 2 - leftOffset));
                }
                if (node.right != null) {
                    if (leftOffset < 0) leftOffset = position * 2 + 1;
                    q.Enqueue((node.right, position * 2 + 1 - leftOffset));
                }
            }

            max = Math.Max(max, rightPos + 1);
        }

        return max;
   }
}
Show More

2

Reply
VK
Varun Kolanu
Top 10%
• 5 months ago

Thanks!

0

Reply
qiong yu
Premium
• 3 months ago

Queue<Pair<TreeNode, Integer>> queue = new LinkedList<>();

The solution uses Pair, but unfortunately we can not use it in the problem because javafx package is not included. Probably need to fix it.

1

Reply
VK
Varun Kolanu
Top 10%
• 5 months ago

I have written the explanation for the leetcode problem (overflowing solved) here

CPP:

/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    int widthOfBinaryTree(TreeNode* root) {
        int maxWidth = 0;
        queue<pair<TreeNode*, int>> q;
        if (root != nullptr) {
            q.push({root, 0});

            // If no children for root, this will be the max width
            maxWidth = 1;
        }
        
        while (!q.empty()) {
            int numNodesInCurrentLevel = q.size();

            // -1 represents non non-null node not found until now
            long long positionOfFirstNodeInCurrentLevel = -1;

            for (int i=0; i<numNodesInCurrentLevel; ++i) {
                auto [parentNode, parentPosition] = q.front();
                q.pop();

                TreeNode* leftChild = parentNode -> left;
                TreeNode* rightChild = parentNode -> right;
                if (leftChild != nullptr) {
                    // Note: Absolute positioning here denotes the position of a node wrt the left most node in
                    // the parent level, and not wrt to the possible left most node in the current level (because
                    // the positions of nodes in parent level itself were relative and the first node in parent
                    // level will have position = 0.)

                    // So, summary: absolute position is wrt to leftmost node in parent level
                    // and relative position is wrt to leftmost node in the current level.
                    long long leftChildAbsolutePosition = 2LL*parentPosition;
                    if (positionOfFirstNodeInCurrentLevel == -1)
                        positionOfFirstNodeInCurrentLevel = leftChildAbsolutePosition;

                    int relativePositionWrtFirstNode = leftChildAbsolutePosition - positionOfFirstNodeInCurrentLevel;
                    q.push({leftChild, relativePositionWrtFirstNode});
                    maxWidth = max(maxWidth, relativePositionWrtFirstNode + 1);
                }

                if (rightChild != nullptr) {
                    long long rightChildAbsolutePosition = 2LL*parentPosition + 1;
                    if (positionOfFirstNodeInCurrentLevel == -1)
                        positionOfFirstNodeInCurrentLevel = rightChildAbsolutePosition;

                    int relativePositionWrtFirstNode = rightChildAbsolutePosition - positionOfFirstNodeInCurrentLevel;
                    q.push({rightChild,  relativePositionWrtFirstNode});
                    maxWidth = max(maxWidth, relativePositionWrtFirstNode + 1);
                }
            }
        }

        return maxWidth;
    }
};
Show More

1

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

Calculating Width

Position of Nodes
