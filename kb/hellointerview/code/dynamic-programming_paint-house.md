# Paint House

> Source: https://www.hellointerview.com/learn/code/dynamic-programming/paint-house
> Scraped: 2026-03-30


You are a renowned painter who is given a task to paint n houses in a row. You can paint each house with one of three colors: Red, Blue, or Green. The cost of painting each house with each color is different and given in a 2D array costs:

costs[i][0] = cost of painting house i Red
costs[i][1] = cost of painting house i Blue
costs[i][2] = cost of painting house i Green

No two neighboring houses can have the same color. Return the minimum cost to paint all houses.

Constraints:

1 ≤ n ≤ 100
costs[i].length == 3
1 ≤ costs[i][j] ≤ 1000

Example 1

Input:

costs = [[8, 4, 15], [10, 7, 3], [6, 9, 12]]

Output:

13

Explanation:

House 0: Blue (cost = 4)
House 1: Green (cost = 3)
House 2: Red (cost = 6)
Total = 4 + 3 + 6 = 13

Example 2

Input:

costs = [[5, 8, 6], [19, 14, 13], [7, 5, 12], [14, 5, 9]]

Output:

30

Explanation: Red(5) → Green(13) → Red(7) → Blue(5) = 30

CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def min_cost(self, costs: List[List[int]]) -> int:
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
Let's understand the problem through a concrete example. We have 3 houses in a row, and each house can be painted Red, Blue, or Green. Each color has a different cost for each house.
House 0
House 1
House 2
The constraint is simple: no two adjacent houses can have the same color. This means if House 0 is Blue, House 1 must be Red or Green.
✓ Valid
Blue
Green
Blue
Cost: 2 + 5 + 3 = 10
✗ Invalid
Blue
Green
Blue
Adjacent same color!
Approach 1: Brute Force (Try All Colorings)
The most straightforward approach is to try every valid coloring and track the minimum cost. For each house, we have 3 color choices (minus whatever the color we chose for the previous house). We can express this as a recursive function:
minCost(house, prevColor)
    if house == n
        return 0  // painted all houses
    
    result = infinity
    for each color in [Red, Blue, Green]
        if color != prevColor
            result = min(result, costs[house][color] + minCost(house + 1, color))
    
    return result
We start with minCost(0, None) since house 0 has no constraint from a previous house.
This give us the final solution by computing each possibility for a house. But, what's the time complexity? At each house we branch into 2 choices, giving us roughly O(2^n) time. Even for a small group od 100 houses, that's way too slow to compute.
The Problem: Overlapping Subproblems
This is where it gets interesting. Let's trace through a small example with 4 houses:
minCost(0, -)
minCost(1, R)
minCost(1, B)
minCost(1, G)
mc(2, B)
mc(2, G)
mc(2, R)
mc(2, G)
mc(2, R)
mc(2, B)
Duplicates at level 2:
mc(2, G) computed twice
mc(2, B) computed twice
mc(2, R) computed twice
See those highlighted boxes? We're computing the same subproblems multiple times! minCost(2, Green) gets called from two different paths, and so do minCost(2, Blue) and minCost(2, Red). As the tree grows deeper, this redundancy explodes exponentially.
From this observation we can conclude that the state that matters is just the <house index, previous color>. There are only n × 3 = O(n) unique states, but we're computing them exponentially many times.
Approach 2: Top-Down DP (Memoization)
The fix for this is simple, just cache the results. Before computing minCost(house, prevColor), check if we've already solved it. If yes, return the cached answer.
memo = {}

minCost(house, prevColor)
    if house == n
        return 0
    
    if (house, prevColor) in memo
        return memo[(house, prevColor)]
    
    result = infinity
    for each color in [Red, Blue, Green]
        if color != prevColor
            result = min(result, costs[house][color] + minCost(house + 1, color))
    
    memo[(house, prevColor)] = result
    return result
