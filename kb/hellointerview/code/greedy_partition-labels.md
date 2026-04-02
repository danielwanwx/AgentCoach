# Partition Labels

> Source: https://www.hellointerview.com/learn/code/greedy/partition-labels
> Scraped: 2026-03-30


Given a string of lowercase letters, split it into as many segments as possible so that each character appears in exactly one segment. When you concatenate all segments, they should form the original string. Return a list of integers representing the length of each segment.

Example 1

Input:

s = "abacbcdd"

Output:

[6, 2]

Explanation: The character 'a' appears at indices 0 and 2, 'b' at 1 and 4, 'c' at 3 and 5, 'd' at 6 and 7. To keep all occurrences of each character together, we partition into "abacbc" (length 6) and "dd" (length 2).

Example 2

Input:

s = "eccbbbbdec"

Output:

[10]

Explanation: All characters are interleaved such that the entire string must be one segment.

CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def partitionLabels(self, s: str) -> List[int]:
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
Picture a string as a sequence of characters laid out left to right. Our job is to chop it into segments where no character type crosses segment boundaries. Every occurrence of 'a' must be in the same segment, every 'b' in the same segment, and so on.
a
b
a
c
b
c
d
d
0
1
2
3
4
5
6
7
Segment 1 (size 6)
Segment 2 (size 2)
Color = Character Type
'a' appears at 0, 2
'b' appears at 1, 4
'c' appears at 3, 5
'd' appears at 6, 7
Looking at "abacbcdd", we see that 'a' shows up at indices 0 and 2, 'b' at 1 and 4, 'c' at 3 and 5, and 'd' at 6 and 7. The first segment must include at least indices 0 through 5 to capture all 'a', 'b', and 'c' occurrences. Then 'd' forms its own segment.
Observaion
Looking back at the example, we can realize that once we start a segment at some index, we're committed to extending it until we've captured the last occurrence of every character we've encountered. If we see 'a' at index 0 and 'a' also appears at index 2, our segment can't end before index 2.
So here's the greedy approach:
Precompute the last occurrence index for each character
Scan left to right, tracking the farthest "must-reach" index
When our current position equals that farthest index, cut the segment
1. Precompute
Scan string once to
record last index of
each character
2. Track Boundary
For each char, update
end = max(end, lastOf[c])
extending our reach
3. Cut Segment
When i == end,
record segment size
and start new one
Pseudocode
partitionLabels(s)
    lastIndex = map of char -> last occurrence index
    
    for i from 0 to length(s) - 1
        lastIndex[s[i]] = i
    
    result = []
    start = 0
    end = 0
    
    for i from 0 to length(s) - 1
        end = max(end, lastIndex[s[i]])
        
        if i == end
            result.append(i - start + 1)
            start = i + 1
    
    return result
Walkthrough
We'll trace through s = "abacbcdd" to see exactly how segments form.
First, we build our lastIndex map by scanning the string once:
'a' last appears at index 2
'b' last appears at index 4
'c' last appears at index 5
'd' last appears at index 7
Now we scan left to right, tracking start (segment start), end (segment must-reach), and cutting when i == end.
Step 1: Process index 0 (char 'a')
We're at index 0 with character 'a'. Looking up lastIndex['a'], we get 2. This means our segment must extend at least to index 2 to capture all 'a' occurrences.
a
b
a
c
b
c
d
d
0
1
2
3
4
5
6
7
i = 0, char = 'a'
lastIndex['a'] = 2
end = max(0, 2) = 2
i ≠ end, continue
We update end = max(0, 2) = 2. Since i = 0 doesn't equal end = 2, we haven't reached our boundary yet.
Step 2: Process index 1 (char 'b')
At index 1, we see 'b' whose last occurrence is at index 4. This pushes our segment boundary further out.
a
b
a
c
b
c
d
d
0
1
2
3
4
5
6
7
i = 1, char = 'b'
lastIndex['b'] = 4
end = max(2, 4) = 4
i ≠ end, continue
Now end = max(2, 4) = 4. Our segment must reach at least index 4 to include all 'b' occurrences. Still not at the boundary.
Step 3: Process index 2 (char 'a')
Index 2 is another 'a'. We already know 'a''s last index is 2, but our end is already 4, so nothing changes.
a
b
a
c
b
c
d
d
0
1
2
3
4
5
6
7
i = 2, char = 'a'
lastIndex['a'] = 2
end = max(4, 2) = 4
i ≠ end, continue
end = max(4, 2) = 4 stays at 4. We've processed all 'a' characters, but we still need to reach index 4 for 'b'.
Step 4: Process index 3 (char 'c')
Now we see 'c' which last appears at index 5. This extends our segment boundary again!
a
b
a
c
b
c
d
d
0
1
2
3
4
5
6
7
i = 3, char = 'c'
lastIndex['c'] = 5
end = max(4, 5) = 5
i ≠ end, continue
end = max(4, 5) = 5. Our segment now needs to reach index 5. Keep going.
Step 5: Process index 4 (char 'b')
At index 4 we see 'b' again. Its last index is 4, which doesn't push end further.
a
b
a
c
b
c
d
d
0
1
2
3
4
5
6
7
i = 4, char = 'b'
lastIndex['b'] = 4
end = max(5, 4) = 5
i ≠ end, continue
end stays at 5. Almost there!
Step 6: Process index 5 (char 'c') - First Segment Cut!
At index 5 we see 'c', and i == end! Time to cut.
a
b
a
c
b
c
d
d
0
1
2
3
4
5
6
7
Segment 1: size = 6
i = 5, char = 'c'
lastIndex['c'] = 5
end = max(5, 5) = 5
i == end! CUT!
size = 5 - 0 + 1 = 6
start = 6
Since i = 5 equals end = 5, we cut here! The segment size is 5 - 0 + 1 = 6. We record 6 in our result and set start = 6 for the next segment.
Step 7: Process index 6 (char 'd')
New segment begins. We see 'd' which last appears at index 7.
a
b
a
c
b
c
d
d
0
1
2
3
4
5
6
7
i = 6, char = 'd'
lastIndex['d'] = 7
end = max(0, 7) = 7
i ≠ end, continue
end = max(0, 7) = 7. The new segment must reach index 7.
Step 8: Process index 7 (char 'd') - Second Segment Cut!
At index 7 we hit 'd' again, and i == end!
a
b
a
c
b
c
d
d
0
1
2
3
4
5
6
7
Segment 2: size = 2
i = 7, char = 'd'
lastIndex['d'] = 7
end = max(7, 7) = 7
i == end! CUT!
size = 7 - 6 + 1 = 2
Segment size is 7 - 6 + 1 = 2. We're done!
Result: [6, 2]
The string "abacbcdd" is partitioned into two segments of sizes 6 and 2. Each character appears in exactly one segment.
Solution
The algorithm scans the string twice: once to build the last-occurrence map, then once to greedily cut segments whenever we've captured all necessary characters.
s
​
|
s
string
Try these examples:
Unique
Repeated
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def partitionLabels(s):
    last_index = {}
    for i, c in enumerate(s):
        last_index[c] = i
    
    result = []
    start = 0
    end = 0
    
    for i, c in enumerate(s):
        end = max(end, last_index[c])
        
        if i == end:
            result.append(i - start + 1)
            start = i + 1
    
    return result
