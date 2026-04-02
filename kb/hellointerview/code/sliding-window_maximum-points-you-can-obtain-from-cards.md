# Max Points You Can Obtain From Cards

> Source: https://www.hellointerview.com/learn/code/sliding-window/maximum-points-you-can-obtain-from-cards
> Scraped: 2026-03-30


Sliding Window
Max Points You Can Obtain From Cards
medium
DESCRIPTION (inspired by Leetcode.com)

Given an array of integers representing card values, write a function to calculate the maximum score you can achieve by picking exactly k cards.

You must pick cards in order from either end. You can take some cards from the beginning, then switch to taking cards from the end, but you cannot skip cards or pick from the middle.

For example, with k = 3:

Take the first 3 cards: valid
Take the last 3 cards: valid
Take the first card, then the last 2 cards: valid
Take the first 2 cards, then the last card: valid
Take card at index 0, skip some, then take card at index 5: not valid (skipping cards)

Constraints: 1 <= k <= cards.length

Example 1: Input:

cards = [2,11,4,5,3,9,2]
k = 3

Output:

17

Explanation:

First 3 cards: 2 + 11 + 4 = 17
Last 3 cards: 3 + 9 + 2 = 14
First 1 + last 2: 2 + 9 + 2 = 13
First 2 + last 1: 2 + 11 + 2 = 15

Maximum score is 17.

Example 2: Input:

cards = [1, 100, 10, 0, 4, 5, 6]
k = 3

Output:

111

Explanation: Take the first three cards: 1 + 100 + 10 = 111. This is better than taking the last 3 cards (4 + 5 + 6 = 15) or any other combination.

CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def maxScore(self, cards: List[int], k: int) -> int:
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
When you pick k cards from either end of the array, you're actually leaving behind n - k consecutive cards in the middle that you didn't pick.
For example, with cards = [2,11,4,5,3,9,2] and k = 3:
2
11
4
5
3
9
2
n - k
2
11
4
5
3
9
2
n - k
2
11
4
5
3
9
2
n - k
2
11
4
5
3
9
2
n - k
Every possible way to pick 3 cards from the ends corresponds to a different window of 4 cards (n - k = 7 - 3 = 4) in the middle that we're NOT picking.
Why This Matters
Since we know the total sum of all cards, we can calculate:
Sum of picked cards = Total sum - Sum of unpicked cards
So to maximize the sum of picked cards, we need to minimize the sum of unpicked cards.
This transforms the problem: instead of trying all combinations of picking from ends, we find the minimum sum of any window of size n - k.
23
state
2
11
4
5
3
9
2
36
total
Sum of picked cards (highlighted) = 36 - 23 = 13
The Algorithm
Use a fixed-length sliding window of size n - k to find the minimum sum of any consecutive n - k cards. For each window position, calculate total - window_sum to get the corresponding score, and track the maximum.
Solution
cards
​
|
cards
comma-separated integers
k
​
|
k
integer
Try these examples:
Take All
Mixed
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def maxScore(cards, k):
  total = sum(cards)
  if k == len(cards):
    return total

  state = 0
  max_points = 0
  start = 0

  for end in range(len(cards)):
    state += cards[end]

    if end - start + 1 == len(cards) - k:
      max_points = max(total - state, max_points)
      state -= cards[start]
      start += 1

  return max_points
2
11
4
5
3
9
2

max points from cards

0 / 18

1x

Mark as read

Next: Max Sum of Distinct Subarrays Length k

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

(49)

Comment
Anonymous
​
Sort By
Popular
Sort By
MM
Minnie Mouse
Top 5%
• 5 months ago

In my opinion, this is the simplest and most straightforward way to think about the solution. Since, we can only take k cards, we start by getting the sum of the last k cards. Then, we just need to subtract each of the last k cards one at a time, while adding cards from the beginning one at a time. Each iteration, we'll check the new sum against the maximum to determine if we've found a higher sum. Here, I've used left and right to represent the beginning and last cards that we are adding/subtracting respectively. We don't need to store left separately as we can calculate left formulaically using right and k (left = right - (n - k)) but I find it much more readable and less taxing mentally to just start left at 0 and increment it, which is potentially useful when your mind is under stress during an interview.

In the worst case, k = n which gives us O(n) time complexity but we can give a tighter bound at O(2k) or, equivalently, O(k). Space complexity is O(1).

def maxScore(self, cardPoints: List[int], k: int) -> int:
        max_score = score = sum(cardPoints[-k:])
        n = len(cardPoints)

        left = 0
        for right in range(n - k, n):
            score += cardPoints[left] - cardPoints[right]
            left += 1
            max_score = max(max_score, score)
        
        return max_score
