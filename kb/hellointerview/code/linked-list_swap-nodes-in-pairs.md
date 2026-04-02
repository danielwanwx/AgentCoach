# Swap Nodes in Pairs

> Source: https://www.hellointerview.com/learn/code/linked-list/swap-nodes-in-pairs
> Scraped: 2026-03-30


Linked List
Swap Nodes in Pairs
medium
DESCRIPTION (inspired by Leetcode.com)

Given a reference head of type ListNode that is the head of a singly linked list, write a function to swap every two adjacent nodes and return its head.

You must solve the problem without modifying the values in the list's nodes (i.e., only nodes themselves may be changed.)

Example 1: input:

5
4
3
2
1
head

output:

4
5
2
3
1
head

Explanation: 5 and 4 are swapped, 3 and 2 are swapped, and 1 is left alone.

Example 2: input:

1
2
3
4
head

output:

2
1
4
3
head

Explanation: 1 and 2 are swapped, 3 and 4 are swapped.

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
    def swapPairs(self, head: ListNode) -> ListNode:
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

Solution
Since we can't modify the values in the nodes, our function needs to swap the nodes by traversing the list and updating the next pointers of the nodes.
This question is an example of how using a dummy node simplifies a solution by removing the need for special logic for swapping the first two nodes in the list. To understand why, let's first look at how to swap a pair of nodes in a linked list.
Let's say we want to swap the pair of nodes first and second in the linked list below:
5
4
3
2
1
first
second
We need to perform 3 operations:
1). Since we need the node before first to point to second instead of first, we need a pointer prev which references the node before first. Then, we can update prev.next to point to second.
5
4
3
2
1
prev
first
second
2). We need to update first.next to point to second.next.
5
4
3
2
1
prev
first
second
3). Finally, we need to update second.next to point to first.
5
4
3
2
1
prev
first
second
Once that is complete, we can move to the next pair of nodes to swap.
Need For A Dummy Node
As we just saw, swapping a pair of nodes requires a pointer to node before the first node in the pair we want to swap. This is not a problem when we are swapping nodes in the middle of the list, but it is when we are swapping the first pair of nodes in the list because there is no node before head!
We fix this by introducing a dummy node that points to the head of the list. This guarantees that each node in the original list has a node before it, meaning we can swap all nodes in the list using the same logic.
VISUALIZATION
Python
Language
Full Screen
def swapPairs(head):
    dummy = ListNode(0)
    dummy.next = head
    tail, first = dummy, head
    
    while first and first.next:
        second = first.next
        
        # swap nodes
        tail.next = second
        first.next = second.next
        second.next = first
        
        tail = first
        first = first.next
    
    return dummy.next
5
4
3
2
1

swap nodes in pairs

0 / 1

1x
From there, we can initialize two pointers, prev and first. first will point to the first node in the pair we want to swap, and prev points to the node before first, which is the dummy node to start. We also initialize the pointer second to point to the node after first.
VISUALIZATION
Python
Language
Full Screen
def swapPairs(head):
    dummy = ListNode(0)
    dummy.next = head
    tail, first = dummy, head
    
    while first and first.next:
        second = first.next
        
        # swap nodes
        tail.next = second
        first.next = second.next
        second.next = first
        
        tail = first
        first = first.next
    
    return dummy.next
5
4
3
2
1
0
dummy
tail

create dummy node and initialize pointers

0 / 2

1x
We then perform the same 3 operations we discussed earlier to swap the pair of nodes:
1). Update prev.next to point to second.
2). Update first.next to point to second.next.
3). Update second.next to point to first.
VISUALIZATION
Python
Language
Full Screen
def swapPairs(head):
    dummy = ListNode(0)
    dummy.next = head
    tail, first = dummy, head
    
    while first and first.next:
        second = first.next
        
        # swap nodes
        tail.next = second
        first.next = second.next
        second.next = first
        
        tail = first
        first = first.next
    
    return dummy.next
5
4
3
2
1
0
first
dummy
tail

swapped: 4 -> 5

0 / 3

1x
Now, with first and second swapped, we move prev and first to prepare for the next iteration. first now points to the node right before the next pair of nodes, so we update prev to point to first and first to point to first.next. After that, we update second to point to first.next, and our pointers are in the same state to perform the same 3 operations to swap the next pair of nodes.
VISUALIZATION
Python
Language
Full Screen
def swapPairs(head):
    dummy = ListNode(0)
    dummy.next = head
    tail, first = dummy, head
    
    while first and first.next:
        second = first.next
        
        # swap nodes
        tail.next = second
        first.next = second.next
        second.next = first
        
        tail = first
        first = first.next
    
    return dummy.next
5
4
3
2
1
0
tail
first
dummy

swapped: 2 -> 3

0 / 2

