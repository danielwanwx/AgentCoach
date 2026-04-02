# Palindrome Linked List

> Source: https://www.hellointerview.com/learn/code/linked-list/palindrome-linked-list
> Scraped: 2026-03-30


Linked List
Palindrome Linked List
easy
DESCRIPTION (inspired by Leetcode.com)

Given a reference of type ListNode which is the head of a singly linked list, write a function to determine if the linked list is a palindrome.

# Definition of a ListNode
class ListNode:
  def __init__(self, value=0, next=None):
    self.value = value
    self.next = next

A linked list is a palindrome if the values of the nodes are the same when read from left-to-right and right-to-left. An empty list is considered a palindrome.

Example 1:

5
4
3
4
5
head

Output:

True
left-to-right:  5 -> 4 -> 3 -> 4 -> 5
right-to-left: 5 -> 4 -> 3 -> 4 -> 5   

Example 2:

5
4
3
head

Output:

False
left-to-right:  5 -> 4 -> 3
right-to-left: 3 -> 4 -> 5
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
    def isPalindrome(self, head: ListNode) -> bool:
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
To determine if a linked list is a palindrome, we need to compare the values of the nodes when read from left-to-right and right-to-left. But since our linked list is singly linked, we can only read its values from left-to-right.
One way around this problem is to convert the linked list to a list, which supports reading values from both directions.
1. Convert to List: Compare Reverse
If we convert the original linked list to a list, we can compare the list with its reverse to determine if it is a palindrome. If the list is a palindrome, the list and its reverse will be equal.
nodes
​
|
nodes
list of integers
Try these examples:
Palindrome
Not Palindrome
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def isPalindrome(head):
    # convert linked list to list
    vals = []
    current_node = head
    while current_node:
        vals.append(current_node.val)
        current_node = current_node.next
    
    # compare list with its reverse
    return vals == vals[::-1]
5
4
3
4
5

palindrome linked list

0 / 7

1x
Time Complexity: O(n) where n is the number of nodes in the linked list. We iterate through each node in the linked list once to convert it to a list and then compare the list with its reverse, both of which are O(n) operations.
Space Complexity: O(n) where n is the number of nodes in the linked list, because we store the values of each node in a list.
2. Convert to List: Two-Pointer Technique
Instead of comparing the entire list with its reverse, we can use the two-pointer technique to check if the values in the list are a palindrome.
Like the previous solution, we first traverse the linked list and store the value of each node in a list.
Then, we initialize two pointers, left and right, at the start and end of the list, respectively. We compare the values at the left and right pointers. If they are equal, we move them both towards the center of the list. If the values at the left and right pointers are not equal, the list is not a palindrome.
nodes
​
|
nodes
list of integers
Try these examples:
Palindrome
Not Palindrome
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def isPalindrome(head):
    # convert linked list to list
    vals = []
    current = head
    while current:
        vals.append(current.val)
        current = current.next
    
    left, right = 0, len(vals) - 1
    while left < right:
        if vals[left] != vals[right]:
            return False
        left, right = left + 1, right - 1
    
    return True
5
4
3
4
5

palindrome linked list

0 / 10

1x
Time Complexity: O(n) where n is the number of nodes in the linked list. We iterate through each node in the linked list once to convert it to a list and then compare the values at the left and right pointers, which is also an O(n) operation. This is a slightly more time efficient solution than the previous one because we can stop as soon as we find a pair of values that are not equal during the palindrome check.
Space Complexity: O(n) where n is the number of nodes in the linked list. Like the previous solution, we store the values of each node in a list. This is also a slightly more space efficient solution than the previous one because we don't have to store the entire reverse of the list to compare it with the original.
3. Optimal Solution: Reverse Second Half
In the two-pointer above approach, we compared the first half of the list with the second half of the list, in reverse.
So if we first modify our linked list by reversing the direction of the nodes in the second half of the list, we can solve this problem without having to first convert the linked list to a list. This is the optimal solution, with a time complexity of O(n) and space complexity of O(1).
Step 1: Find The Middle Of The Linked List
This step can be done using fast and slow pointers, which involves initializing two pointers, fast and slow, at the head of the linked list, and then iterating until fast reaches the end of the list. At each iteration, slow moves one node forward and fast moves two nodes forward. When fast reaches the tail node of the list, slow will point to the middle node in the list.
VISUALIZATION
Python
Language
Full Screen
def is_palindrome(head):
  # find middle node of the list
  slow = fast = head
  while fast and fast.next:
    fast = fast.next.next
    slow = slow.next

  # reverse second half of the list
  curr, prev = slow, None
  while curr:
    next_ = curr.next # save next node
    curr.next = prev # reverse pointer
    prev = curr # move pointers
    curr = next_

  # Check palindrome
  left, right = head, prev
  while right:
    if left.val != right.val:
      return False
    left = left.next
    right = right.next
  return True
