# Decode String

> Source: https://www.hellointerview.com/learn/code/stack/decode-string
> Scraped: 2026-03-30


Stack
Decode String
medium
DESCRIPTION (inspired by Leetcode.com)

Given an encoded string, write a function to return its decoded string that follows a specific encoding rule: k[encoded_string], where the encoded_string within the brackets is repeated exactly k times. Note that k is always a positive integer. The input string is well-formed without any extra spaces, and square brackets are properly matched. Also, assume that the original data doesn't contain digits other than the ones that specify the number of times to repeat the following encoded_string.

Inputs:

s = "3[a2[c]]"

Output:

"accaccacc"
CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def decodeString(self, s: str) -> str:
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
We start by initializing our stack, and the variables curr_string and current_number. The stack allows us to account for nested sequences correctly. curr_string represents the current string we currently decoding, and current_number represents the number of times we need to repeat it when the current decode sequence is completed (i.e. when we encounter a closing "]" bracket).
VISUALIZATION
Hide Code
Python
Language
Full Screen
def decodeString(s):
  stack = []
  curr_string = ""
  current_number = 0

  for char in s:
    if char == "[":
      stack.append(curr_string)
      stack.append(current_number)
      curr_string = ""
      current_number = 0
    elif char == "]":
      num = stack.pop()
      prev_string = stack.pop()
      curr_string = prev_string + num * curr_string
    elif char.isdigit():
      current_number = current_number * 10 + int(char)
    else:
      curr_string += char

  return curr_string
3
[
a
2
[
c
]
]

decode string

0 / 1

1x
We then iterate over each character in the encoded string, handling each character as follows:
"[": Start Of A New Sequence
When we encounter an opening bracket, we push the current string curr_string and the current number current_number to the stack and reset curr_string to an empty string and current_number to 0.
These values that we pushed onto the stack represent the "context" of the current sequence we are decoding. We use current_number to keep track of the number of times we need to repeat the current string we are about to decode, while curr_string represents the value of the string that will be prepended to the result of the current sequence.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def decodeString(s):
  stack = []
  curr_string = ""
  current_number = 0

  for char in s:
    if char == "[":
      stack.append(curr_string)
      stack.append(current_number)
      curr_string = ""
      current_number = 0
    elif char == "]":
      num = stack.pop()
      prev_string = stack.pop()
      curr_string = prev_string + num * curr_string
    elif char.isdigit():
      current_number = current_number * 10 + int(char)
    else:
      curr_string += char

  return curr_string
3
[
a
2
[
c
]
]
stack
currString: ""
currNumber: 3

[

0 / 2

1x
"]": End Of A Sequence
When we encounter a closing bracket, we pop the last element from the stack and repeat the current string curr_string by the number of times current_number and append it to the string at the top of the stack.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def decodeString(s):
  stack = []
  curr_string = ""
  current_number = 0

  for char in s:
    if char == "[":
      stack.append(curr_string)
      stack.append(current_number)
      curr_string = ""
      current_number = 0
    elif char == "]":
      num = stack.pop()
      prev_string = stack.pop()
      curr_string = prev_string + num * curr_string
    elif char.isdigit():
      current_number = current_number * 10 + int(char)
    else:
      curr_string += char

  return curr_string
3
[
a
2
[
c
]
]
""
3
a
2
stack
currString: c
currNumber: 0

]

0 / 1

1x
We are finished decoding 2[c], so we repeat \"c\"2 times and prepend \"a\" and pop the top two values from the stack.
Digit
When char is a digit, we update current_number by multiplying it by 10 and adding the value of the digit. current_number is used to keep track of the number of times we need to repeat the current string we are just about to decode.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def decodeString(s):
  stack = []
  curr_string = ""
  current_number = 0

  for char in s:
    if char == "[":
      stack.append(curr_string)
      stack.append(current_number)
      curr_string = ""
      current_number = 0
    elif char == "]":
      num = stack.pop()
      prev_string = stack.pop()
      curr_string = prev_string + num * curr_string
    elif char.isdigit():
      current_number = current_number * 10 + int(char)
    else:
      curr_string += char

  return curr_string
