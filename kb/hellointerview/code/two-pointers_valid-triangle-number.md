# Triangle Numbers

> Source: https://www.hellointerview.com/learn/code/two-pointers/valid-triangle-number
> Scraped: 2026-03-30


Two Pointers
Triangle Numbers
medium
DESCRIPTION (inspired by Leetcode.com)

Write a function to count the number of triplets in an integer array nums that could form the sides of a triangle.

For three sides to form a valid triangle, all three of these conditions must hold: (a + b > c), (a + c > b), and (b + c > a), where (a), (b), and (c) are the side lengths. In other words, the sum of every possible pair must exceed the third side.

a
b
c
Valid triangle requires:
a + b > c AND a + c > b AND b + c > a
(every pair must sum to more than the third side)

The triplets do not need to be unique.

Example:

Input:

nums = [11,4,9,6,15,18]

Output:

10

Explanation: Valid combinations are...

4, 15, 18
6, 15, 18
9, 15, 18
11, 15, 18
9, 11, 18
6, 11, 15
9, 11, 15
4, 6, 9     
CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def triangleNumber(self, nums: List[int]) -> int:
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
comma-separated integers
Try these examples:
No Triangle
Small Case
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def triangleNumber(nums):
    nums.sort()
    
    count = 0
    for i in range(len(nums) - 1, 1, -1):
        left = 0
        right = i - 1
        while left < right:
            if nums[left] + nums[right] > nums[i]:
                count += right - left
                right -= 1
            else:
                left += 1
    
    return count
11
4
9
6
15
18

valid triangle numbers

0 / 26

1x
Explanation
For three sides to form a valid triangle, all three of these conditions must be true:
(a + b > c)
(a + c > b)
(b + c > a)
where (a), (b), and (c) are the three side lengths. This means the sum of every possible pair of sides must exceed the remaining side. For example, sides [1, 2, 1000] do NOT form a valid triangle because while (2 + 1000 > 1), the condition (1 + 2 > 1000) fails. By sorting the array, we can leverage the two-pointer technique to count all valid triplets in O(n2) time and O(1) space.
The key to this question is realizing that if we sort three numbers from smallest to largest (say a ≤ b ≤ c), we only need to check if a + b > c. If this condition holds, the other two conditions (a + c > b and b + c > a) are automatically satisfied because c ≥ b and b ≥ a. For example, with 4, 8, 9, if 4 + 8 > 9 is true, then we have a valid triplet.
4
8
9
But not only that, triplets where the smallest number is between 4 and 8 are also valid triplets.
4
5
6
7
8
8
9
This means that if we sort the input array, and then iterate from the end of the array to the beginning, we can use the two-pointer technique to efficiently count all valid triplets.
11
4
9
6
15
18
The pointers i, left, and right represent the current triplet we are considering. If nums[left] + nums[right] > nums[i], then we know there are a total of right - left valid triplets, since all triplets between left and right are also valid triplets. We can then decrement right to check for the valid triplets that can be made by decreasing the middle value.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def triangleNumber(nums):
    nums.sort()
    
    count = 0
    for i in range(len(nums) - 1, 1, -1):
        left = 0
        right = i - 1
        while left < right:
            if nums[left] + nums[right] > nums[i]:
                count += right - left
                right -= 1
            else:
                left += 1
    
    return count
11
4
9
6
15
18

valid triangle numbers

0 / 5

1x
When nums[left] + nums[right] < nums[i], we know that all triplets between left and right are also invalid, so we increment left to look for a larger smallest value.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def triangleNumber(nums):
    nums.sort()
    
    count = 0
    for i in range(len(nums) - 1, 1, -1):
        left = 0
        right = i - 1
        while left < right:
            if nums[left] + nums[right] > nums[i]:
                count += right - left
                right -= 1
            else:
                left += 1
    
    return count
11
4
9
6
15
18
i
left
right
Count:
4

move right pointer

0 / 1

1x
Each time left and right cross, we decrement i and reset left and right to their positions at opposite ends of the array. This happens until i is less than 2, at which point we have counted all valid triplets.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def triangleNumber(nums):
    nums.sort()
    
    count = 0
    for i in range(len(nums) - 1, 1, -1):
        left = 0
        right = i - 1
        while left < right:
            if nums[left] + nums[right] > nums[i]:
                count += right - left
                right -= 1
            else:
                left += 1
    
    return count
11
4
9
6
15
18
i
left
right
Count:
4

move left pointer

0 / 20

1x

Mark as read

Next: Move Zeroes

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

(41)

Comment
Anonymous
​
Sort By
Popular
Sort By
Sean Tarzy
Top 5%
• 1 year ago

when you say
The pointers i, left, and right represent the current triplet we are considering. If nums[i] + nums[left] >= nums[right], then we know there are a total of right - left valid triplets, since all triplets between left and right are also valid triplets.
do you mean nums[left] + nums[right] > nums[i]  ? (technically i would be the rightmost index so i think that's why it's kind of confusing)

13

Reply
Benjamin Clark
• 7 months ago

Ya. i think it's a typo.
should be nums[left] + nums[right] > nums[i]

2

Reply
Harshit Tripathi
• 1 year ago

If nums[i] + nums[left] >= nums[right], then we know there are a total of right - left valid triplets, since all triplets between left and right are also valid triplets. We can then decrement typo here should be nums[left]+nums[right]>nums[i]

5

Reply
Erick Mwazonga
• 7 months ago

Good illustration;
I see the solution fixes the largest side and proactively finds the other 2 smaller sides. Using the same technique, can we fix the smallest side and proactively find the other 2 sides?

3

Reply
R
ryan
• 4 months ago

No. Because if you fix the smallest side 'a' then run 2 pointer over 'b' and 'c', if a + b <= c you don't know if incrementing b so that it is bigger or decrementing c so that it's smaller is the correct choice. When you fix the largest side as a, then if b + c <= a, you know that no matter what you do to c, a will never be valid because we are already at the largest c value, so you have to increment a. And when b + c > a, you know that since that c value worked, you should try smaller ones so you decrement it.

7

Reply
Colin Lankau
• 9 months ago

Here is my solution that does not traverse backwards through the array

class Solution:
    def triangleNumber(self, heights: list[int]):
        heights.sort()
        numTriplets = 0
        for i in range(len(heights)-2):
            left, right = i+1, len(heights)-1
            while left < right:
                target = heights[right] - heights[i]
                numTriplets += len([h for h in heights[i+1:right] if h > target])
                right -= 1
        return numTriplets

3

Reply
Prateik D
Premium
• 7 days ago

not efficient though.

0

Reply
T
TenderBronzeFlea698
Premium
• 27 days ago

Time complexity of this is O(n³)

0

Reply
M
madhuradole
Premium
• 7 months ago

Feedback to the Author:

In the first step of the solution, the text says: "If nums[i] + nums[left] > nums[right], then we know there are a total of right - left valid triplets"

This should be: nums[left] + nums[right] > nums[i]

Same for the second step as well: When nums[i] + nums[left] < nums[right], we know that all triplets between left and right are also invalid

This should be: nums[left] + nums[right] < nums[i]

Thank you for the great walkthrough, this is very helpful!

2

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Solution

Explanation