5
4
3
4
5
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
def is_palindrome(head):
  # find middle node of the list
  slow = fast = head
  while fast and fast.next:
    fast = fast.next.next
    slow = slow.next

  # reverse second half of the list
  curr, prev = slow, None
  while curr:
    next_ = curr.next # save next node
    curr.next = prev # reverse pointer
    prev = curr # move pointers
    curr = next_

  # Check palindrome
  left, right = head, prev
  while right:
    if left.val != right.val:
      return False
    left = left.next
    right = right.next
  return True
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
def is_palindrome(head):
  # find middle node of the list
  slow = fast = head
  while fast and fast.next:
    fast = fast.next.next
    slow = slow.next

  # reverse second half of the list
  curr, prev = slow, None
  while curr:
    next_ = curr.next # save next node
    curr.next = prev # reverse pointer
    prev = curr # move pointers
    curr = next_

  # Check palindrome
  left, right = head, prev
  while right:
    if left.val != right.val:
      return False
    left = left.next
    right = right.next
  return True
5
4
3
4
5
slow
fast

find middle node

0 / 10

1x
You need the next_pointer to store the next node in the iteration before overwriting the value of curr.next with prev. If you don't store the next node in the iteration, you will lose the reference to the rest of the linked list.
Step 3: Check For Palindrome
With the nodes reversed, we can now use two pointers to compare the values of the nodes in the first half of the list with the reversed second half of the list.
At this point, prev points to the head of the reversed second half of the list. We can set a pointer left equal to the head of the original list and right equal to prev.
We then iterate through the list, comparing the values at left and right. If the values are not equal, the list is not a palindrome. If they are equal, we move left and right towards the center of the list, until they meet at the same node, at which point we return True because our list is a palindrome.
VISUALIZATION
Python
Language
Full Screen
def is_palindrome(head):
  # find middle node of the list
  slow = fast = head
  while fast and fast.next:
    fast = fast.next.next
    slow = slow.next

  # reverse second half of the list
  curr, prev = slow, None
  while curr:
    next_ = curr.next # save next node
    curr.next = prev # reverse pointer
    prev = curr # move pointers
    curr = next_

  # Check palindrome
  left, right = head, prev
  while right:
    if left.val != right.val:
      return False
    left = left.next
    right = right.next
  return True
5
4
3
4
5
prev
curr
next_

curr = next_, prev = curr

0 / 5

1x
Detecting the list is not a palindrome:
VISUALIZATION
Python
Language
Full Screen
def is_palindrome(head):
  # find middle node of the list
  slow = fast = head
  while fast and fast.next:
    fast = fast.next.next
    slow = slow.next

  # reverse second half of the list
  curr, prev = slow, None
  while curr:
    next_ = curr.next # save next node
    curr.next = prev # reverse pointer
    prev = curr # move pointers
    curr = next_

  # Check palindrome
  left, right = head, prev
  while right:
    if left.val != right.val:
      return False
    left = left.next
    right = right.next
  return True
5
4
2
3
5
prev
curr
next_

curr = next_, prev = curr

0 / 3

1x
Returning false because 4 != 3
To recap:
Find the middle of the linked list using the fast and slow pointers technique.
Reverse the direction of the nodes in the second half of the linked list.
Use two-pointers to check for a palindrome by comparing the values of the nodes in the first half of the list with the reversed second half of the list.
Implementation
Here's the complete optimal solution that implements the three-step approach:
SOLUTION
Python
Language
def is_palindrome(head):
    # Find middle of the linked list using fast and slow pointers
    slow = fast = head
    while fast and fast.next:
        fast = fast.next.next
        slow = slow.next

    # Reverse second half of the list
    curr, prev = slow, None
    while curr:
        next_ = curr.next  # Save next node
        curr.next = prev   # Reverse pointer
        prev = curr        # Move pointers
        curr = next_

    # Check palindrome by comparing halves
    left, right = head, prev
    while right:
        if left.val != right.val:
            return False
        left = left.next
        right = right.next
    return True
