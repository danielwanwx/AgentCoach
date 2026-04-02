# Search in Rotated Sorted Array

> Source: https://www.hellointerview.com/learn/code/binary-search/search-in-rotated-sorted-array
> Scraped: 2026-03-30


Binary Search
Search in Rotated Sorted Array
medium
DESCRIPTION (inspired by Leetcode.com)

You are given a sorted array that has been rotated at an unknown pivot point, along with a target value. Develop an algorithm to locate the index of the target value in the array. If the target is not present, return -1. The algorithm should have a time complexity of O(log n).

Note:

The array was originally sorted in ascending order before being rotated.
The rotation could be at any index, including 0 (no rotation).
You may assume there are no duplicate elements in the array.

Example 1:
Input:

nums = [4,5,6,7,0,1,2], target = 0

Output: 4 (The index of 0 in the array)

Example 2:

Input:

nums = [4,5,6,7,0,1,2], target = 3

Output: -1 (3 is not in the array)

CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def search(self, nums: List[int], target: int) -> int:
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
The fact that this question is asking for a O(log n) solution is a hint that we should be using binary search to solve it. If we can iteratively search for our target value in the array while reducing the relevant search space by half in each iteration, then we can achieve the desired time complexity.
So let's first look at an example of a rotated sorted array and see if we can notice anything that will help us do so.
Reducing The Search Space
The visual below shows the same sorted array rotated at different points, including no rotation at all.
If we draw a line down the middle element of each array, this splits the array into two halves. Notice how at least one of the halves is always sorted in ascending order, shown in dark green in the visual.
We'll learn which half to choose when both halves are sorted (like in the first and fourth arrays) in the next step, when we learn how to determine the sorted half.
We'll also mention why the middle element itself is greyed out a little later.
12
16
17
1
2
3
8
9
10
8
9
10
12
16
17
1
2
3
10
12
16
17
1
2
3
8
9
1
2
3
8
9
10
12
16
17
3
8
9
10
12
16
17
1
2
The fact that one half of the array is always sorted is great for our goal, because we can quickly tell if our target falls within the range of that half by comparing the target with its endpoints.
If our target 3 falls within the range of the sorted half, we can confidently discard the other half of the array:
1
2
3
8
9
10
12
16
17
3
8
9
10
12
16
17
1
2
discard this half!
contains 3, so...
discard this half!
contains 3, so...
Two examples of where our target = 3 falls within the range of the sorted half of the array, which allows us to discard to other half.
Otherwise, we can discard the sorted half and continue our search in the other half.
8
9
10
12
16
17
1
2
3
does NOT contain 3​     discard it!
discard this half!
So we've accomplished our goal - we used the fact the one half of the array is always sorted to reduce our search space by half.
We can now apply the same logic as above to the half of the array we didn't discard. But first, let's see how to determine which half of the array is sorted.
Determining The Sorted Half
In a regular, unrotated, sorted array, the first element will always be less (or equal to) the middle element. However, this isn't always true for a rotated sorted array.
In a rotated search array, the middle element mid will sometimes be less than the first element left. This happens when the rotation occurs somewhere between left and mid, meaning the right half of the array is sorted.
Notice how in the first array, both halves of the array are actually sorted, as the rotation occurs right at mid. However, we still choose the right half as the sorted half because mid < left.
12
16
17
2
3
8
9
10
1
left
mid
16
17
1
3
8
9
10
12
2
However, if the middle element mid is greater than the first element left, we know that the left half of the array is sorted, like shown in the 3 examples below.
8
9
10
16
17
1
12
3
2
left
mid
9
10
12
17
1
2
16
8
3
2
3
8
10
12
16
9
1
17
Algorithm
We now have enough information to visualize our algorithm.
Initialize two pointers left = 0 and right = len(nums) - 1 as the boundaries of our search space.
8
9
10
12
16
17
1
2
3
0
1
2
3
4
5
6
7
8
left
right
Now we iteratively try to reduce our search space until its either empty or we find the target.
Initialize pointer mid = (left + right) // 2, and check if nums[mid] == target. If we find the target, we return mid. If it isn't, this removes mid from our search space.
8
9
10
12
16
17
1
2
3
0
1
2
3
4
5
6
7
8
left
right
target = 3
Determine which half is sorted: check if nums[left] < nums[mid]. If true, the left half is sorted. If not, the right half is sorted.
In this case, the left half is sorted, so we check if the target is within nums[left] (8) and nums[mid] (16).
3 is not within 8 and 16, so we discard the left half of the array from our search space by updating left = mid + 1. We just reduced our search space in half!
8
9
10
12
16
17
1
2
3
0
1
2
3
4
5
6
7
8
left
right
mid
target = 3
Now we repeat the process as above with the updated search space...
Set mid = (left + right) // 2 and check if nums[mid] == target.
8
9
10
12
16
17
1
2
3
0
1
2
3
4
5
6
7
8
left
right
mid
target = 3
Check which half is sorted: nums[left] (17) is greater than nums[mid] (1), so the right half is sorted.
Check if the target is within nums[mid] (1) and nums[right] (3). It is, so we update left = mid + 1 to discard the left half of the array.
8
9
10
12
16
17
1
2
3
0
1
2
3
4
5
6
7
8
left
right
mid
target = 3
This continues until either we find the target or our search space is empty (left > right).
Solution
SOLUTION
Python
Language
def search(nums, target):
    left = 0
    right = len(nums) - 1

    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid

        if nums[left] <= nums[mid]:
            # left half is sorted
            if nums[left] <= target and target < nums[mid]:
                # target is in the left half
                right = mid - 1
            else:
                # target is in the right half
                left = mid + 1
        else:
            # right half is sorted
            if nums[mid] < target and target <= nums[right]:
                # target is in the right half
                left = mid + 1
            else:
                # target is in the left half
                right = mid - 1

    return -1
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
def search(nums, target):
  left = 0
  right = len(nums) - 1

  while left <= right:
    mid = (left + right) // 2
    if nums[mid] == target:
      return mid
    if nums[left] <= nums[mid]:
      if nums[left] <= target and target < nums[mid]:
        right = mid - 1
      else:
        left = mid + 1
    else:
      if nums[mid] < target and target <= nums[right]:
        left = mid + 1
      else:
        right = mid - 1
  return -1
