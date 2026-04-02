# Unique Paths

> Source: https://www.hellointerview.com/learn/code/dynamic-programming/unique-paths
> Scraped: 2026-03-30


You are given a robot that starts at the top-left corner of a grid with dimensions m x n. The robot can only move either down or right at any point in time. The goal is for the robot to reach the bottom-right corner of the grid.

Given the dimensions of the board m and n, write a function to return the number of unique paths the robot can take to reach the bottom-right corner.

Example 1

Input:

m = 2
n = 3

Output: 3

Explanation: The robot starts at the top-left corner and can move right or down. There are 3 unique ways to reach the bottom-right corner of a 2 x 3 grid.

1
2
3

Example 2

Input:

m = 3
n = 7

Output: 28

CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def unique_paths(self, m: int, n: int) -> int:
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
Let's understand the problem through a small example.
Consider a 3 x 2 grid (3 rows, 2 columns). The robot starts at the top-left and needs to reach the bottom-right. Since it can only move right or down, let's manually trace all possible paths:
1
2
3
But, how did the robot reach the destination cell?
Since the robot can only move right or down, it must have arrived at the destination from one of exactly two cells:
From above (by moving down)
From the left (by moving right)
from
above
from
left
destination
The robot can only reach the destination from the cell above or from the cell to the left
This means: the number of ways to reach any cell equals the sum of the ways to reach the cell above it plus the ways to reach the cell to its left. This is the core insight that leads us to a dynamic programming solution.
Finding the Recurrence Relation
Now let's formalize this intuition. We'll define dp[i][j] as the number of unique paths to reach cell (i, j) from the starting cell (0, 0).
Based on our insight above, to reach cell (i, j), the robot must come from either:
Cell (i-1, j) — directly above — and then move down
Cell (i, j-1) — directly to the left — and then move right
This gives us our recurrence relation:
dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
Base cases: If the robot is in the first row (i == 0), it can only have arrived by moving right repeatedly — there's exactly 1 path. Similarly, if the robot is in the first column (j == 0), there's exactly 1 path (moving down repeatedly).
For example, here's the complete DP table for a 3 x 2 grid. Each cell shows the number of unique paths to reach it:
1
1
1
2
1
3
dp[2][1] = 2 + 1 = 3
contributing cells
destination
The destination cell (2,1) gets its value by adding the cell above (2) and the cell to the left (1)
This recurrence relation is the core of our solution. Once we have it, there are two ways to implement it:
Recursive Solution (Top-Down)
The recursive solution directly implements our recurrence relation. We define a function uniquePaths(m, n) that returns the number of unique paths in an m x n grid.
The function recursively calls itself to find the number of paths to the cell above and the cell to the left, then adds them together. The base cases are when the grid has only one row (m == 1) or only one column (n == 1) — in these cases, there's only one possible path.
SOLUTION
Python
Language
def uniquePaths(m: int, n: int) -> int:
    if m == 1 or n == 1:
        return 1
    else:
        return uniquePaths(m - 1, n) + uniquePaths(m, n - 1)
Overlapping Subproblems
If we were to visualize the call tree of this recursive solution, we would see that are a few overlapping subproblems. For example, during a call to uniquePaths(3, 3), we end up calling uniquePaths(2, 2) twice.
(3,3)
(2,3)
(1,3)
(2,2)
(1,2)
(2,1)
(3,2)
(3,1)
(2,2)
(1,2)
(2,1)
To fix this, we can use memoization — storing results of subproblems in a dictionary. When we encounter a subproblem we've already solved, we return the cached result instead of recomputing it.
SOLUTION
Python
Language
def uniquePaths(m: int, n: int, memo: dict = {}) -> int:
    if m == 1 or n == 1:
        return 1
    elif (m, n) in memo:
        return memo[(m, n)]
    else:
        memo[(m, n)] = uniquePaths(m - 1, n, memo) + uniquePaths(m, n - 1, memo)
        return memo[(m, n)]
