# Flood Fill

> Source: https://www.hellointerview.com/learn/code/depth-first-search/flood-fill
> Scraped: 2026-03-30



Given a m x n integer grid image and integers sr, sc, and newColor, write a function to perform a flood fill on the image starting from the pixel image[sr][sc].

In a 'flood fill', start by changing the color of image[sr][sc] to newColor. Then, change the color of all pixels connected to image[sr][sc] from either the top, bottom, left or right that have the same color as image[sr][sc], along with all the connected pixels of those pixels, and so on.

Input:

image = [[1,0,1],[1,0,0],[0,0,1]], sr = 1, sc = 1, color = 2

Output:

[[1,2,1],[1,2,2],[2,2,1]]

The zeroes connected to the starting pixel (1, 1) are colored with the new color (2).

CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def flood_fill(self, image: List[List[int]], sr: int, sc: int, 
    color: int) -> List[List[int]]:
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
This solution uses depth-first search to traverse the grid and perform the flood fill by defining a recursive function dfs that takes in the current row and column of the pixel being explored. Each call to dfs will either change the color of the pixel if the pixel is the same color as the starting pixel, and then recursively call dfs on its connected pixels. If the pixel is not the same color as the starting pixel, the function will return without doing anything.
The algorithm starts at the given starting pixel and uses depth-first search to explore all pixels connected 4-directionally to it. At each pixel, it first checks to see if the pixel is the same color as the starting pixel. If it is, it changes the color of the pixel and continues to explore the connected pixels.
VISUALIZATION
Python
Language
Full Screen
def flood_fill(image, sr, sc, color):
    rows, cols = len(image), len(image[0])
    original_color = image[sr][sc]
    
    if original_color == color:
        return image
        
    def dfs(r, c):
        if image[r][c] == original_color:
            image[r][c] = color
            
            if r >= 1: dfs(r - 1, c)
            if r + 1 < rows: dfs(r + 1, c)
            if c >= 1: dfs(r, c - 1)
            if c + 1 < cols: dfs(r, c + 1)
        return
        
    dfs(sr, sc)
    return image
def dfs(r, c):
    if image[r][c] == original_color:
        image[r][c] = color
        
        if r >= 1: dfs(r - 1, c)
        if r + 1 < rows: dfs(r + 1, c)
        if c >= 1: dfs(r, c - 1)
        if c + 1 < cols: dfs(r, c + 1)
    return
1
0
1
1
2
0
0
0
1
r = 1c = 1
color: 2
original_color: 0

update color

0 / 2

1x
Setting the color of connected pixels.
After changing that pixel's color, the algorithm will continue to explore the connected pixels of that pixel. Whenever it encounters a pixel that is not the same color as the starting pixel, it will return immediately and backtrack to the previous pixel on the call stack, which will then continue to explore its remaining connected pixels.
VISUALIZATION
Python
Language
Full Screen
def flood_fill(image, sr, sc, color):
    rows, cols = len(image), len(image[0])
    original_color = image[sr][sc]
    
    if original_color == color:
        return image
        
    def dfs(r, c):
        if image[r][c] == original_color:
            image[r][c] = color
            
            if r >= 1: dfs(r - 1, c)
            if r + 1 < rows: dfs(r + 1, c)
            if c >= 1: dfs(r, c - 1)
            if c + 1 < cols: dfs(r, c + 1)
        return
        
    dfs(sr, sc)
    return image
def dfs(r, c):
    if image[r][c] == original_color:
        image[r][c] = color
        
        if r >= 1: dfs(r - 1, c)
        if r + 1 < rows: dfs(r + 1, c)
        if c >= 1: dfs(r, c - 1)
        if c + 1 < cols: dfs(r, c + 1)
    return
def dfs(r, c):
    if image[r][c] == original_color:
        image[r][c] = color
        
        if r >= 1: dfs(r - 1, c)
        if r + 1 < rows: dfs(r + 1, c)
        if c >= 1: dfs(r, c - 1)
        if c + 1 < cols: dfs(r, c + 1)
    return
def dfs(r, c):
    if image[r][c] == original_color:
        image[r][c] = color
        
        if r >= 1: dfs(r - 1, c)
        if r + 1 < rows: dfs(r + 1, c)
        if c >= 1: dfs(r, c - 1)
        if c + 1 < cols: dfs(r, c + 1)
    return
1
2
1
1
2
0
0
0
1
r = 1c = 1
color: 2
original_color: 0

recursive call

0 / 6

