# Surrounded Regions

> Source: https://www.hellointerview.com/learn/code/depth-first-search/surrounded-regions
> Scraped: 2026-03-30


Given an m x n matrix grid containing only characters 'X' and 'O', modify grid to replace all regions of 'O' that are completey surrounded by 'X' with 'X'.

A region of 'O' is surrounded by 'X' if there is no adjacent path (cells that border each other in the N, W, E, S directions) consisting of only 'O' from anywhere inside that region to the border of the board.

Input:

grid = [
["X","X","X","X","O"],
["X","X","O","X","X"],
["X","X","O","X","O"],
["X","O","X","X","X"]
["X","O","X","X","X"]
]

Output:

[
["X","X","X","X","O"],
["X","X","X","X","X"],
["X","X","X","X","O"],
["X","O","X","X","X"],
["X","O","X","X","X"]
]

Explanation: The region of O's at grid[1][2] and grid[2][2] is completely surrounded, so we replace them with X's. All the other "O"s are connected to the border by a path of all "O"s, so we leave them as is.

Input:

grid = [
["O","O"],
["O","X"],
]

Output:

[
["O", "O"],
["O", "X"]
]


Explanation: All the "O"s are connected to the border.

CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def surrounded_regions(self, grid: List[List[str]]) -> List[List
    [str]]:
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
In order to solve this problem, we can first recognize that there are two types of "Os" in the grid, those that are reachable on a path of connected "O"s starting from the border of the grid, and those that are not.
X
X
X
X
O
X
X
O
X
X
X
X
O
X
O
X
O
X
X
X
X
O
X
X
X
The "Os" that are reachable from the border are highlighted in light blue, while the ones that aren't a highlighted in dark blue.
The "Os" that are reachable from the border are the ones that we want to keep, while the "Os" that are not reachable from the border are the ones that we want to change to "Xs".
In order for an "O" to be reachable from the border, it must be connected to an "O" that is on the border. This means that we can start from each cell in the border of the grid and use depth-first search to find all the "Os" that are reachable from the border of the grid (by following a path of connected "Os" in the N, E, S, W directions). Whenever we find an "O" that is reachable from the border, we can change its value to "S" to mark it as safe.
X
X
X
X
S
X
X
O
X
X
X
X
O
X
S
X
S
X
X
X
X
S
X
X
X
All the "Os" that are reachable from the border are marked with "S".
After marking them as safe, we can then iterate through each cell in the grid and change the "Os" that are not marked as safe to "Xs", while also changing the "safe" cells back to "Os".
X
X
X
X
O
X
X
X
X
X
X
X
X
X
O
X
O
X
X
X
X
O
X
X
X
The final grid.
SOLUTION
Python
Language
class Solution:
    def surrounded_regions(self, grid): 
        if not grid:
            return grid
        
        rows = len(grid)
        cols = len(grid[0])

        # recursive function to find all the "O"s that are reachable
        # from the border and mark them as "S"
        def dfs(x, y):
            # return immediately if the cell is out of bounds or is not an "O
            if x < 0 or y < 0 or x >= rows or y >= cols or grid[x][y] != 'O':
                return
            grid[x][y] = 'S'

            # explore the neighboring cells
            dfs(x + 1, y)
            dfs(x - 1, y)
            dfs(x, y + 1)
            dfs(x, y - 1)

        # initialize the dfs for the first and last column
        for i in range(rows):
            if grid[i][0] == 'O':
                dfs(i, 0)
            if grid[i][cols - 1] == 'O':
                dfs(i, cols - 1)

         # initialize the dfs for the first and last row
        for j in range(cols):
            if grid[0][j] == 'O':
                dfs(0, j)
            if grid[rows - 1][j] == 'O':
                dfs(rows - 1, j)

        # change the "O"s that are not marked as "S" to "X"s and the "S"s back to "O"s
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == 'O':
                    grid[i][j] = 'X'
                elif grid[i][j] == 'S':
                    grid[i][j] = 'O'
                    
        return grid
Keeping Track of Visited Cells
In the above solution, marking each cell as "S" also serves to keep track of the visited cells. We only make recursive calls to the neighboring cells if the current cell is an "O". This way, we avoid visiting the same cell multiple times, as a cell that was previously "O" but is now "S" will not be visited again.
What is the time complexity of this solution?
1

