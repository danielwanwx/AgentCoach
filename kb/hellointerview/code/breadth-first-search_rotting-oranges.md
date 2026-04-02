# Rotting Oranges

> Source: https://www.hellointerview.com/learn/code/breadth-first-search/rotting-oranges
> Scraped: 2026-03-30


You are given an m x n grid representing a box of oranges. Each cell in the grid can have one of three values:

"E" representing an empty cell
"F" representing a fresh orange
"R" representing a rotten orange

Every minute, any fresh orange that is adjacent (4-directionally: up, down, left, right) to a rotten orange becomes rotten.

Write a function that takes this grid as input and returns the minimum number of minutes that must elapse until no cell has a fresh orange. If it is impossible to rot every fresh orange, return -1.

Example 1:

Input:

grid = [
["R", "F"],
["F", "F"],
]

Output: 2

Explanation:

After Minute 1: The rotting orange at grid[0][0] rots the fresh oranges at grid[0][1] and grid[1][0]. After Minute 2: The rotting orange at grid[1][0] (or grid[0][1]) rots the fresh orange at grid[1][1].

So after 2 minutes, all the fresh oranges are rotten.

Example 2:

Input:

grid = [
["R", "E"],
["E", "F"],
]

Output: -1

Explanation:

The two adjacent oranges to the rotten orange at grid[0][0] are empty, so after 1 minute, there are no fresh oranges to rot. So it is impossible to rot every fresh orange.

Example 3:

Input:

grid = [
["R", "F", "F", "F"],
["F", "F", "F", "R"],
["E", "E", "F", "F"],
]

Output: 2

CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def rotting_oranges(self, grid: List[List[str]]) -> int:
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
We can model this problem as a graph where each cell is a node and the edges are the connections between adjacent cells.
The key to this problem is recognizing that we can simulate the rotting process using a breadth-first search (BFS) traversal of the graph (since any rotting orange will cause its neighbors to rot in the next minute).
Step 1: Initialize BFS Queue And Count Fresh Oranges
We can start by iterating over each cell in the grid and adding the position of all the rotten oranges to a queue. As we iterate, we can also count the number of fresh oranges in the grid - which will help us determine if there are any fresh oranges left after the BFS traversal.
R
F
F
 
F
F
F
R
 
F
F
F
F
F
Queue: [(0, 0), (1, 3)]
Fresh Oranges: 9
Minute: 0
Step 2: BFS Traversal
Next, we find all the oranges that will rot in the next minute. For each rotten orange in the BFS queue, we check if any of its neighbors are fresh oranges. If so, we turn the fresh orange into a rotten orange and add it to the queue to prepare for the next minute (shown in orange in the diagrams below). We also decrement the count of fresh oranges.
When we have finished processing all the rotten oranges in the queue, we increment the minute counter and repeat the process until there are no more fresh oranges left or the queue is empty.
R
R
F
 
R
R
F
R
 
F
F
R
R
F
Queue: [(0, 1), (1, 0), (0, 3), (1, 2), (2, 3)]
Fresh Oranges: 5
Minute: 1
 
 
R
R
R
 
R
R
R
R
 
R
F
R
R
R
Queue: [(0, 2), (1, 1), (2, 0), (2, 2)]
Fresh Oranges: 1
Minute: 2
 
 
R
R
R
 
R
R
R
R
 
R
R
R
R
R
Queue: [(2, 1)]
Fresh Oranges: 0
Minute: 3
 
 
The state of the orange box after each minute. The oranges that became rotten during this minute are colored in orange, while the "visited" oranges are dimmed.
If fresh_oranges is 0, then all oranges have become rotten, and we return the number of minutes it took to make all the oranges rotten. Otherwise, we return -1, as not all oranges can become rotten.
Solution
SOLUTION
Python
Language
from collections import deque

class Solution:
    def rotting_oranges(self, grid):
        if not grid:
            return -1

        rows, cols = len(grid), len(grid[0])
        queue = deque()
        fresh_oranges = 0

        # Step 1: Initialize BFS Queue and Count Fresh Oranges
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == "R":
                    queue.append((r, c))
                elif grid[r][c] == "F":
                    fresh_oranges += 1


        # Step 2: Perform BFS to Simulate Rotting Process
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        minutes = 0
        while queue and fresh_oranges > 0:
            minutes += 1

            # process all the rotten oranges at the current minute
            for _ in range(len(queue)):
                x, y = queue.popleft()
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == "F":
                        grid[nx][ny] = "R"
                        fresh_oranges -= 1
                        queue.append((nx, ny))

        return minutes if fresh_oranges == 0 else -1
What is the time complexity of this solution?
1

O(log m * n)

2

O(m * n)

3

O(n)

4

O(4ⁿ)

