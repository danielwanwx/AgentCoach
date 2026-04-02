# Number of Islands

> Source: https://www.hellointerview.com/learn/code/depth-first-search/number-of-islands
> Scraped: 2026-03-30


You are given binary matrix grid of size m x n, where '1' denotes land and '0' signifies water. Determine the count of islands present in this grid. An island is defined as a region of contiguous land cells connected either vertically or horizontally, and it is completely encircled by water. Assume that the grid is bordered by water on all sides.

Input:

grid = [
[1,1,0,1],
[1,1,0,1],
[1,1,0,0],
]

Output:

2
CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def number_of_islands(self, grid: List[List[int]]) -> int:
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
This solution uses depth-first search to traverse the grid and count the number of islands.
The algorithm starts at the first cell of the grid and explores all the adjacent cells that are part of the same island. To be part of the same island, a cell must be a 1 and must be adjacent to the current cell. During each recursive call, the algorithm first marks the current cell by changing its value to 0 so that it does not explore the same cell again.
We'll walkthrough how the algorithm detects 2 islands in the example grid:
[
[1, 1, 0, 1],
[1, 1, 0, 1],
[1, 1, 0, 0]
]
First Island
The algorithm starts by iterating over all cells in the grid. If it finds a 1, it increments the count variable and starts the depth-first search exploration from that cell. The algorithm explores all the reachable cells of the island, marking them as 0 so that it does not explore them again.
VISUALIZATION
Python
Language
Full Screen
def numIslands(grid):
    if not grid:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    count = 0
    
    def dfs(r, c):
        grid[r][c] = 0
        if r + 1 < rows and grid[r + 1][c] == 1:
            dfs(r + 1, c)
        if r > 0 and grid[r - 1][c] == 1:
            dfs(r - 1, c)
        if c + 1 < cols and grid[r][c + 1] == 1:
            dfs(r, c + 1)
        if c > 0 and grid[r][c - 1] == 1:
            dfs(r, c - 1)
        return
    
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 1:
                count += 1
                dfs(i, j)
    
    return count
1
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
i: 0
j: 0
count: 0

i = 0

0 / 19

1x
Once the algorithm has explored all reachable cells of the island, it iterates over the remaining cells to find the start of the next island. When it finds a 1, it increments the count variable and starts the depth-first search exploration again from that cell, this time exploring all the reachable cells of the new island.
Second Island
Once the first call to dfs has returned, the algorithm continues iterating over the remaining cells. When it finds another cell with value of 1, then this is start of a new island.
VISUALIZATION
Python
Language
Full Screen
def numIslands(grid):
    if not grid:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    count = 0
    
    def dfs(r, c):
        grid[r][c] = 0
        if r + 1 < rows and grid[r + 1][c] == 1:
            dfs(r + 1, c)
        if r > 0 and grid[r - 1][c] == 1:
            dfs(r - 1, c)
        if c + 1 < cols and grid[r][c + 1] == 1:
            dfs(r, c + 1)
        if c > 0 and grid[r][c - 1] == 1:
            dfs(r, c - 1)
        return
    
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 1:
                count += 1
                dfs(i, j)
    
    return count
0
0
0
1
0
0
0
1
0
0
0
0
0
0
0
0
i: 0
j: 0
count: 1

recursive call

0 / 9

1x
The algorithm continues this process until it has explored all the cells of the grid, at which point it returns the count variable, which contains the number of islands.
Animated Solution
nums
​
|
nums
2d-list of 0s and 1s
Try these examples:
All Water
Two Islands
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def numIslands(grid):
    if not grid:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    count = 0
    
    def dfs(r, c):
        grid[r][c] = 0
        if r + 1 < rows and grid[r + 1][c] == 1:
            dfs(r + 1, c)
        if r > 0 and grid[r - 1][c] == 1:
            dfs(r - 1, c)
        if c + 1 < cols and grid[r][c + 1] == 1:
            dfs(r, c + 1)
        if c > 0 and grid[r][c - 1] == 1:
            dfs(r, c - 1)
        return
    
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 1:
                count += 1
                dfs(i, j)
    
    return count
1
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

number of islands

0 / 46

1x
Complexity Analysis
For this problem, let m be the number of rows and n be the number of columns in the grid.
What is the time complexity of this solution?
1

O(log n)

2

O(4^L)

3

O(m * n)

4

O(N + Q)

Mark as read

Next: Surrounded Regions

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

(25)

Comment
Anonymous
​
Sort By
Popular
Sort By
P
PrincipalCoralOctopus997
Top 5%
• 1 year ago

missing runtime and space complexity for solution

17

Reply
S
socialguy
Top 5%
• 1 year ago

The LeetCode problem uses strings, while this problems uses ints. Either specify the type of the input, or align with LeetCode.

11

Reply
S
ShinySapphireHare306
Premium
• 4 months ago

Identified the "directions" pattern that maybe useful for these type of problems (stole this conveniently from a previous problem). Here is modified code

def numIslands(grid):
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return
        if grid[r][c] != '1':
            return
        grid[r][c] = '0'  # mark visited
        for dr, dc in directions:
            dfs(r + dr, c + dc)

    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                dfs(r, c)
    return count
Show More

6

Reply
Abhay Singh
Top 1%
• 1 year ago

Java Solution:

class Solution {

    public void dfs(char[][] grid, int i, int j, int[][] dxy){
        int n = grid.length;
        int m = grid[0].length;

        if(i<0 || j<0 || i==n || j==m || grid[i][j] == '-' || grid[i][j] == '0') return;

        grid[i][j] = '-';
        for(int k=0;k<4;k++){
            int x=i+dxy[k][0], y=j+dxy[k][1];
            dfs(grid, x, y, dxy);
        }
    }

    public int numIslands(char[][] grid) {
        int n = grid.length;
        int m = grid[0].length;

        int[][] dxy = {{-1,0}, {0,1}, {1,0}, {0,-1}};

        int ans = 0;
        for(int i=0;i<n;i++){
            for(int j=0;j<m;j++){
                if(grid[i][j] == '1'){
                    ans++;
                    dfs(grid, i, j, dxy);
                }
            }
        }

        return ans;
    }
}
Show More

4

Reply
H
hkim85
• 1 year ago

there are a mix of ints and strings for the inputs and solutions!

3

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

First Island

Second Island

Animated Solution

Complexity Analysis
