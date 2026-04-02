# Prefix Sum Overview

> Source: https://www.hellointerview.com/learn/code/prefix-sum/overview
> Scraped: 2026-03-30


Manish Aryal
Top 10%
• 1 year ago

in the example, you've written 21-13 instead of 21-8

19

Reply
L
LegalSilverMackerel516
• 1 year ago

typo instead of "We can note that the sum of that subarray (13) is the difference between the sum of two other subarrays (21 - 13)"
it should be "We can note that the sum of that subarray (13) is the difference between the sum of two other subarrays (21 - 8):"

8

Reply
G
gusandrianos
• 3 months ago

The first algorithm is easier to understand as this

public static int[] prefixSums(int[] arr) {
    int n = arr.length;
    int[] prefix = new int[n + 1];
    for (int i = 0; i < n; i++) {
        prefix[i+1] = prefix[i] + arr[i];
    }
    return prefix;
}

The next prefix sum is the current prefix sum and the current element. No need to start the loop from 1, go to n inclusively and subtract from the index.

1

Reply
EasonS
Premium
• 2 months ago

How this technique is used in real work? Can folks share the problem or system that require this technique

0

Reply
Ashutosh Kumar
Premium
• 29 days ago

I haven’t used them practically, but a few of the use cases I could think of are:

Precomputing cumulative metrics to answer range queries(for eg - revenue may be :( )
Running debit/credit totals, average balance between dates, quarterly summaries.
Rate limiting & traffic monitoring ; Counting requests in the last X seconds using cumulative counters.
2D grids (image/heatmaps); Constant-time area sum queries using 2D prefix sums.

1

Reply
Yves Sy
Premium
• 6 months ago

is the last visualization incorrect? Shoudn’t it be:
prefix[0] = arr[0] for the first element of the prefix sum?

0

Reply
W
WispyApricotWren649
• 4 months ago

No. The value for the first index of prefix sum is 0 which means we have not started to scan the arr yet. This way, if you want to have sum of elemnts 0 to 0 you can just do prefix[1] - prefix[0]

1

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Calculating Prefix Sums

Time Complexity

Practice Problems
