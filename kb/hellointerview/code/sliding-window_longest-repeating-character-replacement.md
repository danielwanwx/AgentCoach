# Longest Repeating Character Replacement

> Source: https://www.hellointerview.com/learn/code/sliding-window/longest-repeating-character-replacement
> Scraped: 2026-03-30


Sliding Window
Longest Repeating Character Replacement
medium
DESCRIPTION (inspired by Leetcode.com)

Write a function to find the length of the longest substring containing the same letter in a given string s, after performing at most k operations in which you can choose any character of the string and change it to any other uppercase English letter.

Input:

s = "BBABCCDD"
k = 2

Output:

5

Explanation: Replace the first 'A' and 'C' with 'B' to form "BBBBBCDD". The longest substring with identical letters is "BBBBB", which has a length of 5.

CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
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
In order for a substring to be valid, k + the frequency of the most frequent character in the substring must be greater than or equal to the length of the substring.
For example, if k = 2, and the substring is AABBB, then the most frequent character is B, which shows up 3 times. The substring is valid because 2 + 3 >= 5.
A
A
B
B
B
3
max_freq
k = 2
However, if k = 2 and the substring is AAABBB, then the substring is invalid because 2 + 3 < 6.
A
A
A
B
B
B
3
max_freq
k = 2
We use this fact to solve this problem with a variable-length sliding window to iterate over all valid substrings, and return the longest of those lengths at the end. To represent the state of the current window, we keep track of two variables:
state: A dictionary mapping each character to the number of times it appears in the current window.
max_freq: The maximum number of times a single character has appeared in any window so far.
We start by extending the current window until it becomes invalid (i.e. k + max_freq < window length).
VISUALIZATION
Hide Code
Python
Language
Full Screen
def characterReplacement(s, k):
  state = {}
  max_freq = 0
  max_length = 0
  start = 0

  for end in range(len(s)):
    state[s[end]] = state.get(s[end], 0) + 1
    max_freq = max(max_freq, state[s[end]])

    if k + max_freq < end - start + 1:
      state[s[start]] -= 1
      start += 1

    max_length = max(max_length, end - start + 1)

  return max_length
B
C
B
A
B
C
C
C
C
A

longest repeating character replacement

0 / 12

1x
At this point, the longest substring we have found so far is BCBAB, which has a length of 5 (max_freq = 3 + k = 2).
Now, whenever we try to extend the current window to length 6, it will be invalid unless the character we just included in the window shows up 4 times. So each time we increase the window to length 6, we immediately shrink the window to length 5 until we find a character which shows up 4 times.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def characterReplacement(s, k):
  state = {}
  max_freq = 0
  max_length = 0
  start = 0

  for end in range(len(s)):
    state[s[end]] = state.get(s[end], 0) + 1
    max_freq = max(max_freq, state[s[end]])

    if k + max_freq < end - start + 1:
      state[s[start]] -= 1
      start += 1

    max_length = max(max_length, end - start + 1)

  return max_length
{B:3, C:2, A:1}
state
B
C
B
A
B
C
C
C
C
A
5
max_length

max_count: 3

start: 0 | end: 5

expand window

0 / 9

1x
This continues until we reach the end of the string, at which point we return the length of the longest substring we have found so far.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def characterReplacement(s, k):
  state = {}
  max_freq = 0
  max_length = 0
  start = 0

  for end in range(len(s)):
    state[s[end]] = state.get(s[end], 0) + 1
    max_freq = max(max_freq, state[s[end]])

    if k + max_freq < end - start + 1:
      state[s[start]] -= 1
      start += 1

    max_length = max(max_length, end - start + 1)

  return max_length
{A:1, B:1, C:4}
state
B
C
B
A
B
C
C
C
C
A
5
max_length

max_count: 4

start: 3 | end: 8

expand window

0 / 5

