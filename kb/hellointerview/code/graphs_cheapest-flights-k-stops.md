# Cheapest Flights Within K Stops

> Source: https://www.hellointerview.com/learn/code/graphs/cheapest-flights-k-stops
> Scraped: 2026-03-30


A travel booking system needs to find the lowest-cost route between airports. You're given n cities connected by flights, where each flight [from, to, price] represents a direct route with its cost.

Find the cheapest route from src to dst that uses at most k layovers (intermediate cities). If no such route exists, return -1.

Note: A route with k layovers means visiting k intermediate cities, or equivalently, taking k+1 flights.

Example 1:

$100
$100
$100
$500
0
SRC
1
2
3
DST

Input:

n = 4
flights = [[0,1,100], [1,2,100], [2,3,100], [0,3,500]]
src = 0
dst = 3
k = 1

Output:

500

Explanation: The route 0→1→2→3 costs $300 with 2 layovers (cities 1 and 2), which exceeds k=1. The direct flight 0→3 costs $500 with 0 layovers. Even though it's more expensive, it's the only valid route.

Example 2:

$100
$100
$100
0
SRC
1
2
3
DST

Input:

n = 4
flights = [[0,1,100], [1,2,100], [2,3,100]]
src = 0
dst = 3
k = 1

Output:

-1

Explanation: The only path 0→1→2→3 requires 2 layovers (cities 1 and 2), but we're limited to k=1. No valid route exists.

CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def findCheapestPrice(self, n: int, flights: List[List[int]], src: 
    int, dst: int, k: int) -> int:
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
A flight booking system needs to find the cheapest route between cities, but travelers have a constraint: they don't want too many layovers. Given a network of flights with prices and a maximum number of stops allowed, find the minimum cost to reach the destination.
A
SRC
B
C
D
DST
$50
$30
$40
$60
Max stops: k
A→B→D = 1 stop
A→C→D = 1 stop
The key constraint is the stop limit. A "stop" is an intermediate city, so flying A→B→D has 1 stop (city B). If k=1, both routes above are valid. If k=0, only direct flights work.
First Intuition: Can We Use Dijkstra?
This is a shortest path problem. We need to find the cheapest route from source to destination. In Network Delay Time, we used Dijkstra's algorithm to find shortest paths. The algorithm worked beautifully:
Start from the source with distance 0
Always pick the cheapest unvisited node
Update distances to its neighbors
Once a node is processed, we have its optimal distance
Let's try applying the same approach here. We'll track the minimum cost to reach each city and greedily process the cheapest path first.
Testing Standard Dijkstra
Consider this example: Find the cheapest route from city 0 to city 3 with at most k=1 stops.
0
$10
1
$10
2
$10
3
Total: $30
2 stops ✗
0
$50
2
$10
3
Total: $60
1 stop ✓
Standard Dijkstra picks the $30 route (cheapest)
But it uses 2 stops, violating the k=1 constraint!
Standard Dijkstra greedily picks the cheapest path, but ignores the stop constraint
Why Standard Dijkstra Fails
The issue: Standard Dijkstra only tracks one value per city, i.e. the minimum cost to reach it. Once we mark a city as "visited" with its cheapest cost, we never reconsider it.
In the example above, standard Dijkstra would process cities in order of increasing cost:
Start at city 0 with cost $0
Process city 1 (cost $10), then city 2 (cost $20 via 0→1→2)
Mark city 2 as "visited" with cost $20
Reach city 3 with cost $30 via the 0→1→2→3 path
But there's also a more expensive way to reach city 2 which is directly from city 0 for $50. Standard Dijkstra would ignore this path because city 2 is already visited with a cheaper cost of $20.
But, the $50 path to city 2 only uses 1 stop, making the route 0→2→3 valid for k=1 (total cost $60). The cheaper $20 path uses 2 stops, making 0→1→2→3 invalid for k=1.
Standard Dijkstra greedily picks the cheapest path and misses the valid but more expensive alternative.
The Solution: Track Both City and Stops
We need to track not just "minimum cost to city X" but "minimum cost to city X using exactly S stops". This means our state must include both:
State: (cost, city, stops_used)
Heap: min-heap ordered by cost (same as Dijkstra)
Visited tracking: best[(city, stops)] = minimum cost to reach city having used exactly stops flights
This creates a state space where the same city can be visited multiple times with different stop counts. Each (city, stops) pair is treated as a distinct state.
Before
State: (cost, city)
dist[city] = min cost
One state per city
After
State: (cost, city, stops)
best[(city, stops)] = min cost
Multiple states per city
By extending the state space, we can track multiple ways to reach the same city
How the Algorithm Works
With this modified state, the algorithm becomes:
Initialize: Add (0, src, 0) to a min-heap (zero cost at source, zero stops used)
Process states: Pop the cheapest state (cost, city, stops) from the heap
Check destination: If city == dst, it means we found the cheapest valid route so return cost
Check constraint: If stops > k, this path exceeds the limit so skip it
Explore neighbors: For each neighbor, add (cost + price, neighbor, stops + 1) to the heap
Avoid redundancy: Track best[(city, stops)] to skip states we've seen with lower cost
Because the heap is ordered by cost, the first time we pop the destination city, we're guaranteed it's the cheapest path that satisfies the stop constraint.
This pattern of extending Dijkstra's state with additional constraints appears in many problems: shortest path with fuel limits, paths that must visit certain checkpoints, or paths with time windows. The key is identifying which extra dimension needs tracking.
Walkthrough
Let's trace through flights = [[0,1,100], [1,2,100], [2,3,100], [0,3,500]] with src=0, dst=3, k=1:
Step 1: Initialize
We start at city 0 with no cost and no stops used yet. Our min-heap contains just one state: (0, city=0, stops=0).
Graph State:
0
$0
1
∞
2
∞
3
∞
Min-Heap:
(0, city=0, stops=0)
Step 2: Process city 0
We pop (0, 0, 0) from the heap. City 0 isn't the destination, so we explore its outgoing flights:
Flight to city 1 costs $100: add (100, 1, 1) to heap
Flight to city 3 costs $500: add (500, 3, 1) to heap
Graph State:
0
$0
1
$100
2
∞
3
$500
Min-Heap:
(100, 1, 1)
(500, 3, 1)
Step 3: Process city 1
The min-heap pops (100, 1, 1) since it has the lowest cost. From city 1, we can fly to city 2 for $100, giving total cost $200. We add (200, 2, 2) to the heap.
Now the heap contains (200, 2, 2) and (500, 3, 1). Notice that the state (200, 2, 2) has lower cost but uses 2 flights (stops=2).
Graph State:
0
1
2
$200
3
Min-Heap:
(200, 2, 2)
(500, 3, 1)
Step 4: Process city 2
The heap pops (200, 2, 2). From city 2, we can fly to city 3 for $100, giving total cost $300. We add (300, 3, 3) to the heap.
But, stops=3 means we've taken 3 flights, which corresponds to 2 intermediate cities (1 and 2). This exceeds k=1!
Step 5: Check destination with invalid path
The heap pops (300, 3, 3). City 3 is our destination! But stops=3 > k+1=2, so this path is invalid. We skip it and continue.
Step 6: Found valid path
The heap pops (500, 3, 1). City 3 is the destination, and stops=1 means we took 1 flight (0→3), which has 0 intermediate cities. This is within k=1. Return $500.
Stop counting can be confusing! In this problem, k represents the maximum number of intermediate cities (layovers), not the number of flights. A path with k stops traverses k+1 edges. Our algorithm tracks stops_used which increments with each flight taken. To check validity, we compare stops_used against k+1.
Solution
flights
​
|
flights
[[from, to, cost], ...]
n
​
|
n
cities
src
​
|
src
start
dst
​
|
dst
end
k
​
|
k
max stops
Try these examples:
Too Many Stops
Cheaper Via Stop
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def find_cheapest_flight(flights, n, src, dst, max_stops):
    graph = defaultdict(list)
    for u, v, cost in flights:
        graph[u].append((v, cost))
    
    # (cost, city, stops_used)
    heap = [(0, src, 0)]
    # best[city][stops] = min cost to reach city with exactly stops
    best = {}
    
    while heap:
        cost, city, stops = heappop(heap)
        
        if city == dst:
            return cost
        
        if stops > max_stops:
            continue
        
        if (city, stops) in best and best[(city, stops)] <= cost:
            continue
        best[(city, stops)] = cost
        
        for neighbor, price in graph[city]:
            new_cost = cost + price
            heappush(heap, (new_cost, neighbor, stops + 1))
    
    return -1
