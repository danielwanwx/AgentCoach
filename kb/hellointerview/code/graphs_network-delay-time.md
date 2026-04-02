# Network Delay Time

> Source: https://www.hellointerview.com/learn/code/graphs/network-delay-time
> Scraped: 2026-03-30


A distributed system has n servers labeled 1 to n. The servers communicate through directed connections, where each connection [from, to, latency] means server from can send a message to server to with the given latency (in milliseconds).

When server k broadcasts an alert, it propagates through the network along all available paths. Return the minimum time required for every server to receive the alert. If some servers are unreachable from k, return -1.

Example 1:

3
5
1
1
SOURCE
2
3

Input:

connections = [[1,2,3], [1,3,5], [2,3,1]]
n = 3
k = 1

Output:

4

Explanation: There are two paths to server 3: the direct path 1→3 takes 5ms, but the path 1→2→3 takes only 3+1=4ms. The last server to receive the alert determines the answer.

Example 2:

2
1
1
SOURCE
2
3
UNREACHABLE

Input:

connections = [[1,2,2], [3,2,1]]
n = 3
k = 1

Output:

-1

Explanation: The edge [3,2,1] points from server 3 to server 2, not the other way around. Server 1 can reach server 2, but there's no path from server 1 to server 3.

CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) 
    -> int:
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
We have a network of servers that communicate through directed connections with varying latencies. When server k broadcasts an alert, it propagates through the network along all available paths simultaneously.
1
SOURCE
3ms
2
1ms
3
Alert spreads
along all paths
A server receives the alert via whichever path reaches it first (the shortest path). Our task: find the time until every server has received the alert. If some server is unreachable, return -1.
Choosing the Right Algorithm
Before diving into implementation, let's think about which shortest path algorithm fits this problem. If you've read the Shortest Path Algorithms Overview, you know the decision comes down to the edge weights:
Edge Weights	Algorithm	Time Complexity
Unweighted (all = 1)	BFS	O(V + E)
Non-negative	Dijkstra ✓	O((V + E) log V)
Negative allowed	Bellman-Ford	O(V · E)
In this problem:
All latencies are positive (given in constraints) → Dijkstra works
We need single-source shortest paths (from k to all nodes) → Dijkstra is ideal
If we needed all-pairs shortest paths, we'd consider Floyd-Warshall, but that's overkill here
The observation
The problem asks us how long will it take until every server has received the alert?
Since the alert travels through all paths simultaneously, each server receives it via its shortest path from the source. But we need to wait for the last server to receive it. That means:
Run Dijkstra to find the shortest path from k to every server
The answer is the maximum of all these shortest paths
If any server is unreachable (distance = ∞), return -1
Looking back at the first example we are reminded that there's a direct path 1→3 (5ms) and an indirect path 1→2→3 (3+1=4ms). Dijkstra finds the faster 4ms route.
3
5
1
1
SOURCE
2
3

Two paths to server 3: the direct path costs 5ms, but going via server 2 costs only 4ms.

Handling Unreachable Servers
Not all servers may be reachable from the source. The direction of edges matters: [u, v, w] means u→v, not bidirectional.
Edge [3, 2, 1] means:
3
2
✓ 3 can reach 2
Does NOT mean:
2
3
✗ 2 can reach 3
If the source cannot reach a server, we return -1. In the second example, server 1 can reach server 2, but the only edge involving server 3 points from 3 to 2—not the reverse.
2
1
1
SOURCE
2
3
UNREACHABLE

Server 3 is unreachable from source 1 (edge goes 3→2, not 2→3). Return -1.

How Dijkstra Works
Dijkstra's algorithm greedily expands from the node with the smallest known distance. Because all edges are non-negative, once we process a node, we've found its shortest path.
1. Initialize
dist[source] = 0
dist[others] = ∞
heap = [(0, source)]
2. Pop minimum
(d, node) = heap.pop()
if d > dist[node]: skip
(stale entry)
3. Relax
for each neighbor:
new = d + weight
if new < dist: update
repeat until heap empty
4. Return result
If any dist = ∞ → return -1, else return max(dist)
This problem pattern appears frequently: "Find the shortest X from source to all nodes, then compute some aggregate (max, sum, count reachable)."
Solution
The solution is a direct application of Dijkstra's algorithm:
Build the adjacency list from the connections
Run Dijkstra from server k using a min-heap
Check reachability: if we didn't visit all n servers, return -1
Return max distance: the time for the last server to receive the alert
Watch Dijkstra explore the network. Notice how the min-heap always pops the smallest distance, and how distances update as shorter paths are discovered. Try different inputs to see how the algorithm handles various graph structures.
times
​
|
times
[[from, to, weight], ...]
n
​
|
n
number of nodes
k
​
|
k
source node
Try these examples:
Unreachable
Alt Path
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def network_delay_time(times, n, k):
    # Build adjacency list
    graph = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))
    
    # Dijkstra's algorithm
    distances = {k: 0}
    heap = [(0, k)]
    
    while heap:
        dist, node = heappop(heap)
        
        if dist > distances.get(node, float('inf')):
            continue
        
        for neighbor, weight in graph[node]:
            new_dist = dist + weight
            if new_dist < distances.get(neighbor, float('inf')):
                distances[neighbor] = new_dist
                heappush(heap, (new_dist, neighbor))
    
    # All nodes must be reachable
    if len(distances) != n:
        return -1
    return max(distances.values())
3
5
1
1
1
0
2
∞
3
∞
4
∞
Min-Heap: []

Network Delay Time - Dijkstra's Algorithm

0 / 20

1x
Dijkstra finding shortest paths to all servers
What is the time complexity of this solution?
1

O(4ⁿ)

2

O((V + E) log V)

3

O(4^L)

4

O(V + E)

Why Not BFS?
BFS only finds shortest paths when all edges have equal weight. In this problem, latencies vary, so we need Dijkstra's greedy approach with a priority queue. If all edges were weight 1, BFS would be simpler and faster at O(V + E).

Mark as read

Next: Cheapest Flights Within K Stops

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
fz zy
Premium
• 1 month ago
class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int):
        graph = {}
        for time in times:
            start, end, weight = time
            graph.setdefault(start - 1, []).append((weight, end - 1))
        h = [(0, k - 1)]
        dp = [float('inf')] * n
        dp[k - 1] = 0
        while h:
            weight, idx = heappop(h)
            for next_weight, next_idx in graph.get(idx, []):
                if dp[next_idx] <= weight + next_weight:
                    continue
                dp[next_idx] = weight + next_weight
                heappush(h, (weight + next_weight, next_idx))
        ans = max(dp)
        return -1 if ans == float('inf') else ans

0

Reply
Feng Xia
Premium
• 2 months ago

should the time complexity be O((V+E) log(V +E)) or O((V+E) log(E))  instead? since we are only pushing to the heap, and the maximum number of pushes is E

0

Reply

Comments specific to prior versions of this article

S
sherry-dash-shower
Premium
• 2 months ago

FYI: your JS solution suggests using the nullish coalescing operator (??) but your runtime doesn't support it.

0

Reply
Expand Old Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

Understanding the Problem

Choosing the Right Algorithm

The observation

Handling Unreachable Servers

How Dijkstra Works

Solution

Why Not BFS?
