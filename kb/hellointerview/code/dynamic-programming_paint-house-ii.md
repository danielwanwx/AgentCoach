# Paint House II

> Source: https://www.hellointerview.com/learn/code/dynamic-programming/paint-house-ii
> Scraped: 2026-03-30


You are a renowned painter who is given a task to paint n houses in a row. This time, you have k colors available. The cost of painting each house with each color is different and given in a 2D array costs:

costs[i][j] = cost of painting house i with color j

No two neighboring houses can have the same color. Return the minimum cost to paint all houses.

Constraints:

1 ≤ n ≤ 100
1 ≤ k ≤ 20
costs[i].length == k
1 ≤ costs[i][j] ≤ 1000

Follow-up: Can you solve this in O(n × k) time instead of the naive O(n × k²)?

Example 1

Input:

costs = [[4, 2, 8], [7, 1, 5], [3, 9, 6]]

Output:

8

Explanation:

House 0: Color 0 (cost = 4)
House 1: Color 1 (cost = 1)
House 2: Color 0 (cost = 3)
Total = 4 + 1 + 3 = 8

Example 2

Input:

costs = [[8, 3, 12, 5], [15, 9, 4, 7]]

Output:

7

Explanation: Paint house 0 with color 1 (cost = 3), house 1 with color 2 (cost = 4). Total = 7.

CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def min_cost_ii(self, costs: List[List[int]]) -> int:
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
Building Intuition
This problem is a direct extension of Paint House. If you haven't solved that one yet, start there first since this builds on those concepts.
The setup is the same: paint n houses in a row where no two adjacent houses can share a color. But, instead of just 3 colors, we now have k colors to choose from.
House i
k color options
0
1
2
3
...
k-1
Pick any color ≠ house i-1's color
At first glance, you might think: "I already know how to solve Paint House, I'll just extend that solution." And you'd be right to start there. But there's a catch that makes this problem more interesting.
Approach 1: Direct Extension of Paint House
In Paint House with 3 colors, we defined dp[i][j] as the minimum cost to paint houses 0 through i, where house i uses color j. The recurrence was straightforward:
dp[i][j] = costs[i][j] + min(dp[i-1][m] for all m != j)
With 3 colors, finding "the minimum of all colors except j" meant checking just 2 values. That's O(1) per cell, giving us O(n × 3) = O(n) total time.
But what happens when we scale to k colors?
For each of the k colors at each house, we need to find the minimum among k-1 previous values. That's O(k) work per color, times k colors, times n houses: O(n × k²).
The Problem is that O(n × k²) is too slow. When k = 1000, we're doing ~1 billion operations per house!
The question becomes: can we find "minimum of all except j" faster than scanning all k values every time?
The Key Insight
Let's think about what "minimum of all colors except j" actually means. Suppose we have these values from the previous row:
prev[i-1]:
5
min1 ★
9
7
min2
12
8
[5, 9, 7, 12, 8]
Now, think "what's the minimum excluding index j?", there are really only two scenarios:
Scenario 1: If j is NOT the index of the smallest value (j ≠ 0 in this case), then the minimum excluding j is just... the smallest value! We're excluding something that wasn't the minimum anyway.
Scenario 2: If j IS the index of the smallest value (j = 0 here), then we can't use that value. The next best option? The second smallest value.
If j ≠ min1's index
Answer = min1 = 5
If j = min1's index
Answer = min2 = 7
Track just 3 values: min1, min2, and min1's index
Instead of scanning all k values every time, we precompute the two smallest values from the previous row. Then answering "minimum excluding j" becomes O(1)
Naive: O(n × k²)
Scan all k values for
each of k colors
Optimized: O(n × k)
O(1) lookup using
min1/min2
Approach 2: Optimized DP with Min Tracking
Here's the optimized algorithm:
Initialize with the first row's costs. Find min1, min2, and min1Idx from this row.
For each subsequent house, compute new values:
For color j: new[j] = costs[i][j] + (j == min1Idx ? min2 : min1)
Track new min1, min2, min1Idx as we go
Return the minimum value in the final row.
The recurrence in code form:
minCost(i, j)
    if j == min1Idx
        return costs[i][j] + min2
    else
        return costs[i][j] + min1
