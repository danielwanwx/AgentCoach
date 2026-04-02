# Reorder List

> Source: https://www.hellointerview.com/learn/code/linked-list/reorder-list
> Scraped: 2026-03-30


Linked List
Reorder List
medium
DESCRIPTION (inspired by Leetcode.com)

Given a reference head of type ListNode that is the head of a singly linked list, reorder the list in-place such that the nodes are reordered to form the following pattern:

1st node -> last node -> 2nd node -> 2nd to last node -> 3rd node ...

Example 1: input:

5
4
3
2
1
head

output:

5
1
4
2
3
head

Example 2: input:

0
1
2
head

output:

0
2
1
head
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
    def reorderList(self, head: ListNode) -> None:
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
The first observation is that we can create our final list by merging two smaller lists: the first half of the original list and the reversed second half of the original list.
For example, if our original list is 5 -> 4 -> 3 -> 2 -> 1, then the first half is 5 -> 4 -> 3 and the reversed second half is 1 -> 2. We can merge these two lists to get the final list 5 -> 1 -> 4 -> 2 -> 3.
5
4
3
 
1
2
Above: The first half of the original list
Below: The reversed second half of the original list
With that established, we can focus on getting the reverse of the 2nd half of the list. This breaks down to first finding the middle node of the list, and then reversing the direction of the nodes starting from the middle node to the end of the list.
Put together, the solution involves three steps, each of which involve 3 fairly common linked list operations:
Finding the middle of the linked list (using fast and slow pointers).
Reversing the nodes between the middle and the end of the linked list.
Merging the first half of the linked list with the reversed second half.
Step 1: Find The Middle Of The Linked List
This step can be done using fast and slow pointers, which involves initializing two pointers, fast and slow, at the head of the linked list, and then iterating until fast reaches the end of the list. At each iteration, slow moves one node forward and fast moves two nodes forward. When fast reaches the tail node of the list, slow will point to the middle node in the list.
VISUALIZATION
Python
Language
Full Screen
def reorderList(head):
    if not head or not head.next:
        return head
    
    # find middle node
    slow = fast = head
    while fast and fast.next:
        fast = fast.next.next
        slow = slow.next
    
    # reverse second half of list
    prev, curr = None, slow
    while curr:
        next_ = curr.next
        curr.next = prev
        prev, curr = curr, next_
    
    # merge first and reversed second half of list
    first, second = head, prev
    while second.next:
        first.next, first = second, first.next
        second.next, second = first, second.next
    
    return head
5
4
3
2
1
slow
fast

initialize pointers

0 / 2

1x
When there are an even number of nodes, fast will equal to None after moving past the tail node, and slow will be the first node of the second half of the list. In the case below, there are 4 nodes, so slow will point to the 3rd node.
VISUALIZATION
Python
Language
Full Screen
def reorderList(head):
    if not head or not head.next:
        return head
    
    # find middle node
    slow = fast = head
    while fast and fast.next:
        fast = fast.next.next
        slow = slow.next
    
    # reverse second half of list
    prev, curr = None, slow
    while curr:
        next_ = curr.next
        curr.next = prev
        prev, curr = curr, next_
    
    # merge first and reversed second half of list
    first, second = head, prev
    while second.next:
        first.next, first = second, first.next
        second.next, second = first, second.next
    
    return head
5
4
4
3
slow
fast

initialize pointers

0 / 2

1x
Step 2: Reverse Second Half Of List
At this point, slow points to the middle node in the list. Next, we want to reverse the direction of the pointers of each node starting from slow to the tail of the list.
Reversing the nodes in a linked list is a common problem that can be solved by iterating over each node that needs to be reversed. The key idea is to maintain three pointers, prev, curr, and next_, where prev points to the previous node, curr points to the node with the pointer we want to reverse, and next_ points to the next node in the iteration.
At each iteration, we:
save the next node in the iteration by setting next_ = curr.next
reverse the pointer by setting curr.next = prev
move pointers for the next iteration by set curr = next_ and prev = curr
VISUALIZATION
Python
Language
Full Screen
def reorderList(head):
    if not head or not head.next:
        return head
    
    # find middle node
    slow = fast = head
    while fast and fast.next:
        fast = fast.next.next
        slow = slow.next
    
    # reverse second half of list
    prev, curr = None, slow
    while curr:
        next_ = curr.next
        curr.next = prev
        prev, curr = curr, next_
    
    # merge first and reversed second half of list
    first, second = head, prev
    while second.next:
        first.next, first = second, first.next
        second.next, second = first, second.next
    
    return head
5
4
3
2
1
slow
fast

fast = fast.next.next, slow = slow.next

0 / 10

