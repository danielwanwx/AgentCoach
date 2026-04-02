# Largest Rectangle in Histogram

> Source: https://www.hellointerview.com/learn/code/stack/largest-rectangle-in-histogram
> Scraped: 2026-03-30


Stack
Largest Rectangle in Histogram
hard
DESCRIPTION (inspired by Leetcode.com)

Given an integer array heights representing the heights of histogram bars, write a function to find the largest rectangular area possible in a histogram, where each bar's width is 1.

Inputs:

heights = [2,8,5,6,2,3]

Output:

15
CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
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
To solve this question, we calculate the largest rectangle that contains the bar at each index of the array, and return the largest of those rectangles at the end. By using a monotonically increasing stack, we can solve this question in O(n) time complexity, compared to the brute-force solution which takes O(n2) time.
Largest Rectangle At Each Index
To calculate the largest rectangle at each index, we need to know the index of the first shorter bar to both the left and the right of the current bar. The width of the rectangle is the difference between the two indices - 1, and the height is the height of the current bar.
2
8
5
6
2
3
0
1
2
3
4
5
Index of first shorter bar to left: 0. Index of first shorter bar to right: 2. Total area: 8 * (2 - 0 - 1) = 8
2
8
5
6
2
3
0
1
2
3
4
5
Index of first shorter bar to left: 0. Index of first shorter bar to right: 4. Total area: 5 * (4 - 0 - 1) = 15
Brute-Force Solution
The brute-force solution iterates over each bar in the array, and for each bar, finds the first shortest bar to the left and the right of the bar using two while loops, for a time complexity of O(n2).
SOLUTION
Python
Language
def largestRectangleArea(heights):
    max_area = 0
    n = len(heights)

    for i in range(n): 
        left = i - 1
        while left >= 0 and heights[left] >= heights[i]:
            left -= 1

        right = i + 1
        while right < n and heights[right] >= heights[i]:
            right += 1

        max_area = max(max_area, (right - left - 1) * heights[i])
    
    return max_area
Monotonically Increasing Stack
By using a monotonically increasing stack, we can find the first shortest bar to the left and right of each bar in O(n) time complexity.
We first initialize our stack, as well as a variable to store the maximum area and a pointer i to iterate over the array. The stack contains the indices of the bars in increasing order of their heights. When an index is placed on the stack, it means we are waiting to find a shorter bar to the right of that current index.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def largest_rectangle_area(heights):
  stack = []
  max_area = 0
  i = 0
  while i < len(heights):
    if not stack or heights[i] >= heights[stack[-1]]:
      stack.append(i)
      i += 1
    else:
      top = stack.pop()
      right = i - 1
      left = stack[-1] if stack else -1
      area = heights[top] * (right - left)
      max_area = max(max_area, area)

  while stack:
    top = stack.pop()
    width = i - stack[-1] - 1 if stack else i
    area = heights[top] * width
    max_area = max(max_area, area)
  return max_area
2
8
5
6
2
3
0
1
2
3
4
5

largest rectangle in histogram

0 / 1

1x
We then iterate over the array. If height[i] is greater than the height of the index at the top of the stack, we push i onto the stack. If i is less than the height of index at the top of the stack, we pop the index at the top of the stack and calculate the area of the rectangle containing that index.
Pushing To The Stack
If height[i] is greater than the height of the index at the top of the stack (or if the stack is currently empty), we push i onto the stack. This means we are waiting to find a shorter bar to the right of i, and we increment i.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def largest_rectangle_area(heights):
  stack = []
  max_area = 0
  i = 0
  while i < len(heights):
    if not stack or heights[i] >= heights[stack[-1]]:
      stack.append(i)
      i += 1
    else:
      top = stack.pop()
      right = i - 1
      left = stack[-1] if stack else -1
      area = heights[top] * (right - left)
      max_area = max(max_area, area)

  while stack:
    top = stack.pop()
    width = i - stack[-1] - 1 if stack else i
    area = heights[top] * width
    max_area = max(max_area, area)
  return max_area
2
8
5
6
2
3
0
1
2
3
4
5
i
maxArea: 0
stack

initialize variables

0 / 2