This allows us to "prune" parts of the call tree to avoid redundant calculations, which reduces the time complexity to O(m * n).
(3,3)
(2,3)
(1,3)
(2,2)
(1,2)
(2,1)
(3,2)
(3,1)
(2,2)
(1,2)
(2,1)
redundant call ​to (2, 2) pruned
x
Iterative Solution (Bottom-Up)
The other way to solve this problem is by using an iterative, "bottom-up" approach.
We'll initialize a 2D integer-array of size m x n called dp. Each entry in dp will hold the answer to a smaller subproblem. Since arrays are 0-indexed, dp[0][0] represents the number of unique paths the robot can take through a 1 x 1 grid, and dp[m - 1][n - 1] represents the number of unique paths the robot can take through a m x n grid. For this reason, it might be helpful to think of dp[i][j] as representing the number of unique paths a robot can take from cell (0, 0) to cell (i, j), which we'll do from now on.
Being able to clearly and precisely define what each subproblem returns is crucial for working effectively with dynamic programming algorithms.
In an iterative approach, we start by calculating the number of paths to reach cell [1][1], and then use that to calculate the number of paths to reach cell [1][2], [1][3], ..., [2][1], [2][2], [2][3], and so forth.
Step 1 is to define the base cases. We know that there is only one way to reach any cell in the top row (i == 0, j), or the leftmost column (i, j == 0), so we can initialize those values in dp directly.
# Set base case: there is only one way to reach any cell in the first row (moving only right)
for i in range(m):
    dp[0][i] = 1
# Set base case: there is only one way to reach any cell in the first column (moving only down)
for j in range(n):
    dp[j][0] = 1
Next, we can use a nested for-loop and our recurrence relation to calculate the number of paths to cells (1, 1), (1, 2), (1, 3), ... until cell m - 1, n - 1. After that is complete, we can return the value of dp[m - 1][n - 1] as the answer to our question.
Solution
SOLUTION
Python
Language
class Solution:
    def unique_paths(self, m: int, n: int) -> int:
        # Initialize a 2D array with dimensions m x n
        dp = [[0] * n for _ in range(m)]
        
        # base case: there is only one way to reach any cell in the first row (moving only right)
        for i in range(n):
            dp[0][i] = 1
            
        # Set base case: there is only one way to reach any cell in the first column (moving only down)
        for j in range(m):
            dp[j][0] = 1
        
        # Fill the rest of the dp array
        for i in range(1, m):
            for j in range(1, n):
                dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
        
        return dp[m - 1][n - 1]
What is the time complexity of this solution?
1

O(1)

2

O(n * logn)

3

O(4ⁿ)

4

O(m * n)

Mark as read

Next: Maximal Square

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

(7)

Comment
Anonymous
Abhay Singh
Top 1%
• 1 year ago

Java Solution: Combinatorics

class Solution {

    public long ncr(int n, int r){
        long ans=1;
        for(int i=0;i<r;i++){
            ans *= (n-i);
            ans /= (i+1);
        }
        
        return ans;
    }

    public int uniquePaths(int m, int n) {
        return (int) ncr(n+m-2, Math.min(n-1, m-1));
    }
}

6

Reply
Ognjen Sobajic
Premium
• 6 months ago

This is probably not the best example of dynamic programming. This solution runs in O(nxm) time takes O(nxm) space where a much better solution is to do simply calculate binomial coefficient of n+m-2 over m-1 because out of n+m-2 steps we decide between m-1 Ds and n-1 Rs, for example RDDRRR. A better example for understanding dynamic programming would be finding the number of ways but with obstacles, for example 0=way 1=wall in the matrix. That would be a perfect example.

2

Reply
fz zy
Premium
• 2 months ago
class Solution:
    def unique_paths(self, m: int, n: int):
        dp = [1] * n
        for i in range(1, m):
            for j in range(1, n):
                dp[j] += dp[j - 1]
        return dp[-1]

1

Reply
Kelvin Su
• 3 months ago

The explanation diagram is wrong. The matrix is m rows by n columns. So when m = 3, n = 2, the matrix should have 3 rows and 2 columns. The explanation diagram has 2 rows and 3 columns.

1

Reply
S
sherry-dash-shower
Premium
• 1 month ago

Since we're always adding the rows together, we can actually use a single DP array and just iterate over it m - 1 times for a slight space improvement. The AI actually pointed this out to me, but it's lacking from the suggested solution.

0

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

Building Intuition

Finding the Recurrence Relation

Recursive Solution (Top-Down)

Iterative Solution (Bottom-Up)

Solution
