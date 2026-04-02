# Fixed Length Sliding Window

> Source: https://www.hellointerview.com/learn/code/sliding-window/fixed-length
> Scraped: 2026-03-30


​
Sort By
Popular
Sort By
Summer Than
Premium
• 4 months ago

This section and its example problems should really come first in this module as it's simpler than variable-length sliding windows and easier for a beginner to grasp

15

Reply
dib
Premium
• 1 year ago

Could you pls add space/time complexity for Fixed Length window solutions?
Thanks

6

Reply
Semyon Gaivoronskiy
Premium
• 1 month ago

Hey! Thank you for the great content! It seems that the practice problems for the Fixed Size Sliding Window and the Variable Length Sliding Window are swapped in the left-hand menu. The “Longest Substring…” problems appear under the Fixed-Size section, while the “Max Points…” problems are listed under the Variable-Length section.

1

Reply

Shivam Chauhan

Admin
• 1 month ago

Hey! Thanks for pointing this out. You are right, the problems are swapped in the sections, this is fixed and will be updated in next release.

0

Reply
Daksh Gargas
Premium
• 2 months ago

This misses out the negative-numbered array since we're always starting maxSum with 0.

Try this out. (Lang: Go)

func maxSubarraySum(nums[] int, k int) int {
	if k > len(nums) { return 0 }
	windowSum := 0
	for i := 0; i < k; i ++ {
		windowSum += nums[i]
	}
	maxSum := windowSum
	for i := k; i < len(nums); i++ {
		windowSum -= nums[i - k]
		windowSum += nums[i]
		maxSum = max(maxSum, windowSum)
	}
	return maxSum
}

1

Reply
A
AmazingFuchsiaQuelea523
Premium
• 1 month ago

state has an overloaded meaning.  Better choice of variable name in this case would be running_sum.

0

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Fixed-Length Sliding Window

Problem: Maximum Sum of Subarray with Size K

Template

When Do I Use This?

Practice Problems

Fixed-Length
