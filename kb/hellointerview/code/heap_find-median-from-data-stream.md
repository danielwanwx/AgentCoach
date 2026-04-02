# Find Median from Data Stream

> Source: https://www.hellointerview.com/learn/code/heap/find-median-from-data-stream
> Scraped: 2026-03-30

Find Median from Data Stream
hard
DESCRIPTION (inspired by Leetcode.com)

A live analytics dashboard starts with nums. New readings arrive in order in adds. After each incoming value is inserted, return the current median of all readings seen so far. If the count is even, the median is the average of the two middle values.

Example 1:

Inputs:

nums = [5, 2, 8]
adds = [3, 10, 4]

Output:

[4, 5, 4.5]
CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def medianStream(self, nums: List[int], adds: List[int]) -> List
    [float]:
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

Building Intuition
Picture a live dashboard that keeps updating as new readings arrive. After each new value, you want the median of everything seen so far, not the average.
Here is the concrete example we will use throughout the page:
nums = [5, 2, 8]
adds = [3, 10, 4]
Starting readings
5
2
8
Incoming
3
10
4
Goal after each new reading
return the median of
all readings so far
Approach 1: Sort Every Time
The most direct idea is to keep every value in a list, insert the new value, sort, then pick the middle.
If there are n values so far, that sort costs O(n log n). Doing it after each of m incoming values becomes O(m * n log n). It works, but it does not scale.
Why That Hurts
Most of the list is not needed. The median only cares about the middle, so sorting everything over and over is wasted effort.
What Do We Actually Need?
Think about what the median really is. If we have a sorted list, the median is just one or two middle values. We don't need to know the exact position of every element, we only need a way to quickly access the middle value(s).
So, the problem actually becomes: Can we track the middle elements without sorting everything?
Let's think about what we know at any point:
Middle value divides the list into 2 halfs, one having all elements smaller to middle while other having all numbers larger than middle value.
We need to split all values into these two groups: smaller half and larger half
The median is either the largest value from the smaller half, or the average of the largest from smaller and smallest from larger
Using this observation, we need:
Quick access to the maximum of the smaller half
Quick access to the minimum of the larger half
Does that remind you of any data structure?
Building Toward Heaps
What if we maintained two separate collections:
One holding the smaller values, where we can quickly grab the largest one
One holding the larger values, where we can quickly grab the smallest one
A max-heap gives us the maximum in O(1) time. A min-heap gives us the minimum in O(1) time. And both allow insertions in O(log n).
So, if we keep:
The smaller half in a max-heap (so the top is the boundary)
The larger half in a min-heap (so the top is the boundary)
Then the median is always right there at the tops of the heaps.
But there's one more thing: we need to keep the heaps balanced. If one heap gets too large, the median calculation breaks. We'll need to rebalance by moving elements between heaps.
Approach 2: Split the Stream Into Two Heaps
Keep two heaps that always stay balanced:
A max-heap lower holds the smaller half of the numbers.
A min-heap upper holds the larger half.
The top of lower is the largest value in the lower half, and the top of upper is the smallest value in the upper half.
That gives us the median immediately:
If both heaps are the same size, median = (lowerTop + upperTop) / 2.
If lower has one extra element, median = lowerTop.
We always keep lower either the same size as upper or one element larger. That way the median is always at the top of one or two heaps.
Pseudocode
medianStream(nums, adds)
    lower = maxHeap
    upper = minHeap

    for num in nums
        addNum(lower, upper, num)

    result = empty list
    for val in adds
        addNum(lower, upper, val)
        result.append(getMedian(lower, upper))

    return result

addNum(lower, upper, value)
    if lower is empty OR value <= lower.top
        lower.push(value)
    else
        upper.push(value)

    if lower.size > upper.size + 1
        upper.push(lower.pop())
    else if upper.size > lower.size
        lower.push(upper.pop())

getMedian(lower, upper)
    if lower.size == upper.size
        return (lower.top + upper.top) / 2
    return lower.top
