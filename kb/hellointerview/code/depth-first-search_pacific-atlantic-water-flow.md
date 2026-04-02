# Pacific Atlantic Water Flow

> Source: https://www.hellointerview.com/learn/code/depth-first-search/pacific-atlantic-water-flow
> Scraped: 2026-03-30


You are given an m x n matrix of non-negative integers representing a grid of land, where rain falls on every cell. Each value in the grid represents the height of that piece of land.

The Pacific Ocean touches the left and top edges of the matrix, while the Atlantic Ocean touches the right and bottom edges. Water can only flow from a cell to its neighboring cells directly north, south, east, or west, but only if the height of the neighboring cell is equal to or lower than the current cell.

1
2
2
3
3
2
3
4
3
2
4
5
3
2
4
5
Pacific
Atlantic
Pacific
Atlantic
Water can flow from grid[3][2] to the neighboring cells with a lower height.

Write a function to return a list of grid coordinates (i, j) where water can flow to both the Pacific and Atlantic Oceans. Water can flow from all cells directly adjacent to the ocean into that ocean.

Example 1:

Input:

grid = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
1
2
3
4
5
6
7
8
9
Pacific
Pacific
Atlantic
Atlantic
Water can flow from the cells with circles above to both the Pacific and Atlantic Oceans

Output:

[
    [0, 2],
    [1, 2],
    [2, 0],
    [2, 1],
    [2, 2]
]
CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def pacific_atlantic_flow(self, grid: List[List[int]]) -> List[List
    [int]]:
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
To solve this question, we need to traverse the grid to find all cells where water can flow to both the Pacific and Atlantic Oceans, and then find the cells that are contained in both those sets.
Approach 1: Brute Force Approach
Let's focus on how to find all the cells that are reachable from an ocean. One straightforward approach is to iterate over each cell in the graph, and then check if there is a valid path from that cell to the ocean. If there is, we can add it to a set (depending on if it reaches the Pacific or Atlantic Ocean). After iterating over each cell, we can return the intersection of those two sets.
SOLUTION
Python
Language
class Solution:
    def pacificAtlantic(self, matrix):
        if not matrix or not matrix[0]:
            return []

        rows, cols = len(matrix), len(matrix[0])
        pacific = set()
        atlantic = set()

        # Try to find a path from r, c to the Pacific or Atlantic ocean
        # via neighboring cells with lower heights
        def dfs(start_r, start_c, r, c, visited):
            if (r, c) in visited:
                return
            
            visited[(r, c)] = True

            if r == 0 or c == 0:
                pacific.add((start_r, start_c))
            if r == rows - 1 or c == cols - 1:
                atlantic.add((start_r, start_c))

            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] <= matrix[r][c]:
                    dfs(start_r, start_c, nr, nc, visited)
                    visited[(nr, nc)] = False

        # Perform full DFS from each cell.
        for r in range(rows):
            for c in range(cols):
                visited = {}
                dfs(r, c, r, c, visited)
                
        return list(pacific & atlantic)
The problem with this approach is that it is very inefficient. For each cell, we have to perform a full DFS traversal of the entire grid in the worst case, resulting in a run-time of O((m x n)2).
Approach 2: Boundary DFS
The brute-force approach is inefficient because there is a lot of repeat work being done. For example, we have to calculate parts of the same path multiple times as we check if there is a valid path from a cell to the ocean.
1
2
3
4
5
6
7
8
9
Pacific
Pacific
Atlantic
1
2
3
4
5
6
7
8
9
Pacific
Atlantic
1
2
3
4
5
6
7
8
9
Pacific
Atlantic
Atlantic
The three seperate calls to dfs in the brute-force solution above would calculate parts of the same path multiple times.
A more efficient approach is to use "boundary DFS". With this approach, we "invert" the problem by starting from all cells adjacent to each ocean, and then use DFS to find cells that can flow into that cell. All the cells that we visit during each of these traversals are the set of cells that can flow into the ocean that the DFS originated from.
This is more efficient because it reduces redundant work - once we visit a cell using this traversal, we can mark it as visited so it is not visited by future traversals.
At the end, we can return the intersection of both sets to get the final answer.
Solution
SOLUTION
Python
Language
class Solution:
    def pacific_atlantic_flow(self, grid): 
        if not grid or not grid[0]:
            return []

        rows, cols = len(grid), len(grid[0])
        # Step 1: Initialize empty sets
        pacific_reachable = set()
        atlantic_reachable = set()

        def dfs(r, c, reachable):
            reachable.add((r, c))
            for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if (nr, nc) not in reachable and grid[nr][nc] >= grid[r][c]:
                        dfs(nr, nc, reachable)

        # initializes DFS from all cells in the Atlantic and Pacific Oceans
        # Note how we share a single visited set
        # across DFS calls that originate from the same ocean
        for r in range(rows):
            dfs(r, 0, pacific_reachable)
            dfs(r, cols - 1, atlantic_reachable)

        for c in range(cols):
            dfs(0, c, pacific_reachable)
            dfs(rows - 1, c, atlantic_reachable)

        # return the intersection of both sets.
        return list(pacific_reachable & atlantic_reachable)