100
200
400
50
100
0
$0
1
∞
2
∞
3
∞
Min-Heap: []

Build adjacency list from flight routes

0 / 21

1x
Modified Dijkstra tracking (cost, city, stops)
What is the time complexity of this solution?
1

O(n log n)

2

O(2ⁿ)

3

O(n * logn)

4

O(n · k · log(n · k))

When to Use This Pattern
This modified Dijkstra with state extension is useful in these scenarios:
Scenario	State Extension
Limited stops/hops	(cost, node, stops)
Fuel constraints	(cost, node, fuel_left)
Must-visit checkpoints	(cost, node, visited_mask)
Time windows	(cost, node, arrival_time)
Alternative: Bellman-Ford Approach
An alternative is to use a Bellman-Ford variant: run k+1 iterations, where each iteration relaxes all edges. This gives O(k · E) time complexity. For small k with many edges, this can be more efficient. However, the Dijkstra approach is more intuitive and generalizes better to other constraint types.
Connection to Network Delay Time
Both problems use shortest path algorithms, but:
Network Delay Time	Cheapest Flights
Standard Dijkstra	Modified Dijkstra
State: (dist, node)	State: (cost, city, stops)
Find min dist to ALL nodes	Find min cost to ONE node
Return max of all distances	Return first arrival at dst
No hop constraint	Limited to k stops

Mark as read

Next: Path With Minimum Effort

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

(5)

Comment
Anonymous
fz zy
Premium
• 1 month ago
class Solution:
    def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int):
        graph = {}
        for _src, _dst, _price in flights:
           graph.setdefault(_src, []).append((_dst, _price))
        pq = [(-1, 0, src)]
        dp = [float("inf")] * n
        while pq:
            stop, price, _from = heappop(pq)
            print(stop, price, _from)
            for _next, _next_price in graph.get(_from, []):
                if dp[_next] <= price + _next_price:
                    continue
                dp[_next] = price + _next_price
                if stop + 1 == k:
                    continue
                heappush(pq, (stop + 1, dp[_next], _next))
        return -1 if dp[dst] == float("inf") else dp[dst]  

0

Reply
Feng Xia
Premium
• 2 months ago

we can also check if k is valid before adding to the heap instead of checking when popping?

0

Reply
xiaoxiao liu
Premium
• 2 months ago

Agree, or change

if stops > max_stops:
            continue


to

if stops == max_stops:
            continue


0

Reply
Manoj Reddy
Premium
• 2 months ago
• edited 2 months ago

It would be

if stops == max_stops+1:
            continue


or the existing code also works with

if stops > max_stops:
           continue


Because max layovers +1 would be max flights(stops)

0

Reply
xiaoxiao liu
Premium
• 2 months ago

Yes, stops > max_stops or stops == max_stops+1 also works if you allow pushing an extra level and prune later.
In my implementation, stops represents edges used, and I prune before expansion, so stops == max_stops is the correct boundary and avoids pushing invalid states.

0

Reply
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

Understanding the Problem

First Intuition: Can We Use Dijkstra?

Testing Standard Dijkstra

Why Standard Dijkstra Fails

The Solution: Track Both City and Stops

How the Algorithm Works

Walkthrough

Solution

When to Use This Pattern

Alternative: Bellman-Ford Approach

Connection to Network Delay Time