1x
Pushing `i = 0` and `i = 1` to the stack
Popping From The Stack
If height[i] is less than the height of the index at the top of the stack, we have enough information to calculate the area of the rectangle containing the index at the top of the stack. i is the first shorter bar to the right of the index at the top of the stack. Because the stack is monotonically increasing, the index beneath the index at the top is the first shorter bar to the left of it (or -1 if the stack is empty).
VISUALIZATION
Hide Code
Python
Language
Full Screen
def largest_rectangle_area(heights):
  stack = []
  max_area = 0
  i = 0
  while i < len(heights):
    if not stack or heights[i] >= heights[stack[-1]]:
      stack.append(i)
      i += 1
    else:
      top = stack.pop()
      right = i - 1
      left = stack[-1] if stack else -1
      area = heights[top] * (right - left)
      max_area = max(max_area, area)

  while stack:
    top = stack.pop()
    width = i - stack[-1] - 1 if stack else i
    area = heights[top] * width
    max_area = max(max_area, area)
  return max_area
2
8
5
6
2
3
0
1
2
3
4
5
i
maxArea: 0
0
1
stack

push to stack

0 / 1

1x
At this point, i = 2, and the top of the stack is 1. heights[2] < heights[1] (5 < 8), so i is the right boundary for the rectangle at index 1. The left boundary is the index at the top of the stack after popping 1 from the stack (in this case, 0).
i still has the potential to be the right boundary for the new index at the top of the stack after the previous index was popped, so we don't increment i, and instead, move to the next iteration.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def largest_rectangle_area(heights):
  stack = []
  max_area = 0
  i = 0
  while i < len(heights):
    if not stack or heights[i] >= heights[stack[-1]]:
      stack.append(i)
      i += 1
    else:
      top = stack.pop()
      right = i - 1
      left = stack[-1] if stack else -1
      area = heights[top] * (right - left)
      max_area = max(max_area, area)

  while stack:
    top = stack.pop()
    width = i - stack[-1] - 1 if stack else i
    area = heights[top] * width
    max_area = max(max_area, area)
  return max_area
2
8
5
6
2
3
0
1
2
3
4
5
i
maxArea: 8
0
2
3
stack

push to stack

0 / 2

1x
Another example. `i = 4`, and is the right boundary for both indexes 3 and 2.
Emptying The Stack
When i has iterated over the entire array, we still need to process the remaining indexes on the stack, which are the indexes that have not yet found a shorter bar to the right. So to calculate the area of the rectangle for these indexes, we use the end of the array as the right boundary, while the calculation for the left boundary remains the same.
When the stack is empty, we have processed all the indexes, and we return the maximum area.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def largest_rectangle_area(heights):
  stack = []
  max_area = 0
  i = 0
  while i < len(heights):
    if not stack or heights[i] >= heights[stack[-1]]:
      stack.append(i)
      i += 1
    else:
      top = stack.pop()
      right = i - 1
      left = stack[-1] if stack else -1
      area = heights[top] * (right - left)
      max_area = max(max_area, area)

  while stack:
    top = stack.pop()
    width = i - stack[-1] - 1 if stack else i
    area = heights[top] * width
    max_area = max(max_area, area)
  return max_area
2
8
5
6
2
3
0
1
2
3
4
5
i
maxArea: 15
0
4
5
stack

push to stack

0 / 4

1x
Emptying the stack, and returning `maxArea`.
Solution
heights
​
|
heights
list of integers
Try these examples:
Flat
Valley
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def largest_rectangle_area(heights):
  stack = []
  max_area = 0
  i = 0
  while i < len(heights):
    if not stack or heights[i] >= heights[stack[-1]]:
      stack.append(i)
      i += 1
    else:
      top = stack.pop()
      right = i - 1
      left = stack[-1] if stack else -1
      area = heights[top] * (right - left)
      max_area = max(max_area, area)

  while stack:
    top = stack.pop()
    width = i - stack[-1] - 1 if stack else i
    area = heights[top] * width
    max_area = max(max_area, area)
  return max_area
2
8
5
6
2
3
0
1
2
3
4
5

largest rectangle in histogram

0 / 14

1x
What is the time complexity of this solution?
1

O(n³)

2

O(4ⁿ)

3

O(2ⁿ)

4

O(n)

Mark as read

Next: Linked List Overview

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

(31)

Comment
Anonymous
​
Sort By
Popular
Sort By
A
AddedLimeCarp593
Top 1%
• 9 months ago

Not optimal because it does 3 passes but here's my O(n) approach. For each building it finds the closest shorter building to the left and right using monotonic stack, then takes the max of height*(index of closest shorter right building - index of closest shorter left building - 1).

class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        largest = 0
        right = [len(heights)]*len(heights)
        stack = []
        for i in range(len(heights)):
            while stack and heights[i] < heights[stack[-1]]:
                right[stack.pop()] = i
            stack.append(i)
        
        left = [-1]*len(heights)
        stack = []
        for i in range(len(heights)-1, -1, -1):
            while stack and heights[i] < heights[stack[-1]]:
                left[stack.pop()] = i
            stack.append(i)
        
        for i in range(len(heights)):
            largest = max(largest, heights[i]*(right[i]-left[i]-1))

        return largest