Code
To construct the linked list that is used in the animation below, provide a list of integers nodes. Each integer in nodes is used as the value of a node in the linked list, and the order of the integers in the list will be the order of the nodes in the linked list.
For example, if nodes = [1, 2, 3], the linked list will be 1 -> 2 -> 3.
nodes
​
|
nodes
list of integers
Try these examples:
Palindrome
Not Palindrome
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def is_palindrome(head):
  # find middle node of the list
  slow = fast = head
  while fast and fast.next:
    fast = fast.next.next
    slow = slow.next

  # reverse second half of the list
  curr, prev = slow, None
  while curr:
    next_ = curr.next # save next node
    curr.next = prev # reverse pointer
    prev = curr # move pointers
    curr = next_

  # Check palindrome
  left, right = head, prev
  while right:
    if left.val != right.val:
      return False
    left = left.next
    right = right.next
  return True
5
4
3
4
5

palindrome linked list

0 / 18

1x
Edge Cases
Empty List
When the linked list is empty, all of the pointers will be None, and the function returns True immediately because an empty list is a palindrome.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def is_palindrome(head):
  # find middle node of the list
  slow = fast = head
  while fast and fast.next:
    fast = fast.next.next
    slow = slow.next

  # reverse second half of the list
  curr, prev = slow, None
  while curr:
    next_ = curr.next # save next node
    curr.next = prev # reverse pointer
    prev = curr # move pointers
    curr = next_

  # Check palindrome
  left, right = head, prev
  while right:
    if left.val != right.val:
      return False
    left = left.next
    right = right.next
  return True
None

palindrome linked list

0 / 4

1x
`nodes = []`
Single Node
When the linked list has a single node:
fast.next is None, so the first while loop to find the middle node doesn't execute.
Reversing the second half of the list has no effect because there is only one node.
The palindrome check returns True because a single node is a palindrome.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def is_palindrome(head):
  # find middle node of the list
  slow = fast = head
  while fast and fast.next:
    fast = fast.next.next
    slow = slow.next

  # reverse second half of the list
  curr, prev = slow, None
  while curr:
    next_ = curr.next # save next node
    curr.next = prev # reverse pointer
    prev = curr # move pointers
    curr = next_

  # Check palindrome
  left, right = head, prev
  while right:
    if left.val != right.val:
      return False
    left = left.next
    right = right.next
  return True
5

palindrome linked list

0 / 8

1x
`nodes = [5]`
Two Nodes (Palindrome)
When the linked list has two nodes:
The first while loop sets the slow pointer to the second node.
Reversing the second half of the list has no effect slow.next is None already.
The palindrome check compares the values of the two nodes and returns True if they are equal.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def is_palindrome(head):
  # find middle node of the list
  slow = fast = head
  while fast and fast.next:
    fast = fast.next.next
    slow = slow.next

  # reverse second half of the list
  curr, prev = slow, None
  while curr:
    next_ = curr.next # save next node
    curr.next = prev # reverse pointer
    prev = curr # move pointers
    curr = next_

  # Check palindrome
  left, right = head, prev
  while right:
    if left.val != right.val:
      return False
    left = left.next
    right = right.next
  return True
2
2

palindrome linked list

0 / 9

1x
`nodes = [2, 2]`
Two Nodes (Not Palindrome)
VISUALIZATION
Hide Code
Python
Language
Full Screen
def is_palindrome(head):
  # find middle node of the list
  slow = fast = head
  while fast and fast.next:
    fast = fast.next.next
    slow = slow.next

  # reverse second half of the list
  curr, prev = slow, None
  while curr:
    next_ = curr.next # save next node
    curr.next = prev # reverse pointer
    prev = curr # move pointers
    curr = next_

  # Check palindrome
  left, right = head, prev
  while right:
    if left.val != right.val:
      return False
    left = left.next
    right = right.next
  return True
2
3

palindrome linked list

0 / 8

1x
`nodes = [2, 3]`
What is the time complexity of this solution?
1

O(n)

2

O(2ⁿ)

3

O(n³)

4

O(4ⁿ)