a
0
b
1
a
2
c
3
b
4
c
5
d
6
d
7

Partitioning "abacbcdd" into segments

0 / 27

1x
Greedy partition with last-occurrence tracking
What is the time complexity of this solution?
1

O(4ⁿ)

2

O(n)

3

O(n * logn)

4

O(x * y)

When to Use This Pattern
This "track the farthest boundary" technique applies whenever you need to:
Partition data where certain elements must stay together
Find minimal groupings that satisfy containment constraints
Merge overlapping intervals conceptually
The core idea is that each element "forces" the boundary to extend to its last occurrence, and you cut only when you've satisfied all pending constraints.

Mark as read

Next: Trie Overview

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

(2)

Comment
Anonymous
Satya Dasara
Premium
• 2 months ago
• edited 2 months ago

I tried to solve this problem on my own without looking at the solution. It felt like merging overlapping intervals problem where each alphabet has a start and end as it's boundary interval. All overlapping boundaries can be merged into one boundary and their length can be calculated.

class Solution:
    def partitionLabels(self, s: str):
        alphabets = set(s)
        start_map = {}
        end_map = {}

        for idx, c in enumerate(s):
            if c not in start_map:
                start_map[c] = idx
            end_map[c] = idx

        boundaries = [[start_map[alphabet], end_map[alphabet]] for alphabet in alphabets]

        boundaries.sort(key = lambda boundary: boundary[0])

        merged = [boundaries[0]]

        for boundary in boundaries[1:]:
            if merged[-1][1] > boundary[0]:
                merged[-1][1] = max(boundary[1], merged[-1][1])
            else:
                merged.append(boundary)
        
        print(merged)

        return [x[1] - x[0] + 1 for x in merged]

The greedy solution is obviously less verbose and easy once you understand it

class Solution:
    def partitionLabels(self, s: str):
        end_map = {}

        for i, c in enumerate(s):
            end_map[c] = i

        res = []
        start = 0
        end = 0

        for i, c in enumerate(s):
            end = max(end, end_map[c])

            if i == end:
                res.append(end - start + 1)
                start = i + 1
                end = i + 1

        return res 
Show More

3

Reply
fz zy
Premium
• 1 month ago
class Solution:
    def partitionLabels(self, s: str):
        offset = [-1] * 26
        for i, c in enumerate(s):
            offset[ord(c) - 97] = i
        cut = -1
        start = 0
        ans = []
        for i, c in enumerate(s):
            idx = ord(c) - 97
            if i > cut:
                start = i
                cut = offset[idx]
                ans.append(i - start + 1)
                continue
            cut = max(cut, offset[idx])
            ans[-1] = cut - start + 1
        return ans

0

Reply
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Building Intuition

Observaion

Pseudocode

Walkthrough

Solution

When to Use This Pattern