Mark as read

Next: 01-Matrix

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

(13)

Comment
Anonymous
​
Sort By
Popular
Sort By
2
22-quibble-herder
Premium
• 5 months ago

I got asked this question in an interview a few months ago, I was able to come up with BFS but didn't think about doing simultaneous level-order traversals from multiple grid cells. Awesome!

4

Reply
Perry Lim
• 2 months ago

yahoo

0

Reply
A
AcceptedCopperRaven971
Premium
• 1 month ago

You have an error in your tests.
If the grid is empty, then it takes 0 steps to rot every fresh orange.

The expected output for test case 2 should be 0, not -1.

0

Reply
E
EntireBrownDragon895
Premium
• 8 days ago

I think 0 and -1 both make sense. 0 because there are not fresh oranges so it takes 0 minutes. -1 because there are no fresh oranges to it's impossible to let them rot.

0

Reply
L
LexicalBronzeWolverine167
Premium
• 2 months ago
def rotting_oranges(self, grid: List[List[str]]):
        if not grid:
            return -1
            
        row_max = len(grid)
        col_max = len(grid[0])
        butti = [[-1 for _ in range(col_max)] for _ in range(row_max)]
        dirs = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        queue = deque()
        fresh_orange_present = False

        for i in range(row_max):
            for j in range(col_max):
                if grid[i][j] == 'F':
                    butti[i][j] = 0
                    fresh_orange_present = True
                elif grid[i][j] == 'R':
                    butti[i][j] = 1
                    queue.append((i, j))

        if not queue and fresh_orange_present:
            return -1

        print(queue)
        while queue:
            row, col = queue.popleft()

            for d in dirs:
                nrow = row + d[0]
                ncol = col + d[1]

                if (
                    0 <= nrow < row_max
                    and 0 <= ncol < col_max
                    and butti[nrow][ncol] == 0
                ):
                    butti[nrow][ncol] = butti[row][col] + 1
                    queue.append((nrow, ncol))

        min_time = 0
        for i in range(row_max):
            for j in range(col_max):
                if butti[i][j] == 0:
                    return -1
                min_time = max(min_time, butti[i][j])

        return min_time - 1
Show More

0

Reply
M
malinibhandaru
Premium
• 2 months ago
• edited 2 months ago

I ended up just using the grid and for-loops and while (fresh and change), still O(MxN), and used marker to not in a sweep mess with timing. Love your BFS solution.

def markRot(self, grid, i, j):
        if i >= 0 and i < len(grid) and j >= 0 and j < len(grid[0]): # valid cell
            if grid[i][j] == "F": # fresh orange
                grid[i][j] = "NR"
                

    def rotting_oranges(self, grid: list[list[str]]):
        if not grid   :
            return -1

        fresh = True
        steps = 0
        change = True
        while change and fresh:
            #print("Inside while loop")
            fresh = False
            change = False
            for i in range(len(grid)):
                for j in range(len(grid[0])):
                    if grid[i][j] == "R":
                        # mark rot for next time interval
                        self.markRot(grid, i-1, j)
                        self.markRot(grid, i+1, j)
                        self.markRot(grid, i, j-1)
                        self.markRot(grid, i, j+1)
                        
                # change the "NR" to "R" to affect new cells in next cycle
            for i in range(len(grid)):
                for j in range(len(grid[0])):
                    if grid[i][j] == "NR":
                        grid[i][j] = "R"
                        change = True
                    elif grid[i][j] == "F":
                        fresh = True
            if change:
                steps += 1

        print(f"fresh = {fresh}, change = {change}, steps = {steps}")
        if fresh:
            return -1
        else:
            return steps# Your code goes here
Show More

0

Reply
fz zy
Premium
• 2 months ago
class Solution:
    def rotting_oranges(self, grid: List[List[str]]):
        if not grid:
            return -1
        n, m = len(grid), len(grid[0])
        queue = deque([])
        cnt = 0
        for i in range(n):
            for j in range(m):
                if grid[i][j] == 'R':
                    queue.append((i, j))
                if grid[i][j] == 'F':
                    cnt += 1
        minutes = 0
        dirs = [-1, 0, 1, 0, -1]
        while cnt and queue:
            size = len(queue)
            for i in range(size):
                x, y = queue.popleft()
                for i in range(4):
                    nx, ny = x + dirs[i], y + dirs[i + 1]
                    if 0 <= nx < n and 0 <= ny < m and grid[nx][ny] == 'F':
                        grid[nx][ny] = 'R'
                        cnt -= 1
                        queue.append((nx, ny))
            minutes += 1
        return -1 if cnt else minutes
        
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

Step 1: Initialize BFS Queue and Count Fresh Oranges

Step 2: BFS Traversal

Solution
