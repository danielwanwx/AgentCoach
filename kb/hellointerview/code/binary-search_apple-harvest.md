# Apple Harvest (Koko Eating Bananas)

> Source: https://www.hellointerview.com/learn/code/binary-search/apple-harvest
> Scraped: 2026-03-30


Binary Search
Apple Harvest (Koko Eating Bananas)
medium
DESCRIPTION (inspired by Leetcode.com)

Bobby has an orchard of apple trees, and each tree has a certain number of apples on it.

Bobby wants to collect all the apples by the end of the day by collecting a fixed number of apples per hour. He can only harvest apples from one tree per hour - if he finishes collecting apples from a tree before the hour is up, he must wait until the next hour to move to the next tree.

For example, if there are 3 apples on a tree and Bobby collects 1 apple per hour, it will take him 3 hours to finish collecting the apples on that tree.
If he harvests 2 apples per hour, it will take him 2 hours to finish collecting all the apples on that tree (he waits until the hour is up even though he finishes early).

Write a function to determine the slowest rate of apples Bobby can harvest per hour to finish the job in at most 'h' hours. The input to the function is an array of integers representing the number of apples on each tree and an integer 'h' representing the number of hours Bobby has to finish the job within.

Example 1:

Input:

apples = [3, 6, 7], h = 8

Output: 3

Explanation:

1 apple per hour: 3 hours for first tree, 6 hours the second tree, and 7 hours for third tree. This totals 16 hours, which is more than the 8 hours he has to finish the job. NOT VALID.
2 apples per hour: 2 + 3 + 4 = 9 hours, which is more than the 8 hours he has to finish the job. NOT VALID.
3 apples per hour: 1 + 2 + 3 = 6 hours, which is less than the 8 hours he has to finish the job. VALID.
4 apples per hour: 1 + 2 + 2 = 5 hours, which is less than the 8 hours he has to finish the job. VALID.
5 apples per hour: 1 + 2 + 2 = 5 hours, which is less than the 8 hours he has to finish the job. VALID.

Therefore, the minimum number of apples Bobby must harvest per hour to finish the job in 8 hours or less is 3.

Example 2:

Input:

apples = [25, 9, 23, 8, 3], h = 5

Output: 25 (Bobby must harvest 25 apples per hour to finish in 5 hours or less)

CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def minHarvestRate(self, apples: List[int], h: int) -> int:
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
In this problem, we are trying to find the slowest rate at reach we can harvest all the apples in the orchard within the given time limit and the requirements of the problem.
Brute-Force Approach
One observation before starting to solve this problem:
The slowest rate at which can harvest apples is 1.
The fastest rate at which can harvest apples is equal to the maximum number of apples in the orchard, as going any faster than this will not change the time taken to harvest all the apples.
For example, if apples = [25, 9, 23, 8, 3], then going at rate any faster than 25 apples per hour will take the same time as going at 25 apples per hour.
The brute-force approach to this problem works similar to the explanation in the Example section above.
We'll start with a rate of 1, and calculate the time taken to harvest all the apples at this rate.
If that time is less than or equal to the given time limit, then we've found the slowest rate at which we can harvest all the apples in the given time limit, so we return this rate.
If the time taken is greater than the given time limit, then we increase the rate by 1 and repeat.
Calculating Time Taken
To calculate the time taken to harvest all the apples at a given rate, we can use this function:
SOLUTION
Python
Language
def time_taken(rate):
    time = 0
    for i in range(len(apples)):
        time += (apples[i] + rate - 1) // rate
    return time
This function takes O(n) where n is the number of trees (the length of the apples array) to run, as we iterate over each tree in apples.
Brute-Force Solution
Here is the brute-force solution to the problem:
SOLUTION
Python
Language
def min_rate(apples, h):
    def time_taken(rate):
        time = 0
        for i in range(len(apples)):
            time += (apples[i] + rate - 1) // rate
        return time

    rate = 1
    while time_taken(rate) > h:
        rate += 1
    return rate
