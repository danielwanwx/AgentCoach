# Merge Intervals

> Source: https://www.hellointerview.com/learn/code/intervals/merge-intervals
> Scraped: 2026-03-30


Intervals
Merge Intervals
medium
DESCRIPTION (inspired by Leetcode.com)

Write a function to consolidate overlapping intervals within a given array intervals, where each interval intervals[i] consists of a start time starti and an end time endi.

Two intervals are considered overlapping if they share any common time, including if one ends exactly when another begins (e.g., [1,4] and [4,5] overlap and should be merged into [1,5]).

The function should return an array of the merged intervals so that no two intervals overlap and all the intervals collectively cover all the time ranges in the original input.

Input:

intervals = [[3,5],[1,4],[7,9],[6,8]]

Output:

[[1,5],[6,9]]

Explanation: The intervals [3,5] and [1,4] overlap and are merged into [1,5]. Similarly, [7,9] and [6,8] overlap and are merged into [6,9].

CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def mergeIntervals(self, intervals: List[List[int]]) -> List[List
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
Since this question involves merging intervals that overlap, we want to first sort the intervals by their start time. This allows us to easily check if an interval overlaps with the one before it. Then we create a new array to store the merged intervals.
We iterate through the sorted intervals and check if the current interval overlaps with the last interval in the merged array. If it does, we merge the intervals by updating the end time of the last interval in the merged array to be the maximum of the end times of the current interval and the last interval in the merged array (i.e. max(merged[-1][1], current[1])).
Note the first interval can always be added directly to the merged array.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def mergeIntervals(intervals):
    sortedIntervals = sorted(intervals, key=lambda x: x[0])
    merged = []
        
    for interval in sortedIntervals:
        if not merged or interval[0] > merged[-1][1]:
            merged.append(interval)
        else:
            merged[-1][1] = max(interval[1], merged[-1][1])

    return merged
]
[
5
1
]
[
6
3
]
[
10
8
]
[
18
15
merged
]
[
5
1

intervals[1]

0 / 1

1x
Merging an overlapping interval
If it doesn't, we add the current interval directly to the merged array.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def mergeIntervals(intervals):
    sortedIntervals = sorted(intervals, key=lambda x: x[0])
    merged = []
        
    for interval in sortedIntervals:
        if not merged or interval[0] > merged[-1][1]:
            merged.append(interval)
        else:
            merged[-1][1] = max(interval[1], merged[-1][1])

    return merged
]
[
5
1
]
[
6
3
]
[
10
8
]
[
18
15
merged
]
[
6
1

intervals[2]

0 / 1

1x
Adding an interval that does not overlap
What is the time complexity of this solution?
1

O(V + E)

2

O(n)

3

O(n³)

4

O(n * logn)

Solution
intervals
​
|
intervals
list of intervals [start, end]
Try these examples:
Nested
No Overlap
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def mergeIntervals(intervals):
    sortedIntervals = sorted(intervals, key=lambda x: x[0])
    merged = []
        
    for interval in sortedIntervals:
        if not merged or interval[0] > merged[-1][1]:
            merged.append(interval)
        else:
            merged[-1][1] = max(interval[1], merged[-1][1])

    return merged
]
[
5
1
]
[
6
3
]
[
10
8
]
[
18
15

merge intervals

0 / 10

1x

Mark as read

Next: Employee Free Time

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

(14)

Comment
Anonymous
​
Sort By
Popular
Sort By
LC
Leonardo Cardoso
• 6 months ago
class Solution:
    def mergeIntervals(self, intervals: List[List[int]]):
        
        if not intervals:
            return []

        sorted_interv = sorted(intervals, key=lambda x:x[0])
        merged = []
        merged.append(sorted_interv[0])

        for i in range(1, len(sorted_interv)):
            if merged[-1][1] >= sorted_interv[i][0]:
                merged[-1][1] = max(merged[-1][1], sorted_interv[i][1])
            else:
                merged.append(sorted_interv[i])
        
        return merged

2

Reply
Sumanth
Premium
• 3 months ago
class Solution {
    mergeIntervals(intervals: number[][]): number[][] {
        if (!intervals.length) return [];
        intervals.sort((a: number[], b: number[]) => a[0] - b[0]);

        let res: number[][] = [];
        let [newStart, newEnd] = intervals[0];

        for (let i = 1; i < intervals.length; i++) {
            const [start, end] = intervals[i];

            if (start > newEnd) {
                res.push([newStart, newEnd]);
                newStart = start;
                newEnd = end;
            } else {
                newStart = Math.min(newStart, start);
                newEnd = Math.max(newEnd, end);
            }
        }

        res.push([newStart, newEnd]);
        return res;
    }
}
Show More

1

Reply
Abhay Singh
Top 1%
• 1 year ago

Java Solution:

class Solution {
    public int[][] merge(int[][] intervals) {
        Arrays.sort(intervals, (a, b) -> a[0] - b[0]);

        int n = intervals.length;

        List<List<Integer>> mergedIntervals = new ArrayList<>();
        int s = intervals[0][0], e = intervals[0][1];
        for(int i=1;i<n;i++){
            int si = intervals[i][0], ei = intervals[i][1];

            if(si <= e){
                e = Math.max(e, ei);
            }else{
                mergedIntervals.add(Arrays.asList(s,e));
                s = si;
                e = ei;
            }
        }

        mergedIntervals.add(Arrays.asList(s,e));

        int[][] ans = new int[mergedIntervals.size()][2];
        for(int i=0;i<mergedIntervals.size();i++){
            ans[i][0] = mergedIntervals.get(i).get(0);
            ans[i][1] = mergedIntervals.get(i).get(1);
        }

        return ans;
    }
}
Show More

1

Reply
Noah
Premium
• 3 days ago
class Solution {
    mergeIntervals(intervals) {
        if (intervals.length === 0) return []

        intervals.sort((a, b) => a[0] - b[0])

        const result = [intervals[0]]

        for (let i = 1; i < intervals.length; i++) {
            const prevInterval = result[result.length - 1]
            const currInterval = intervals[i]

            if (currInterval[0] <= prevInterval[1]) {
                prevInterval[1] = Math.max(currInterval[1], prevInterval[1])
            } else {
                result.push(currInterval)
            }
        }

        return result
    }
}
Show More

0

Reply
Jingyang Liu
• 12 days ago

class Solution:
def mergeIntervals(self, intervals: List[List[int]]) -> List[List[int]]:
# Your code goes here
if not intervals:
return []
res = []
intervals.sort()
i=0
while i < len(intervals):
start,end = intervals[i]
while i+1<len(intervals) and end>=intervals[i+1][0]:
end = max(end,intervals[i+1][1])
i+=1
res.append([start,end])
i+=1

    return res

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

Solution
