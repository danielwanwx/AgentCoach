# Palindrome Partitioning

> Source: https://www.hellointerview.com/learn/code/backtracking/palindrome-partitioning
> Scraped: 2026-03-30


Given a string s, split it into segments where each segment is a palindrome (reads the same forwards and backwards).

Return all possible ways to partition the string into palindromic segments.

Constraints:

1 <= s.length <= 16
s contains only lowercase English letters

Example 1:

Input:

s = "noon"

Output:

[["n","o","o","n"], ["n","oo","n"], ["noon"]]

Explanation:

["n","o","o","n"] - All single characters are palindromes
["n","oo","n"] - "oo" is a palindrome in the middle
["noon"] - The entire word is a palindrome

Example 2:

Input:

s = "civic"

Output:

[["c","i","v","i","c"], ["c","ivi","c"], ["civic"]]
CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def partition(self, s: str) -> List[List[str]]:
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

Building Intuition
Given a word like "noon", we want to find every possible way to split it into segments where each segment is a palindrome.
Input: "noon"
n
o
o
n
["n","o","o","n"]
All single chars
["n","oo","n"]
"oo" is a palindrome
["noon"]
Entire word is palindrome
Every single character is automatically a palindrome. So one valid partition is always splitting into individual characters. But we can also group consecutive characters together if they form a palindrome.
Finding All Partitions
The problem asks us to find all possible partitions, not just one. We can't just greedily take the longest palindrome at each step; we need to explore every valid way to split the string.
Think of partitioning as making cuts. At each position start, you're choosing where to end your next segment. You pick an end index and commit to the segment s[start..end]. The only rule? That segment must be a palindrome.
Where to make the first cut in "noon"?
n
o
o
n
"n" ✓
"no" ✗
"noo" ✗
"noon" ✓
For the string "noon":
Cut after index 0 → segment "n" (palindrome ✓) → recurse on "oon"
Cut after index 1 → segment "no" (not palindrome ✗) → skip
Cut after index 2 → segment "noo" (not palindrome ✗) → skip
Cut after index 3 → segment "noon" (palindrome ✓) → recurse on ""
Once you frame it this way, the recursion becomes simple: from position start, try every possible end. If s[start..end] is a palindrome, add it to your current path and recurse from end + 1. When start == n, you've reached the end, so record the path.
This is backtracking: make a choice (commit to a palindrome segment), explore what follows, then undo that choice and try a different cut.
The Solution-Space Tree
Each partitioning problem can be visualized as a tree. Each node represents a recursive call with a particular start position. From each node, we branch out to try different ending positions. Each branch represents "take s[start..end] as the next segment."
Here's the complete solution-space tree for "noon":
start=0
"n"
"no"
"noo"
"noon"
✓ ["noon"]
"o"
"oo"
"oon"
"o"
"on"
"n"
✓ ["n","oo","n"]
"n"
✓ ["n","o","o","n"]
✗
✗
✗
✗
Starting position
Valid palindrome (exploring)
Complete partition found
Not a palindrome (pruned)
The tree shows a glimpse of how backtracking works, notice how "no", "noo", "oon", and "on" all get pruned because they're not palindromes. We end up with 3 valid partitions: ["n","o","o","n"], ["n","oo","n"], and ["noon"].
Let's understand this below thoroughly.
The Algorithm
The algorithm follows directly from the tree structure. Each node represents a recursive call at position start. For each call, we try all possible cuts:
1. Try All Cuts
For each end from
start to n-1, check if
s[start..end] is valid
2. Commit & Recurse
If palindrome, add
segment to path and
recurse from end+1
3. Base Case
When start == n,
we've partitioned
everything → save it!
4. Backtrack
Pop last segment
and try a longer
cut position
Checking for Palindromes
A string is a palindrome if it reads the same forwards and backwards. We can check this by comparing characters from both ends moving inward:
isPalindrome(s, left, right)
    while left < right
        if s[left] != s[right]
            return false
        left = left + 1
        right = right - 1
    return true
Here's the complete algorithm:
partition(s)
    result = []
    path = []
    backtrack(s, 0, path, result)
    return result

backtrack(s, start, path, result)
    if start == length(s)           // reached the end, valid partition!
        result.add(copy of path)
        return
    
    for end from start to length(s) - 1     // try all cut positions
        if isPalindrome(s, start, end)      // only proceed if segment is palindrome
            path.add(s[start..end])         // commit to this cut
            backtrack(s, end + 1, path, result)  // recurse from end+1
            path.removeLast()               // undo the cut (backtrack)
