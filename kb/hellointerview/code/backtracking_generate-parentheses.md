# Generate Parentheses

> Source: https://www.hellointerview.com/learn/code/backtracking/generate-parentheses
> Scraped: 2026-03-30



​
Sort By
Popular
Sort By
W
WispyOliveIguana961
Top 10%
• 11 months ago

Aren't we introducing unnecessary time overhead by storing our working path as a string? Each time we add a parenthesis to s we must recreate the string (since strings are immutable) in O(n). Wouldn't it be better for use to use a list? We can simply append to it in O(1).

9

Reply
S
sherry-dash-shower
Premium
• 2 months ago

Using a list also better demonstrates backtracking, since we have to pop as opposed to just creating immutable copies of things.

It's also odd that the suggested solution to previous problem ("Subsets") takes this approach, yet we go for the copy approach here.

1

Reply
Jordan Leal-Walker
• 3 days ago

Don't have to use push and pop. Can pre-allocate array length and use index assignment:

    generateParenthesis(n: number): string[] {
        const maxLen = n * 2;
        const result: string[] = [];
        const subset: string[] = new Array(maxLen);

        function backtrack(len: number, closedNeeded: number): void {
            if (len === maxLen) {
                if (closedNeeded === 0) result.push(subset.join(""));
                return;
            }

            if (closedNeeded < maxLen - len) {
                subset[len] = "(";
                backtrack(len + 1, closedNeeded + 1);
            }

            if (closedNeeded !== 0) {
                subset[len] = ")";
                backtrack(len + 1, closedNeeded - 1);
            }
        }

        backtrack(0, 0);
        return result;
    }
Show More

1

Reply
Muhammad Kamran Khan
• 2 months ago

using a list, we have to copy it and join it only at the base case.

if len(s) == 2 * n:
    res.append("".join(s))
    return

Am I correct?

0

Reply
S
sherry-dash-shower
Premium
• 1 month ago

Yup

0

Reply
dib
Premium
• 1 year ago

What is the space and time complexity for this one?

1

Reply
Jimmy Zhang
Top 5%
• 1 year ago

Good Q.

A loose upper bound for the time complexity is O(2 * 2^n), where n is the number of parentheses we are trying to pair. You can visualize as the solution space tree without pruning any of the invalid parenthesis. The tree will have a height of 2 * n, so there will be a total of 2 * 2^n of nodes in the tree.

It's possible to calculate a tighter bound, but it's very math heavy and I wouldn't expect that you have to know how to do that for the coding interview.

I'll add a visual to make this easier to visualize when I get a chance. Let me know if that helps!

6

Reply
A
AddedLimeCarp593
Top 1%
• 9 months ago

If the height is 2N, then why isn't the complexity upper bound O(2^(2N))? Branching factor raised to the power of the height.

1

Reply
dib
Premium
• 1 year ago

Thank you.

0

Reply
W
WillowyBlushCephalopod239
Premium
• 1 month ago

Solution that involves tracking the opening and closing parentheses, and stores the current representation of parentheses as a list of chars

class Solution:
    def generateParenthesis(self, n: int):
        # Your code goes here
        res = []
        def backtrack(head, tail, curr):
            if head == tail == n:
                res.append("".join(curr))
                return
            
            if head < n:
                curr.append("(")
                backtrack(head+1, tail, curr)
                curr.pop()
            
            if tail < head:
                curr.append(")")
                backtrack(head, tail+1, curr)
                curr.pop()

        backtrack(0, 0, [])
        return res
Show More

0

Reply
S
sherry-dash-shower
Premium
• 2 months ago

You can just compare closed to n instead of multiplying n for every recursive call. At the very least you can stick n * 2 in a var. For some languages this might get optimized into a constant, but still feels like bad form.

0

Reply
fz zy
Premium
• 2 months ago
class Solution:
    def generateParenthesis(self, n: int):
        ans = []
        stk = ['(']
        while stk:
            curr = stk.pop()
            if len(curr) == 2 * n:
                ans.append(curr)
                continue
            left = 0
            for c in curr:
                if c == '(':
                    left += 1
            if left < n:
                stk.append(curr + '(')
            if left > len(curr) - left:
                stk.append(curr + ')') 
        return ans   

0

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

Writing the Backtracking Function