Show More

3

Reply
Abhay Singh
Top 1%
• 1 year ago

Java Solution:

class Solution {

    int[] nearestSmallerRight(int[] arr){
        int n = arr.length;

        int[] nsr = new int[n];
        Stack<Pair<Integer, Integer>> st = new Stack<>();

        for(int i=n-1;i>=0;i--){
            while(!st.isEmpty() && st.peek().getValue() >= arr[i]){
                st.pop();
            }

            nsr[i] = st.isEmpty() ? n:st.peek().getKey();
            st.add(new Pair(i, arr[i])); 
        }

        return nsr;
    }

    int[] nearestSmallerLeft(int[] arr){
        int n = arr.length;

        int[] nsl = new int[n];
        Stack<Pair<Integer, Integer>> st = new Stack<>();

        for(int i=0;i<n;i++){
            while(!st.isEmpty() && st.peek().getValue() >= arr[i]){
                st.pop();
            }

            nsl[i] = st.isEmpty() ? -1:st.peek().getKey();
            st.add(new Pair(i, arr[i])); 
        }

        return nsl;
    }

    public int largestRectangleArea(int[] heights) {
        int n = heights.length;
        
        int[] nsr = nearestSmallerRight(heights);
        int[] nsl = nearestSmallerLeft(heights);

        int ans = 0;
        for(int i=0;i<n;i++){
            int h = heights[i];
            int w = nsr[i] - nsl[i] - 1;

            ans = Math.max(ans, h*w);
        }

        return ans;
    }
}
Show More

2

Reply
Rahul
• 2 months ago

other way to solve

class Solution:
    def largestRectangleArea(self, heights: List[int]):
        # Your code goes here
        st = []
        n = len(heights)
        ans = 0
        for i in range(n):
            while st and heights[st[-1]] >= heights[i]:
                ht = heights[st.pop()]
                wd = i-(st[-1]+1 if st else 0) 
                ans = max(ans, ht*wd)
            st.append(i)
            
        while st:
            idx = st.pop()
            ht = heights[idx]
            wd = n - st[-1] -1 if st else n
            ans = max(ans, wd*ht)
        return ans
Show More

1

Reply
E
ElegantAquaMouse760
• 1 month ago

I did something similar but more intuitive.

def largestRectangleArea(self, heights: List[int]):
        n = len(heights)
        area_max = 0
        stack = []
        for i in range(n):
            while stack and heights[i] < heights[stack[-1]]:
                top = stack.pop()
                right = i - 1
                left = stack[-1] if stack else -1
                area_max = max(area_max, heights[top] * (right - left))
            stack.append(i)

        while stack:
            top = stack.pop()
            right, left = n - 1, stack[-1] if stack else -1
            height = heights[top]
            area_max = max(area_max, height * (right - left))

        return area_max
Show More

0

Reply
Armando Martínez
Premium
• 3 months ago
undefined

right = i - 1


This part is pretty confusing, its succinct but it would be clearer if it was just i and then the  ```python
-1
``` was used for the width calculation


1

Reply
mohammad nayeem
• 1 year ago
import java.util.Stack;

public class LargestRectangleArea {
    public static int largestRectangleArea(int[] heights) {
        Stack<Integer> stack = new Stack<>();
        int maxArea = 0;
        int i = 0;

        while (i < heights.length) {
            if (stack.isEmpty() || heights[i] >= heights[stack.peek()]) {
                stack.push(i);
                i++;
            } else {
                int top = stack.pop();
                int right = i - 1;
                int left = stack.isEmpty() ? -1 : stack.peek();

                int area = heights[top] * (right - left);
                maxArea = Math.max(maxArea, area);
            }
        }

        while (!stack.isEmpty()) {
            int top = stack.pop();
            int width = stack.isEmpty() ? i : i - stack.peek() - 1;
            int area = heights[top] * width;
            maxArea = Math.max(maxArea, area);
        }

        return maxArea;
    }

    public static void main(String[] args) {
        int[] heights = {2, 1, 5, 6, 2, 3};
        int maxArea = largestRectangleArea(heights);
        System.out.println("The largest rectangle area is: " + maxArea);
    }
}
Show More

1

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

Largest Rectangle at each Index

Brute-Force Solution

Monotonically Increasing Stack

Pushing to the Stack

Popping from the Stack

Emptying the Stack

Solution
