# Gas Station

> Source: https://www.hellointerview.com/learn/code/greedy/gas-station
> Scraped: 2026-03-30


There are n gas stations along a circular route. You are given two integer arrays gas and cost of length n. At each gas station i, gas[i] represents the amount of gas you receive by stopping at this station, and cost[i] represents the amount of gas required to travel from station i to the next station. You begin the journey with an empty tank at one of the gas stations.

Write a function to return the starting gas station's index if you can travel around the circuit once in the clockwise direction; otherwise, return -1. Note that if there exists a solution, it is guaranteed to be unique. Also, you can only travel from station i to station i + 1, and the last station will lead back to the first station.

Input:

gas = [5,2,0,3,3]
cost = [1,5,5,1,1]

Output:

3

Explanation:

Start at station 4 (index 3) and fill up with 3 units of gas. Your tank = 0 + 3 = 3 Travel to station 4 with 1 unit of gas, and fill up with 3 units of gas. Your tank = 3 - 1 + 3 = 5 Travel to station 0 with 1 unit of gas, and fill up with 5 units of gas. Your tank = 5 - 1 + 5 = 9 Travel to station 1 with 5 units of gas, and fill up with 2 units of gas. Your tank = 9 - 5 + 2 = 6 Travel to station 2 with 5 units of gas, and fill up with 0 units of gas. Your tank = 6 - 5 + 0 = 1 Travel back to station 3 with 1 unit of gas to complete the circuit. Therefore, return 3 as the starting index.

CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
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

Solution
gas
​
|
gas
list of integers
cost
​
|
cost
list of integers
Try these examples:
No Solution
Wrap Around
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def canCompleteCircuit(gas, cost):
    if sum(gas) < sum(cost):
        return -1
    
    start, fuel = 0, 0
    for i in range(len(gas)):
        if fuel + gas[i] - cost[i] < 0:
            # can't reach next station:
            # try starting from next station
            start, fuel = i + 1, 0
        else:
            # can reach next station:
            # update remaining fuel
            fuel += gas[i] - cost[i]
    
    return start
5
2
0
3
3
1
5
5
1
1

gas station

0 / 12

1x
Explanation
If there is more gas along the route than the cost of the route, then there is guaranteed to be a solution to the problem. So the first step is to check if the sum of the gas is greater than or equal to the sum of the cost. If it is not, then we return -1.
Next, we iterate through the gas station to find the starting index of our circuit using a greedy approach: whenever we don't have enough gas to reach the next station, we move our starting gas station to the next station and reset our gas tank.
Walkthrough
We start at the first station, and fill our tank with gas[0] = 5 units of gas. From there, it takes cost[0] = 1 units of gas to travel to the next station, so we arrive at station 2 (index 1) with 4 units of gas.
VISUALIZATION
Python
Language
Full Screen
def canCompleteCircuit(gas, cost):
    if sum(gas) < sum(cost):
        return -1
    
    start, fuel = 0, 0
    for i in range(len(gas)):
        if fuel + gas[i] - cost[i] < 0:
            # can't reach next station:
            # try starting from next station
            start, fuel = i + 1, 0
        else:
            # can reach next station:
            # update remaining fuel
            fuel += gas[i] - cost[i]
    
    return start
5
2
0
3
3
start = 0
i = 0
1
5
5
1
1
fuel
0

i = 0

0 / 2

1x
Traveling between stations 1 (`i = 0`) and 2 (`i = 2`)
At station 2, we fill our tank with gas[1] = 2 units of gas, for a total of 6 units of gas. It takes cost[1] = 5 units of gas to travel to the next station, so we arrive at station 3 with 1 unit of gas.
VISUALIZATION
Python
Language
Full Screen
def canCompleteCircuit(gas, cost):
    if sum(gas) < sum(cost):
        return -1
    
    start, fuel = 0, 0
    for i in range(len(gas)):
        if fuel + gas[i] - cost[i] < 0:
            # can't reach next station:
            # try starting from next station
            start, fuel = i + 1, 0
        else:
            # can reach next station:
            # update remaining fuel
            fuel += gas[i] - cost[i]
    
    return start
5
2
0
3
3
start = 0
i = 1
1
5
5
1
1
fuel
4

i = 1

0 / 2

1x
Traveling between stations 2 (`i = 1`) and 3 (`i = 2`)
Greedy Approach
Now at station 3, we fill our tank with gas[2] = 0 units of gas, for a total of 1 unit of gas. It takes cost[2] = 5 units of gas to travel to the next station, which we don't have.
This is where our greedy approach comes in. We reset our starting station to the next station i + 1 and reset our gas tank to 0. We can do this because all other start indexes between 0 and 2 will also run into the same problem of not having enough gas to reach the next station, so we can rule them out.
VISUALIZATION
Python
Language
Full Screen
def canCompleteCircuit(gas, cost):
    if sum(gas) < sum(cost):
        return -1
    
    start, fuel = 0, 0
    for i in range(len(gas)):
        if fuel + gas[i] - cost[i] < 0:
            # can't reach next station:
            # try starting from next station
            start, fuel = i + 1, 0
        else:
            # can reach next station:
            # update remaining fuel
            fuel += gas[i] - cost[i]
    
    return start
