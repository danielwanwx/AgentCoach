# Can Attend Meetings

> Source: https://www.hellointerview.com/learn/code/intervals/can-attend-meetings
> Scraped: 2026-03-30


Intervals
Can Attend Meetings
easy
DESCRIPTION (inspired by Leetcode.com)

Write a function to check if a person can attend all the meetings scheduled without any time conflicts. Given an array intervals, where each element [s1, e1] represents a meeting starting at time s1 and ending at time e1, determine if there are any overlapping meetings. If there is no overlap between any meetings, return true; otherwise, return false.

Note that meetings ending and starting at the same time, such as (0,5) and (5,10), do not conflict.

Input:

intervals = [(1,5),(3,9),(6,8)]

Output:

false

Explanation: The meetings (1,5) and (3,9) overlap.

Input:

intervals = [(10,12),(6,9),(13,15)]

Output:

true

Explanation: There are no overlapping meetings, so the person can attend all.

CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def canAttendMeetings(self, intervals: List[List[int]]) -> bool:
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
A person can attend all meetings if and only if none of the meetings overlap. By sorting the intervals by start time, we can easily check if any two consecutive intervals overlap.
We iterate over each interval, beginning with the second interval in the sorted list. We compare the start time of the current interval with the end time of the previous interval. If the start time of the current interval is less than the end time of the previous interval, then the two intervals overlap and the person cannot attend both meetings, so we return false.
]
[
5
1
]
[
8
3
Two overlapping meeting intervals
Otherwise, the person can attend both meetings, and we continue to the next interval. If we reach the end of the list without finding any overlapping intervals, then the person can attend all meetings, and we return true.
Solution
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
Hide Code
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
What is the time complexity of this solution?
1

O(log m * n)

2

O(1)

3

O(V + E)

4

O(n * logn)

Mark as read

Next: Insert Interval

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

(25)

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

public class Solution {
    public boolean canAttendMeetings(int[][] intervals) {
        Arrays.sort(intervals, (a, b) -> a[0] - b[0]);

        for (int i = 1; i < intervals.length; i++) {
            if (intervals[i][0] < intervals[i - 1][1]) {
                return false;
            }
        }

        return true;
    }
}

9

Reply
U
UsualWhiteBobolink705
Premium
• 2 months ago

What if we sort by end times, will there be any issue?

0

Reply
Raj Kumar Meena
Premium
• 1 month ago

Yes, when you sort by end time, you are not aware which interval to compare the current one with.
Even the interval with the greatest end time can conflict with the one with the least end time.

0

Reply
aditya patel
Premium
• 1 month ago

Js Solution:
class Solution {
canAttend(intervals) {
const len = intervals.length;

    if(len <= 1) return true;

    // sort intervals 
    const sortedIntervals = intervals.slice().sort((a, b) => a[0] - b[0]);

    for(let i = 0; i < len; i++) {
      if(i > 0) {
        // check for overlap 
        // s2 < e1 means overlap is there 
        if(sortedIntervals[i][0] < sortedIntervals[i - 1][1]) {
          return false;
        }
      }
    }

    return true;
}


}

Show More

2

Reply
Ankit kumar Singh
• 2 months ago

nice kick start

2

Reply
Nick Name
• 18 days ago

It is a blessing that Hello Interview exists.
Continue what you are doing.
I love you

1

Reply
Chukwuemeka Duru
• 1 year ago

This Solution is O(n) and 0(1) time and space complexitiy. There is not need to sort the array. Just simple equality limits:

class Solution:
    def canAttendMeetings(self, intervals: list[list[int]]):
        # Your code goes here
        prev_s1 = intervals[0][0]
        prev_e1 = intervals[0][1]

        for idx in range(1, len(intervals)):
            cur_interval = intervals[idx]
            s1 = cur_interval[0]
            e1 = cur_interval[1]
            if prev_s1 < s1 < prev_e1:
                return False
            else:
                prev_s1 = s1
                prev_e1 = e1
        return True

1

Reply
R
RulingCoffeeOstrich196
• 1 year ago

it does not work for this test case [[10,20],[5,15]] , starts earlier and ends later.

3

Reply
A
amit
• 7 months ago

you need to sort it

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
