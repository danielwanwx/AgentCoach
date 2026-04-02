# Merge K Sorted Lists

> Source: https://www.hellointerview.com/learn/code/heap/merge-k-sorted-lists
> Scraped: 2026-03-30


Heap
Merge K Sorted Lists
hard
DESCRIPTION (inspired by Leetcode.com)

Given k linked lists, each sorted in ascending order, in a list lists, write a function to merge the input lists into one sorted linked list.

Example 1:

Inputs:

lists = [[3,4,6],[2,3,5],[-1,6]]
3 -> 4 -> 6
2 -> 3 -> 5
-1 -> 6

Output:

[-1,2,3,3,4,5,6,6]

-1 -> 2 -> 3 -> 3 -> 4 -> 5 -> 6 -> 6

CODE EDITOR
Python
​
Full Screen
1
2
3
4
5
6
7
8
9
# class ListNode:
#     def __init__(self, val: int = 0, next: 'ListNode' = None):
#         self.val = val
#         self.next = next
class Solution:
    def mergeKLists(self, lists: List[ListNode]) -> ListNode:
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
This problem can be solved using a min-heap of size k.
The min-heap will always store the next unmerged element from each of the k sorted arrays. The element with the smallest value sits at the root of the heap. We build the merged array by repeatedly popping the root from the heap. Each time we pop from the heap, we also push the next element from the same array (if one exists) onto the heap.
When the heap is empty, all elements from all arrays have been merged, and we can return the merged result.
Step 1: Initialize The Heap
The first step is to initialize the heap with the first element from each of the k arrays. We iterate over each array and push a tuple containing three values onto the heap:
The element's value
The array's index (which array it came from)
The element's index within that array (starting at 0)
VISUALIZATION
Python
Language
Full Screen
from heapq import heappush, heappop

def mergeKLists(lists):
  if not lists:
    return None
  
  non_empty = [head for head in lists if head]
  if not non_empty:
    return None
  
  heap = []
  for head in non_empty:
    heappush(heap, (head.val, id(head), head))
  
  dummy = ListNode(0)
  current = dummy
  
  while heap:
    val, _, node = heappop(heap)
    current.next = node
    current = current.next
    
    if node.next:
      heappush(heap, (node.next.val, id(node.next), node.next))
  
  return dummy.next
3
4
6
2
3
5
-1
6

initialize heap

0 / 3

1x
Step 2: Build The Merged Array
With the heap initialized, we can now build the merged result array. We start by creating an empty result array where we'll append elements in sorted order.
VISUALIZATION
Python
Language
Full Screen
from heapq import heappush, heappop

def mergeKLists(lists):
  if not lists:
    return None
  
  non_empty = [head for head in lists if head]
  if not non_empty:
    return None
  
  heap = []
  for head in non_empty:
    heappush(heap, (head.val, id(head), head))
  
  dummy = ListNode(0)
  current = dummy
  
  while heap:
    val, _, node = heappop(heap)
    current.next = node
    current = current.next
    
    if node.next:
      heappush(heap, (node.next.val, id(node.next), node.next))
  
  return dummy.next
3
4
6
2
3
5
-1
6
-1,2,0
3,0,0
2,1,0

add -1 to heap

0 / 1

1x
Now, we repeatedly pop the root of the heap, which gives us the element with the smallest value among the unmerged elements from the k arrays. We append this value to our result array.
VISUALIZATION
Python
Language
Full Screen
from heapq import heappush, heappop

def mergeKLists(lists):
  if not lists:
    return None
  
  non_empty = [head for head in lists if head]
  if not non_empty:
    return None
  
  heap = []
  for head in non_empty:
    heappush(heap, (head.val, id(head), head))
  
  dummy = ListNode(0)
  current = dummy
  
  while heap:
    val, _, node = heappop(heap)
    current.next = node
    current = current.next
    
    if node.next:
      heappush(heap, (node.next.val, id(node.next), node.next))
  
  return dummy.next
3
4
6
2
3
5
-1
6
-1,2,0
3,0,0
2,1,0
0
curr

initialize result array

0 / 1

1x
To ensure that our heap always contains the next unmerged element from each array, after popping an element, we check if there's a next element in the same array. If there is, we push a tuple with the next element's value, the same array index, and the incremented element index onto the heap.
VISUALIZATION
Python
Language
Full Screen
from heapq import heappush, heappop

def mergeKLists(lists):
  if not lists:
    return None
  
  non_empty = [head for head in lists if head]
  if not non_empty:
    return None
  
  heap = []
  for head in non_empty:
    heappush(heap, (head.val, id(head), head))
  
  dummy = ListNode(0)
  current = dummy
  
  while heap:
    val, _, node = heappop(heap)
    current.next = node
    current = current.next
    
    if node.next:
      heappush(heap, (node.next.val, id(node.next), node.next))
  
  return dummy.next
3
4
6
2
3
5
-1
6
2,1,0
3,0,0
0
-1
curr

add -1 to result

0 / 1

1x
When the heap is empty, all elements from all arrays have been merged, and we can return the result array.
VISUALIZATION
Python
Language
Full Screen
from heapq import heappush, heappop

