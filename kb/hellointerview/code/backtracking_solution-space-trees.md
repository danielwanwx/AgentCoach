# Solution Space Trees

> Source: https://www.hellointerview.com/learn/code/backtracking/solution-space-trees
> Scraped: 2026-03-30


In the Overview section, we use Depth-First Search to explore all valid root-to-leaf paths in a binary tree that we are given. In most backtracking problems, we won't be given an explicit tree to traverse. Instead, our algorithm needs to construct the tree based on the problem.
Example: Letter Combinations of a Phone Number
DESCRIPTION
Given a string containing digits from 2-9 inclusive, return all possible letter combinations that the number could represent. Return the answer in any order.
A mapping of digit to letters (just like on the telephone buttons) is given below. Note that 1 does not map to any letters.
2: "abc"
3: "def"
4: "ghi"
5: "jkl"
6: "mno"
7: "pqrs"
8: "tuv"
9: "wxyz"
Example:
Input:
"23"
Output:
["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]
We can think about solving this problem incrementally, using the input "23" as an example.
We start with an empty string, and form all possible combinations that can be made using the first digit.
"2" -> ["a", "b", "c"]
Now we take each of these combinations above and add the letters corresponding to the second digit, "3".
Since "3" maps to "def", we add "d" to "a", "b", and "c", then "e" to "a", "b", and "c", and finally "f" to "a", "b", and "c".
"23" -> ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]
If we were to visualize this process a tree, it would look like this, where the leaf nodes represent the final combinations:
a
b
c
ad
ae
af
bd
be
bf
cd
ce
cf
This tree conceptually represents the "solution space" of all possible letter combinations of the phone number. If we can traverse this tree, we can find all valid combinations.
So how do we do so without an explicit tree to traverse? Let's break it down.
Writing a Backtracking Algorithm
Now that we can visualize the "solution-space" tree, our next step is to write a backtracking solution which uses depth-first search to explore all possible paths in the tree.
Defining the Recursive Function
Conceptually, each node in the tree corresponds to a single recursive call. Each recursive call will make additional recursive calls, which are represented by the edges in the tree.
To define our recursive function, we need to figure out what information we need to pass to each recursive call / node so that it can reach its neighbors, as this determines the parameters of our recursive function.
Let's illustrate with the example of "23":
At the root node, we start with an empty string. The children of the root node are "a", "b", and "c", which correspond to the digit 2. So we can label the root node with 2 parameters, the empty string, and 0, which represents the index of the digit in the input phone number we are currently processing.
"", 0
This suggests that our recursive function should have two arguments: the current combination, and the index of the digit we are currently processing.
SOLUTION
Python
Language
def backtrack(path, idx):
Next, we need to figure out how to explore the neighbors of the root node, which are "a", "b", and "c". We can get "a", "b", "c" by iterating over the letters corresponding to our digit "2", and adding each letter to our current combination (which right now is the empty string). For each of these letters, we make a recursive call with the updated combination and the next digit in the phone number.
"", 0
"a", 1
"b", 1
"c", 1
Since each edge in our tree corresponds to a recursive call, this suggests that the body of our recursive function should iterate over the letters corresponding to the current digit, and make a recursive call for each letter with the updated combination and the next digit in the phone number.
SOLUTION
Python
Language
def backtrack(path, idx):
    # base case
    ...

    for letter in phone[digits[idx]]:
        backtrack(path + letter, idx + 1)
Those recursive calls lead us to the last level of the tree, which are the leaf nodes. At the leaf nodes, we should add the current combination to our list of valid combinations.
"", 0
"a", 1
"b", 1
"c", 1
"ad", 2
"ae", 2
"af", 2
"bd", 2
"be", 2
"bf", 2
"cd", 2
"ce", 2
"cf", 2
We know we are at a leaf node when the index of the digit we are processing is equal to the length of the phone number. So we can add a base case to our recursive function to check if the index is equal to the length of the phone number. If it is, we add the current combination to our list of valid combinations.
SOLUTION
Python
Language
def backtrack(path, idx):
    # base case: we have reached a leaf node
    if idx == len(digits):
        result.append(path)
        return

    for letter in phone[digits[idx]]:
        backtrack(path + letter, idx + 1)
