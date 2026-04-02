# Non-Overlapping Intervals

> Source: https://www.hellointerview.com/learn/code/intervals/non-overlapping-intervals
> Scraped: 2026-03-30


Intervals
Non-Overlapping Intervals
medium
DESCRIPTION (inspired by Leetcode.com)

Write a function to return the minimum number of intervals that must be removed from a given array intervals, where intervals[i] consists of a starting point starti and an ending point endi, to ensure that the remaining intervals do not overlap.

Input:

intervals = [[1,3],[5,8],[4,10],[11,13]]

Output:

1

Explanation: Removing the interval [4,10] leaves all other intervals non-overlapping.

CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def nonOverlappingIntervals(self, intervals: List[List[int]]) -> int:
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
This question reduces to finding the maximum number of non-overlapping intervals. Once we know that value, then we can subtract it from the total number of intervals to get the minimum number of intervals that need to be removed.
]
[
3
2
]
[
4
1
]
[
5
3
]
[
8
6
If we remove [1, 4], then all the remaining intervals are non-overlapping.
To find the maximum number of non-overlapping intervals, we can sort the intervals by their end time. We then use a greedy approach: we iterate over each sorted interval, and repeatedly try to add that interval to the set of non-overlapping intervals. Sorting by the end time allows us to choose the intervals that end the earliest first, which frees up more time for intervals to be included later.
We start by keeping track of a variable end which represents the end time of the latest interval in our set of non-overlapping intervals, as well as a variable count which represents the number of non-overlapping intervals we have found so far.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def nonOverlappingIntervals(intervals):
    if not intervals:
        return 0

    intervals.sort(key=lambda x: x[1])
    end = intervals[0][1]
    count = 1

    for i in range(1, len(intervals)):
        # Non-overlapping interval found
        if intervals[i][0] >= end:
            end = intervals[i][1]
            count += 1

    return len(intervals) - count
]
[
6
4
]
[
17
11
]
[
18
2
]
[
10
7

sort by end time

0 / 1

1x
We then iterate over each interval starting from the second interval in the list (the first interval is always non-overlapping). For each interval, we compare the start time of the interval to end. If it is less than end, then we cannot add the interval to our set of non-overlapping intervals, so we move onto the next interval without updating end or count.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def nonOverlappingIntervals(intervals):
    if not intervals:
        return 0

    intervals.sort(key=lambda x: x[1])
    end = intervals[0][1]
    count = 1

    for i in range(1, len(intervals)):
        # Non-overlapping interval found
        if intervals[i][0] >= end:
            end = intervals[i][1]
            count += 1

    return len(intervals) - count
]
[
6
4
]
[
17
11
]
[
18
2
]
[
10
7
end
count: 1

i = 1

0 / 1

1x
We cannot add [1, 4] to the set of non-overlapping intervals.
If it is greater than or equal to end, then we can add the interval to our set of non-overlapping intervals by updating count. We then update the value of end to be the end time of the current interval.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def nonOverlappingIntervals(intervals):
    if not intervals:
        return 0

    intervals.sort(key=lambda x: x[1])
    end = intervals[0][1]
    count = 1

    for i in range(1, len(intervals)):
        # Non-overlapping interval found
        if intervals[i][0] >= end:
            end = intervals[i][1]
            count += 1

    return len(intervals) - count
]
[
6
4
]
[
17
11
]
[
18
2
]
[
10
7
end
count: 2

non-overlapping interval found

0 / 4

1x
Handling non-overlapping intervals.
Solution
intervals
​
|
intervals
list of intervals [start, end]
Try these examples:
Overlaps
Sparse
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def nonOverlappingIntervals(intervals):
    if not intervals:
        return 0

    intervals.sort(key=lambda x: x[1])
    end = intervals[0][1]
    count = 1

    for i in range(1, len(intervals)):
        # Non-overlapping interval found
        if intervals[i][0] >= end:
            end = intervals[i][1]
            count += 1

    return len(intervals) - count
]
[
6
4
]
[
17
11
]
[
18
2
]
[
10
7

non-overlapping intervals

0 / 8

1x
What is the time complexity of this solution?
1

O(4ⁿ)

2

O(n)

3

O(n * logn)

4

O(n³)

Mark as read

Next: Merge Intervals

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

(17)

Comment
Anonymous
​
Sort By
Popular
Sort By
P
PayableRedHarrier765
• 1 year ago

Intuitively, it made more sense for me to count the overlapping intervals, despite the name of the problem

def nonOverlappingIntervals(self, intervals: list[list[int]]):
    if not intervals:
        return 0

    intervals.sort(key=lambda x: x[1])
    count = 0
    end = intervals[0][1]

    for i in range(1, len(intervals)):
        if intervals[i][0] < end:
            count += 1
        else:
            end = intervals[i][1]
    
    return count

16

Reply
Mingyu Dai
• 1 year ago

why this greedy algorithm works

8

Reply
Abhay Singh
Top 1%
• 1 year ago

I think if we had sorted by start_time, there could be cases where start_time is small but end_time is quite large which can overlap with multiple future intervals:
[[1,9], [2,4], [4,6], [5,7],[8,9]].
By sorting with smaller end_time, it will itself ensure that start < end & we get more non-overlapping intervals

1

Reply
Ravi
• 8 months ago

in that case, we can drop the one with larger end time. The code runs with all the test cases as well

public Integer nonOverlappingIntervals(int[][] intervals) {
        // Your code goes here
        Comparator<int[]> cmp = (a, b) -> Integer.compare(a[0], b[0]);
        Arrays.sort(intervals, cmp);

        int ans = 0;

        int lastEnding = intervals[0][1];

        for (int idx = 1; idx < intervals.length; idx++) {

            if (intervals[idx][0] < lastEnding) {
                lastEnding = Math.min(lastEnding, intervals[idx][1]);
                ans++;
            } else {
                lastEnding = intervals[idx][1];
            }
        }
        return ans;
    }
Show More

0

Reply
Thuc Nguyen
• 3 months ago

This strategy works because by sorting end time, in O(n) time we can greedily pick out the most number of non-overlapping intervals (count), as well as the least overlapping intervals (len() - count). Then you might ask how we sure the len()-count guarenteed to be the min number of intervals to be removed:

Assuming there is a smaller set of overlapping intervals, called k and k < (len()-count), then there must exist non-overlapping intervals  c = (len()-count) - k  > 0 and c should be included in count. Which contradicts with our initial algo that count is the largest non-overlapping interval.

Hope that makes sense :) Good luck

