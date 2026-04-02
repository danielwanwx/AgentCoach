# Two Sum (Sorted Array)

> Source: https://www.hellointerview.com/learn/code/two-pointers/two-sum
> Scraped: 2026-03-30


Two Pointers
Two Sum (Sorted Array)
medium
DESCRIPTION (inspired by Leetcode.com)

Given a sorted array of integers nums, determine if there exists a pair of numbers that sum to a given target.

Example 1:

Input:

nums = [1,3,4,6,8,10,13]
target = 13

Output:

True # (3 + 10 = 13)

Example 2:

Input:

nums = [1,3,4,6,8,10,13]
target = 6

Output:

False
CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def twoSum(self, nums: List[int], target: int) -> bool:
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

Solution
nums
​
|
nums
sorted, comma-separated integers
target
​
|
target
integer
Try these examples:
Has Pair
No Pair
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def twoSum(nums, target):
  left, right = 0, len(nums) - 1
      
  while left < right:
    current_sum = nums[left] + nums[right]
    if current_sum == target:
        return True

    if current_sum < target:
        left += 1
    else:
        right -= 1
      
  return False
1
3
4
6
8
10
13

two sum algorithm

0 / 7

1x
Explanation
Because the input is sorted, we can solve this question in O(n) time and O(1) space using the two-pointer technique by eliminating unnecessary pairs from our search.
Let's say we want to find a pair of numbers that sum to 13 in the following array:
1
3
4
6
8
10
13
We start by initializing two pointers at opposite ends of the array, which represent the pair of numbers we are currently considering. Note that this pair has a sum (14) that is greater than our target (13). Starting at opposite ends lets us efficiently adjust: moving left right increases the sum, while moving right left decreases it.
1
3
4
6
8
10
13
Because our array is sorted, all other pairs using 13 (the element at our right pointer) also have sums greater than our target, as they all use numbers greater than 1 (the element at our left pointer).
1
3
4
6
8
10
13
left
right
So, we move our right pointer back, which elimininates those unnecessary pairs from our search, and arrive at the next pair to consider.
1
3
4
6
8
10
13
left
right
16
17
19
21
23
Now, since our sum is less than our target, we know that all other pairs using 1 also have sums less than our target. So, we move our left pointer forward to eliminate those unnecessary pairs and arrive at the next pair to consider.
1
3
4
6
8
10
13
left
right
This continues until either our pointers meet (in which case we did not find a successful pair) or until we find a pair that sums to our target, like we did here.
1
3
4
6
8
10
13
left
right
Summary
We initialize our two pointers at opposite ends of the array, and start our search.
If the sum of the current pair is greater than our target, we move our right pointer back. If it is less than our target, we move our left pointer forward.
Each time we move a pointer, we eliminate unnecessary pairs from our search.
We continue this process until either our pointers meet or until we find a pair that sums to our target.
While this question is on the easier side for many coding interviews, it's a key step in harder questions such as 3Sum and 3Sum closest, which start by sorting an unsorted array in order to use the two-pointer technique described here.

Mark as read

Next: 3-Sum

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

(24)

Comment
Anonymous
​
Sort By
Popular
Sort By
S
SophisticatedWhiteJellyfish172
• 6 months ago

we can also use map

func twoSum(nums []int, target int) bool {
    m := make(map[int]int)

    for i, v := range nums {
        _, ok2 := m[target-v]

        if ok2 {
            return true
        }

        _, ok := m[v]
        if !ok {
            m[v] = i
        } 
    }

    return false
}
Show More

4

Reply
אור סהר
• 5 months ago

This solution requires extra memory that isn't needed. If the array wasn't sorted, I would go with your approach...

15

Reply
MR
Marwan Radwan
• 1 month ago

Only if the array wasn't sorted that would help !

0

Reply
V
VoluntaryCrimsonBear999
Premium
• 1 month ago

This uses extra memory. Since we have to only return a boolean rather that the pair of numbers summing upto the target, a Two-Pointer approach would be more efficient.

0

Reply
RR
Premium
• 4 months ago

If the input array is already sorted, we can use the classic two-pointer pattern to check whether any pair sums up to the target. Start one pointer at the beginning and the other at the end:

If nums[left] + nums[right] is too small → move left forward

If it's too big → move right backward

If it matches → return true

This gives an O(n) solution without extra space.

class Solution {
public:
    bool twoSum(vector<int>& nums, int target) {
        int left = 0;
        int right = nums.size() - 1;

        while (left < right) {
            int sum = nums[left] + nums[right];

            if (sum == target)
                return true;
            else if (sum < target)
                left++;
            else
                right--;
        }
        return false;
    }
};

Time complexity: O(n)
Space: O(1)

Show More

2

Reply
Bhumi Bhatt
• 2 months ago

I did the same. or hashmap for unsorted.

2

Reply
aditya patel
Premium
• 28 days ago
• edited 28 days ago

js solution:

function twoSum(nums: number[], target: number): number[] {
    const len =  nums.length;

    let left = 0, right = len - 1;

    while(left < right) {
        const val1 = nums[left];
        const val2 = nums[right];
        const sum = val1 + val2;

        if(target === sum) {
            return [left + 1, right + 1];
        } else if(target < sum){
            right--;
        } else {
            left++;
        }
    }

    return [-1, -1];
};
Show More

1

Reply
Kaushik Ramabhotla
• 1 month ago

C# solution

public class Solution {
    public bool twoSum(int[] nums, int target) {
        // Your code goes here
        if(nums == null) return false;
        int n= nums.Length;
        if(n < 2) return false;
        int l=0, r = n-1;

        while(l < r)
        {
            int sum = nums[l] + nums[r];
            if(sum == target) return true;
            else if(sum > target) r--;
            else l++;
        }
        return false;
    }
}
Show More

1

Reply
Belka h.j
Premium
• 2 months ago

Pretty sure it isn't a medium difficulty.
Two Sum is literally one of the easier problems and a must-know.

1

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Solution

Explanation

Summary
