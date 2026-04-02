# Split Array Largest Sum

> Source: https://www.hellointerview.com/learn/code/binary-search/split-array-largest-sum
> Scraped: 2026-03-30


Binary Search
Split Array Largest Sum
hard
DESCRIPTION (inspired by Leetcode.com)

You are given an array nums and an integer k. nums represents the weights of n consecutive tasks while k represents the number of workers. Tasks are assigned to the workers as contiguous blocks.

Your goal is to distribute the work so that the heaviest workload (sum of task weights for any single worker) is as small as possible.

Return the minimum possible value of the maximum workload.

Example 1:

Input:

nums = [4, 8, 15, 7, 3], k = 3

Output: 15

Explanation: One optimal split is [4, 8] (sum=12), [15] (sum=15), [7, 3] (sum=10). The maximum workload among workers is 15.

Example 2:

Input:

nums = [6, 3, 9, 2, 1, 8], k = 2

Output: 18

Explanation: Split into [6, 3, 9] (sum=18) and [2, 1, 8] (sum=11). The heaviest workload is 18. Any other split with 2 groups results in a higher maximum.

CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def splitArray(self, nums: List[int], k: int) -> int:
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

Understanding the Problem
We have an array of positive integers and need to split it into exactly k contiguous subarrays. Among all possible ways to split, we want to find the one where the maximum subarray sum is as small as possible.
7
2
5
10
8
0
1
2
3
4
nums =
Subarray 1
sum = 14
Subarray 2
sum = 18
Split into k=2 parts
Max sum = 18
Goal: minimize this!
Think of it like distributing work among k workers, where each worker handles a contiguous portion. We want to minimize the maximum load on any single worker.
Key Observation: The Answer Has Bounds
Before diving into the solution, let's think about what values the answer could possibly take:
10
max(nums)
32
sum(nums)
18
answer
Search Space
Minimum possible: At least max(nums) = 10. Why? Because every element has to land in some subarray, and a subarray containing the largest element will have a sum of at least that element's value. If we tried a max sum of, say, 9, the element 10 couldn't fit in any subarray at all — the split would be impossible. So max(nums) is the smallest max-sum that's even worth considering.
Maximum possible: At most sum(nums) = 32. This happens when k = 1 (one big subarray).
So our answer lies in the range [10, 32].
Why Binary Search?
Here's the crucial observation: if we can split with max sum X, we can definitely split with any max sum greater than X.
Can't split
answer = 18
Can split ✓
More capacity =
more flexibility
maxSum too small
maxSum large enough
This monotonic property is exactly what enables binary search! The search space is divided into two halves: values that don't work, and values that do. Binary search finds the boundary.
This is the "Binary Search on Answer" pattern. Instead of searching through the array for an element, we search through the space of possible answers to find the optimal one. The monotonic property guarantees binary search will find it.
The Binary Search Algorithm
Here's how the binary search works:
left
mid
right
Algorithm:
1. mid = (left + right) / 2
2. canSplit(mid)?
Yes → right = mid
No → left = mid + 1
3. Repeat until left == right
Initialize: left = max(nums), right = sum(nums)
Loop while left < right:
Pick mid = (left + right) / 2
If we can split with max sum ≤ mid: answer might be smaller → right = mid
If we can't: answer must be larger → left = mid + 1
Return left (the minimum valid answer)
splitArray(nums, k)
    left = max(nums)
    right = sum(nums)
    
    while left < right
        mid = (left + right) / 2
        if canSplit(nums, k, mid)
            right = mid
        else
            left = mid + 1
    
    return left
The Feasibility Check (Helper Function)
For each mid, we need a helper function to check: "Can we split into ≤ k subarrays with max sum ≤ mid?"
7
2
5
10
8
sum = 14 ≤ 18 ✓
sum = 18 ≤ 18 ✓
canSplit(maxSum = 18)
Greedy: pack as much
as possible per subarray
Need 2 subarrays, k = 2
Return: true
Greedy approach (O(n) per check):
Iterate left to right, greedily adding elements to the current subarray
When the sum would exceed maxSum, start a new subarray
Return true if subarrays_needed ≤ k, else false
canSplit(nums, k, maxSum)
    subarrays = 1
    currentSum = 0
    
    for num in nums
        if currentSum + num > maxSum
            subarrays = subarrays + 1
            currentSum = num
        else
            currentSum = currentSum + num
    
    return subarrays <= k
