# Monotonic Stack

> Source: https://www.hellointerview.com/learn/code/stack/monotonic-stack
> Scraped: 2026-03-30

Monotonic Stack
A monotonic stack is a special type of stack in which all elements on the stack are sorted in either descending or ascending order. The ordering can be strict (no duplicates allowed) or non-strict (duplicates allowed), which variant you use depends on the problem. In most problems, including the ones below, a non-strict monotonic stack works. It is used to solve problems that require finding the next greater or next smaller element in an array.
73
72
72
68
stack
A monotonically decreasing stack (non-strict i.e. duplicates like 72 are allowed)
Problem: Next Greater Element
DESCRIPTION
Given an array of integers, find the next greater element for each element in the array. The next greater element of an element x is the first element to the right of x that is greater than x. If there is no such element, then the next greater element is -1.
Example
Input: [2, 1, 3, 2, 4, 3]
Output: [3, 3, 4, 4, -1, -1]
The solution iterates over each index in the input array. For each index, it checks if the element at that index is the next greater element for any previous elements in the array. In order to perform that check efficiently, we'll use a monotonic decreasing stack.
Initialization
We start by initializing our stack and our results array, with each value in the results array initialized to -1. Our stack stores the indexes of the elements in the input array that have not yet found their next greater element.
VISUALIZATION
Python
Language
Full Screen
def nextGreaterElement(nums):
  n = len(nums)
  result = [-1] * n
  stack = []

  for i in range(n):
    while stack and nums[i] > nums[stack[-1]]:
      index = stack.pop()
      result[index] = nums[i]
    stack.append(i)

  return result
2
1
3
2
4
3
0
1
2
3
4
5

0 / 1

1x
Iteration
We then iterate over the input array. To check if the current element nums[i] is the next greater element for any of the previous elements in the array, we compare the current element with the element at the index at the top of the stack nums[stack[-1]].
If the stack is empty, or if nums[i] is less than nums[stack[-1]], we push the current index onto the stack.
VISUALIZATION
Python
Language
Full Screen
def nextGreaterElement(nums):
  n = len(nums)
  result = [-1] * n
  stack = []

  for i in range(n):
    while stack and nums[i] > nums[stack[-1]]:
      index = stack.pop()
      result[index] = nums[i]
    stack.append(i)

  return result
2
1
3
2
4
3
0
1
2
3
4
5
-1
-1
-1
-1
-1
-1
result
stack

0 / 4

1x
Pushing indexes 0 and 1 onto the stack
Recall that the stack contains the indexes of the elements in the input array that have not yet found their next greater element. At this point, we can see that the values at each of the indexes on the stack (i.e. nums[0] and nums[1]) are monotonically decreasing. This property allows us to check if nums[i] is the next greater element for any of the indexes on the stack efficiently.
If nums[i] is smaller than nums[stack[-1]], because the stack is monotonically decreasing, we also know that nums[i] is not the next greater element for any of the other indexes on the stack as well, so we can push index i onto the stack.
Processing Next Greater Elements
If the nums[i] is greater than nums[stack[-1]], then we have found the next greater element for the index stack[-1]. So we pop that index from the stack (idx), and update results[idx] to be nums[i].
Because it is still possible for nums[i] to be the next greatest element for the remaining indexes on the stack, we have to repeat this processing operation until nums[i] is not greater than nums[stack[-1]], at which point we have finished processing all the indexes for which nums[i] is the next greatest element, so we push i onto the stack.
VISUALIZATION
Python
Language
Full Screen
def nextGreaterElement(nums):
  n = len(nums)
  result = [-1] * n
  stack = []

  for i in range(n):
    while stack and nums[i] > nums[stack[-1]]:
      index = stack.pop()
      result[index] = nums[i]
    stack.append(i)

  return result
2
1
3
2
4
3
0
1
2
3
4
5
i
-1
-1
-1
-1
-1
-1
result
0
1
stack

0 / 4

1x
Processing indexes for which 3 is the next greatest element
Popping all the elements that are smaller than nums[i] from the stack before pushing i ensures that the stack stays monotonically decreasing.
This process continues until the end of the input array, at which point the results array contains the next greater element for each element in the input array, or -1 if there is no such element.
Solution
nums
​
|
nums
list of integers
Try these examples:
Decreasing
Mixed
Reset
VISUALIZATION
Python
Language
Full Screen
def nextGreaterElement(nums):
  n = len(nums)
  result = [-1] * n
  stack = []

  for i in range(n):
    while stack and nums[i] > nums[stack[-1]]:
      index = stack.pop()
      result[index] = nums[i]
    stack.append(i)

  return result
2
1
3
2
4
3
0
1
2
3
4
5

0 / 18

1x
Next Smaller Element
Following the same pattern, we can use a monotonically increasing stack to solve problems that require finding the next smaller element in an array.
nums
​
|
nums
list of integers
Try these examples:
Decreasing
Mixed
Reset
VISUALIZATION
Python
Language
Full Screen
def nextSmallerElement(nums):
  n = len(nums)
  result = [-1] * n
  stack = []

  for i in range(n):
    while stack and nums[i] < nums[stack[-1]]:
      index = stack.pop()
      result[index] = nums[i]
    stack.append(i)

  return result
2
1
3
2
4
3
0
1
2
3
4
5

0 / 17

1x
Practice Problems
For more practice with problems that use a monotonic stack, try:
Daily Temperatures
Leetcode | Solution
Largest Rectangle in Histogram
Leetcode | Solution
Buildings with an Ocean View
Leetcode

Mark as read

Next: Daily Temperatures

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

(9)

Comment
Anonymous
Ratnesh Raghubir Singh Thakur
Top 10%
• 4 months ago

Suggestion - Monotonic Stack is named Overview in the menu. Therefore, It is hard to find it for someone specifically looking for Monotonic stack through menu. Suggesting to use Monotonic stack name as well in menu.

27

Reply
Yoga Ranjan Singh
Premium
• 8 months ago

Just this one line is enough to understand monotonic stacks: Our stack stores the indexes of the elements in the input array that have not yet found their next greater element.
Love your explanations

6

Reply
Patricia Pan
Top 1%
• 1 year ago

Here's my solution for Buildings with an Ocean View, which is very similar to Daily Temperatures:

class Solution:
    def findBuildings(self, heights: List[int]) -> List[int]:
        stack = [] # store indices, monotonically decreasing stack
        for i, height in enumerate(heights):            
            while stack and heights[stack[-1]] <= height:
                stack.pop()

            stack.append(i)
        return stack

5

Reply
JP
Jai P
• 3 months ago

Leetcode #496. Next Greater Element I
Almost similar except results will be stored in dictionary to lookup the desired elements.

1

Reply
M
MysteriousIvoryBird646
Premium
• 8 months ago

I think there maybe an issue with the solution in "Next Smaller Element". The solution is exactly the same as "Next Greater Element". Condition in the while loop should be

nums[i] < nums[stack[stack.length - 1]]

1

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Problem: Next Greater Element

Solution

Next Smaller Element

Practice Problems