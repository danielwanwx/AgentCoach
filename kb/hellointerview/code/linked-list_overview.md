# Linked List Overview

> Source: https://www.hellointerview.com/learn/code/linked-list/overview
> Scraped: 2026-03-30

Linked List Overview
This page covers common operations and strategies that frequently show up in linked list problems for the coding interview.
Basics
A linked list is a data structure consisting of sequence of a nodes, where each node contains a value and reference to the next node in the sequence.
In Python, we can represent a linked list node with a ListNode class, where val is a piece of data and next is a reference to the next node in the linked list.
SOLUTION
Python
Language
# Definition of a ListNode
class ListNode:
  def __init__(self, val=0, next=None):
    self.val = val
    self.next = next
We can visualize a linked list as a sequence of nodes connected by arrows that point to the next node in the sequence. The first node in a linked list is referred to as the head, and the last node is referred to as the tail. The next field of the tail node is None (unless the linked list contains a cycle) which indicates the end of the linked list.
VISUALIZATION
Python
Language
Full Screen
# visualizing linked lists
head = ListNode(1)
head.next = ListNode(2)
head.next.next = ListNode(3)
head.next.next.next = ListNode(4)

0 / 4

1x
Visualizing a linked list with 4 nodes.
Basic Operations
These operations demonstrate some of the fundamentals of working with linked lists.
Traversing a Linked List
When traversing a linked list, we initialize a pointer current that starts at the head node of the linked list and follows next pointers until it is None. This allows us to visit each node in the linked list, and perform operations such as finding the length of the linked list.
VISUALIZATION
Python
Language
Full Screen
def findLength(head):
    length = 0
    current = head
    while current:
        length += 1
        current = current.next
    return length
1
2
3
4
head

0 / 6

1x
Traversing a linked list to find its length.
Complexity Analysis
Time Complexity: The time complexity of this algorithm is O(n) where n is the number of nodes in the linked list. The algorithm iterates through each node in the linked list once.
Space Complexity: The space complexity of this algorithm is O(1) since we only use one pointer to traverse the linked list regardless of the number of nodes in the linked list.
Deleting a Node With a Given Target
To delete a node with a given target, we need a reference to both the node we want to delete, and the node right before it.
We'll keep two pointers, curr and prev, and update curr until it reaches the target node, or None. We'll also update prev to be the node before curr at each step. When curr reaches the target node, we can delete it by setting prev.next = curr.next.
We have to handle deleting the head of the linked list as a special case, because there is no node before the head. We can simplify this by using a dummy node, which we'll cover later.
head
​
|
head
list of integers
target
​
|
target
integer
Try these examples:
Remove Present
No Match
Reset
VISUALIZATION
Python
Language
Full Screen
def deleteNode(head, target):
    if head.val == target:
        return head.next
    
    prev = None
    curr = head
    
    while curr:
        if curr.val == target:
            prev.next = curr.next
            break
        prev = curr
        curr = curr.next
    
    return head
5
4
3
2
1

delete node with target value

0 / 6

1x
Complexity Analysis
Time Complexity: The time complexity of this algorithm is O(n) where n is the number of nodes in the linked list. The algorithm iterates through each node in the linked list once in the worst case (when the target does not exist in the linked list).
Space Complexity: The space complexity of this algorithm is O(1) since we only use two pointers to traverse the linked list regardless of the number of nodes in the linked list.
Operations to Know for Interviews
Linked list interview questions require manipulating pointers in specific ways that depend entirely on the requirements of the problem. However, there are a few core operations that you should be familiar with, as they show up in multiple linked list questions.
This section covers those operations. At the end, we'll look at problems that will give you more practice with these operations.
1. Fast and Slow Pointers
Fast and slow pointers is a technique that is used to find the middle node in a linked list. We initialize two pointers, slow and fast, that start at the head of the linked list. We then iterate until fast reaches the end of the list. During each iteration, the slow pointer advances by one node, while the fast pointer advances by two nodes. When the fast pointer reaches tail of the list, the slow pointer points to the middle node.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def fastAndSlow(head):
    fast = head
    slow = head
    while fast and fast.next:
        fast = fast.next.next
        slow = slow.next
    return slow