5
2
0
3
3
start = 0
i = 2
1
5
5
1
1
fuel
1

i = 2

0 / 2

1x
Resetting the start index
If we follow this approach of resetting the start index and gas tank whenever we don't have enough gas to reach the next station, then when we finish iterating, the last start index will be the solution to the problem.
VISUALIZATION
Python
Language
Full Screen
def canCompleteCircuit(gas, cost):
    if sum(gas) < sum(cost):
        return -1
    
    start, fuel = 0, 0
    for i in range(len(gas)):
        if fuel + gas[i] - cost[i] < 0:
            # can't reach next station:
            # try starting from next station
            start, fuel = i + 1, 0
        else:
            # can reach next station:
            # update remaining fuel
            fuel += gas[i] - cost[i]
    
    return start
5
2
0
3
3
start = 3
i = 3
1
5
5
1
1
fuel
2

update fuel

0 / 3

1x
What is the time complexity of this solution?
1

O(n log n)

2

O(4ⁿ)

3

O(log m * n)

4

O(n)

Mark as read

Next: Jump Game

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

(10)

Comment
Anonymous
R
ReliableBrownTakin454
Premium
• 3 months ago

The way I understand why this works, and why greedy algorithm is a good fit here - is that you are guaranteed you never went below 0 no matter what. so if at some point fuel gets lower than 0, you know no other starting point earlier would have work, because we already tried each of them with a starting fuel greater than zero, so there's no way they'd work with starting fuel 0.

11

Reply
Michał Rybiński
• 2 months ago

Thanks, that really cleared it out for me

1

Reply
S
SuccessfulBlueMarmoset808
Premium
• 11 months ago
def canCompleteCircuit(gas, cost):
        total_gas = 0
        total_cost = 0
        tank = 0
        start = 0

        for i in range(len(gas)):
            total_gas += gas[i]
            total_cost += cost[i]
            tank += gas[i] - cost[i]
        
            if tank < 0:
                start = i + 1
                tank = 0
            
        if total_gas < total_cost:
            return -1 
        
        return start
Show More

2

Reply
Shehab Abdelgawad
Premium
• 11 months ago

this is O(n), while the solution provided is O(3n) which is still O(n), but this solution is faster

0

Reply
Arun prasath
• 1 year ago

Nice solution. I iterated 2n-1 stations before I conclude. We can conclude at the nth station.

1

Reply
KT
kisan team outing
Premium
• 6 days ago

**Easier single pass solution: **

Gemini said
The "gist" of this algorithm is a Single-Pass Greedy Strategy. It relies on two mathematical certainties to avoid the O(n
2
) brute-force approach.

The "Total Fuel" Rule (Global Check) The most important rule is that if the total gas available is less than the total cost to travel the entire circle, a solution is mathematically impossible.

By tracking totalSurplus, you determine if a path exists at all by the end of the loop.

If ∑(gas−cost)≥0, a starting point is guaranteed to exist.

The "Point of No Return" Rule (Greedy Choice) This is where the surplus < 0 logic comes in.

The Problem: If you start at Station A and run out of gas at Station B, you can't just try starting at the station immediately after A.

The Insight: Any station between A and B is also a failing starting point. Why? Because you reached those intermediate stations with some amount of gas (or at least zero) from A. If you couldn't make it to B with a "head start" from A, you definitely won't make it starting from those stations with an empty tank.

The Action: When surplus hits a negative value, you "fail forward" by resetting your start to the very next station (i + 1) and clearing your current surplus.

class Solution {
public:
    int canCompleteCircuit(vector<int> gas, vector<int> cost) {
        int totalSurplus = 0;
        int surplus = 0;
        int start = 0;

        for(int i =0; i<gas.size(); i++){
            totalSurplus = totalSurplus + gas[i] - cost[i];
            surplus = surplus + gas[i] - cost[i];
            if(surplus < 0){
                start = i+1;
                surplus = 0;
            }
        }

        return totalSurplus >= 0 ? start : -1;
    }
};
Show More

0

Reply
Satya Dasara
Premium
• 2 months ago
• edited 2 months ago

The trick here is if you fail at i index it means you'll always fail at all indices till i. The bonus fuel to complete trip might be in i+1 index so continue from there and check.

If total gas less than total cost you can never make a round trip. This is because at i index if gas is less than cost at i then you either need surplus fuel from before or next stop travel impossible. So atleast sum(gas) == sum(cost) for this to work.

class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:

        if sum(gas) < sum(cost):
            return -1

        start = 0
        fuel = 0
        N = len(gas)

        for i in range(0, N):
            if fuel + gas[i] >= cost[i]:
                fuel += gas[i] - cost[i]
            else:
                start = i + 1
                fuel = 0

        return start 
Show More

0

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Solution

Explanation

Walkthrough