1x
Termination
We can stop the loop when first is None, or when first.next is None. When there an even number of nodes in the list, first will be None when all pairs of nodes have been swapped. When there is an odd number of nodes, first.next will be None when first is at the last node in the list, which we can't swap.
After the loop terminates, we return dummy.next, which is the head of the list with all pairs of nodes swapped.
VISUALIZATION
Python
Language
Full Screen
def swapPairs(head):
    dummy = ListNode(0)
    dummy.next = head
    tail, first = dummy, head
    
    while first and first.next:
        second = first.next
        
        # swap nodes
        tail.next = second
        first.next = second.next
        second.next = first
        
        tail = first
        first = first.next
    
    return dummy.next

0 / -1

1x
Implementation
Here's the complete dummy node approach that elegantly handles all edge cases:
SOLUTION
Python
Language
def swapPairs(head):
    # Create dummy node to simplify edge cases
    dummy = ListNode(0)
    dummy.next = head
    prev = dummy
    
    # Process pairs while both nodes exist
    while prev.next and prev.next.next:
        # Identify the two nodes to swap
        first = prev.next
        second = prev.next.next
        
        # Perform the swap by adjusting pointers
        prev.next = second        # Link previous to second node
        first.next = second.next  # Link first to node after second
        second.next = first       # Link second to first (completing swap)
        
        # Move prev to the end of swapped pair for next iteration
        prev = first
    
    return dummy.next  # Return new head
Code
To construct the linked list that is used in the animation below, provide a list of integers nodes. Each integer in nodes is used as the value of a node in the linked list, and the order of the integers in nodes will be the order of the nodes in the linked list.
For example, if nodes = [1, 2, 3], the linked list will be 1 -> 2 -> 3.
nodes
​
|
nodes
list of integers
Try these examples:
Even
Odd
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def swapPairs(head):
    dummy = ListNode(0)
    dummy.next = head
    tail, first = dummy, head
    
    while first and first.next:
        second = first.next
        
        # swap nodes
        tail.next = second
        first.next = second.next
        second.next = first
        
        tail = first
        first = first.next
    
    return dummy.next
5
4
3
2
1

swap nodes in pairs

0 / 10

1x
Edge Cases
Empty List
When the list is empty, head is None. The while loop never runs, and we return dummy.next, which is equal to None.
nodes
​
|
nodes
list of integers
Try these examples:
Even
Odd
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def swapPairs(head):
    dummy = ListNode(0)
    dummy.next = head
    tail, first = dummy, head
    
    while first and first.next:
        second = first.next
        
        # swap nodes
        tail.next = second
        first.next = second.next
        second.next = first
        
        tail = first
        first = first.next
    
    return dummy.next

swap nodes in pairs

0 / 3

1x
`head = []`
One Node
When there is only one node in the list, first is the only node in the list, and first.next is None. The while loop never runs, and we return dummy.next, which is head with the single node.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def swapPairs(head):
    dummy = ListNode(0)
    dummy.next = head
    tail, first = dummy, head
    
    while first and first.next:
        second = first.next
        
        # swap nodes
        tail.next = second
        first.next = second.next
        second.next = first
        
        tail = first
        first = first.next
    
    return dummy.next
1

swap nodes in pairs

0 / 4

1x
`head = [1]`
Two Nodes
When there are two nodes in the list, first is the first node, and second is the second node. The while loop runs once to swap the two nodes, after which fast is None so the loop terminates. We return dummy.next, which is the head of the list with the two nodes swapped.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def swapPairs(head):
    dummy = ListNode(0)
    dummy.next = head
    tail, first = dummy, head
    
    while first and first.next:
        second = first.next
        
        # swap nodes
        tail.next = second
        first.next = second.next
        second.next = first
        
        tail = first
        first = first.next
    
    return dummy.next
1
2

swap nodes in pairs

0 / 7

1x
`head = [1, 2]`
What is the time complexity of this solution?
1

O(n!)

2

O(m * n)

3

O(n)

4

O(4ⁿ)

Mark as read

Next: Binary Search Overview

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
A
addresseerajat
• 1 year ago

Hello folks,
The animations and visualizations are not in sync. Could you please take a look ?

10

Reply
Abhay Singh
Top 1%
• 1 year ago

Java Solution:

class Solution {
    public ListNode swapPairs(ListNode head) {
        if(head==null || head.next==null){
            return head;
        }

        ListNode  subList = swapPairs(head.next.next);
        ListNode newHead = head.next;
        newHead.next = head;
        head.next = subList;

        return newHead;
    }
}

3

Reply
S
StrictGrayChickadee213
• 9 months ago

Just asking if we use this recursion solution.
Space complexity will be O(n/2), so the iterative way is preferred over recursion?

0

Reply
L
LesserTanMite551
Top 10%
• 1 year ago

Visualizations are off on this. Can we please fix this?

2

Reply
P
PriorAmaranthDamselfly777
• 1 year ago

No where to add code

2

Reply
Nicholas Reid
Premium
• 1 month ago

Simple recursive soln

class Solution:
    def swapPairs(self, head: ListNode):
        if not head or not head.next: return head
        next, rest = head.next, head.next.next
        rest = self.swapPairs(rest)
        next.next = head
        head.next = rest
        return next

1

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Solution

Need for a Dummy Node

Termination

Implementation

Code

Edge Cases
