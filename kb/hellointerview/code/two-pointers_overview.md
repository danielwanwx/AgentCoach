# Two-Pointer Overview

> Source: https://www.hellointerview.com/learn/code/two-pointers/overview
> Scraped: 2026-03-30

Two-Pointer Overview
2:51
7 chapters • 1 interactive checkpoints
This technique refers to using two pointers that start at opposite ends of an array and gradually move towards each other.
1
3
4
6
8
10
13
left
right
In this page, we'll cover:
A simple problem that illustrates the motivation behind the two-pointer technique.
The types of problem for which you should consider using this technique.
A list of problems (with animated solutions!) for you to try that build upon the concepts covered here.
Problem: Two Sum
DESCRIPTION
Given a sorted array of integers nums, determine if there exists a pair of numbers that sum to a given target.
Example:
Input: nums = [1,3,4,6,8,10,13], target = 13
Output: True (3 + 10 = 13)
Input: nums = [1,3,4,6,8,10,13], target = 6
Output: False
The naive approach to this problem uses two-pointers i and j in a nested for-loop to consider each pair in the input array, for a total of O(n2) pairs considered.
nums
​
|
nums
comma-separated integers
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
def isPairSum(nums, target):
  for i in range(len(nums)):
    for j in range(i + 1, len(nums)):
      if nums[i] + nums[j] == target:
        return True
  return False
1
3
4
6
8
10
13

two sum naive

0 / 11

1x
However, if we put a bit more thought into how we initialize our pointers and how we move them, we can eliminate the number of pairs we consider down to O(n). Understanding why we are able to eliminate pairs is key to understanding the two-pointer technique.
1
3
4
6
8
10
13
i
j
1
3
4
6
8
10
13
i
j
1
3
4
6
8
10
13
i
j
1
3
4
6
8
10
13
i
j
1
3
4
6
8
10
13
i
j
1
3
4
6
8
10
13
i
j
1
3
4
6
8
10
13
i
j
1
3
4
6
8
10
13
i
j
1
3
4
6
8
10
13
i
j
1
3
4
6
8
10
13
i
j
13
1
3
4
6
8
10
13
left
right
1
3
4
6
8
10
13
left
right
1
3
4
6
8
10
13
left
right
13
Naive (left) vs. Two-Pointer Technique (right)
Eliminating Pairs
The two-pointer technique leverages the fact that the input array is sorted.
Let's use it to solve the Two Sum problem when nums = [1, 3, 4, 6, 8, 10, 13] and target = 13.
1
3
4
6
8
10
13
Goal: find this pair of numbers that sum to 13
We start by initializing two pointers at opposite ends of the array, which represent the pair of numbers we are currently considering.
1
3
4
6
8
10
13
This pair has a sum (14) that is greater than our target (13). And because our array is sorted, all other pairs ending at our right pointer (13) also have sums greater than our target, as they all involve numbers greater than 1, the value at our left pointer.
1
3
4
6
8
10
13
left
right
So, to move onto the next pair we move our right pointer back, which elimininates those unnecessary pairs from our search.
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
Move right pointer back.
Now, since our sum is less than our target, we know that all other pairs involving our left pointer also have sums less than our target. So, we move our left pointer forward to eliminate those unnecessary pairs and arrive at the next pair to consider.
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
Summary
The two-pointer technique leverages the fact that the input array is sorted to eliminate the number of pairs we consider from O(n2)down to O(n).
The two-pointers start at opposite ends of the array, and represent the pair of numbers we are currently considering.
We repeatedly compare the sum of the current pair to the target, and move a pointer in a way that eliminates unnecessary pairs from our search.
When Do I Use This?
Consider using the two-pointer technique for questions that involve searching for a pair (or more) of items in an array that meet a certain criteria.
Examples:
Finding a pair of items that sum to a given target in an array.
Finding a triplet of items that sum to 0 in a given array.
Finding the maximum amount of water that can be held between two array items representing wall heights.
Practice Problems
Try applying the concepts related to eliminating unnecessary pairs to the following problems:
Done
	
Question
	
Difficulty


	
Container With Most Water
	
Medium


	
3-Sum
	
Medium


	
Triangle Numbers
	
Medium
Bonus: Additional Problems
These problems also use two pointers in an array, but instead, each pointer represents a logical "region" of the array.
Done
	
Question
	
Difficulty


	
Move Zeroes
	
Easy


	
Sort Colors
	
Medium


	
Trapping Rain Water
	
Hard

Mark as read

Next: Container With Most Water

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

(34)

Comment
Anonymous
​
Sort By
Popular
Sort By
Sridhar K
Top 5%
• 1 year ago

Well-written articles, top-class, easy to understand approach, and the visualization is helping me a lot. Thank you, team!

37

Reply
Mahesh Babar
• 1 year ago

Nicely explained.
Graphics make it more effective.
Thanks.

9

Reply
hassan mohagheghian
• 1 year ago

Thank you for fine explaining.

It seems this overview isn't in the menu. Please add this topic in menu below the Two Pointers as Overview to better finding.

4

Reply

Evan King

Admin
• 1 year ago

on it!

4

Reply
A
a.m.bharath
• 5 months ago

Animations and the style of explanation are top-notch - thank you!

3

Reply
sanjay B
• 2 months ago

started grinding this sheets helps a lot

2

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Problem: Two Sum

Eliminating Pairs

Solution

Summary

When Do I Use This?

Practice Problems

Bonus: Additional Problems