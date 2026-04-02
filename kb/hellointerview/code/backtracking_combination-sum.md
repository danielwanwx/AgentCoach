# Combination Sum

> Source: https://www.hellointerview.com/learn/code/backtracking/combination-sum
> Scraped: 2026-03-30


Given an array of distinct integers candidates and a target integer target, generate all unique combinations of candidates which sum to target. The combinations may be returned in any order, and the same number may be chosen from candidates an unlimited number of times.

Constraints:

All values in candidates are positive integers.
1 <= candidates.length <= 30
2 <= candidates[i] <= 40
All elements of candidates are distinct.
1 <= target <= 40

Input:

candidates = [2,3,6,7]
target = 7

Output:

[[2,2,3],[7]]

Explanation:

2 and 3 are candidates, and 2 + 2 + 3 = 7. Note that 2 can be used multiple times. 7 is a candidate, and 7 = 7. These are the only two combinations.

CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List
    [List[int]]:
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

Solution
candidates
​
|
candidates
2d-list of integers
target
​
|
target
integer
Try these examples:
No Solution
Simple
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def combinationSum(candidates, target):
    def backtrack(start, combo, current_target):
        if current_target == 0:
            result.append(list(combo))
            return
        for i in range(start, len(candidates)):
            curr = candidates[i]
            if candidates[i] > current_target:
                return
            combo.append(curr)
            backtrack(i, combo, current_target - curr)
            combo.pop()
        return
    
    candidates.sort()
    result = []
    backtrack(0, [], target)
    return result
2
3
6
7

combination sum

0 / 56

1x
Explanation
This solution uses backtracking to find all the combinations of numbers that sum up to the target. The backtracking function is a recursive function that uses depth-first search to explore all possible combinations of candidates that sum up to the target. Each call to backtracking takes in parameters start, combo, and current_target. The start parameter is the index of the current candidate, combo is the current combination of numbers, and the current_target parameter is the target we are trying to hit (equal to target - the sum of combo).
The first step is to sort candidates, which makes it easy to tell when the current search combination exceeds the target, and can be pruned.
VISUALIZATION
Python
Language
Full Screen
def combinationSum(candidates, target):
    def backtrack(start, combo, current_target):
        if current_target == 0:
            result.append(list(combo))
            return
        for i in range(start, len(candidates)):
            curr = candidates[i]
            if candidates[i] > current_target:
                return
            combo.append(curr)
            backtrack(i, combo, current_target - curr)
            combo.pop()
        return
    
    candidates.sort()
    result = []
    backtrack(0, [], target)
    return result
2
3
6
7

combination sum

0 / 1

1x
Next, we kick off the search. Each call to the backtracking function first checks if the current_target is equal to 0. If so, that means the current value for combo is a valid solution, so we add it to the result. If not, the function iterates through the candidates starting from the start index. For each candidate, we add it to the current combination and recursively call the backtracking function with the updated current_target. Since we can use the same candidate multiple times, we pass the start index as the current index to the next call.
VISUALIZATION
Python
Language
Full Screen
def combinationSum(candidates, target):
    def backtrack(start, combo, current_target):
        if current_target == 0:
            result.append(list(combo))
            return
        for i in range(start, len(candidates)):
            curr = candidates[i]
            if candidates[i] > current_target:
                return
            combo.append(curr)
            backtrack(i, combo, current_target - curr)
            combo.pop()
        return
    
    candidates.sort()
    result = []
    backtrack(0, [], target)
    return result
2
3
6
7
result
[]

sort candidates

0 / 10

1x
Recursively exploring all combinations
If at any point the current_target becomes less than 0, we know that the current combo is not a valid solution, so we backtrack to the previous call.
For the backtracking step, we remove the last number from the current combination and try the next candidate. This process continues until we have tried all the candidates.
VISUALIZATION
Python
Language
Full Screen
def combinationSum(candidates, target):
    def backtrack(start, combo, current_target):
        if current_target == 0:
            result.append(list(combo))
            return
        for i in range(start, len(candidates)):
            curr = candidates[i]
            if candidates[i] > current_target:
                return
            combo.append(curr)
            backtrack(i, combo, current_target - curr)
            combo.pop()
        return
    
    candidates.sort()
    result = []
    backtrack(0, [], target)
    return result
def backtrack(start, combo, current_target):
    if current_target == 0:
        result.append(list(combo))
        return
    for i in range(start, len(candidates)):
        curr = candidates[i]
        if candidates[i] > current_target:
            return
        combo.append(curr)
        backtrack(i, combo, current_target - curr)
        combo.pop()
    return
def backtrack(start, combo, current_target):
    if current_target == 0:
        result.append(list(combo))
        return
    for i in range(start, len(candidates)):
        curr = candidates[i]
        if candidates[i] > current_target:
            return
        combo.append(curr)
        backtrack(i, combo, current_target - curr)
        combo.pop()
    return
def backtrack(start, combo, current_target):
    if current_target == 0:
        result.append(list(combo))
        return
    for i in range(start, len(candidates)):
        curr = candidates[i]
        if candidates[i] > current_target:
            return
        combo.append(curr)
        backtrack(i, combo, current_target - curr)
        combo.pop()
    return
def backtrack(start, combo, current_target):
    if current_target == 0:
        result.append(list(combo))
        return
    for i in range(start, len(candidates)):
        curr = candidates[i]
        if candidates[i] > current_target:
            return
        combo.append(curr)
        backtrack(i, combo, current_target - curr)
        combo.pop()
    return
2
3
6
7
i = 0
result
[]
start
0
combo
[2,2,2]
current_target
1

i = 0

0 / 2

1x
Backtracking to the previous call. Notice how we `pop` from `combo` when we backtrack.

Mark as read

Next: Palindrome Partitioning

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
Dan Carpenter
Top 5%
• 5 months ago

I don't see a section here to try this problem myself. This question seems to have a buggy layout and missing elements.

40

Reply
Narendra Naidu Lolugu
Premium
• 7 months ago

better way to represent like below

class Solution {

    public List<List<Integer>> combinationSum(int[] candidates, int target) {
        List<Integer> running = new ArrayList();
        List<List<Integer>> ans = new ArrayList();
        
        backTrack(candidates, target, 0, running, ans);

        return ans;
    }

    public void backTrack(int[] candidates, int target, int idx, List<Integer> running, List<List<Integer>> ans) {
        if (idx == candidates.length) {
            if (target == 0) {
                ans.add(new ArrayList(running));
            }
            return;
        }

         if (target - candidates[idx] >= 0) {
            running.add(candidates[idx]);
            backTrack(candidates, target - candidates[idx], idx, running, ans);
            running.remove(running.size()-1);
         }
         
         backTrack(candidates, target, idx+1, running, ans);
    }
}
Show More

5

Reply
N
Top 5%
• 10 months ago

internal 500 error for animations

3

Reply
A
AddedLimeCarp593
Top 1%
• 9 months ago

How does this solution prevent duplicate answers?

2

Reply
U
UsualMoccasinMacaw440
• 9 months ago

It's achieved through the for loop index starting at the start instead of 0. For example [2,3,6,7], target = 7 - in this case the moment index points to the value 3, it never checks the combinational with 2 again but all the values after 3.

7

Reply
C
cargobike
Premium
• 19 days ago

Kudos to whoever built the UI and animation at Hello Interview. It should have been this visual all along.

1

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Solution

Explanation