1x
You need the next_pointer to store the next node in the iteration before overwriting curr.next = prev. If you don't store the next node in the iteration, you will lose the reference to the rest of the linked list.
Step 3: Merge First Half With Reversed Second Half
At this point, when curr is None, then prev will be the head of the reversed second half of the list. We can then merge the first half of the list with the reversed second half by iterating over the two halves and updating the pointers of the nodes.
We can do so by initializing two pointers: first, which points to the head of the first half of the list, and second, which points to the head of the reversed second half of the list, which is initially prev.
VISUALIZATION
Python
Language
Full Screen
def reorderList(head):
    if not head or not head.next:
        return head
    
    # find middle node
    slow = fast = head
    while fast and fast.next:
        fast = fast.next.next
        slow = slow.next
    
    # reverse second half of list
    prev, curr = None, slow
    while curr:
        next_ = curr.next
        curr.next = prev
        prev, curr = curr, next_
    
    # merge first and reversed second half of list
    first, second = head, prev
    while second.next:
        first.next, first = second, first.next
        second.next, second = first, second.next
    
    return head
5
4
3
2
1
prev
curr
next_

curr = next_, prev = curr

0 / 1

1x
From there, we want to merge the nodes at first and second together, with first coming before second. To do so, we first set first.next = second. And since we are over-writing first.next, we need to simultaneously advance first = first.next so that we have access to the next node in the first half of the list.
VISUALIZATION
Python
Language
Full Screen
def reorderList(head):
    if not head or not head.next:
        return head
    
    # find middle node
    slow = fast = head
    while fast and fast.next:
        fast = fast.next.next
        slow = slow.next
    
    # reverse second half of list
    prev, curr = None, slow
    while curr:
        next_ = curr.next
        curr.next = prev
        prev, curr = curr, next_
    
    # merge first and reversed second half of list
    first, second = head, prev
    while second.next:
        first.next, first = second, first.next
        second.next, second = first, second.next
    
    return head
5
4
3
2
1
first
second

first = head, second = prev

0 / 1

1x
Now the first node in the original list and the first node in the reversed second half are connected, so we need to connect the 2nd node in the original list with the first node in the reversed second half. We can do so by setting second.next = first and making sure we simultaneously advance second = second.next so that we have access to the next node in the reversed second half.
VISUALIZATION
Python
Language
Full Screen
def reorderList(head):
    if not head or not head.next:
        return head
    
    # find middle node
    slow = fast = head
    while fast and fast.next:
        fast = fast.next.next
        slow = slow.next
    
    # reverse second half of list
    prev, curr = None, slow
    while curr:
        next_ = curr.next
        curr.next = prev
        prev, curr = curr, next_
    
    # merge first and reversed second half of list
    first, second = head, prev
    while second.next:
        first.next, first = second, first.next
        second.next, second = first, second.next
    
    return head
5
4
3
2
1
first
second

first.next = 1, first = 4

0 / 1

1x
At this point, the first three nodes in our original linked list are correctly ordered, and first and second are pointing to the next nodes in each half that we need to merge together. So we can continue the merge until second has reached the end of the reversed second half of the list, at which point we can return None.
VISUALIZATION
Python
Language
Full Screen
def reorderList(head):
    if not head or not head.next:
        return head
    
    # find middle node
    slow = fast = head
    while fast and fast.next:
        fast = fast.next.next
        slow = slow.next
    
    # reverse second half of list
    prev, curr = None, slow
    while curr:
        next_ = curr.next
        curr.next = prev
        prev, curr = curr, next_
    
    # merge first and reversed second half of list
    first, second = head, prev
    while second.next:
        first.next, first = second, first.next
        second.next, second = first, second.next
    
    return head
5
4
3
2
1
first
second

second.next = 4, second = 2

0 / 3

1x
Implementation
Here's the complete 3-step solution that reorders the list in-place:
SOLUTION
Python
Language
def reorderList(head):
    if not head or not head.next:
        return
    
    # Step 1: Find the middle of the list using slow/fast pointers
    slow = head
    fast = head
    
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
    
    # Step 2: Reverse the second half starting from slow.next
    second_half = reverse_list(slow.next)
    slow.next = None  # Cut the list into two halves
    
    # Step 3: Merge two halves alternately
    first_half = head
    
    while second_half:
        first_next = first_half.next   # Store next nodes
        second_next = second_half.next
        
        first_half.next = second_half  # Link first to second
        second_half.next = first_next  # Link second to first's next
        
        first_half = first_next        # Move to next nodes
        second_half = second_next

def reverse_list(head):
    prev = None
    current = head
    
    while current:
        next_temp = current.next
        current.next = prev
        prev = current
        current = next_temp
    
    return prev
Code
To construct the linked list that is used in the animation below, provide a list of integers nodes. Each integer in nodes is used as the value of a node in the linked list, and the order of the integers in the list will be the order of the nodes in the linked list.
For example, if nodes = [1, 2, 3], the linked list will be 1 -> 2 -> 3.
nodes
​
|
nodes
list of integers
Try these examples:
Odd Length
Even Length
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def reorderList(head):
    if not head or not head.next:
        return head
    
    # find middle node
    slow = fast = head
    while fast and fast.next:
        fast = fast.next.next
        slow = slow.next
    
    # reverse second half of list
    prev, curr = None, slow
    while curr:
        next_ = curr.next
        curr.next = prev
        prev, curr = curr, next_
    
    # merge first and reversed second half of list
    first, second = head, prev
    while second.next:
        first.next, first = second, first.next
        second.next, second = first, second.next
    
    return head
