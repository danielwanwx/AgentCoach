# Decode Ways

> Source: https://www.hellointerview.com/learn/code/dynamic-programming/decode-ways
> Scraped: 2026-03-30


Your are given a string s containing only digits. Write a function to return the number of ways to decode using the following mapping:

'1' -> "A"
'2' -> "B"
'3' -> "C"
...
'26' -> "Z"

There may be multiple ways to decode a string. For example, "14" can be decoded as "AD" or "N".

Input:

s = 101

Output:

1

Explanation: The only way to decode it is "JA". "01" cannot be decoded into "A" as "1" and "01" are different.

CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def num_decodings(self, s: str) -> int:
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
This solution uses a bottom-up dynamic programming approach to solve the problem. We'll walkthrough how the solution solves the problem when the input string is s = 11106.
We create an integer array dp of length n + 1 where n is the length of the input string s. dp[i] is equal to the number of ways to decode the first i characters of the string s. If the first character of the string is 0, we can return 0 immediately. Otherwise, we initialize dp[0] = 1 (there is one way to decode an empty string) and dp[1] = 1 (one way to decode the first character of s).
VISUALIZATION
Python
Language
Full Screen
def num_decodings(s):
  if not s or s[0] == '0':
    return 0

  n = len(s)
  dp = [0] * (n + 1)
  dp[0], dp[1] = 1, 1

  for i in range(2, n + 1):
    digit = int(s[i - 1])
    if digit != 0:
      dp[i] += dp[i - 1]
        
    digit = int(s[i - 2:i])
    if 10 <= digit <= 26:
      dp[i] += dp[i - 2]

  return dp[n]
1
1
1
0
6
dp
0
1
2
3
4
5

decode ways

0 / 1

1x
We then use a for-loop i which goes from 2 to n to iterate through the string. The body of each loop determines the correct value of dp[i] by looking at the previous two characters of the string.
Single Digit
We first check the ith digit of the string. If it is not equal to 0, then the number of ways we to decode the first i characters of the string is equal to the number of ways to decode the first i - 1 characters of the string (each of those ways and the encoding of the ith digit). This allows us to set dp[i] = dp[i - 1].
VISUALIZATION
Python
Language
Full Screen
def num_decodings(s):
  if not s or s[0] == '0':
    return 0

  n = len(s)
  dp = [0] * (n + 1)
  dp[0], dp[1] = 1, 1

  for i in range(2, n + 1):
    digit = int(s[i - 1])
    if digit != 0:
      dp[i] += dp[i - 1]
        
    digit = int(s[i - 2:i])
    if 10 <= digit <= 26:
      dp[i] += dp[i - 2]

  return dp[n]
i = 2
1
1
1
0
6
1
1
0
0
0
0
dp
0
1
2
3
4
5

i = 2

0 / 2

1x
When it is equal to 0, it's not possible to decode the ith digit alone, so we leave dp[i] as 0 and continue.
VISUALIZATION
Python
Language
Full Screen
def num_decodings(s):
  if not s or s[0] == '0':
    return 0

  n = len(s)
  dp = [0] * (n + 1)
  dp[0], dp[1] = 1, 1

  for i in range(2, n + 1):
    digit = int(s[i - 1])
    if digit != 0:
      dp[i] += dp[i - 1]
        
    digit = int(s[i - 2:i])
    if 10 <= digit <= 26:
      dp[i] += dp[i - 2]

  return dp[n]
i = 4
1
1
1
0
6
digit
1
1
2
3
0
0
dp
0
1
2
3
4
5

digit = 0

0 / 1

1x
Double Digit
Next, we move onto checking the ith and ith - 1 digits together. If they form a number between 10 and 26 (inclusive), then we can decode the ith and ith - 1 digits together. This means we have an additional dp[i - 2] ways to decode the first i characters of the string (each of those ways and the encoding of the ith and ith - 1 digits). This allows us to set dp[i] += dp[i - 2].
VISUALIZATION
Python
Language
Full Screen
def num_decodings(s):
  if not s or s[0] == '0':
    return 0

  n = len(s)
  dp = [0] * (n + 1)
  dp[0], dp[1] = 1, 1

  for i in range(2, n + 1):
    digit = int(s[i - 1])
    if digit != 0:
      dp[i] += dp[i - 1]
        
    digit = int(s[i - 2:i])
    if 10 <= digit <= 26:
      dp[i] += dp[i - 2]

  return dp[n]