What is the time complexity of this solution?
1

O(1)

2

O(2ⁿ)

3

O(n log n)

4

O(m * n)

Mark as read

Next: Breadth-First Search Introduction

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
Abhay Singh
Top 1%
• 1 year ago

Java Solution:

class Solution {

    int[][] dxy={{-1,0},{0,1},{1,0},{0,-1}};
    
    void boundary_dfs(int[][] grid, int i, int j, int prev, boolean[][] visited){
        int n = grid.length;
        int m = grid[0].length;
        
        if(i<0 || j<0 || i==n || j==m || visited[i][j]==true || grid[i][j] < prev) return;
        
        visited[i][j]=true;
        for(int k=0;k<4;k++){
            int x=i+dxy[k][0], y=j+dxy[k][1];
            
            boundary_dfs(grid, x, y, grid[i][j], visited);
        }
    }

    public List<List<Integer>> pacificAtlantic(int[][] heights) {
        int n = heights.length;
        int m = heights[0].length;

        boolean[][] pacific = new boolean[n][m];
        boolean[][] atlantic = new boolean[n][m];

        // moving from boundaries to inwards cells where we can reach
        for(int j=0;j<m;j++){
            boundary_dfs(heights,0,j,Integer.MIN_VALUE,pacific);
            boundary_dfs(heights,n-1,j,Integer.MIN_VALUE,atlantic);
        }
        
        for(int i=0;i<n;i++){
            boundary_dfs(heights,i,0,Integer.MIN_VALUE,pacific);
            boundary_dfs(heights,i,m-1,Integer.MIN_VALUE,atlantic);
        }
        
        List<List<Integer>> ans = new ArrayList<>();
        for(int i=0;i<n;i++){
            for(int j=0;j<m;j++){
                if(atlantic[i][j]==true && pacific[i][j]==true) ans.add(Arrays.asList(i,j));
            }
        }
        return ans;
    }
}
Show More

4

Reply
Summer Than
Premium
• 3 months ago

The text in the illustrations is almost the same as the background color and very hard to read in dark mode

2

Reply
Arun prasath
• 1 year ago

Looks like test cases are expecting ordering of the result. Please fix it.
If you guys need any help. Please let me know

thanks
Arun prasath N
+91 98801 45446

class Solution:
    def pacific_atlantic_flow(self, grid):

        n = len(grid)
        if n == 0:
            return 0
        
        m = len(grid[0])

        pacific = [(0, c) for c in range(m)] + [(r,0) for r in range(n)]
        atlantic = [(n-1, c) for c in range(m)] + [(r, m-1) for r in range(n)]

        def valid_adjs(nd):
            i,j = nd
            res = []
            for x,y in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
                if x >=0 and x < n and y >= 0 and y < m:
                    res.append((x,y))
            
            return res

        def dfs(nd, ocean):
            ocean.add(nd)
            i,j = nd
            for adj in valid_adjs(nd):
                x,y = adj
                if grid[x][y] >= grid[i][j]:
                    if adj not in ocean:
                        dfs(adj, ocean)

        flows_to_pacific = set()
        flows_to_atlantic = set()

        for nd in pacific:
            dfs(nd, flows_to_pacific)

        for nd in atlantic:
            dfs(nd, flows_to_atlantic)

        res = flows_to_atlantic.intersection(flows_to_pacific)            

        return list(res)