1
2
3
4
5

fast and slow pointers

0 / 4

1x
When there are an even number of nodes, there are two possible choices for the middle node, and this technique will find the second of those two nodes.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def fastAndSlow(head):
    fast = head
    slow = head
    while fast and fast.next:
        fast = fast.next.next
        slow = slow.next
    return slow
1
2
3
4

fast and slow pointers

0 / 4

1x
It helps to make the connection between the position of the fast pointer when the iteration finishes and the condition of the while loop. For example, in the case of an odd number of nodes, the fast pointer reaches the last node of the linked list, so the while fast.next part of the loop condition is false, and the loop terminates.
5
4
3
2
1
fast
In the case of an even number of nodes, the fast pointer is None (via the next pointer of the last node), so the while fast part of the loop condition is false, and the loop terminates.
5
4
3
2
fast
In general, when working with linked list questions, having a clear understanding of what each pointer in your algorithm represents, and being able to visualize where they should end up when the iteration finishes will help you avoid off-by-one errors and null pointer exceptions.
Complexity Analysis
Time Complexity: The time complexity of this algorithm is O(n) where n is the number of nodes in the linked list. The algorithm terminates when the fast pointer reaches the end. Since fast advances two nodes per iteration, the loop runs approximately n/2 times, which is O(n).
Space Complexity: The space complexity of this algorithm is O(1) since we only use two pointers to traverse the linked list regardless of the number of nodes in the linked list.
Cycle Detection
The same fast and slow pointers technique can also be used to determine if a linked list contains a cycle. If we follow the same iteration pattern and the linked list contains a cycle, the fast pointer will eventually overlap the slow pointer and they will point to the same node.
VISUALIZATION
Full Screen
5
4
3
2
0

linked list cycle

0 / 5

