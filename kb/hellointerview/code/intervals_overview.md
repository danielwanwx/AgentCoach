# Intervals Overview

> Source: https://www.hellointerview.com/learn/code/intervals/overview
> Scraped: 2026-03-30

Intervals Overview
4:10
5 chapters • 1 interactive checkpoints
This page covers problems involving intervals, which are given as a list of [start, end] times.
]
[
7
1
]
[
12
9
]
[
6
3
]
[
11
8
Sorting intervals by start time.
Interval problems typically involve sorting the given intervals, and then processing each interval in sorted each order. On this page, we'll cover:
Sorting intervals by start time
Sorting intervals by end time
Sorting by Start Time
Sorting intervals by their start times makes it easy to merge two intervals that are overlapping.
]
[
3
1
]
[
6
2
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
3
1
Merging two overlapping intervals.
Overlapping Intervals
After sorting by start time, an interval overlaps with the previous interval if it starts before the end time of the previous interval.
]
[
2
0
]
[
8
3
]
[
10
6
]
[
15
12
Overlapping intervals shown in green.
Detecting overlapping intervals is the basis of the question Can Attend Meetings, in which we are given a list of intervals representing the start and end times of meetings, and we need to determine if a person can attend all meetings.
We sort the intervals by their start times and iterate over each meeting. If the current meeting overlaps with the previous one, we return False. If we make it through the entire list without finding any overlaps, we return True.
intervals
​
|
intervals
list of intervals [start, end]
Try these examples:
Overlaps
No Overlap
Reset
VISUALIZATION
Python
Language
Full Screen
def canAttendMeetings(intervals):
    if not intervals:
        return True
    
    intervals.sort(key=lambda x: x[0])
    
    for i in range(1, len(intervals)):
        if intervals[i][0] < intervals[i-1][1]:
            return False
    
    return True
]
[
4
2
]
[
12
9
]
[
9
6
]
[
15
13

can attend meetings

0 / 5

1x
Merging Intervals
When an interval overlaps with the previous interval in a list of intervals sorted by start times, they can be merged into a single interval.
To merge an interval into a previous interval, we set the end time of the previous interval to be the max of either end time.
prev_interval[1] = max(prev_interval[1], interval[1])
Python code for merging interval into prev_interval
In Merge Intervals, we are given a list of intervals and need to return a list with all overlapping intervals merged together. We create a new list containing the merged intervals, sort the intervals by their start times, and then iterate over each interval. If the current interval overlaps with the last interval in the merged list, we merge the current interval into the last interval in the merged list. Otherwise, we add the current interval to the merged list.
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
Sorting by End Time
To see why we sometimes want to sort by end times instead of start time, let's consider the question of finding the maximum number of non-overlapping intervals in a given list of intervals.
Our solution will sort the intervals, and then greedily try to add each interval to the set of non-overlapping intervals.
If we sort by start time, we risk adding an interval that starts early but ends late, which will block us from adding other intervals until that interval ends.
For example, given the following intervals, if we sort by start time, choosing the first interval prevents us from adding another interval until after time 18. This blocks the remaining intervals from being added to the set of non-overlapping intervals, even though none of those intervals overlap with each other.
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
Sorting by start time yields 1 non-overlapping interval.
If instead we sort by end time, we can start by adding the intervals that end the earliest. Intuitively, this frees time for us to add more intervals as early as possible, and yields the correct answer.
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
Sorting by end time correctly yields 3 non-overlapping intervals.
Non-Overlapping Intervals
This is the basis for the question Non-Overlapping Intervals, in which we are given a list of intervals and asked to find the minimum number of intervals to remove to eliminate any overlap".
We sort the intervals by their end times, and then iterate over each interval, keeping a count of all intervals that DO NOT overlap with the last interval in the non-overlapping set. We return the total number of intervals minus the count of NON-overlapping intervals.
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
Practice Problems
Working through these questions will give you more practice with intervals:
Done
	
Question
	
Difficulty


	
Can Attend Meetings
	
Easy


	
Insert Interval
	
Medium


	
Non-Overlapping Intervals
	
Medium


	
Merge Intervals
	
Medium


	
Employee Free Time
	
Hard

Mark as read

Next: Can Attend Meetings

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
D
DirectLimeMoth809
• 1 year ago

On nonOverlappingIntervals,
why do you return len(intervals) - count ? why not just count ?

9

Reply
P
ProudAmethystKiwi382
Premium
• 1 year ago

Because the problem what we are solving is "to return the minimum number of intervals that must be removed from a given array , where consists of a starting point and an ending point , to ensure that the remaining intervals do not overlap"

12

Reply
Alex Butera
Premium
• 7 months ago

Non-Overlapping Intervals paragraph contains two mistakes. It currently says:

"We sort the intervals by their end times, and then iterate over each interval, keeping a count of all intervals that overlap with the last interval in the non-overlapping set. We return the total number of intervals minus the count of overlapping intervals."

Instead it should say:
"We sort the intervals by their end times, and then iterate over each interval, keeping a count of all intervals that DO NOT overlap with the last interval in the non-overlapping set. We return the total number of intervals minus the count of **NON-**overlapping intervals."

4

Reply
C
CasualIvoryGoat374
Premium
• 10 months ago

The description for Non-Overlapping Intervals is incorrect. Even the original problem page says that this problem's goal is to return the number of intervals to remove to get non-overlapping intervals. But that is not the description used for this problem within this page, which instead says the goal is to return number of non-overlapping intervals, though the code solution here reflects the original problem's described goals.

1

Reply
E
ElegantGoldMeadowlark796
Premium
• 10 months ago

Is the solution correct? I have 4 non overlapping intervals, but this code returns 0 as the answer.

In [139]: intervals
Out[139]: [[4, 6], [7, 10], [11, 17], [18, 19]]

In [140]: nonOverlappingIntervals(intervals)
Out[140]: 0

Should just return count.

1

Reply
praveen kurmala
Premium
• 2 months ago

In my opinion - output =0 is correct.

Per question it is to identify minimum number of intervals to remove to eliminate any overlap.

Given your input does not have any overlapping intervals, no need to remove any interval. so the output should be zero.

1

Reply
mohammad nayeem
• 1 year ago
public static boolean canAttendMeetings(int[][] intervals) {
    Arrays.sort(intervals, Comparator.comparingInt(a -> a[0]));
    
    for (int i = 1; i < intervals.length; i++) {
        if (intervals[i][0] < intervals[i - 1][1]) {
            return false;
        }
    }
    
    return true;
}

1

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Sorting by Start Time

Overlapping Intervals

Merging Intervals

Sorting by End Time

Non-Overlapping Intervals

Practice Problems