i = 2
1
1
1
0
6
digit
1
1
1
0
0
0
dp
0
1
2
3
4
5

digit = 11

0 / 2

1x
Finally, we return dp[n] which is the number of ways to decode the entire string.
Solution
s
​
|
s
string
Try these examples:
Zero
Simple
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def num_decodings(s):
  if not s or s[0] == '0':
    return 0

  n = len(s)
  dp = [0] * (n + 1)
  dp[0], dp[1] = 1, 1

  for i in range(2, n + 1):
    digit = int(s[i - 1])
    if digit != 0:
      dp[i] += dp[i - 1]
        
    digit = int(s[i - 2:i])
    if 10 <= digit <= 26:
      dp[i] += dp[i - 2]

  return dp[n]
1
1
1
0
6
dp
0
1
2
3
4
5

decode ways

0 / 20

1x
What is the time complexity of this solution?
1

O(n³)

2

O(n)

3

O(V + E)

4

O(m * n)

Mark as read

Next: Unique Paths

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

(19)

Comment
Anonymous
​
Sort By
Popular
Sort By
Aadil Sarfani
Premium
• 1 year ago

This can be done in constant space if I'm not mistaken; you only need to remember the number of encodings up to the last two characters.

12

Reply
N
NakedSalmonAntelope132
Premium
• 1 month ago

Constant space solution:

class Solution:
    def num_decodings(self, s: str):
        if not s or s[0] == '0': return 0

        prev, curr = 1, 1

        for i in range(2, len(s) + 1):
            new = 0
            digit = int(s[i - 1])
            if digit != 0:
                new += curr
        
            digit = int(s[i - 2:i])
            if 10 <= digit <= 26:
                new += prev
            
            prev, curr = curr, new
        return curr
Show More

0

Reply
U
UsualMoccasinMacaw440
• 9 months ago

dp[0] = 1 (there is one way to decode an empty string)  -> Why is there one way to decode an empty string given the first mapping is "1"-> "A" ?

5

Reply
U
UsualMoccasinMacaw440
• 9 months ago

In dynamic programming, dp[0] = 1 is used as a base case to represent "one way to decode nothing"—by doing nothing.

1

Reply
Pauras Jadhav
• 5 months ago

Because “doing nothing” counts as one valid way. In combinatorics and in this DP, the empty string represents a fully decoded prefix, so it contributes 1 to the count.

0

Reply
Johan Ospina
Premium
• 4 months ago

Because “doing nothing” counts as one valid way. In combinatorics and in this DP, the empty string represents a fully decoded prefix, so it contributes 1 to the count.

To me this is only part of the intuition you need, for this specific question dp[0] = 0 (or dp[n] = 0 if you iterate backwards) denotes reaching the empty set thus the number of combinations to make from the empty set is exactly 1.

that's a more rigorous explanation.

The final piece of the puzzle is to realize that any transition created from taking 1 or taking 2 characters will get you closer to that empty set state. which means that you're creating a path from the initial question and navigating the sub problems until you get to the empty set. In this question we're counting unique paths from root to leaf so the base case of the empty set is a flag that whatever path we're on is viable. We don't care too much about the unique elements that make up of these paths. just that there are k of them for example.

0

Reply
Abhay Singh
Top 1%
• 1 year ago

Java Solution: Top-Down (recursion)

class Solution {

    public int solve(String s, int idx, int[] memo){
        int n = s.length();

        if(idx == n) return 1;
        if(memo[idx] != -1) return memo[idx];

        if(s.charAt(idx) == '0') return memo[idx] = 0;

        // single
        int cnt = solve(s, idx+1, memo);

        // pair 
        if(idx < n-1){
            int val = (s.charAt(idx)-'0')*10 + (s.charAt(idx+1)-'0');
            if(val <= 26) cnt += solve(s, idx+2, memo);
        }

        return memo[idx] = cnt;
    }

    public int numDecodings(String s) {
        int n = s.length();
        int[] memo = new int[n+1];
        Arrays.fill(memo, -1);

        return solve(s, 0, memo);
    }
}
Show More

3

Reply
M
malinibhandaru
Premium
• 2 months ago

I used your current/prev trick for constant space

1

Reply
RS
Raymond See
• 11 months ago

Typo "botton-up" in the Explanation section.

1

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

Single Digit

Double Digit

Solution
