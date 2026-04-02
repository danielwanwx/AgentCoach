# Max Sum of Distinct Subarrays Length k

> Source: https://www.hellointerview.com/learn/code/sliding-window/maximum-sum-of-distinct-subarrays-with-length-k
> Scraped: 2026-03-30


Sliding Window
Max Sum of Distinct Subarrays Length k
medium
DESCRIPTION (inspired by Leetcode.com)

Given an integer array nums and an integer k, write a function to identify the highest possible sum of a subarray within nums, where the subarray meets the following criteria: its length is k, and all of its elements are unique. If no such subarray exists, return 0.

Example 1: Input:

nums = [3, 2, 2, 3, 4, 6, 7, 7, -1]
k = 4

Output:

20

Explanation: The subarrays of nums with length 4 are:

[3, 2, 2, 3] # elements 3 and 2 are repeated.
[2, 2, 3, 4] # element 2 is repeated.
[2, 3, 4, 6] # meets the requirements and has a sum of 15.
[3, 4, 6, 7] # meets the requirements and has a sum of 20.
[4, 6, 7, 7] # element 7 is repeated.
[6, 7, 7, -1] # element 7 is repeated.

We return 20 because it is the maximum subarray sum of all the subarrays that meet the conditions.

Example 2: Input:

nums = [5, 5, 5, 5, 5]
k = 3

Output:

0

Explanation: Every subarray of length 3 contains duplicate elements, so no valid subarray exists. Return 0.

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
This solution uses a fixed-length sliding window to iterate over all subarrays of length k in O(n) time and O(k) space. For each subarray of length k, we check if all elements are distinct. If they are, then we compute the sum of the subarray and compare it to the maximum sum we have seen so far, and return the maximum sum at the end.
We represent the state of the current window using two variables:
curr_sum: The sum of all elements in the window.
state: A dictionary mapping each element in the window to the number of times it appears in the window.
We use a for-loop to iterate through each element in nums. For each element, we increment its count in state and add its value to curr_sum. We do this until the window reaches size k:
VISUALIZATION
Hide Code
Python
Language
Full Screen
def maxSum(nums, k):
  max_sum = float("-inf")
  start = 0
  state = {}
  curr_sum = 0

  for end in range(len(nums)):
    curr_sum = curr_sum + nums[end]
    state[nums[end]] = state.get(nums[end], 0) + 1
    
    if end - start + 1 == k:
      if len(state) == k:
        max_sum = max(max_sum, curr_sum)

      curr_sum = curr_sum - nums[start]
      state[nums[start]] = state[nums[start]] - 1
      if state[nums[start]] == 0:
        del state[nums[start]]
      start += 1

  return 0 if max_sum == float("-inf") else max_sum
3
2
2
3
4
6
7
7
-1

max sum distinct subarrays of size k

0 / 5

1x
Expanding window until it reaches size k = 4
Each time the window is of size k, we check if the window contains all distinct elements by comparing the length of state to k (if len(state) == k, then all elements in the window are distinct):
If it is, then we compare curr_sum to max_sum and update max_sum if curr_sum is greater.
We then prepare for the next iteration by contracting the window, which involves decrementing the count of the leftmost element in the window and removing it from state if its count is 0. We also subtract the leftmost element from curr_sum. This allows us to maintain the fixed length of the window.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def maxSum(nums, k):
  max_sum = float("-inf")
  start = 0
  state = {}
  curr_sum = 0

  for end in range(len(nums)):
    curr_sum = curr_sum + nums[end]
    state[nums[end]] = state.get(nums[end], 0) + 1
    
    if end - start + 1 == k:
      if len(state) == k:
        max_sum = max(max_sum, curr_sum)

      curr_sum = curr_sum - nums[start]
      state[nums[start]] = state[nums[start]] - 1
      if state[nums[start]] == 0:
        del state[nums[start]]
      start += 1

  return 0 if max_sum == float("-inf") else max_sum
{3:2, 2:2}
state
3
2
2
3
4
6
7
7
-1
0
max_sum

curr_sum: 10

start: 0 | end: 3

expand window

0 / 4

1x
Expanding and contracting the window until first valid subarray is found
We do this until the window reaches the end of nums and return max_sum at the end.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def maxSum(nums, k):
  max_sum = float("-inf")
  start = 0
  state = {}
  curr_sum = 0

  for end in range(len(nums)):
    curr_sum = curr_sum + nums[end]
    state[nums[end]] = state.get(nums[end], 0) + 1
    
    if end - start + 1 == k:
      if len(state) == k:
        max_sum = max(max_sum, curr_sum)

      curr_sum = curr_sum - nums[start]
      state[nums[start]] = state[nums[start]] - 1
      if state[nums[start]] == 0:
        del state[nums[start]]
      start += 1

  return 0 if max_sum == float("-inf") else max_sum
{2:1, 3:1, 4:1, 6:1}
state
3
2
2
3
4
6
7
7
-1
0
max_sum

curr_sum: 15

start: 2 | end: 5

expand window

0 / 10

