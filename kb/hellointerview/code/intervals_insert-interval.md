# Insert Interval

> Source: https://www.hellointerview.com/learn/code/intervals/insert-interval
> Scraped: 2026-03-30


Intervals
Insert Interval
medium
DESCRIPTION (inspired by Leetcode.com)

Given a list of intervals intervals and an interval newInterval, write a function to insert newInterval into a list of existing, non-overlapping, and sorted intervals based on their starting points. The function should ensure that after the new interval is added, the list remains sorted without any overlapping intervals, merging them if needed.

Input:

intervals = [[1,3],[6,9]]
newInterval = [2,5]

Output:

[[1,5],[6,9]]

Explanation: The new interval [2,5] overlaps with [1,3], so they are merged into [1,5].

CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def insertIntervals(self, intervals: List[List[int]], newInterval: 
    List[int]) -> List[List[int]]:
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
We first want to create a new list merged to store the merged intervals we will return at the end.
This solution operates in 3 phases:
Add all the intervals ending before newInterval starts to merged.
Merge all overlapping intervals with newInterval and add that merged interval to merged.
Add all the intervals starting after newInterval to merged.
Phase 1
In this phase, we add all the intervals that end before newInterval starts to merged. This involves iterating through the intervals list until the current interval no longer ends before newInterval starts (i.e. intervals[i][1] >= newInterval[0]).
VISUALIZATION
Hide Code
Python
Language
Full Screen
def insertIntervals(intervals, newInterval):
    merged = []
    i = 0
    n = len(intervals)

    while i < n and intervals[i][1] < newInterval[0]:
        merged.append(intervals[i])
        i += 1

    while i < n and intervals[i][0] <= newInterval[1]:
        newInterval[0] = min(intervals[i][0], newInterval[0])
        newInterval[1] = max(intervals[i][1], newInterval[1])
        i += 1

    merged.append(newInterval)
    for j in range(i, n):
        merged.append(intervals[j])

    return merged
]
[
3
1
]
[
6
4
]
[
7
6
]
[
10
8
]
[
15
11
newInterval
]
[
8
5
merged

initialize variables

0 / 1

1x
Phase 2
In this phase, we merge all the intervals that overlap with newInterval together into a single interval by updating newInterval to be the minimum start and maximum end of all the overlapping intervals. This involves iterating through the intervals list until the current interval starts after newInterval ends (i.e. intervals[i][0] > newInterval[1]).
When that condition is met, we add newInterval to merged and move onto phase 3.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def insertIntervals(intervals, newInterval):
    merged = []
    i = 0
    n = len(intervals)

    while i < n and intervals[i][1] < newInterval[0]:
        merged.append(intervals[i])
        i += 1

    while i < n and intervals[i][0] <= newInterval[1]:
        newInterval[0] = min(intervals[i][0], newInterval[0])
        newInterval[1] = max(intervals[i][1], newInterval[1])
        i += 1

    merged.append(newInterval)
    for j in range(i, n):
        merged.append(intervals[j])

    return merged
]
[
3
1
]
[
6
4
]
[
7
6
]
[
10
8
]
[
15
11
newInterval
]
[
8
5
merged
]
[
3
1

add intervals before newInterval

0 / 4

1x
Phase 3
Phase 3 involves adding all the intervals starting after newInterval to merged. This involves iterating through the intervals list until the end of the list, and adding each interval to merged.
After completing these 3 phases, we return merged as the final result.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def insertIntervals(intervals, newInterval):
    merged = []
    i = 0
    n = len(intervals)

    while i < n and intervals[i][1] < newInterval[0]:
        merged.append(intervals[i])
        i += 1

    while i < n and intervals[i][0] <= newInterval[1]:
        newInterval[0] = min(intervals[i][0], newInterval[0])
        newInterval[1] = max(intervals[i][1], newInterval[1])
        i += 1

    merged.append(newInterval)
    for j in range(i, n):
        merged.append(intervals[j])

    return merged
]
[
3
1
]
[
6
4
]
[
7
6
]
[
10
8
]
[
15
11
newInterval
]
[
10
4
merged
]
[
3
1
]
[
10
4

j = 4

0 / 2

1x
What is the time complexity of this solution?
1

O(n³)

2

O(m * n * 4^L)

3

O(n)

4

O(4^L)

Solution
intervals
​
|
intervals
list of intervals [start, end]
newInterval
​
|
newInterval
[start, end]
Try these examples:
Insert Front
Overlap Many
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def insertIntervals(intervals, newInterval):
    merged = []
    i = 0
    n = len(intervals)

    while i < n and intervals[i][1] < newInterval[0]:
        merged.append(intervals[i])
        i += 1

    while i < n and intervals[i][0] <= newInterval[1]:
        newInterval[0] = min(intervals[i][0], newInterval[0])
        newInterval[1] = max(intervals[i][1], newInterval[1])
        i += 1

    merged.append(newInterval)
    for j in range(i, n):
        merged.append(intervals[j])

    return merged
]
[
3
1
]
[
6
4
]
[
7
6
]
[
10
8
]
[
15
11
newInterval
]
[
8
5

insert interval

0 / 9

1x

Mark as read

Next: Non-Overlapping Intervals

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

(35)

Comment
Anonymous
​
Sort By
Popular
Sort By
Don A W.
• 11 months ago

I thought overlapping was only if the end time for 'x' was past the start time for 'y', like it was mentioned in the previous exercise, but here it's overlapping when they are the same time. Should make that clear imo.

13

Reply
D
DevelopedGrayPanther583
Premium
• 15 days ago

That's the case for can attend meetings because you can go from one meeting to the next without issue. In this case though it is overlapping if the numbers match or if previous[start] > current[end]

0

Reply
Abhay Singh
Top 1%
• 1 year ago

Java Solution:

class Solution {

    public int[][] insert(int[][] intervals, int[] newInterval) {
        int n = intervals.length;

        List<int[]> intervalList = new ArrayList<>(Arrays.asList(intervals));
        
        int j = 0;
        while (j < intervalList.size() && intervalList.get(j)[0] < newInterval[0]){
            j++;
        }
        
        intervalList.add(j, newInterval);

        List<List<Integer>> ans = new ArrayList<>();
        int s = intervalList.get(0)[0], e = intervalList.get(0)[1];

        for(int i=1;i<n+1;i++){
            int si = intervalList.get(i)[0], ei = intervalList.get(i)[1];
            System.out.println(si + "->" + ei);

            if(si > e){
                ans.add(Arrays.asList(s,e));
                s = si;
                e = ei;
            }else{
                e = Math.max(e, ei);
            }
        }

        ans.add(Arrays.asList(s,e));

        n = ans.size();
        int[][] finalAns = new int[n][2];
        for(int i=0;i<n;i++){
            finalAns[i][0] = ans.get(i).get(0);
            finalAns[i][1] = ans.get(i).get(1);
        }

        return finalAns;
    }
}
Show More

3

Reply
O
OlympicBlackLynx843
Top 1%
• 1 year ago

You could just as easily:

append the newInterval

sort by start time

merge overlapping while inserting into a new result array (standard template)

return result array

I tried this and it passes all the tests - the complexity should be the same, right?

4

Reply
Abhay Singh
Top 1%
• 1 year ago

Hey @OlympicBlackLynx843, if we sort Time Complexity will be O(NlogN).
Since intervals are already sorted, so we should take advantage of that info

21

Reply
M
MarkedPlumOcelot115
Premium
• 1 day ago

Since you now sort the array, instead of becoming 0(n) it will become 0(nlogn) thats worse time complexity than linear so thats the catch.

0

Reply
AS
Arun S
Top 10%
• 21 days ago

The overlap is checked with the following statement

while i < n and intervals[i][0] <= newInterval[1]:


Why is it not necessary to check the overlap as the following?

newInterval[0] < intervals[i][1]


1

Reply
Paroksh Saxena
Premium
• 15 days ago
• edited 15 days ago

Hey @Arun S,
When we are looking at inserting new interval, we need to skip all intervals whose end time is greater than new interval start tine. This is done using below code

newInterval[0] < intervals[i][1]

And when we are looking at merging the intervals with new interval, we need to look
for intervals whose start time is less than new interval end time. That is done using below code

while i < n and intervals[i][0] <= newInterval[1]:

0

Reply
aditya patel
Premium
• 1 month ago

Js Solution:
function insert(intervals: number[][], newInterval: number[]): number[][] {
const n = intervals.length;

if(n < 2) return [newInterval];

const merged: number[][] = [];
let i = 0;

// push until overlap is detected
while(i < n && intervals[i][1] < newInterval[0]) {
    merged.push(intervals[i]);
    i++;
}

// update new interval
while(i < n && intervals[i][0] <= newInterval[1]) {
    newInterval[0] = Math.min(newInterval[0], intervals[i][0]);
    newInterval[1] = Math.max(newInterval[1], intervals[i][1]);
    i++;
}

merged.push(newInterval);

while(i < n) {
    merged.push(intervals[i]);
    i++;
}

return merged;


};

Show More

1

Reply
chiranjeet mishra
• 5 months ago

class Solution:
def insertIntervals(self, intervals: List[List[int]], newInterval: List[int]):
# approach 1
# merged = []
# i = 0
# n = len(intervals)

    # while i < n and intervals[i][1] < newInterval[0]:
    #     merged.append(intervals[i])
    #     i += 1

    # while i < n and intervals[i][0] <= newInterval[1]:
    #     newInterval[0] = min(intervals[i][0], newInterval[0])
    #     newInterval[1] = max(intervals[i][1], newInterval[1])
    #     i += 1

    # merged.append(newInterval)
    # for j in range(i, n):
    #     merged.append(intervals[j])

    # return merged
    #approach 2
    intervals.append(newInterval)
    intervals = sorted(intervals, key=lambda x: x[0])
    merged = []
    for cat in intervals:
        if not merged or cat[0]>merged[-1][1]:
            merged.append(cat)
        else:
            merged[-1][1] = max(cat[1], merged[-1][1])
    return merged

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

Solution