Show More

49

Reply
E
ElegantAquaMouse760
• 1 month ago

even better this one has O(k) time complexity, which is better than the O(n) of the standard solution.
I also made it start on the left itself:

class Solution:
    def maxScore(self, cards: List[int], k: int):
           k_sum = sum(cardPoints[0:k])
           max_sum = k_sum
           for i in range(1,k+1):
                 k_sum = k_sum - cardPoints[ k - i] + cardPoints[-i]
                 max_sum = max(max_sum, k_sum)
            
           return max_s

1

Reply
Dawid Kałuża
Premium
• 2 months ago
• edited 2 months ago

Agreed, I came up with pretty much the same idea in Java. Instead of iterating through cards, I iterate from 0 to k, and using index i sum elements from 0 to i and from cards.length to cards.length - k - i, where k - i is a number of picks left, and check if the sum is the best one.

public class Solution {
    public Integer maxScore(int[] cards, Integer k) {
        if (cards.length <= k) {
            return IntStream.of(cards).sum();
        }

        int bestScore = 0;
        for (int i = 0; i < k; i++) {
            int leftSum = IntStream.of(
                Arrays.copyOfRange(cards, 0, i)
            ).sum();
            int remainingPicksNum = k - i;
            int rightSum = IntStream.of(
                Arrays.copyOfRange(
                    cards, 
                    cards.length - remainingPicksNum, 
                    cards.length
                )
            ).sum();
            bestScore = Math.max(leftSum + rightSum, bestScore);
        }

        return bestScore;
    }
}
Show More

1

Reply
Ruth Nadav
• 11 months ago

thers a way to calculate it in o(2k) and not o(n)

class Solution:
    def maxScore(self, cards: list[int], k: int):
        window_points = 0
        max_points = 0
        len_cards = len(cards)
        start = len_cards - k
        for i in range(start, start + (k*2)):
            window_points += cards[i % len_cards]
            if i - start >= k:
                window_points -= cards[start % len_cards]
                start += 1
            max_points = max(max_points, window_points)
        return max_points

if you dont want to use modulo you can also start by sum the last cards and looo over the beginning of the array:

class Solution:
    def maxScore(self, cards: list[int], k: int):
        len_cards = len(cards)
        start = len_cards - k
        window_points = sum(cards[start:])
        max_points = window_points
        print(window_points)
        for card in cards[:k]:
            window_points += card
            window_points -= cards[start]
            start += 1
            max_points = max(max_points, window_points)
        return max_points
Show More

5

Reply
Manish Kunwar
• 8 months ago

Non sane solution. Since sliding window seems to only care about first k and last k element, rearrange the array so that it becomes linear array.

class Solution:
    def maxScore(self, cards: List[int], k: int):
        rearranged_list = cards[-k:] + cards[:k]
        start = 0
        sum_ = 0
        state = 0
        
        for end in range(len(rearranged_list)):
            state += rearranged_list[end]

            if end - start  >= k:
                state -= rearranged_list[start]
                start += 1
            
            sum_ = max(state, sum_)
        return sum_

3

Reply
Sean Tarzy
Top 5%
• 1 year ago

here's a think a more straightforward way of thinking about it. instead of 'subtracting the middle' we can just think of it as sliding the indices we're gonna use for adding from frontend to back (typescript):

function maxScore(cardPoints: number[], k: number): number {
// [1,2,3,4,5,6,1]
// think of it as a sliding window
// we're we have the window wrap around from the start to the end
//  
//   s          e
// [1,2,3,4,5,6,1]
// what we can do is, when we shift the window,
//          - subtract the former starting element
//          - add the new element

let start = k - 1
let end = 0 

let currentSum = calculateSum(cardPoints,k)
let maxSum = currentSum 

while(k >0){
    end-- 
    if(end < 0){
        end = cardPoints.length -1 
    }
    let formerStart = start
    start--
     if(start < 0){
        start = cardPoints.length -1 
    }

    currentSum -= cardPoints[formerStart]
    currentSum+= cardPoints[end]
    maxSum = Math.max(currentSum,maxSum)
    k--
}
return maxSum
};

const calculateSum = (cardPoints: number[],k: number): number=>{
    let sum = 0 

    for(let i =0; i<k; i++){
        sum+= cardPoints[i]
    }
    return sum
}
Show More

3

Reply
Arun prasath
• 1 year ago

Problem statement is not clear enough. Please address it

2

Reply
Jimmy Zhang
Top 5%
• 1 year ago

updated to be more clear

0

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

Why This Matters

The Algorithm

Solution
