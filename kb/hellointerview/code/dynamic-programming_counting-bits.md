# Counting Bits

> Source: https://www.hellointerview.com/learn/code/dynamic-programming/counting-bits
> Scraped: 2026-03-30



hassan mohagheghian
• 6 months ago

Also, we can solve this problem with bit manipulation.

def count_bits(n: int) -> list[int]:
    res = [0] * (n + 1)
    for i in range(n + 1):
        res[i] = res[i >> 1] + (i & 1)
    return res

10

Reply
E
ExpensiveFuchsiaSalmon151
• 8 months ago

Can we also support c# plz.

3

Reply
Michael Duren
Premium
• 2 months ago

Second this!

0

Reply
S
sherry-dash-shower
Premium
• 1 month ago
• edited 1 month ago

This feels like more a problem of testing your understanding of basic bit manipulation than dp.

For those of use using languages without the // operator, the recurrence relationship explanation is confusing. I'd just say "right shift" or use >> 1 which is both conceptually more accurate and more universal than a special integer division operator.

2

Reply
cst labs
Top 5%
• 1 month ago
• edited 1 month ago

A better approach is to leverage bit count:

public int[] count_bits(Integer n) {
       int[] result = new int[n+1];
       for (int i=1;i<=n;i++) {
           result[i] = result[i & (i-1)] + 1;
       }
       return result;
   }

0

Reply
Satya Dasara
Premium
• 1 month ago
• edited 1 month ago

Getting the idea for the recurrence relation is the tough part for DP

class Solution:
    def count_bits(self, n: int):

        dp = [0] * (n+1)
        
        for i in range(1, n+1):
            dp[i] = dp[i//2]+ (i%2)
        
        return dp

        """
        0 -> 0
        1 -> 1
        2 -> 10 = Bin(1)/[2//2] + 2%2
        3 -> 11 = Bin(1)/[3//2] + 3%2
        4 -> 100 = Bin(2)/[4//2] + 4%2
        5 -> 101 = Bin(2)/[5//2] + 5%2
        """
Show More

0

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

Solution