Now each state is computed exactly once. With n houses and 3 colors, we have O(n) unique states, and each takes O(1) work → O(n) time.
This pattern of "recursion + memoization" is called top-down DP. You naturally discover the states by thinking about what information the recursive function needs to make decisions.
Approach 3: Bottom-Up DP
Once you understand the states from top-down thinking, you can flip it around. Instead of starting from house 0 and recursing forward, fill a table starting from the base case.
What state do we need? From the recursive approach, we learned: (house index, color used for that house). So our DP table is:
dp[i][0] = minimum cost to paint houses 0 to i, where house i is painted Red
dp[i][1] = minimum cost to paint houses 0 to i, where house i is painted Blue
dp[i][2] = minimum cost to paint houses 0 to i, where house i is painted Green
House i -1
(some color)
House i
pick different color
To paint house i, we look at house i-1 and choose one of the other two colors
The Recurrence
Since adjacent houses cannot have the same color, if we want to paint house i with a certain color, we must have painted house i - 1 with one of the other two colors.
For example, if we want to paint house i Red, house i - 1 must be Blue or Green:
House i-1
Blue
Green
Red ✗
can't be Red
min()
+
costs[i][Red]
House i
=
dp[i][Red]
dp[i][Red] = costs[i][Red] + min(dp[i-1][Blue], dp[i-1][Green])
To paint house i Red, take the minimum cost from Blue or Green at house i-1, then add the Red cost
This gives us our recurrence:
dp[i][0] = costs[i][0] + min(dp[i-1][1], dp[i-1][2])  # Paint house i Red
dp[i][1] = costs[i][1] + min(dp[i-1][0], dp[i-1][2])  # Paint house i Blue
dp[i][2] = costs[i][2] + min(dp[i-1][0], dp[i-1][1])  # Paint house i Green
Base case: For house 0, there's no previous constraint, so dp[0][color] = costs[0][color].
Answer: min(dp[n-1][0], dp[n-1][1], dp[n-1][2])
Walkthrough
Let's trace through the example costs = [[17, 2, 17], [16, 16, 5], [14, 3, 19]]:
House 0 (Base Case):
Red: 17, Blue: 2, Green: 17
House 1:
Red: 16 + min(2, 17) = 16 + 2 = 18
Blue: 16 + min(17, 17) = 16 + 17 = 33
Green: 5 + min(17, 2) = 5 + 2 = 7
House 2:
Red: 14 + min(33, 7) = 14 + 7 = 21
Blue: 3 + min(18, 7) = 3 + 7 = 10
Green: 19 + min(18, 33) = 19 + 18 = 37
Answer: min(21, 10, 37) = 10
The optimal choice is: House 0 → Blue (2), House 1 → Green (5), House 2 → Blue (3) = 10
VISUALIZATION
Python
Language
Full Screen
def min_cost(costs):
    if not costs:
        return 0
    
    n = len(costs)
    dp = [[0] * 3 for _ in range(n)]
    
    # Base case: first house
    dp[0][0] = costs[0][0]  # Red
    dp[0][1] = costs[0][1]  # Blue
    dp[0][2] = costs[0][2]  # Green
    
    # Fill DP table
    for i in range(1, n):
        dp[i][0] = costs[i][0] + min(dp[i-1][1], dp[i-1][2])
        dp[i][1] = costs[i][1] + min(dp[i-1][0], dp[i-1][2])
        dp[i][2] = costs[i][2] + min(dp[i-1][0], dp[i-1][1])
    
    return min(dp[n-1][0], dp[n-1][1], dp[n-1][2])
2D DP Table Approach
dp[i][j]
Red (j=0)
Blue (j=1)
Green (j=2)
Input costs[i]
i=0
0
0
0
[17, 2, 17]
i=1
0
0
0
[16, 16, 5]
i=2
0
0
0
[14, 3, 19]

paint house - 2D DP approach

0 / 11

1x
2D DP table filling - O(n) space
Space Optimization
Notice that to compute dp[i], we only need values from dp[i-1]. This means we don't need to store the entire 2D array - we can just keep track of the previous row's values.
Instead of a 2D array, we can use just 3 variables to track the minimum costs for each color at the previous house. This reduces space from O(n) to O(1).
This space optimization pattern is common in DP problems where the current state only depends on the immediately previous state.
Solution
The space-optimized solution uses only 3 variables (prevRed, prevBlue, prevGreen) instead of a full 2D table. For each house, we calculate the new costs and then update our variables.
costs
​
|
costs
2D array: [[R,B,G], ...]
Try these examples:
One House
Two Houses
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def min_cost(costs):
    if not costs:
        return 0
    
    prev_red = costs[0][0]
    prev_blue = costs[0][1]
    prev_green = costs[0][2]
    
    for i in range(1, len(costs)):
        curr_red = costs[i][0] + min(prev_blue, prev_green)
        curr_blue = costs[i][1] + min(prev_red, prev_green)
        curr_green = costs[i][2] + min(prev_red, prev_blue)
        
        prev_red = curr_red
        prev_blue = curr_blue
        prev_green = curr_green
    
    return min(prev_red, prev_blue, prev_green)
