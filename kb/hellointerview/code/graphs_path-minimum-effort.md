# Path With Minimum Effort

> Source: https://www.hellointerview.com/learn/code/graphs/path-minimum-effort
> Scraped: 2026-03-30


A hiking app needs to find the easiest route across terrain. Given a 2D grid where each cell represents the elevation at that point, find the path from the top-left corner to the bottom-right corner that minimizes the "effort".

The effort of moving between two adjacent cells is the absolute difference in their elevations. The effort of a path is the maximum single-step effort along that path.

You can move up, down, left, or right from any cell. Return the minimum effort required.

Example 1:

1
10
2
2
3
3
3
2
1

Input:

heights = [[1,10,2], [2,3,3], [3,2,1]]

Output:

1

Explanation: The cliff (10) has a huge elevation difference. Going around via 1→2→3→2→1 avoids it entirely, with each step having effort at most 1.

Example 2:

4
3
2
2
6
3
3
2
1

Input:

heights = [[4,3,2], [2,6,3], [3,2,1]]

Output:

2

Explanation: The center peak (6) would require effort 3 to cross. Going around the top: 4→3→2→3→1 keeps maximum effort at 2.

CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def minimumEffortPath(self, heights: List[List[int]]) -> int:
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
Understanding the Problem
The key twist here is what we're optimizing for. We're not finding the shortest path (fewest steps) or the path with the smallest total elevation change. Instead, we want to minimize the single hardest step along the entire path.
Think of it like planning a hike: you might choose a longer, winding trail if it means avoiding one extremely steep section. The steepest part determines how difficult the hike feels, not the total distance or cumulative elevation gain.
1
START
10
2
2
3
3
3
2
1
END
Comparing two paths:
Path A (through cliff): 1→10→2→3→1
Steps: |10-1|=9, |2-10|=8, ...
Max effort = 9
Path B (around): 1→2→3→2→1
Steps: |2-1|=1, |3-2|=1, |2-3|=1, |1-2|=1
Max effort = 1 ✓ (optimal)
Answer: 1 (avoid the cliff!)
Notice something interesting, both paths visit the same number of cells, but Path B has much lower effort. This is because we're optimizing for the maximum step, not the sum of steps. A single "cliff" can ruin an otherwise reasonable path.
Brute Force: Try Every Path
The most straightforward approach: use DFS to explore every possible path from (0,0) to (m-1, n-1), track the maximum step along each path, and return the minimum across all paths.
SOLUTION
Python
Language
def minimumEffortPath(self, heights):
    rows, cols = len(heights), len(heights[0])
    result = float('inf')

    def dfs(r, c, max_effort, visited):
        nonlocal result
        if r == rows - 1 and c == cols - 1:
            result = min(result, max_effort)
            return
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                diff = abs(heights[nr][nc] - heights[r][c])
                visited.add((nr, nc))
                dfs(nr, nc, max(max_effort, diff), visited)
                visited.remove((nr, nc))

    dfs(0, 0, 0, {(0, 0)})
    return result
