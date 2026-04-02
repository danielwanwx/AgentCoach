# Kth Smallest Element in a Sorted Matrix

> Source: https://www.hellointerview.com/learn/code/binary-search/kth-smallest-element-in-a-sorted-matrix
> Scraped: 2026-03-30


Binary Search
Kth Smallest Element in a Sorted Matrix
medium
DESCRIPTION (inspired by Leetcode.com)

You're given a square grid (n × n matrix) where each row is sorted in ascending order from left to right, and each column is also sorted in ascending order from top to bottom.

Given the matrix and an integer k, find the k-th smallest element among all elements in the matrix.

Note: k is 1-indexed, meaning k = 1 returns the smallest element.

Example 1:

Input:

matrix = [
    [ 1, 5, 9],
    [10,11,13],
    [12,13,15]]
k = 8

Output: 13

Explanation: The elements in sorted order are [1,5,9,10,11,12,13,13,15]. The 8th smallest element is 13.

Example 2:

Input:

matrix = [[-5]], k = 1

Output: -5

Explanation: The matrix has only one element, so it's the 1st smallest.

CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def kthSmallest(self, matrix: List[List[int]], k: int) -> int:
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

Building Intuition
3×3 Matrix (each row and column sorted)
1
5
9
10
11
13
12
13
15
rows sorted →
cols
sorted
↓
k = 8
Sorted: 1,5,9,10,11,12,13,13,15
Answer: 13 (8th smallest)
The matrix has a powerful property: we always know the minimum (matrix[0][0]) and maximum (matrix[n-1][n-1]) values. But finding the k-th smallest isn't straightforward because elements aren't globally sorted rather they're only sorted within each row and column.
Approach 1: Brute Force (Flatten and Sort)
The simplest idea is to collect all elements into a single array, sort it, and return the k-th element.
kthSmallest(matrix, k)
    allElements = []
    for each row in matrix
        for each element in row
            allElements.append(element)
    
    sort(allElements)
    return allElements[k - 1]
This works, but it throws away the matrix's sorted structure entirely. For an n × n matrix, we have n² elements, giving us O(n² log n²) time complexity.
Can We Use Binary Search?
The matrix has sorted rows and columns, so can we use binary search? We could have use it directly but the problem is that the traditional binary search works only on a globally sorted array where we can compare our target to the middle element and eliminate half the search space.
Here, the matrix isn't globally sorted. Look at this example:
[ 1,  3, 11]
[ 2,  6, 15]
[ 5, 10, 20]
If we pick the "middle" element (6) and want to find where 5 belongs, we can't eliminate half the search space. Is 5 to the left of 6? Yes (3 is left, then 1). But 5 is also below 6 (5 is left below). Elements smaller than 6 scatter in multiple directions: left (1, 3, 2), above-left (1, 3), and even below-left (5).
Traditional binary search assumes sorted order where "smaller" consistently means "go left" or "go up." That property doesn't exist here.
So traditional binary search on position won't work.
Observation
But instead of checking current element being smaller or greater than left or right, we see how many elements are less than current number, we can optimise for it. For example, let's say we pick mid = 11. We can count how many elements are ≤ 11. And here's the crucial property: if there are exactly k elements ≤ 11, then 11 might be our answer.
Even better: this counting property is monotonic. If 6 elements are ≤ 11, then we know:
At least 6 elements are ≤ 12
At least 6 elements are ≤ 13
And so on...
Counting Property: count(value) is monotonically increasing
value = 9
count = 3
value = 11
count = 5
value = 13
count = 8
value = 14
count = 8
value = 15
count = 9
As value increases, count never decreases → perfect for binary search!
This monotonicity means we CAN use binary search, but not on the matrix positions. Instead, we binary search on the value space itself.
Binary Search on the Value
Here's the reframed question: Instead of finding "what is the k-th smallest element?", we find: "for a given value mid, how many elements in the matrix are ≤ mid?"
1
min
15
max
13
k-th smallest
Question:
How many values
are ≤ mid?
If count ≥ k,
answer is ≤ mid
Now we can binary search the value space: find the smallest value where count(value) ≥ k. That value must be our k-th smallest element!
This pattern is called "Binary Search on Answer." Instead of binary searching through array positions, we binary search through the space of possible answer values (min to max). The key requirement: the predicate function must be monotonic. Here, count(value) ≥ k is monotonic because as value increases, count never decreases.
Counting Elements ≤ mid
The matrix's sorted structure lets us count elements ≤ mid in O(n) time using a "staircase" traversal. Start from the bottom-left corner:
Counting elements ≤ 11
1
5
9
10
11
13
12
13
15
start here
Staircase Algorithm:
1. Start at bottom-left (row=n-1, col=0)
2. If matrix[row][col] ≤ mid:
→ All elements above are ≤ mid too
→ Add (row+1) to count, move right
3. If matrix[row][col] > mid:
→ Move up (smaller values)
Count: 2 + 3 = 5 elements ≤ 11
If matrix[row][col] ≤ mid: All elements above in that column are also ≤ mid (column is sorted!). Add row + 1 to our count, then move right.
If matrix[row][col] > mid: Move up to find smaller values.
This traverses at most 2n cells (n moves right + n moves up), giving us O(n) counting!
Putting It Together
1. Initialize
left = matrix[0][0]
right = matrix[n-1][n-1]
(min and max values)
2. Binary Search
mid = (left + right) / 2
count = countLessOrEqual
(matrix, mid)
3. Narrow Search
count ≥ k?
Yes → right = mid
No → left = mid + 1
4. Return
left
kthSmallest(matrix, k)
    n = matrix.length
    left = matrix[0][0]
    right = matrix[n-1][n-1]
    
    while left < right
        mid = (left + right) / 2
        count = countLessOrEqual(matrix, mid)
        
        if count >= k
            right = mid
        else
            left = mid + 1
    
    return left