Space-Optimized Paint House
Houses
0
1
2
Input Costs
Red
Blue
Green
17
2
17
16
16
5
14
3
19
Cumulative
Red
17
Blue
2
Green
17

paint house

0 / 12

1x
Space-optimized solution - O(1) space
What is the time complexity of this solution?
1

O(n log n)

2

O(n)

3

O(m * n)

4

O(4^L)

Mark as read

Next: Paint House II

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

(6)

Comment
Anonymous
xiaoxiao liu
Premium
• 2 months ago

It’s often not intuitive to derive the DP recurrence directly. I usually start with a top-down DFS + memo to clarify the states and transitions, then convert it to bottom-up, and finally refine it into a prefix DP as the final solution.

3

Reply
Haris Osmanagić
Premium
• 2 months ago

Great article, as always! Thanks for the graphics and the very detailed explanation.

There's one thing I'd generally suggest (not only here, but actually anywhere where these problems appear), and that is to use a bit more natural inputs, like describing colors with strings ("red", "blue", "green"). It makes the problems easier to work with, and that's how we'd write production code anyway.:)

2

Reply
A
AcuteLavenderBug994
Premium
• 1 month ago

My Swift O(n) solution

func minCostToPaintAllHouses(arr: [[Int]]) -> Int {
    var map:[String:Int] = [:]
    return min(min(minCostToPaintAllHouses_helper(houseIdx: 0, colorIdx: 0, arr: arr, map: &map), minCostToPaintAllHouses_helper(houseIdx: 0, colorIdx: 1, arr: arr, map: &map)), minCostToPaintAllHouses_helper(houseIdx: 0, colorIdx: 2, arr: arr, map: &map))
}

func minCostToPaintAllHouses_helper(houseIdx: Int, colorIdx: Int, arr: [[Int]], map: inout [String:Int]) -> Int {
    if houseIdx == arr.count {
        return 0
    }
    let mapIdx = String(houseIdx) + String(colorIdx)
    if let x = map[mapIdx] {
        return x
    }
    var nextcolorIdx1 = 0, nextcolorIdx2 = 0
    if colorIdx == 0 {
        nextcolorIdx1 = 1
        nextcolorIdx2 = 2
    } else if colorIdx == 1 {
        nextcolorIdx1 = 0
        nextcolorIdx2 = 2
    } else {
        nextcolorIdx1 = 0
        nextcolorIdx2 = 1
    }
    let y = arr[houseIdx][colorIdx] + min(minCostToPaintAllHouses_helper(houseIdx: houseIdx + 1, colorIdx: nextcolorIdx1, arr: arr, map: &map),  minCostToPaintAllHouses_helper(houseIdx: houseIdx + 1, colorIdx: nextcolorIdx2, arr: arr, map: &map))
    map[mapIdx] = y
    return y
}

Show More

0

Reply
M
MeltedAmberPiranha299
Top 10%
• 2 months ago

Top-down approach:

class Solution:
    def min_cost(self, costs: List[List[int]]):
        if not costs:
            return 0
        COLORS = [0, 1, 2]
        memo = {}
        def dp(i, prev):
            if i >= len(costs):
                return 0
            if (i, prev) in memo:
                return memo[(i, prev)]
            best = min(costs[i][c] + dp(i + 1, c) for c in COLORS if c != prev)
            memo[(i, prev)] = best
            return memo[(i, prev)]
        return dp(0, -1)

0

Reply

Comments specific to prior versions of this article

brave warrior
Premium
• 2 months ago

In the description, second example explanation is wrong - costs = [[5, 8, 6], [19, 14, 13], [7, 5, 12], [14, 5, 9]].

Correct explanation : Red (5) -> Green (13) -> red (7) -> blue (5) so the total will be 30 not 31.

1

Reply
Expand Old Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

Building Intuition

Approach 1: Brute Force (Try All Colorings)

The Problem: Overlapping Subproblems

Approach 2: Top-Down DP (Memoization)

Approach 3: Bottom-Up DP

The Recurrence

Walkthrough

Space Optimization

Solution
