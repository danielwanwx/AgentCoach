# Rotate Image

> Source: https://www.hellointerview.com/learn/code/matrices/rotate-image
> Scraped: 2026-03-30


Write a function to rotate an n x n 2D matrix representing an image by 90 degrees clockwise. The rotation must be done in-place, meaning you should modify the input matrix directly without using an additional matrix for the operation.

Input:

matrix = [
    [1,4,7],
    [2,5,8],
    [3,6,9]
]

Output:

[
    [3,2,1],
    [6,5,4],
    [9,8,7]
]

Explanation: The matrix is rotated by 90 degrees clockwise, transforming its columns into rows in reverse order.

CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def rotate_image(self, matrix: List[List[int]]) -> None:
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
This problem can be done in two steps. We first transpose the matrix, then reverse the elements in each row.
Step 1:
Transpose the matrix by swapping the elements across the diagonal. This can be done in-place by using a nested for loop to swap the elements.
VISUALIZATION
Python
Language
Full Screen
def rotate_image(matrix):
    n = len(matrix)

    # Transpose the matrix
    for i in range(n):
        for j in range(i, n):
            matrix[i][j], matrix[j][i] = \
                matrix[j][i], matrix[i][j]

    # Reverse each row
    for i in range(n):
        matrix[i] = matrix[i][::-1]
    return matrix
1
4
7
2
5
8
3
6
9

n = 3

0 / 12

1x
Step 2:
Reverse the elements in each row of the matrix.
VISUALIZATION
Python
Language
Full Screen
def rotate_image(matrix):
    n = len(matrix)

    # Transpose the matrix
    for i in range(n):
        for j in range(i, n):
            matrix[i][j], matrix[j][i] = \
                matrix[j][i], matrix[i][j]

    # Reverse each row
    for i in range(n):
        matrix[i] = matrix[i][::-1]
    return matrix
1
4
7
2
5
8
3
6
9
i = 2j = 2

swap matrix[2][2] and matrix[2][2]

0 / 4

1x
Solution
matrix
​
|
matrix
2d-list of integers
Try these examples:
2x2
3x3
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def rotate_image(matrix):
    n = len(matrix)

    # Transpose the matrix
    for i in range(n):
        for j in range(i, n):
            matrix[i][j], matrix[j][i] = \
                matrix[j][i], matrix[i][j]

    # Reverse each row
    for i in range(n):
        matrix[i] = matrix[i][::-1]
    return matrix
1
4
7
2
5
8
3
6
9

rotate image

0 / 17

1x
What is the time complexity of this solution?
1

O(2ⁿ)

2

O(4ⁿ)

3

O(n²)

4

O(n log n)

Mark as read

Next: Set Matrix Zeroes

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

(11)

Comment
Anonymous
​
Sort By
Popular
Sort By
S
SoftGrayFirefly749
• 1 year ago

matrix[i] = matrix[i][::-1] creates a copy of the row and reverses that. It will use O(n) space for the duration of the iteration, which would then be (presumably) garbage collected when the iteration is done. matrix[i].reverse() is in place and doesn't use the extra space (i.e. it's O(1)).
Does it matter? Probably not. Might be good to mention during an interview though.

12

Reply
Alexandru-Ionuț Mustață
Premium
• 10 months ago

Another solution using in place swapping of elements of the matrix:

class Solution:
    def rotate_image(self, matrix: list[list[int]]):
        n = len(matrix)
        for i in range(0, n):
            for j in range(i + 1, n - i):
                aux = matrix[i][j]
                matrix[i][j] = matrix[n - 1 - j][i]
                matrix[n - 1 - j][i] = matrix[n - 1 - i][n - 1 - j]
                matrix[n - 1 - i][n - 1 - j] = matrix[j][n - 1 - i]
                matrix[j][n - 1 - i] = aux

        return matrix

3

Reply
J
jitendra
Premium
• 2 months ago

Doesn't matrix[i] = matrix[i][::-1] create a copy? Here is my in-place solution using pointers.

def rotate(self, matrix: List[List[int]]) -> None:
    """
    Do not return anything, modify matrix in-place instead.
    """
    n = len(matrix)
    # in-place transpose
    for r in range(n):
        for c in range(r + 1, n):
            matrix[r][c], matrix[c][r] = matrix[c][r], matrix[r][c]

    # in-place reverse of each row
    for row in matrix:
        left, right = 0, n - 1
        while left < right:
            row[left], row[right] = row[right], row[left]
            left += 1
            right -= 1
Show More

2

Reply
Satya Dasara
Premium
• 2 months ago

The main trick here is knowing that for Transpose the nested column starts from row + 1

class Solution:
    def rotate_image(self, matrix: List[List[int]]):
        R = len(matrix)
        C = len(matrix[0])

        for r in range(R):
            for c in range(r+1, C):
                if r == c:
                    continue
                
                temp = matrix[r][c]
                matrix[r][c] = matrix[c][r]
                matrix[c][r] = temp
    

        for idx, row in enumerate(matrix):
            # matrix[idx] = matrix[idx][::-1] 
            matrix[idx].reverse()
        
        return matrix
Show More

0

Reply
Asaf Miller
Premium
• 2 months ago

my solution that uses O(n) space and O(n^2) time complexity of course, it is pretty easy to understand if you ask me

rotate_image(matrix: number[][]): void {
        var n = matrix.length;
        var flatMatrix = matrix.flat();
        for (var i = 0; i< n; i++) {
            var newRow = [];
            for (var j = n-1; j> -1; j--) {
                newRow.push(flatMatrix[i+j*n]);
            }
            matrix[i] = newRow;
        }
    }

0

Reply
Prateik D
Premium
• 5 days ago

no interviewer will accept this :P

0

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

Step 1:

Step 2:

Solution
