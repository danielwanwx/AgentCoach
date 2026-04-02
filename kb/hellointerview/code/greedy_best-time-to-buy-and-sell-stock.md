# Best Time to Buy and Sell Stock

> Source: https://www.hellointerview.com/learn/code/greedy/best-time-to-buy-and-sell-stock
> Scraped: 2026-03-30



E
ExpectedGreenSkunk751
Premium
• 1 month ago

Article is missing practice section for writing code before going though solution like other pages.

7

Reply
Shashi Kant
Premium
• 3 months ago

I started off from right end while managing the maxSeenSofar.

public int maxProfit(int[] prices) {
		int maxProfit = 0;
		int maxSeenSoFar = prices[prices.length - 1];
		for (int i = prices.length - 2; i >= 0; i--) {
			if(prices[i] > maxSeenSoFar) {
				maxSeenSoFar = prices[i];
			} else {
				maxProfit = Math.max(maxProfit, maxSeenSoFar - prices[i]);
			}
		}
		
		return maxProfit;
	}


1

Reply
S
srirama.kusu
Premium
• 7 months ago
# TC:O(n) and SC: O(1)
def maxProfit(prices):
    minPrice = float("inf")
    maxProfit = 0
    for price in prices:
        if price < minPrice:
            minPrice = price
        if price - minPrice > maxProfit:
            maxProfit = price - minPrice
    return maxProfit

1

Reply
cst labs
Top 5%
• 4 months ago

I had come up with the same solution but after giving it a thought, the solution conceptually looked wrong to me.  While I agree that we will find the same answers with both variations of solutions  but The code below

for (int i = 0; i < prices.length; i++) {
        minPrice = Math.min(minPrice, prices[i]);
        maxProfit = Math.max(maxProfit, prices[i] - minPrice);
    }

We are picking the minPrice first and then calculate the maxProfit. Ideally we should have reverse order since with what we have - it may mean that we are selling the stocks on the same day.

0

Reply
A
AddedLimeCarp593
Top 1%
• 9 months ago

What makes this solution greedy and the DP solution to the longest increasing subsequence problem not greedy? Both are finding the "best" answer at a given index and using that to build up the final answer.

0

Reply
A
amit01112
Premium
• 9 months ago

I believe it is the backtracking. If you look at the solution of the above problem it iterates again on the already "seen" array to set the max length of increasing subsequence while greedy approach can't do that.

0

Reply
S
srirama.kusu
Premium
• 7 months ago

For Buy & Sell Stock, greedy works because just tracking the lowest price so far is enough — the best local choice always leads to the global best.

0

Reply
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Solution

Explanation

