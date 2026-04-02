# Linked List Cycle

> Source: https://www.hellointerview.com/learn/code/linked-list/linked-list-cycle
> Scraped: 2026-03-30


Linked List
Linked List Cycle
easy
DESCRIPTION (inspired by Leetcode.com)

Write a function that takes in a parameter head of type ListNode that is a reference to the head of a linked list. The function should return True if the linked list contains a cycle, and False otherwise, without modifying the linked list in any way.

# Definition of a ListNode
class ListNode:
  def __init__(self, value=0, next=None):
    self.value = value
    self.next = next

Example 1:

5
4
3
2
0
head

Output: true, there is a cycle between node 0 and node 3.

Example 2:

5
4
3
2
0
head

Output: false, there is no cycle in the linked list.

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
    def hasCycle(self, head: ListNode) -> bool:
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

We recommend taking some time to solve the problem on your own before reading the solutions below.
Solutions
1. Keep Track of Visited Nodes
One approach to this problem is to keep a set of visited nodes while iterating through the linked list. At each node, we check if the node exists in the set. If it does, then the linked list contains a cycle. If it doesn't, we add the node to the set and move to the next node. If we reach the end of the linked list without encountering a node in the dictionary, then the linked list does not contain a cycle.
SOLUTION
Python
Language
class ListNode:
  def __init__(self, val=0, next=None):
    self.val = val
    self.next = next

def hasCycle(head):
  visited_nodes = set()

  current_node = head
  while current_node is not None:
    if current_node in visited_nodes:
      return True  # Cycle detected

    visited_nodes.add(current_node)
    current_node = current_node.next

  return False
What is the time complexity of this solution?
1

O(n)

2

O(N + Q)

3

O(m * n)

4

O(m * n * 4^L)

2. Optimal Solution: Fast and Slow Pointers
The approach above requires O(n) space to store each visited node in the set. A more optimal solution solves this problem without using additional space (i.e. constant, O(1) space) by using fast and slow pointers.
This approach starts by initializing two pointers, fast and slow at the head of the list. It then iterates over the linked list, and in each iteration, the slow pointer advances by one node, while the fast pointer advances by two nodes.
Detecting A Cycle
If the linked list contains a cycle, the fast pointer will eventually overlap the slow pointer, and both pointers will point to the same node.
VISUALIZATION
Full Screen
5
4
3
2
0
slow
fast

initialize pointers

0 / 4

1x
When the list contains a cycle, fast and slow eventually meet at the same node.
No Cycle
When there is no cycle, the fast pointer reaches the tail of the linked list, where fast.next = None (step 3 in the animation below). This is enough to determine the linked list does not contain a cycle.
VISUALIZATION
Full Screen
5
4
3
2
0
slow
fast

initialize pointers

0 / 3

1x
If there is no cycle, eventually `fast.next = None`
When there is no cycle and the linked list has an even number of nodes, eventually fast = None (step 2 in the animation below).
VISUALIZATION
Full Screen
5
4
3
0
slow
fast

initialize pointers

0 / 3

1x
Even # of nodes and no cycle, eventually `fast.next = None`
Putting it all together, our algorithm involves the following steps:
Initialize fast and slow pointers at the head of the linked list.
Iterate over the linked list. Each iteration advances slow by one node and fast by two nodes.
If the fast pointer reaches the end of the linked list (either fast.next = None or fast = None), then the linked list does not contain a cycle.
If the fast and slow pointers meet at the same node (fast == slow), then the linked list contains a cycle.
Code
To construct the linked list that is used in the animation below, provide a list of integers nodes and an integer tail. Each integer in nodes is used as the value of a node in the linked list, and the order of the integers in the list will be the order of the nodes in the linked list.
The tail integer is the index of the node that the last node in the linked list points to form a cycle. If there is no cycle, set tail = -1.
nodes
​
|
nodes
list of integers
tail
​
|
tail
integer
Try these examples:
No Cycle
Cycle At 1
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def hasCycle(head):
    slow = head
    fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        if slow == fast:
            return True

    return False