8
9
10
12
16
17
1
2
3
0
1
2
3
4
5
6
7
8

search for 3 in rotated sorted array

0 / 9

1x
What is the time complexity of this solution?
1

O(m * n)

2

O(n²)

3

O(log n)

4

O(4ⁿ)

Mark as read

Next: Split Array Largest Sum

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

(14)

Comment
Anonymous
​
Sort By
Popular
Sort By
mj park
• 6 months ago

In the explanation, it says

Determine which half is sorted: check if nums[left] < nums[mid]. If true, the left half is sorted. If not, the right half is sorted.

However, I want to call out that the solution is using the check <= instead of <

if nums[left] <= nums[mid]:

In fact, we should use <= so that it correctly handles the situation where only two elements exist in an array (e.g. [3,1]). In such case, it should treat the left half as sorted.

7

Reply
SM
Sriharsha Madala
Premium
• 7 months ago

A simpler approach is to use binary search to find the index where the rotation happened. This would split the input into two sorted arrays. Perform binary search on each of them.

5

Reply
Abhay Singh
Top 1%
• 1 year ago

Java Solution:

class Solution {
    public int search(int[] nums, int target) {
        int n = nums.length;

        int l = 0, r = n - 1;

        while(l <= r){
            int m = l + (r-l)/2;

            if(nums[m] == target){
                return m;
            }

            // left segment
            if(nums[m] > nums[n-1]){
                // move right
                if(nums[m] < target || target < nums[0]){
                    l=m+1;
                }else{
                    r=m-1;
                }
            }else{
                // move left
                if(nums[m] > target || target > nums[n-1]){
                    r=m-1;
                }else{
                    l=m+1;
                }
            }
        }

        return -1;
    }
}
Show More

3

Reply
mohammad nayeem
• 1 year ago
public class BinarySearch {
    public static int search(int[] nums, int target) {
        int left = 0;
        int right = nums.length - 1;

        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (nums[mid] == target) {
                return mid;
            }

            if (nums[left] <= nums[mid]) {
                // Left half is sorted
                if (nums[left] <= target && target < nums[mid]) {
                    // Target is in the left half
                    right = mid - 1;
                } else {
                    // Target is in the right half
                    left = mid + 1;
                }
            } else {
                // Right half is sorted
                if (nums[mid] < target && target <= nums[right]) {
                    // Target is in the right half
                    left = mid + 1;
                } else {
                    // Target is in the left half
                    right = mid - 1;
                }
            }
        }

        return -1; // Target not found
    }
}
Show More

2

Reply
H G
• 1 month ago

hmm why make it way more complicated when it can be just like

    def search(self, nums: List[int], target: int):
        i, j = 0, len(nums) - 1
        while i <= j:
            m = (i + j) // 2
            if nums[m] == target: return m
            elif (nums[m] < target and nums[j] >= target) or (nums[m] > target and nums[i] > target): i = m + 1
            elif (nums[m] > target and nums[i] <= target) or (nums[m] < target and nums[j] < target): j = m - 1
        return -1

0

Reply
T
TenderIndigoOpossum389
Premium
• 1 month ago

It's not a competition for lesser lines. Readability is important in coding. Cheers.

2

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

Reducing the Search Space

Determining the Sorted Half

Algorithm

Solution
