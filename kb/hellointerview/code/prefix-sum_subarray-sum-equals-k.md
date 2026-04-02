# Subarray Sum Equals K

> Source: https://www.hellointerview.com/learn/code/prefix-sum/subarray-sum-equals-k
> Scraped: 2026-03-30


Write a function that returns the total number of contiguous subarrays within a given integer array whose elements sum up to a target K.

Example 1: Input:

nums = [3, 4, 7, 2, -3, 1, 4, 2]
k = 7

Output: 4

Explanation: The subarrays that sum to 7 are:

[3, 4], [7], [7, 2, -3, 1], [1, 4, 2]

Example 2: Input:

nums = [1, -1, 0]
k = 0

Output: 3

Explanation: The subarrays that sum to 0 are:

[-1, 1], [0], [1, -1, 0]
CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
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
We can solve this question efficiently by leveraging the Prefix-Sum technique.
Let's start by visualizing the role that the prefix sum plays in this solving this problem. Let's say I have the following array:
3
2
-1
2
-3
1
0
1
2
3
4
5
I also have the sum of all the elements starting from the beginning of the array up to index 3 (arr[0] + arr[1] + arr[2] + arr[3]) stored in a variable sum_.
sum_
6
3
2
-1
2
-3
1
0
1
2
3
4
5
I also have the prefix sums of all the elements up to index 2 stored in an array called prefix:
sum_
6
3
2
-1
2
-3
1
0
1
2
3
4
5
0
3
5
4
​arr[0] + arr[1] + arr[2]
0
1
2
3
prefix
nums
When looking at these visuals, recall that prefix[i] contains the prefix sum of all elements up to i - 1 in the array.
prefix[i] = arr[0] + arr[1] + ... + arr[i - 1]
Each of the values in the prefix_sum array tells us about the sum of all the different subarrays tha ends at index 3:
For example, let's look at prefix[1], which is 3, but we'll refer to as x for now. From this, we can tell that there exists a subarray ending at index 3 that has a sum of sum_ - x (6 - 3 = 3):
x
x
3
2
-1
2
-3
1
0
1
2
3
4
5
0
3
5
4
0
1
2
3
prefix
nums
sum - x
3
This applies to each value in prefix:
x
3
2
-1
2
-3
1
0
1
2
3
4
5
0
3
5
4
0
1
2
3
prefix
nums
sum - x
6
x
5
x
3
2
-1
2
-3
1
0
1
2
3
4
5
0
3
5
4
0
1
2
3
prefix
nums
sum - x
1
sum - x
x
3
2
-1
2
-3
1
0
1
2
3
4
5
0
3
5
4
0
1
2
3
prefix
nums
x
4
To recap, if we have:
a value sum_ that contains the prefix sum of the array up to index i
another value x that is the prefix sum of the array up to index j (where j comes before i)
then there exists a subarray ending at i with sum sum_ - x.
We'll use this fact to solve our problem.
Counting Subarrays with Sum K
The question is asking for the number of distinct subarrays that sum to k. So we can turn our prefix array into a dictionary mapping each prefix sum to the number of times it has been seen.
{ -2:1, 0:1, 1:1, 2:2, 4:1, 7: 1 }
2
-1
-3
4
2
3
0
1
2
3
4
5
prefix_counts
nums
prefix
0
2
1
-2
2
7
4
The prefix_counts dictionary maps each value in prefix to the number of times it appears in the array.
Now, we can use this dictionary to count the number of subarrays that sum to k that end at each index in the array.
Recall from above, we can calculate the sum of any subarray ending at index j by using the difference of prefix sums: if the current prefix sum up to index j is sum_, and there was an earlier prefix sum prev_sum at some index before j, then the subarray sum between them is sum_ - prev_sum.
This means that to find a subarray that sums to k ending at the current index (with prefix sum sum_), we need to find a previous prefix sum equal to sum_ - k in the prefix_counts dictionary. More importantly, the number of subarrays that sum to k that end at index i is equal to prefix_counts[sum_ - k].
Here's a visual to help us understand this better:
For example, let's say we have the array below and we are interested in finding the number of subarrays that sum to k = 5. At index 5, we have sum_ = 7
{ -2:1, 0:1, 1:1, 2:2, 4:1, 7: 1 }
2
-1
-3
4
2
3
0
1
2
3
4
5
prefix_counts
nums
sum
7
Since we are looking for subarrays that sum to k = 5 and end at index 5, this is equivalent to finding a prefix sum sum_ such that sum_ - k = 7 - 5 = 2. The prefix_counts dictionary tells us that there are 2 of these prefix sums, so there are 2 subarrays that sum to k = 5 and end at index 5:
{ -2:1, 0:1, 1:1, 2:2, 4:1, 7: 1 }
2
-1
-3
4
2
3
0
1
2
3
4
5
prefix_counts
nums
sum
7
The two subarrays that sum to 5 and end at index 5 are underlined in green.
Solution
At a high level, our solution will iterate over each element in the array and calculate the number of subarrays that sum to k that end at that index using the approach outlined above. We will keep track of the total number of subarrays that sum to k as we iterate over the array, and return it at the end.
initialize a prefix_counts dictionary with a single entry 0: 1. The entry 0: 1 represents that an empty subarray sums to 0, which lets us correctly account for subarrays that start at index 0 and sum to k. The values in the dictionary represent the number of times we have seen a particular prefix sum as we iterate.
initialize sum_ to 0 and count to 0. sum_ represents the prefix sum up to the current index, and count represents the total number of subarrays that sum to k.
iterate over the array, updating sum_ and count as follows:
update sum_ by adding the current element to it.
calculate the number of subarrays that sum to k that end at the current index by looking up prefix_counts[sum_ - k] and adding it to count.
update the prefix_counts dictionary by incrementing the count of sum_ by 1.
SOLUTION
Python
Language