5
4
3
2
0

linked list cycle

0 / 5

1x
Edge Cases
Empty List
When the linked list is empty, fast = None to start, the while loop never runs and the function returns False.
VISUALIZATION
Hide Code
Python
Language
Full Screen
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def hasCycle(head):
    slow = head
    fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        if slow == fast:
            return True

    return False

linked list cycle

0 / 2

1x
`nodes = []`, `tail = -1`
Single Node (No Cycle)
When the linked list contains a single node without a cycle, fast.next = None to start and the function returns False without running the while loop.
VISUALIZATION
Hide Code
Python
Language
Full Screen
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def hasCycle(head):
    slow = head
    fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        if slow == fast:
            return True

    return False
1

linked list cycle

0 / 2

1x
`nodes = [1]`, `tail = -1`
Single Node (With Cycle)
When the linked list contains a single node with a cycle, slow.next and fast.next.next point to the same single node, and the function returns True during the first iteration of the while loop.
VISUALIZATION
Hide Code
Python
Language
Full Screen
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def hasCycle(head):
    slow = head
    fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        if slow == fast:
            return True

    return False
1

linked list cycle

0 / 3

1x
`nodes = [1]`, `tail = 0`
Worst Case Scenario
In the worst case scenario, the fast pointer traverses the entire list twice before meeting the slow pointer.
VISUALIZATION
Hide Code
Python
Language
Full Screen
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def hasCycle(head):
    slow = head
    fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        if slow == fast:
            return True

    return False
5
4
3
2

linked list cycle

0 / 6

1x
`nodes = [5, 4, 3, 2]`, `tail = 0`
What is the time complexity of this solution?
1

O(n)

2

O(N + Q)

3

O(m * n)

4

O(m * n * 4^L)

Mark as read

Next: Palindrome Linked List

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

(12)

Comment
Anonymous
​
Sort By
Popular
Sort By
C
CalmIndigoPython390
Top 1%
• 1 year ago

The edge cases are very well done -- thank you for not just mentioning them, but also visualizing them!

21

Reply
Abhay Singh
Top 1%
• 1 year ago

Java Solution:

public class Solution {
    public boolean hasCycle(ListNode head) {
        Set<ListNode> st = new HashSet<>();

        while(head != null){
            if(st.contains(head)){
                return true;
            }
            st.add(head);
            head = head.next;
        }

        return false;
    }
}
public class Solution {
    public boolean hasCycle(ListNode head) {
        if(head == null) return false;

        ListNode slow, fast;
        slow = head;
        fast = head.next;

        while(slow != null && fast != null && slow != fast){
            slow = slow.next;
            fast = fast.next;
            if(fast != null){
                fast = fast.next;
            }
        }

        return slow == fast;
    }
}
Show More

3

Reply
Neil Belen
• 1 year ago

Hi, not sure if its meant to be this way but there is no where on this page to input our solution. It starts with the question then straight to the solution after the question box.

3

Reply
Dhruv Erry
• 1 year ago

Simply solve it on LeetCode Neil.

4

Reply
Manu GP
Premium
• 5 months ago

But I'm paying helloInterview not LeetCode.

1

Reply

Evan King

Admin
• 5 months ago

Will try to add! FYI, all code content is free

2

Reply
D
DynamicScarletDove797
• 18 days ago

There are no test cases involving the actual cycle. All the expected values are false.

0

Reply
Stanley Lin
• 1 month ago

I am struggling to see how single node is True. The while loop will not run because fast.next is none and we will simply move straight to False. Perhaps I am not seeing things correctly, someone can clarify

0

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Solutions

1. Keep Track of Visited Nodes

2. Optimal Solution: Fast and Slow Pointers

Code

Edge Cases
