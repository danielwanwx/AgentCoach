# Find K Closest Elements

> Source: https://www.hellointerview.com/learn/code/heap/find-k-closest-elements
> Scraped: 2026-03-30


Heap
Find K Closest Elements
medium
DESCRIPTION (inspired by Leetcode.com)

Given a sorted array nums, a target value target, and an integer k, find the k closest elements to target in the array, where "closest" is the absolute difference between each element and target. Return these elements in array, sorted in ascending order.

Example 1:

Inputs:

nums = [-1, 0, 1, 4, 6]
target = 1
k = 3

Output:

[-1, 0, 1]

Explanation: -1 is 2 away from 1, 0 is 1 away from 1, and 1 is 0 away from 1. All other elements are more than 2 away. Since we need to return the elements in ascending order, the answer is [-1, 0, 1]

Example 2:

Inputs:

nums = [5, 6, 7, 8, 9]
target = 10
k = 2

Output:

[8, 9]
CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def kClosest(self, nums: List[int], k: int, target: int) -> List[int]
    :
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
Approach 1: Sorting
The simplest approach is to calculate the distance of each element from the target and to sort the elements based on that distance. This approach has a time complexity of O(n log n) where n is the number of points in the array, and a space complexity of O(n) (to store the sorted array of distances).
Approach 2: Max-Heap
This problem can be solved using a similar approach to the one used to solve Kth Largest Element in an Array, with the key difference being that we need to find the k closest elements to the target, rather than the k largest elements. Since we are looking for the k smallest elements, we need a max-heap, rather than a min-heap.
By default, python's heapq module implements a min-heap, but we can make it behave like a max-heap by negating the values of everything we push onto it.
First, we push the first k elements to the heap by storing a tuple containing the negative of the distance of the element from the target, and the element itself. After that is finished, our heap contains the k closest elements to the target that we've seen so far, with the element furthest from the target at the root of the heap.
k = 3, target = 5
VISUALIZATION
Python
Language
Full Screen
def k_closest(nums, k, target):
    heap = []
    for num in nums:
        distance = abs(num - target)
        if len(heap) < k:
            heapq.heappush(heap, (-distance, num))
        elif distance < -heap[0][0]:
            heapq.heappushpop(heap, (-distance, num))
    
    distances = [pair[1] for pair in heap]
    distances.sort()
    return distances
-1
1
2
4
6

initialize heap

0 / 6

1x
Pushing the first `k = 3` elements onto the heap. The root of the heap after this is done holds a tuple containing the negative of the distance of the element furthest from the target, and the element itself (-6, -1).
For each element after the first k, we calculate the distance from the target and compare it with the root of the heap. If the current element is closer to the target than the root of the heap, we pop the root and push a tuple containing the negative distance of the current element from the target and the element itself onto the heap.
k = 3, target = 5
VISUALIZATION
Python
Language
Full Screen
def k_closest(nums, k, target):
    heap = []
    for num in nums:
        distance = abs(num - target)
        if len(heap) < k:
            heapq.heappush(heap, (-distance, num))
        elif distance < -heap[0][0]:
            heapq.heappushpop(heap, (-distance, num))
    
    distances = [pair[1] for pair in heap]
    distances.sort()
    return distances
-6,-1
-4,1
-3,2
-1
1
2
4
6
num

distance = 1

0 / 1

1x
The current element `num = 4` is closer to the target than the root of the heap, so we pop the root and push `(-1, 4)`. The new root of the heap `(-4, 1)` is now the element furthest from the target amongst the `k` closest elements we've seen so far.
At the end of the iteration, the heap will contain the k closest elements to the target. We can iterate over the heap and return the element associated with each tuple, and sort the result to return the elements in ascending order.
k = 3, target = 5
VISUALIZATION
Python
Language
Full Screen
def k_closest(nums, k, target):
    heap = []
    for num in nums:
        distance = abs(num - target)
        if len(heap) < k:
            heapq.heappush(heap, (-distance, num))
        elif distance < -heap[0][0]:
            heapq.heappushpop(heap, (-distance, num))
    
    distances = [pair[1] for pair in heap]
    distances.sort()
    return distances
-3,2
-1,4
-1,6
-1
1
2
4
6
num

pushpop from heap

0 / 1

1x
Solution
nums
​
|
nums
list of integers
k
​
|
k
integer
target
​
|
target
integer
Try these examples:
Target Outside
Centered
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def k_closest(nums, k, target):
    heap = []
    for num in nums:
        distance = abs(num - target)
        if len(heap) < k:
            heapq.heappush(heap, (-distance, num))
        elif distance < -heap[0][0]:
            heapq.heappushpop(heap, (-distance, num))
    
    distances = [pair[1] for pair in heap]
    distances.sort()
    return distances
