# Course Schedule

> Source: https://www.hellointerview.com/learn/code/graphs/course-schedule
> Scraped: 2026-03-30



A
AddedLimeCarp593
Top 1%
• 9 months ago

Easier to just build a graph from the input and run dfs from every node checking if a cycle exists.

10

Reply
I
InterestingCoffeeCapybara976
• 1 year ago

There can be situations where the list of courses may not always start from 0. For example, in this input : prerequisites = [[1,4],[2,4],[3,1],[3,2]], we don't even have course 0 , but since we initialised indegreeList for course 0 as 0 ..it will be added to the queue and the execution proceeds in the unexpected way.

Solution : We need to maintain a list of courses fetched from pre-requisites list and only add those courses to the queue.

2

Reply
S
SubjectiveIndigoSkink289
• 4 months ago

Perhaps they fixed it after your comment, but this will not be an issue based on the current problem description:

You have to take a total of numCourses courses, which are labeled from 0 to numCourses - 1

1

Reply
Satya Dasara
Premium
• 2 months ago
• edited 2 months ago

Whenever we hear about dependencies in a graph we should think about topological sort with BFS.

First get all the 0 indegree nodes and remove them from search space and decrement indegree of their neighbors. If new indegree is zero add to queue and continue.

If there is a cycle then count of nodes explored will be less than total number of nodes.
This is because nodes part of a cycle will always have indegree > 0 hence will never get added to BFS queue for exploration.

from collections import deque

class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]):
        indegree = [0]*numCourses
        adjacency_list = { node: set() for node in range(numCourses)}

        for prerequisite in prerequisites:
            a, b = prerequisite
            adjacency_list[a].add(b)
            indegree[b] += 1

        q = deque([i for i in range(numCourses) if indegree[i] == 0])

        count =  0

        while q:
            node = q.popleft()
            count += 1

            for nei in adjacency_list[node]:
                indegree[nei] -= 1
                if indegree[nei] == 0:
                    q.append(nei)
        
        return count == numCourses

Show More

1

Reply
fz zy
Premium
• 2 months ago
class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]):
        adj = [[] for i in range(numCourses)]
        visited, pathVisited = [0] * numCourses, [0] * numCourses
        def dfs(node):
            visited[node] = 1
            pathVisited[node] = 1
            for neighbor in adj[node]:
                if not visited[neighbor]:
                    if not dfs(neighbor):
                        return False
                elif pathVisited[neighbor]:
                        return False
            pathVisited[node] = 0
            return True
        
        for prerequisite in prerequisites:
            adj[prerequisite[1]].append(prerequisite[0])

        for i in range(numCourses):
            if not visited[i] and not dfs(i):
                return False
        
        return True
Show More

0

Reply
J
josemanuelcastaneda
• 3 months ago

Time Complexity may grow to O(V^2) because of the while { for {} }.

Sample: Imagine a sequence of courses where each course is a pre-requisite of all the following courses. This would look like a triangle with surface =  1/2 (V x V)

*Edit: In such case, "E" (number of dependencies), which is also an input, would be 1/2 (V x V), so we could argue time complexity is linear

0

Reply
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

Cycle

Topological Sort