O(m * n)

2

O(N + Q)

3

O(4ⁿ)

4

O(log n)

Mark as read

Next: Pacific Atlantic Water Flow

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

(16)

Comment
Anonymous
​
Sort By
Popular
Sort By
S
SoftGrayFirefly749
• 1 year ago

Very difficult question considering you need to invert what the question is asking for to land on the optimal result.

6

Reply
W
WoodenAquamarineSnipe931
Top 10%
• 10 months ago

Could you consider changing x and y to r and c in the interest of maintaining consistency of naming conventions?

3

Reply
Abhay Singh
Top 1%
• 1 year ago

Java Solution:

class Solution {

    int[][] dxy={{-1,0},{0,1},{1,0},{0,-1}};
    
    void boundary_dfs(char[][] grid, int i, int j){
        int n = grid.length;
        int m = grid[0].length;
        
        if(i<0 || j<0 || i==n || j==m || grid[i][j]!='O') return;
        
        grid[i][j]='#';
        for(int k=0;k<4;k++){
            int x=i+dxy[k][0], y=j+dxy[k][1];
            
            boundary_dfs(grid,x,y);
        }
    }

    public void solve(char[][] grid) {
        int n = grid.length;
        int m = grid[0].length;

        for(int i=0;i<n;i++){
            if(grid[i][0]=='O') boundary_dfs(grid,i,0);
            if(grid[i][m-1]=='O') boundary_dfs(grid,i,m-1);
        }
        for(int j=0;j<m;j++){
            if(grid[0][j]=='O') boundary_dfs(grid,0,j);
            if(grid[n-1][j]=='O') boundary_dfs(grid,n-1,j);
        }
        
        for(int i=0;i<n;i++){
            for(int j=0;j<m;j++){
                if(grid[i][j]=='#'){
                    grid[i][j]='O';
                }else if(grid[i][j]=='O'){
                    grid[i][j]='X';
                }
            }
        }
    }
}
Show More

2

Reply
L
LuckyJadeMouse301
• 3 months ago

Hey team great stuff here in general

Small nitpick / understanding check from my side:
"Time Complexity: O(M * N) where M is the number of rows and N is the number of columns in the grid. We are iterating through each cell in the grid once."

Believe we are iterating over each cell in the grid 1-3 times depending on the position and initial value

Conceptually our approach is to start DFS from all border "O"s to paint them with the "to flip" letter, which could visit the rest of the grid

Then we do a second pass across to flip those and the non visited "O"s

So just thought "once" conflicted a bit with the high level understanding of the approach
It is just constant anyway which leaves the stated Big O correct 🙂

Thanks!

PS: Wow I wish we could shuffle our anonymous name 😝

1

Reply
Geethu Krishna
• 1 month ago

Time Complexity: O(m × n)
Space Complexity: O(m × n) (visited + recursion stack)

Java Solution

public class Solution {
    public static int[][] directions = { { -1, 0 }, { 1, 0 }, { 0, -1 }, { 0, 1 } };
    
     public static String[][] surrounded_regions(String[][] grid) {
        // Your code goes here
        if (grid == null || grid.length == 0 || grid[0].length == 0) return grid;
        HashSet<String> visited = new HashSet<>();
        for(int i=0 ; i< grid.length ; i++){
            dfs(grid , i ,0 , visited);
            dfs(grid , i , grid[0].length-1 , visited);

        }
        for(int j=0 ; j< grid[0].length ; j++){
            dfs(grid , 0 ,j , visited);
            dfs(grid , grid.length-1 ,j , visited);

        }
        for(int i=0 ; i< grid.length ; i++){
            for(int j=0 ; j< grid[0].length ; j++){
                if( (grid[i][j].equals("O"))  & !visited.contains(i+"_"+j)){
                    grid[i][j] = "X";
                }
            }
        }
        return grid;
    }

    public static void dfs(String[][] grid , int i , int j , HashSet<String> visited){
         if (i < 0 || i >= grid.length || j < 0 || j >= grid[0].length || !grid[i][j].equals("O")) {
            return;
        }
        if(visited.contains(i+"_"+j)){
            return;
        }else{
            visited.add(i+"_"+j);
        }

        for(int[] dir : directions){
            dfs(grid , i + dir[0], j+dir[1], visited);
        }

    }
}
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

Keeping Track of Visited Cells