countLessOrEqual(matrix, target)
    n = matrix.length
    count = 0
    row = n - 1
    col = 0
    
    while row >= 0 and col < n
        if matrix[row][col] <= target
            count = count + row + 1
            col = col + 1
        else
            row = row - 1
    
    return count
Walkthrough
We'll trace through matrix = [[1, 5, 9], [10, 11, 13], [12, 13, 15]] with k = 8 to see exactly how binary search finds the 8th smallest element.
Step 1: Initialize the search bounds
We start by establishing our search space. The minimum value in the matrix is at the top-left: matrix[0][0] = 1. The maximum is at the bottom-right: matrix[2][2] = 15.
Step 1:
Initialize search bounds
left=1
right=15
Search space: [1, 15]
Our search space is the range of possible values [1, 15]. The answer (the 8th smallest) must lie somewhere in this range.
Step 2: First binary search iteration
We calculate mid = (1 + 15) / 2 = 8. Now we count how many elements are ≤ 8 using the staircase method.
Starting at (row=2, col=0):
matrix[2][0] = 12 > 8 → move up, row = 1
matrix[1][0] = 10 > 8 → move up, row = 0
matrix[0][0] = 1 ≤ 8 → count += 0 + 1 = 1, move right, col = 1
matrix[0][1] = 5 ≤ 8 → count += 0 + 1 = 1, move right, col = 2
matrix[0][2] = 9 > 8 → move up, row = -1, exit loop
Total count = 2 elements ≤ 8. Since 2 < k = 8, we need to search higher values. Set left = mid + 1 = 9.
Step 2:
mid = 8, count = 2 < k=8 → search higher
left=1
mid=8
right=15
left = 9
Step 3: Second iteration
Now left = 9, right = 15. Calculate mid = (9 + 15) / 2 = 12.
Count elements ≤ 12 using staircase from (2, 0):
matrix[2][0] = 12 ≤ 12 → count += 3, col = 1
matrix[2][1] = 13 > 12 → row = 1
matrix[1][1] = 11 ≤ 12 → count += 2, col = 2
matrix[1][2] = 13 > 12 → row = 0
matrix[0][2] = 9 ≤ 12 → count += 1, col = 3, exit loop
Total count = 3 + 2 + 1 = 6 elements ≤ 12. Since 6 < k = 8, search higher. Set left = 13.
Step 3:
mid = 12, count = 6 < k=8 → search higher
left=9
mid=12
right=15
left = 13
Step 4: Third iteration
Now left = 13, right = 15. Calculate mid = (13 + 15) / 2 = 14.
Count elements ≤ 14:
matrix[2][0] = 12 ≤ 14 → count += 3, col = 1
matrix[2][1] = 13 ≤ 14 → count += 3, col = 2
matrix[2][2] = 15 > 14 → row = 1
matrix[1][2] = 13 ≤ 14 → count += 2, col = 3, exit loop
Total count = 3 + 3 + 2 = 8 elements ≤ 14. Since 8 >= k = 8, we found a valid answer! But maybe there's a smaller value that also works. Set right = mid = 14.
Step 4:
mid = 14, count = 8 ≥ k=8 → search lower
left=13
mid=14
right=15
right = 14
Step 5: Fourth iteration
Now left = 13, right = 14. Calculate mid = (13 + 14) / 2 = 13.
Count elements ≤ 13:
matrix[2][0] = 12 ≤ 13 → count += 3, col = 1
matrix[2][1] = 13 ≤ 13 → count += 3, col = 2
matrix[2][2] = 15 > 13 → row = 1
matrix[1][2] = 13 ≤ 13 → count += 2, col = 3, exit loop
Total count = 3 + 3 + 2 = 8 elements ≤ 13. Since 8 >= k = 8, set right = 13.
Now left = right = 13, so we're done!
Step 5:
Converged: left = right = 13
Answer: 13
Result: 13
The 8th smallest element in the matrix is 13. If we list all elements in sorted order: 1, 5, 9, 10, 11, 12, 13, 13, 15, the 8th element is indeed 13.
Solution
matrix
​
|
matrix
2d-list of integers
k
​
|
k
1 to 9
Try these examples:
2x2
3x3
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def kthSmallest(matrix, k):
    n = len(matrix)
    left = matrix[0][0]
    right = matrix[n-1][n-1]
    
    while left < right:
        mid = (left + right) // 2
        count = countLessOrEqual(matrix, mid)
        if count >= k:
            right = mid
        else:
            left = mid + 1
    
    return left