-1
1
2
4
6

find k closest elements

0 / 12

1x
What is the time complexity of this solution?
1

O(log m * n)

2

O(N + Q)

3

O(n * log k)

4

O(4ⁿ)

Bonus Approach: Two Pointers + Binary Search
We can also leverage the fact that the input array is sorted to solve this problem using a two-pointer approach combined with binary search. This approach is based on the observation that the k closest elements to the target will occur in a contiguous subarray of length k in the sorted array.
This algorithm initializes two pointers, left at index 0 and right at index len(nums) - k. The indicies between left and right represent the possible starting indices of the k closest elements to the target.
k = 3, target = 5
VISUALIZATION
Python
Language
Full Screen
def findClosestElements(nums, k, target):
    left, right = 0, len(nums) - k
    while left < right:
        mid = left + (right - left) // 2
        if target - nums[mid] > nums[mid + k] - target:
            left = mid + 1
        else:
            right = mid
    return nums[left:left + k]
-1
1
1
4
6
8
10
0
1
2
3
4
5
6

find k closest elements

0 / 1

1x
The two pointers `left` and `right` are initialized at index 0 and `len(nums) - k` respectively. The indices between `left` and `right` represent the possible starting indices of the `k` closest elements to the target.
We then perform a binary search to find the starting index of the k closest elements. We do so by first calculating the midpoint of the two pointers, mid. We then compare the distance of the element at mid from the target with the distance of the element at mid + k from the target.
In the case below, nums[mid] = 1 and nums[mid + k] = 8. Since target = 5, nums[mid + k] is closer to the target than nums[mid].
k = 3, target = 5
VISUALIZATION
Python
Language
Full Screen
def findClosestElements(nums, k, target):
    left, right = 0, len(nums) - k
    while left < right:
        mid = left + (right - left) // 2
        if target - nums[mid] > nums[mid + k] - target:
            left = mid + 1
        else:
            right = mid
    return nums[left:left + k]
-1
1
1
4
6
8
10
0
1
2
3
4
5
6
left
right

initialize pointers

0 / 1

1x
This is where the choice to compare the distances between nums[mid] and nums[mid + k] comes into play. The contiguous subarray containing the k closest elements cannot contain both nums[mid] and nums[mid + k] because they are located k + 1 elements apart. So when nums[mid + k] is closer to the target than nums[mid], this tells us that the final answer might include nums[mid + k], but it will definitely not incldue nums[mid]. To reflect this, we move the left pointer to mid + 1 to indicate that the starting index of the k closest elements will be to the right of mid.
k = 3, target = 5
VISUALIZATION
Python
Language
Full Screen
def findClosestElements(nums, k, target):
    left, right = 0, len(nums) - k
    while left < right:
        mid = left + (right - left) // 2
        if target - nums[mid] > nums[mid + k] - target:
            left = mid + 1
        else:
            right = mid
    return nums[left:left + k]
-1
1
1
4
6
8
10
0
1
2
3
4
5
6
left
right
mid = 2
mid + k = 5

nums[mid] = 1, nums[mid + k] = 8

0 / 1

1x
(The opposite is true when nums[mid] is closer to the target than nums[mid + k]. In this case, the final answer might include nums[mid] but it will definitely not include nums[mid + k]. To reflect this, we move the right pointer to mid.)
Now, we've reduced the search space of the starting index of the k closest elements by half of its previous size. We can continue this process until left and right meet at the same index. At this point, the starting index of the k closest elements will be left.
k = 3, target = 5
VISUALIZATION
Python
Language
Full Screen
def findClosestElements(nums, k, target):
    left, right = 0, len(nums) - k
    while left < right:
        mid = left + (right - left) // 2
        if target - nums[mid] > nums[mid + k] - target:
            left = mid + 1
        else:
            right = mid
    return nums[left:left + k]
-1
1
1
4
6
8
10
0
1
2
3
4
5
6
left
right
mid = 2
mid + k = 5

left = 3

0 / 3

1x
Solution
nums
​
|
nums
list of integers
k
​
|
k
integer
target
​
|
target
integer
Try these examples:
Target Below
Centered
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def findClosestElements(nums, k, target):
    left, right = 0, len(nums) - k
    while left < right:
        mid = left + (right - left) // 2
        if target - nums[mid] > nums[mid + k] - target:
            left = mid + 1
        else:
            right = mid
    return nums[left:left + k]
-1
1
1
4
6
8
10
0
1
2
3
4
5
6

find k closest elements

0 / 6

1x
Complexity Analysis
Time Complexity: O(log(n - k) + k). We run binary search over n - k elements, and in each iteration of the binary search, we reduce the search space by half, for a total run time of O(log(n - k)). After finding the starting index of the k closest elements, we iterate over the k closest elements to build the result array, which takes O(k) time.
Space Complexity: O(1). We only use a constant amount of extra space.

