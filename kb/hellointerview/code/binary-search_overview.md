# Binary Search Overview

> Source: https://www.hellointerview.com/learn/code/binary-search/overview
> Scraped: 2026-03-30

Binary Search Overview
3:29
9 chapters • 1 interactive checkpoints
This section covers Binary Search, which is an efficient algorithm for searching a sorted array for a target value.
We'll focus on how to visualize the algorithm, and how visualization can help us when we are implementing the algorithm. We'll then look at some practice questions involving Binary Search.
The classic Binary Search algorithm is used to search for a target value in a sorted array.
DESCRIPTION
Given a sorted array of integers nums and a target value target, write a function to determine if target is in the array. If target is present in the array, return its index. Otherwise, return -1.
Example 1:
Input:
nums = [-1,0,3,5,9,12], target = 9
Output: 4 (nums[4] = 9)
Example 2:
Input:
nums = [-1,0,3,5,9,12], target = 2
Output: -1 (2 is not in the array, so we return -1.)
The appeal of Binary Search is readily apparent when we compare it to the brute-force approach.
The graphic below shows how the brute-force approach searches the sorted array for the target value 6. The elements considered during the search are highlighted in darker color.
1
2
3
4
5
6
7
8
9
10
1
2
3
4
5
6
7
8
9
10
1
2
3
4
5
6
7
8
9
10
1
2
3
4
5
6
7
8
9
10
1
2
3
4
5
6
7
8
9
10
1
2
3
4
5
6
7
8
9
10
Compare that to Binary Search, which locates 6 after only 3 "steps":
1
2
3
4
5
6
7
8
9
10
1
2
3
4
5
6
7
8
9
10
1
2
3
4
5
6
7
8
9
10
These two graphics show the efficiency of Binary Search, which performs the search in O(log n) time, compared to the much slower O(n) time of the Brute-Force Approach.
Intuition
Binary Search is efficient because it repeatedly cuts the portion of the array that needs to be searched in half.
Some of the visuals below are animated. Click on the 
 to the left of each visual to start the animation.
Binary Search works because our array is sorted, and the middle element of a sorted array is a great starting point. All the elements to the left of the middle element are smaller than or equal to it, and all the elements to the right are larger than or equal to it.
1
2
3
4
5
6
7
8
9
10
0
1
2
3
4
5
6
7
8
9
Let's say our target is 6.
Since our target is greater than the middle element, we can safely ignore the left half of the array - we know the target is not there. We indicate this in the visual by turning those elements gray.
This leaves the right half of the array to search, and we've cut the search space in half for the first time.
1
2
3
4
5
6
7
8
9
10
0
1
2
3
4
5
6
7
8
9
target = 6
How do we search the right half? With the same approach! We take the middle element of the right half (8), and compare it to the target.
Since our target is less than the middle element, we can now ignore the right half of the updated search space. We've just cut the search space in half again!
1
2
3
4
5
6
7
8
9
10
0
1
2
3
4
5
6
7
8
9
target = 6
Now our search space has only two elements. By convention, we choose the first of these two elements as the "middle". Our target is equal to the middle element, meaning we've found it!
1
2
3
4
5
6
7
8
9
10
0
1
2
3
4
5
6
7
8
9
target = 6
Key Takeaway
Binary Search works by repeatedly cutting the relevant search space of the array in half, until it either finds the target or the search space is empty, at which point it concludes that the target is not in the array. The halving is where the algorithm gets its O(log n) time complexity.
Implementation
Variables
Before diving into the code, let's first learn what each variable represents in the Binary Search algorithm, and visualize how they change during the search.
For these visualizations, target = 6 and nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10].
Initialize two pointers, left and right, to the start and end of the array, respectively. These two pointers represent the search space of the array. Since the entire search space is valid, they are shown in green.
1
2
3
4
5
6
7
8
9
10
0
1
2
3
4
5
6
7
8
9
target = 6
Next, we iteratively halve the search space until we've either found the target or the search space is empty (we will learn how to visualize this in the next section).
So while left <= right:
Initialize a pointer mid = (left + right) // 2. mid represents the middle of the current search space, as well as the element that we compare to target.
1
2
3
4
5
6
7
8
9
10
0
1
2
3
4
5
6
7
8
9
left
right
target = 6
Note: The // operator is used for integer division in Python. For example, in the visual above, 9 // 2 = 4.
This means that mid is always an integer, and will be the first of the two possible middle elements if the search space has an even number of elements.
1
3
4
8
0
1
2
3
left
right
mid
Show More
Compare the element at mid to the target. In this case, target > nums[mid], so we drop the left half of the search space by updating left = mid + 1. The elements that have been dropped are shown in gray.
1
2
3
4
5
6
7
8
9
10
0
1
2
3
4
5
6
7
8
9
left
right
mid
target = 6
At this point, left and right reflect the updated search space. So set mid = (left + right) // 2 again, and repeat the process until either nums[mid] == target or left > right.
1
2
3
4
5
6
7
8
9
10
0
1
2
3
4
5
6
7
8
9
left
right
mid
target = 6
Code
Let's see the code!
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
Found
Missing
Reset
VISUALIZATION
Python
Language
Full Screen
def binary_search(nums, target):
  left = 0
  right = len(nums) - 1

  while left <= right:
    mid = (left + right) // 2
    if nums[mid] == target:
      return mid
    if nums[mid] < target:
      left = mid + 1
    else:
      right = mid - 1

  return -1