This gives us O(n × k) time because we do O(k) work per house (computing k new values and finding the new min1/min2), and we have n houses.
Walkthrough
Let's trace through a concrete example to see how this works in practice. We'll use costs = [[1, 5, 3], [2, 9, 4], [8, 1, 6], [4, 2, 3]] with 4 houses and 3 colors.
Step 1: Initialize with House 0
For the first house, we simply copy the costs. There's no previous house to consider.
House 0:
1
min1 ★
5
3
min2
prev = [1, 5, 3]
min1 = 1 (at index 0)
min2 = 3
We scan through and find: min1 = 1 (at index 0), min2 = 3. These values will determine what each color at house 1 adds to its cost.
Step 2: Process House 1
Now the optimization kicks in. For each color j at house 1:
If j = 0 (the min1 index), we must use min2 = 3
Otherwise, we use min1 = 1
House 1:
cost[1] + best from prev
5
2 + min2(3)
10
9 + min1(1)
5
4 + min1(1)
j=0: uses min2 (can't use min1)
j=1: uses min1
j=2: uses min1
New: prev = [5, 10, 5]
min1 = 5 (index 0), min2 = 5
Notice color 0's calculation: we can't use min1 (since min1 came from color 0 in the previous row), so we fall back to min2.
Step 3: Process House 2
House 2:
13
8 + min2(5)
6
1 + min1(5) ★
11
6 + min1(5)
New: prev = [13, 6, 11]
min1 = 6 (index 1)
min2 = 11
Step 4: Process House 3 (Final)
House 3:
10
4 + min1(6)
13
2 + min2(11)
9
3 + min1(6) ★
Final: min(10, 13, 9)
Answer: 9
The minimum cost to paint all 4 houses is 9, achieved by painting them: Color 0 → Color 2 → Color 1 → Color 2.
The min1/min2 tracking pattern shows up frequently! Whenever you need "minimum excluding current index" efficiently, this approach reduces O(k) lookup to O(1).
Solution
The visualization below shows the optimized algorithm in action. Watch how we track min1, min2, and min1Idx after each row, and how those values determine the additions for the next row.
costs
​
|
costs
2D array: [[c0,c1,...], ...]
Try these examples:
Two Houses
Three Colors
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def min_cost_ii(costs):
    if not costs:
        return 0
    
    n, k = len(costs), len(costs[0])
    prev = costs[0][:]
    
    for i in range(1, n):
        min1, min2, min1_idx = float('inf'), float('inf'), -1
        for j in range(k):
            if prev[j] < min1:
                min2, min1, min1_idx = min1, prev[j], j
            elif prev[j] < min2:
                min2 = prev[j]
        
        curr = [0] * k
        for j in range(k):
            if j == min1_idx:
                curr[j] = costs[i][j] + min2
            else:
                curr[j] = costs[i][j] + min1
        prev = curr
    
    return min(prev)
Paint House II (k colors)
costs[i][j]
R
B
G
0
1
5
3
1
2
9
4
2
8
1
6
3
4
2
3
prev[]
1
5
3

Paint House II: minimize cost with k colors

0 / 20

1x
O(n×k) solution using min tracking
What is the time complexity of this solution?
1

O(x * y)

2

O(n × k)

3

O(log m * n)

4

O(4^L)

Why Not O(1) Space Like Paint House?
In the original Paint House with 3 colors, we optimized space from O(n) to O(1) by keeping just 3 variables instead of the full array. You might wonder: can we do the same here?
Unfortunately, no. With k colors, we need to store all k previous values because we're computing k new values simultaneously. Each new value needs to know which index had the minimum in the previous row, and we can't overwrite values we still need.
O(k) space is still much better than the naive O(n × k) space from storing the full 2D table.

Mark as read

Next: Minimum Window Subsequence

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
fz zy
Premium
• 2 months ago
class Solution:
    def min_cost_ii(self, costs: List[List[int]]):
        min1, min2, min_idx = 0, 0, -1
        for cost in costs:
            next_min1 = next_min2 = float("inf")
            next_idx = -1
            for idx, val in enumerate(cost):
                next_min = float("inf")
                if idx != min_idx:
                    next_min = min1 + val
                else:
                    next_min = min2 + val
                if next_min < next_min1:
                    next_min2 = next_min1
                    next_min1 = next_min
                    next_idx = idx
                    continue
                next_min2 = min(next_min2, next_min)
            min1, min2, min_idx = next_min1, next_min2, next_idx
        return min1
Show More

2

Reply
F
FascinatingAmethystMarsupial369
Top 1%
• 2 months ago

The problem "1289. Minimum Falling Path Sum 2" is the same problem and same solution works. Might be good to have a similar problems section at the end of the problem.

Also there is a O(1) solution for this problem as a commentor posted, so would be good to have it included here. If this gets asked at Meta, you bet they would expect the O(1) solution

1

Reply
Michael
Premium
• 24 days ago
• edited 24 days ago

well we can still use O(1) space, since we only need to track preSecMinCost, preMinCost with preColor.

   public int min_cost_ii(int[][] costs) {
        if (costs == null || costs.length == 0 || costs[0].length == 0)  {
            return 0;
        }

        int m = costs.length;
        int k = costs[0].length;
        if (k == 1) {
            return m == 1 ? costs[0][0] : -1;
        }
        int preMinCost = 0;
        int preSecMinCost = 0;
        int preColor = -1;
        for (int i = 0; i < m; i++) {
            int curMinCost = Integer.MAX_VALUE;
            int curSecMinCost = Integer.MAX_VALUE;
            int curColor = -1;
            for (int j = 0; j < k; j++) {
                int cost = costs[i][j] + (j == preColor ? preSecMinCost : preMinCost);
                if (cost < curMinCost) {
                    curSecMinCost = curMinCost;
                    curMinCost = cost;
                    curColor = j;
                } else if (cost < curSecMinCost) {
                    curSecMinCost = cost;
                }
            }
            preMinCost = curMinCost;
            preSecMinCost = curSecMinCost;
            preColor = curColor;
        }
        return preMinCost;
    }
Show More

0

Reply
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

Building Intuition

Approach 1: Direct Extension of Paint House

The Key Insight

Approach 2: Optimized DP with Min Tracking

Walkthrough

Solution

Why Not O(1) Space Like Paint House?