def countLessOrEqual(matrix, target):
    n = len(matrix)
    count = 0
    row = n - 1
    col = 0
    while row >= 0 and col < n:
        if matrix[row][col] <= target:
            count += row + 1
            col += 1
        else:
            row -= 1
    return count
1
5
9
10
11
13
12
13
15
0
1
2
0
1
2
left: —
mid: —
right: —
count: —
Counted
Matrix cell

Find the 8-th smallest element in the 3×3 matrix

0 / 62

1x
Binary search on value with staircase counting
What is the time complexity of this solution?
1

O(4ⁿ)

2

O(V + E)

3

O(n * log(max - min))

4

O(log m * n)

Why Does This Work?
The binary search finds the smallest value v where countLessOrEqual(v) >= k. This must be the k-th smallest because:
If the count is exactly k, then v is the k-th smallest
If the count is greater than k, then v appears multiple times in the matrix, and at least one occurrence is the k-th smallest
When you see a problem involving "k-th smallest/largest" in a sorted matrix, consider binary search on the value. Recognize that the sorted row/column property gives you an efficient way to count elements in the staircase traversal pattern.
Alternate Solution: Min-Heap
There's another approach that uses a min-heap. Since each row and column is sorted, we can treat this like merging n sorted lists.
Start by pushing the top-left element (value, row, col) onto a min-heap. Then pop the smallest element k times, and each time we pop from position (row, col), push the element to the right (row, col+1) if it exists and hasn't been visited.
We will be discussing heap in next section.

Mark as read

Next: Minimum Shipping Capacity

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

(10)

Comment
Anonymous
M
MeltedAmberPiranha299
Top 10%
• 1 month ago

TBH the binary search solution for this problem feels more like a hard. The analysis required to get the right insight into the solution space to bisect on requires some level of mastery of binary search IMO. Nice write up.

11

Reply
K
kapild.fb
Premium
• 2 months ago

Thanks for adding new questions. I am wondering if there is a way we can get notified (via email) that the following questions were recently added. I just logged on the website and I found these these questions and now I am having FOMO.

1

Reply

Shivam Chauhan

Admin
• 2 months ago

Hey, I am glad you are liking our new questions!
Newly Released Content is shown on the Dashboard, and on the Changelog.
You are correct and these will be included in email updates soon. Btw, if you haven't joined already, we do regular Product Announcements on our Discord which might be helpful for updates.

1

Reply
Michael Genchev
Premium
• 3 days ago

blem

problem*

0

Reply
Joel Wang
Premium
• 1 month ago
class Solution:
    def kthSmallest(self, matrix: List[List[int]], k: int):
        # Your code goes here
        n = len(matrix)

        def num_elem(target):
            row, col = n - 1, 0
            count = 0
            while row >= 0 and col < n:
                if matrix[row][col] <= target:
                    count += row + 1
                    col += 1
                else:
                    row -= 1
            return count
     

        left, right = matrix[0][0], matrix[n-1][n-1]
        res = left
        while left <= right:
            mid = (left + right) // 2
            num = num_elem(mid)
            if num >= k:
                res = mid
                right = mid - 1
            else:
                left = mid + 1

        return res
Show More

0

Reply
vivian W
Premium
• 1 month ago

how to guarantee the smallest val we found through value space binary search where count(val) >= k exist in matrix?

0

Reply
leonel paulino
Premium
• 1 month ago

Maybe an example could help:
Consider the array [1, 2, 2, 3, 4, 5].
count(3) = 4 because there are four numbers less than or equal to 3.
For any number smaller than 3, the count must be strictly less than 4. We can see that with count(2) = 3.
Now look at [1, 2, 2, 4, 5], where 3 is missing.
count(3) = 3
count(2) = 3
In this case, two different values share the same count because one value is not present in the array.

Therefore:
The smallest number that satisfies count(value) ≥ k must actually exist in the matrix because if it doesn't, then there has to be a smaller number that also satisfies the condition.

4

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Building Intuition

Approach 1: Brute Force (Flatten and Sort)

Can We Use Binary Search?

Observation

Binary Search on the Value

Counting Elements ≤ mid

Putting It Together

Walkthrough

Solution

Why Does This Work?

Alternate Solution: Min-Heap
