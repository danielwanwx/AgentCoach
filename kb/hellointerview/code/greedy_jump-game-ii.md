# Jump Game II

> Source: https://www.hellointerview.com/learn/code/greedy/jump-game-ii
> Scraped: 2026-03-30


Imagine stepping stones across a river. You start on the first stone (index 0) and need to reach the final stone. Each stone has a number indicating the maximum distance you can leap from that position. Find the fewest number of leaps required to reach the end. You may assume a path to the end always exists.

Example 1

Input:

nums = [3, 4, 2, 1, 2, 1]

Output:

2

Explanation: From stone 0, leap to stone 1 (you could go up to 3 stones, but 1 is strategic). From stone 1, leap directly to stone 5 (4 stones forward). Total = 2 leaps.

Example 2

Input:

nums = [1, 2, 1, 1, 1]

Output:

3

Explanation: Leap 0→1, then 1→3, then 3→4. Three leaps total.

CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def jump(self, nums: List[int]) -> int:
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
This is a follow-up to Jump Game. In that problem, we just needed to know if we could reach the end. Here, we need to find the minimum number of jumps to get there.
Building Intuition
Think of each index as a platform. The value at each platform tells you how far you can jump from there. Your goal: reach the last platform with as few jumps as possible.
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
can reach 1 or 2
Value = max jump distance
= Goal (index n-1)
From index 0 (value = 2), we can jump to index 1 or 2. But which one should we choose? Let's think about this differently.
Think in Levels
Instead of deciding where to land, think about when to count a jump. Imagine grouping positions by how many jumps it takes to reach them:
2
0
3
1
1
2
1
4
3
4
Level 0
(0 jumps)
Level 1
(1 jump)
Level 2
(2 jumps)
Dashed lines =
boundaries
When we cross a
boundary, we count
a jump!
This is exactly like BFS! Each "level" contains positions reachable with the same number of jumps. The boundary of each level is the farthest position reachable with that many jumps.
The Greedy Strategy
Here's the clever part: we don't need a queue. We just track two boundaries:
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
currentEnd
farthest
i (current position)
currentEnd:
boundary of current jump
farthest:
best we can do from
positions seen so far
currentEnd: The boundary of the current level (positions reachable with current number of jumps)
farthest: The farthest position reachable from any position we've scanned in the current level
When i reaches currentEnd, we've finished scanning the current level. Time to jump! We increment jumps and set currentEnd = farthest.
Walkthrough
Let's trace through nums = [2, 3, 1, 1, 4] step by step to see how the boundary tracking works.
We start with three variables:
jumps = 0: our answer (number of jumps taken)
currentEnd = 0: the boundary of positions reachable with current number of jumps
farthest = 0: the farthest position we can reach from any position we've scanned
Step 1: Process index 0
We're at index 0, which has value 2. This means from here we can jump to index 1 or index 2.
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
jumps = 0
currentEnd = 0
farthest = 0 → 2
i == currentEnd → Jump!
First, we update farthest = max(0, 0 + 2) = 2. From index 0, the farthest we can reach is index 2.
Now check: is i == currentEnd? Yes! i = 0 and currentEnd = 0. We've finished scanning all positions reachable with the current number of jumps (which is just index 0 itself). Time to make a jump!
Increment jumps to 1
Update currentEnd = farthest = 2 (our new boundary)
Step 2: Process index 1
Now we're scanning index 1, which has value 3. From here we could jump to indices 2, 3, or 4.
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
jumps = 1
currentEnd = 2
farthest = 2 → 4
i < currentEnd, continue
Update farthest = max(2, 1 + 3) = 4. Index 1 can reach all the way to index 4 (the goal!). We now know we can reach the end.
Check: is i == currentEnd? No, i = 1 but currentEnd = 2. We're still within our current level (positions reachable with 1 jump), so we don't count another jump yet. Keep scanning.
Step 3: Process index 2
Index 2 has value 1, so from here we can only reach index 3.
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
jumps = 1 → 2
currentEnd = 2 → 4
farthest = 4
i == currentEnd → Jump!
Update farthest = max(4, 2 + 1) = 4. Index 2 can only reach index 3, which doesn't improve our farthest.
Check: is i == currentEnd? Yes! i = 2 and currentEnd = 2. We've finished scanning all positions reachable with 1 jump. Time for jump #2!
Increment jumps to 2
Update currentEnd = farthest = 4
Since currentEnd = 4 now covers the goal (index 4), we're done!
Result: 2 jumps
The optimal path is: 0 → 1 → 4 (jump from index 0 to index 1, then from index 1 to index 4).
We only iterate up to n - 1 (not the last index) because if we're already at the goal, we don't need another jump. This also handles the edge case where currentEnd lands exactly on the last element.
Solution
nums
​
|
nums
comma-separated integers
Try these examples:
Single
Reachable
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def jump(nums):
    if len(nums) <= 1:
        return 0
    
    jumps = 0
    current_end = 0
    farthest = 0
    
    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])
        
        if i == current_end:
            jumps += 1
            current_end = farthest
    
    return jumps
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
jumps = 0

Finding the minimum jumps to reach the end

0 / 16

1x
Greedy solution with boundary tracking
The solution walks through the array once, tracking how far we can reach (farthest) and counting jumps only when we cross boundaries (i == currentEnd). This is essentially a level-order traversal but on a linear scan space.
What is the time complexity of this solution?
1

O(m * n)

2

O(n²)

3

O(n)

4

O(log m * n)

Comparison with Jump Game I
Aspect	Jump Game	Jump Game II
Question	Can we reach the end?	Minimum jumps to reach?
Tracking	Just maxReach	currentEnd + farthest + jumps
Return	Boolean	Integer (count)
The core greedy approach is the same, we greedily track the maximum reach, but Jump Game II adds the boundary concept to count how many jumps we need.

Mark as read

Next: Partition Labels

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

(3)

Comment
Anonymous
Brahmaji Muthoju
Premium
• 29 days ago

notice, i < nums.length - 1, think this needs a special mention.  :))

1

Reply
Tom Tran
Premium
• 1 month ago

Well done!

A very beautiful insight :)

1

Reply
fz zy
Premium
• 3 months ago
class Solution:
    def jump(self, nums: List[int]):
        cutoff, step, furthest = -1, -1, 0
        for i, num in enumerate(nums):
            if i > cutoff:
                step += 1
                cutoff = furthest
            furthest = max(furthest, i + num)
        return step

1

Reply
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

Building Intuition

Think in Levels

The Greedy Strategy

Walkthrough

Solution

Comparison with Jump Game I
