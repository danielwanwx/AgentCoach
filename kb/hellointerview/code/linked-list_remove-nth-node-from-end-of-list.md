# Remove Nth Node From End of List

> Source: https://www.hellointerview.com/learn/code/linked-list/remove-nth-node-from-end-of-list
> Scraped: 2026-03-30


Linked List
Remove Nth Node From End of List
medium
DESCRIPTION (inspired by Leetcode.com)

Given a reference head of type ListNode that is the head node of a singly linked list and an integer n, write a function that removes the n-th node from the end of the list and returns the head of the modified list.

Note: n is guaranteed to be between 1 and the length of the list. If n is the length of the list, the head of the list should be removed.

Example 1:

Input: n = 2

5
4
3
2
1
head

Output:

5
4
3
1
head

Explanation: The 2nd to last node is removed from the list.

Example 2:

Input: n = 5

5
4
3
2
1
head

Output:

4
3
2
1
head

Explanation: The 5th to last node is the head node, so it is removed.

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
    def removeNthFromEnd(self, head: ListNode, n: int) -> ListNode:
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

Solutions
In order to remove the n-th node from the end of the list, we first need to locate the node right before it.
For example, if our list is [5, 4, 3, 2, 1] and n = 2, then we need to remove the 2nd node from the end with value 2. In order to do so, we first need to locate the node right before it, with value 3.
5
4
3
2
1
remove
If we have a pointer to that node current, we can delete node 2 by setting current.next = current.next.next, which removes node 2 from the list (as no nodes point to it).
5
4
3
2
1
current
Here are a 3 solutions to this problem, each of which approach the problem of locating the node right before the n-th node from the end in a different way.
1. Find the Length of the List
The first approach is to traverse the list to find its length. Once we know the length of the list, we can find the node right before the n-th node from the end by traversing length - n - 1 nodes from the head.
head
​
|
head
list of integers
n
​
|
n
integer
Try these examples:
Remove Head
Remove Last
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def removeNthFromEnd(head, n):
    # find length
    length = 0
    current = head
    while current:
        length += 1
        current = current.next
    
    target = length - n
    if target == 0:
        return head.next
    
    current = head
    for _ in range(target - 1):
        current = current.next
    
    current.next = current.next.next
    return head
5
4
3
2
1

remove nth node from end of list

0 / 11

1x
We have to handle the special case when n is equal to the length of the list, which requires removing the head node. This needs to be handled separately because head does not have a node right before it to locate. Instead, when n == length, we can remove the head node by returning head.next directly.
Time Complexity: O(N), where N is the number of nodes in the list. We traverse the list once to find the length of the list, and another time to find the node right before the n-th node from the end. Both traversals take O(N) time.
Space Complexity: O(1). We only use a constant amount of extra space for the pointers, regardless of the number of nodes in the list.
2. Use Two Pointers
Instead of traversing the list once to find its length, we can use two pointers, fast and slow that both start at head. To start, fast advances n nodes ahead of slow. Then both pointers advance one node at a time until fast reaches the last node in the list.
At this point, slow will point to the node right before the n-th node from the end, and we can remove the n-th node by setting slow.next = slow.next.next.
head
​
|
head
list of integers
n
​
|
n
integer
Try these examples:
Remove Head
Middle
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def removeNthFromEnd(head, n):
    fast = slow = head
    for _ in range(n):
        fast = fast.next
    
    # special case: removing head
    if not fast:
        return head.next
    
    while fast.next:
        fast = fast.next
        slow = slow.next
    
    slow.next = slow.next.next
    return head
5
4
3
2
1

remove nth node from end of list

0 / 7

1x
Like before, we have to handle the special case when n is equal to the length of the list. Since we don't know the length of the list, we can't detect this case by comparing the two values directly. Instead, if fast is None after advancing n nodes, we know that n is equal to the length of the list, and we can remove the head node by returning head.next directly.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def removeNthFromEnd(head, n):
    fast = slow = head
    for _ in range(n):
        fast = fast.next
    
    # special case: removing head
    if not fast:
        return head.next
    
    while fast.next:
        fast = fast.next
        slow = slow.next
    
    slow.next = slow.next.next
    return head
5
4
3
2
1

remove nth node from end of list

0 / 7

1x
Handling of special case when removing the head of the list. (`n = 5`)
Time Complexity: O(N), where N is the number of nodes in the list. The fast pointer first advances n nodes, then both pointers advance together until fast reaches the end. In total, fast traverses N nodes and slow traverses N - n nodes, giving us O(N) time.
Space Complexity: O(1). We only use a constant amount of extra space for the pointers, regardless of the number of nodes in the list.
3. Dummy Node
In the two above approaches, we need special logic to handle removing the head node because the head node does not have a node right before it to locate.
We can avoid this special case by introducing a dummy node that points to the head of the list. The dummy node allows us to treat every node, including the head, as if it has a preceding node. With the dummy node established, we can again use the two-pointer approach to find the node right before the n-th node from the end.
VISUALIZATION
Python
Language
Full Screen
def removeNthFromEnd(head, n):
    dummy = ListNode(0)
    dummy.next = head
    
    fast, slow = dummy, dummy
    for _ in range(n):
        fast = fast.next
    
    while fast.next:
        fast = fast.next
        slow = slow.next
    
    # remove nth node from end
    slow.next = slow.next.next
    return dummy.next
5
4
3
2
1

remove nth node from end of list

0 / 1

