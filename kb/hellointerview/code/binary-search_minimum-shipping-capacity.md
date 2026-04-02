# Minimum Shipping Capacity

> Source: https://www.hellointerview.com/learn/code/binary-search/minimum-shipping-capacity
> Scraped: 2026-03-30


Binary Search
Minimum Shipping Capacity
medium
DESCRIPTION (inspired by Leetcode.com)

You're a logistics manager preparing to ship products from a warehouse. Each product type has both a quantity and a weight per item. Shipping boxes have TWO constraints:

Capacity limit: Maximum number of items per box
Weight limit: Maximum weight (kg) per box

Rules:

Each product type must be packed separately
All boxes have the same capacity and weight limits
A box can hold at most capacity items OR maxWeightPerBox kg, whichever comes first
Items must be whole numbers (can't pack fractional items)

Given arrays of quantities and weights per item, plus box and weight constraints, find the minimum box capacity needed to ship all products.

Example 1:

Input:

quantities = [8, 12, 5]
weights = [2, 3, 1]  # kg per item
maxBoxes = 6
maxWeightPerBox = 20  # kg

Output: 5

Explanation: With capacity 5:

Product 0 (8 items @ 2kg): min(5, 10, 8) = 5 items/box → needs 2 boxes (5 + 3 items)
Product 1 (12 items @ 3kg): min(5, 6, 12) = 5 items/box → needs 3 boxes (5 + 5 + 2 items)
Product 2 (5 items @ 1kg): min(5, 20, 5) = 5 items/box → needs 1 box Total: 6 boxes ≤ 6 ✓

Example 2:

Input:

quantities = [10, 15, 8]
weights = [5, 2, 3]
maxBoxes = 10
maxWeightPerBox = 15

Output: 4

Explanation: With capacity 4:

Product 0 (10 items @ 5kg): min(4, ⌊15/5⌋, remaining) = 3 items/box → needs 4 boxes
Product 1 (15 items @ 2kg): min(4, ⌊15/2⌋, remaining) = 4 items/box → needs 4 boxes
Product 2 (8 items @ 3kg): min(4, ⌊15/3⌋, remaining) = 4 items/box → needs 2 boxes Total: 10 boxes ≤ 10 ✓
CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def minimumShippingCapacity(self, quantities: List[int], weights: 
    List[int], maxBoxes: int, maxWeightPerBox: int) -> int:
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

Building Intuition
5 items
10kg
4
3
2
1
3 items
6kg
2
1
Product A
8 items @ 2kg
2 boxes
5 items
15kg
4
3
2
1
5 items
15kg
4
3
2
1
2 items
6kg
1
Product B
12 items @ 3kg
3 boxes (weight limit!)
5 items
5kg
4
3
2
1
Product C
5 items @ 1kg
1 box
Constraints:
maxBoxes = 6
maxWeight = 20kg
Find minimum capacity
Answer: 5 items/box
With capacity = 5 items/box:
Fits in capacity & weight limits
Needs extra boxes (weight limited)
You're shipping products from a warehouse, but here's the twist: each product has both a quantity and a weight per item. Your shipping boxes have two constraints:
Capacity limit: Maximum number of items per box
Weight limit: 20kg per box
Whichever limit is hit first determines how many items fit in that box.
Given: quantities = [8, 12, 5], weights = [2, 3, 1] kg per item, maxBoxes = 6, maxWeightPerBox = 20
With capacity = 5 items/box:
Product 0 (8 items @ 2kg each): Each box can hold min(5, ⌊20/2⌋, remaining) = min(5, 10, remaining) = 5 items. Needs 2 boxes: [5 items/10kg] + [3 items/6kg]
Product 1 (12 items @ 3kg each): Each box can hold min(5, ⌊20/3⌋, remaining) = min(5, 6, remaining) = 5 items. Needs 3 boxes: [5 items/15kg] + [5 items/15kg] + [2 items/6kg]
Product 2 (5 items @ 1kg each): Each box can hold min(5, ⌊20/1⌋, remaining) = min(5, 20, 5) = 5 items. Needs 1 box: [5 items/5kg]
Total: 2 + 3 + 1 = 6 boxes, which exactly meets our limit of 6 ✓
Can we find a smaller capacity that still works?
Brute Force: Try Every Capacity?
The brute force approach would be to try every possible capacity from 1 up to max(quantities) and check each one:
bruteForce(quantities, weights, maxBoxes, maxWeightPerBox)
    for capacity = 1 to max(quantities)
        boxes = countBoxesNeeded(capacity)
        if boxes <= maxBoxes
            return capacity
    return max(quantities)
The counting function now needs to handle weight constraints:
countBoxesNeeded(capacity)
    boxes = 0
    for i = 0 to quantities.length - 1
        remaining = quantities[i]
        while remaining > 0
            itemsThisBox = min(
                capacity,
                floor(maxWeightPerBox / weights[i]),
                remaining
            )
            boxes = boxes + 1
            remaining = remaining - itemsThisBox
    return boxes
This works, but if the largest quantity is 1,000,000, we'd need up to 1 million iterations. Can we do better?
The Monotonic Property
If capacity c works (uses ≤ maxBoxes), then any capacity larger than c also works. Bigger boxes = fewer boxes needed.
This holds even with weight constraints. If we can fit items with capacity 5, we can definitely fit them with capacity 6 (assuming weight doesn't become the limiting factor, which it won't because we're still packing the same items).
Too many boxes
answer = 5
Fits in maxBoxes ✓
Bigger capacity =
fewer boxes needed
(still works)
capacity too small
capacity sufficient
This monotonic property tells us the search space is divided into two regions: capacities that don't work (too small) and capacities that do work (large enough). We want to find the boundary i.e. the smallest capacity that works.
Binary search is perfect for finding boundaries in monotonic search spaces.
When the answer lies in a range and there's a monotonic property (if X works, all values greater/less than X also work), binary search can find the optimal answer in O(log n) iterations instead of O(n).
How Binary Search Works Here
1. Initialize
left = 1
right = max(quantities)
2. Try Mid
mid = (left + right) / 2
count boxes needed
3. Narrow
Works → right = mid
Doesn't → left = mid+1
4. Done
left == right
return left
For each candidate capacity mid, we check if it's feasible by counting how many boxes we'd need. This is where the weight constraint makes things interesting:
countBoxes(quantities, weights, capacity, maxWeightPerBox)
    boxes = 0
    for i = 0 to quantities.length - 1
        remaining = quantities[i]
        while remaining > 0
            itemsThisBox = min(
                capacity,
                floor(maxWeightPerBox / weights[i]),
                remaining
            )
            boxes = boxes + 1
            remaining = remaining - itemsThisBox
    return boxes
For each product, we pack items into boxes until we've packed everything. Each box can hold:
At most capacity items (the capacity limit we're testing)
At most floor(maxWeightPerBox / weights[i]) items (the weight limit)
At most remaining items (can't pack more than we have)
We take the minimum of these three values.
minimumShippingCapacity(quantities, weights, maxBoxes, maxWeightPerBox)
    left = 1
    right = max(quantities)
    
    while left < right
        mid = (left + right) / 2
        if countBoxes(quantities, weights, mid, maxWeightPerBox) <= maxBoxes
            right = mid
        else
            left = mid + 1
    
    return left
Walkthrough
Let's trace through quantities = [8, 12, 5], weights = [2, 3, 1] with maxBoxes = 6 and maxWeightPerBox = 20 step by step.
Step 1: Initialize the search bounds
We establish the range of possible capacities. The minimum is 1 (smallest possible box). The maximum is max(quantities) = 12 because a box that holds 12 items can ship any single product type in one box (assuming weight allows).
Step 1:
Initialize bounds
left=1
right=12
Search space: [1, 12]
Our search space is [1, 12]. Now we start binary searching for the minimum valid capacity.
Step 2: First binary search iteration
We calculate mid = (1 + 12) / 2 = 6. Can we ship everything with capacity 6 using at most 6 boxes?
Let's count:
Product 0 (8 items @ 2kg): min(6, floor(20/2), 8) = min(6, 10, 8) = 6 items/box → needs ceil(8/6) = 2 boxes
Product 1 (12 items @ 3kg): min(6, floor(20/3), 12) = min(6, 6, 12) = 6 items/box → needs ceil(12/6) = 2 boxes
Product 2 (5 items @ 1kg): min(6, floor(20/1), 5) = min(6, 20, 5) = 5 items/box → needs 1 box
Total: 2 + 2 + 1 = 5 boxes ≤ 6 ✓
Since 5 ≤ 6, capacity 6 works! But maybe we can do better with smaller boxes. We set right = mid = 6 to search the lower half.
Step 2:
mid = 6, boxes needed = 5 ≤ 6 ✓
left=1
mid=6
right=6
Step 3: Second binary search iteration
Now left = 1, right = 6. We try mid = (1 + 6) / 2 = 3.
Let's count:
Product 0 (8 items @ 2kg): min(3, floor(20/2), 8) = min(3, 10, 8) = 3 items/box → needs ceil(8/3) = 3 boxes
Product 1 (12 items @ 3kg): min(3, floor(20/3), 12) = min(3, 6, 12) = 3 items/box → needs ceil(12/3) = 4 boxes
Product 2 (5 items @ 1kg): min(3, floor(20/1), 5) = min(3, 20, 5) = 3 items/box → needs ceil(5/3) = 2 boxes
Total: 3 + 4 + 2 = 9 boxes > 6 ✗
Capacity 3 is too small! We set left = mid + 1 = 4.
Step 3:
mid = 3, boxes needed = 9 > 6 ✗
left=1
mid=3
right=6
→ left = 4
Step 4: Third binary search iteration
Now left = 4, right = 6. We try mid = (4 + 6) / 2 = 5.
Let's count:
Product 0 (8 items @ 2kg): min(5, floor(20/2), 8) = min(5, 10, 8) = 5 items/box → needs ceil(8/5) = 2 boxes
Product 1 (12 items @ 3kg): min(5, floor(20/3), 12) = min(5, 6, 12) = 5 items/box → needs ceil(12/5) = 3 boxes
Product 2 (5 items @ 1kg): min(5, floor(20/1), 5) = min(5, 20, 5) = 5 items/box → needs 1 box
Total: 2 + 3 + 1 = 6 boxes ≤ 6 ✓
Capacity 5 works! Try smaller: right = mid = 5.
Step 4:
mid = 5, boxes needed = 6 ≤ 6 ✓
left=4
mid=5
right=6
→ right = 5
Step 5: Fourth binary search iteration
Now left = 4, right = 5. We try mid = (4 + 5) / 2 = 4.
Let's count:
Product 0 (8 items @ 2kg): min(4, floor(20/2), 8) = min(4, 10, 8) = 4 items/box → needs ceil(8/4) = 2 boxes
Product 1 (12 items @ 3kg): min(4, floor(20/3), 12) = min(4, 6, 12) = 4 items/box → needs ceil(12/4) = 3 boxes
Product 2 (5 items @ 1kg): min(4, floor(20/1), 5) = min(4, 20, 5) = 4 items/box → needs ceil(5/4) = 2 boxes
Total: 2 + 3 + 2 = 7 boxes > 6 ✗
Capacity 4 is too small! We set left = mid + 1 = 5.
Step 5:
mid = 4, boxes needed = 7 > 6 ✗
left=4
mid=4
right=5
→ left = 5
Step 6: Converged
Now left = right = 5. The loop ends, and we return 5.
Step 6:
Converged: left = right = 5
5
Answer: 5
Result: 5
The minimum box capacity is 5 items per box. With this capacity and weight constraints:
Product 0 (8 items @ 2kg each): 2 boxes [5 items/10kg] + [3 items/6kg]
Product 1 (12 items @ 3kg each): 3 boxes [5 items/15kg] × 2 + [2 items/6kg]
Product 2 (5 items @ 1kg each): 1 box [5 items/5kg]
Total: 2 + 3 + 1 = 6 boxes, which exactly meets our limit of 6.
Solution
quantities
​
|
quantities
item counts (comma-separated)
weights
​
|
weights
kg per item (comma-separated)
maxBoxes
​
|
maxBoxes
max boxes allowed
maxWeight
​
|
maxWeight
max kg per box
Try these examples:
Example
Heavy
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def minimumShippingCapacity(quantities, weights, maxBoxes, maxWeightPerBox):
    def countBoxes(capacity):
        boxes = 0
        for i in range(len(quantities)):
            remaining = quantities[i]
            while remaining > 0:
                itemsThisBox = min(capacity, maxWeightPerBox // weights[i], remaining)
                boxes += 1
                remaining -= itemsThisBox
        return boxes
    
    left = 1
    right = max(quantities)
    
    while left < right:
        mid = (left + right) // 2
        if countBoxes(mid) <= maxBoxes:
            right = mid
        else:
            left = mid + 1
    
    return left
left: —
mid: —
right: —
maxBoxes: —
boxes: —
8
0
12
1
5
2

Binary search on capacity: find minimum box size that fits in maxBoxes

0 / 49

1x
Try different quantities, weights, and constraints
What is the time complexity of this solution?
1

O(n²)

2

O(n · m · log(max))

3

O(n³)

4

O(log n)

Recognizing This Pattern
This problem follows the "binary search on answer" pattern with an added twist: compound constraints. Look for these signals:
Find minimum/maximum that satisfies multiple constraints - here, minimum capacity with both box limit and weight limit
Monotonic relationship despite compound constraints - if capacity X works, X+1 also works (since we're packing the same items)
Bounded search space - capacity ranges from 1 to max(quantities)
Complex feasibility check - counting boxes requires simulating packing with multiple constraints
The difference from simpler binary search problems is the counting function is more complex because each box must satisfy two independent constraints (capacity AND weight). You can't use simple ceiling division - you must simulate the packing process.
Similar problems include:
Koko eating bananas (single constraint: finish in h hours)
Ship packages within D days (single constraint: time limit)
Split array into subarrays (single constraint: number of subarrays)
This problem is harder because the weight constraint creates a non-uniform packing pattern - different products may be limited by different constraints (capacity vs weight).
When you see "find the minimum X such that condition holds" with multiple interacting constraints, recognize that:
The monotonic property still applies if the constraints are independent
The feasibility check becomes a simulation rather than a formula
You need to handle each constraint correctly (use min() to find the effective limit per box)
Always ask: "What's the actual limiting factor for each iteration?" Here, it's min(capacity, floor(maxWeight/itemWeight), remaining).

Mark as read

Next: Heap Overview

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
P
PregnantOliveFelidae174
Premium
• 2 months ago

Leetcode link should be: https://leetcode.com/problems/capacity-to-ship-packages-within-d-days

5

Reply

Shivam Chauhan

Admin
• 2 months ago

Hey, those 2 are different problem. Leetcode 1011. Capacity To Ship Packages Within D Days allows combining of different products under same box, while this problem focuses on having quantities from single product in a box, which changes the question entirely.

2

Reply
F
ForeignBronzeFelidae167
Premium
• 16 days ago

public Integer minimumShippingCapacity(int[] quantities,
int[] weights, Integer maxBoxes, Integer maxWeightPerBox) {

// 1.) Calculate the min. number of qty. for each product type which one can ship
//     based on the max box weight constraint.
for (int x=0; x<weights.length; x++) {
if (weights[x]>maxWeightPerBox) {
return -1; // this item cannot fit into the box.
}
weights[x]=quantities[x]*weights[x];
}
int[] maxQtyPerProductCanBeShippedOnABox=new int[weights.length];
int maxQtyOverAll=Integer.MIN_VALUE;
for (int x=0; x<quantities.length; x++) {
maxQtyPerProductCanBeShippedOnABox[x]=
Math.min(quantities[x], (quantities[x]*maxWeightPerBox)/weights[x]);
maxQtyOverAll=Math.max(maxQtyOverAll, maxQtyPerProductCanBeShippedOnABox[x]);
}
// 2.) Calculate the min. box qty. capacity we can have using Binary Search.
int s=1;
int e=maxQtyOverAll;
int capacityQty=Integer.MAX_VALUE;
while (s<=e) {
int mid=s+(e-s)/2;
int cap=0;
for (int y=0; y<quantities.length; y++) {
int denominator=Math.min(mid, maxQtyPerProductCanBeShippedOnABox[y]);
cap+= (int) Math.ceil((double)quantities[y]/denominator);
}
if (cap>maxBoxes) {
s=mid+1;
} else {
capacityQty=Math.min(capacityQty, mid);
e=mid-1;
}
} // ends while loop.
return capacityQty;
}

Show More

0

Reply
Joel Wang
Premium
• 1 month ago
• edited 1 month ago
class Solution:
    def minimumShippingCapacity(self, quantities: List[int], weights: List[int], maxBoxes: int, maxWeightPerBox: int):
        # Your code goes here
        left, right = 1, max(quantities)

        def boxes_needed(target):
            s = 0
            for i in range(len(quantities)):
                min_cap = min(target, maxWeightPerBox//weights[i], quantities[i])
                s += (quantities[i] - 1) // min_cap + 1
            
            return s

        res = maxBoxes
        while left <= right:
            mid = (left + right) // 2

            if boxes_needed(mid) <= maxBoxes:
                res = mid
                right = mid - 1
            else:
                left = mid + 1

        return res
Show More

0

Reply
A
AcceptedCopperRaven971
Premium
• 1 month ago

I don't see the difference between this and Apple Harvest.
In fact, copy-pasting your solution from that problem to this problem works

0

Reply
fz zy
Premium
• 1 month ago
class Solution:
    def minimumShippingCapacity(self, quantities: List[int], maxBoxes: int):
        left, right = 1, max(quantities)
        while left <= right:
            mid = left + ((right - left) >> 1)
            tot = 0
            for quantity in quantities:
                tot += (quantity + mid - 1) // mid
            if tot > maxBoxes:
                left = mid + 1
            else:
                right = mid - 1
        return left

0

Reply
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Building Intuition

Brute Force: Try Every Capacity?

The Monotonic Property

How Binary Search Works Here

Walkthrough

Solution

Recognizing This Pattern