Walkthrough
Let's trace through nums = [7, 2, 5, 10, 8] with k = 2 to see how the binary search narrows down the answer.
Step 1: Initialize the search bounds
First, we establish the range of possible answers. The minimum possible max-sum is max(nums) = 10 — no matter how we split, the subarray containing 10 will have a sum of at least 10, so there's no point trying anything smaller. The maximum is sum(nums) = 32 (if we put everything in one subarray).
Step 1:
Initialize bounds
left=10
right=32
Our search space is [10, 32]. Now we start binary searching for the minimum valid max-sum.
Step 2: First binary search iteration
We try mid = (10 + 32) / 2 = 21. Can we split into ≤ 2 subarrays where each has sum ≤ 21?
Using the greedy check: [7, 2, 5] has sum 14 ≤ 21 ✓, then [10, 8] has sum 18 ≤ 21 ✓. That's only 2 subarrays, so yes, it's feasible!
Since mid = 21 works, the answer might be even smaller. We set right = mid = 21 to search the lower half.
Step 2:
mid = 21, canSplit? → ✓ (needs 2 subarrays)
left=10
mid=21
right=21
Step 3: Second binary search iteration
Now left = 10, right = 21. We try mid = (10 + 21) / 2 = 15. Can we split with max sum ≤ 15?
Greedy check: [7, 2, 5] sum = 14 ≤ 15 ✓, but [10] alone is already 10 ≤ 15 ✓, then [8] is 8 ≤ 15 ✓. Wait, that's 3 subarrays! We only have k = 2.
Actually, let's be more careful: [7, 2] sum = 9, adding 5 gives 14 ≤ 15 ✓. Adding 10 would give 24 > 15 ✗, so start new subarray. [10] sum = 10 ≤ 15 ✓. Adding 8 would give 18 > 15 ✗, so start new subarray. [8] sum = 8. That's 3 subarrays, but we need ≤ 2. Not feasible!
Since mid = 15 doesn't work, the answer must be larger. We set left = mid + 1 = 16.
Step 3:
mid = 15, canSplit? → ✗ (needs 3 subarrays)
left=10
mid=15
right=21
left = 16
Step 4: Continue narrowing
Now left = 16, right = 21. We continue binary searching:
mid = 18: Can we split with max ≤ 18? [7, 2, 5] = 14 ≤ 18 ✓, [10, 8] = 18 ≤ 18 ✓. Yes! Set right = 18.
mid = 17: Can we split with max ≤ 17? [7, 2, 5] = 14 ≤ 17 ✓, [10] = 10 ≤ 17 ✓, [8] = 8 ≤ 17 ✓. That's 3 subarrays. No! Set left = 18.
Now left = right = 18, so we're done!
Step 4:
Converged: left = right = 18
left=18
right=18
Answer: 18
Result: 18
The minimum possible max-subarray-sum is 18, achieved by splitting [7, 2, 5] (sum = 14) and [10, 8] (sum = 18).
Visualization
nums
​
|
nums
comma-separated positive integers
k
​
|
k
subarrays
Try these examples:
K=1
Balanced
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def splitArray(nums, k):
    def canSplit(maxSum):
        subarrays = 1
        currentSum = 0
        for num in nums:
            if currentSum + num > maxSum:
                subarrays += 1
                currentSum = num
            else:
                currentSum += num
        return subarrays <= k
    
    left = max(nums)
    right = sum(nums)
    
    while left < right:
        mid = (left + right) // 2
        if canSplit(mid):
            right = mid
        else:
            left = mid + 1
    
    return left
left: —
mid: —
right: —
k: —
subarrays: —
sum: —
7
0
2
1
5
2
10
3
8
4

Binary search on the answer: find the minimum possible largest subarray sum

0 / 42

1x
Solution
The algorithm combines binary search with a greedy feasibility check:
Initialize bounds: left = max(nums), right = sum(nums)
Binary search: While left < right
Calculate mid = (left + right) / 2
Use the greedy helper to check if we can split with max sum ≤ mid
If yes: answer might be smaller, set right = mid
If no: answer must be larger, set left = mid + 1
Return left as the answer
The greedy check runs in O(n) time, and binary search runs O(log(sum - max)) iterations, giving us O(n * log(sum)) total time complexity.
What is the time complexity of this solution?
1

O(1)

2

O(n * log(sum))

3

O(n)

4

O(n³)

