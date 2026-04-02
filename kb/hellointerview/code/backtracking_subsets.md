# Subsets

> Source: https://www.hellointerview.com/learn/code/backtracking/subsets
> Scraped: 2026-03-30



​
Sort By
Popular
Sort By
L
LesserTanMite551
Top 10%
• 1 year ago

I dont know why but this one is really hard to visualize in head. Can you add the interactive visualization to this one pls?

21

Reply
D
DoubleHarlequinMink620
• 1 year ago

I agree, Is it possible to add the visualizations for this problem.

6

Reply
R
RadicalAquaBedbug232
Top 10%
• 1 year ago

Would be nice to include complexity analysis

5

Reply
A
Anatoly
Premium
• 7 months ago

Is complexity here O(n * 2^n) ?

3

Reply
Sayan Sarkar
Top 10%
• 7 months ago

Yes, it is be O(2^n * n).

0

Reply
Hieronim Kubica
Premium
• 7 months ago

I think so - 2^n quite obvious since at each index you branch out based on the 2 choices you have - include or exclude. The n factor because of creating a subset copy in the base case.

0

Reply
saurabh vaidya
• 5 months ago

can someone please explain why tweaking the above solution not work?

original

            # include nums[index]
            path.append(nums[index])
            dfs(index + 1, path)

            # exclude nums[index]
            path.pop()
            dfs(index + 1, path)

Tweak: calling order

            # call exclude first
            dfs(index + 1, path)
            # include nums[index]
            path.append(nums[index])
            dfs(index + 1, path)

Show More

1

Reply
C
ClearAquaAphid538
Premium
• 4 months ago

Because path is a shared mutable list. In the tweaked version you append after the “exclude” branch, so that change isn’t undone and affects later calls. You need to add a pop() at the end to restore path.

1

Reply
Muhammad Kamran Khan
• 2 months ago
• edited 2 months ago

may be this help you:

        result = []

        def backtrack(path: List[int], idx: int) -> None:
            if len(nums) == idx:
                result.append(path)
                return

            backtrack(path.copy(), idx + 1)
            path.append(nums[idx])
            backtrack(path.copy(), idx + 1)

        backtrack([], 0)
        return result

lists in python are passed as reference.

0

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

Step 1 (first element)

Step 2 (second element)

Step 3 (third element)

Writing the Backtracking Function

