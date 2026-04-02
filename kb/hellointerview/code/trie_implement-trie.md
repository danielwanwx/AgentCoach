# Implement Trie Methods

> Source: https://www.hellointerview.com/learn/code/trie/implement-trie
> Scraped: 2026-03-30



Insert
The intiution for searching is to search for each character in the word by traversing down nodes in the trie. When we reach the end of the word, we check if that node is marked as the end of a word. This is necessary
SOLUTION
Python
Language
def search(self, word):
    """
    Search the trie for the given word.

    Returns True if the word exists in the trie, False otherwise
    """
    # start from the root node
    node = self.root
    
    for char in word:
        if char not in node.children:
            return False
        node = node.children[char]
    
    return node.is_end
Delete
Intuition
To delete a word from a trie, we need to first unmark the node corresponding to the last character of the word as the end of a word.
The Trie below contains BAT and BATH. To delete BAT, we need to unmark T as the end of a word.
H
T
A
B
H
T
A
B
Then, we need to delete all nodes from that word that are not part of any other words in the trie.
For example, the Trie below contains two words: "BALLET" and "BALLOON". If we were to delete "BALLET", we can safely delete "E" and "T", but not "BALL" because it is part of "BALLOON".
T
E
N
O
O
L
L
A
B
If we look closer at the nodes we can delete, they have two properties in common:
They are not the end of any word
They don't have any children
So we want to first traverse down to the node corresponding to the last character of the word we are trying to delete and unmark it as the end of a word. From there, we can traverse back "up" by deleting nodes that are not part of any other words based on the two conditions above.
Implementation
The above logic is best implemented recursively with a helper function _delete. Each call to _delete returns a boolean indicating whether the current node can be deleted from its' parent's dictionary of children.
It returns True if:
The current node is not the end of any word (not node.isEndOfWord) AND
The current node has no children (len(node.children) == 0)
Base Case
The base case for the recursive function is when we reach the end of the word. We need to set node.isEndOfWord = False to ensure that we removed the given word from the trie.
At this point, we can start deleting nodes that are not part of any other words. Each node returns True if it should be deleted from its parent's dictionary of children based on the two conditions above.
The parent receives that boolean and:
If the boolean is True, it deletes the child node from its dictionary of children. The parent node then returns if it should be deleted as well.
If the boolean is False, it does not delete the child node and returns False, which prevents any further deletions.
SOLUTION
Python
Language
def delete(self, word):
    """
    Deletes the given the word from the Trie.

    Returns None.
    """
    def _delete(node, index):
        # base case: We have reached the end of the word
        if index == len(word):
            # Mark the node as not being the end of a word
            node.is_end = False
            # Return True if the node should be deleted
            return len(node.children) == 0
        
        char = word[index]
        child = node.children.get(char)
        
        if child is None:
            return False  # Word not found
        
        should_delete_child = _delete(child, index + 1)
        
        if should_delete_child:
            del node.children[char]
        
        # Return True if current node should be deleted
        return not node.is_end and len(node.children) == 0
    
    _delete(self.root, 0)

Mark as read

Next: Prefix Matching

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

(12)

Comment
Anonymous
​
Sort By
Popular
Sort By
Z
ZerothPurpleMarten917
Top 10%
• 1 year ago

Just a small feedback: I spent a lot of time trying to understand the delete function. It would have been better with visualization/ animation of the internal working.

30

Reply
S
selectfromall
Top 5%
• 1 year ago

Test case #1 is a flawed test case IMO. The article implies you can only delete words that exist, but here it shows you can delete words that don't exist.

initialWords: [apple,app,apartment]
commands: [[search,apple],[search,apartment],[search,appl],[delete,appl],[search,apple]]
expected: [true,true,false,false]

When we send a command to delete "appl", that should exit the method early, since "appl" is not a legit word. Then, when we send a command to search for "apple" we should expect "true", since it is a legit word and have not been deleted yet.

8

Reply
Richard
Premium
• 1 year ago

Agreed

2

Reply
M
MaleGreenCatfish294
Premium
• 1 month ago

We can have an explicit stack too, to eliminate the complications of recursive delete.

2

Reply
P
ParallelBrownHawk162
Premium
• 7 months ago

Selecting Ruby from the language dropdown doesn't change the language to Ruby. It just keeps the Python code and removes the Python syntax highlighting. But the in-depth explanations are a huge help to me, as always!

2

Reply
Mike Chang
Premium
• 10 months ago

Please fix test case 1

2

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