0

Reply
Abhay Singh
Top 1%
• 1 year ago

Java Solution:

class Solution {
    public int eraseOverlapIntervals(int[][] intervals) {
        Arrays.sort(intervals, (a, b) -> a[1] - b[1]);

        int n = intervals.length;
        
        int cnt = 0;
        int e = intervals[0][1];
        for(int i=1;i<n;i++){
            int si = intervals[i][0], ei = intervals[i][1];

            if(si < e){
                cnt++;
            }else{
                e = ei;
            }
        }

        return cnt;
    }
}
Show More

2

Reply
V
vp.dev.ltd
• 2 days ago

5 years ago I solved it in a different way.
Time/space is the same. But good to see other options

class Solution {
    public int eraseOverlapIntervals(int[][] intervals) {
        if (intervals == null || 
            intervals.length == 0 || 
            intervals[0].length == 0) return 0;
        // sort by start time
        Arrays.sort(intervals, (int[] a, int[] b) -> a[0] - b[0]);

        int previousEnd = intervals[0][0];
        int result = 0;
        // iterate over each sorted interval
        for (int[] interval : intervals) {
            // valid interval - move forward update end time
            if (interval[0] >= previousEnd) {
                previousEnd = interval[1];
                continue;
            } else {
                // if the new interval is starting before the previous end 
                // then one to be removed
                result++;
                // and smaller end time to be set
                previousEnd = Math.min(previousEnd, interval[1]);
            }   
        }
        
        return result;
    }
}
Show More

0

Reply
Tuğba Tümer
• 16 days ago

In the "Can Attend Meetings" question, you stated that the space complexity is O(n) because the sorting step requires O(n) auxiliary space in most language implementations (for example, Timsort in Python or merge sort in Java).

However, this question also includes a sorting step, yet you mentioned the space complexity is O(1). I believe this may be incorrect, since the sorting operation would still require additional space.

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
