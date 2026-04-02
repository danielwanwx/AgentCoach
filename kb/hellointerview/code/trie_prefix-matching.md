# Prefix Matching

> Source: https://www.hellointerview.com/learn/code/trie/prefix-matching
> Scraped: 2026-03-30


match(prefix) returns a list of all words in the Trie that start with the given prefix. The words can be in any order.

The creation of the Trie is already implemented for you.

The test cases include two parameters:

words: a list of words to add to the Trie,
prefix: a prefix to search for.

The test cases will create the Trie with the initial words, and then run the match command, and compare the output to the expected output.

Example 1:

Input:

initialWords = ["apple", "app", "apartment", "ap", "apricot"]
prefix = "app"

Output: ["apple", "app"]

Example 2:

Input:

initialWords = ["ball", "bath", "bat", "batter"]
prefix = "bat"

Output: ["bat", "bath", "batter"]

CODE EDITOR
Python
​
Full Screen
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
class TrieNode:
    def __init__(self):
        self.children = {}
        self.isEndOfWord = False
class Solution:
    def create_trie(self, words):
        # === DO NOT MODIFY ===
        self.root = TrieNode()
        for word in words:
            self.insert(word)
    def insert(self, word):
        # === DO NOT MODIFY ===
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.isEndOfWord = True
    
    def prefix(self, word):
        """
        Return a list of all words in the trie that start with the given 
        prefix.
        """
        # === YOUR CODE HERE ===
        return []
    def trie(self, words, prefix):
        # === DO NOT MODIFY ===
        self.create_trie(words)
        return self.prefix(prefix)
Results

AI Feedback

Past Submissions

Reset
View Answer
Run

Run your code to see results here

Have suggestions or found something wrong?

Explanation
We need to use the Trie to find all words that have a given prefix. The intuition is to search for the prefix in the trie and then perform depth-first search to find all words that have the given prefix.
The animation below visualizes what that looks like:
Prefix: BA
E
L
P
P
A
S
T
L
L
A
B
result
[]
Step 1: Search For The Prefix
The first step is to search for the prefix in the trie. We start from the root node and traverse down the trie to find the node that corresponds to the prefix. If the prefix does not exist in the trie, we return an empty list. We stop at the node that corresponds to the prefix.
SOLUTION
Python
Language
def prefix(self, word):
    """
    Return a list of all words in the trie
    that start with the given prefix.
    """
    node = self.root
    for char in word:
        if char not in node.children:
            return []  # Prefix not found in trie
        node = node.children[char]
Step 2: Perform Depth-First Search
After finding the node that corresponds to the prefix, we perform a depth-first search to find all words that have the given prefix.
We can introduce a helper function dfs that takes the current node and the current word as arguments. Each call to dfs will explore the children of the current node and append the characters to the current word. When we reach the end of a word, we add the current word to the result list, which we will return at the end.
SOLUTION
Python
Language
def prefix(self, word):
        """
        Return a list of all words in the trie that start with the given prefix.
        """
        node = self.root
        for char in word:
            if char not in node.children:
                return []  # Prefix not found in trie
            node = node.children[char]
        
        # Now perform DFS to collect all words
        result = []
        
        def dfs(current_node, current_word):
            if current_node.isEndOfWord:
                result.append(current_word)
            
            for char, child_node in current_node.children.items():
                dfs(child_node, current_word + char)
        
        dfs(node, word)
        return result
What is the time complexity of this solution?
1

O(2ⁿ)

2

O(4ⁿ)

3

O(N + M)

4

O(N + Q)

If N is the length of the prefix and M is the number of characters in the words that match the prefix, the space complexity is O(x * N + M) for the output list, where x is the number of words that match the prefix.
The exact calculation of this space complexity is not as important as understanding why the output list dominates the space complexity.

Mark as read

Next: Prefix Sum Overview

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

(5)

Comment
Anonymous
S
Suraj
Top 5%
• 11 months ago

Can you please post the corresponding Leetcode problem link ? Folks, who work on non-Python languages will find it useful.

6

Reply
S
StatutoryOrangeGuppy644
Top 10%
• 6 months ago

Leetcode link: https://leetcode.com/problems/counting-words-with-a-given-prefix/

5

Reply
S
selectfromall
Top 5%
• 1 year ago

Bug: Animation results say [BATS, BALL] but it should be [BAT, BATS, BALL]

3

Reply
Hieronim Kubica
Premium
• 7 months ago

Is the complexity really O(N+M)? With each recursive call do dfs creating a new string, isn't it rather O(N + M^2)?

2

Reply
yaotong cheng
Premium
• 5 months ago

dfs(child_node, current_word + char) the string concatenation will cost extra time right? To have a real
O(N + M) time complexity, I think using a list in the dfs helper func would be better

1

Reply
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

Step 1: Search for the Prefix

Step 2: Perform Depth-First Search