This works, but the number of possible paths through a grid grows exponentially. For a 3x3 grid it's fine, but for 100x100? We'd be waiting until the heat death of the universe. The time complexity is O(4^(m×n)) in the worst case, since at each cell we can branch in up to 4 directions.
We need something smarter.
A Clever Shortcut: Binary Search + BFS
Here's an interesting observation: if we could walk a path where no single step exceeds some threshold t, then we could definitely walk any path where the threshold is t+1 or higher. This monotonic property means we can binary search on the answer.
For a given threshold t, we just need to check: "Is there any path from start to end where every step has height difference ≤ t?" That's a simple BFS/DFS reachability check where we only traverse edges with weight ≤ t.
Binary search on threshold t:
t=0: Can we reach end? No path exists
t=1: Can we reach end? Yes! (answer ≤ 1)
Search space: [0, max_height]
Each check is O(m×n) BFS
Binary search: O(log(max_height))
Total: O(m×n × log(max_height))
This is way better than brute force! But we're running a full BFS for each binary search step, and the search range depends on the maximum height value (up to 10^6). Can we do even better?
Recognizing the Graph Pattern
Step back and think about what we actually have here:
Each cell is a node
Moving between adjacent cells is an edge with weight = height difference
We want to find the path from start to end that minimizes the maximum edge weight
This is a shortest path problem on a graph, but with a twist. In our previous shortest path problems like Network Delay Time and Cheapest Flights, we minimized the sum of edge weights. Here, we're minimizing the maximum edge weight along the path.
This is called a minimax path problem: find the path that minimizes the maximum edge weight.
This min-max pattern appears in many real-world scenarios: network bandwidth (limited by the slowest link), road capacity (limited by the narrowest segment), or hiking difficulty (limited by the steepest section).
Why Modified Dijkstra Works
Can we adapt Dijkstra's algorithm for this? In standard Dijkstra, we compute distances as the sum of edge weights. Here, we'd compute them as the max of edge weights. Does the greedy property still hold?
Think about it: if we've reached cell X with effort E (the max step along the path so far), any path that goes through X will have effort ≥ E, because max can only stay the same or increase as we add more edges. So when we pop a cell from the priority queue, we know no future path to that cell can do better.
That's the same greedy guarantee that makes standard Dijkstra work. The only thing that changes is the relaxation rule:
	Standard Dijkstra	Our Modified Version
Combine	new_dist = dist[curr] + weight	new_effort = max(effort[curr], weight)
Update	if new_dist < dist[next]	if new_effort < effort[next]
curr
current_effort
w
next
Update Rule:
new_effort = max(current_effort, w)
if new_effort < dist[next]: update
The algorithm is almost identical to standard Dijkstra:
State: (effort, row, col) where effort is the max step along the path so far
Priority Queue: Pop the cell with minimum effort first
Relaxation: For each neighbor with edge weight w, compute new_effort = max(current_effort, w). If it improves the best known effort to that neighbor, update and push
Early exit: The first time we pop the destination cell, that's our answer
Walkthrough
Let's trace through a 3×3 grid: [[1,10,2], [2,3,3], [3,2,1]]
Step 1: Initialize
Start at (0,0) with effort 0. Distance matrix initialized to ∞ except dist[0][0] = 0.
Priority Queue: [(0, 0, 0)]
1
d=0
10
d=∞
2
d=∞
2
d=∞
3
d=∞
3
d=∞
3
d=∞
2
d=∞
1
d=∞
Current: (0, 0, 0)
Neighbors: (0,1), (1,0)
Edge weights: |10-1|=9, |2-1|=1
Step 2: Process (0,0), update neighbors
Pop (effort=0, row=0, col=0) from the queue. We look at neighbors (0,1) and (1,0):
To (0,1): The height difference is |10-1| = 9. Since max(0, 9) = 9 < ∞, we update dist[0][1] = 9
To (1,0): The height difference is |2-1| = 1. Since max(0, 1) = 1 < ∞, we update dist[1][0] = 1
Priority Queue: [(1, 1, 0), (9, 0, 1)]
1
d=0 ✓
10
d=9
2
d=∞
2
d=1
3
d=∞
3
d=∞
3
d=∞
2
d=∞
1
d=∞
Observation:
Going right has effort 9 (cliff!)
Going down has effort 1 (better)
Notice the queue is sorted by effort: (1, 1, 0) comes before (9, 0, 1). The greedy approach will explore the low-effort path first.
Step 3: Process (1,0), continue exploring
Pop (effort=1, row=1, col=0). Check neighbors:
To (0,0): Already processed, skip
To (1,1): Height diff |3-2| = 1. new_effort = max(1, 1) = 1 < ∞, update dist[1][1] = 1
To (2,0): Height diff |3-2| = 1. new_effort = max(1, 1) = 1 < ∞, update dist[2][0] = 1
Priority Queue: [(1, 1, 1), (1, 2, 0), (9, 0, 1)]
1
d=0 ✓
10
d=9
2
d=∞
2
d=1 ✓
3
d=1
3
d=∞
3
d=1
2
d=∞
1
d=∞
Key insight:
We're expanding outward with
effort still at 1 (no cliffs yet)
Step 4-6: Reach destination
The algorithm continues, always picking the lowest-effort cell. It reaches (2,2) via the path that goes down and right, avoiding the "cliff" at cell (0,1).
Final distances:
1
d=0
10
d=9
2
d=2
2
d=1
3
d=1
3
d=2
3
d=1
2
d=1
1
d=1
Optimal Path Found!
(0,0) → (1,0) → (2,0)
→ (2,1) → (2,2)
Max effort = 1
The final answer is 1, we found a path where no single step requires more than 1 unit of effort. The cliff at (0,1) with height 10 was completely avoided by going around.
Solution
heights
​
|
heights
2D grid of elevations
Try these examples:
Flat
Steep Ridge
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def minimum_effort_path(heights):
    rows, cols = len(heights), len(heights[0])
    
    # Initialize distance array
    dist = [[float('inf')] * cols for _ in range(rows)]
    dist[0][0] = 0
    
    # Min-heap: (effort, row, col)
    heap = [(0, 0, 0)]
    
    # Directions: up, down, left, right
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while heap:
        effort, row, col = heapq.heappop(heap)
        
        # Check if reached destination
        if row == rows - 1 and col == cols - 1:
            return effort
        
        # Skip if already found better path
        if effort > dist[row][col]:
            continue
        
        # Explore neighbors
        for dr, dc in dirs:
            nr, nc = row + dr, col + dc
            
            if 0 <= nr < rows and 0 <= nc < cols:
                diff = abs(heights[nr][nc] - heights[row][col])
                new_effort = max(effort, diff)
                
                if new_effort < dist[nr][nc]:
                    dist[nr][nc] = new_effort
                    heapq.heappush(heap, (new_effort, nr, nc))
    
    return dist[rows - 1][cols - 1]
