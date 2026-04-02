# Jump Game

> Source: https://www.hellointerview.com/learn/code/greedy/jump-game
> Scraped: 2026-03-30


Write a function to determine whether you can travel from the first index to the last index of an integer array nums, where each number in the array specifies the maximum distance you can jump from that index. The function should return true if reaching the last index is possible, and false otherwise.

Input:

nums = [1, 3, 0, 1, 4]

Output:

true

Explanation: You can jump from index 0 to index 1, then jump from index 1 to index 4 which is the last index.

Example: Input:

nums = [2,2,1,0,5,1,1]

Output:

false

Explanation: The first three indexes take you to index 3 no matter what. But you cannot move beyond index 3 because its maximum jump length is 0, making the indexes after index 3 unreachable.

CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def canJump(self, nums: List[int]) -> bool:
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
Given an array where each element represents the maximum jump length from that position, determine if you can reach the last index starting from the first index.
Building Intuition
Think of each index as a platform. The value at each platform tells you the maximum distance you can jump from there. You need to figure out: can you reach the goal?
2
3
1
1
4
0
1
2
3
4
nums =
Start
Goal
Value = max jump distance
= Goal (index n-1)
The question isn't about how to get there - just whether it's possible.
The Greedy Insight
We don't need to track every possible path. We just need to track the farthest position we can reach so far.
2
3
1
1
4
0
1
2
3
4
max_reach = 2
From index 0, we can
reach up to index 2.
max_reach = 0 + 2 = 2
As we iterate through the array:
At each position i, update max_reach = max(max_reach, i + nums[i])
If i > max_reach, we're stuck - return false
If we finish the loop, return true
Walkthrough
Let's trace through nums = [2, 3, 1, 1, 4]:
2
3
1
1
4
0
1
2
3
4
i=0:
i=0 ≤ max_reach=0 ✓
max_reach = max(0, 0+2) = 2
i=0: Can we reach index 0? Yes (we start here). From here, we can reach up to index 2. max_reach = 2.
2
3
1
1
4
0
1
2
3
4
i=1:
i=1 ≤ max_reach=2 ✓
max_reach = max(2, 1+3) = 4
i=1: Can we reach index 1? Yes (1 ≤ 2). From here, we can reach up to index 4! max_reach = 4.
2
3
1
1
4
0
1
2
3
4
i=2:
i=2 ≤ max_reach=4 ✓
max_reach = max(4, 2+1) = 4
i=2: Can we reach index 2? Yes (2 ≤ 4). max_reach stays 4.
We continue... max_reach = 4 >= n-1 = 4. Answer: true!
When It Fails
What if we can't reach the end? Consider nums = [3, 2, 1, 0, 4]:
3
2
1
0
4
0
1
2
3
4
At i=3:
max_reach = 3
nums[3] = 0, can't go further
Stuck! Return false
At index 3, nums[3] = 0 means we can't jump anywhere. Since max_reach = 3 and we need to reach index 4, we're stuck.
Visualization
nums
​
|
nums
comma-separated integers
Try these examples:
Stuck
Short Hops
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def canJump(nums):
    max_reach = 0
    for i in range(len(nums)):
        if i > max_reach:
            return False
        max_reach = max(max_reach, i + nums[i])
    return True
2
0
3
1
1
2
1
3
4
4

Checking if we can reach the last index

0 / 12

1x
Try [3, 2, 1, 0, 4] to see a case that returns false!
What is the time complexity of this solution?
1

O(1)

2

O(n)

3

O(log n)

4

O(4^L)

Mark as read

Next: Jump Game II

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

(8)

Comment
Anonymous
Mostafa Shalaby
• 11 months ago

this is such a clever solution

5

Reply
M
ManagerialOliveAntelope938
Premium
• 4 months ago

good solution!

1

Reply
L
LexicalAmaranthEagle768
Premium
• 1 year ago

Am I missing something with second example nums = [4,2,1,0,5,1,1] , this seems to return "true" for me

1

Reply
M
MeaningfulIvoryCod139
Premium
• 1 year ago

Had the same thought. [3,2,1,0,5,1,1] this might be a better fit for the example.

0

Reply
M
MeltedAmberPiranha299
Top 10%
• 22 days ago

Slight alternative:

class Solution:
    def canJump(self, nums: List[int]):
        if not nums:
            return False

        jumps_remaining = nums[0]
        for num in nums[1:]:
            if jumps_remaining == 0:
                return False
            jumps_remaining -= 1
            if num > jumps_remaining:
                jumps_remaining = num
        return True

I'll always just take the largest possible jump I see. It'll fail if at any point in the iteration jumps_remaining == 0.

0

Reply
S
srirama.kusu
Premium
• 7 months ago
# TC: O(n) and SC: O(1)
class Solution:
    def canJump(self, nums: List[int]) -> bool:
        n = len(nums)
        max_reachable = 0 # farthest index we can reach so far
        for i in range(n):
            # If we reach a point that is beyond max_reach, we are stuck
            if i > max_reachable:
                return False
            
            # Update farthest we can reach
            max_reachable = max(max_reachable, i + nums[i])

            # If we can already reach the last index, return True
            if max_reachable >= n - 1:
                return True

0

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

Building Intuition

The Greedy Insight

Walkthrough

When It Fails

Visualization
