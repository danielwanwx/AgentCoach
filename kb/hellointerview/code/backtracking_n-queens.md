# N-Queens

> Source: https://www.hellointerview.com/learn/code/backtracking/n-queens
> Scraped: 2026-03-30


You're arranging a chess tournament and need to set up n queens on an n × n chessboard for a special demonstration. The challenge is to place all queens such that no two queens threaten each other.

In chess, a queen can attack any piece on the same row, column, or diagonal. Find all distinct arrangements where all n queens can coexist peacefully.

Constraints:

1 <= n <= 9

Example 1:

Input:

n = 4

Output:

[[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]
Solution 1
♛
♛
♛
♛
One of two valid arrangements

Explanation: There are two distinct arrangements for 4 queens on a 4×4 board where no queen attacks another.

Example 2:

Input:

n = 1

Output:

[["Q"]]
CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
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
Picture a chessboard where you need to place n queens such that none of them can attack each other. A queen attacks along rows, columns, and both diagonals. With a 4×4 board and 4 queens, how do we find all valid arrangements?
Queen Attack Pattern
♛
Queen attacks all red squares
Placement Rules
✓ Valid
♛
♛
♛
♛
✗ Invalid
♛
♛
Same diagonal!
The constraint seems simple, but it's deceptively tricky. With n queens on an n×n board, we need exactly one queen per row and column. The diagonals are where things get complicated.
The Approach
The naive approach would be to try every possible placement of n queens on n² squares. For n = 8, that's choosing 8 positions from 64 squares (roughly 4 billion combinations). Most are obviously invalid (multiple queens in the same row), so we're wasting massive computation.
A better strategy is to place queens one row at a time. Since each row must have exactly one queen, we only need to decide which column in each row. This reduces our choices from n² per queen to n per queen.
Row-by-Row Strategy
Row 0
♛
Row 1
♛
♛
Row 2...
♛
♛
But what happens when we reach a row where no column is valid? We've hit a dead end. This is where backtracking comes in: we undo our last choice and try a different option. If that row runs out of options too, we backtrack further, potentially unwinding several rows before finding a new path forward.
See it in action
Before diving into the details, watch the algorithm in action. Notice how it explores paths, hits dead ends, and unwinds the call stack when backtracking:
n
​
|
n
board size (1-6)
Try these examples:
2x2 Board
4x4 Board
Reset
VISUALIZATION
Full Screen
4-Queens Board
0
1
2
3
0
1
2
3
Searching...
Queen
Trying
Invalid

Initialize 4×4 chessboard

0 / 232

1x
Watch the algorithm explore, backtrack, and find solutions
Pay attention to when the algorithm backtracks multiple levels. Not just to the previous row, but sometimes all the way back to the beginning. When a path fails, we don't just try the next option at the current level. We may need to completely abandon earlier decisions too.
How It Works
Checking Validity
Before placing a queen at position (row, col), we check three things. Since we place row-by-row, we only need to check squares above the current row.
Column: Is there a queen in the same column above?
Upper-left diagonal: Any queen on the diagonal going up-left?
Upper-right diagonal: Any queen on the diagonal going up-right?
isValid(board, row, col)
    // Check column above
    for i from 0 to row - 1
        if board[i][col] == 'Q'
            return false
    
    // Check upper-left diagonal
    i = row - 1, j = col - 1
    while i >= 0 and j >= 0
        if board[i][j] == 'Q'
            return false
        i = i - 1, j = j - 1
    
    // Check upper-right diagonal
    i = row - 1, j = col + 1
    while i >= 0 and j < n
        if board[i][j] == 'Q'
            return false
        i = i - 1, j = j + 1
    
    return true
The Complete Algorithm
Here's how the pieces fit together:
solveNQueens(n)
    board = n x n grid of '.'
    result = []
    backtrack(0, board, result)
    return result

backtrack(row, board, result)
    if row == n
        result.add(copy of board)
        return
    
    for col from 0 to n - 1
        if isValid(board, row, col)
            board[row][col] = 'Q'
            backtrack(row + 1, board, result)
            board[row][col] = '.'  // backtrack
We try each column in the current row. If valid, place the queen and recurse. When we return from recursion (whether we found a solution or hit a dead end), we remove the queen and try the next column. This "place, recurse, remove" pattern is the essence of backtracking.
Walkthrough
Let's trace through n = 4 step by step, paying special attention to what happens when the algorithm backtracks multiple levels.
Phase 1: Initial Exploration
Step 1: Start at row 0, place at column 0
We begin with an empty board. At row 0, we try column 0 first. Valid! The board is empty.
♛
Place queen at (0, 0) ✓
Step 2: Row 1, find valid column
At row 1, columns 0 and 1 are blocked (column and diagonal). Column 2 is valid!
♛
♛
Place queen at (1, 2) ✓
Step 3: Row 2 hits a dead end
At row 2, let's check each column:
Column 0: Same column as queen at (0,0) ✗
Column 1: Diagonal from (0,0) ✗
Column 2: Same column as queen at (1,2) ✗
Column 3: Diagonal from (1,2) ✗
No valid position! We must backtrack.
♛
♛
Row 2: All columns blocked! Backtrack...
Phase 2: First Backtrack (Row 2 → Row 1)
Step 4: Back to row 1, try column 3
We return to row 1, remove the queen from column 2, and try column 3. Valid!
♛
♛
Remove (1,2), place at (1, 3) ✓
Step 5: Row 2 hits another dead end
At row 2, check each column:
Column 0: Same column as (0,0) ✗
Column 1: Diagonal from (0,0) ✗
Column 2: Diagonal from (1,3) ✗
Column 3: Same column as (1,3) ✗
Dead end again! Row 1 has no more columns to try (we already tried 2 and 3).
♛
♛
Row 2 blocked again! Row 1 exhausted...
Phase 3: Deep Backtrack (Row 2 → Row 1 → Row 0)
Step 6: Backtrack TWO levels to row 0
This is the critical moment. Row 1 has no more options, so we must backtrack further, all the way to row 0! We remove the queen from (0,0) and try column 1.
♛
Deep backtrack! Remove (0,0), try (0, 1)
This is multi-level backtracking in action. We didn't just undo one decision. We unwound the entire call stack back to the very first row.
Phase 4: Finding the First Solution
Step 7: Row 1 with fresh start, column 3 works
With the queen at (0,1), row 1's columns 0, 1, 2 are blocked. Column 3 is valid!
♛
♛
Place queen at (1, 3) ✓
Step 8: Row 2, column 0 works!
At row 2, column 0 is finally valid (no conflicts with queens at (0,1) or (1,3)).
♛
♛
♛
Place queen at (2, 0) ✓
Step 9: Row 3, column 2 completes the solution!
At row 3, column 2 is valid. We've placed all 4 queens. First solution found!
♛
♛
♛
♛
Solution #1 found!
Phase 5: Continuing to Find All Solutions
The algorithm doesn't stop at the first solution. It continues backtracking to find all valid configurations. After recording this solution, it backtracks from row 3 and continues exploring, eventually finding the second (and only other) solution:
Solution 1
♛
♛
♛
♛
Solution 2
♛
♛
♛
♛
These are mirror images of each other, which is common in symmetric problems like N-Queens.
Solution
Now that you understand how backtracking explores and unwinds, here's the algorithm with code. Watch how each step in the visualization corresponds to the highlighted lines:
n
​
|
n
board size (1-6)
Try these examples:
2x2 Board
4x4 Board
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def solveNQueens(n):
    result = []
    board = [['.' for _ in range(n)] for _ in range(n)]
    
    def backtrack(row):
        if row == n:
            result.append([''.join(r) for r in board])
            return
        for col in range(n):
            if is_valid(row, col):
                board[row][col] = 'Q'
                backtrack(row + 1)
                board[row][col] = '.'
    
    backtrack(0)
    return result
4-Queens Board
0
1
2
3
0
1
2
3
Searching...
Queen
Trying
Invalid

Initialize 4×4 chessboard

0 / 232

1x
N-Queens backtracking with code
What is the time complexity of this solution?
1

O(n!)

2

O(m * n * 4^L)

3

O(n log n)

4

O(n²)

Optimization: Use Sets for O(1) Conflict Check
Instead of scanning columns and diagonals each time, we can track occupied columns and diagonals in sets:
cols: set of occupied column indices
diag1: set of (row - col) values for upper-left to lower-right diagonals
diag2: set of (row + col) values for upper-right to lower-left diagonals
This reduces the validity check from O(n) to O(1), improving performance though the worst-case complexity remains O(n!).
Backtracking with constraint checking is perfect for:
Combinatorial puzzles (Sudoku, crosswords)
Constraint satisfaction problems
Problems asking for "all valid configurations"
Any search where you can detect invalid partial solutions early

Mark as read

Next: Topological Sort

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

(4)

Comment
Anonymous
Feng Xia
Premium
• 2 months ago
• edited 2 months ago

a slight suggestion - we could use sets to store the column indices we've placed queens before, and similarly using two sets for diagonals, one for left leaning diagonal and one for right leaning diagonal, please see details in the Leetcode's solution. This will reduce the check for a position to place queen is valid or not down to O(1) instead of O(N) in the current method.

1

Reply

Shivam Chauhan

Admin
• 2 months ago

Yes, this is a valid optimisation which we have mentioned in Optimization: Use Sets for O(1) Conflict Check section of the article. Nevertheless still the  time complexity would come out to be O(n!)

0

Reply
Akhil Mittal
Premium
• 2 months ago

Great article!

1

Reply
fz zy
Premium
• 1 month ago
import copy

class Solution:
    def solveNQueens(self, n: int):
        bits = [0] * n
        curr = [""] * n
        rowStrings = [["."] * n for _ in range(n)]
        for i in range(n):
            rowStrings[i][i] = 'Q'
            rowStrings[i] = ''.join(rowStrings[i])
        ans = []
        def dfs(row):
            if row == n:
                ans.append(copy.copy(curr))
                return
            for i in range(n):
                bit = 1 << i
                for j in range(row):
                    if bit in (bits[j], bits[j] << (row - j), bits[j] >> (row - j)):
                        break
                else:
                    bits[row] = bit
                    curr[row] = rowStrings[i]
                    dfs(row + 1)
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

The Approach

See it in action

How It Works

Checking Validity

The Complete Algorithm

Walkthrough

Phase 1: Initial Exploration

Phase 2: First Backtrack (Row 2 → Row 1)

Phase 3: Deep Backtrack (Row `2` → Row `1` → Row `0`)

Phase 4: Finding the First Solution

Phase 5: Continuing to Find All Solutions

Solution

Optimization: Use Sets for O(1) Conflict Check