3
[
a
2
[
c
]
]
stack
currString: ""
currNumber: 0

initialize variables

0 / 2

1x
We need to repeat the result of decoding a2[c] 3 times.
Letter
When we encounter a letter, we append it to the current string curr_string.
Solution
s
​
|
s
string
Try these examples:
Simple
Nested
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def decodeString(s):
  stack = []
  curr_string = ""
  current_number = 0

  for char in s:
    if char == "[":
      stack.append(curr_string)
      stack.append(current_number)
      curr_string = ""
      current_number = 0
    elif char == "]":
      num = stack.pop()
      prev_string = stack.pop()
      curr_string = prev_string + num * curr_string
    elif char.isdigit():
      current_number = current_number * 10 + int(char)
    else:
      curr_string += char

  return curr_string
3
[
a
2
[
c
]
]

decode string

0 / 20

1x
Complexity Analysis
For this problem, let n be the length of the input string and S be the length of the decoded output string.
What is the time complexity of this solution?
1

O(4ⁿ)

2

O(n³)

3

O(1)

4

O(S)

Mark as read

Next: Longest Valid Parentheses

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

(33)

Comment
Anonymous
​
Sort By
Popular
Sort By
I
InnovativeCyanAntelope719
Top 5%
• 11 months ago

Another way - which is probably our fist instinct on how this should be solved.

class Solution:
    def decodeString(self, s: str):
        stack = []
        for char in s:
            if char == ']':
                tmp = ''
                while stack and stack[-1] != '[':
                    tmp = stack.pop() + tmp
                stack.pop()  # remove '['
                multiplier = ''
                while stack and stack[-1].isdigit():
                    multiplier = stack.pop() + multiplier
                stack.append(int(multiplier) * tmp)
            else:
                stack.append(char)
        return ''.join(stack)

39

Reply
A
AddedLimeCarp593
Top 1%
• 9 months ago

I find this solution much easier to understand.

5

Reply
Stanley Lin
• 1 month ago

very intuitive and easy to follow.

0

Reply
S
seatoocean
• 3 months ago

this solution was easy for me to grasp the concept.

0

Reply
O
OkVioletAmphibian280
Premium
• 1 month ago

Suggestion : please provide the constraints also, for all the possible variables, here k constraint is important to know

2

Reply
Anas
• 3 months ago

For typescript/Javascript the line where we test if the char is a number should be /\d/.test(char)

2

Reply
Abhay Singh
Top 1%
• 1 year ago

Java Solution:

class Solution {
    public String decodeString(String s) {
        Stack<Pair<String, Integer>> st = new Stack<>();

        StringBuilder cur = new StringBuilder("");

        int i=0;
        while(i < s.length()){
            char ch = s.charAt(i);

            if(Character.isDigit(ch)){
                int cnt = 0;
                while(Character.isDigit(s.charAt(i))){
                    cnt = cnt*10 + s.charAt(i)-'0';
                    i++;
                }
                st.add(new Pair(cur.toString(), cnt));
                cur.setLength(0);
            }else if(Character.isLetter(ch)){
                cur.append(ch);
            }else if(ch == '['){

            }else if(ch == ']'){
                Pair<String, Integer> p = st.pop();
                String prev = p.getKey();
                int k = p.getValue();

                StringBuilder sb = new StringBuilder(prev);
                while(k-- > 0){
                    sb.append(cur);
                }

                cur = sb;
            }

            i++;
        }

        return cur.toString();
    }
}
Show More

2

Reply
C
ControlledWhiteFox228
• 1 month ago

This one is very hard to understand. Why do we multiply the number by 10? Also, 3 is the first character but it's only described in the last step.

1

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

"[": Start of a new sequence

"]": End of a sequence

Digit

Letter

Solution

Complexity Analysis