Walkthrough
We will trace nums = [5, 2, 8] and adds = [3, 10, 4]. We will keep two heaps: lower (max-heap) and upper (min-heap).
Step 1: Seed the heaps with nums
Insert 5, 2, and 8 one by one. The smaller half ends up in lower, the larger half in upper. After balancing, lower = [5, 2] and upper = [8].
lower has one extra element, so the median is the top of lower: median = 5.
Lower (max-heap)
5
2
Upper (min-heap)
8
median = 5
Step 2: Add 3
3 belongs in the lower half because 3 <= 5. Now lower = [5, 3, 2] and upper = [8], which is too imbalanced. We rebalance by moving the top of lower to upper.
After rebalancing, lower = [3, 2] and upper = [5, 8]. The heaps are the same size, so the median is the average: (3 + 5) / 2 = 4.
Lower (max-heap)
3
2
Upper (min-heap)
5
8
median = (3 + 5) / 2 = 4
Step 3: Add 10
10 is larger than lower's top 3, so it goes to upper: upper = [5, 8, 10]. Now upper is larger, so we move its top 5 back to lower.
After rebalancing, lower = [5, 3, 2] and upper = [8, 10]. lower is larger by one, so the median is 5.
Lower (max-heap)
5
3
2
Upper (min-heap)
8
10
median = 5
Step 4: Add 4
4 <= 5, so it goes to lower. Now lower = [5, 4, 3, 2] and upper = [8, 10]. That is too lopsided, so we move 5 to upper.
After balancing, lower = [4, 3, 2] and upper = [5, 8, 10]. The heaps are the same size, so the median is (4 + 5) / 2 = 4.5.
Lower (max-heap)
4
3
2
Upper (min-heap)
5
8
10
median = (4 + 5) / 2 = 4.5
Result
After each add, the medians are [4, 5, 4.5].
Solution
We keep a max-heap for the lower half and a min-heap for the upper half. Each insert goes to one heap, then we rebalance so the sizes stay within 1. The median is always on top of one heap or the average of the two tops.
nums
​
|
nums
starting readings
adds
​
|
adds
incoming readings
Try these examples:
Multiple
Short
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
import heapq

def median_stream(nums, adds):
    lower = []
    upper = []

    def add_num(value):
        if not lower or value <= -lower[0]:
            heapq.heappush(lower, -value)
        else:
            heapq.heappush(upper, value)

        if len(lower) > len(upper) + 1:
            heapq.heappush(upper, -heapq.heappop(lower))
        elif len(upper) > len(lower):
            heapq.heappush(lower, -heapq.heappop(upper))

    def get_median():
        if len(lower) == len(upper):
            return (-lower[0] + upper[0]) / 2
        return -lower[0]

    for num in nums:
        add_num(num)

    result = []
    for val in adds:
        add_num(val)
        result.append(get_median())

    return result
Lower half (max-heap)
Upper half (min-heap)
lowerTop
-
upperTop
-
median
-

Track the running median with a max-heap for the lower half and a min-heap for the upper half

0 / 20

1x
Watch the lower max-heap and upper min-heap rebalance while the median updates after each incoming value.
What is the time complexity of this solution?
1

O(x * y)

2

O(V + E)

3

O((n + m) log (n + m))

4

O(n³)

Mark as read

Next: Introduction

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

(3)

Comment
Anonymous
KT
kisan team outing
Premium
• 8 days ago

Use this way more simple and understandable.

class Solution {
private:
    // Member variables: These hold the state across function calls
    priority_queue<int> maxHeap; 
    priority_queue<int, vector<int>, greater<int>> minHeap;