Mark as read

Next: Merge K Sorted Lists

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
B
binliu.zhang
Premium
• 1 year ago

For the bonus approach Two pointers + Binary search, not quite understand why we're using
 if target - nums[mid] > nums[mid + k] - target: here,
instead of if abs(target - nums[mid]) > abs(target - nums[mid + k])
or if target - nums[mid] > target - nums[mid + k].
Could you help elaborate a bit more?

5

Reply
Jimmy Zhang
Top 5%
• 1 year ago

Yeah really good question.

You are comparing nums[mid] and nums[mid + k] to see which one is closer to the target, but also which direction to move the left and right pointers.

Another way to write that condition is: if target > (nums[mid + k] + nums[mid]) / 2, which is comparing the target to the midpoint of the two values. when that condition is true, move the left pointer, and when its false, move the right pointer.

try working through this case: nums = [1,1,2,2,2,2,2,3,3], target = 3, k = 3 to see if that helps you understand the condition better.

I hope that helps!

5

Reply
K
kapild.fb
Premium
• 3 months ago

This condition now makes the solution more understandable

if target > (nums[mid + k] + nums[mid]) / 2

Thanks, I will remember is now instead of rote learning .. haha

0

Reply
Samin Islam
Premium
• 6 months ago

Since the array is sorted target - nums[mid] and nums[mid + k] - target guarantees a positive number

1

Reply
P
PreviousBlueHawk549
Premium
• 13 days ago

Statement:  target - nums[mid]   >  nums[mid + k] - target

This statement literally means "Left side is farther from target  and Right side is closer to target" .i.e. difference/distance from target is reducing so we should continue move towards right.

else shift towards left.

0

Reply
M
mit
Premium
• 3 months ago

@Jimmy, could you help me understand what does

if (target - nums[mid] > nums[mid + k] - target)

actually do in the binary search solution? I've looked at the visualization and it makes sense but i don't understand the purpose of that. Is that if statement basically maintaining a K size range?

0

Reply
Janina
• 2 months ago
• edited 2 months ago

I found it confusing at first as well, but here’s a way to think about it. We’re sliding a fixed-size window of length k across our sorted array to find the elements closest to the target. The binary search in this case is not looking for the exact target, but rather for the starting index of that k-sized window.

python target - nums[mid]
The distance from the left end of the window to the target

python nums[mid + k] - target
The distance from the element just after the right end of the window to the target

If we define a distance function to make it more compact visually:

def distance(x, target):
    return abs(x - target)

if distance(nums[mid], target) > distance(nums[mid + k], target):
    # left end is farther: shift window right
else:
    # right end is closer: shift window left

So basically, if the left end of the window is farther from the target than the element just outside the right end, we move the window to the right by mid + 1 since both elements are k + 1 elements apart and cannot both be part of the same k-sized window (as in the description); otherwise, we move it to the left. After the binary search, the pointer left points to the starting index of the k closest elements within our window.

Show More

0

Reply
Abhay Singh
Top 1%
• 1 year ago

Java Solution: (Sliding Window)

class Solution {
    public List<Integer> findClosestElements(int[] arr, int k, int x) {
        int curSum = 0;
        int minSum = Integer.MAX_VALUE;

        int si = -1;

        int i=0, j=0;
        while(j < arr.length){
            curSum += Math.abs(arr[j] - x);

            if(j-i+1 == k){
                if(curSum < minSum){
                    minSum = curSum;
                    si = i;
                }
                curSum -= Math.abs(arr[i++] - x);
            }
            j++;
        }

        List<Integer> ans = new ArrayList<>();
        for(int idx=si;idx<si+k;idx++){
            ans.add(arr[idx]);
        }

        return ans;
    }
}
Show More

3

Reply
S
SpecialTomatoChicken155
Premium
• 1 month ago
• edited 1 month ago

Please add this condition in the question description as the solution uses this

*An integer a is closer to x than an integer b if:

|a - x| < |b - x|, or
|a - x| == |b - x| and a < b *

1

Reply
A
Abhi
Premium
• 5 months ago

In the max heap approach why is there no tiebreaker if the distances are equal for different indices?

1

Reply
S
SpecialTomatoChicken155
Premium
• 1 month ago
• edited 1 month ago

There is, although not explicit. A lower index at the same distance takes precedence which is apparent from this line "elif distance < -heap[0][0]:"

0

Reply
G
GlobalPinkUrial902
Premium
• 5 months ago

this should be moved to binary search

1

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

Approach 1: Sorting

Approach 2: Max-Heap

Solution

Bonus Approach: Two Pointers + Binary Search

Solution

Complexity Analysis
