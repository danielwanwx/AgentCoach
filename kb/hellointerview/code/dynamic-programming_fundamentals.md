# Dynamic Programming Fundamentals

> Source: https://www.hellointerview.com/learn/code/dynamic-programming/fundamentals
> Scraped: 2026-03-30

Dynamic Programming Fundamentals
5:43
11 chapters • 2 interactive checkpoints
In this section, we'll learn about dynamic programming by looking at a classic dynamic programming problem. We'll start with the brute-force solution and gradually optimize it using key dynamic programming concepts.
Climbing Stairs
DESCRIPTION (inspired by Leetcode.com)
You can climb a staircase by taking either 1 or 2 steps at a time. If there are n steps in the staircase, how many distinct ways are there to climb to the top step?
Example
n = 3
Output: 3
1st way: 1 step + 1 step + 1 step
2nd way: 1 step + 2 steps
3rd way: 2 steps + 1 step
Brute-Force Solution
The brute-force solution to this problem tries every possible combination of 1 or 2 steps to climb the stairs and counts the ones that successfully reach the top step.
We can visualize that process as a tree, where each node represents a choice of either 1 or 2 steps, and each root-to-leaf path represents a different combination of steps to climb the stairs.
For example, there are 3 ways to climb 3 steps: (1 + 1 + 1, 1 + 2, 2 + 1)
1
1
1
2
2
1
This tree gets big pretty quickly. For example, when n = 5:
1
1
1
1
1
2
2
1
2
1
1
2
2
1
1
1
2
2
1
The 8 different ways to climb 5 steps are shown by the root-to-leaf paths.
We can implement this brute-force solution using recursion. Each call to climbStairs(n - 1) and climbStairs(n - 2) represents a choice of taking 1 or 2 steps, respectively.
SOLUTION
Python
Language
def climbStairs(n):
    # base cases
    if n <= 1:
        return 1
    
    return climbStairs(n - 1) + climbStairs(n - 2)
This recursive function is an example of a backtracking algorithm that solves a problem by generating all possible combinations.
The call tree for this recursive function looks like the tree above. In the call tree below, each node represents a call to climbStairs(n), starting from climbStairs(5) (labeled s(n) for short):
s(5)
s(4)
s(3)
s(2)
s(1)
s(0)
s(1)
s(2)
s(1)
s(0)
s(3)
s(2)
s(1)
s(0)
s(1)
The most glaring issue with this approach is that it is very inefficient. The time complexity is O(2n) as each call to climbStairs(n) results in two more calls to climbStairs(n - 1) and climbStairs(n - 2). This leads to an exponential number of calls and makes the solution very slow for large values of n.
The call tree is a useful starting point for understanding two dynamic programming concepts: overlapping subproblems and optimal substructure.
Optimal Substructure
We can think of optimal substructure as a fancy way of saying we can use recursion to solve the problem.
More formally, the problem has optimal substructure if an optimal solution to the problem contains optimal solutions to subproblems.
For this problem, if we know:
the number of ways to climb 3 steps
the number of ways to climb 4 steps
Then, we can add those together to get the number of ways to climb 5 steps.
The number of ways to climb 3 and 4 steps represent the optimal solutions to the subproblems.
1
2
3
4
5
Visualizing the optimal substructure property. If we know climbStairs(3) and climbStairs(4), then we also know climbStairs(5).
Overlapping Subproblems
The call tree makes it easy to see that the brute-force solution has overlapping subproblems, which is a fancy way of saying there is repeat work being done.
For example, climbStairs(3) is called twice. Each of those calls then results in the same exact sequence of recursive calls to climbStairs(1) and climbStairs(2).
s(5)
s(4)
s(3)
s(2)
s(1)
s(0)
s(1)
s(2)
s(1)
s(0)
s(3)
s(2)
s(1)
s(0)
s(1)
The repeat calls to climbStairs(3) are shown in gray.
So, if a problem has optimal substructure (it can be solved using recursion), and there are overlapping subproblems (the same recursive call is made multiple times), then we can use dynamic programming to handle the overlapping subproblems more efficiently.
There are two strategies for doing so, but they both boil down to the same idea: only solve each subproblem once.
Memoization
The first strategy is known as memoization.
Let's return to the call tree. It shows that climbStairs(3) is called once by climbStairs(4), and later on by climbStairs(5).
Since the result of climbStairs(3) won't change between these two calls, we can store the result of climbStairs(3) in a "cache". When climbStairs(5) needs to calculate climbStairs(3) again, we can simply look up the result in the cache instead of recalculating it, eliminating a series of redundant recursive calls. This is known as memoization.
Here's the same call tree with memoization applied. The nodes that have been memoized are highlighted in green. Notice how they return immediately without expanding to make any further recursive calls.
s(5)
s(4)
s(3)
s(3)
s(2)
s(2)
s(1)
s(1)
s(0)
The savings from memoization become more visible as n grows larger. Take n = 6 for example. The calls that are memoized are highlighted in green, and the calls that get skipped are grayed out.
s(6)
s(5)
s(4)
s(3)
s(2)
s(1)
s(0)
s(1)
s(2)
s(1)
s(0)
s(3)
s(2)
s(1)
s(0)
s(1)
s(4)
s(3)
s(2)
s(1)
s(0)
s(1)
s(2)
s(1)
s(0)
We can add memoization by taking our brute-force recursive solution and adding a dictionary memo. Memo maps n to the result of climbStairs(n), and serves as our cache. We need to remember to do two things when adding memoization:
Before making a recursive call, we check if the value for n is already in the cache. If it is, we return the value immediately without making any further recursive calls.
After obtaining the result for n, we store it in the cache before returning it to the caller.
SOLUTION
Python
Language
def climbStairs(n: int) -> int:
    memo = {}
    
    def climb_helper(i: int) -> int:
        if i <= 1:
            return 1
        
        # check if value is already in cache
        # before making recursive calls
        # corresponds to the green nodes in the diagram
        if i in memo:
            return memo[i]
        
        # store result in cache before returning
        memo[i] = climb_helper(i - 1) + climb_helper(i - 2)
        return memo[i]
    
    return climb_helper(n)
