# Adjacency List

> Source: https://www.hellointerview.com/learn/code/depth-first-search/adjacency-list
> Scraped: 2026-03-30



​
Sort By
Popular
Sort By
Sayan Sarkar
Top 10%
• 7 months ago

I think Java implementation is not correct. You are calling a method from inside another method. This will not compile.

    void dfsHelper(int node) {

is inside of

public void dfs(Map<Integer, List<Integer>> adjList) {


13

Reply
Y
yanniel.alvarez
Premium
• 7 months ago

You are right, Sayan. It is not correct. Java does not allow declaring a method directly inside another method as done in this example. I have seen this mistake in other places in Hello Interview, so I wonder if it is a direct translation of the Python code.

2

Reply
R
RetiredPinkFelidae839
Premium
• 9 months ago

FIX:
As pointed out by others:

dfs_helper(adjList[0]) should be

 first_node = next(iter(adjList))
 dfs_helper(first_node)

Also, if its a disconnected graph something like this would work

for node in adjList:
        if node not in visited:
            dfs_helper(node)

2

Reply
Shivam Chauhan
• 9 months ago

Hi thanks, this is fixed!

0

Reply
Benjamin Teo
Premium
• 10 days ago

I don't see it fixed, the helper is still being called inside of the dfs method.

0

Reply
U
UpperEmeraldSkink457
Premium
• 1 year ago

In DFS on an Adjacency List, we call dfs_helper(adjList[0]) to start the DFS. Shouldn't the parameter be a node? Isn't adjList a dictionary, and 0 might not even be a key? Should it be something like dfs_helper(adjList[1][0]) instead?

2

Reply
S
SpecialYellowNightingale688
• 10 months ago

yeah -- in this example, adjList[0] is the dictionary key-value entry "1": ["2", "4"]. I think instead you should have something like adjList.keys()[0]

0

Reply
Du Zheng
• 1 year ago

The keys of the adjacency list are the values of the nodes, and the values are the neighbors of the nodes.

dfs_helper(adjList[0]) means start from node '1' in the animation.

0

Reply
I
InvisibleAmaranthBee655
• 11 months ago

But dfs_helper(adjList[0]) would fail. It should updated to adjList['1'] instead looking at the adjList that is defined above.

1

Reply
Shubham Sharma
Top 10%
• 10 months ago

In case of a disconnected graph, just doing  dfs_helper(adjList[0]) won't help. You'll have to iterate over the entire list of nodes and call dfs_helper

1

Reply
Shivam Chauhan
• 9 months ago

Hi thanks, this is fixed!

0

Reply
R
ReasonableWhiteDragonfly506
• 11 months ago

dfs_helper(0) should be correct input here as fds_helper(map[0]) will put list in visited not the node:
Corrected version is below

def dfs(map_):
  if not map_:
    return
  visited = set()
  def dfs_heler(node):
    if node in visited:
      return
    visited.add(node)
    print(node, end=" ")
    for n in map_[node]:
      dfs_heler(n)
    return
  dfs_heler(0)
dfs(map_)

1

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