def mergeKLists(lists):
  if not lists:
    return None
  
  non_empty = [head for head in lists if head]
  if not non_empty:
    return None
  
  heap = []
  for head in non_empty:
    heappush(heap, (head.val, id(head), head))
  
  dummy = ListNode(0)
  current = dummy
  
  while heap:
    val, _, node = heappop(heap)
    current.next = node
    current = current.next
    
    if node.next:
      heappush(heap, (node.next.val, id(node.next), node.next))
  
  return dummy.next
3
4
6
2
3
5
-1
6
0
-1
2
3
3
4
5
6
6
curr

add 6 to result

0 / 1

1x
Solution
lists
​
|
lists
list of integers
Try these examples:
One List
Three Short
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
from heapq import heappush, heappop

def mergeKLists(lists):
  if not lists:
    return None
  
  non_empty = [head for head in lists if head]
  if not non_empty:
    return None
  
  heap = []
  for head in non_empty:
    heappush(heap, (head.val, id(head), head))
  
  dummy = ListNode(0)
  current = dummy
  
  while heap:
    val, _, node = heappop(heap)
    current.next = node
    current = current.next
    
    if node.next:
      heappush(heap, (node.next.val, id(node.next), node.next))
  
  return dummy.next
3
4
6
2
3
5
-1
6

merge k sorted arrays

0 / 19

1x
What is the time complexity of this solution?
1

O(N + Q)

2

O(4ⁿ)

3

O(2ⁿ)

4

O(n * log k)

Mark as read

Next: Find Median from Data Stream

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

(22)

Comment
Anonymous
​
Sort By
Popular
Sort By
Nathan Li
Premium
• 5 months ago
class Solution:
    def mergeKLists(self, lists: List[List[int]]):

How come this lists is a list of int, this is very misleading, it should be a List[Node]

7

Reply
Abhay Singh
Top 1%
• 1 year ago

Java Solution: PriorityQueue and MergeSort

class Solution {
    public ListNode mergeKLists(ListNode[] lists) {
        PriorityQueue<ListNode> pq = new PriorityQueue<>((a, b) -> Integer.compare(a.val, b.val));
        for(ListNode node : lists){
            if(node != null){
                pq.add(node);
            }
        }

        ListNode head, tail;
        head = tail = new ListNode(-1);

        while(!pq.isEmpty()){
            ListNode cur = pq.poll();

            tail.next = cur;
            if(cur.next != null){
                pq.add(cur.next);
            }
            tail = tail.next;
        }

        return head.next;
    }
}
class Solution {
    
    public ListNode merge(ListNode h1, ListNode h2){
        ListNode head, tail;
        head = tail = new ListNode(-1);

        while(h1!=null || h2!=null){
            int val1 = (h1 == null ? Integer.MAX_VALUE : h1.val);
            int val2 = (h2 == null ? Integer.MAX_VALUE : h2.val);

            if(val1 <= val2){
                tail.next = h1;
                h1 = h1.next;
            }else{
                tail.next = h2;
                h2 = h2.next;
            }

            tail = tail.next;
        }

        return head.next;
    }

    public ListNode mergeSort(ListNode[] lists, int l, int r){
        if(l > r) return null;
        if(l == r) return lists[l];

        int m = l + (r-l)/2;
        ListNode left = mergeSort(lists, l, m);
        ListNode right = mergeSort(lists, m+1, r);

        return merge(left, right);
    }

    public ListNode mergeKLists(ListNode[] lists) {
        return mergeSort(lists, 0, lists.length-1);
    }
}
Show More

5

Reply
Shannon Monasco
• 1 year ago

Can you set this up so that we can try it before reading the solution?

4

Reply
Chang Liu
Premium
• 4 months ago

Just FYI, the question, stub functions and explanations bounce around between arrays and linked lists.

2

Reply

Shivam Chauhan

Admin
• 4 months ago

Thanks for pointing this out! This is fixed and will be live in next release!

0

Reply
I
InnovativeCyanAntelope719
Top 5%
• 11 months ago

We don't need idx in there.

import heapq

class Solution(object):
    def mergeKLists(self, lists):
        """
        :type lists: List[Optional[ListNode]]
        :rtype: Optional[ListNode]
        """
        if not lists:
            return None
        
        heap = []
        for node in lists:
            if node: 
                heapq.heappush(heap, (node.val, node))
        
        dummy = ListNode(0)
        curr = dummy

        while heap: 
            value, node = heapq.heappop(heap)
            curr.next = node
            curr = curr.next

            if node.next:
                heapq.heappush(heap, (node.next.val, node.next))
        
        return dummy.next
Show More

1

Reply
Nathan Li
Premium
• 5 months ago
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        # Your code goes here
        if not lists:
            return None

        heap = []
        counter = count()  #tie-breaker
        for i, node in enumerate(lists):
            if node:
                heapq.heappush(heap, (node.val, next(counter), node))

        dummy = ListNode(0)
        curr = dummy

        while heap:
            val, i,  node = heappop(heap)
            curr.next = node
            curr = curr.next

            if node.next:
                heapq.heappush(heap, (node.next.val, next(counter), node.next))

        return dummy.next
Show More

0

Reply
Nathan Li
Premium
• 5 months ago

I think without idx you will get this

TypeError: '<' not supported between instances of 'ListNode' and 'ListNode'
    heapq.heappush(heap, (node.val,node))

0

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

Step 1: Initialize the heap

Step 2: Build the merged array

Solution