When to Use Binary Search on Answer
This technique applies when:
The answer lies within a known range [lo, hi]
There's a monotonic predicate: if answer x is feasible, then all values > x (or < x) are also feasible
You can efficiently check if a given candidate is feasible
Common problems using this pattern:
Minimize the maximum (or maximize the minimum) of something
Capacity/allocation problems
"Can we do X with budget Y?" questions
When you see "minimize the maximum" or "maximize the minimum", consider binary search on the answer. The key is identifying the monotonic property and designing an efficient feasibility check.

Mark as read

Next: Kth Smallest Element in a Sorted Matrix

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

(6)

Comment
Anonymous
HD
HARDIK DADHICH
Premium
• 27 days ago

well, I didn't intuitively came with the lowest boundary could be max(nums).
example above  : Minimum possible: At least max(nums) = 10.
Tried a long to understand this :

is it due to in positive numbers of array ex : [1,2,3,4]  if we try to split it at least in 1 part then in among those part the maximum sum is always the max number ?
ex : [1,2,3] --> sum(6) ,  [4] --> sum(4) , shouldn't the min value of subarray we should take min(nums) ?

1

Reply
F
ForeignBronzeFelidae167
Premium
• 16 days ago

public Integer splitArray(int[] nums, Integer k) {
int start=0;
int sum=0;
for (int x=0; x<nums.length; x++) {
sum+=nums[x];
start=Math.max(start, nums[x]);
}
int ans=Integer.MAX_VALUE;
// At-least start amt. of work every worker should have.
while (start<=sum) {
int mid=(start+sum)/2;
// Assign at-least mid quantities to each worker.
int assignedQty=0;
int workersCovered=1;
for (int i=0; i<nums.length; i++) {
// if (nums[i]>mid) {
//     break;
//}
if (nums[i]+assignedQty<=mid) {
assignedQty+=nums[i];
} else {
assignedQty=nums[i];
workersCovered++;
}
} // ends for loop.
if (workersCovered<=k) {
ans=Math.min(ans, mid);
sum=mid-1;
} else if (workersCovered>k) {
start=mid+1;
}
} // ends while loop.
return ans;
}

Show More

0

Reply
M
ModestAquaWildfowl918
Premium
• 1 month ago

Just to be sure I understood the problem right, for the example 2:

Input:
nums = [6, 3, 9, 2, 1, 8], k = 2

Output: 18

Explanation: Split into [6, 3, 9] (sum=18) and [2, 1, 8] (sum=11). The heaviest workload is 18. Any other split with 2 groups results in a higher maximum.

However, if we split into [2, 9, 3] (sum=14) and [6, 1, 8] (sum = 15). We end up with a smaller maximum of 15.

0

Reply
E
EssentialAmberCondor519
Premium
• 1 month ago

Each subarray has to be contiguous. From the problem description: Tasks are assigned to the workers as contiguous blocks.

0

Reply
Joel Wang
Premium
• 1 month ago

Very interesting problem.

class Solution:
    def splitArray(self, nums: List[int], k: int):
        n = len(nums)

        def qualified(target):
            """If it's possible to find groups <= k that any sum(group) <= target"""
            groups = 0
            curr_sum = 0
            for i in range(n):
                if curr_sum + nums[i] > target:
                    curr_sum = nums[i]
                    groups += 1
                else:
                    curr_sum += nums[i]
            
            # add the last group
            groups += 1
            
            return groups <= k
        
        left, right = max(nums), sum(nums)
        res = right
        while left <= right:
            mid = (left + right) // 2
            if qualified(mid):
                res = mid
                right = mid - 1
            else:
                left = mid + 1
        
        return res

Show More

0

Reply
fz zy
Premium
• 2 months ago
class Solution:
    def splitArray(self, nums: List[int], k: int):
        def findNSplit(val):
            cnt, curr = 0, 0
            for i in range(len(nums) - 1):
                curr += nums[i]
                if curr + nums[i + 1] > val:
                    cnt += 1
                    curr = 0
            return 1 + cnt
        
        left, right = max(nums), sum(nums)
        while left <= right:
            mid = (left + right) >> 1
            n = findNSplit(mid)
            if n <= k:
                right = mid - 1
            else:
                left = mid + 1
        return left
Show More

0

Reply
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Understanding the Problem

Key Observation: The Answer Has Bounds

Why Binary Search?

The Binary Search Algorithm

The Feasibility Check (Helper Function)

Walkthrough

Visualization

Solution

When to Use Binary Search on Answer
