# Minimum Knight Moves

> Source: https://www.hellointerview.com/learn/code/breadth-first-search/minimum-knight-moves
> Scraped: 2026-03-30



​
Sort By
Popular
Sort By
W
WispyOliveIguana961
Top 10%
• 11 months ago

Another option here is to do level-by-level bfs where the depth of the "level" represents the number of moves made.

13

Reply
S
SubjectiveIndigoSkink289
• 4 months ago

Agree, this feels cleaner than having to store the move count with each coordinate since it requires less space.

3

Reply
Shannon Monasco
• 1 year ago

Minimum Knight Moves and the previous graphs page are missing from the contents on the left.

3

Reply
Orkhan Huseynli
Premium
• 17 days ago
• edited 17 days ago

This solution TLEs on LeetCode.

class Solution {
    minimum_knight_moves(x, y) {
        const DIRECTIONS = [
            [-2, 1], [-1, 2], [1, 2], [2, 1], // right side
            [-1, -2], [-2, -1], [1, -2], [2, -1] // left side
        ];

        const queue = [[0, 0]];
        const visited = new Set();
        visited.add('0,0');

        let steps = 0;
        while (queue.length > 0) {
            const size = queue.length;

            for (let i = 0; i < size; i++) {
                const [cx, cy] = queue.shift();

                if (cx == x && cy == y) {
                    return steps;
                }

                for (const [dx, dy] of DIRECTIONS) {
                    const [nx, ny] = [cx + dx, cy + dy];
                    const key = `${nx},${ny}`;

                    if (!visited.has(key)) {
                        visited.add(key);
                        queue.push([nx, ny]);
                    }
                }
            }

            steps++;
        }

        return -1;
    }
}
Show More

1

Reply
Sutirtho Datta
Premium
• 7 months ago
set syntax needs a minor correction

visited = {(0,0)} - Correction

visited = set((0,0))

The above actually creates a set with two separate elements {0}, because set() interprets (0,0) as an iterable of two integers. Try printing it and you will get output as {0} initially instead of {(0, 0)} expected.

The bug only affects the starting node (0,0). The BFS still works because we eventually mark every other coordinate visited correctly (visited.add((nx, ny)) stores tuples fine).
But we are doing one unnecessary duplicate visit for (0,0), which does not break correctness here but is logically wrong and could cause issues in other BFS problems.

1

Reply
Miriam Connor
• 1 year ago

Wait a minute. It can't be true that there are a total of x*y cells on the chessboard, can it?

Explanation: The knight can move from (0, 0) to (4, 4) in four moves ( [0, 0] -> [2, 1] -> [4, 2] -> [6, 3] -> [4, 4] )

On of the cells on the chessboard is [6, 3], which is outside a 4x4 board. But maybe I'm missing something about cells that aren't reachable, or would never be reached before returning?

1

Reply
retr0
• 1 year ago

Note that the board is of 'infinite size'. For testing purposes the problem later defines it as (-200,200) at max. This is why the algorithm is not dealing with any matrix nor graph. You assume the input will always be within the chessboard boundaries.

2

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

Step 1: Initialize the Queue and Visited Set

Step 2: Perform BFS Traversal

Solution