Thus, the total time complexity of the brute-force approach is O(n * (max(apples) - 1)), as we iterate from 1 to the maximum number of apples in the orchard. For each iteration, we calculate the time taken to harvest all the apples using the time_taken function in O(n) time.
Binary Search Approach
One way to visualize all the rates we check in the brute-force approach is like this, shown for when apples = [4, 7, 9, 12] and h = 6.
1
2
3
4
5
6
7
F
F
F
F
F
F
T
The array on top represents the rate we are trying to harvest apples at, while the array on the bottom represents if that corresponding time is less than or equal to the given time limit h (F for False, T for True). Our brute-force solution returns the rate corresponding to the first T in the bottom array, or 7.
Now let's image our brute-force solution tried everything between 1 and the max_apples in the orchard, instead of returning after the first T. Then the array would look like this:
F
F
F
F
F
F
T
1
2
3
4
5
6
7
8
9
10
11
12
T
T
T
T
T
apples = [4, 7, 9, 12] and h = 6
Why visualize the problem this way? Well, we have a sorted array on top, and a search condition ("find the first T") on the bottom. If we can find a way to eliminate half of the array from our search space at each step, then we can use binary search to solve this problem in O(log(max(apples)) * n) time.
Reducing Search Space
Let's set up the pointers like we do in classic binary search:
F
F
F
F
F
F
T
1
2
3
4
5
6
7
8
9
10
11
12
T
T
T
T
T
left
right
mid
apples = [4, 7, 9, 12] and h = 6
At this point, mid points to a rate of 6 apples per hour. This would take 7 hours to harvest all the apples, which is too slow. So we need to reduce our search space.
How should we do it? Well, if 6 apples per hour is already too slow, then anything slower than 6 apples will also be too slow. So we can set left = mid + 1 to discard the left half of the array. Now we're doing binary search!
F
F
F
F
F
F
T
1
2
3
4
5
6
7
8
9
10
11
12
T
T
T
T
T
left
right
mid
apples = [4, 7, 9, 12] and h = 6
Next iteration: set mid = (left + right) // 2. Now, mid points to a rate of 9 apples per hour. This would take 5 hours to harvest all the apples, which is fast enough. But can we do better? (i.e. can we find a slower rate that still lets us finish in time?).
F
F
F
F
F
F
T
1
2
3
4
5
6
7
8
9
10
11
12
T
T
T
T
T
left
right
mid
apples = [4, 7, 9, 12] and h = 6
We're not sure yet, so let's keep searching. At this point, we can discard the right half of the array by setting right = mid - we know that any rate faster than 9 apples per hour will not be a better answer than 9.
Note how we set right = mid instead of right = mid - 1. This is because mid is still a valid answer, and we don't want to remove it from our search space just yet, like we would if we set it as mid - 1.
F
F
F
F
F
F
T
1
2
3
4
5
6
7
8
9
10
11
12
T
T
T
T
T
left
right
mid
apples = [4, 7, 9, 12] and h = 6
This binary search continues until left and right are equal.
Set mid = (left + right) / 2 = 8 apples per hour.
F
F
F
F
F
F
T
1
2
3
4
5
6
7
8
9
10
11
12
T
T
T
T
T
left
right
mid
This is fast enough (T), so we set right = mid.
mid
F
F
F
F
F
F
T
1
2
3
4
5
6
7
8
9
10
11
12
T
T
T
T
T
left
right
Set mid = (right + left) / 2.
mid
F
F
F
F
F
F
T
1
2
3
4
5
6
7
8
10
11
12
9
T
T
T
T
T
left
right
This is still fast enough (T), so set right = mid.
mid
F
F
F
F
F
F
T
1
2
3
4
5
6
7
8
10
11
12
9
T
T
T
T
T
left
right
Now, left = right, our search space only has one element left. We can return the answer as left (or right).
Optimal Solution
SOLUTION
Python
Language
class Solution:
    def minHarvestRate(self, apples, h):
        # Binary search on harvest rate: find minimum rate to finish in h hours
        def time_taken(rate):
            time = 0
            # Calculate total time needed at this harvest rate
            for i in range(len(apples)):
                # Ceiling division: (apples[i] + rate - 1) // rate
                time += (apples[i] + rate - 1) // rate 
            return time

        # Binary search bounds: minimum rate = 1, maximum rate = max apples
        left, right = 1, max(apples)
        
        # Binary search for minimum valid harvest rate
        while left < right:
            mid = (left + right) // 2
            if time_taken(mid) > h:
                # Rate too slow, need faster rate
                left = mid + 1
            else:
                # Rate is sufficient, try slower rate
                right = mid
                
        return left