class Solution:
    def subarraySum(self, nums, k):
        count = 0
        sum_ = 0
        prefix_counts = {0: 1}

        for num in nums:
            sum_ += num
            if sum_ - k in prefix_counts:
                count += prefix_counts[sum_ - k]

            # update the seen prefix sum counts
            prefix_counts[sum_] = prefix_counts.get(sum_, 0) + 1

        return count

What is the time complexity of this solution?
1

O(m * n * 4^L)

2

O(log n)

3

O(n)

4

O(V + E)

Mark as read

Next: Spiral Matrix

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

(12)

Comment
Anonymous
​
Sort By
Popular
Sort By
Mayank Kumar
Premium
• 2 months ago

If you have done the classic problem of sum of two numbers equal to k or slightly modified version count of number of two elements in the array whose count is equal to k, for solving this problem you just need to find the number of prefixSum sum difference equal to k

Classic Two-Sum Problem

arr[i] + arr[j] = k
arr[i] = k - arr[j]

Use a map to store elements seen so far and check for k - current → standard two-sum logic.

Subarray Sum Equals k Problem
prefixSum[j+1] - prefixSum[i] = k
prefixSum[i] = prefixSum[j+1] - k

✅ This is exactly like two-sum:
prefixSum[j+1] → current element
prefixSum[i] → previous element we need
Map stores all previous prefix sums with their frequency
For each prefix sum, count += map.getOrDefault(currentSum - k, 0)

Show More

3

Reply
Mayank Kumar
Premium
• 2 months ago
import java.util.*;

class Solution {
    public int subarraySum(int[] nums, int k) {
        int n = nums.length;
        
        // Step 1: Build the prefix sum array
        int[] prefix = new int[n + 1];
        prefix[0] = 0;
        for (int i = 0; i < n; i++) {
            prefix[i + 1] = prefix[i] + nums[i];
        }

        // Step 2: Use a map to solve like two-sum on prefix sums
        Map<Integer, Integer> map = new HashMap<>();
        map.put(0, 1); // handle subarrays starting at index 0
        int count = 0;

        for (int j = 1; j <= n; j++) {
            int current = prefix[j];
            // Check how many previous prefix sums differ by k
            count += map.getOrDefault(current - k, 0);
            // Add current prefix sum to map
            map.put(current, map.getOrDefault(current, 0) + 1);
        }

        return count;
    }
}

Show More

0

Reply
K
KeenSilverBobolink836
Premium
• 11 months ago

Given example starts with array: 3,2,7,2,-3,1 but changes to 3,2,-1,2,-3,1. Why? Why does 7 change to -1?

3

Reply
E
ElegantGoldMeadowlark796
Premium
• 9 months ago

Yeah I think thats a mistake.. it confused me too

0

Reply
Shivam Chauhan
• 9 months ago

Thanks for pointing this out, it is fixed and will be live after next deployment!

0

Reply
H
HeavyAmaranthCephalopod183
Premium
• 1 year ago

Great content!

This question passes for me with the brute force approach O(n^2) approach. Not sure how frequently this section is used but it could be good to add a test case that causes TLE.

1

Reply
nailyk
Premium
• 1 month ago

typo error:

subarrays tha ends at index 3:

subarrays that* ends...

0

Reply
S
sherry-dash-shower
Premium
• 1 month ago

FYI: The JavaScript editor doesn't support ??, whereas it does for other problems.

0

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

Counting Subarrays with Sum K

Solution
