# Maximum Profit in Job Scheduling

> Source: https://www.hellointerview.com/learn/code/dynamic-programming/maximum-profit-in-job-scheduling
> Scraped: 2026-03-30


Given three arrays, starts, ends, and profits, each representing the start time, end time, and profit of jobs respectively, your task is to schedule the jobs to maximize total profit. You can only work on one job at a time, and once a job has been started, you must finish it before starting another. The goal is to find the maximum profit that can be earned by scheduling jobs such that they do not overlap.

Input:

starts = [1, 3, 6, 10]
ends = [4, 5, 10, 12]
profits = [20, 20, 100, 70]

The optimal solution would schedule the jobs as follows:

Start the first job at time 1 and complete it by 4 for a profit of 20. Start the next job at time 6 and complete it by 10 for a profit of 100. Start the last job at time 10 and complete it by 12 for a profit of 70.

The total profit is 20 + 100 + 70 = 190

CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def job_scheduling(self, startTime: List[int], endTime: List[int], 
    profit: List[int]) -> int:
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
Note: The solution below uses the key parameter in the bisect_right function to find the latest job ending before the start time of the current job, which is only available in Python 3.10 and above.
The idea behind this solution is to first sort the jobs by their end times. Afterwards, we initialize an array dp of length len(jobs) + 1 with 0s, where dp[i] represents the maximum profit that can be earned by scheduling the first i jobs (sorted by end time). dp[0] is initialized to 0, as scheduling 0 jobs would yield 0 profit.
VISUALIZATION
Python
Language
Full Screen
from bisect import bisect_right

def job_scheduling(starts, ends, profits):
    jobs = sorted(zip(starts, ends, profits),
                  key=lambda x: x[1])

    dp = [0] * (len(jobs) + 1)
    for i in range(1, len(jobs) + 1):
        start, end, profit = jobs[i - 1]
        # find number of jobs to finish before start of current job
        num_jobs = bisect_right([job[1] for job in jobs], start)
        
        dp[i] = max(dp[i - 1], dp[num_jobs] + profit)
        
    return dp[-1]

maximum profit in job scheduling

0 / 2

1x
Sorting and initializing `dp` array
Next, we iterate over each index in dp starting from index 1. At each iteration, we calculate the maximum profit that can be earned by scheduling the first i jobs (sorted by end time). So when i = 1, we are calculating the maximum profit that can be earned by scheduling the first job.
1). We find the corresponding start time and profit of the current job (jobs[i - 1]).
2). Next, we use binary search (bisect_right) to find the number of jobs that have ended before the start time of the current job, and store this number in a variable num_jobs. dp[num_jobs] will also tell us the maximum profit that can be earned by scheduling all the jobs that have ended before the current job.
To breakdown our call to bisect_right: we are looking for the rightmost index in job in job with an end time (key=lambda x: x[1]) that is less than or equal to the start time of the current job (start).
In this case, start = 1, which means this is the first job we can possibly schedule, and num_jobs = 0.
VISUALIZATION
Python
Language
Full Screen
from bisect import bisect_right

