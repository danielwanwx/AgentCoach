# Find City with Fewest Reachable

> Source: https://www.hellointerview.com/learn/code/graphs/find-city-fewest-reachable
> Scraped: 2026-03-30


A regional planning committee wants to identify the most "isolated" city in a road network. Given n cities connected by bidirectional roads with varying distances, find the city that can reach the fewest other cities within a given distance threshold.

If multiple cities have the same minimum count, return the city with the highest number.

Note: The distance between two cities is the shortest path distance considering all possible routes.

Example 1:

0
1
2
3
3
2
1
4
5
Threshold: 4
Answer: 3
1 reachable

Input:

n = 4
edges = [[0,1,3], [1,2,1], [1,3,4], [2,3,1]]
distanceThreshold = 4

Output:

3

Explanation: City 3 can only reach city 1 (distance 4) within the threshold. Cities 0 and 2 can each reach 2 cities, and city 1 can reach 3 cities. City 3 has the fewest reachable.

Example 2:

0
1
2
3
4
2
3
1
1
1
8
Threshold: 2
Answer: 0
1 reachable

Input:

n = 5
edges = [[0,1,2], [0,4,8], [1,2,3], [1,4,2], [2,3,1], [3,4,1]]
distanceThreshold = 2

Output:

0

Explanation: With threshold 2, city 0 can only reach city 1 (distance 2). Other cities can reach more neighbors. City 0 has the fewest reachable.

CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def findTheCity(self, n: int, edges: List[List[int]], 
    distanceThreshold: int) -> int:
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
A regional planning committee wants to identify the most "isolated" city in a road network for building a new data center. The ideal location minimizes connectivity to reduce network congestion risks. Given a network of cities connected by bidirectional roads with travel distances, find the city that can reach the fewest other cities within a given distance threshold.
0
1
2
3
ANSWER
3
2
1
4
5
Threshold: 4
City 3 reaches only
city 1 within dist 4
→ Fewest reachable!
With a threshold of 4, each city can reach different numbers of neighbors:
City 0: reaches cities 1 (dist 3) and 2 (dist 2) → 2 reachable
City 1: reaches cities 0 (dist 3), 2 (dist 1), 3 (dist 4) → 3 reachable
City 2: reaches cities 0 (dist 2), 1 (dist 1) → 2 reachable
City 3: reaches only city 1 (dist 4) → 1 reachable ← fewest!
City 3 can reach the fewest other cities, making it the most isolated and our answer.
Why This Differs from Previous Problems
In Network Delay Time, we needed shortest paths from one source to all nodes. Dijkstra was perfect. In Cheapest Flights, we needed shortest path from one source to one destination with constraints where some modification in Dijkstra worked.
But here, we need shortest paths from every city to every other city. Running Dijkstra n times for each node will give us the result, but there's a more optimised approach: Floyd-Warshall.
Single-Source
Network Delay Time
Cheapest Flights
Dijkstra: O((V+E) log V)
All-Pairs
Find City Fewest
Reachable
Floyd-Warshall: O(V³)
The Floyd-Warshall Approach
Floyd-Warshall finds shortest paths between all pairs of vertices using dynamic programming. The idea is that for each pair (i, j), we check if going through an intermediate vertex k gives a shorter path or not.
i
j
dist[i][j]
k
dist[i][k]
dist[k][j]
Relaxation:
dist[i][j] = min(dist[i][j],
dist[i][k] + dist[k][j])
The algorithm iterates through all possible intermediate vertices k, and for each k, checks if it provides a shorter path for every pair (i, j).
The Algorithm Step by Step
Initialize: dist[i][j] = edge weight if edge exists, 0 if i=j, ∞ otherwise
For each intermediate vertex k (outer loop):
For each source i (middle loop):
For each destination j (inner loop):
If dist[i][k] + dist[k][j] < dist[i][j], update dist[i][j]
Count reachable: For each city, count how many cities are within threshold
Return: City with minimum reachable count (highest numbered if tied)
The order of loops is critical in Floyd-Warshall. The intermediate vertex k must be the outermost loop. This ensures that when we consider paths through vertex k, we've already computed the best paths using vertices 0 to k-1.
Walkthrough
Let's trace through with 4 cities, edges [[0,1,3], [0,2,2], [1,2,1], [1,3,4], [2,3,5]], and threshold 4.
Step 1: Initialize Distance Matrix
Start with direct edge weights. Diagonal is 0, missing edges are ∞.
Initial dist[][] matrix:
0
1
2
3
0
0
3
2
∞
1
3
0
1
4
2
2
1
0
5
3
∞
4
5
0
Note
Roads are bidirectional
so dist[i][j] = dist[j][i]
(symmetric matrix)
Step 2: Process k=0, k=1, k=2, k=3
For each intermediate vertex, check if routing through it improves any path. After processing k=1:
dist[0][3] updates: 0→3 was ∞, but 0→1→3 = 3+4 = 7
After processing k=2:
dist[0][3] updates again: 0→2→3 = 2+5 = 7 (same)
dist[1][3] stays 4 (1→3 direct is better than 1→2→3 = 1+5 = 6)
Step 3: Count Reachable Cities (threshold=4)
After Floyd-Warshall completes, for each city count neighbors within threshold:
Reachable count (threshold=4):
0
→ cities 1 (dist 3), 2 (dist 2) = 2 reachable
1
→ cities 0 (dist 3), 2 (dist 1), 3 (dist 4) = 3 reachable
2
→ cities 0 (dist 2), 1 (dist 1) = 2 reachable
3
→ only city 1 (dist 4) = 1 reachable ✓
City 3 has the fewest reachable cities (1), so return 3.
Tie-breaking rule: If multiple cities have the same minimum reachable count, return the city with the highest number. This is why we iterate from 0 to n-1 and update the answer whenever we find a city with count ≤ current minimum.
When to Use Floyd-Warshall vs. Running Dijkstra n Times
Scenario	Floyd-Warshall	n × Dijkstra
Time complexity	O(V³)	O(V · (V+E) log V)
Dense graph (E ≈ V²)	O(V³) ✓	O(V³ log V)
Sparse graph (E ≈ V)	O(V³)	O(V² log V) ✓
Simple implementation	✓ Three nested loops	More complex
Works with negative edges	✓ (no negative cycles)	✗
For this problem, V ≤ 100, so Floyd-Warshall's O(V³) = O(10⁶) is fast enough and simpler to implement.
Solution
The solution applies Floyd-Warshall to compute all-pairs shortest paths, then counts reachable cities for each city:
Initialize distance matrix from edges (bidirectional, so set both directions)
Run Floyd-Warshall to find all shortest paths
Count reachable cities within threshold for each city
Return city with minimum count (highest number if tied)
edges
​
|
edges
[[u, v, weight], ...]
n
​
|
n
cities
threshold
​
|
threshold
max distance
Try these examples:
Threshold Tight
Larger Graph
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def find_the_city(n, edges, distance_threshold):
    # Initialize distance matrix with infinity
    dist = [[float('inf')] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    
    # Fill in direct edges (bidirectional)
    for u, v, w in edges:
        dist[u][v] = w
        dist[v][u] = w
    
    # Floyd-Warshall: try each vertex as intermediate
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    
    # Find city with fewest reachable within threshold
    result = 0
    min_reachable = n
    
    for city in range(n):
        count = sum(1 for j in range(n) 
                    if city != j and dist[city][j] <= threshold)
        if count <= min_reachable:
            min_reachable = count
            result = city
    
    return result
3
1
4
1
0
1
2
3
0
1
2
3
0
0
∞
∞
∞
1
∞
0
∞
∞
2
∞
∞
0
∞
3
∞
∞
∞
0

Initialize distance matrix: diagonal = 0, all others = ∞

0 / 21

1x
Floyd-Warshall finding all-pairs shortest paths
What is the time complexity of this solution?
1

O(m * n * 4^L)

2

O(V³)

3

O(m * n)

4

O(4^L)

Mark as read

Next: Dynamic Programming Fundamentals

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

(2)

Comment
Anonymous
fz zy
Premium
• 1 month ago
class Solution:
    def findTheCity(self, n: int, edges: List[List[int]], distanceThreshold: int):
        dp = [[float("inf")] * n for _ in range(n)]
        for src, dst, edge in edges:
            dp[dst][src] = dp[src][dst] = edge
        for k in range(n):
            for i in range(n):
                for j in range(i + 1, n):
                    dp[i][j] = dp[j][i] = min(dp[j][i], dp[j][k] + dp[k][i])
        ans = -1
        minCities = float("inf")
        for i in range(n - 1, -1, -1):
            cities = 0
            for j in range(n):
                cities += 1 if dp[i][j] <= distanceThreshold else 0
            if cities < minCities:
                ans = i
                minCities = cities
        return ans
Show More

0

Reply
C
ContinuousBlackRodent503
Premium
• 21 days ago

Need to check if i != j for cities += 1 although it's not affecting result

0

Reply
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

Understanding the Problem

Why This Differs from Previous Problems

The Floyd-Warshall Approach

The Algorithm Step by Step

Walkthrough

When to Use Floyd-Warshall vs. Running Dijkstra n Times

Solution
