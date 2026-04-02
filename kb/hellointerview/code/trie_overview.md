# Trie Overview

> Source: https://www.hellointerview.com/learn/code/trie/overview
> Scraped: 2026-03-30


The search operation takes a search term as input and returns whether the term exists in the trie.
We start from the root node and the first character of the search term. We then traverse down the trie by checking if any of the children of the current node match the next character in the search term. If they do, we move to that node and continue the search with the next character in the search term.
The animation below visualizes the search operation for an input (case sensitive) of your choice, with a trie storing APPLE, APP, BAT, BALL, BATS, and BALL.
Try different search terms to get a feel for how the search operation works.
BALL returns true
BA returns false, as BA is not marked as the end of a word
search term
​
|
search term
string
Try these examples:
Found
Missing
Reset
VISUALIZATION
Full Screen
BATH
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

search for BATH

0 / 5

2x
Time Complexity
O(L), where L is the length of the word being searched in the worst case we need to traverse L nodes in the Trie to find the word. Each node traversal takes constant time O(1), for a total of O(L) operations.
Insertion
The insert operation takes a word as input and adds it to the trie.
We traverse the trie until we reach the last character of the search term. From there, we add the nodes that don't exist already in the trie, and mark the last node as the end of a word.
The animation visualizes the insert operation for a word of your choice (case-sensitive) into a trie containing APPLE, APP, BAT, BATS, and BALLET.
The animation resets back to the original trie after each insertion - the trie does not accumulate words as you insert them.
Some example words to insert:
APPLE (already exists)
BALL (no new nodes created, but "L" is marked as the end of a word)
COAL (creates a new branch in the trie from the root)
insert term
​
|
insert term
string
Try these examples:
Short
New Branch
Reset
VISUALIZATION
Full Screen
E
L
P
P
A
S
T
T
E
L
L
A
B

insert BALLOON

0 / 3

2x
Time Complexity
O(L) where L is the length of the word being inserted. In the worst case, such as when the trie is empty or the word being inserted has no common prefixes with existing words, we need to insert L nodes, each of which takes constant time O(1).
Deletion
The delete operation deletes a word from the trie.
We traverse down to the last character of the word we want to delete, set the "end of word" flag to false, and then remove any nodes that are not part of any other words in the trie.
The animation visualizes a delete operation from a trie containing APPLE, APP, BAT, BATS, BALL, and BALLET.
The animation resets back to the original trie after each deletion - meaning the trie does not continuously shrink as you delete words.
Some example words to delete:
BALL (removes the EOW marker from the "L" node)
COAL (does nothing, as the word does not exist in the trie)
BATS (removes the "S" node)
delete term
​
|
delete term
string
Try these examples:
Remove Existing
Missing
Reset
VISUALIZATION
Full Screen
E
L
P
P
A
S
T
T
E
L
L
A
B

delete BALLET

0 / 5

2x
Time Complexity
O(L). In the worst case, such as when the word to delete is the only word in the trie, we need to first traverse L nodes in the trie to find the word to delete, and then delete L nodes. Each node traversal takes constant time O(1), for a total 2L operations, which is O(L).
Summary
Operation	Description	Time Complexity
Search	Search for a word in the trie	O(L)
Insert	Insert a word in the trie	O(L)
Delete	Delete a word from the trie	O(L)
Space Complexity
The space complexity of a trie is O(C), where C is the total number of characters between all the words stored in the trie. This is due to the worst case, which happens when there are no common prefixes between the words stored in the trie.
E
L
P
P
A
D
R
A
O
B
L
A
O
C
A trie in which there are no shared nodes.

Mark as read

Next: Implement Trie Methods

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

(1)

Comment
Anonymous
Randy Tsui
Top 10%
• 11 months ago

The default argument in python is evaluated during function creation and not on every instantiation. This means all future TrieNode() calls will share the same exact dictionary instance.

class TrieNode:
    def __init__(self, children = {}, eow = False):
        self.children = children
        self.is_end_of_word = eow

The recommendation I read from https://docs.python-guide.org/writing/gotchas/ is to do something like the following:

class TrieNode:
    def __init__(self, children = None, eow = False):
        if children is None:
            self.children = {}
        self.is_end_of_word = eow
Show More

36

Reply
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Basics

Trie Class

TrieNodes

Trie Operations