Trade-off: The O(1) space solution mutates the input
The O(1) space solution comes with a significant practical downside: it mutates the input linked list. During execution, the second half of the list is reversed in-place, which means any other code holding a reference to nodes in that portion of the list will see a corrupted structure while the check is running.
You could reverse the second half again after the palindrome check to restore the original list, but that's additional O(n) work and still isn't safe in concurrent or multi-threaded contexts where another thread might read the list mid-mutation.
In real-world code, mutating an input data structure passed to a read-only query function like isPalindrome is almost always unacceptable. If you need to avoid mutation, you're back to O(n) space — whether that's copying the list, collecting values into an array, or using a stack. The array-based solutions (Solutions 1 and 2 above) are typically the better choice in practice for this reason.
The O(1) space approach is worth knowing because interviewers often ask for it specifically, and it demonstrates important linked list manipulation techniques (fast/slow pointers, in-place reversal). Just be ready to discuss why you might not use it in production.

Mark as read

Next: Remove Nth Node From End of List

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

(13)

Comment
Anonymous
​
Sort By
Popular
Sort By
B
Bruk
• 3 months ago
• edited 1 month ago

using a stack to store values in nodes in first half.

class Solution:
    def isPalindrome(self, head: ListNode):
        slow = fast = head 
        stack = []
        while fast and fast.next:
            stack.append(slow.val)
            slow = slow.next
            fast = fast.next.next 

        # skip poping once  if the length is odd
        if fast:
            slow = slow.next 

        while slow:
            if slow.val != stack.pop():
                return False 
            slow = slow.next 

        return True
Show More

3

Reply
Stanley Lin
• 1 month ago

I came up with this exact solution right now. Awesome

1

Reply
Abhay Singh
Top 1%
• 1 year ago

Java Solution:

class Solution {

    ListNode reverse(ListNode head){
        ListNode q = null, p = head;
        while(p != null){
            ListNode nxt = p.next;

            p.next = q;
            q = p;
            p = nxt;
        }
        return q;
    }

    ListNode middle(ListNode head){
        ListNode slow, fast;

        slow = head;
        fast = head.next;
        while(slow!=null && fast!=null && fast.next!=null){
            slow = slow.next;
            fast = fast.next.next;
        }

        return slow;
    }

    public boolean isPalindrome(ListNode head) {
        ListNode mid = middle(head);
        ListNode secondHalf = reverse(mid.next);
        mid.next = null;

        while(secondHalf != null){
            if(head.val != secondHalf.val){
                return false;
            }
            head = head.next;
            secondHalf = secondHalf.next;
        }

        return true;
    }
}
Show More

3

Reply
C
c0ff33f4ce
Premium
• 3 months ago

Won't something like this also work ?

ListNode front;

boolean isPalindrome(ListNode head) {
    front = head;
    return recurse(head);
}

boolean recurse(ListNode node) {
    if (node == null) return true;

    if (!recurse(node.next)) return false;

    boolean equal = (node.val == front.val);
    front = front.next;
    return equal;
}

This way we have O(n) traversal and keep the original list intact?

2

Reply
Thanh Nguyễn
Premium
• 2 months ago

Yes, but you also need O(n) space for the stack frames, and this is quite complex than reversing the list. But your solution is correct.

1

Reply
E
EquivalentLavenderFinch265
Premium
• 6 months ago

Can you add a place to write the code on this site

1

Reply
mohammad nayeem
• 1 year ago
class ListNode {
    int val;
    ListNode next;
    ListNode(int x) { val = x; }
}

public class Solution {
    public boolean isPalindrome(ListNode head) {
        if (head == null) return true;
        
        // Find the middle node
        ListNode slow = head;
        ListNode fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }
        
        // Reverse the second half
        ListNode curr = slow;
        ListNode prev = null;
        while (curr != null) {
            ListNode next = curr.next;
            curr.next = prev;
            prev = curr;
            curr = next;
        }
        
        // Compare the first half and the reversed second half
        ListNode left = head;
        ListNode right = prev;
        while (right != null) {
            if (left.val != right.val) {
                return false;
            }
            left = left.next;
            right = right.next;
        }
        return true;
    }
}
Show More

1

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Solutions

1. Convert to List: Compare Reverse

2. Convert to List: Two-Pointer Technique

3. Optimal Solution: Reverse Second Half

Implementation

Code

Edge Cases

Trade-off: The O(1) space solution mutates the input