1x
Expanding and contracting the window until the end of the array.
Example Input 2
Let's look at an edge case: nums = [5, 5, 5, 5, 5] and k = 3.
At first glance, you might think the answer is 15 (since 5 + 5 + 5 = 15). But remember, the problem asks for the maximum sum of subarrays with distinct elements only.
In this case, every subarray of length 3 contains duplicate elements:
[5, 5, 5] - all three elements are the same (not distinct)
[5, 5, 5] - still all duplicates
[5, 5, 5] - same issue
Since no subarray of length 3 contains all distinct elements, we can't sum any of them. The answer is 0.
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
Duplicates
Distinct Window
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def maxSum(nums, k):
  max_sum = float("-inf")
  start = 0
  state = {}
  curr_sum = 0

  for end in range(len(nums)):
    curr_sum = curr_sum + nums[end]
    state[nums[end]] = state.get(nums[end], 0) + 1
    
    if end - start + 1 == k:
      if len(state) == k:
        max_sum = max(max_sum, curr_sum)

      curr_sum = curr_sum - nums[start]
      state[nums[start]] = state[nums[start]] - 1
      if state[nums[start]] == 0:
        del state[nums[start]]
      start += 1

  return 0 if max_sum == float("-inf") else max_sum
3
2
2
3
4
6
7
7
-1

max sum distinct subarrays of size k

0 / 19

1x

Mark as read

Next: Variable Length Sliding Window

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

(46)

Comment
Anonymous
​
Sort By
Popular
Sort By
shivam sahu
• 1 year ago

More Intuitive for me -

public long maximumSubarraySum(int[] nums, int k) {

    Set<Integer> numSet = new HashSet<>();
    int left=0;
    long sum=0,maxSum=0;
    for(int right=0;right<nums.length;right++){

        while(numSet.contains(nums[right])){
            sum = sum - nums[left];
            numSet.remove(nums[left]);
            left++;
        }

        sum = sum + nums[right];
        numSet.add(nums[right]);

        if( right-left+1 == k ){
            maxSum = Math.max(maxSum,sum);
            sum = sum - nums[left];
            numSet.remove(nums[left]);
            left++;
        }
    } 

    return maxSum; 
}
Show More

16

Reply
D
DustyYellowAardwolf840
Premium
• 1 hour ago

Using set won't catch the case where k = 3 and your array is [0, 1, 2, 1, 1]. It will accept 2, 1, 1 subarray as unique since you would remove 1 from the set?

0

Reply
L
LocalPinkImpala397
Premium
• 2 months ago

using a Set can fail for large k and long nums array

0

Reply
Amit K
Premium
• 9 months ago

Based on the fixed length pattern,

I think this is much easier and understandable to read and follows the same principal you suggested only difference is we use set instead of a map


class Solution {
    maxSum(nums, k) {
        let n = nums.length;
        let set = new Set();

        let end = 0, start = 0;
        let sum = 0;
        let result = 0;
        for (let end = 0; end < n; end += 1) {
            // check to see if the element already exists, keep contracting the window
            while (set.has(nums[end])) {
                set.delete(nums[start]);
                sum -= nums[start];
                start += 1;
            }
            
            // add and put the distinct element onto set
            sum += nums[end];
            set.add(nums[end]);

            // same logic as fixed length window proble,
            if (end - start + 1 === k) {
                // keep track of the result
                result = Math.max(result, sum);

                // prepare for the next window
                sum -= nums[start];
                set.delete(nums[start]);
                start += 1;
            } 
        }

        return result;
    }
}

Appreciate a like if possible

Show More

7

Reply
Alexander Gordon
• 1 year ago

I think you have a minor mistake,
if end - start + 1 == 1: on line 12 -> should be: if end - start + 1 == k;

6

Reply
Jimmy Zhang
Top 5%
• 1 year ago

Thank you!

0

Reply
C
chenyuluforever
Premium
• 2 months ago

Problem should specify that the numbers are positive. Otherwise it would be wrong to assume that  max_sum is 0 at the beginning.

4

Reply
Abhay Singh
Top 1%
• 1 year ago

Java Solution:

class Solution {
    public long maximumSubarraySum(int[] nums, int k) {
        int n = nums.length;

        long ans = 0, sum = 0;

        Map<Integer, Integer> mp = new HashMap<>();
        int i = 0, j = 0;
        while (j < n) {
            mp.put(nums[j], mp.getOrDefault(nums[j], 0) + 1);
            sum += nums[j];

            while (mp.size() < j - i + 1) {
                if (mp.put(nums[i], mp.get(nums[i]) - 1) == 1) {
                    mp.remove(nums[i]);
                }
                sum -= nums[i];
                i++;
            }

            if (j - i + 1 == k) {
                if (mp.size() == k) ans = Math.max(ans, sum);

                if (mp.put(nums[i], mp.get(nums[i]) - 1) == 1) {
                    mp.remove(nums[i]);
                }
                sum -= nums[i];
                i++;
            }

            j++;
        }

        return ans;
    }
}
Show More

4

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

Example Input 2

Solution