1x
Introducing a dummy node
Both the fast and slow pointers start at the dummy node, and like before, fast advances n nodes ahead of slow. Then both pointers advance one node at a time until fast reaches the last node in the list.
VISUALIZATION
Python
Language
Full Screen
def removeNthFromEnd(head, n):
    dummy = ListNode(0)
    dummy.next = head
    
    fast, slow = dummy, dummy
    for _ in range(n):
        fast = fast.next
    
    while fast.next:
        fast = fast.next
        slow = slow.next
    
    # remove nth node from end
    slow.next = slow.next.next
    return dummy.next
5
4
3
2
1
0
dummy

initialize dummy node

0 / 6

1x
Introducing a dummy node
At this point, slow will point to the node right before the n-th node from the end, and we can remove the n-th node by setting slow.next = slow.next.next, and return dummy.next as the head of the modified list.
VISUALIZATION
Python
Language
Full Screen
def removeNthFromEnd(head, n):
    dummy = ListNode(0)
    dummy.next = head
    
    fast, slow = dummy, dummy
    for _ in range(n):
        fast = fast.next
    
    while fast.next:
        fast = fast.next
        slow = slow.next
    
    # remove nth node from end
    slow.next = slow.next.next
    return dummy.next
5
4
3
2
1
0
slow
fast
dummy

fast = fast.next, slow = slow.next

0 / 2

1x
Removing The Head Node
With the dummy node, when n is equal to the length of the list, slow still points to the dummy node after both the fast and slow pointers finish advancing.
Now, we can remove the head node by setting slow.next = slow.next.next, and return slow.next as the head of the modified list - which is the exact same logic as removing any other node!
VISUALIZATION
Python
Language
Full Screen
def removeNthFromEnd(head, n):
    dummy = ListNode(0)
    dummy.next = head
    
    fast, slow = dummy, dummy
    for _ in range(n):
        fast = fast.next
    
    while fast.next:
        fast = fast.next
        slow = slow.next
    
    # remove nth node from end
    slow.next = slow.next.next
    return dummy.next
5
4
3
2
1
0
fast
dummy
slow

fast = fast.next

0 / 2

1x
Removing the head node (`n = 5`)
Implementation
Here's the complete dummy node approach that elegantly handles all edge cases:
SOLUTION
Python
Language
def removeNthFromEnd(head, n):
    # Create dummy node to handle edge case of removing head
    dummy = ListNode(0)
    dummy.next = head
    fast = dummy
    slow = dummy
    
    # Move fast pointer n steps ahead to create n-node gap
    for i in range(n):
        fast = fast.next
    
    # Move both pointers until fast reaches end
    # When fast is at last node, slow will be at node before target
    while fast.next is not None:
        fast = fast.next
        slow = slow.next
    
    # Remove the nth node from end by skipping it
    slow.next = slow.next.next
    
    return dummy.next  # Return head of modified list
Code
To construct the linked list that is used in the animation below, provide a list of integers nodes. Each integer in nodes is used as the value of a node in the linked list, and the order of the integers in the list will be the order of the nodes in the linked list.
For example, if nodes = [1, 2, 3], the linked list will be 1 -> 2 -> 3.
head
​
|
head
list of integers
n
​
|
n
integer
Try these examples:
Remove Head
Remove Last
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def removeNthFromEnd(head, n):
    dummy = ListNode(0)
    dummy.next = head
    
    fast, slow = dummy, dummy
    for _ in range(n):
        fast = fast.next
    
    while fast.next:
        fast = fast.next
        slow = slow.next
    
    # remove nth node from end
    slow.next = slow.next.next
    return dummy.next
5
4
3
2
1

remove nth node from end of list

0 / 9

1x
What is the time complexity of this solution?
1

O(4ⁿ)

2

O(x * y)

3

O(n)

4

O(m * n * 4^L)

Mark as read

Next: Reorder List

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

(8)

Comment
Anonymous
P
PriorAmaranthDamselfly777
• 1 year ago

No where to add code

8

Reply
Xavier Elon
Premium
• 1 year ago

This problem does not appear in the side bar

2

Reply
A
AppropriateOliveAnaconda130
Premium
• 7 months ago

FYI there would a corner case where N > length of the list causing you to set fast = None in the loop and subsequently attempting to dereference it. Probably I would say you can find a way to solve this in the dummy node init to avoid advancing fast in the setup of the solution.

1

Reply
Sumanth
Premium
• 2 months ago
• edited 2 months ago

With prev and curr Nodes:

public ListNode RemoveNthFromEnd(ListNode head, int n) {
        ListNode curr = head, prev = null;
        int length = 0;
        
        while (curr != null) {
            length += 1;
            curr = curr.next;
        }

        curr = head;
        int index = 0;
        while (index < length - n) {
            prev = curr;
            curr = curr.next;
            index += 1;
        }

        if (prev == null) {
            return head.next;
        } else {
            ListNode next = curr.next;
            prev.next = next;
            curr.next = null;
        }

        return head;
    }

With only one  curr:

public ListNode RemoveNthFromEnd(ListNode head, int n) {
       ListNode curr = head;
       int length = 0;
       
       while (curr != null) {
           length += 1;
           curr = curr.next;
       }

       curr = head;
       int target = length - n;

       for (int i = 0; i < target - 1; i++) {
           curr = curr.next;
       }

       if (target == 0) {
           return head.next;
       } else {
           curr.next = curr.next.next;
       }

       return head;
   }
Show More

0

Reply
Omar David Hernández
Premium
• 2 months ago

In the Implementation section the stopping criteria is i <= n:

    // Move fast pointer n+1 steps ahead to create n-node gap
    for (let i = 0; i <= n; i++) {
        fast = fast!.next;
    }

And this differs from the i < n stopping criteria used in the other code snippets.

0

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Solutions

1. Find the Length of the List

2. Use Two Pointers

3. Dummy Node

Implementation

Code
