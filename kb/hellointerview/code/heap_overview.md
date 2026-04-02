# Heap Overview

> Source: https://www.hellointerview.com/learn/code/heap/overview
> Scraped: 2026-03-30

Heap Overview
4:05
5 chapters • 3 interactive checkpoints
We can think of a heap as an array with a special property: the smallest value in the array is always in the first index of the array.
If we remove the smallest value from the heap, the elements of the array efficiently re-arrange so that the next smallest value takes its place at the front of the array.
Heaps are most frequently used in coding interviews to solve a class of problems known as "Top K" problems, which involve finding the k smallest or largest elements in a collection of elements.
This module prepares you to use heaps during the coding interview by covering:
How heaps are able to achieve their special property efficiently, which enable you to discuss heaps effectively during the interview.
How to use heaps in Python.
The types of coding interview questions that are best solved using heaps.
Heap Properties
Although we can think of a heap as an array, it's more helpful to visualize a heap as a binary tree. For example, we can visualize the heap [1, 2, 4, 5, 8, 6, 9] like this:
1
2
5
8
4
6
9
The elements correspond to a level-order traversal of the binary tree. The root of the binary tree is stored at index 0, its left and right children are stored at indices 1 and 2, respectively, and so on.
1
2
5
8
4
6
9
9
2
4
5
8
1
6
6
i = 2
1
2
3
4
5
0
i = 6
i = 1
i = 0
i = 3
i = 4
i = 5
The array representation is shown above the heap. Each node in the binary tree is labeled with the corresponding index in the array.
These two representations of a heap are equivalent. The binary tree representation is a more intuitive way to understand how a heap works. But during the coding interview, you will most likely be working with the array representation of a heap, as it more efficient to work with.
Our heap is a min-heap because the smallest value in the heap is at the root node (compare that to a max-heap, in which the largest value is at the root).
The binary tree satisfies the heap property: each node in the tree has a value that is less than or equal to the values of both its children.
1
2
5
8
4
6
9
Node 2 has a value that is less than both its children (5 and 8).
Any binary tree that satisfies the heap property is a heap:
1
2
4
8
5
9
6
1
8
4
2
5
9
X
6
Left: A valid heap, right: an invalid heap.
Heaps are complete binary trees, which means that all levels of the tree are fully filled except for the last level, which is filled from left to right.
1
2
4
8
5
9
1
8
4
2
X
5
6
Left: A valid heap, right: an invalid heap.
Since heaps are complete binary trees, the height of a heap is O(log n), where n is the number of elements in the heap. This is an important property to keep in mind when analyzing the time complexity of heap operations.
Max Heap
The heap property for a max heap is that each node has a value that is greater than or equal to the values of both its children.
9
8
4
6
5
2
1
Parent-Child Relationship
We can express the parent-child relationships of the binary tree representation of a heap using the indexes of the array. Given a node at index i in the array:
Node	Index
Left Child	2 * i + 1
Right Child	2 * i + 2
Parent	⌊(i - 1) / 2⌋ (floor division)
For example, for the node at index i = 2:
The left child 
L
 is at index 2 * 2 + 1 = 5:
The right child 
R
 is at index 2 * 2 + 2 = 6:
The parent 
P
 is at index ⌊(2 - 1) / 2⌋ = 0:
1
2
5
8
4
6
9
9
2
4
5
8
1
6
6
i = 2
1
2
3
4
5
0
i = 6
i = 1
i = 3
i = 4
i = 5
i = 0
R
L
P
P
Heap Operations
A heap supports the following operations:
push(element): Add a new element to the heap.
pop(): Remove the root element from the heap.
peek(): Get the root element without removing it.
heapify([elements]): Convert an array into a heap in-place.
We'll learn about each of these operations on a min-heap by visualizing how both the array and binary tree representation of a heap change after each operation. Doing so will help us understand the time complexity of each operation.
We omit the actual code implementation for these operations, as Python provides a built-in heapq module that you can use to create and manipulate heaps during your interviews.
However, understanding how the operations work conceptually allow you to discuss heaps at the level required for the interview. In particular, you need to know how these operations allow the heap to efficiently maintain the heap property.
Push
The push operation takes a new element and adds it to the heap. The element is added in a way such that the heap property is maintained.
We'll visualize each step of how the heap on the left changes after we add a new value of 3:
Step 1:
Add the new element to the next available position in the last level of the tree.
1
2
4
8
5
9
1
2
4
8
5
9
3
1
2
5
4
8
9
1
2
5
4
8
9
3
Step 2: "Bubble Up"
Compare the new element with its parent. If the new element is less than its parent, swap the two elements. Repeat this process until the new element is greater than its parent, or until it reaches the root of the heap.
1
2
4
8
5
9
3
1
2
4
8
3
9
5
1
2
5
4
8
9
3
1
2
3
4
8
9
5
Since the new element 3 is less than its parent 5, we swap the two values.
Time Complexity
The time complexity of the push operation is O(log n), where n is the number of items in the heap.
In the worst case, the new element will start at the last level of the tree and will "bubble-up" to the root, which takes O(log n) swaps, or the height of the tree. Since we are swapping indexes in an array, each swap operation takes O(1) time.
Pop
The pop operation removes and returns the minimum value from the heap. When the pop operation is complete, the new root of the heap is the new minimum value in the heap, and the heap property is restored.
We'll visualize each step of how the heap on the left changes after we remove the root element (1):
Step 1:
Remove the root element from the heap, and replace it with the last element in the heap (the rightmost node in the last level).
1
2
4
8
3
9
5
5
2
4
8
3
9
1
2
3
4
8
9
5
5
2
3
4
8
9
Replacing the root with Node 5.
Step 2: "Bubble Down"
Compare the new root with its children. If the new root is greater than either of its children, swap the root with the smaller of the two children. Repeat this process until the new root is less than both of its children, or until it reaches the last level of the heap.
5
2
4
8
3
9
2
5
4
8
3
9
5
2
3
4
8
9
2
5
3
4
8
9
Swapping the root (5) with its smaller child (2).
Time Complexity
The time complexity of the pop operation is O(log n), where n is the number of items in the heap.
In the worst case, after removing the root element, the new root starts at the top of the tree and "bubbles-down" to the last level of the tree, which takes O(log n) swaps, or the height of the tree.
Peek
The peek operation returns the minimum value in the heap without removing it. The minimum value is always the root of the heap.
Time Complexity
O(1): The peek operation has a constant time complexity since it only involves accessing the root of the heap, which is always index 0 in the array.
Heapify
The heapify operation takes a list of elements and converts it into a heap in O(n) time.
We'll start with [4, 6, 9, 3, 2, 8, 3] and convert it into a heap using the heapify operation:
4
6
3
2
9
8
3
The given array represented as a binary tree. Note this not yet a heap!
Step 1
Starting with the first non-leaf node (the parent of the last element in the array), compare the node with its children. If the node is greater than either of its children, swap the node with the smaller of the two children.
4
6
3
2
9
8
3
4
6
3
2
3
8
9
4
6
9
3
2
8
3
4
6
3
3
2
8
9
Starting with Node 9, we swap it with Node 3. The highlighted subtree is now a min-heap.
Step 2
Move to the next non-leaf node and repeat the process until the root of the tree is reached.
4
6
3
2
3
8
9
4
2
3
6
3
8
9
4
6
3
3
2
8
9
4
2
3
3
6
8
9
Moving onto Node 6, we swap it with Node 2. At this point, both the left and right subtrees of the heap are valid min-heaps.
4
2
3
6
3
8
9
2
4
3
6
3
8
9
4
2
3
3
6
8
9
2
4
3
3
6
8
9
Move to the root node, swap it with Node 2. At this point, the left subtree is not a valid min-heap.
2
4
3
6
3
8
9
2
3
4
6
3
8
9
2
4
3
3
6
8
9
2
3
3
4
6
8
9
Move to node 4, and swap it with Node 3. Our heap is now a min heap!
Time Complexity
O(n). The formal proof for the time complexity of the heapify operation is very math heavy, and beyond the scope of coding interviews, and thus, this lesson as well. If you're interested in learning more about the time complexity of the heapify operation, you can refer to the Wikipedia page.
Summary
If you only takeaway one thing from this section, remember that the pop and push operations both have a time complexity of O(log n). The worst case for each operation involves swapping elements from the root of the heap to the last level of the tree, or vice versa, which takes O(log n) time.
Operation	Time Complexity	Notes
pop	O(log n)	Visualize bubbling down the new root to the last level of the tree.
push	O(log n)	Visualize bubbling up the new element to the root of the tree.
peek	O(1)	Access the root of the heap.
heapify	O(n)	Just memorize this!
Python HeapQ Module
Python provides a built-in module called heapq that we can use to turn arrays into min-heaps.
The heapify function can be used to convert an array into a heap in-place. The heappush and heappop functions are used to push and pop elements from the heap, respectively.
Usage
SOLUTION
Python
Language
import heapq

arr = [3, 1, 4, 1, 5, 9, 2]

# convert array into a heap in-place. O(n)
heapq.heapify(arr)

# push 0 to the heap. O(log n)
heapq.heappush(arr, 0)

# peek the min element = 0. O(1)
arr[0]

# pop and return the min element = 0. O(log n)
min_element = heapq.heappop(arr)

# peek the new min element = 1. O(1)
arr[0]
Max Heap
By default, the heapq module creates a min-heap. To create a max-heap, we can negate the values in the list and then convert it into a heap using the heapify function. We also need to remember to negate the values when we push and pop elements from the heap.
SOLUTION
Python
Language
import heapq