5
4
3
2
1

reorder list

0 / 19

1x
Edge Cases
Empty List
When the linked list is empty, the initial check for head being None will return None immediately.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def reorderList(head):
    if not head or not head.next:
        return head
    
    # find middle node
    slow = fast = head
    while fast and fast.next:
        fast = fast.next.next
        slow = slow.next
    
    # reverse second half of list
    prev, curr = None, slow
    while curr:
        next_ = curr.next
        curr.next = prev
        prev, curr = curr, next_
    
    # merge first and reversed second half of list
    first, second = head, prev
    while second.next:
        first.next, first = second, first.next
        second.next, second = first, second.next
    
    return head

reorder list

0 / 1

1x
`head = []`
Single Node
When the linked list has one node, the initial check for head.next being None will return head immediately.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def reorderList(head):
    if not head or not head.next:
        return head
    
    # find middle node
    slow = fast = head
    while fast and fast.next:
        fast = fast.next.next
        slow = slow.next
    
    # reverse second half of list
    prev, curr = None, slow
    while curr:
        next_ = curr.next
        curr.next = prev
        prev, curr = curr, next_
    
    # merge first and reversed second half of list
    first, second = head, prev
    while second.next:
        first.next, first = second, first.next
        second.next, second = first, second.next
    
    return head
1

reorder list

0 / 1

1x
`head = [1]`
Two Nodes
When the linked list has two nodes, the linked list is already in the correct order.
The while loop to find the middle node iterates once, with slow pointing to the 2nd node.
The while loop to reversing the second half runs once, but since there is only one node in the 2nd half of the list, no pointers are updated, and prev points to the 2nd node.
The while loop to merge the two halves doesn't run, as second.next is None.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def reorderList(head):
    if not head or not head.next:
        return head
    
    # find middle node
    slow = fast = head
    while fast and fast.next:
        fast = fast.next.next
        slow = slow.next
    
    # reverse second half of list
    prev, curr = None, slow
    while curr:
        next_ = curr.next
        curr.next = prev
        prev, curr = curr, next_
    
    # merge first and reversed second half of list
    first, second = head, prev
    while second.next:
        first.next, first = second, first.next
        second.next, second = first, second.next
    
    return head
1
2

reorder list

0 / 8

1x
`head = [1, 2]`
What is the time complexity of this solution?
1

O(4ⁿ)

2

O(m * n * 4^L)

3

O(n)

4

O(1)

Mark as read

Next: Swap Nodes in Pairs

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
Nathan Li
Premium
• 5 months ago

There is a minor issue here; you need to disconnect the first and second halves.

second = slow.next
slow.next = None
prev = None

4

Reply
E
ElegantAquaMouse760
• 1 month ago

The disconnecting is not needed because:

When an even number of elements last slow element would always be after the last element of the first half list in the re-ordered list. e.g. [1,2,3,4] -> [1,4,2,3]: as you can see, the next pointer of 2 will be pointing to 3. No change needed.
When an odd number of elements, the next pointer of the element before the middle element will be overridden by the last phase. e.g: [1,2,3,4,5] -> [1,5,2,4,3] -> the next pointer of 2 will be made to point to 4 by the 3rd phase

1

Reply
N
Top 5%
• 10 months ago

this problem also not in side bar

2

Reply
P
PriorAmaranthDamselfly777
• 1 year ago

No where to add code

2

Reply
M
MathematicalRedWombat488
Premium
• 3 months ago

5 -> 4 -> 3 -> -> 2 -> 1

Typo error

1

Reply

Shivam Chauhan

Admin
• 3 months ago

Thanks! Fix will be updated in next release.

0

Reply
Alex h
Premium
• 5 days ago

Python solution with multiple helper functions for easier understanding:

def reorderList(self, head: ListNode) -> None:
        # Your code goes here
        left=head
        right=self.splitList(head)
        right=self.reverList(right)
        head=self.mergeList(left,right)
        
    def splitList(self, head):
        slow=fast=head
        while fast and fast.next:
            slow=slow.next
            fast=fast.next.next
        h=slow.next
        slow.next=None
        return h
    
    def reverList(self, head):
        prev=None
        curNode=head
        while curNode:
            tmp=curNode.next
            curNode.next=prev
            prev=curNode
            curNode=tmp
        return prev
    
    def mergeList(self, left, right):
        h=left
        while left and right:
            nextLeft=left.next
            nextRight=right.next
            left.next=right
            right.next=nextLeft
            left=nextLeft
            right=nextRight
        return h
Show More

0

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Solution

Step 1: Find the Middle of the Linked List

Step 2: Reverse second half of list

Step 3: Merge first half with reversed second half

Implementation

Code

Edge Cases
