# Minimum Window Subsequence

> Source: https://www.hellointerview.com/learn/code/dynamic-programming/minimum-window-subsequence
> Scraped: 2026-03-30


Given a source string s1 and a pattern string s2, find the shortest contiguous portion of s1 that contains s2 as a subsequence.

Return the shortest such substring. If no valid substring exists, return an empty string.

When multiple substrings of equal minimum length exist, return the one that appears first (leftmost).

Reminder: A subsequence maintains the relative order of characters but doesn't require them to be consecutive.

Example 1

Input:

s1 = "hellointerview"
s2 = "her"

Output:

"hellointer"

Explanation: We need 'h' → 'e' → 'r' in order. The shortest window containing this subsequence starts at 'h' (index 0), includes 'e' (index 1), and ends at 'r' (index 9), giving us "hellointer".

Example 2

Input:

s1 = "codingisfun"
s2 = "xyz"

Output:

""

Explanation: None of the characters 'x', 'y', or 'z' appear in s1, so no valid subsequence window exists.

CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def min_window(self, s1: str, s2: str) -> str:
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
Building Intuition
We need to find the shortest substring of s1 that contains s2 as a subsequence. What's the difference?
Substring
(consecutive characters)
a
b
c
d
e
"bcd" is substring of "abcde"
Subsequence
(same order, gaps allowed)
a
b
c
d
e
f
"bdf" is subsequence of "abcdef"
Our goal: find the shortest window in s1 that contains s2 as a subsequence.
s1 =
a
b
c
d
e
b
d
d
e
window: "bcde" (length 4)
s2 =
b
d
e
(find this as subsequence in shortest window)
Find the shortest substring of s1 containing s2 as a subsequence
Starting Simple: The Brute Force Approach
The most straightforward approach? Try every possible substring of s1 and check if s2 is a subsequence of it.
brute_force(s1, s2)
    for each starting position i in s1
        for each ending position j >= i
            if s2 is subsequence of s1[i:j+1]
                track if this is the shortest so far
    return shortest window
This works, but it's painfully slow. We're checking O(m²) substrings, and each subsequence check takes O(window length) time. Since windows can be up to length m, that's O(m³) total - way too slow for large inputs.
A Smarter Approach: Forward Then Backward
A better approach would be, instead of checking random substrings, what if we:
Find where s2 ends - Scan forward through s1, matching characters of s2 one by one until we've matched all of s2
Shrink from the start - Once we've found a complete match ending at position i, walk backwards to find where this particular match started
This is more efficient because we're not checking unnecessary substrings. But there's still room for improvement - we might re-scan the same portions of s1 multiple times.
The Key Observation
Think about what information we actually need. When we're at position i in s1 and we find a character that matches s2[j]:
If this is the first character of s2 (j=0), we're starting a new potential window right here at position i
If this is a later character of s2 (j>0), we need to know: "Where did the window that matched s2[0..j-1] start?"
That second point is crucial. We don't need to re-scan backwards - we just need to remember where each partial match started.
Why Dynamic Programming?
This is exactly what DP is good for: remembering previous computations to avoid redoing work.
Let's define: dp[j] = the starting index in s1 from which we can form s2[0..j] ending at our current position.
s2 =
b
d
e
dp =
1
1
1
dp[0]
dp[1]
dp[2]
dp[j] = start index where we can form
s2[0..j] ending at current position
Example: dp = [1, 1, 1]
→ All of "bde" matched starting from
index 1 in s1
When we find s1[i] == s2[j]:
Case 1: j == 0
(first char of s2)
dp[0] = i
Start new window here
Case 2: j > 0
(later char of s2)
dp[j] = dp[j-1]
Inherit start from previous match
When dp[n-1] becomes valid (not -1), we've found a complete subsequence! The window goes from dp[n-1] to our current position i.
The DP array stores starting indices, not counts or boolean values. This lets us immediately compute the window length when we find a complete match.
Why Iterate Backwards Through s2?
We iterate j from n-1 down to 0 (backwards) because each dp[j] depends on dp[j-1]. If we iterated forwards, we'd overwrite dp[j-1] before using it for dp[j].
Walkthrough
Let's trace through s1 = "abcdebdde", s2 = "bde":
Initial state: dp = [-1, -1, -1] (all -1 means no matches found yet)
Step 1: At position i=1, we find 'b'
We're scanning through s1 and encounter the character 'b' at index 1. This matches the first character of s2 (which is s2[0] = 'b'). Since this is the start of a potential subsequence match, we record where this match begins by setting dp[0] = 1.
a
b
c
d
e
...
dp = [
1
, -1, -1]
← new window starts at index 1
Step 2: At position i=3, we find 'd'
Continuing our scan, we reach index 3 where s1[3] = 'd'. This matches s2[1] = 'd', the second character in our target. Since we already have a partial match for the first character (stored in dp[0] = 1), we now set dp[1] = dp[0] = 1. This means "the window that matches the first two characters of s2 ('bd') starts at index 1".
a
b
c
d
e
...
dp = [1,
1
, -1]
← inherits start from dp[0]
Step 3: At position i=4, we complete the first match!
We hit index 4 where s1[4] = 'e'. This matches the final character s2[2] = 'e'. Now dp[2] = dp[1] = 1, meaning we've found a complete match for all of "bde" starting at index 1. The window spans from index 1 to index 4: s1[1:5] = "bcde" with length 4. We save this as our current best answer.
a
b
c
d
e
...
dp = [1, 1,
1
]
✓ Complete! "bcde" (len=4)
Step 4: Continuing the scan, we find another match
The algorithm doesn't stop at the first match - it keeps scanning to see if there's a shorter window. At index 5, we find another 'b', starting a new potential match. Eventually at index 8, we complete another match: s1[5:9] = "bdde" with length 4. Since this is the same length as our first match and we already have one, we stick with "bcde".
a
b
c
d
e
b
d
d
e
dp = [5, 5, 5]
"bdde" (len=4, same as before)