def job_scheduling(starts, ends, profits):
    jobs = sorted(zip(starts, ends, profits),
                  key=lambda x: x[1])

    dp = [0] * (len(jobs) + 1)
    for i in range(1, len(jobs) + 1):
        start, end, profit = jobs[i - 1]
        # find number of jobs to finish before start of current job
        num_jobs = bisect_right([job[1] for job in jobs], start)
        
        dp[i] = max(dp[i - 1], dp[num_jobs] + profit)
        
    return dp[-1]
]
[
4
1
20
]
[
5
3
18
]
[
8
4
70
]
[
10
5
100
0
0
0
0
0

initialize dp array

0 / 2

1x
Finding the latest job ending before the start time of the current job
Once we have this index, we have two options:
We can schedule the current job, in which case the profit would be dp[num_jobs] + profit.
We can skip the current job, in which case the profit would be dp[i - 1].
By taking the maximum of these two options, we can calculate the maximum profit that can be earned by scheduling the first i jobs.
In this case, since this is the first job we can possibly schedule, we schedule it and update dp[i] to dp[num_jobs] + profit.
VISUALIZATION
Python
Language
Full Screen
from bisect import bisect_right

def job_scheduling(starts, ends, profits):
    jobs = sorted(zip(starts, ends, profits),
                  key=lambda x: x[1])

    dp = [0] * (len(jobs) + 1)
    for i in range(1, len(jobs) + 1):
        start, end, profit = jobs[i - 1]
        # find number of jobs to finish before start of current job
        num_jobs = bisect_right([job[1] for job in jobs], start)
        
        dp[i] = max(dp[i - 1], dp[num_jobs] + profit)
        
    return dp[-1]
]
[
4
1
20
]
[
5
3
18
]
[
8
4
70
]
[
10
5
100
0
0
0
0
0
num_jobs = 0
i = 1

num_jobs = 0

0 / 1

1x
Calculating the maximum profit that can be earned by scheduling the first job
Skipping The Current Job
The next iteration is an example of when we would choose to skip the current job. For this job, start = 3. This job overlaps with the first job, so num_jobs = 0. If we consider the two cases:
We can schedule the current job, in which case the profit would be dp[num_jobs] + profit = 0 + 18 = 18.
We can skip the current job, in which case the profit would be dp[i - 1] = 20.
We can see that skipping the current job (in favor of choosing the previous one) would yield a higher profit, so we update dp[i] to dp[i - 1].
VISUALIZATION
Python
Language
Full Screen
from bisect import bisect_right

def job_scheduling(starts, ends, profits):
    jobs = sorted(zip(starts, ends, profits),
                  key=lambda x: x[1])

    dp = [0] * (len(jobs) + 1)
    for i in range(1, len(jobs) + 1):
        start, end, profit = jobs[i - 1]
        # find number of jobs to finish before start of current job
        num_jobs = bisect_right([job[1] for job in jobs], start)
        
        dp[i] = max(dp[i - 1], dp[num_jobs] + profit)
        
    return dp[-1]
]
[
4
1
20
]
[
5
3
18
]
[
8
4
70
]
[
10
5
100
0
20
0
0
0
num_jobs = 0
i = 1

dp[1] = max(0, 0 + 20)

0 / 3

1x
Calculating the maximum profit that can be earned by scheduling the first job
If we examine the state of the dp array at this point, it tells us at that the maximum profit we can obtain from scheduling any combination of the first two jobs is 20.
We can continue this process for the remaining jobs, and the final value of dp[-1] will tell us the maximum profit that can be earned by scheduling all the jobs.
Solution
starts
​
|
starts
list of integers
ends
​
|
ends
list of integers
profits
​
|
profits
list of integers
Try these examples:
One Job
Short Mix
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
from bisect import bisect_right

def job_scheduling(starts, ends, profits):
    jobs = sorted(zip(starts, ends, profits),
                  key=lambda x: x[1])

    dp = [0] * (len(jobs) + 1)
    for i in range(1, len(jobs) + 1):
        start, end, profit = jobs[i - 1]
        # find number of jobs to finish before start of current job
        num_jobs = bisect_right([job[1] for job in jobs], start)
        
        dp[i] = max(dp[i - 1], dp[num_jobs] + profit)
        
    return dp[-1]

maximum profit in job scheduling

0 / 15

1x
What is the time complexity of this solution?
1

O(n * logn)

2

O(2ⁿ)

3

O(n!)

4

O(n²)

Mark as read

Next: Paint House

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

(15)

Comment
Anonymous
​
Sort By
Popular
Sort By
S
selectfromall
Top 5%
• 9 months ago

IMO, cleaner Python code without using all those built-in functions:

class Job:
    def __init__(self, start, end, profit):
        self.start = start
        self.end = end
        self.profit = profit

class Solution:
    def jobScheduling(
        self, startTime: List[int], endTime: List[int], profit: List[int]
    ) -> int:
        jobs = [Job(startTime[i], endTime[i], profit[i]) for i in range(len(profit))]
        jobs.sort(key=lambda j: j.end)

        dp = [0] * len(jobs)
        dp[0] = jobs[0].profit

        for i in range(1, len(jobs)):
            job = jobs[i]
            maxProfit = job.profit

            left = 0
            right = i - 1
            jobIdx = None
            while left <= right:
                mid = (left + right) // 2
                if jobs[mid].end <= job.start:
                    jobIdx = mid
                    left = mid + 1
                else:
                    right = mid - 1

            if jobIdx is not None:
                maxProfit += dp[jobIdx]

            dp[i] = max(dp[i - 1], maxProfit)

        return dp[-1]
Show More

4

Reply
S
socialguy
Top 5%
• 1 year ago

The loop range is off by 1. Do you actually run the code? Also:

bisect_right() got an unexpected keyword argument 'key'

4

Reply
T
TastyAzurePorpoise110
• 1 year ago

I believe the input of the example at the top of the page is incorrect.
The input has the 4th job starting at 9 and ending at 8, which doesn't make sense :)

Also, the description in the leetcode page has the follwing constraints:
1 <= startTime.length == endTime.length == profit.length <= 5 * 104
1 <= startTime[i] < endTime[i] <= 109
1 <= profit[i] <= 104

2

Reply
C
ConservativeLimeBarnacle928
Premium
• 11 months ago

start time is 4 (job4)

0

Reply
V
vmlellis
Premium
• 10 days ago
• edited 10 days ago

My DP solution in Go:

func jobScheduling(startTime []int, endTime []int, profit []int) int {
    n := len(startTime)
    jobs := make([][3]int, n)
    for i := range n {
        jobs[i] = [3]int{startTime[i], endTime[i], profit[i]}
    }

    sort.Slice(jobs, func(i, j int) bool {
        return jobs[i][1] < jobs[j][1]
    })

    dp := make([]int, n + 1)
    for i := 1; i <= n; i++ {
        start, profit := jobs[i-1][0], jobs[i-1][2]

        j := sort.Search(n, func(k int) bool {
            return jobs[k][1] > start
        }) - 1;

        take := profit
        if j >= 0 {
            take += dp[j+1]
        }

        if take > dp[i-1] {
            dp[i] = take
        } else {
            dp[i] = dp[i-1]
        }
    }

    return dp[n]
}
Show More

0

Reply
Shivam Choudhary
Premium
• 1 month ago

/usr/bin/ld: /tmp/cccFsqU0.o: in function cmp1(std::vector<int, std::allocator<int> >&, std::vector<int, std::allocator<int> >&)': TestSolution.cpp:(.text+0x0): multiple definition of cmp1(std::vector<int, std::allocator<int> >&, std::vector<int, std::allocator<int> >&)'; /tmp/ccsDZzhJ.o:Solution.cpp:(.text+0x0): first defined here
collect2: error: ld returned 1 exit status

correct  it

0

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

Skipping the current job

Solution