1x
Backtracking to the previous pixel
The algorithm will continue to explore the connected pixels of the starting pixel until it has explored all connected pixels of the start pixel.
Animated Solution
image
​
|
image
2d-list of integers
sr
​
|
sr
integer
sc
​
|
sc
integer
color
​
|
color
integer
Try these examples:
No Change
Small Fill
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def flood_fill(image, sr, sc, color):
    rows, cols = len(image), len(image[0])
    original_color = image[sr][sc]
    
    if original_color == color:
        return image
        
    def dfs(r, c):
        if image[r][c] == original_color:
            image[r][c] = color
            
            if r >= 1: dfs(r - 1, c)
            if r + 1 < rows: dfs(r + 1, c)
            if c >= 1: dfs(r, c - 1)
            if c + 1 < cols: dfs(r, c + 1)
        return
        
    dfs(sr, sc)
    return image
1
0
1
1
0
0
0
0
1
color: 2

flood fill

0 / 39

1x
Complexity Analysis
For this problem, let m be the number of rows and n be the number of columns in the grid.
What is the time complexity of this solution?
1

O(log m * n)

2

O(4ⁿ)

3

O(V + E)

4

O(m * n)

Mark as read

Next: Number of Islands

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

(18)

Comment
Anonymous
​
Sort By
Popular
Sort By
Abhay Singh
Top 1%
• 1 year ago

Java Solution:

class Solution {

    public void dfs(int[][] image, int i, int j, int matchingColor, int[][] dxy){
        int n = image.length;
        int m = image[0].length;

        if(i<0 || j<0 || i==n || j==m || image[i][j] != matchingColor) return;

        image[i][j] = -1;
        for(int k=0;k<4;k++){
            int x=i+dxy[k][0], y=j+dxy[k][1];
            dfs(image, x, y, matchingColor, dxy);
        }
    }

    public int[][] floodFill(int[][] image, int sr, int sc, int color) {
        int n = image.length;
        int m = image[0].length;

        int[][] dxy = {{-1,0}, {0,1}, {1,0}, {0,-1}};

        dfs(image, sr, sc, image[sr][sc], dxy);
        for(int i=0;i<n;i++){
            for(int j=0;j<m;j++){
                if(image[i][j] == -1) image[i][j] = color;
            }
        }

        return image; 
    }
}
Show More

3

Reply
N
NaturalSilverDolphin574
Premium
• 1 year ago

I feel using BFS for this problem was more intuitive for me

/**
 * @param {number[][]} image
 * @param {number} sr
 * @param {number} sc
 * @param {number} color
 * @return {number[][]}
 */
var floodFill = function(image, sr, sc, color) {
    const visited = new Set()
    const target = image[sr][sc];
    const queue = [[sr, sc]]
    const isOutOfBounds = (y, x) => y < 0 || x < 0 || y >= image.length || x >= image[0].length

    while (queue.length) {
        const [y, x] = queue.shift()
        if (isOutOfBounds(y, x) || image[y][x] !== target || visited.has(`${y},${x}`)) continue
        
        // update color, add to set to avoid revisiting
        visited.add(`${y},${x}`)
        image[y][x] = color
        
        // move right, left, up, down
        for (const [dx, dy] of [[0,1], [0,-1], [1,0], [-1,0]]) 
            queue.push([y + dy, x + dx])
    }
    
    return image
};
Show More

3

Reply
Satya Dasara
Premium
• 2 months ago

When exploring with DFS we need to explore neighboring nodes only if :

Satisfying boundary ranges
Not in visited set
Have same color as original color of image[sr][sc]
class Solution:
    def floodFill(self, image: List[List[int]], sr: int, sc: int, color: int):
        
        directions = [(1,0), (-1,0), (0, 1), (0, -1)]
        R = len(image)
        C = len(image[0])
        visited = set()
        original_color = image[sr][sc]
        
        def dfs(image, sr, sc, color):
            
            image[sr][sc] = color
            
            nonlocal visited
            visited.add((sr, sc))

            nonlocal original_color
            nonlocal directions

            for direction in directions:
                dx, dy = direction
                nr = sr + dx
                nc = sc + dy

                if nr >= R or nr < 0 or nc >=C or nc < 0:
                    pass
                elif (nr, nc) not in visited and image[nr][nc] == original_color:
                    dfs(image, nr, nc, color)
            
        
        dfs(image, sr, sc, color)

        return image
Show More

1

Reply
Thanh Nguyễn
Premium
• 1 month ago
• edited 1 month ago

Yes your intuition is correct, however we could remove visited set - we can check if the color of the current node is similar to the original color or not -> this can also check if a node is visited and its color is changed without the need of an extra set.

0

Reply
Ashley Yeong
Premium
• 2 months ago

missing <Next: Types of DFS> page.

1

Reply
Nachiket Galande
Premium
• 11 days ago

Can the Time and Space Complexity be added at the end?

0

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

Animated Solution

Complexity Analysis
