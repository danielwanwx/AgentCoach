# Spiral Matrix

> Source: https://www.hellointerview.com/learn/code/matrices/spiral-matrix
> Scraped: 2026-03-30


Write a function to traverse an m x n matrix in spiral order and return all elements in a single list. The traversal should start from the top left corner and proceed clockwise, spiraling inward until every element has been visited.

Input:

matrix = [
    [0,1,2],
    [3,4,5],
    [6,7,8]
]

Output:

[0,1,2,5,8,7,6,3,4]

Explanation: The elements of the matrix are returned in the order they are visited in a clockwise spiral starting from the top left corner.

CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def spiral_order(self, matrix: List[List[int]]) -> List[int]:
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
This solution uses 4 steps to traverse the matrix in spiral order:
1. Top Row
The first step is to pop the first row of the matrix, while copying those elements into the result array from left to right.
VISUALIZATION
Python
Language
Full Screen
from collections import deque

def spiral_order(matrix):
    matrix = deque(deque(row) for row in matrix)
    result = []
    while matrix:
        result += matrix.popleft()
        if matrix and matrix[0]:
            for row in matrix:
                result.append(row.pop())
        if matrix:
            result += reversed(matrix.pop())
        if matrix and matrix[0]:
            for row in reversed(matrix):
                result.append(row.popleft())
    return result
0
1
2
3
4
5
6
7
8
result
[]

initialize result

0 / 1

1x
2. Right Column
Next, we traverse the right column of the matrix, popping the last element of each remaining row in matrix and copying those elements into the result array from top to bottom.
VISUALIZATION
Python
Language
Full Screen
from collections import deque

def spiral_order(matrix):
    matrix = deque(deque(row) for row in matrix)
    result = []
    while matrix:
        result += matrix.popleft()
        if matrix and matrix[0]:
            for row in matrix:
                result.append(row.pop())
        if matrix:
            result += reversed(matrix.pop())
        if matrix and matrix[0]:
            for row in reversed(matrix):
                result.append(row.popleft())
    return result
3
4
5
6
7
8
result
[0,1,2]

traverse top row

0 / 2

1x
3. Bottom Row
Next, we traverse the bottom row of the matrix, popping the last row of matrix and copying those elements into the result array from right to left.
VISUALIZATION
Python
Language
Full Screen
from collections import deque

def spiral_order(matrix):
    matrix = deque(deque(row) for row in matrix)
    result = []
    while matrix:
        result += matrix.popleft()
        if matrix and matrix[0]:
            for row in matrix:
                result.append(row.pop())
        if matrix:
            result += reversed(matrix.pop())
        if matrix and matrix[0]:
            for row in reversed(matrix):
                result.append(row.popleft())
    return result
3
4
6
7
result
[0,1,2,5,8]

traverse right column

0 / 1

1x
4. Left Column
Finally, we traverse the left column of the matrix, popping the first element of each remaining row in matrix and copying those elements into the result array from bottom to top.
VISUALIZATION
Python
Language
Full Screen
from collections import deque

def spiral_order(matrix):
    matrix = deque(deque(row) for row in matrix)
    result = []
    while matrix:
        result += matrix.popleft()
        if matrix and matrix[0]:
            for row in matrix:
                result.append(row.pop())
        if matrix:
            result += reversed(matrix.pop())
        if matrix and matrix[0]:
            for row in reversed(matrix):
                result.append(row.popleft())
    return result
3
4
result
[0,1,2,5,8,7,6]

traverse bottom row

0 / 1

1x
Repeat
At this point, we have traversed the perimeter of the original matrix in a clockwise spiral order. We repeat the process for the inner submatrix, until there are no more elements left to traverse.
VISUALIZATION
Python
Language
Full Screen
from collections import deque

def spiral_order(matrix):
    matrix = deque(deque(row) for row in matrix)
    result = []
    while matrix:
        result += matrix.popleft()
        if matrix and matrix[0]:
            for row in matrix:
                result.append(row.pop())
        if matrix:
            result += reversed(matrix.pop())
        if matrix and matrix[0]:
            for row in reversed(matrix):
                result.append(row.popleft())
    return result
4
result
[0,1,2,5,8,7,6,3]

traverse left column

0 / 2

1x
Solution
matrix
​
|
matrix
2d-list of integers
Try these examples:
2x2
4x4
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
from collections import deque

def spiral_order(matrix):
    matrix = deque(deque(row) for row in matrix)
    result = []
    while matrix:
        result += matrix.popleft()
        if matrix and matrix[0]:
            for row in matrix:
                result.append(row.pop())
        if matrix:
            result += reversed(matrix.pop())
        if matrix and matrix[0]:
            for row in reversed(matrix):
                result.append(row.popleft())
    return result
0
1
2
3
4
5
6
7
8

spiral matrix

0 / 8

1x
What is the time complexity of this solution?
1

O(m * n)

2

O(N + Q)

3

O(n log n)

4

O(log n)

Mark as read

Next: Rotate Image

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

(20)

Comment
Anonymous
​
Sort By
Popular
Sort By
Sean Tarzy
Top 5%
• 1 year ago

