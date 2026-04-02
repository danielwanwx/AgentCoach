# Kth Largest Element in an Array

> Source: https://www.hellointerview.com/learn/code/heap/kth-largest-element-in-an-array
> Scraped: 2026-03-30


Heap
Kth Largest Element in an Array
medium
DESCRIPTION (inspired by Leetcode.com)

Write a function that takes an array of unsorted integers nums and an integer k, and returns the kth largest element in the array. This function should run in O(n log k) time, where n is the length of the array.

Example 1:

Inputs:

nums = [5, 3, 2, 1, 4]
k = 2

Output:

4
CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def kthLargest(self, nums: List[int], k: int) -> int:
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
Approach 1: Sorting
The simplest approach is to sort the array in descending order and return the kth element. This approach has a time complexity of O(n log n) where n is the number of elements in the array, and a space complexity of O(1).
Approach 2: Min Heap
By using a min-heap, we can reduce the time complexity to O(n log k), where n is the number of elements in the array and k is the value of k.
The idea behind this solution is to iterate over the elements in the array while storing the k largest elements we've seen so far in a min-heap. At each element, we check if it is greater than the smallest element (the root) of the heap. If it is, we pop the smallest element from the heap and push the current element into the heap. This way, the heap will always contain the k largest elements we've seen so far.
After iterating over all the elements, the root of the heap will be the kth largest element in the array.
Solution
nums
​
|
nums
list of integers
k
​
|
k
integer
Try these examples:
Single
Top Two
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def kth_largest(nums, k):
    if not nums:
        return 
    
    heap = []
    for num in nums:
        if len(heap) < k:
            heapq.heappush(heap, num)
        elif num > heap[0]:
            heapq.heappushpop(heap, num)
    
    return heap[0]
5
3
2
1
4

kth largest element in an array

0 / 10

1x
What is the time complexity of this solution?
1

O(N + Q)

2

O(n log k)

3

O(log n)

4

O(4^L)

Mark as read

Next: K Closest Points to Origin

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

(22)

Comment
Anonymous
​
Sort By
Popular
Sort By
A
AssociatedGoldScorpion296
• 1 year ago

Would you be able to add a solution with quick select as well, since it is a popular follow up?

12

Reply
VK
Varun Kolanu
Top 10%
• 5 months ago

QuickSelect:
Though this hits TLE in Leetcode for n <= 10^5 because even when we use random pivot, it can't help when all the elements in an array are equal. Then the time complexity becomes O(n^2 as:

T(n) = T(n-1) + n
==> T(n) = T(n-2) + (n-1) + n
...
==> T(n) = T(1) + 2 + 3 + ... n
==> T(n) = n(n+1)/2 =~ O(n^2)

CPP:

class Solution {
public:
    // Returns pivot index
    int getPivot(vector<int> &nums, int l, int r) {
        /*
        Returns `i` such that:
            nums[ind] >= nums[i] for all ind < i
            nums[ind] < nums[i] for all ind > i
        */

        int pivotIndex = l + rand() % (r - l + 1);
        swap(nums[pivotIndex], nums[r]);

        int i = l;
        for (int j=l; j<=r-1; ++j) {
            // Change the condition to nums[j] <= nums[r]
            // if the question is Kth Smallest Element
            if (nums[j] >= nums[r]) {
                swap(nums[j], nums[i]);
                ++i;
            }
        }
        swap(nums[i], nums[r]);
        return i;
    }

    int helperFindKthLargest(vector<int> &nums, int l, int r, int k) {
        int pivot = getPivot(nums, l, r);

        if (pivot - l == k-1)
            return nums[pivot];
        
        if (pivot -l >= k)
            return helperFindKthLargest(nums, l, pivot-1, k);
        
        return helperFindKthLargest(nums, pivot + 1, r, k - (pivot - l + 1));
    }

    int findKthLargest(vector<int>& nums, int k) {
        return helperFindKthLargest(nums, 0, nums.size()-1, k);
    }
};
Show More

2

Reply
Tony Kuo
Premium
• 14 days ago

Quick select, the worst case time complexity is n^2, by average it can be n and O(1) space (without counting the func calls in stack)

0

Reply
Abhay Singh
Top 1%
• 1 year ago

Java Solution:

class Solution {
    public int findKthLargest(int[] nums, int k) {
        PriorityQueue<Integer> pq = new PriorityQueue<>();
        for(int val : nums){
            pq.add(val);

            if(pq.size() > k){
                pq.poll();
            }
        }

        return pq.poll();
    }
}

2

Reply
P
PureGrayCheetah337
Premium
• 1 month ago

Here is my solution:
import heapq
class Solution:
def kthLargest(self, nums: List[int], k: int):
if not nums:
raise ValueError("Empty input")
if k <= 0 or k > len(nums):
raise ValueError(f"Invalid k: {k}")
return heapq.nlargest(k, nums)[-1]

1

Reply
Arun Ramakrishnan
Premium
• 3 months ago

Quick-select solution in Java

    public Integer kthLargest(int[] nums, Integer k) {
        // O(n) on avg. Can pretty much guarantee if preprocessed with Knuth shuffle
        int n = nums.length;
        quickSelect(nums, n-k, 0, n-1);
        return nums[n-k];
    }
    private void quickSelect(int[] nums, int k, int lo, int hi)
    {
        if (hi <= lo)
            return;

        int lt = lo; //elements less than pivot are on the left of lt
        int gt = hi; //elements greater than pivot are on the right of gt
        int i = lo; //current index (unexplored). elemets equal to pivot are between lt(inclusive) and i(exclusive)
        int pivot = nums[lo];
        while (i <= gt)
        {
            if (nums[i] == pivot)
                i++;
            else if (nums[i] < pivot)
                exchange(nums, i++, lt++);
            else
                exchange(nums, i, gt--);
        }

        if (k < lt)
            quickSelect(nums, k, lo, lt-1); // O(n) + O(n/2) + O(n/4).. O(1) -> O(2n)-> O(n)
        else if (k > gt)
            quickSelect(nums, k, gt+1, hi);
        else
            return;
    }
    private void exchange (int[] nums, int i, int j)
    {
        int temp = nums[i];
        nums[i] = nums[j];
        nums[j] = temp;
    }
}
Show More

1

Reply
Swapnil
Premium
• 2 months ago

Meta is super interested on this method.

0

Reply
Joy Elo-oghene
• 5 months ago

This was my solution

class Solution:
```python
def kthLargest(self, nums: List[int], k: int):
negated = [-x for x in nums]

    heapq.heapify(negated)

    for _ in range(k):
        kth_max = -heapq.heappop(negated)
    return kth_max


1

Reply
Anh Minh Nguyễn Đoàn
• 3 months ago

this solution takes O(n + logk * n) time complexity and O(n) space complexity.

0

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

Approach 1: Sorting

Approach 2: Min Heap

Solution