What is the time complexity of this solution?
1

O(x * y)

2

O(n!)

3

O(log m * n)

4

O(m * n * 4^L)

Mark as read

Next: Search in Rotated Sorted Array

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

(20)

Comment
Anonymous
​
Sort By
Popular
Sort By
N
npuniya
Premium
• 7 months ago

time += (apples[i] + rate - 1) / rate;
The above code can be replaced by
Math.ceil((double)appleCount/rate)

Which is clean and easy to understand.

9

Reply
Johan Ospina
Premium
• 4 months ago

If you wanted to avoid casting while still being legible I think you can also do something like this.

Though, I have seen the pure arithmetic expression before in CUDA programming samples so I think one could argue that it has merit in efficient compute environments.

if (apples[i] % rate == 0) {
  return apples[i] / rate;
} else {
  return apples[i] / rate + 1;
}

3

Reply
Carlos Magdalena
• 1 year ago

Hey Jimmy, thanks for answering, I think there was a misunderstanding...

I overlook at your time complexity, I assumed it was written O(log m + n)

But indeed it is correct O(log m * n) as the same is correct what I said, O(n log m)... I just expressed in a different way:

Your O(log m * n) == O(n log m)

Thanks for taking the time to answer.

4

Reply
Stanley Lin
• 1 month ago

I was just going to point out the same thing. the complexity should be O(n log m)

0

Reply
M
mit
Premium
• 3 months ago

yeah i had the same issue, solved this myself and came out to be O(n lgm) then i saw the solution and i'm like O(lg m * n) ? which at the time I thought it was lg (m * n)  haha

0

Reply
Abhay Singh
Top 1%
• 1 year ago

Java Solution:

class Solution {

    public boolean possible(int[] piles, int maxBananasAllowed, int hrs){
        int t = 0;
        for(int b : piles){
            t += (b/maxBananasAllowed) + (b%maxBananasAllowed != 0 ? 1:0);
        }

        return (t <= hrs);
    }

    public int minEatingSpeed(int[] piles, int h) {
        int l = 1;
        int r = Arrays.stream(piles).max().orElse(0);

        while(l < r){
            int m = l + (r-l)/2;

            if(possible(piles, m, h)){
                r=m;
            }else{
                l=m+1;
            }
        }

        return l;
    }
}
Show More

3

Reply
mohammad nayeem
• 1 year ago
public static int minEatingSpeed(int[] piles, int h) {
    int left = 1;
    int right = 1000000000;

    while(left <= right){
        int mid = left + (right - left) / 2;
        if(canEatInTime(piles, mid, h)) right = mid - 1;
        else left = mid + 1;
    }
    return left;
}
public static boolean canEatInTime(int piles[], int k, int h){
    int hours = 0;
    for(int pile : piles){
        int div = pile / k;
        hours += div;
        if(pile % k != 0) hours++;
    }
    return hours <= h;
}
Show More

1

Reply
L
LatinTurquoiseRhinoceros505
Premium
• 1 month ago

Notes for rust solution:

one can use time += apples[i].div_ceil(rate);
the apples.iter().max().unwrap() would panic on empty vec

0

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

Brute-Force Approach

Calculating Time Taken

Brute-Force Solution

Binary Search Approach

Reducing Search Space

Optimal Solution
