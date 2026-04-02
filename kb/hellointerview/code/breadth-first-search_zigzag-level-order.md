# Zigzag Level Order

> Source: https://www.hellointerview.com/learn/code/breadth-first-search/zigzag-level-order
> Scraped: 2026-03-30



​
Sort By
Popular
Sort By
A
AtomicTealChicken803
Premium
• 8 months ago

Return type for Java version is int[][] in the code editor, however in the solution it is List<List<Integer>>.
Can we please get this fixed?

3

Reply
Shivam Chauhan
• 8 months ago

Hey thanks for pointing this out!
This is fixed.

0

Reply
Benjamin Teo
Premium
• 1 month ago

It's still int[][] for me in the code editor.

2

Reply
Hrushikesh Mulavekar
Premium
• 1 month ago

it is not

0

Reply
A
akshaykbkale
• 3 months ago

My simple solution of using existing size of queue after traversing a level, not sure this is acceptable in interviews.

def zig_zag(self, root: TreeNode):
        # Your code goes here
        if not root:
            return []
        dq = deque([root])
        res = []
        reverse = True
        while dq:
            size = len(dq)
            levelValues = [0]*size
            for i in range(size):
                idx = i if not reverse else size - i - 1
                node = dq.popleft()
                levelValues[idx] = node.val
                if node.left:
                    dq.append(node.left)
                if node.right:
                    dq.append(node.right)
            res.append(levelValues)
            reverse = not reverse
        return res
Show More

1

Reply
E
ExpensiveMagentaCrocodile897
Premium
• 8 months ago

For Ruby, the Queue class doesn't have double-ended popping, and the Array class doesn't have a O(1) dequeue, so I instead am using an Array and popping from the end, and using the left_to_right variable to know whether to insert the .right first or the .left first.
Since its a stack, we can't just pop from the end and then insert right back in at the front, so I use a second copy of a stack (I've seen this technique used elsewhere)

def zigzag_level_order(root)
    res = []
    stack = []
    stack.push(root) if root

    reverse = false
    while !stack.empty?
        level = []
        next_stack = []
        length = stack.length

        length.times do 
            node = stack.pop
            level.push(node.val)
            if reverse
                next_stack.push(node.right) if node.right
                next_stack.push(node.left) if node.left
            else
                next_stack.push(node.left) if node.left
                next_stack.push(node.right) if node.right
            end
        end

        reverse = !reverse
        stack = next_stack
        res << level
    end

    res
end
Show More

1

Reply
Daksh Gargas
Premium
• 15 days ago
• edited 15 days ago

Go Lang Solution:

// type TreeNode struct {
//     Val   int
//     Left  *TreeNode
//     Right *TreeNode
// }

// Using Go 1.22+
func zig_zag(root *TreeNode) [][]int {
	result := [][]int{}
	if root == nil {
		return result
	}

	queue := []*TreeNode{root}
        head := 0
	shouldReverse := false

	for head < len(queue) {
		levelSize := len(queue) - head
        res := make([]int, levelSize)
		for i := range levelSize {
			node := queue[head]; head++
			if shouldReverse {
				res[(levelSize-1)-i] = node.Val
			} else {
				res[i] = node.Val
			}
			if node.Left != nil {
				queue = append(queue, node.Left)
			}
			if node.Right != nil {
				queue = append(queue, node.Right)
			}
		}
		result = append(result, res)
        if head > len(queue) / 2 { queue, head = queue[head:], 0}
        shouldReverse = !shouldReverse
	}

	return result
}
Show More

0

Reply
A
AdvisoryApricotErmine448
• 1 month ago

Minor suggestion - The active page should be highlighted in the left sidebar list. It should also update when the user clicks the 'Next' link.

0

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

Left to Right Processing

Right to Left Processing

