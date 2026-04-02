# Rightmost Node

> Source: https://www.hellointerview.com/learn/code/breadth-first-search/rightmost-node
> Scraped: 2026-03-30



​
Sort By
Popular
Sort By
B
BeneficialJadeRook909
Premium
• 1 year ago

I think when users click on the Leetcode link (I assume most do, since they're most likely are familiar with it), it should open the link in a new tab, instead of navigating away from this page. I find myself having to go back manually many times just because of this.

7

Reply

Stefan Mai

Admin
• 1 year ago

Makes sense, fixing!

7

Reply
Amit Chavan
Premium
• 6 months ago

Important detail is to add left child nodes into the queue before the right child nodes

5

Reply
vaibhav aggarwal
Premium
• 1 month ago

I think does not matter. you can reverse the loop condition as well accordingly.

1

Reply
Amit Chavan
Premium
• 1 month ago

That is correct

0

Reply
Xavier Elon
Premium
• 1 year ago

Should show TreeNode class as well so we know what properties to access. Tried to access value instead of val

4

Reply
Muhammad Kamran Khan
• 2 months ago
• edited 2 months ago

Simple Solution.

class Solution:
    def rightmostNode(self, root: TreeNode):
        """
        Returns the right most node at each level of binary tree
        """
        if not root:
            return []

        q = deque([root])
        res = []

        while q:
            k = len(q)
            # it will refer to right most node at the end of each level
            right_most: TreeNode | None = None

            for _ in range(k):
                right_most = q.popleft()

                if right_most.left:
                    q.append(right_most.left)
                if right_most.right:
                    q.append(right_most.right)
            res.append(right_most.val)
        return res
Show More

2

Reply
Mariachi Coder
• 1 year ago

You can also solved this by traversing from right to left

# add nodes as normal to the queue
if node.right:
    queue.append(node.right)
if node.left:
    queue.append(node.left)


2

Reply
Dhruv Erry
• 1 year ago

This is true. Then, this line:

if i == level_size - 1:

Will change to:

if i == 0:

3

Reply
A
AddedLimeCarp593
Top 1%
• 9 months ago

Or you could peek the first element in the queue.

2

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