    // Helper Function 1: Adds a number and keeps the two halves balanced
    void addNum(int num) {
        maxHeap.push(num);
        
        // Step 1: Force the largest of the small half into the large half
        minHeap.push(maxHeap.top());
        maxHeap.pop();

        // Step 2: If the large half is bigger, move one back to the small half
        // This ensures maxHeap.size() is always >= minHeap.size()
        if (minHeap.size() > maxHeap.size()) {
            maxHeap.push(minHeap.top());
            minHeap.pop();
        }
    }

    // Helper Function 2: Calculates the median based on current heap sizes
    float getMedian() {
        if (maxHeap.size() > minHeap.size()) {
            // Odd number of elements: maxHeap has the middle one
            return (float)maxHeap.top();
        } else {
            // Even number of elements: Average of the two middle ones
            // Using 2.0f ensures the result is a float, not an integer
            return (maxHeap.top() + minHeap.top()) / 2.0f;
        }
    }

public:
    vector<float> medianStream(vector<int> nums, vector<int> adds) {
        vector<float> result;

        // 1. Process the initial static data
        for (int n : nums) {
            addNum(n);
        }

        // 2. Process the dynamic 'adds' and record the median each time
        for (int a : adds) {
            addNum(a);
            result.push_back(getMedian());
        }

        return result;
    }
};
Show More

0

Reply
R
RunningCoralPuppy575
Premium
• 1 month ago
class Solution {
public:
    vector<float> medianStream(vector<int> nums, vector<int> adds) {
        // Your code goes here
        vector<float> fans;

        multiset<int> mini,maxi;
        for(auto p : nums){
            maxi.insert(p);
            int sz1=mini.size();
            int sz2=maxi.size();
            if(sz2>sz1){
                auto fk=*maxi.begin();
                mini.insert(fk);
                maxi.erase(maxi.find(fk));
            }
            if(!mini.empty() && !maxi.empty() && (*mini.rbegin()) > (*maxi.begin())){
                auto fk1=*mini.rbegin();
                auto fk2=*maxi.begin();
                mini.erase(mini.find(fk1));
                maxi.erase(maxi.find(fk2));
                mini.insert(fk2);
                maxi.insert(fk1);
            }
        }

        for(auto p : adds){
            maxi.insert(p);
            int sz1=mini.size();
            int sz2=maxi.size();
            if(sz2>sz1){
                auto fk=*maxi.begin();
                mini.insert(fk);
                maxi.erase(maxi.find(fk));
            }
            if(!mini.empty() && !maxi.empty() && (*mini.rbegin()) > (*maxi.begin())){
                auto fk1=*mini.rbegin();
                auto fk2=*maxi.begin();
                mini.erase(mini.find(fk1));
                maxi.erase(maxi.find(fk2));
                mini.insert(fk2);
                maxi.insert(fk1);
            }
            float ans=*mini.rbegin();
            if(mini.size()==maxi.size()){
                float ans1=*maxi.begin();
                ans+=ans1;
                ans/=2.0;
            }
            fans.push_back(ans);
        }

        return fans;
    }
};
Show More

0

Reply
fz zy
Premium
• 1 month ago
import heapq

class Solution:
    def medianStream(self, nums: List[int], adds: List[int]):
        max_heap, min_heap, ans = [], [], []
        for num in nums:
           heapq.heappush(min_heap, -heapq.heappushpop(max_heap, -num))
           if len(min_heap) > len(max_heap) + 1:
                heapq.heappush(max_heap, -heapq.heappop(min_heap))
        for num in adds:
            heapq.heappush(min_heap, -heapq.heappushpop(max_heap, -num))
            if len(min_heap) > len(max_heap) + 1:
                heapq.heappush(max_heap, -heapq.heappop(min_heap))
            if len(min_heap) == len(max_heap):
                ans.append((min_heap[0] - max_heap[0]) / 2)
                continue
            ans.append(min_heap[0]) 
        return ans

0

Reply
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Building Intuition

Approach 1: Sort Every Time

Why That Hurts

What Do We Actually Need?

Building Toward Heaps

Approach 2: Split the Stream Into Two Heaps

Pseudocode

Walkthrough

Solution