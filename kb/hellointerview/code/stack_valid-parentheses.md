# Valid Parentheses

> Source: https://www.hellointerview.com/learn/code/stack/valid-parentheses
> Scraped: 2026-03-30


Stack
Valid Parentheses
easy
DESCRIPTION (inspired by Leetcode.com)

Given an input string s consisting solely of the characters '(', ')', '{', '}', '[' and ']', determine whether s is a valid string. A string is considered valid if every opening bracket is closed by a matching type of bracket and in the correct order, and every closing bracket has a corresponding opening bracket of the same type.

Example 1:

Inputs:

s = "(){({})}"

Output:

True

Example 2:

Inputs:

s = "(){({}})"

Output:

False
CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def isValid(self, s: str) -> bool:
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
The input string can contain nested brackets which must adhere to a Last-In, First-Out ordering (i.e. if our input string is {[, then the closing ] must come before before the closing }). For this reason, our solution will use a stack.
The solution iterates through the string. Whenever it encounters an opening bracket, the bracket is pushed onto the stack. When it encounters a closing bracket, we check to see if it is the corresponding closing bracket for the opening bracket at the top of the stack. If it is, we pop from the stack (because we have found a matching parantheses) and continue iterating. If it isn't, the string is invalid, and we return False.
The string is valid if the stack is empty after iterating through the string.
Solution
s
​
|
s
string
Try these examples:
Empty
Nested
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def isValid(s):
  stack = []
  mapping = {")": "(", "}": "{", "]": "["}

  for char in s:
    if char in mapping:
      if not stack or stack[-1] != mapping[char]:
        return False
      stack.pop()
    else:
      stack.append(char)

  return len(stack) == 0
(
)
{
(
{
}
)
}

valid parentheses

0 / 18

1x

Mark as read

Next: Decode String

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

(21)

Comment
Anonymous
​
Sort By
Popular
Sort By
Patricia Pan
Top 1%
• 2 years ago

I knew that this solution used a stack since this problem was in the stack section. From there, I came up with the below solution which is similar but slightly different from the one here:

class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        match = {
            '(':')',
            '{':'}',
            '[':']'
        }
        for char in s:
            if char in match:
                stack.append(match[char])
            else:
                if not stack:
                    return False
                expected = stack.pop()
                if char != expected:
                    return False

        return True and len(stack) == 0
Show More

11

Reply
Arup Chauhan
Premium
• 6 days ago

You have made the dictionary very elegantly, copying it as future style.

0

Reply
S
socialguy
Top 5%
• 1 year ago

Problem description is missing curly braces.

2

Reply
Abhay Singh
Top 1%
• 1 year ago

Java Solution:

class Solution {

    public boolean isMatchingParenthese(char cur, char top){
        return ((cur == ')' && top == '(') || (cur == '}' && top == '{') || (cur == ']' && top == '['));
    }

    public boolean isValid(String s) {
        int n = s.length();

        Stack<Character> st = new Stack<>();
        for(int i=0;i<s.length();i++){
            char ch = s.charAt(i);
            if(ch == '(' || ch == '{' || ch == '['){
                st.push(ch);
            }else{
                if(!st.isEmpty() && isMatchingParenthese(ch, st.peek())){
                    st.pop();
                }else{
                    return false;
                }
            }
        }

        return st.isEmpty();
    }
}

Show More

1

Reply
C
CuriousPlumImpala974
Premium
• 9 days ago
• edited 9 days ago

we can also do early exit by checking if the length of the input string is even or not ( some minor performance optimization )

0

Reply
I
ImpressiveMaroonSnail520
• 1 month ago

C# Solution

public class Solution {
    public bool isValid(string s) {
        if(s == null) return true;
        // Your code goes here
        Stack<char> st =new Stack<char>();
        foreach(char c in s)
        {
            if(c == '(' || c== '[' || c == '{')
            {
                st.Push(c);
            }
            else
            {
                if(st.Count == 0) return false;
                //if stack is empty, then we cannot pop, hence a check before is good
                char openChar =  st.Peek();
                char closeChar = c;

                if(!IsMatching(openChar, closeChar)) return false;
                st.Pop();
            }
        }
        return st.Count == 0;
    }

    private bool IsMatching(char openChar, char closeChar)
    {
        bool a = (openChar == '(' && closeChar == ')');
        bool b = (openChar == '[' && closeChar == ']');
        bool c = (openChar == '{' && closeChar == '}');

        if(a || b || c) return true;
        return false;
    }
}
Show More

0

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

Solution
