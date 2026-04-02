# Bus Routes

> Source: https://www.hellointerview.com/learn/code/breadth-first-search/bus-routes
> Scraped: 2026-03-30



​
Sort By
Popular
Sort By
P
PassiveBlackChimpanzee437
Top 10%
• 1 year ago

the last paragraph of step 3 is not finished

4

Reply
Claudia Sun (Claudia)
Premium
• 3 months ago

solution needs to be updated from pop(0) to popleft()

3

Reply
H
HandsomeIvoryCrow799
Top 10%
• 8 months ago

Assuming:

N is number of routes.
b is maximum number of bus stops per route.

If we keep tracks of visited buses only then the time complexity would be: O(N*b*N)

But if we keep tracks of visited stops as well then the time complexity would be: O(N*b)

Each bus will be visited once, everytime we visit a bus, we'll visit all stops of that bus: O(N*b)
For each stop, we'll go through their list of associated buses only once: O(b*N)

Total time complexity: O(N*b+b*N) = O(N*b)

The code:

class Solution:
    def bus_routes(self, routes: List[List[int]], source: int, target: int):
        if source == target:
            return 0
        stopToBusMap = {}
        for i in range(len(routes)):
            for stop in routes[i]:
                if stop not in stopToBusMap:
                    stopToBusMap[stop] = []
                stopToBusMap[stop].append(i)        
        if source not in stopToBusMap:
            return -1
        queue = deque(stopToBusMap[source])
        visitedBus = set()
        visitedStop = set()
        numberOfBuses = 1
        while queue:
            levelSize = len(queue)
            for _ in range(levelSize):
                i = queue.popleft()
                if i in visitedBus:
                    continue
                visitedBus.add(i)
                nextRoutes = set()
                for stop in routes[i]:
                    if stop in visitedStop:
                        continue
                    if stop == target:
                        return numberOfBuses
                    nextRoutes.update(stopToBusMap[stop])
                    visitedStop.add(stop)
                queue.extend(list(nextRoutes))
            numberOfBuses += 1
        return -1
Show More

2

Reply
L
Libo
• 1 year ago

I think there's a typo in the sample solution. queue should be initialized as a deque() instead of a list.

2

Reply
Z
zachcristol
• 1 year ago

Looks to be resolved.

0

Reply
VK
Varun Kolanu
Top 10%
• 5 months ago

I have done it with another perspective wrt the stops. Posted the intuition and story for this
problem, and how a normal person would think in daily life here

The Code in CPP:

class Solution {
public:
    int numBusesToDestination(vector<vector<int>>& stopsServedByABus, int source, int target) {
        if (source == target) return 0;

        // Constructing buses that stop at a particular busStop
        unordered_map<int, vector<int>> busesThatStopAtAStop {};
        for (int bus=0; bus<stopsServedByABus.size(); ++bus) {
            for (auto &stop: stopsServedByABus[bus]) {
                busesThatStopAtAStop[stop].push_back(bus);
            }
        }

        // Maintenance
        queue<int> stopsToTry {};
        vector<int> didYouTryBus(stopsServedByABus.size(), 0);
        unordered_map<int, int> didYouAddStopInQueue {};
        int busesTakenToReach { 0 };

        stopsToTry.push(source);

        while (!stopsToTry.empty()) {
            int numStopsToTry = stopsToTry.size();
            ++busesTakenToReach;

            while (numStopsToTry--) {
                int currentStop = stopsToTry.front();

                for (auto &bus: busesThatStopAtAStop[currentStop]) {
                    if (!didYouTryBus[bus]) {
                        for (auto &stop: stopsServedByABus[bus]) {
                            if (!didYouAddStopInQueue[stop]) {
                                if (stop == target)
                                    return busesTakenToReach;
                                
                                stopsToTry.push(stop);
                                didYouAddStopInQueue[stop] = 1;
                            }
                        }
                        didYouTryBus[bus] = 1;
                    }
                }
                stopsToTry.pop();
            }
        }

        return -1;
    }
};
Show More

1

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

Representing the Graph

Walkthrough

Step 1: Initialize the Graph

Step 2: Initialize the Queue and Visited Set

Step 3: Perform BFS Traversal

