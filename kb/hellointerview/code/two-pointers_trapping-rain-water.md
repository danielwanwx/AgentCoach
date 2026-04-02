# Trapping Rain Water

> Source: https://www.hellointerview.com/learn/code/two-pointers/trapping-rain-water
> Scraped: 2026-03-30


Two Pointers
Trapping Rain Water
hard
DESCRIPTION (inspired by Leetcode.com)

Write a function to calculate the total amount of water trapped between bars on an elevation map, where each bar's width is 1. The input is given as an array of n non-negative integers height representing the height of each bar.

Example:

3
4
1
2
2
5
1
0
2
2
1
3
6
5
4
8
7
10
9
Count:
10
height = [3, 4, 1, 2, 2, 5, 1, 0, 2]

Output:

10
CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def trappingWater(self, height: List[int]) -> int:
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
We can use the two-pointer technique to solve this problem in O(n) time and O(1) space.
In order for any index in the array to be able to trap rain water, there must be higher bars on both the left and right side of the index. For example, index 2 in the following array has height 1. It can trap water because there are higher bars to the left and right of it.
3
4
1
2
2
5
1
0
2
To calculate the exact amount of water that can be trapped at index 2, we first take the minimum height of the highest bars to the left and right of it, which in this case is 4. We then subtract the height of the bar at index 2, which is 1,
3
4
1
2
2
5
1
0
2
So if we knew the height of the highest bars to the left and right of every index, we could iterate through the array and calculate the amount of water that can be trapped at each index.
But we don't need to know the exact height of both the highest bars to the left and right of every index. For example, let's say we know the highest bar to the right of index 7 with height 0 has a height of 2.
3
4
1
2
2
5
1
0
2
If we also knew that there exists a higher bar than 2 anywhere to the left of index 7, then we also know that the minimum height of the highest bars to the left and right of index 7 is 2. This means that we have enough information to calculate the amount of water that can be trapped at index 7, which is 2 - 0 = 2.
This is the insight behind how the two-pointer technique can be used to solve this problem. We initialize two pointers left and right at opposite ends of the array. We also keep two variables leftMax and rightMax to keep track of the highest bars each pointer has seen.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def trappingWater(heights):
    if not heights:
        return 0
    left, right = 0, len(heights) - 1
    leftMax, rightMax = heights[left], heights[right]
    count = 0
    
    while left < right:
        if leftMax < rightMax:
            left += 1
            if heights[left] >= leftMax:
                leftMax = heights[left]
            else:
                count += leftMax - heights[left]
        else:
            right -= 1
            if heights[right] >= rightMax:
                rightMax = heights[right]
            else:
                count += rightMax - heights[right]
    
    return count
3
4
1
2
2
5
1
0
2

trapping rain water

0 / 1

1x
We now use the values of leftMax and rightMax to visit every single index in the array exactly once. We start by comparing leftMax and rightMax. In this case, rightMax is smaller than leftMax, so we know that:
The maximum height of the highest bar to the right of right - 1 is rightMax
There exists a higher bar than rightMax somewhere to the left of right
These two facts mean that we have enough information to calculate the amount of water that can be trapped at index right - 1. So first we move the right pointer back by 1:
VISUALIZATION
Hide Code
Python
Language
Full Screen
def trappingWater(heights):
    if not heights:
        return 0
    left, right = 0, len(heights) - 1
    leftMax, rightMax = heights[left], heights[right]
    count = 0
    
    while left < right:
        if leftMax < rightMax:
            left += 1
            if heights[left] >= leftMax:
                leftMax = heights[left]
            else:
                count += leftMax - heights[left]
        else:
            right -= 1
            if heights[right] >= rightMax:
                rightMax = heights[right]
            else:
                count += rightMax - heights[right]
    
    return count
3
4
1
2
2
5
1
0
2
left
right
leftMax
rightMax
Count:
0

initialize pointers

0 / 1

1x
There are two possible cases to consider when calculating the amount of water that can be trapped at the current index of right:
The height of the bar at index right is smaller than rightMax
The height of the bar at index right is greater than or equal to rightMax
In our case, the height of the bar at index right is smaller than rightMax, so we know that the amount of water that can be trapped at index 1 is rightMax - height[right], and we can move to the next iteration, which follows the same logic:
VISUALIZATION
Hide Code
Python
Language
Full Screen
def trappingWater(heights):
    if not heights:
        return 0
    left, right = 0, len(heights) - 1
    leftMax, rightMax = heights[left], heights[right]
    count = 0
    
    while left < right:
        if leftMax < rightMax:
            left += 1
            if heights[left] >= leftMax:
                leftMax = heights[left]
            else:
                count += leftMax - heights[left]
        else:
            right -= 1
            if heights[right] >= rightMax:
                rightMax = heights[right]
            else:
                count += rightMax - heights[right]
    
    return count
3
4
1
2
2
5
1
0
2
left
right
leftMax
rightMax
Count:
0

