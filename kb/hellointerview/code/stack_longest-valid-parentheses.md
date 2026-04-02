# Longest Valid Parentheses

> Source: https://www.hellointerview.com/learn/code/stack/longest-valid-parentheses
> Scraped: 2026-03-30


Stack
Longest Valid Parentheses
hard
DESCRIPTION (inspired by Leetcode.com)

Given a string containing just the characters '(' and ')', find the length of the longest valid (well-formed) parentheses substring. A well-formed parentheses string is one that follows these rules:

Open brackets must be closed by a matching pair in the correct order.

For example, given the string "(()", the longest valid parentheses substring is "()", which has a length of 2. Another example is the string ")()())", where the longest valid parentheses substring is "()()", which has a length of 4.

Example 1:
Inputs:

s = "())))"

Output:

2

(Explanation: The longest valid parentheses substring is "()")

Example 2:
Inputs:

s = "((()()())"

Output:

8

(Explanation: The longest valid parentheses substring is "(()()())" with a length of 8)

Example 3:
Inputs:

s = ""

Output:

0
CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def longest_valid_parentheses(self, s: str) -> int:
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
At a high level, we can solve this problem by iterating over each index of the string, and then calculating the length of the longest valid parentheses substring that ends at that index. We can then take the maximum of these lengths to get the final answer.
Each time we encounter a closing parenthesis ')', it has the potential to close a valid parentheses substring. In order to calculate the length of the longest valid parentheses substring that ends at a given index, we need to know the index of the last unmatched opening parenthesis '('.
The length of the valid substring ending at the current index can be calculated by taking the difference between the current index and the index of the last unmatched opening parenthesis.
Let's visualize a few examples to understand how that calculation works:
(
(
)
2
0
1
Current index: 2. Last unmatched opening parenthesis at index 0. Length: 2 - 0 = 2
(
(
)
(
3
0
1
2
Current index: 3. Last unmatched opening parenthesis at index 1. Length: 3 - 1 = 2
(
(
)
(
(
)
3
0
1
5
2
4
Current index: 5. Last unmatched opening parentheses = 1. Length = 5 - 1 = 4.
If there aren't any unmatched opening parentheses remaining after using the current closing parentheses, then we need to know the "start" of the current valid substring. Setting this value to -1 makes our calculation easier, as we can simply take the difference between the current index and the start of the valid substring to get the length.
(
)
)
(
3
-1
1
2
0
Current index: 3. The start of the current valid substring is -1, so length = 3 - (-1) = 4
However, if the closing parenthesis ')' doesn't close any valid substring (as shown below), then we can simply ignore it, and set the start of the current valid substring to the current index.
(
)
)
)
 
3
0
1
2
Current index: 3. But there is no unmatched opening parenthesis. Length: 0
This leads us to the following algorithm:
Initialize a stack. The stack will always contain the index of the last unmatched opening parenthesis, or the "start" of the current valid substring. Initially, the stack will contain -1 as the start of the current valid substring.
Each time we encounter an opening parenthesis '(', we'll push its index onto the stack, which represents the index of the last unmatched opening parenthesis.
Each time we encounter a closing parenthesis ')', we'll do the following:
We first pop the top element from the stack, as this closing parenthesis has the potential to close a valid parentheses substring.
Now, after popping, there are two possible cases:
The stack is not empty, and the top of the stack represents the index of the last unmatched opening parenthesis. We calculate the length of the valid substring ending at the current index by taking the difference between the current index and the index of the last unmatched opening parenthesis.
The stack is empty. This means that this closing parenthesis was unmatched. We'll update the start of the valid substring to the current index by pushing the current index onto the stack.
Solution
s
​
|
s
string
Try these examples:
All Open
Separated
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def longest_valid_parentheses(s):
  max_len = 0
  stack = [-1]
  
  for i, char in enumerate(s):
    if char == '(':
      stack.append(i)
    else:
      stack.pop()
      if not stack:
        stack.append(i)
      else:
        max_len = max(max_len, i - stack[-1])
  
  return max_len
(
(
)
(
)
)

longest valid parentheses

0 / 17

1x
Solution Visualization
s
​
|
s
string
Try these examples:
All Open
Separated
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def longest_valid_parentheses(s):
  max_len = 0
  stack = [-1]
  
  for i, char in enumerate(s):
    if char == '(':
      stack.append(i)
    else:
      stack.pop()
      if not stack:
        stack.append(i)
      else:
        max_len = max(max_len, i - stack[-1])
  
  return max_len
(
(
)
(
)
)

longest valid parentheses

0 / 17

1x
Walkthrough
Example 1
s = "(()())":
Initialization: Stack: [-1]
Traverse the string:
Index 0, '(':
Push index 0 onto the stack.
Stack: [-1, 0]
Index 1, '(':
Push index 1 onto the stack.
Stack: [-1, 0, 1]
Index 2, ')':
Pop the stack (index 1).
Stack: [-1, 0]
Calculate length: 2 - 0 = 2
Index 3, '(':
Push index 3 onto the stack.
Stack: [-1, 0, 3]
Index 4, ')':
Pop the stack (index 3).
Stack: [-1, 0]
Calculate length: 4 - 0 = 4
Index 5, ')':
Pop the stack (index 0).
Stack: [-1]
Calculate length: 5 - (-1) = 6
Return
We can return the max of each calculated length, which is 6.
Example 2
s = ")())()()"
Initialization: Stack: [-1]
Traverse the string:
Index 0, ')':
Pop the stack (index -1). The stack is empty, so push index 0 onto the stack.
Note: We don't need to calculate the length here, as there is no valid substring ending at index 0. Instead, index 0 will be the start of the next valid substring.
Stack: [0]
Index 1, '(':
Push index 1 onto the stack.
Stack: [0, 1]
Index 2, ')':
Pop the stack (index 1).
Stack: [0]
Calculate length: 2 - 0 = 2
Index 3, ')':
Pop the stack (index 0). The stack is empty, so push index 3 onto the stack.
Note: We don't need to calculate the length here, as there is no valid substring ending at index 3. Instead, index 3 will be the start of the next valid substring.
Stack: [3]
Index 4, '(':
Push index 4 onto the stack.
Stack: [3, 4]
Index 5, ')':
Pop the stack (index 4).
Stack: [3]
Calculate length: 5 - 3 = 2
Index 6, '(':
Push index 6 onto the stack.
Stack: [3, 6]
Index 7, ')':
Pop the stack (index 6).
Stack: [3]
Calculate length: 7 - 3 = 4
Return
We can return the max of each calculated length, which is 4.
What is the time complexity of this solution?
1

O(n)

2

O(n³)

3

O(2ⁿ)

4

O(n * logn)

Mark as read

Next: Monotonic Stack

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

(18)

Comment
Anonymous
​
Sort By
Popular
Sort By
Allen Liu (Hsin-tzu)
Top 5%
• 6 months ago

I came up with this solution, which passed all test cases (include Leetcode), before I looked at the answer.

class Solution:
    def longestValidParentheses(self, s: str) -> int:
        
        ans = 0
        curr_len = 0
        stack = []

        for c in s:
            if c == '(':
                stack.append(curr_len)
                curr_len = 0
            elif stack:
                curr_len += stack.pop() + 2
                ans = max(ans, curr_len)
            else:
                curr_len = 0

        return ans

What happens here is as follows:

we always push the opening parenthesis '(' and only the opening parenthesis into the stack. --> We end up with a stack of unclosed opening parentheses during the traversal process.
We need to keep track of the length of the latest valid length that ends right before the last unclosed opening parenthesis. --> Therefore, instead of actually pushing an opening "parenthesis" into the stack, i push the current valid length instead whereas the mere presence of a stack item already imply an unclosed opening parenthesis.
As we encounter a closing parenthesis during the traversal, we pop from the stack and add 2 to the last valid length.
Show More

19

Reply
MM
Minnie Mouse
Top 5%
• 23 days ago

Very elegant. Well done.

0

Reply
Zaber Jamal
• 4 months ago

Love this solution bro thank you

0

Reply
aditya patel
Premium
• 1 month ago

One liner to remember this solution:

current_index - last_invalid_index = valid_length****

5

Reply
Abhay Singh
Top 1%
• 1 year ago

Java Solution:

class Solution {
    public int longestValidParentheses(String s) {
        Stack<Integer> st = new Stack<>();
        
        // index before start of possible valid sub-string
        st.push(-1);

        int n = s.length();
        int ans = 0;
        for(int i=0;i<n;i++){
            char ch = s.charAt(i);

            if(ch == '('){
                st.push(i);
            }else{
                st.pop();
                if(st.isEmpty()){
                    st.push(i);
                }else{
                    ans = Math.max(ans, i - st.peek());
                }
            }
        }

        return ans;
    }
}
Show More

2

Reply
O
OkVioletAmphibian280
Premium
• 1 month ago
int longestValidParentheses(string s) {
        int ans = 0;
        stack<int> st;
        st.push(-1);
        for(int i=0; i<s.size(); i++){
            if(s[i] == '(') st.push(i);
            else{
                st.pop();
                if(st.empty()) st.push(i);
                else ans = max(ans, i - st.top());
            }
        }
        return ans;
    }

1

Reply
R
rathinam.ramesh
Premium
• 6 months ago

Why cant we apply the same approach as in "ValidParentheses" and have a counter(multiply by 2) whenever the stack pop
public static boolean isValid(String s) {
Stack<Character> stack = new Stack<>();
Map<Character, Character> mapping = new HashMap<>();
mapping.put(')', '('); mapping.put('}', '{'); mapping.put(']', '[');
int count = 0;

    for (char c : s.toCharArray()) {
        if (mapping.containsKey(c)) {
            if (stack.isEmpty() || stack.peek() != mapping.get(c)) {
                return false;
            }
            stack.pop();
            count++;
        } else {
            stack.push(c);
        }
    }
    return stack.isEmpty();
}


1

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

Solution

Solution Visualization

Walkthrough
