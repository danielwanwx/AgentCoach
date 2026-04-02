# Course Schedule II

> Source: https://www.hellointerview.com/learn/code/graphs/course-schedule-ii
> Scraped: 2026-03-30



U
UpperIvoryWhitefish562
• 1 year ago

I think it's all great but if there was a way to see the last saved code it'd be nice to revise.

7

Reply
R
RoyalAquaSloth800
• 1 year ago

https://leetcode.com/problems/find-eventual-safe-states is a great question too!

3

Reply
Satya Dasara
Premium
• 2 months ago

Similar to Course Schedule 1 but we just have to append nodes popped out into a result list and return them.

Make sure that your indegree list and adjacency list map logic is correct as they'll be most bug prone in the code.

from collections import deque

class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]):
        
        indegree = [0 for i in range(numCourses)]
        adjacency_map = {i : [] for i in range(numCourses)}

        for prerequisite in prerequisites:
            a, b = prerequisite
            adjacency_map[b].append(a)
            indegree[a] += 1
        
        q = deque([node for node in range(numCourses) if indegree[node]==0])

        res = []

        while q:
            node = q.popleft()
            res.append(node)

            for nei in adjacency_map[node]:
                indegree[nei] -= 1
                if indegree[nei] == 0:
                    q.append(nei)
        
        return res if len(res) == numCourses else []   
Show More

0

Reply
fz zy
Premium
• 2 months ago
class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]):
        in_degrees = [0] * numCourses
        adj = [[] for _ in range(numCourses)]
        queue = deque([])

        for prerequisite in prerequisites:
            _to, _from = prerequisite
            adj[_from].append(_to)
            in_degrees[_to] += 1

        for i in range(numCourses):
            if not in_degrees[i]:
               queue.append(i)

        ans = []
        while queue:
            size = len(queue)
            for i in range(size):
                node = queue.popleft()
                ans.append(node)
                for neighbor in adj[node]:
                    in_degrees[neighbor] -= 1
                    if not in_degrees[neighbor]:
                        queue.append(neighbor)
        return ans if len(ans) == numCourses else []
Show More

0

Reply
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

Solution