Final Answer: "bcde" (length 4)

Both windows have the same length, so we return the first one we found

Visualization
s1
s1
s2
s2
VISUALIZATION
Hide Code
Python
Language
Full Screen
def min_window(s1, s2):
    m, n = len(s1), len(s2)
    dp = [-1] * n
    result = ""
    min_len = float('inf')
    
    for i in range(m):
        for j in range(n - 1, -1, -1):
            if s1[i] == s2[j]:
                if j == 0:
                    dp[j] = i
                else:
                    dp[j] = dp[j - 1]
            
        if dp[n - 1] != -1:
            start = dp[n - 1]
            length = i - start + 1
            if length < min_len:
                min_len = length
                result = s1[start:i + 1]
    
    return result
s1
a
0
b
1
c
2
d
3
e
4
b
5
d
6
d
7
e
8
s2
b
0
d
1
e
2
dp
-1
-1
-1

Finding the shortest substring containing s2 as a subsequence

0 / 50

1x
DP solution tracking start indices
Solution
The solution iterates through s1 once. For each character, we check all positions in s2 (in reverse order) to update our DP array. Whenever the last entry dp[n-1] becomes valid, we've found a complete subsequence and can check if it's the shortest so far.
What is the time complexity of this solution?
1

O(4^L)

2

O(n * logn)

3

O(m * n)

4

O(2ⁿ)

Alternative Approaches
Two Pointers with Expansion: Find each occurrence of s2 as a subsequence, then try to shrink from the left. Same time complexity but with higher constants.
2D DP: Use dp[i][j] to track starting positions for each (i, j) pair. Uses O(m * n) space but might be conceptually clearer for some.
The 1D DP approach we use is space-optimal while maintaining the same time complexity.

Mark as read

Next: Greedy Algorithms Overview

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

(9)

Comment
Anonymous
fz zy
Premium
• 2 months ago
class Solution:
    def min_window(self, s1: str, s2: str):
        dp = [-1] * (len(s2) + 1)
        leftMost = -1
        minLen = len(s1) + 1
        for i in range(len(s1)):
            prev = i
            for j in range(len(s2)):
                tmp = dp[j]
                if s1[i] == s2[j]:
                    dp[j] = max(dp[j], prev)
                prev = tmp
            if dp[-2] != -1 and minLen > i - dp[-2] + 1:
                minLen = i - dp[-2] + 1
                leftMost = dp[-2]
        return "" if leftMost == -1 else s1[leftMost:leftMost+minLen]

1

Reply
S
SamR
Premium
• 4 days ago

Why Iterate Backwards Through s2?

We iterate j from n-1 down to 0 (backwards) because each dp[j] depends on dp[j-1]. If we iterated forwards, we'd overwrite dp[j-1] before using it for dp[j].

It works fine if we iterate forwards through s2:

class Solution:
def min_window(self, s1: str, s2: str) -> str:
min_length = float("inf")
min_len_sub = ""

    dp = [-1] * len(s2)

    for i in range(len(s1)):
        for j in range(len(s2)):
            if s1[i] == s2[j]:
                if j == 0:
                    dp[j] = i
                else:
                    dp[j] = dp[j - 1]
        
        if dp[-1] != -1:
            sub_len = i - dp[-1] + 1
            if sub_len < min_length:
                min_length = sub_len
                min_len_sub = s1[dp[-1]:i+1]

    return min_len_sub

Show More

0

Reply
Akash Solanki
Premium
• 28 days ago

For some reason, the code editor doesn't allow me to write the code!! Is anyone else facing this?

0

Reply

Shivam Chauhan

Admin
• 28 days ago

Hey Akash, not able to repro this. Can you provide more info like your browser info, etc. Thanks!

0

Reply
Akash Solanki
Premium
• 28 days ago

Thanks for replying this quickly, you guys are amazing!

This was probably because I was using my office network. It seems to be working when I'm on my home network.

1

Reply

Comments specific to prior versions of this article

Michał Rybiński
• 2 months ago

Hey, test 2 and 3 are wrong, even your answer fails on them.

1

Reply
M
MathematicalBlackPenguin921
Premium
• 3 months ago

O(m × n) vs O(m × n)

What is the difference between these time complexities?

1

Reply
Expand Old Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

Building Intuition

Starting Simple: The Brute Force Approach

A Smarter Approach: Forward Then Backward

The Key Observation

Why Dynamic Programming?

Why Iterate Backwards Through s2?

Walkthrough

Visualization

Solution

Alternative Approaches