arr = [3, 1, 4, 1, 5, 9, 2]

# negate the values in the array
negated_arr = [-x for x in arr]

# convert array into a min-heap
heapq.heapify(negated_arr) 

# push 11 to the heap by negating it
heapq.heappush(negated_arr, -11)

# peek root of heap = -11
negated_arr[0]

# pop and return the max element = -11
max_element = -heapq.heappop(negated_arr)

# peek the new max element = 9
negated_arr[0]
Storing Tuples
The heapq module can also be used to store tuples in the heap. By default, the heap is ordered based on the first element of the tuple. If the first elements are equal, the second elements are compared, and so on.
SOLUTION
Python
Language
import heapq

arr = [(3, 1), (1, 5), (4, 2), (1, 9), (5, 3), (9, 4), (2, 6)]
heapq.heapify(arr)

# pop and return the min element = (1, 5)
min_element = heapq.heappop(arr)

# peek the new min element = (1, 9)
arr[0]

# push (1, 7) to the heap, which is smaller than (1, 9)
heapq.heappush(arr, (1, 7))

# peek the min element = (1, 7)
arr[0]
Use Case
Top-K Largest Elements In An Array
Heaps are useful for solving problems that require finding the "top k" elements in an array. For example, let's use a heap to find the 3 largest elements in an array.
DESCRIPTION
Given an integer array nums, return the 3 largest elements in the array in any order.
Example
Input: nums = [9, 3, 7, 1, -2, 6, 8]
Output: [8, 7, 9]
# or [7, 9, 8] or [9, 7, 8] ...
Here's how we can solve this problem using a min-heap:
Create a min-heap that stores the first 3 elements of the array. These represent the 3 largest elements we have seen so far, with the smallest of the 3 at the root of the heap.
3
9
7
Iterate through the remaining elements in the array.
If the current element is larger than the root of the heap, pop the root and push the current element into the heap.
Otherwise, continue to the next element.
9
3
7
1
-2
6
8
num
3
9
7
9
3
7
1
-2
6
8
num
3
9
7
9
3
7
1
-2
6
8
num
6
9
7
Pop 3 from the heap and push 6.
9
3
7
1
-2
6
8
num
7
9
8
Pop 6 from the heap and push 8.
After iterating through all the elements, the heap contains the 3 largest elements in the array.
Solution
SOLUTION
Python
Language
import heapq

def three_largest(nums):
    # create a min-heap with the first 3 elements
    heap = nums[:3]
    heapq.heapify(heap)
    
    # iterate through the remaining elements
    for num in nums[3:]:
        if num > heap[0]:
            heapq.heappop(heap)
            heapq.heappush(heap, num)
    
    return heap
What is the time complexity of this solution?
1

O(n²)

2

O(m * n * 4^L)

3

O(n)

4

O(4^L)

Mark as read

Next: Kth Largest Element in an Array

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

(37)

Comment
Anonymous
​
Sort By
Popular
Sort By
Eric Lloyd
Top 10%
• 11 months ago

The diagram demonstrating Pop is incorrect -- the initial state of the heap is invalid. The 3 is a branch of the 5, instead of the other way around.

It looks like you improperly recycled the diagram from the Bubble-Up phase of the Push operation.

22

Reply
Q
QuickestIndigoCanid988
Top 10%
• 1 year ago

I feel like the intuition completely goes out of the window when we get to the use case. We're trying to get the top K largest elements, so naturally we'd expect to use a max heap. Instead in this example we're using a min heap? Maybe it's just me but it feels like there's a big leap to min heap without any reason why.

I found a great video here that explains the motivation behind the min-heap approach - in case anyone else was confused:
https://www.youtube.com/watch?v=ZmGk7h8KZLs

21

Reply
Stanley Lin
• 2 months ago

What if we just negate the numbers, and heapify the array to get a max heap and then take the first three and reverse the negation. You would still get O(N) time

0

Reply
S
selectfromall
Top 5%
• 1 year ago

Can you fix the complexity analysis? The question asks for top K, so interviewees should calculate the time complexity relative to N and K:

Time: O(NlogK)
Space: O(K)

18

Reply
E
ElaborateAmethystWoodpecker542
• 1 year ago

heapq has a function called heappushpop, which results in a better performance compared to doing it separately.

https://docs.python.org/3/library/heapq.html

8

Reply
I
IntellectualMoccasinCamel649
• 1 year ago

Good to know!

0

Reply
Mohamed Niyaz
• 2 months ago
• edited 2 months ago

Timecomplexity should be O(n * log K) if K=3

2

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Heap Properties

Parent-Child Relationship

Heap Operations

Push

Pop

Peek

Heapify

Summary

Python HeapQ Module

Use Case