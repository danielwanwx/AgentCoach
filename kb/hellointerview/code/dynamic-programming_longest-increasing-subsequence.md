# Longest Increasing Subsequence

> Source: https://www.hellointerview.com/learn/code/dynamic-programming/longest-increasing-subsequence
> Scraped: 2026-03-30



Antoine Dussarps
Top 10%
• 1 year ago

There is also an aesthetic  O(nLog(n)) solution for this classical problem, using binary search.

15

Reply
Karuna Kukreja
Premium
• 1 month ago
• edited 1 month ago

Here is the explanation for the binary search solution for this problem:

Solution 2: Greedy with Binary Search

Let's construct the idea from following example.

Consider the example nums = [2, 6, 8, 3, 4, 5, 1], let's try to build the increasing subsequences starting with an empty one: sub1 = [].
Let pick the first element, sub1 = [2].
6 is greater than previous number, sub1 = [2, 6]
8 is greater than previous number, sub1 = [2, 6, 8]
3 is less than previous number, we can't extend the subsequence sub1, but we must keep 3 because in the future there may have the longest subsequence start with [2, 3], sub1 = [2, 6, 8], sub2 = [2, 3].
With 4, we can't extend sub1, but we can extend sub2, so sub1 = [2, 6, 8], sub2 = [2, 3, 4].
With 5, we can't extend sub1, but we can extend sub2, so sub1 = [2, 6, 8], sub2 = [2, 3, 4, 5].
With 1, we can't extend neighter sub1 nor sub2, but we need to keep 1, so sub1 = [2, 6, 8], sub2 = [2, 3, 4, 5], sub3 = [1].
Finally, length of longest increase subsequence = len(sub2) = 4.

In the above steps, we need to keep different sub arrays (sub1, sub2..., subk) which causes poor performance. But we notice that we can just keep one sub array, when new number x is not greater than the last element of the subsequence sub, we do binary search to find the smallest element >= x in sub, and replace with number x.

Let's run that example nums = [2, 6, 8, 3, 4, 5, 1] again:
Let pick the first element, sub = [2].
6 is greater than previous number, sub = [2, 6]
8 is greater than previous number, sub = [2, 6, 8]
3 is less than previous number, so we can't extend the subsequence sub. We need to find the smallest number >= 3 in sub, it's 6. Then we overwrite it, now sub = [2, 3, 8].
4 is less than previous number, so we can't extend the subsequence sub. We overwrite 8 by 4, so sub = [2, 3, 4].
5 is greater than previous number, sub = [2, 3, 4, 5].
1 is less than previous number, so we can't extend the subsequence sub. We overwrite 2 by 1, so sub = [1, 3, 4, 5].
Finally, length of longest increase subsequence = len(sub) = 4.
The reason for replacing is -> nums 2, 5, 3, 4. Start dp = [2]. 
See 5 so dp = [2, 5]. 
See 3 so replace 5 with 3 to get dp = [2, 3]. 
See 4 so append to get dp = [2, 3, 4]. 
Length is 3. 
         
 If you had kept 5, dp would be [2, 5], and 4 would not extend it, 
 so you would be stuck at length 2. 
 The replacement does not record the actual sequence. 
 It only preserves the best tails so the final length stays maximal

Code:

class Solution {
    public int lengthOfLIS(int[] nums) {
        if(nums == null || nums.length == 0) {
            return 0;
        }
        List<Integer> sub = new ArrayList();
        sub.add(nums[0]);
        
        for(int i= 1; i< nums.length;i++) {
            if(nums[i] <= sub.get(sub.size() - 1)) {
                int index = Collections.binarySearch(sub, nums[i]);
                if(index < 0) {
                    index = -(index + 1);
                }
                sub.set(index, nums[i]);
            } else {
                sub.add(nums[i]); 
            }
        }
        return sub.size();
    }
}
Show More

4

Reply
Daniel Kim
Premium
• 1 month ago

Java solution using binary search O(nlogn) time complexity:

public Integer longest_increasing_subsequence(int[] nums) {
        if(nums == null || nums.length == 0) {
            return 0;
        }

        List<Integer> ans = new ArrayList();
        ans.add(nums[0]);
        for(int i = 1; i < nums.length; i++) {
            if(nums[i] > ans.get(ans.size()-1)) {
                ans.add(nums[i]);
            } else {
                int index = Collections.binarySearch(ans, nums[i]);
                if(index < 0) {
                    index = -(index + 1);
                }
                ans.set(index, nums[i]);
            }
        }
        return ans.size();
    }
Show More

2

Reply
Subarna Lamsal
Premium
• 9 months ago

res = []
for n in nums:
idx = bisect_left(res,n)
if idx == len(res):
res.append(n)
else:
res[idx] = n
return len(res)

2

Reply
Nisal Perera
• 1 year ago

correction

This is because the i-th element can extend the increasing subsequence ending at the j-th element by 1.

should be

This is because the j-th element can extend the increasing subsequence ending at the i-th element by 1.

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

