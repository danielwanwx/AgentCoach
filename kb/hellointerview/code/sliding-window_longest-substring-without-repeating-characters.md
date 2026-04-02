# Longest Substring Without Repeating Characters

> Source: https://www.hellointerview.com/learn/code/sliding-window/longest-substring-without-repeating-characters
> Scraped: 2026-03-30


Sliding Window
Longest Substring Without Repeating Characters
medium
DESCRIPTION (inspired by Leetcode.com)

Write a function to return the length of the longest substring in a provided string s where all characters in the substring are distinct.

Example 1: Input:

s = "eghghhgg"

Output:

3

The longest substring without repeating characters is "egh" with length of 3.

Example 2: Input:

s = "substring"

Output:

8

The answer is "ubstring" with length of 8.

CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def longestSubstringWithoutRepeat(self, s: str) -> int:
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
This solution uses a variable-length sliding window to consider all substrings without repeating characters, and returns the length of the longest one at the end.
We represent the state of the current window with a dictionary state which maps each character to the number of times it appears in the window.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def longestSubstringWithoutRepeat(s):
  state = {}
  max_length = 0
  start = 0

  for end in range(len(s)):
    state[s[end]] = state.get(s[end], 0) + 1
    while state[s[end]] > 1:
      state[s[start]] -= 1
      start += 1

    max_length = max(max_length, end - start + 1)
  return max_length
e
g
h
g
h
h
g
g

longest substring without repeating characters

0 / 1

1x
Initializing Variables
We use a for-loop to increment end to repeatedly expand the window. Each time we expand the window, we first increment the count of s[end] in state. As long as the character at end is not a duplicate character in the window, we can compare the length of the current window to the longest window we've seen so far, and continue expanding. The character at end is a duplicate if state[s[end]] > 1.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def longestSubstringWithoutRepeat(s):
  state = {}
  max_length = 0
  start = 0

  for end in range(len(s)):
    state[s[end]] = state.get(s[end], 0) + 1
    while state[s[end]] > 1:
      state[s[start]] -= 1
      start += 1

    max_length = max(max_length, end - start + 1)
  return max_length
{}
state
e
g
h
g
h
h
g
g
0
max_length

start: 0 | end: -

initialize variables

0 / 7

1x
Expanding window until duplicate `g`
At this point, we have to contract the window because it contains more than one g. We do this by removing the leftmost character (start += 1) from the window, and decrementing its count in state until there is only one g left in the window.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def longestSubstringWithoutRepeat(s):
  state = {}
  max_length = 0
  start = 0

  for end in range(len(s)):
    state[s[end]] = state.get(s[end], 0) + 1
    while state[s[end]] > 1:
      state[s[start]] -= 1
      start += 1

    max_length = max(max_length, end - start + 1)
  return max_length
{e:1, g:2, h:1}
state
e
g
h
g
h
h
g
g
3
max_length

start: 0 | end: 3

expand window

0 / 2

1x
Contracting window until duplicate `g` is removed
At this point, our window is valid again, and we can continue this process of expanding and contracting the window until end reaches the end of the string.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def longestSubstringWithoutRepeat(s):
  state = {}
  max_length = 0
  start = 0

  for end in range(len(s)):
    state[s[end]] = state.get(s[end], 0) + 1
    while state[s[end]] > 1:
      state[s[start]] -= 1
      start += 1

    max_length = max(max_length, end - start + 1)
  return max_length
{h:1, g:1}
state
e
g
h
g
h
h
g
g
3
max_length

start: 2 | end: 3

contract window

0 / 15

