# Level Order Sum

> Source: https://www.hellointerview.com/learn/code/breadth-first-search/level-order-sum
> Scraped: 2026-03-30



​
Sort By
Popular
Sort By
Viktoryia Gruzitskaya
Premium
• 1 year ago

The input for example 2 should be [1, 2, 5, 3, null, null, null, 4] instead of [1, 2, 5, 3, null, null, 4].

6

Reply
L
LexicalBronzeWolverine167
Premium
• 2 months ago
def level_order_sum(self, root: TreeNode):
        def traverse(root, ind):
            if not root:
                return
            
            if len(self.levels) == ind:
                self.levels.append(0)
            
            self.levels[ind] += root.val

            traverse(root.left, ind + 1)
            traverse(root.right, ind + 1)

        self.levels = []
        traverse(root, 0)

        return self.levels

1

Reply
C
CivicGreenAardwolf945
Premium
• 1 month ago

Please fix Rust test cases. root is always passed as None.

0

Reply
Geethu Krishna
• 1 month ago

Time : O(n)
Space : O(n)

Java Solution

public class Solution {
    public List<Integer> level_order_sum(TreeNode root) {
         ArrayList<Integer> result = new ArrayList<Integer>();
        Queue<TreeNode> queue = new LinkedList<TreeNode>();
        if(root == null)
            return result;

        queue.offer(root);

        while(!queue.isEmpty()){
            int size = queue.size();
            int sum = 0;

            for(int i = 0; i < size; i++){
                TreeNode node = queue.poll();
                sum+= node.val;
                if(node.left != null)
                    queue.offer(node.left);
                if(node.right!=null)
                    queue.offer(node.right);
            }
            result.add(sum);
        }
        return result;
    }
}
Show More

0

Reply
S
socialguy
Top 5%
• 1 year ago

Some weird error for perfectly valid code.

class Solution:
    def level_order_sum(self, root: TreeNode) -> list[int]:
        to_visit = deque([root])
        level_sum: list[int] = []

        while to_visit:
            n = len(to_visit)
            running_sum = 0
            for _ in range(n):
                node = to_visit.popleft()
                running_sum += node.val
                if node.left is not None:
                    to_visit.append(node.left)
                if node.right is not None:
                    to_visit.append(node.right)
            level_sum.append(running_sum)

        return level_sum

Traceback (most recent call last): File "/box/TestSolution.py", line 48, in <module> test_case4() File "/box/TestSolution.py", line 42, in test_case4 result = solution.level_order_sum(TreeNode.from_array([])) File "/box/Solution.py", line 17, in level_order_sum running_sum += node.val AttributeError: 'NoneType' object has no attribute 'val'

Show More

0

Reply
Peter Kim
• 1 year ago

Add if not root: return []

3

Reply
S
socialguy
Top 5%
• 1 year ago

root is typed as not null, so, either there is an invalid test case, or the function signature needs to be changed to Optional.

2

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

