# 01-Matrix

> Source: https://www.hellointerview.com/learn/code/breadth-first-search/01-matrix
> Scraped: 2026-03-30



A
Anatoly
Premium
• 8 months ago

It's not necessary to calculate distance in a separate variable and introduce for loop.
output[r][c] has the distance to nearest zero, its neighbors will have +1 distance.

while (queue.length > 0) {
    const [r, c] = queue.shift();

    for (const [dr, dc] of directions) {
        const nr = r + dr;
        const nc = c + dc;

        if (nr >= 0 && nr < rows && nc >= 0 && nc < cols) {
            if (output[nr][nc] === -1) {
                output[nr][nc] = output[r][c] + 1;
                queue.push([nr, nc]);
            }
        }
    }
}

7

Reply
P
PrincipalCoralOctopus997
Top 5%
• 1 year ago

dont understand why its O(m*n) time complexity here but O(n) time complexity and space for rotting oranges, both very similar and operate on all the cells of the matrix in the worst case right

1

Reply
Jimmy Zhang
Top 5%
• 1 year ago

Hey nice catch. The rotting oranges time complexity is confusing as written, it says where N is the total cells in the matrix, which is the same as m * n.

i'll update it.

4

Reply
H
HolyBeigeDragon306
Premium
• 1 month ago
• edited 1 month ago

The time complexity O(x * y), can also be true depending how you phrase it similar to O(m * n):

Time Complexity: O(x * y) where x is the number of rows and y is the number of columns in the input matrix. We visit each cell at most once, and each cell is enqueued at most once

0

Reply
L
LexicalBronzeWolverine167
Premium
• 2 months ago
def updateMatrix(self, mat: List[List[int]]):
        row_max = len(mat)
        col_max = len(mat[0])
        output = [[-1 for _ in range(col_max)] for _ in range(row_max)]
        dirs = [[-1, 0], [1, 0], [0, -1], [0, 1]]

        queue = deque()
        visited = set()

        for i in range(row_max):
            for j in range(col_max):
                if mat[i][j] == 0:
                    output[i][j] = 0
                    queue.append((i, j))
                    visited.add((i, j))
        
        while queue:
            row, col = queue.popleft()

            for d in dirs:
                nrow = row + d[0]
                ncol = col + d[1]

                if 0 <= nrow < row_max and 0 <= ncol < col_max and (nrow, ncol) not in visited:
                    output[nrow][ncol] = output[row][col] + 1
                    queue.append((nrow, ncol))
                    visited.add((nrow, ncol))

        return output
Show More

0

Reply
C
chenyuluforever
Premium
• 2 months ago

What a great way to use output matrix to store the state of BFS! We save an additional set with this approach.

0

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

Step 1: Initialize the Queue

Step 2: Perform BFS Traversal (Distance 1)

Step 3: Perform BFS Traversal (Distance 2)

Step 4: Perform BFS Traversal (Distance 3)

Step 5: Return the Output Grid

Solution

