# Word Break

> Source: https://www.hellointerview.com/learn/code/dynamic-programming/word-break
> Scraped: 2026-03-30


You are provided with a string s and a set of words called wordDict. Write a function to determine whether s can be broken down into a sequence of one or more words from wordDict, where each word can appear more than once and there are no spaces in s. If s can be segmented in such a way, return true; otherwise, return false.

Input:

s = "catsandog", wordDict = ["cats","dog","sand","and","cat"]

Output:

false

Explanation: There is no valid segmentation of "catsandog" into dictionary words from wordDict.

Input:

s = "hellointerview", wordDict = ["hello","interview"]

Output:

true

Explanation: Return true because "hellointerview" can be segmented as "hello" and "interview".
Note that you are allowed to reuse a dictionary word.

CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def word_break(self, s: str, wordDict: List[str]) -> bool:
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
This solution uses bottom-up dynamic programming to solve the problem.
We create a boolean array dp of size n + 1 where n is the length of the input string. dp[i] is true if the first i characters of s can be segmented into a valid sequence of dictionary words. dp[0] is True because the empty string is a valid sequence - all other values are false to start.
VISUALIZATION
Python
Language
Full Screen
def wordBreak(s, wordDict):
  wordSet = set(wordDict)
  dp = [False] * (len(s) + 1)
  dp[0] = True # Empty string is a valid break

  for i in range(1, len(s) + 1):
    for j in range(i):
      sub = s[j:i]
      if dp[j] and sub in wordSet:
        dp[i] = True
        break

  return dp[len(s)]
c
a
t
s
a
n
d
o
g
c
a
t
s
a
n
d
o
g
dp
0
1
2
3
4
5
6
7
8
9

word break

0 / 1

1x
We then use a for-loop i which goes from 1 to n to iterate through the string. Inside the body of this loop, we determine the correct value for dp[i]. We do this by using another for-loop j, which goes from 0 to i and represents the start of the substring we are considering. If dp[j] is true and the substring from j to i (sub) is in the dictionary, then we have found a valid segmentation, and can therefore set dp[i] to True.
VISUALIZATION
Python
Language
Full Screen
def wordBreak(s, wordDict):
  wordSet = set(wordDict)
  dp = [False] * (len(s) + 1)
  dp[0] = True # Empty string is a valid break

  for i in range(1, len(s) + 1):
    for j in range(i):
      sub = s[j:i]
      if dp[j] and sub in wordSet:
        dp[i] = True
        break

  return dp[len(s)]
i = 1
c
a
t
s
a
n
d
o
g
c
a
t
s
a
n
d
o
g
T
F
F
F
F
F
F
F
F
F
dp
0
1
2
3
4
5
6
7
8
9

i = 1

0 / 11

1x
Iterating until we set `dp[i] = True` for the first time.
As soon as we find a valid segmentation, we can break out of the inner for-loop and move on to the next character in the string.
Finally, after we finished iterating, we return dp[n] which is the value of the last element in the array. This value will be True if the entire string can be segmented into valid dictionary words, and False otherwise.
What is the time complexity of this solution?
1

O(m * n)

2

O(n!)

3

O(n²)

4

O(n log n)

Solution
s
​
|
s
string
wordDict
​
|
wordDict
list of strings
Try these examples:
Simple
Split
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def wordBreak(s, wordDict):
  wordSet = set(wordDict)
  dp = [False] * (len(s) + 1)
  dp[0] = True # Empty string is a valid break

  for i in range(1, len(s) + 1):
    for j in range(i):
      sub = s[j:i]
      if dp[j] and sub in wordSet:
        dp[i] = True
        break

  return dp[len(s)]
c
a
t
s
a
n
d
o
g
c
a
t
s
a
n
d
o
g
dp
0
1
2
3
4
5
6
7
8
9

word break

0 / 88

1x
Alternative Solution
An alternative solution follows the same bottom-up approach. We use the same for loop to iterate through the string, but instead of iterating over all substrings ending at i, we instead iterate over all words in the dictionary. If the current word matches the substring ending at i and if dp[i - word.length] is True, then we have found a valid segmentation and can set dp[i] to True.
s
​
|
s
string
wordDict
​
|
wordDict
list of strings
Try these examples:
Simple
Split
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def wordBreak(s, wordDict):
  dp = [False] * (len(s) + 1)
  dp[0] = True # Empty string is a valid break

  for i in range(1, len(s) + 1):
    for word in wordDict:
      if i >= len(word) and dp[i - len(word)]:
        sub = s[i - len(word):i]
        if sub == word:
          dp[i] = True
          break

  return dp[len(s)]
c
a
t
s
a
n
d
o
g

word break

0 / 65

1x
What is the time complexity of this solution?
1

O(4ⁿ)

2

O(n!)

3

O(n * m)

4

O(V + E)

Mark as read

Next: Maximum Profit in Job Scheduling

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
Sayan Sarkar
Top 10%
• 6 months ago

Time complexity for the alternative solution is not correct. "s.substring" method itself take "K" time where K is the length of begin and endIndex. So, Time complexity will be O(M * N * K)

11

Reply
U
UniformSalmonAntlion275
• 1 month ago

I believe the alternative solution is better if we are told the dictionary is small but the string is millions of characters long.

1

Reply
Nisal Perera
• 1 year ago

recursive solution

class Solution:
    def word_break(self, s: str, wordDict: list[str]):
        # Your code goes here
        
        s_len = len(s)

        def word_break_helper(i, sub_string):

            if len(sub_string) == 0:
                return True
            elif i == s_len:
                return False

            if sub_string[0:i] in wordDict:
                return word_break_helper(0, sub_string[i:]) or word_break_helper(i + 1, sub_string)
            else:
                return word_break_helper(i + 1, sub_string)

    
        return word_break_helper(0, s)
Show More

1

Reply
kebin gopher
• 1 year ago

A typo in the beginning:

s = "catsanddog", wordDict = ["cats","dog","sand","and","cat"]

It should be "catsandog". O/W, it IS a valid one.

1

Reply
W
WillowyChocolateOcelot938
• 1 year ago

it was correct because it has "catsandog"

0

Reply
R
RealChocolateGrasshopper986
Premium
• 2 months ago

"catsanddog"

Example s = "catsandog" (one 'd') but Explanation says "catsanddog" (two 'd')

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

Alternative Solution