Adding memoization to our solution reduces the time complexity from O(2n) to O(n). As we can see in the memoized call tree, each subproblem is solved once and then stored in the cache, and future recursive calls to the same subproblem are looked up in O(1) time. The space complexity is also O(n) because we store the result of each value in the cache.
Bottom-Up Approach
The recursive approach with memoization is known as the top-down approach to dynamic programming. The call tree starts with the original problem and works its way down to the base cases.
There's an alternative approach to dynamic programming known as the bottom-up approach, which is based on the following observation: we already know the base cases of our problem, namely that there is 1 way to climb 0 steps and 1 way to climb 1 step.
SOLUTION
Python
Language
climbStairs(0) = 1
climbStairs(1) = 1
This is enough to calculate the number of ways to climb 2 steps:
SOLUTION
Python
Language
climbStairs(2) = climbStairs(1) + climbStairs(0) # 1 + 1 = 2
And now that climbStairs(2) is known, we can calculate climbStairs(3):
SOLUTION
Python
Language
climbStairs(3) = climbStairs(2) + climbStairs(1) # 2 + 1 = 3
which continues until we reach climbStairs(n), where n is the original value.
We can visualize this process as starting from the leaf nodes of the memoized call-tree and working up to the root node, shown below for n = 5.
VISUALIZATION
Full Screen
s(5)
s(4)
s(3)
s(3)
s(2)
s(2)
s(1)
s(1)
s(0)

bottom up

0 / 4

2x
But we can't use recursion to implement the bottom-up approach because we need to start from the base cases and work our way up.
Implementing the Bottom-Up Approach
The bottom-up approach starts by creating an array dp of size n + 1 to store the number of ways to climb n steps. dp[0] contains the number of ways to climb 0 steps, dp[1] contains the number of ways to climb 1 step, and so on. This dp array is analogous to the cache we used in the memoized recursive approach.
We initialize the base cases dp[0] = 1 and dp[1] = 1, and then iterate from 2 to n, calculating dp[i] = dp[i - 1] + dp[i - 2]. The animation below shows the process of filling in the dp array for n = 5, and how it corresponds to going from the bottom of the memoized call tree to the top. When the iteration is complete, we return dp[n] as the final answer.
VISUALIZATION
Full Screen
s(5)
s(4)
s(3)
s(3)
s(2)
s(2)
s(1)
s(1)
s(0)
s(5)
s(4)
s(3)
s(3)
s(2)
s(2)
s(1)
s(1)
s(0)
0
1
2
3
4
5