Finally, in the main function, we kick off the call to our recursive function with the empty string and the index 0 (the root node of our tree).
SOLUTION
Python
Language
def letterCombinations(digits):
    phone = {
        "2": "abc",
        "3": "def",
        "4": "ghi",
        "5": "jkl",
        "6": "mno",
        "7": "pqrs",
        "8": "tuv",
        "9": "wxyz"
    }

    def backtrack(path, idx):
        if idx == len(digits):
            result.append(path)
            return

        for letter in phone[digits[idx]]:
            backtrack(path + letter, idx + 1)

    result = []
    if digits:
        backtrack("", 0)
    return result
Summary
The first step in solving a backtracking problem is to visualize the solution-space tree.
Each node in the solution-space tree corresponds to a single recursive call.
The parameters of the recursive function correspond to the information needed to reach the neighbors of a node.
The body of the recursive function should iterate over the neighbors of a node and make recursive calls for each neighbor.
What is the time complexity of this solution?

where n = the number of digits in the input phone number

1

O(4ⁿ)

2

O(n * logn)

3

O(1)

4

O(4^L)

Solution-Space Tree Examples
The solution-space tree will look different for each backtracking problem, but one common type is a binary tree, where each node in the tree represents a "choose" or "don't choose" decision at that level.
This tree can be used to generate all possible subsets of a list of integers, which we breakdown below:
DESCRIPTION
Given a set of distinct integers, nums, return all possible subsets (the power set), without duplicates.
Example:
Input: nums = [1,2,3]
Output: [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]
The solution-space tree for this problem is a binary tree. Each node in the binary tree represents a different subset of the input.
[]
[1]
[1,2]
[1,2,3]
[1,2]
[1]
[1,3]
[1]
[]
[2]
[2, 3]
[2]
[]
[3]
[]
So how do we go from one node to its children in this tree? Each level in the tree corresponds to a different element in the input set, and each child node corresponds to either including (left) or excluding (right) the current element in the subset represented by the parent node.
At the root node, where current subset = [], and the current element is 1:
Left Child: We take the current subset and include 1. This gives us the subset [1].
Right Child: We take the current subset and exclude 1. This gives us the subset [].
For the subset [1], we repeat the process, now with current element 2:
Left Child: We take the current subset and include 2. This gives us the subset [1, 2].
Right Child: We take the current subset and exclude 2. This gives us the subset [1].
Given that information, try writing a backtracking solution for this problem on your own!

Mark as read

Next: Subsets

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

(16)

Comment
Anonymous
​
Sort By
Popular
Sort By
S
Suraj
Top 5%
• 1 year ago

I am not 100% sure but the time complexity for letter-combinations problem is O(N * 4 ^ N) and not O ( 4 ^ N). This is because we are copying the string towards the end which is internally an O(N) operation.

https://leetcode.com/problems/letter-combinations-of-a-phone-number

7

Reply
Aneesh Mysore
• 1 year ago

Yep correct. I think that was missed as strings are immutable so technically a new string is created every time a letter is added to the path

2

Reply
U
UniformSalmonAntlion275
• 1 month ago
• edited 1 month ago

https://leetcode.com/problems/subsets/description/
Leetcode was not happy with arr.copy(), then I used arr[:] instead.

    def subsets(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        if not nums:
            return [[]]
        result = []
               
        def dfs(i, arr):
            if i >= len(nums) :
                result.append(arr[:])
                return

            arr.append(nums[i])
            dfs(i + 1, arr)

            arr.pop()
            dfs(i + 1, arr)
        
        dfs(0, [])
        return result
Show More

1

Reply
P
PureCoralEagle843
Premium
• 10 months ago

I did not understand "For our problem, ... the branching factor is 4 (each digit maps to at most 4 letters, so 4 recursive calls are made)."

How is it 4 and not 3? In your solution space tree also you've shown the branching factor as 3.

1

Reply
W
WoodenAquamarineSnipe931
Top 10%
• 9 months ago

Take 9 : wxyz, length is 4 in the worst case. Hence branching factor of 4.

3

Reply
Mingyu Dai
• 1 year ago

nit: we can use list instead of string to reduce space complexity

1

Reply
Edwin Huang
Premium
• 3 days ago

What is n and L  in the complexity question? maybe include definitions for that would help a bit

0

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Example: Letter Combinations of a Phone Number

Writing a Backtracking Algorithm

Summary

Solution-Space Tree Examples