1x
Solution
s
​
|
s
string
k
​
|
k
integer
Try these examples:
Tight
Mixed
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def characterReplacement(s, k):
  state = {}
  max_freq = 0
  max_length = 0
  start = 0

  for end in range(len(s)):
    state[s[end]] = state.get(s[end], 0) + 1
    max_freq = max(max_freq, state[s[end]])

    if k + max_freq < end - start + 1:
      state[s[start]] -= 1
      start += 1

    max_length = max(max_length, end - start + 1)

  return max_length
B
C
B
A
B
C
C
C
C
A

longest repeating character replacement

0 / 26

1x

Mark as read

Next: Intervals Overview

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

(42)

Comment
Anonymous
​
Sort By
Popular
Sort By
C
CalmIndigoPython390
Top 1%
• 2 years ago

Having trouble with the intuition, if the window isn't valid (if k_max_freq < end-start+1), how come we don't check if our max frequency has been reduced? Like what if the character at the start of the window that got removed was part of the max frequency?

36

Reply
C
CalmIndigoPython390
Top 1%
• 2 years ago

Are we assuming that we don't care if the max frequency doesn't go down, because the max length only increases if the max frequency ever goes up? (aka the start doesn't get incremented closer toward the end when max frequency goes up)

5

Reply
Jimmy Zhang
Top 5%
• 2 years ago

"Are we assuming that we don't care if the max frequency doesn't go down, because the max length only increases if the max frequency ever goes up?"  (aka the start doesn't get incremented closer toward the end when max frequency goes up)

yep, exactly! if you want see that in action look at steps 20-21 in the original input.

I agree its not the most intuitive solution because it kind of alternates between a variable length and fixed length windows as it goes, but it sounds like you get it!

6

Reply
W
WorldwidePeachHornet934
• 1 year ago

I am still not able to get the intuition why the max_freq is not changed after moving start :(

4

Reply
H
HolyOlivePike441
• 1 year ago

You can decrement max_freq if you want and it'll only take O(26).

The reason that not updating it works is because we're trying to maximize (end - start + 1) (aka length), while minimizing the (end - start + 1) - max_freq (number of required corrections). So having an overestimated max_freq ends up helping us in saving steps and delays contacting the window.

Imo if this was real prod code, since this behavior is just an unclear coincidence, it's not worth sacrificing readability for such tiny improvement

6

Reply
L
LatinGreenCrayfish104
• 1 year ago

I think instead of if, if you use while, then it's variable length window. In essence, you get back to a "valid" window, each time the validity breaks.

while (k + max_freq < end - start + 1)
  state[s[start]] -= 1
  start += 1

0

Reply
E
eki
Premium
• 8 months ago

You shouldn't use while, because the max_freq is not being updated between iterations.

1

Reply
Haikal Yusuf
Premium
• 4 months ago

you don't have to do a while, because when the right side of the window expands to take 1 new character, you will have to shift the left side (start) of the window by at most 1 character

also this behavior of the sliding window is why it's parked under the "fixed sliding window" variant, not the "variable sliding window"

0

Reply
B
Binary.Beast
Premium
• 15 days ago

Think of a case where the start/left pointer is pointing to either maxFreq character or any other distinct character. In any of these cases, because freq reduced by only 1, as start increments by 1 in next step, maxFreq does not change. Ex: {A:10, B:9, C:4} start pointing to A or B or C, we reduce the freq in map, no need to update maxFreq, as it still remains 9 in this case.

1

Reply
Shalom Deitch
Premium
• 2 months ago

the answer will be (max same letter in run) + min(totalLen, k)
all we need to do is find which of k and totalLength to use

it took me a long time to work that out too

0

Reply
MM
Minnie Mouse
Top 5%
• 5 months ago

How come these problems don't come with time/space complexity analysis?

6

Reply
Abhay Singh
Top 1%
• 1 year ago

Java Solution:

class Solution {

    public int maxFreq(int[] arr) {
        return Arrays.stream(arr).max().orElse(0);
    }

    public int characterReplacement(String s, int k) {
        int n = s.length();

        int[] freq = new int[26];
        Arrays.fill(freq, 0);
        
        int ans = 0;

        int i=0, j=0;

        while(j < n){
            int idx = s.charAt(j) - 'A';
            freq[idx]++;

            int badCharCount = j-i+1 - maxFreq(freq);
            while(i<=j && badCharCount > k){
                idx = s.charAt(i) - 'A';
                freq[idx]--;

                i++;
                badCharCount = j-i+1 - maxFreq(freq);
            }

            ans = Math.max(ans, j-i+1);
            j++;
        }

        return ans;
    }
}
Show More

6

Reply
P
PatientCyanJellyfish520
Premium
• 1 month ago
• edited 1 month ago

I kept the Sliding Window pattern in the back of my head to help with the intuition. Based on the problem, we know that we have to:

Iterate over a data structure
Keep track of our desired state
Find a window that satisfies our desired state

Let’s try it on paper first. Suppose we have the following input:

s = "ABABBA", k = 2

We need to find the longest contiguous substring where k replacements are allowed to make all the characters the same. We begin iterating through the string as the first step.

Now, how do we know which characters need replacing? We need to store the frequency count of the characters in our current window. A set doesn’t really help here, and an array isn’t necessary, so we use a map.

As we iterate, we update the frequency map. At some point, our window might look like this:

A B A B B
map = {A: 2, B: 3}

This represents our current window. Since k = 2, we are allowed to replace up to 2 characters to make all characters in the window the same.

So what does it mean for our state to be invalid?
To make all characters the same, we only need to replace the characters that are not the most frequent one. That means the number of replacements needed is:

current window size - highest frequency character

So our invalid state is:

if (end - start + 1) - highest_frequency > k

If we move on to the next character, the state can become invalid and we may need to move the window:

A B A B B A
map = {A: 3, B: 3}

if (end - start + 1) - highest_frequency > k
=> if 6 - 3 > 2
=> TRUE

At this point, we’ve exceeded the number of allowed replacements, so the window is no longer valid.

How do we slide over and fix the state? We move the start pointer up by one and remove that character from the map, since it no longer represents our current window:

if (end - start + 1) - highest_frequency > k:
    map[s[start]] -= 1
    start += 1

#  A [B A B B A]

This shrinks the window until it becomes valid again.

Relating this back to a Sliding Window template

Here is the generic variable-length Sliding Window template from the Overview (the exact condition varies by problem):

def variable_length_sliding_window(nums):
    state = {}    # map | set | other
    start = 0
    max_ = 0

    for end in range(len(nums)):
        state[nums[end]] = state.get(nums[end], 0) + 1

        # shrink window if state is invalid
        if state is not valid:
            state[nums[start]] -= 1
            start += 1

        # update answer for valid window
        max_ = max(max_, end - start + 1)

    return max_

Final Solution

def characterReplacement(self, s: str, k: int) -> int:
    max_string = 0
    start = 0
    repeated = {}
    maxRepeat = 0

    for end in range(len(s)):
        repeated[s[end]] = repeated.get(s[end], 0) + 1
        maxRepeat = max(maxRepeat, repeated[s[end]])

        if (end - start + 1) - maxRepeat > k:
            repeated[s[start]] -= 1
            start += 1

        max_string = max(max_string, end - start + 1)

    return max_string

Hope this helps!

Show More

5

Reply
S
SwiftIvoryPinniped329
• 1 month ago

amazing

0

Reply
Abhay Singh
Top 1%
• 1 year ago

why are we not modifying "max_freq" while we are reducing count in "state" ?

3

Reply
Anand raj
• 2 months ago

since k is fixed, and we have got one solution which is current max_freq+k then considering any other possibilities with lesser max_freq anyhow won't alter solution so it is kind of eliminating those unnecessary calculations.It will consider only if max_freq is found to be greater than older values

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
