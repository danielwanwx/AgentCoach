# Employee Free Time

> Source: https://www.hellointerview.com/learn/code/intervals/employee-free-time
> Scraped: 2026-03-30


Intervals
Employee Free Time
hard
DESCRIPTION (inspired by Leetcode.com)

Write a function to find the common free time for all employees from a list called schedule. Each employee's schedule is represented by a list of non-overlapping intervals sorted by start times. The function should return a list of finite, non-zero length intervals where all employees are free, also sorted in order.

Input:

schedule = [[[2,4],[7,10]],[[1,5]],[[6,9]]]

Output:

[(5,6)]

Explanation: The three employees collectively have only one common free time interval, which is from 5 to 6.

CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def employeeFreeTime(self, schedule: List[List[List[int]]]) -> List
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

Explanation
This problems builds upon the concept of merging intervals. We can solve this problem by first merging all the employee meeting intervals into a single list. The free times are then the gaps between those merged intervals.
Important Note on Boundaries: In this problem, we only consider the gaps between busy intervals as free time. We do not consider:
Time before the earliest busy interval (e.g., if the first meeting starts at 9:00 AM, we don't count 8:00-9:00 AM as "free time")
Time after the latest busy interval (e.g., if the last meeting ends at 5:00 PM, we don't count 5:00-6:00 PM as "free time")
This is because the problem asks for common free time when all employees are available, and we're only given their scheduled busy intervals within a certain working timeframe.
Phase 1
We first want to flatten the list of intervals into a single list, and then sorting them by their start time to make the merge process easier.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def employeeFreeTime(schedule):
    flattened = [i for employee in schedule for i in employee]
    intervals = sorted(flattened, key=lambda x: x[0])

    merged = []
    for interval in intervals:
        if not merged or merged[-1][1] < interval[0]:
            merged.append(interval)
        else:
            merged[-1][1] = max(merged[-1][1], interval[1])

    free_times = []
    for i in range(1, len(merged)):
        start = merged[i-1][1]
        end = merged[i][0]
        free_times.append([start, end])

    return free_times
]
[
4
2
]
[
10
7
]
[
5
1
]
[
9
6
merged
free_times

employee free time

0 / 1

1x
Phase 2
Next, we want to merge all the intervals into a single list. We can do this by iterating through the list of intervals and comparing the end time of the current interval with the start time of the next interval. If the end time of the current interval is greater than or equal to the start time of the next interval, we merge the two intervals. Otherwise, we add the current interval to the merged list.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def employeeFreeTime(schedule):
    flattened = [i for employee in schedule for i in employee]
    intervals = sorted(flattened, key=lambda x: x[0])

    merged = []
    for interval in intervals:
        if not merged or merged[-1][1] < interval[0]:
            merged.append(interval)
        else:
            merged[-1][1] = max(merged[-1][1], interval[1])

    free_times = []
    for i in range(1, len(merged)):
        start = merged[i-1][1]
        end = merged[i][0]
        free_times.append([start, end])

    return free_times
]
[
4
2
]
[
10
7
]
[
5
1
]
[
9
6
merged
free_times

merge intervals

0 / 8

1x
Phase 3
In this phase, we return the employee free times by finding the gaps between the merged intervals. We can do this by iterating through the merged intervals, and creating a new interval from the end time of the current interval and the start time of the next interval.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def employeeFreeTime(schedule):
    flattened = [i for employee in schedule for i in employee]
    intervals = sorted(flattened, key=lambda x: x[0])

    merged = []
    for interval in intervals:
        if not merged or merged[-1][1] < interval[0]:
            merged.append(interval)
        else:
            merged[-1][1] = max(merged[-1][1], interval[1])

    free_times = []
    for i in range(1, len(merged)):
        start = merged[i-1][1]
        end = merged[i][0]
        free_times.append([start, end])

    return free_times
]
[
4
2
]
[
10
7
]
[
5
1
]
[
9
6
merged
]
[
5
1
]
[
10
6
free_times

merge

0 / 4

1x
What is the time complexity of this solution?
1

O(n³)

2

O(n * logn)

3

O(n²)

4

O(4ⁿ)

Solution
intervals
​
|
intervals
list of intervals [start, end]
Try these examples:
No Gaps
Clear Gap
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def employeeFreeTime(schedule):
    flattened = [i for employee in schedule for i in employee]
    intervals = sorted(flattened, key=lambda x: x[0])

    merged = []
    for interval in intervals:
        if not merged or merged[-1][1] < interval[0]:
            merged.append(interval)
        else:
            merged[-1][1] = max(merged[-1][1], interval[1])

    free_times = []
    for i in range(1, len(merged)):
        start = merged[i-1][1]
        end = merged[i][0]
        free_times.append([start, end])

    return free_times
]
[
4
2
]
[
10
7
]
[
5
1
]
[
9
6
merged
free_times

employee free time

0 / 14

1x

Mark as read

Next: Stack Overview

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

(39)

Comment
Anonymous
​
Sort By
Popular
Sort By
Yohannes Berhane
Premium
• 7 months ago

You don't need to merge the intervals. You can just create an all_intervals list which has all the intervals sorted by start and then just iterate from 1 -> end checking if current.start > (current-1).end. If so that means there is a gap. This is O(NlogN) and O(N) space where N is the number of intervals.

A better way to do this through a min heap where there is at most K (number of employees) intervals in the tree. This is O(Nlogk) and O(K) space

class Solution:
    def employeeFreeTime(self, schedule: List[List[List[int]]]):
        # Your code goes here
        free_time = []
        intervals = sorted(
            [i for employee in schedule for i in employee],
            key=lambda x: x[0]
        )

        for i in range(len(intervals)):
            if intervals[i][0] > intervals[i-1][1]:
                free_time.append((intervals[i-1][1], intervals[i][0]))
        
        return free_time
Show More

19

Reply
D
DeliberateMagentaHornet578
Premium
• 4 months ago

with sorted_interval = [[1, 10], [2, 3],  [6,7]]
won't the code give wrong free time as [3,6]?
also i in the for loop would start at 0 and i-1 will give you index out of bound

10

Reply
Shashi Kant
Premium
• 3 months ago

yup i used min heap as well.

0

Reply
MM
Minnie Mouse
Top 5%
• 5 months ago

I used the min heap approach as well but while reviewing hellointerview's solution, it didn't cross my mind that we don't even need to merge the intervals at all. Thanks for sharing!

0

Reply
S
socialguy
Top 5%
• 1 year ago

Problem description is unclear. It seems the employees are all free from 0-1, and after 10.

5

Reply
A
AddedLimeCarp593
Top 1%
• 9 months ago

I think we assume time begins at the earliest point and ends at the latest point.

2

Reply
I
ImplicitEmeraldVicuna183
• 1 year ago

Why there is no code editor here to code?

3

Reply
Nick Cushman
• 1 year ago

I'm assuming this is because the problem is locked on leetcode if you're not a premium member.

2

Reply
C
CalmIndigoPython390
Top 1%
• 1 year ago

Great observation, thanks for sharing!

0

Reply
Anurag K
Premium
• 1 year ago

+1, unable to try it out.

1

Reply
james war
• 11 days ago
• edited 11 days ago

Great breakdown of the “Employee Free Time” problem—this is a classic example of how important the interval merging pattern is in real-world scenarios. I really liked how the solution focuses on flattening all schedules, sorting them, and then identifying gaps after merging overlapping intervals. That approach makes the logic much cleaner and scalable.

What stood out to me is that the problem essentially reduces to identifying gaps between merged busy intervals, which is a very practical concept—not just for coding interviews but also for real-world workforce management systems.

Interestingly, this same concept is widely used in employee productivity and time tracking tools. For example, solutions like DeskTrack use similar logic to analyze working patterns, detect idle gaps, and provide insights into actual productive vs non-productive time.

So problems like this are not just theoretical—they directly map to how modern tools optimize team efficiency and scheduling.

Really helpful explanation overall—this is the kind of problem every developer should understand deeply!

2

Reply
Abhay Singh
Top 1%
• 1 year ago

Java Solution:

class Solution {
    public int[][] employeeFreeTime(int[][] intervals) {
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

        List<List<Integer>> availableTime = new ArrayList<>();
        for(int i=1;i<mergedIntervals.size();i++){
            int fs = mergedIntervals.get(i-1)[1];
            int fe = mergedIntervals.get(i)[0];
            availableTime.add(Arrays.asList(fs, fe));
        }

        int[][] ans = new int[availableTime.size()][2];
        for(int i=0;i<availableTime.size();i++){
            ans[i][0] = availableTime.get(i).get(0);
            ans[i][1] = availableTime.get(i).get(1);
        }

        return ans;
    }
}
Show More

2

Reply
Sudarshan Gawale
• 10 months ago

Thanks, suggestion: You can directly use List<int[]> in java. Returning 2-D array can also be simplified using return availableTime.toArray(new int[availableTime.size()][]);

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