1
0
10
∞
2
∞
2
∞
3
∞
3
∞
3
∞
2
∞
1
∞
Min-Heap: [(0, 0, 0)]

Initialize: Start at (0,0). Push (effort=0, row=0, col=0) into min-heap

0 / 24

1x
Modified Dijkstra for minimum effort path
What is the time complexity of this solution?
1

O(m × n × log(m × n))

2

O(n³)

3

O(n)

4

O(V + E)

Mark as read

Next: Find City with Fewest Reachable

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

(3)

Comment
Anonymous
M
MeltedAmberPiranha299
Top 10%
• 1 month ago

The solution kind of just jumps into a 2d graph with d=infinite between edges. I think for that reason, this article feels much lower quality than some of the others. There's less tuition building here and it glosses over a lot of why things are done this way and what's been optimized. I wish to continue to see brute force > point out inefficiency > how we can do better > why this algorithm is the right solve.

0

Reply
fz zy
Premium
• 1 month ago
class Solution:
    def minimumEffortPath(self, heights: List[List[int]]):
        n, m = len(heights), len(heights[0])
        dxy = [-1, 0, 1, 0, -1]
        pq = [(0, 0, 0)]
        dp = [[float("inf")] * m for _ in range(n)]
        dp[0][0] = 0
        while pq:
            delta, x, y = heappop(pq)
            for i in range(4):
                nx = x + dxy[i]
                ny = y + dxy[i + 1]
                if nx < 0 or nx >= n or ny < 0 or ny >= m:
                    continue
                new_delta = max(delta, abs(heights[x][y] - heights[nx][ny]))
                if new_delta >= dp[nx][ny]:
                    continue
                dp[nx][ny] = new_delta
                heappush(pq, (dp[nx][ny], nx, ny))
        return dp[n-1][m-1]
Show More

0

Reply

Comments specific to prior versions of this article

Y
YelpingHarlequinMite618
Premium
• 2 months ago

soemthing

Incorrect spelling

2

Reply
Expand Old Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

Understanding the Problem

Brute Force: Try Every Path

A Clever Shortcut: Binary Search + BFS

Recognizing the Graph Pattern

Why Modified Dijkstra Works

Walkthrough

Solution