1x
Expanding window until end of string
Alternate (Faster) Solution
An slightly more optimized solution represents the state of each window with a dictionary mapping each character to the index at which it last appeared in the window.
Each time we increment end to expand the window, we first check if the character at end is a duplicate by checking if s[end] is in the dictionary. If it is, we can contract the window until it is valid again by setting start to max(start, last_index + 1) where last_index is the previous appearance of s[end]. We use max() to ensure start never moves backward (the previous occurrence might be before the current window). This is faster because we can contract the window in one operation instead of using a while-loop to do it incrementally.
SOLUTION
Python
Language
def longestSubstringWithoutRepeat(s):
    state = {}
    start = 0
    max_length = 0

    for end in range(len(s)):
        if s[end] in state:
            start = max(start, state[s[end]] + 1)

        state[s[end]] = end
        max_length = max(max_length, end - start + 1)
    return max_length
Solution
s
​
|
s
string
Try these examples:
Repeats
Mixed
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def longestSubstringWithoutRepeat(s):
  state = {}
  max_length = 0
  start = 0

  for end in range(len(s)):
    state[s[end]] = state.get(s[end], 0) + 1
    while state[s[end]] > 1:
      state[s[start]] -= 1
      start += 1

    max_length = max(max_length, end - start + 1)
  return max_length
e
g
h
g
h
h
g
g

longest substring without repeating characters

0 / 25

1x

Mark as read

Next: Longest Repeating Character Replacement

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
We don't actually need a map/dictionary - just a set.
class Solution:
    def longestSubstringWithoutRepeat(self, s: str):
        seen = set()
        start = 0
        max_value = 0
        
        for i in range(len(s)):
            element = s[i]
            
            while element in seen:
                r = s[start]
                seen.remove(element)
                start += 1

            seen.add(element)
            max_value = max(max_value, i - start + 1)
        return max_value

37

Reply
MM
Minnie Mouse
Top 5%
• 5 months ago

Looks good but the line seen.remove(element) should be seen.remove(r)!

11

Reply
Joel Wang
Premium
• 1 month ago

My solution below, don't need to adjust the left of window step by step, directly skip to the last_seen + 1

class Solution:
    def longestSubstringWithoutRepeat(self, s: str):
        # Your code goes here
        last_seen = {}
        max_len, left = 0, 0
        
        for right, ch in enumerate(s):
            if ch in last_seen:
                # if the ch last seen is before left, left will move backwards
                left = max(left, last_seen[ch] + 1)
            
            max_len = max(max_len, right - left + 1)
            last_seen[ch] = right
        
        return max_len

2

Reply
Tuan Anh Nguyen
• 2 months ago

An clear solution with comments

class Solution:
    def longestSubstringWithoutRepeat(self, s: str):
        start = 0
        state = set()
        max_ = 0
        for end in range (len(s)):
            # Shirk window until there is no dup characters
            while s[end] in state:
                state.remove(s[start])
                start += 1
            state.add(s[end]) # add char to the state
            max_ = max(max_, end - start + 1) # record the max length of current window
        return max_

1

Reply
Sumanth
Premium
• 2 months ago
• edited 2 months ago

My C# solution:

public class Solution {
    public int LengthOfLongestSubstring(string s) {
        HashSet<char> charSet = new HashSet<char>();
        int longest = 0;
        int start = 0;

        for (int end = 0; end < s.Length; end++) {
            while (charSet.Contains(s[end])) {
                charSet.Remove(s[start]);
                start += 1;
            }

            charSet.Add(s[end]);
            longest = Math.Max(longest, charSet.Count);
        }

        return longest;
    }
}
Show More

1

Reply
S
SensitiveSalmonMeerkat564
• 10 months ago

Without using a dictionary

def longsubstr(str):
	start = 0
	end = 0
	maxlen = 0
	for end in range(1,len(str)):
		if str[end] not in str[start:end]:
			maxlen = max(maxlen, end-start+1)
		else:
			start=end
	return maxlen

1

Reply
Sagnik Pal
• 5 months ago

Existence check in slices or list is O(n),  for strings of the length 10^5 or 10^6 this check can result in O(n^2) complexity in worst case. And we use sliding window to avoid the same. So I feel set or map would be more appropriate.

2

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

Alternate (Faster) Solution

Solution