here is a javascript solution that treats it like a snake game. for simple-minded folk like me:

function spiralOrder(matrix: number[][]): number[] {
    let spiral = [matrix[0][0]]

    let matrixRowStart = 0 
    let matrixColStart = 0

    let currentMatrixRow = 0
    let currentMatrixCol = 0  

    let matrixColEnd = matrix[0].length -1 
    let matrixRowEnd = matrix.length -1 
    let direction: "left" | "right" | "up" | "down" | "end" = "right"
    if(matrix[0].length === 1){
        // if we have a one-column matrix, our first move will be down
        direction = "down"
    }
    let matrixSize = matrix.length * matrix[0].length
    while( matrixSize > spiral.length){
        // until we have our spiral array of matching size to our matrix input (we need all the elments)
        switch(direction){
            case "right":
                 currentMatrixCol++
                 if(currentMatrixCol >= matrixColEnd){
                    currentMatrixCol = matrixColEnd
                    direction = "down"
                    // when we've taken a turn down, our matrix row start increases
                    // - we have shrinking barriers throughout the traversal 
                    matrixRowStart++
                 }
                 break;
            case "down": 
                currentMatrixRow++
                if(currentMatrixRow >= matrixRowEnd){
                    direction = "left"
                    matrixColEnd--
                }
                break;
            case "left": 
                currentMatrixCol--
                if(currentMatrixCol === matrixColStart){
                    direction = "up"
                    matrixRowEnd--
                }
                break
            case "up": 
                currentMatrixRow--
                  if(currentMatrixRow === matrixRowStart){
                    direction = "right"
                    matrixColStart++
                }
                break
            default: 
                break
        }
       spiral.push(matrix[currentMatrixRow][currentMatrixCol])
        
    }
    return spiral
};
Show More

11

Reply
A
Anatoly
Premium
• 7 months ago

Same principle but with little tweaks

/**
 * @param {number[][]} matrix
 * @return {number[]}
 */
var spiralOrder = function(matrix) {
    if (!matrix || !matrix[0]) {
        return [];
    }

    // right down left up
    const directions = [[0, 1], [1, 0], [0, -1], [-1, 0]];

    const rows = matrix.length;
    const cols = matrix[0].length;

    let row = 0;        // Current row
    let col = 0;        // Current column
    let direction = 0;  // Current direction
    let rowsParsed = 0; // Full rows parsed
    let colsParsed = 0; // Full columns parsed
    let segment = cols; // How many items to add before direction change

    const result = [];

    for (i = 0; i < rows * cols; i++) {
        result[i] = matrix[row][col];   // Adding current item
        segment--;  // Decreasing count

        // Need to change direction
        if (segment === 0) {
            if (direction % 2 === 0) {
                rowsParsed++;   // Horizontal direction - full row parsed
            }
            else {
                colsParsed++;   // Vertical direction - full column parsed
            }

            // Change direction (90 degreees clockwise)
            direction = (direction === 3) ? 0 : direction + 1;

            // New segment length
            segment = (direction % 2 === 0) ? cols - colsParsed : rows - rowsParsed;
        }

        // Move pointers
        row += directions[direction][0];
        col += directions[direction][1];
    }

    return result;
};
Show More

0

Reply
F
FancyBrownHerring325
• 1 year ago

The += operation is not of constant time complexity. It creates a new list containing the LHS + RHS.  The extra copy operation moves this from linear in the number of matrix entries to quadratic.

4

Reply
A
AdvisoryApricotErmine448
• 1 month ago

The solution code is different in code editor answer & explanation sections. First is based on arrays & second is list.

2

Reply
S
srirama.kusu
Premium
• 7 months ago
# TC: O(m*n) and SC: O(m*n)
class Solution:
    def spiral_order(self, matrix: List[List[int]]):
        min_col = 0
        max_col = len(matrix[0])
        min_row = 0
        max_row = len(matrix)
        output = []

        while min_col < max_col and min_row < max_row:
            # right ->
            for col in range(min_col, max_col):
                output.append(matrix[min_row][col])
            min_row += 1 # Shrink top boundary
            
            # down !
            for row in range(min_row, max_row):
                output.append(matrix[row][max_col - 1])
            max_col -= 1 # Shrink right boundary

            # left <-
            if min_row < max_row: # check if there is still a row to traverse
                for col in range(max_col - 1, min_col - 1, - 1):
                    output.append(matrix[max_row - 1][col])
                max_row -= 1 # Shrink bottom boundary
            
            # top ^
            if min_col < max_col: # check if there is still a col to traverse
                for row in range(max_row - 1, min_row - 1, -1):
                    output.append(matrix[row][min_col])
                min_col += 1 # Shrink left boundary
        return output
Show More

2

Reply
T
TinyBrownMole852
Premium
• 4 days ago

Great solution, but should copy the matrix into a deque first. The solution provided isn't O(mn) given .pop(0), but deque implementation would be O(mn) since popleft() is O(1) . Converting matrix to deque has O(mn) cost, but doesn't change complexity, and we're using O(mn) space complexity already given the result space.

1

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

1. Top Row

2. Right Column

3. Bottom Row

4. Left Column

Repeat

Solution
