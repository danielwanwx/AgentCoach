# Set Matrix Zeroes

> Source: https://www.hellointerview.com/learn/code/matrices/set-matrix-zeroes
> Scraped: 2026-03-30


Write a function to modify an m x n integer matrix matrix directly, such that if any element in the matrix is 0, its entire corresponding row and column are set to 0. This transformation should be done in place, without using any additional data structures for storage.

Input:

matrix = [
    [0,2,3],
    [4,5,6],
    [7,8,9]
]

Output:

[
    [0,0,0],
    [0,5,6],
    [0,8,9]
]

Explanation: Since the element at the first row and first column is 0, set all elements in the first row and first column to 0.

CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
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

Understanding the Problem
The naive approach would use O(m + n) extra space by storing which rows and columns need to be zeroed in separate sets. But we can do better by using the matrix itself as storage.
1
1
1
1
0
1
1
1
1
→
1
0
1
0
0
0
1
0
1
Input
Output
Use the Matrix Itself!
Instead of extra arrays, we can use the first row and first column as markers. When we find a zero at [i][j], we mark:
matrix[i][0] = 0 → "row i needs to be zeroed"
matrix[0][j] = 0 → "column j needs to be zeroed"
col 0
col 1
col 2
row 0
row 1
row 2
First row/column = markers
matrix[i][0] = 0 means
"zero out row i"
matrix[0][j] = 0 means
"zero out column j"
But there's a catch! If we modify the first row/column while scanning, we'll lose information about whether they originally had zeros. So we save that first.
Walkthrough
Let's trace through matrix = [[1,1,1],[1,0,1],[1,1,1]]:
Step 1: Save first row/column state
Check if the first row or column originally contains any zeros. Save in boolean flags.
1
1
1
1
0
1
1
1
1
Step 1:
Check highlighted cells
firstRowZero = false
firstColZero = false
(no zeros in first row/col)
Step 2: Mark zeros using first row/column
Scan the inner matrix [1:][1:]. When we find a zero, mark the corresponding first row and first column cells.
1
0
1
0
0
1
1
1
1
Step 2:
Found 0 at [1][1]
→ Set matrix[1][0] = 0
→ Set matrix[0][1] = 0
(markers for row 1 & col 1)
Step 3: Zero the inner matrix
Use the markers to zero out cells. If matrix[i][0] == 0 or matrix[0][j] == 0, set matrix[i][j] = 0.
1
0
1
0
0
0
1
0
1
Step 3:
Zero based on markers:
Row 1: all zeros
Col 1: all zeros
(check matrix[i][0] & matrix[0][j])
Step 4: Handle first row/column
If our saved flags indicate the first row/column originally had zeros, zero them now.
1
0
1
0
0
0
1
0
1
Step 4:
firstRowZero = false
firstColZero = false
→ No changes needed
✓ Done!
The order is crucial: we must save the first row/column state before using them as markers, and zero them last so we don't corrupt the markers we're reading.
Solution
matrix
​
|
matrix
2d-list of integers
Try these examples:
No Zeros
Multiple Zeros
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def setZeroes(matrix):
    rows, cols = len(matrix), len(matrix[0])
    first_row_zero = any(matrix[0][j] == 0 for j in range(cols))
    first_col_zero = any(matrix[i][0] == 0 for i in range(rows))

    for i in range(1, rows):
        for j in range(1, cols):
            if matrix[i][j] == 0:
                matrix[i][0] = 0
                matrix[0][j] = 0

    for i in range(1, rows):
        for j in range(1, cols):
            if matrix[i][0] == 0 or matrix[0][j] == 0:
                matrix[i][j] = 0

    if first_row_zero:
        for j in range(cols):
            matrix[0][j] = 0

    if first_col_zero:
        for i in range(rows):
            matrix[i][0] = 0
1
1
1
1
0
1
1
1
1
firstRowZero = false
firstColZero = false

Set Matrix Zeroes - O(1) space solution

0 / 15

1x
What is the time complexity of this solution?
1

O(m × n)

2

O(x * y)

3

O(m * n * 4^L)

4

O(V + E)

Mark as read

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

(19)

Comment
Anonymous
​
Sort By
Popular
Sort By
C
ConcernedAzureWhale369
• 1 year ago

The problem statement says: "without using any additional data structures for storage" (which differs from the problem statement on LeetCode), and then it uses "zero_rows, zero_cols"?

10

Reply
Jimmy Zhang
Top 5%
• 1 year ago

yeah you're right great catch! That's an oversight on my part. I'll be updating the problem description and the solution to show solutions in terms of more and more optimal space complexities when I can.

0

Reply
P
PreliminaryGreenGecko935
Premium
• 10 months ago

The issue still exists.

a. Description still says -- "This transformation should be done in place, without using any additional data structures for storage."
b. The optimal solution that uses O(1) space is still not provided.

8

Reply
Sahil Singh
• 7 months ago

You can do it this way:

Iterate through matrix
If you find 0 value, set the value of non-zero elements in the corresponding row and column to 'X'.
Iterate again and set the 'X' to 0

1

Reply
G
GreatMagentaChimpanzee521
Premium
• 4 months ago

This will not work.
lets suppose you have 0 at (0,0) index and this make first row as 0 . then while checking 2nd row. you will also mark this 0 as complete first row now become 0.
So this is incorrect.
Better way to do it is not to process 1st row and 1st column and use that to store which row or column to make zero.
and process them in last.

0

Reply
Yoel Feuermann (BladeFistX2)
• 5 months ago

That will work but will be very slow. Since you will be hitting the zeros you created, and re iterating them over and over again.

0

Reply
Thomas Bao
Premium
• 1 year ago

This solution does not use constant space.  It creates 2 sets to track the columns and rows to zero and the total size of the sets is O(n + m)

7

Reply
Burhan
• 1 year ago

You can use first row and col instead of sets. For the first column, you can create a boolean flag.

3

Reply
A
ArchitecturalPlumReptile288
Premium
• 10 months ago

The space complexity is not O(1) since you used zero_rows, zero_cols.

1

Reply
G
GloriousLavenderLark534
• 1 year ago

Space complexity is worst case O(max(m,n)). To avoid adding space with m or n, we can treat one row (the first) as a lookup for any columns that will be zeroed (instead of zero_cols), and the same for rows (so , no zero_rows). The only thing to note is that these will require special treatment--using an extra pair of booleans to indicate whether these initially had any zero cells respectively, avoiding them while iterating cells, and finally using said booleans to zero them if required.

1

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Understanding the Problem

Use the Matrix Itself!

Walkthrough

Step 1: Save first row/column state

Step 2: Mark zeros using first row/column

Step 3: Zero the inner matrix

Step 4: Handle first row/column

Solution
