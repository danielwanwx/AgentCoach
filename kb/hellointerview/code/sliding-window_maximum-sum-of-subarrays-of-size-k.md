# Maximum Sum of Subarrays of Size K

> Source: https://www.hellointerview.com/learn/code/sliding-window/maximum-sum-of-subarrays-of-size-k
> Scraped: 2026-03-30


Sliding Window
Maximum Sum of Subarrays of Size K
easy
DESCRIPTION

Given an array of integers nums and an integer k, find the maximum sum of any contiguous subarray of size k.

Example 1: Input:

nums = [2, 1, 5, 1, 3, 2]
k = 3

Output:

9

Explanation: The subarray with the maximum sum is [5, 1, 3] with a sum of 9.

CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def maxSum(self, nums: List[int], k: int) -> int:
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
This problem uses a fixed-size sliding window to efficiently find the maximum sum among all subarrays of length k. Instead of recalculating the sum for each subarray from scratch, we slide the window across the array and update the sum incrementally.
This approach is efficient because we calculate each window's sum in constant time by:
Adding the new element entering the window (nums[end])
Subtracting the old element leaving the window (nums[start])
Instead of summing k elements for each window (which would be O(n*k)), we do constant work per window, giving us O(n) time complexity.
Solution
nums
​
|
nums
comma-separated integers
k
​
|
k
integer
Try these examples:
Small
Larger
Reset
VISUALIZATION
Python
Language
Full Screen
def max_subarray_sum(nums, k):
  max_sum = float('-inf')
  state = 0
  start = 0

  for end in range(len(nums)):
    state += nums[end]

    if end - start + 1 == k:
      max_sum = max(max_sum, state)
      state -= nums[start]
      start += 1

  return max_sum
2
1
5
1
3
2

max subarray sum of size k

0 / 16

1x

Mark as read

Next: Max Points You Can Obtain From Cards

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
S
selectfromall
Top 5%
• 1 year ago

AI feedback thinks that the problem is https://leetcode.com/problems/maximum-sum-of-distinct-subarrays-with-length-k when evaluating the solution, which is a harder variation of this problem.

19

Reply
Allen Liu (Hsin-tzu)
Top 5%
• 8 months ago
    def maxSum(self, nums: List[int], k: int):
        ans = cur = sum(nums[:k])
        for i in range(k, len(nums)):
            cur += nums[i] - nums[i - k]
            ans = max(ans, cur)
        return ans

5

Reply
H
HuskyCrimsonOrca275
• 4 months ago

That is more simple, but heads up, your version uses O(k) memory on the slice nums[:k] part, where the optimal solution uses O(1).

cur = sum(nums[i] for i in range(k)) is better.

4

Reply
R
RobustFuchsiaCrocodile893
Premium
• 7 months ago

This was my intuition too. get the sum of the first k elements, then loop over the rest and add the current element, subtract the starting previous one, compare which sum was larger. O(n) solution

2

Reply
K
KeenSilverBobolink836
Premium
• 9 months ago

AI is thinking k should be distinct element count:

class Solution:
    def maxSum(self, nums: list[int], k: int):
        max_sum = 0
        current_sum = 0
        start = 0
        seen = set()

        for end in range(len(nums)):
            while nums[end] in seen:
                seen.remove(nums[start])
                current_sum -= nums[start]
                start += 1

            seen.add(nums[end])
            current_sum += nums[end]

            if end - start + 1 == k:
                max_sum = max(max_sum, current_sum)
                seen.remove(nums[start])
                current_sum -= nums[start]
                start += 1

        return max_sum
Show More

2

Reply
Charles Mr
Premium
• 1 month ago

simple python implementation

class Solution:
    def maxSum(self, nums: List[int], k: int):
        start = 0
        state = 0
        window_max = -float('inf')

        for i in range(len(nums)):
            state += nums[i]

            if i - start + 1 == k:
                window_max = max(window_max, state)
                state -= nums[start]
                start += 1
            else:
                i += 1
        return window_max

1

Reply
B
Bruk
• 1 month ago
• edited 1 month ago

The code works, but it is wrong. Incrementing i in the else block is useless since the for loop uses an internal counter. The loop automatically assigns the next value from the range which overrides the manually assigned value of i in the code. Check its effect with a debugging tool.

0

Reply
Akshay Borude
• 6 days ago

I think this is somewhat better and intuitive:

public class Solution {
    public Integer maxSum(int[] nums, Integer k) {
        int max = Integer.MIN_VALUE;
        int sum = 0;
        for(int i = 0 ; i <= nums.length-k; i++){
            sum = 0;
            for(int j = 0; j < k; j++){
                sum+= nums[i+j];
            }
            max = Math.max(max, sum);
        }
        return max;
    }
}

0

Reply
E
elapidae
Premium
• 2 days ago

This is O(n*k).

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