1x
This is a common interview question, and a good problem to practice using the fast and slow pointers technique (see question #1, Leetcode 141 in Practice Problems).
2. Reversing a Linked List
Reversing a linked list involves changing the direction of the next pointers in a linked list so the last node becomes the head of the reversed linked list.
The algorithm for reversing a linked list is an iterative algorithm which involves 3 pointers, prev, current, and next_.
current points to the node we are currently reversing.
prev is the last node that was reversed, and also the node that current.next will point to after reversing.
next_ is the next node we will reverse. We need a pointer to this node before we overwrite the current.next so we can continue reversing the list in the next iteration.
When the iteration completes, current will be None, and prev will be the new head of the linked list.
VISUALIZATION
Python
Language
Full Screen
def reverse(head):
    prev = None
    current = head
    while current:
        next_ = current.next
        current.next = prev
        prev = current
        current = next_
    return prev
1
2
3
4
5

reverse linked list

0 / 17

1x
Complexity Analysis
Time Complexity: The time complexity of this algorithm is O(n) where n is the number of nodes in the linked list. The algorithm iterates through each node in the linked list once.
Space Complexity: The space complexity of this algorithm is O(1) since we only use three pointers to reverse the linked list regardless of the number of nodes in the linked list.
3. Merging Two Linked Lists
The last operation is merging two linked lists. As an example of this operation, we'll look at how to merge two sorted linked lists.
As an input to this problem, we are given the heads of two sorted linked lists, l1 and l2, and we need to return the head of a new linked list that contains all the nodes from the two input linked lists in sorted order.
To merge two sorted linked lists, we start by determining the head of the merged linked list by comparing the values of l1 and l2, and setting the head to the smaller of the two nodes. We then advance l1 = l1.next or l2 = l2.next depending on which node we chose as the head of the merged linked list.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def merge_lists(l1, l2):
    if not l1: return l2
    if not l2: return l1

    if l1.val < l2.val:
        head = l1
        l1 = l1.next
    else:
        head = l2
        l2 = l2.next

    current = head
    while l1 and l2:
        if l1.val < l2.val:
            current.next = l1
            l1 = l1.next
        else:
            current.next = l2
            l2 = l2.next
        current = current.next

    current.next = l1 or l2
    return head
1
4
6
l1
2
3
l2

merge two linked lists

0 / 1

1x
Now, we can initialize a pointer tail, which represents the last node of the merged linked list. We then iterate through the two input linked lists, comparing the values of l1 and l2 at each step. We append the smaller of the two nodes to the tail of the merged linked list, and advance the pointer of the node we appended.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def merge_lists(l1, l2):
    if not l1: return l2
    if not l2: return l1

    if l1.val < l2.val:
        head = l1
        l1 = l1.next
    else:
        head = l2
        l2 = l2.next

    current = head
    while l1 and l2:
        if l1.val < l2.val:
            current.next = l1
            l1 = l1.next
        else:
            current.next = l2
            l2 = l2.next
        current = current.next

    current.next = l1 or l2
    return head
1
4
6
l1
2
3
l2
1
head

head = l1; l1 = l1.next

0 / 5

1x
When either l1 or l2 is None, we can we append the remaining nodes of the other linked list to the merged linked list, and return head.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def merge_lists(l1, l2):
    if not l1: return l2
    if not l2: return l1

    if l1.val < l2.val:
        head = l1
        l1 = l1.next
    else:
        head = l2
        l2 = l2.next

    current = head
    while l1 and l2:
        if l1.val < l2.val:
            current.next = l1
            l1 = l1.next
        else:
            current.next = l2
            l2 = l2.next
        current = current.next

    current.next = l1 or l2
    return head
1
4
6
l1
2
3
l2
1
2
3
head
current

current = current.next

0 / 2

1x
What is the time complexity of this solution?
1

O(n log n)

2

O(x * y)

3

O(V + E)

4

O(n + m)

Practice Problems
These practice problems will give you practice with these core operations:
Linked List Cycle
Leetcode #141 | Solution
Hint: Use fast and slow pointers to determine if a linked list contains a cycle.
Palindrome Linked List
Leetcode #234 | Solution
Hint: Use fast and slow pointers to find the middle of the linked list, and reverse the second half of the linked list, and compare the values of the nodes in the first half and the reversed second half.
Reorder List
Leetcode #143 | Solution
Hint: Use fast and slow pointers to find the middle of the linked list, reverse the second half of the linked list, and merge the two halves of the linked list together.
Dummy Nodes
Merging two sorted linked lists is an example of a problem where using a dummy node can simplify the logic of the code.
Notice that in the solution for merging two lists above, the logic for choosing the head of the merged linked list is the same as the logic for choosing the next node to append. We need to handle it as a special case because without it, we wouldn't have a starting point for the merged linked list.
We can avoid this by creating a dummy node to represent the starting point of the merged linked list. This allows us to move directly into the iteration processes without having to introduce a special case to initialize the head of the merged linked list. When the iteration finishes we return dummy.next as the head of the merged linked list.
Note: The term "dummy node" refers to creating a new node that isn't part of the input linked list(s) (line 2 in the code below).
VISUALIZATION
Hide Code
Python
Language
Full Screen
def merge_two_lists(l1, l2):
    dummy = ListNode()
    tail = dummy
    while l1 and l2:
        if l1.val < l2.val:
            tail.next = l1
            l1 = l1.next
        else:
            tail.next = l2
            l2 = l2.next
        tail = tail.next
    tail.next = l1 or l2
    return dummy.next
1
4
6
l1
2
3
l2

merge two linked lists

0 / 9

1x
Advantages of a Dummy Node
The advantage of using a dummy node for this question is that it allows us to avoid having to initializing the head of the merged linked list as a special case. This simplifies the logic of the code, and also reduces the need to check if either of the merged linked lists are None (which we need to do if we don't use a dummy node because we reference either l1.next or l2.next as part of initializing the head of the merged linked list. If either l1 or l2 are None, then that reference would throw a null pointer exception).
When to Use a Dummy Node
If you find yourself writing a solution where you need to introduce a special case to initialize the head of a linked list, and the logic for handling the head is the same as the logic for handling the rest of the linked list, you should consider using a dummy node to simplify your solution.
Using a dummy node under these conditions involves the following 3 steps:
Creating the dummy node to represent the head of the linked list you are constructing.
Now, you can iteratively append nodes to the end that linked list based on the logic of the problem.
Returning dummy.next as the head of the linked list you constructed.
This might be confusing, so the best way to understand this concept is through practice.
Other Use Cases
Dummy nodes can also simplify the logic of removing a node in a linked list. As we saw above, removing a node in a linked list requires a reference to the previous node of the node you want to remove. By prepending a dummy node to the head of the link list, we can ensure that each node (including the head) has a previous node, and we can avoid handling the head of the linked list as a special case.
Removing A Node In A Linked List With A Dummy Node
head
​
|
head
list of integers
target
​
|
target
integer
Try these examples:
Remove Present
No Match
Reset
VISUALIZATION
Python
Language
Full Screen
def deleteNode(head, target):
    dummy = ListNode(0)
    dummy.next = head
    
    prev = dummy
    curr = head
    
    while curr:
        if curr.val == target:
            prev.next = curr.next
            break
        prev = curr
        curr = curr.next
    
    return dummy.next
5
4
3
2
1

delete node with target value

0 / 7

1x
Practice Problems
Swap Nodes in Pairs
Leetcode #24 | Solution
Hint: Start by figuring out the pointers you need to manipulate in order to swap two nodes in the middle of a linked list, then think about how using a dummy node can simplify your solution.
Partition List
Leetcode #86
Hint: Use two dummy nodes!
Remove Nth Node From End of List
Leetcode #19 | Solution
Hint: Use a dummy node to avoid handling the case of removing the head of the linked list as a special case.

Mark as read

Next: Linked List Cycle

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

(11)

Comment
Anonymous
​
Sort By
Popular
Sort By
Patricia Pan
Top 1%
• 1 year ago

can you add a link to "reverse linked list" as a practice problem as well?

https://leetcode.com/problems/reverse-linked-list/description/

22

Reply
sensei
Premium
• 1 month ago

LRU also comes under linked list(doubly linked list) , amazon asked me exact question in my interview.
https://leetcode.com/problems/lru-cache/description/

4

Reply
Stanley Lin
• 1 month ago

hope you aced it?

0

Reply
W
WilyYellowCaterpillar346
• 2 months ago

The  visualizations are very helpful but for these problems it would help even more if the pointers were labeled, especially for the reverse linked list example.

3

Reply
T
TropicalAquaGuineafowl629
Premium
• 3 months ago

tail

I think here is 'head'

2

Reply
C
CasualIvoryGoat374
Premium
• 10 months ago

Wording in the Advantages of a Dummy Node section seems vague imo. I'd suggest the following fix:

The advantage of using a dummy node for this question is that it allows us to avoid having to initialize the head of the final merged linked list as a special case. This also reduces the need to check if either of the linked lists to be merged are None, which we would need to do if we don't use a dummy node because we reference either l1.next or l2.next as part of initializing the head of the final merged linked list: if either l1 or l2 are None, then that reference would throw a null pointer exception.

2

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Basics

Basic Operations

Traversing a Linked List

Deleting a Node With a Given Target

Operations to Know for Interviews

1. Fast and Slow Pointers

2. Reversing a Linked List

3. Merging Two Linked Lists

Practice Problems

Dummy Nodes

Advantages of a Dummy Node

When to Use a Dummy Node

Practice Problems