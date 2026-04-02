# Maximal Square

> Source: https://www.hellointerview.com/learn/code/dynamic-programming/maximal-square
> Scraped: 2026-03-30


Given an m x n 2D matrix with only 0's and 1's, write a function to return the area of the largest square containing only 1's.

Input:

matrix = [
[0, 0, 1, 0, 0],
[1, 1, 1, 0, 1],
[0, 1, 1, 0, 0]
]

Output:

4
CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def maximal_square(self, matrix: List[List[int]]) -> int:
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
Let's say we're scanning through a binary matrix and we land on a cell that contains a 1. We want to know: what's the largest square of all 1's that has this cell as its bottom-right corner?
If the cell is on the first row or first column, the answer is easy, it would be at most a 1x1 square (just the cell itself). But what about cells deeper in the matrix?
Consider this small example. We're looking at the highlighted cell and want to know the largest square ending there:
1
1
1
1
1
1
1
0
1
The highlighted cell can form
a 2x2 square (side length = 2)
It can't form a 3x3 because
row 0 only has 3 cells to its
left including itself.
To form a square of side length k ending at a cell, three things must all be true:
The cell above it must be able to form a square of at least side k - 1 (enough 1's stretching up)
The cell to the left must be able to form a square of at least side k - 1 (enough 1's stretching left)
The cell diagonally above-left must be able to form a square of at least side k - 1 (enough 1's filling the interior)
If any one of those three neighbors has a smaller square, that becomes the bottleneck. The current cell's square can only be one bigger than the smallest of the three.
diagonal
dp[i-1][j-1]
above
dp[i-1][j]
left
dp[i][j-1]
current
dp[i][j]
dp[i][j] = 1 + min(
dp[i-1][j-1],
dp[i-1][j],
dp[i][j-1]
)
only when matrix[i][j] = 1
Why the Minimum?
Imagine the three neighbors have square sizes of 3, 2, and 3. You might think the answer is 4 (biggest neighbor + 1), but it's actually 3 (smallest neighbor + 1). Why?
3
3
2
?
min(3, 3, 2) + 1
= 3
The left neighbor can only form a 2x2 square.
That means there aren't enough 1's extending
to the left to support a 4x4 square here.
The weakest neighbor is the bottleneck — you
can only extend the square by 1 beyond it.
The square ending at the current cell is built by extending squares from those three directions. If any direction can't support a large enough square, the whole thing collapses.
The Recurrence Relation
Here's the formal recurrence, we define dp[i][j] as the side length of the largest square of all 1's whose bottom-right corner is at cell (i, j).
if matrix[i][j] == '1':
    dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
else:
    dp[i][j] = 0
Base cases: For cells in the first row or first column, dp[i][j] is just 1 if the cell contains a 1, and 0 otherwise. There's no room to form anything bigger than a 1x1 square on the edges.
The answer is max_side * max_side, where max_side is the largest value in the entire dp table.
Bottom-Up Solution
Now we can implement this. We create a 2D array dp of size (r + 1) x (c + 1) (padded by one row and column to avoid boundary checks). dp[i][j] stores the side length of the largest square ending at matrix[i - 1][j - 1]. Everything starts at 0.
VISUALIZATION
Python
Language
Full Screen
def maximal_square(matrix):
  if not matrix:
    return 0

  r = len(matrix)
  c = len(matrix[0])
  dp = [[0] * (c + 1) for _ in range(r + 1)]
  max_side = 0

  for i in range(1, r + 1):
    for j in range(1, c + 1):
      if matrix[i - 1][j - 1] == 1:
        top = dp[i - 1][j]
        left = dp[i][j - 1]
        diag = dp[i - 1][j - 1]
        dp[i][j] = min(top, left, diag) + 1
        max_side = max(max_side, dp[i][j])

  return max_side * max_side
1
0
1
0
0
1
0
1
1
1
1
1
1
1
1
1
0
0
1
0

maximal square

0 / 1

1x
We iterate through each cell. When we find a 1, we apply our recurrence — take the min of the three neighbors and add 1. We also track max_side as we go.
VISUALIZATION
Python
Language
Full Screen
def maximal_square(matrix):
  if not matrix:
    return 0

  r = len(matrix)
  c = len(matrix[0])
  dp = [[0] * (c + 1) for _ in range(r + 1)]
  max_side = 0

  for i in range(1, r + 1):
    for j in range(1, c + 1):
      if matrix[i - 1][j - 1] == 1:
        top = dp[i - 1][j]
        left = dp[i][j - 1]
        diag = dp[i - 1][j - 1]
        dp[i][j] = min(top, left, diag) + 1
        max_side = max(max_side, dp[i][j])

  return max_side * max_side
1
0
1
0
0
1
0
1
1
1
1
1
1
1
1
1
0
0
1
0
i,j
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0

i = 1 | j = 1

0 / 2

1x
Calculating size of the maximal square when `matrix[i - 1][j - 1] = 1`
VISUALIZATION
Python
Language
Full Screen
def maximal_square(matrix):
  if not matrix:
    return 0

  r = len(matrix)
  c = len(matrix[0])
  dp = [[0] * (c + 1) for _ in range(r + 1)]
  max_side = 0

  for i in range(1, r + 1):
    for j in range(1, c + 1):
      if matrix[i - 1][j - 1] == 1:
        top = dp[i - 1][j]
        left = dp[i][j - 1]
        diag = dp[i - 1][j - 1]
        dp[i][j] = min(top, left, diag) + 1
        max_side = max(max_side, dp[i][j])

  return max_side * max_side
1
0
1
0
0
1
0
1
1
1
1
1
1
1
1
1
0
0
1
0
i,j
0
0
0
0
0
0
0
1
0
1
0
0
0
1
0
1
1
1
0
1
1
1
0
0
0
0
0
0
0
0

i = 3 | j = 4

0 / 2

1x
Another maximal square calculation when `matrix[i - 1][j - 1] = 1`
At the end, max_side has the side length of the largest square, and the area is max_side * max_side.
Solution
nums
​
|
nums
2d-list of integers
Try these examples:
All Zeros
Small Square
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def maximal_square(matrix):
  if not matrix:
    return 0

  r = len(matrix)
  c = len(matrix[0])
  dp = [[0] * (c + 1) for _ in range(r + 1)]
  max_side = 0

  for i in range(1, r + 1):
    for j in range(1, c + 1):
      if matrix[i - 1][j - 1] == 1:
        top = dp[i - 1][j]
        left = dp[i][j - 1]
        diag = dp[i - 1][j - 1]
        dp[i][j] = min(top, left, diag) + 1
        max_side = max(max_side, dp[i][j])

  return max_side * max_side
1
0
1
0
0
1
0
1
1
1
1
1
1
1
1
1
0
0
1
0

maximal square

0 / 48

1x
What is the time complexity of this solution?
1

O(log n)

2

O(n * logn)

3

O(m * n)

4

O(n²)

Mark as read

Next: Longest Increasing Subsequence

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
Thomas Bao
Premium
• 1 year ago

I feel like this problem should be placed after unique paths, since the intuition is similar but requires an extra step which is to figure out a less trivial optimal substructure

6

Reply
R
RegulatoryMagentaPlatypus147
• 1 year ago

I agree

2

Reply
B
BeneficialApricotKoi336
Premium
• 3 months ago

Agreed, this problem is way easier after understanding the intuition behind Unique Paths

1

Reply
Abhay Singh
Top 1%
• 1 year ago

Java Solution: Top-Down

class Solution {

    int solve(char[][] grid, int i, int j, int[][] memo){
        int n=grid.length, m=grid[0].length;
        
        if(i<0 || j<0 || i==n || j==m || grid[i][j]=='0') return 0;
        
        if(memo[i][j] != -1) return memo[i][j];
        
        int c1 = solve(grid,i+1,j,memo);
        int c2 = solve(grid,i,j+1,memo);
        int c3 = solve(grid,i+1,j+1,memo);
        
        return memo[i][j] = 1 + Math.min(c1, Math.min(c2, c3));
    }

    public int maximalSquare(char[][] grid) {
        int n=grid.length, m=grid[0].length;

        int[][] memo = new int[n][m];
        for (int i = 0; i < n; i++) {
            Arrays.fill(memo[i], -1);
        }

        int ans = 0;
        for(int i=0;i<n;i++){
            for(int j=0;j<m;j++){
                if(grid[i][j] == '1'){
                    int c = solve(grid,i,j,memo);
                    ans = Math.max(ans, c*c);
                }
            }
        }

        return ans;
    }
}
Show More

4

Reply
B
BackIvoryDove366
Premium
• 2 months ago

Any reason to use different starting indices for matrix and dp? It looks very confusing

0

Reply
B
BackIvoryDove366
Premium
• 2 months ago

nvm, it's for padding dp with 0s to have clean solution on the first row and columns.

1

Reply
fz zy
Premium
• 2 months ago
class Solution:
    def maximal_square(self, matrix: List[List[int]]):
        if not matrix:
            return 0
        n, m = len(matrix), len(matrix[0])
        dp = [0] * (m + 1)
        largest = 0
        for i in range(n):
            for j in range(m):
                if matrix[i][j] == 1:
                    r = min(dp[j], dp[j - 1])
                    dp[j] = r + (1 if matrix[i - r][j - r] == 1 else 0)
                    largest = max(largest, dp[j])
        return largest * largest

0

Reply
Arun Ramakrishnan
Premium
• 3 months ago

Java top-down

public class Solution {
    int maxSide = 0;
    int[][] matrix;
    int m,n;
    Integer[][] memo;
    public Integer maximal_square(int[][] matrix) {
        // Your code goes here
        this.matrix = matrix;
        if (matrix == null || matrix.length == 0)
            return 0;
        this.m = matrix.length;
        this.n = matrix[0].length;
        memo = new Integer[m][n];
        helper(0,0);
        return maxSide*maxSide;
    }
    private Integer helper(int row, int col)
    {
        if (row >= m || col >= n)
            return 0;

        if (memo[row][col] == null)
        {
            int right = helper(row, col+1);
            int bottom = helper(row+1, col);
            int diagonal = helper(row+1, col+1);
            
            if (matrix[row][col] == 0)
            {
                memo[row][col] = 0;
            }
            else
            {
                memo[row][col] = 1+ Math.min(right, Math.min(bottom, diagonal));
                maxSide = Math.max(maxSide, memo[row][col]);
            }
        }
        return memo[row][col];
    }
}
Show More

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

Why the Minimum?

The Recurrence Relation

Bottom-Up Solution

Solution