1
2
3
4
5
6
7
8
9
10
0
1
2
3
4
5
6
7
8
9

binary search for 6

0 / 7

1x
Edge Cases
To deepen our understanding of Binary Search, let's consider some edge cases:
Empty Array
If the input array is empty, left starts at 0, right starts at -1, and the loop will not run, and we will return -1.
target = 2, nums = []
VISUALIZATION
Python
Language
Full Screen
def binary_search(nums, target):
  left = 0
  right = len(nums) - 1

  while left <= right:
    mid = (left + right) // 2
    if nums[mid] == target:
      return mid
    if nums[mid] < target:
      left = mid + 1
    else:
      right = mid - 1

  return -1

binary search for 2

0 / 2

1x
Single Element Array
If the input array has only one element, left, mid, and right will all be the same, and the loop will run once. If the single element is the target, we return its index. Otherwise, left > right, so we exit the loop and return -1.
target = 2, nums = [1]
VISUALIZATION
Python
Language
Full Screen
def binary_search(nums, target):
  left = 0
  right = len(nums) - 1

  while left <= right:
    mid = (left + right) // 2
    if nums[mid] == target:
      return mid
    if nums[mid] < target:
      left = mid + 1
    else:
      right = mid - 1

  return -1
1
0

binary search for 2

0 / 4

1x
Target Not in Array
If the target is not in the array, left will eventually be greater than right, and we will return -1.
target = 2, nums = [1, 3, 4, 8]
VISUALIZATION
Python
Language
Full Screen
def binary_search(nums, target):
  left = 0
  right = len(nums) - 1

  while left <= right:
    mid = (left + right) // 2
    if nums[mid] == target:
      return mid
    if nums[mid] < target:
      left = mid + 1
    else:
      right = mid - 1

  return -1
1
3
4
8
0
1
2
3

binary search for 2

0 / 6

1x
This example helps us visualize the termination condition of Binary Search.
When left = right, as shown below, there is still one element in the search space, highlighted in green.
1
3
4
8
0
1
2
3
left
right
mid
However, when left > right, as shown below, the search space is empty, and we know that the target is not in the array. We can visualize the binary search algorithm stopping when the left pointer "passes" the right pointer.
1
3
4
8
0
1
2
3
left
right
mid
These visualizations should help you internalize why the condition left <= right is used in the Binary Search algorithm - once left overtakes right, the search space is empty and we know that the target is not in the array.
What is the time complexity of this solution?
1

O(n)

2

O(4ⁿ)

3

O(4^L)

4

O(log n)

Summary
Binary Search is an effective algorithm because it allows us to repeatedly cut our search space in half until we find the target or conclude that it is not in the array. In other words, during each iteration of the algorithm, we are able to discard half of the search space.
Here are some problems that also use this concept of repeatedly discarding half of the search space:
Done
	
Question
	