move right pointer

0 / 4

1x
Now, we run into case 2, where height[right] is greater than or equal to rightMax. This means we can't trap any water at this index, so instead we update rightMax to the height of the bar at index right to prepare for the next iteration.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def trappingWater(heights):
    if not heights:
        return 0
    left, right = 0, len(heights) - 1
    leftMax, rightMax = heights[left], heights[right]
    count = 0
    
    while left < right:
        if leftMax < rightMax:
            left += 1
            if heights[left] >= leftMax:
                leftMax = heights[left]
            else:
                count += leftMax - heights[left]
        else:
            right -= 1
            if heights[right] >= rightMax:
                rightMax = heights[right]
            else:
                count += rightMax - heights[right]
    
    return count
3
4
1
2
2
5
1
0
2
left
right
2
1
3
leftMax
rightMax
Count:
3

move right pointer

0 / 2

1x
The same logic applies when leftMax is less than rightMax, and this continues until every index has been visited exactly once, for a total time complexity of O(n) and a space complexity of O(1).
VISUALIZATION
Hide Code
Python
Language
Full Screen
def trappingWater(heights):
    if not heights:
        return 0
    left, right = 0, len(heights) - 1
    leftMax, rightMax = heights[left], heights[right]
    count = 0
    
    while left < right:
        if leftMax < rightMax:
            left += 1
            if heights[left] >= leftMax:
                leftMax = heights[left]
            else:
                count += leftMax - heights[left]
        else:
            right -= 1
            if heights[right] >= rightMax:
                rightMax = heights[right]
            else:
                count += rightMax - heights[right]
    
    return count
3
4
1
2
2
5
1
0
2
left
right
2
1
3
leftMax
rightMax
Count:
3

update leftMax

0 / 7

1x
Solution
heights
​
|
heights
comma-separated integers
Try these examples:
Shallow
Classic
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def trappingWater(heights):
    if not heights:
        return 0
    left, right = 0, len(heights) - 1
    leftMax, rightMax = heights[left], heights[right]
    count = 0
    
    while left < right:
        if leftMax < rightMax:
            left += 1
            if heights[left] >= leftMax:
                leftMax = heights[left]
            else:
                count += leftMax - heights[left]
        else:
            right -= 1
            if heights[right] >= rightMax:
                rightMax = heights[right]
            else:
                count += rightMax - heights[right]
    
    return count
3
4
1
2
2
5
1
0
2

trapping rain water

0 / 16

1x

Mark as read

Next: Fixed Length Sliding Window

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

(33)

Comment
Anonymous
​
Sort By
Popular
Sort By
Sean Tarzy
Top 5%
• 1 year ago

We now use the values of leftMax and rightMax to visit every single index in the array exactly once. We start by comparing leftMax and rightMax. In this case, leftMax is smaller than rightMax, so we know that:

do you not mean rightMax is smaller than leftMax (2<3) ?

14

Reply
T
TechnicalSapphireBedbug377
Premium
• 11 months ago

It says "We now use the values of leftMax and rightMax to visit every single index in the array exactly once. We start by comparing leftMax and rightMax. In this case, leftMax is smaller than rightMax, so we know that:" but in the given example, leftMax is bigger than rightMax.

9

Reply
Abhay Singh
Top 1%
• 1 year ago

2 Java Solutions:

class Solution {
    public int trap(int[] height) {
        int n = height.length;

        int[] leftMax = new int[n];
        Arrays.fill(leftMax, -1);

        for(int i=1;i<n;i++) leftMax[i] = Math.max(leftMax[i-1], height[i-1]);

        int[] rightMax = new int[n];
        Arrays.fill(rightMax, -1);

        for(int i=n-2;i>=0;i--) rightMax[i] = Math.max(rightMax[i+1], height[i+1]);

        int ans = 0;
        for(int i=1;i<n-1;i++){
            ans += Math.max(0, Math.min(leftMax[i], rightMax[i]) - height[i]);
        }

        return ans;
    }
}
class Solution {
    public int trap(int[] height) {
        int n = height.length;

        // since our answer always depend on min of max values to right & left
        // so we don't have to know exact values for both
        int leftMax = height[0], rightMax = height[n-1];
        int i = 1, j = n-2;

        int ans = 0;
        while(i <= j){
            if(leftMax < rightMax){
                ans += Math.max(0, leftMax - height[i]);

                leftMax = Math.max(leftMax, height[i]);
                i++;
            }else{
                ans += Math.max(0, rightMax - height[j]);

                rightMax = Math.max(rightMax, height[j]);
                j--;
            }
        }

        return ans;
    }
}
Show More

5

Reply
M
MagicVioletGecko251
• 1 year ago

Had to add this to get the tests to work:

if not height or len(height) < 3:
    return 0

5

Reply
Ritik Ranjan Behera
• 1 month ago

It's such a pretty problem

3

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

Solution