The loop for end from start to length(s) - 1 tries every possible cut position. If s[start..end] is a palindrome, we commit to that segment (add it to path), then recurse to partition the remainder starting at end + 1. When we return, we undo the choice and try the next cut position.
Step-by-Step Walkthrough
Let's trace through s = "noon" step by step, watching how we traverse the solution-space tree. This is essentially a depth-first traversal of the tree we discussed above.
Here's the complete tree for reference (same as above, showing all branches):
∅
"n"
"no"
"noo"
"noon"
["noon"]
"o"
"oo"
"oon"
"o"
"on"
"n"
["n","oo","n"]
"n"
["n","o","o","n"]
Now let's walk through the DFS traversal:
Step 1: Start with "n"
Starting at root, we try the first cut: take "n". It's a single character (always a palindrome), so we recurse.
∅
"n"
"no"
"noo"
"noon"
"o"
"oo"
"oon"
"o"
"on"
"n"
"n"
path = ["n"], checking remaining "oon"
Step 2: Continue with "o", then another "o"
Following the DFS, we take "o" (palindrome), then another "o" (palindrome).
∅
"n"
"no"
"noo"
"noon"
"o"
"oo"
"oon"
"o"
"on"
"n"
"n"
path = ["n","o","o"], checking remaining "n"
Step 3: Take "n" — found first partition!
Taking "n" completes the path. Now start = 4, which equals length("noon"). We've found our first complete partition!
∅
"n"
"no"
"noo"
"noon"
"o"
"oo"
"oon"
"o"
"on"
"n"
"n"
🎉 Found: ["n","o","o","n"]
Step 4: Backtrack, try "oo" — found second partition!
We backtrack and try "oo" instead of "o". It's a palindrome (reads same forwards and backwards)! Then we take "n" and find another complete partition.
∅
"n"
"no"
"noo"
"noon"
"o"
"oo"
"oon"
"o"
"on"
"n"
"n"
🎉 Found: ["n","oo","n"]
Step 5: Backtrack to root, try "noon" — found third partition!
We backtrack all the way to the root and try "noon". The entire string is a palindrome! This gives us our third complete partition.
∅
"n"
"no"
"noo"
"noon"
"o"
"oo"
"oon"
"o"
"on"
"n"
"n"
🎉 Found: ["noon"]
Final Result
The complete traversal found 3 valid partitions:
∅
"n"
"no"
"noo"
"noon"
["noon"]
"o"
"oo"
"oon"
"o"
"on"
"n"
["n","oo","n"]
"n"
["n","o","o","n"]
Found partition
Pruned (not palindrome)
Solution
The backtracking algorithm systematically explores all possible ways to partition the string. At each position, we try every possible palindromic prefix and recursively solve for the remainder.
s
​
|
s
string
Try these examples:
Civic
Palindrome
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def partition(s):
    result = []
    current = []
    
    def backtrack(start):
        if start == len(s):
            result.append(current[:])
            return
        for end in range(start, len(s)):
            if is_palindrome(s, start, end):
                current.append(s[start:end+1])
                backtrack(end + 1)
                current.pop()
    
    backtrack(0)
    return result
Input: "noon"
"n"
"o"
"on"
"o"
"n"
"oo"
"oon"
"n"
"no"
"noo"
"noon"
∅
Checking "n"...
path: []
exploring
found
pruned

palindrome partitioning

0 / 47

1x
Recursion tree for palindrome partitioning — watch how we explore branches and prune invalid paths
What is the time complexity of this solution?
1

O(n!)

2

O(m * n * 4^L)

3

O(n × 2^n)

4

O(n * logn)

Optimization: Precompute Palindromes
We can avoid redundant palindrome checks by precomputing a 2D table where dp[i][j] tells us whether s[i..j] is a palindrome. This uses dynamic programming:
Single characters: dp[i][i] = true
Two characters: dp[i][i+1] = (s[i] == s[i+1])
Longer: dp[i][j] = (s[i] == s[j]) && dp[i+1][j-1]
This changes each palindrome check from O(n) to O(1), but the overall complexity remains because we still need to enumerate all partitions.
This backtracking pattern applies whenever you need to find all ways to split or partition something with constraints. Similar problems include:
Word Break II (partition into dictionary words)
Restore IP Addresses (partition into valid IP segments)
Expression Add Operators (partition with operators)

Mark as read

Next: N-Queens

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

(3)

Comment
Anonymous
R
RoundHarlequinWolverine735
Premium
• 4 days ago

This seems too tricky to visualize after looking at the solution visualization also

0

Reply
N
NursingSalmonSheep993
Premium
• 8 days ago

Nicely written article!

0

Reply
fz zy
Premium
• 1 month ago
import copy

class Solution:
    def partition(self, s: str):
        n = len(s)
        ans = []
        curr = []
        dp = [[False for _ in range(n)] for _ in range(n)]
        def dfs(i):
            if i == n:
                ans.append(copy.copy(curr))
                return
            for j in range(i, n):
                if s[i] == s[j] and (j - i <= 2 or dp[i + 1][j - 1]):
                    dp[i][j] = True
                    curr.append(s[i:j + 1])
                    dfs(j + 1)
                    curr.pop()
        dfs(0)
        return ans
Show More

0

Reply
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Building Intuition

Finding All Partitions

The Solution-Space Tree

The Algorithm

Checking for Palindromes

Step-by-Step Walkthrough

Solution

Optimization: Precompute Palindromes
