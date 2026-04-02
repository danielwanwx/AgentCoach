# Word Search

> Source: https://www.hellointerview.com/learn/code/backtracking/word-search
> Scraped: 2026-03-30



S
StripedMagentaBarracuda334
• 8 months ago

Since we are pruning the direction that we are coming from using #, Isn't TC O(N * 3^L) here instead of  O(N * 4^L)?

9

Reply
Gaurav Verma
Top 10%
• 1 year ago

would have been nice if we can switch the programming language here. :(

9

Reply
S
Suraj
Top 5%
• 1 year ago

Need support for other languages specially Java here.

5

Reply
Zhanibek Bakin
• 1 year ago

same here, if you could add c++ as well, that would be great

2

Reply
Daniel Mai
Premium
• 1 month ago
        def backtrack(r: int, c: int, index: int, path: List[int]):
            if index == wordLen:
                return True
            
            if r < 0 or r >= rows \
                or c < 0 or c >= cols \
                or board[r][c] != word[index] \
                or (r, c) in path:
                return False

            path.append((r, c))
            isFound = backtrack(r + 1, c, index + 1, path) \
                    or backtrack(r - 1, c, index + 1, path) \
                    or backtrack(r, c + 1, index + 1, path) \
                    or backtrack(r, c - 1, index + 1, path)
            path.remove((r, c))

            return isFound

Instead of flipping the cell to '#', I personally found that do it by using extra path variable would be more clear? What would interviewer think about that during an interview?

Show More

1

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

Depth-First Search Function

Keeping Track of Visited Cells

Solution