Difficulty


	
Apple Harvest (Koko Eating Bananas)
	
Medium


	
Search in Rotated Sorted Array
	
Medium


	
Split Array Largest Sum
	
Hard


	
Kth Smallest Element in a Sorted Matrix
	
Medium


	
Minimum Shipping Capacity (with Weight Constraints)
	
Hard

Mark as read

Next: Apple Harvest (Koko Eating Bananas)

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

(7)

Comment
Anonymous
Allen Putich
Top 10%
• 11 months ago

Great article! One important detail to mention is that using mid = (low + high) / 2 can cause integer overflow if low + high exceeds the 32-bit limit of the int type (i.e. goes beyond the range of -2^31 to 2^31 - 1). A safer alternative is to use mid = low + (high - low) / 2, which avoids this overflow as long as low and high are valid int values and low <= high by reordering the calculation.

If you're curious or forget that equation how you get that equation, you apply some algebra and substitute high = high + low - low into mid = (low + high) / 2.

28

Reply
gabrielle rosa
• 5 months ago

Thank you! This is a great point

0

Reply
mohammad nayeem
• 1 year ago
public class BinarySearch {
    public static int binarySearch(int[] nums, int target) {
        int left = 0;
        int right = nums.length - 1;

        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (nums[mid] == target) {
                return mid;
            } else if (nums[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }

        return -1;
    }

    public static void main(String[] args) {
        int[] nums = {1, 3, 5, 7, 9};
        int target = 5;
        int index = binarySearch(nums, target);
        System.out.println("Target " + target + " found at index " + index);
    }
}
Show More

3

Reply
Mohamed Sallam
Premium
• 2 months ago

Binary Search on solution spaces is not here! Actually, that is the main challenging pattern in Binary search, also, there are multiple variants of BS, as below

**Binary search: duplicate elements, left-most insertion point
**

public int fn(int[] arr, int target) {
    int left = 0;
    int right = arr.length;
    while (left < right) {
        int mid = left + (right - left) / 2;
        if (arr[mid] >= target) {
            right = mid;
        } else {
            left = mid + 1;
        }
    }

    return left;
}

**Binary search: duplicate elements, right-most insertion point
**

public int fn(int[] arr, int target) {
    int left = 0;
    int right = arr.length;
    while (left < right) {
        int mid = left + (right - left) / 2;
        if (arr[mid] > target) {
            right = mid;
        } else {
            left = mid + 1;
        }
    }

    return left;
}

**Binary search: for greedy problems
**
*If looking for a minimum:
*

public int fn(int[] arr) {
    int left = MINIMUM_POSSIBLE_ANSWER;
    int right = MAXIMUM_POSSIBLE_ANSWER;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (check(mid)) {
            right = mid - 1;
        } else {
            left = mid + 1;
        }
    }

    return left;
}

public boolean check(int x) {
    // this function is implemented depending on the problem
    return BOOLEAN;
}

*If looking for a maximum:
*

public int fn(int[] arr) {
    int left = MINIMUM_POSSIBLE_ANSWER;
    int right = MAXIMUM_POSSIBLE_ANSWER;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (check(mid)) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }

    return right;
}

public boolean check(int x) {
    // this function is implemented depending on the problem
    return BOOLEAN;
}
Show More

2

Reply
SW
• 8 months ago

Leetcode link https://leetcode.com/problems/binary-search/?envType=study-plan-v2&envId=binary-search

2

Reply
L
LatinTurquoiseRhinoceros505
Premium
• 1 month ago
• edited 1 month ago

The Rust solution will panic on empty slice. The let mut right = nums.len() - 1; will underflow because len() returns 0usize. It has also potential to underflow on right = mid - 1. And it also does not handle the potential overflow for finding min that was mentioned by the previous commenters.

The safer solution:

fn binary_search(nums: &[i32], target: i32) -> i32 {
    let mut left = 0;
    let mut right = nums.len();

    while left < right {
        let mid = left + (right - left) / 2;

        if nums[mid] == target {
            return mid as i32;
        } else if nums[mid] < target {
            left = mid + 1;
        } else {
            right = mid;
        }
    }

    -1
}

Show More

0

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Intuition

Implementation

Summary