0 / 6

2x
Here's what that looks like in code:
SOLUTION
Python
Language
def stairs(n):
    if n <= 1:
        return 1
    dp = [0] * (n + 1)

    dp[0] = 1
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]
Time And Space Complexity
Time Complexity: This approach has a time complexity of O(n) because we iterate from 2 to n to calculate the number of ways to climb n steps. Each iteration takes O(1) time.
Space Complexity: The space complexity is also O(n) because we use an array of size n + 1 to store the number of ways to climb n steps.
Space Optimization
Take another look at the loop body: dp[i] = dp[i - 1] + dp[i - 2]. At each step, we only ever read the two most recent values. We never go back and look at dp[i - 3] or anything earlier. That means we're paying for a whole array when two variables would do.
Instead of maintaining the full dp array, we can keep just two variables, prev1 and prev2, that track the previous two results. After computing the current value, we shift them forward. This drops the space complexity from O(n) to O(1) while keeping the same O(n) time complexity.
SOLUTION
Python
Language
def stairs(n):
    if n <= 1:
        return 1

    prev2 = 1
    prev1 = 1
    for i in range(2, n + 1):
        curr = prev1 + prev2
        prev2 = prev1
        prev1 = curr
    return prev1
This is a common optimization pattern in dynamic programming: whenever your recurrence only depends on a fixed number of previous states, you can replace the array with that many variables.
Summary
Both the top-down and bottom-up approaches are valid ways to solve problems by avoiding redundant calculations. The top-down approach uses recursion and memoization to store the results of subproblems, while the bottom-up approach iterates from the base cases to the original problem.
The top-down approach is often more intuitive to those who are first learning dynamic programming, but the bottom-up approach is generally more efficient because it avoids the overhead of recursive calls and function calls. In the next section, we'll build upon these concepts and follow a structured approach to solve dynamic programming problems.

Mark as read

Next: Solving a Question with Dynamic Programming

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

(27)

Comment
Anonymous
​
Sort By
Popular
Sort By
J
jamesgold
Top 1%
• 9 months ago

I think you can get the space complexity down to O(1) because when calculating the nth value you only need to know the values at n-1 and n-2, not all the values 0...n.

16

Reply
Aman Rawat
Premium
• 1 month ago

i was so into the article - i didn't noticed that xD

0

Reply
saurabh vaidya
• 6 months ago

While I get the intuition, in the bottom up approach I cannot wrap my head around base case where we assume

climbStairs(0) = 1

Aren't there 0 ways to climb 0 steps ?

8

Reply
G
gaastonsr
Premium
• 6 months ago

Good question, I struggled with this one too. The intuition is not that there is 1 way to climb 0 steps, it is that when there are 0 steps to climb, you found 1 solution. The same when there is 1 step to climb, you also found 1 solution because there is only one way to climb 1 step.

8

Reply
A
AmazingIndigoCaribou141
Top 10%
• 4 months ago

It's like the permutation problem - 0! = 1, as there is 1 way to permute a set of 0 object (that way is - drumroll.... by not permuting any)

Similarly, if we have no stairs, we have 1 way to climb it (by not climbing it)

6

Reply
Haris Osmanagić
Premium
• 3 months ago

Alternatively, you define the base cases as climbStairs(1) and climbStairs(2).

0

Reply
I
IntellectualJadePrawn323
Premium
• 8 months ago

i wish someone explained DP to me like this in college

4

Reply
V
vinothj23
• 1 month ago

This is the cleanest explanation I have read about Dynamic Programming.

Love your work!

2

Reply
JP
Jai P
• 13 days ago

Video explanation covered whole topic in just 5 minutes , this is brilliant !! Thanks for making such a great content freemium.

1

Reply

Stefan Mai

Admin
• 13 days ago

Tell your friends :)

1

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Climbing Stairs

Brute-Force Solution

Optimal Substructure

Overlapping Subproblems

Memoization

Bottom-Up Approach

Summary