Show More

1

Reply
Jimmy Zhang
Top 5%
• 1 year ago

This is fixed! Thanks for bringing it to our attention

1

Reply
Arun prasath
• 1 year ago

Awesome!!! Quality of the content is very good. Keep going!!!
thanks
Arun prasath N

2

Reply
S
StandardCopperLobster574
• 6 months ago

is moble number needed to be shared on ?   here and there will be some corrections they might take time based on priorities

0

Reply
Daksh Gargas
Premium
• 16 days ago

Go lang solution:


func pacific_atlantic_flow(grid [][]int) [][]int {
	output := [][]int{}
	if len(grid) == 0 || len(grid[0]) == 0 {
		return output
	}

	directions := [][]int{{0, 1}, {1, 0}, {-1, 0}, {0, -1}}

	pacific := make([][]bool, len(grid))
	atlantic := make([][]bool, len(grid))
	for i := range len(grid) {
		pacific[i] = make([]bool, len(grid[0]))
		atlantic[i] = make([]bool, len(grid[0]))
	}
	rows, cols := len(grid), len(grid[0])

	var dfs func(int, int, [][]bool)
	dfs = func(r, c int, ocean [][]bool) {
		if ocean[r][c] {
			return
		}
		ocean[r][c] = true
		for _, dir := range directions {
			nr, nc := r+dir[0], c+dir[1]
			if nr < 0 || nr >= rows || nc < 0 || nc >= cols {
				continue
			}
			if grid[r][c] > grid[nr][nc] {
				continue
			} // if bigger, then can't go inwards
			dfs(nr, nc, ocean)
		}
	}

	for r := range rows {
		dfs(r, 0, pacific) // first col, all rows
		dfs(r, cols-1, atlantic)
	}

	for c := range cols {
		dfs(0, c, pacific) // first row, all cols
		dfs(rows-1, c, atlantic)
	}

	// find intersections
	for r := range rows {
		for c := range cols {
			if pacific[r][c] && atlantic[r][c] {
				output = append(output, []int{r, c})
			}
		}
	}

	return output
}
Show More

0

Reply
Satya Dasara
Premium
• 2 months ago
• edited 2 months ago

Top left is Pacific
Bottom right is Atlantic

If we start from a particular cell and reach c = -1 or r = -1 we reach Pacific
Similarly if we reach c = C and r = R we reach Atlantic

Trick is to maintain 2 sets, one for Pacific one of Atlantic
We should also send starting row and column as parameter to DFS method
Also for every cell don't forget to reset visited set

This is downhill approach and time complexity is O((R x C)^2) so it's slow but more intuitive and should be okay for interviews

class Solution:
    def pacific_atlantic_flow(self, grid: List[List[int]]):
        if not grid or not grid[0]:
            return []

        # reach pacific when r = -1 or c = -1
        pacific_set = set()

        # reach atlantic when r = R or c = C
        atlantic_set = set()

        visited = set()

        R = len(grid)
        C = len(grid[0])
        directions = [(1,0), (-1,0), (0,1), (0,-1)]

        def dfs(start_r, start_c, r, c, grid):
            nonlocal visited
            nonlocal R
            nonlocal C
            nonlocal directions
            nonlocal pacific_set
            nonlocal atlantic_set

            visited.add((r,c))

            for direction in directions:
                dr, dc = direction
                nr = r + dr
                nc = c + dc

                if nr < 0 or nc < 0:
                    pacific_set.add((start_r, start_c))
                elif nr >= R or nc >= C:
                    atlantic_set.add((start_r, start_c))
                
                if 0 <= nr < R and 0 <= nc < C and (nr, nc) not in visited and grid[nr][nc] <= grid[r][c]:
                    dfs(start_r, start_c, nr, nc, grid)
        
        for r in range(R):
            for c in range(C):
                visited = set()
                dfs(r, c, r, c, grid)
        
        return list(pacific_set & atlantic_set)
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

Approach 1: Brute Force Approach

Approach 2: Boundary DFS

Solution
