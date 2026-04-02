# 3-Sum

> Source: https://www.hellointerview.com/learn/code/two-pointers/3-sum
> Scraped: 2026-03-30


Two Pointers
3-Sum
medium
DESCRIPTION (inspired by Leetcode.com)

Given an input integer array nums, write a function to find all unique triplets [nums[i], nums[j], nums[k]] such that i, j, and k are distinct indices, and the sum of nums[i], nums[j], and nums[k] equals zero. Ensure that the resulting list does not contain any duplicate triplets.

Input:

nums = [-1,0,1,2,-1,-1]

Output:

[[-1,-1,2],[-1,0,1]]

Explanation: Both nums[0], nums[1], nums[2] and nums[1], nums[2], nums[4] both include [-1, 0, 1] and sum to 0. nums[0], nums[3], nums[4] ([-1,-1,2]) also sum to 0.

Since we are looking for unique triplets, we can ignore the duplicate [-1, 0, 1] triplet and return [[-1, -1, 2], [-1, 0, 1]].

The order of the triplets and the order of the elements within the triplets do not matter.

CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
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
nums
​
|
nums
comma-separated integers
Try these examples:
All Zeros
No Solution
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
class Solution:
    def threeSum(self, nums: List[int]):
      nums.sort()
      result = []
      for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]:
          continue
        left = i + 1
        right = len(nums) - 1
        while left < right:
          total = nums[i] + nums[left] + nums[right]
          if total < 0:
            left += 1
          elif total > 0:
            right -= 1
          else:
            result.append([nums[i], nums[left], nums[right]])
            while left < right and nums[left] == nums[left + 1]:
              left += 1
            while left < right and nums[right] == nums[right - 1]:
              right -= 1
            left += 1
            right -= 1
      return result
-1
0
1
2
-1
-1
Result

3 sum

0 / 18

1x
Explanation
We can leverage the two-pointer technique to solve this problem by first sorting the array. We can then iterate through each element in the array. The problem then reduces to finding two numbers in the rest of the array that sum to the negative of the current element, which follows the same logic as the Two Sum (Sorted Array) problem from the overview.
-1
0
1
2
-1
-1
Result

Since our first triplet sums to 0, we can add it to our result set.
VISUALIZATION
Hide Code
Python
Language
Full Screen
class Solution:
    def threeSum(self, nums: List[int]):
      nums.sort()
      result = []
      for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]:
          continue
        left = i + 1
        right = len(nums) - 1
        while left < right:
          total = nums[i] + nums[left] + nums[right]
          if total < 0:
            left += 1
          elif total > 0:
            right -= 1
          else:
            result.append([nums[i], nums[left], nums[right]])
            while left < right and nums[left] == nums[left + 1]:
              left += 1
            while left < right and nums[right] == nums[right - 1]:
              right -= 1
            left += 1
            right -= 1
      return result
-1
0
1
2
-1
-1
Result

3 sum

0 / 5

1x
Avoiding Duplicates
As soon as we find a triplet that sums to 0, we can add it to our result set. We then have to move our left and right pointers to look for the next triplet while avoiding duplicate triplets. We can do this by moving the left and right pointers until they point to different numbers than the ones they were pointing to before.
Here we move the left pointer once until it reaches the last -1 in the array. Then, we can move both the left and right pointers so that they both point to new numbers.
VISUALIZATION
Hide Code
Python
Language
Full Screen
class Solution:
    def threeSum(self, nums: List[int]):
      nums.sort()
      result = []
      for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]:
          continue
        left = i + 1
        right = len(nums) - 1
        while left < right:
          total = nums[i] + nums[left] + nums[right]
          if total < 0:
            left += 1
          elif total > 0:
            right -= 1
          else:
            result.append([nums[i], nums[left], nums[right]])
            while left < right and nums[left] == nums[left + 1]:
              left += 1
            while left < right and nums[right] == nums[right - 1]:
              right -= 1
            left += 1
            right -= 1
      return result
-1
0
1
2
-1
-1
i
left
right
0
Result

[-1, -1, 2]

add triplet to output

0 / 2

1x
Here we can do another iteration of the Two Sum problem using the new positions of the left and right pointers.
VISUALIZATION
Hide Code
Python
Language
Full Screen
class Solution:
    def threeSum(self, nums: List[int]):
      nums.sort()
      result = []
      for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]:
          continue
        left = i + 1
        right = len(nums) - 1
        while left < right:
          total = nums[i] + nums[left] + nums[right]
          if total < 0:
            left += 1
          elif total > 0:
            right -= 1
          else:
            result.append([nums[i], nums[left], nums[right]])
            while left < right and nums[left] == nums[left + 1]:
              left += 1
            while left < right and nums[right] == nums[right - 1]:
              right -= 1
            left += 1
            right -= 1
      return result
-1
0
1
2
-1
-1
i
left
right
0
Result

[-1, -1, 2]

move both pointers

0 / 3

1x
At this point our left and right pointers have crossed, so we can move our iterator to the next number in the array.
Avoiding Duplicates II
In this case, since the next number in the array is the same as the previous number, we can skip it. We can do this by moving our iterator until it points to a new number.
VISUALIZATION
Hide Code
Python
Language
Full Screen
class Solution:
    def threeSum(self, nums: List[int]):
      nums.sort()
      result = []
      for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]:
          continue
        left = i + 1
        right = len(nums) - 1
        while left < right:
          total = nums[i] + nums[left] + nums[right]
          if total < 0:
            left += 1
          elif total > 0:
            right -= 1
          else:
            result.append([nums[i], nums[left], nums[right]])
            while left < right and nums[left] == nums[left + 1]:
              left += 1
            while left < right and nums[right] == nums[right - 1]:
              right -= 1
            left += 1
            right -= 1
      return result
-1
0
1
2
-1
-1
i
left
right
0
Result

[-1, -1, 2]
[-1, 0, 1]

move both pointers

0 / 3

1x
And we're ready to start the Two Sum algorithm again, so we reset our left and right pointers, and start the algorithm.
VISUALIZATION
Hide Code
Python
Language
Full Screen
class Solution:
    def threeSum(self, nums: List[int]):
      nums.sort()
      result = []
      for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]:
          continue
        left = i + 1
        right = len(nums) - 1
        while left < right:
          total = nums[i] + nums[left] + nums[right]
          if total < 0:
            left += 1
          elif total > 0:
            right -= 1
          else:
            result.append([nums[i], nums[left], nums[right]])
            while left < right and nums[left] == nums[left + 1]:
              left += 1
            while left < right and nums[right] == nums[right - 1]:
              right -= 1
            left += 1
            right -= 1
      return result
-1
0
1
2
-1
-1
i
left
right
Result

[-1, -1, 2]
[-1, 0, 1]

initialize pointers

0 / 2

1x
Termination
Our algorithm terminates when i reaches the 3rd to last element in the array (i.e., i < n - 2). This is because we need at least 2 more elements after i for left and right to form a triplet.
VISUALIZATION
Hide Code
Python
Language
Full Screen
class Solution:
    def threeSum(self, nums: List[int]):
      nums.sort()
      result = []
      for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]:
          continue
        left = i + 1
        right = len(nums) - 1
        while left < right:
          total = nums[i] + nums[left] + nums[right]
          if total < 0:
            left += 1
          elif total > 0:
            right -= 1
          else:
            result.append([nums[i], nums[left], nums[right]])
            while left < right and nums[left] == nums[left + 1]:
              left += 1
            while left < right and nums[right] == nums[right - 1]:
              right -= 1
            left += 1
            right -= 1
      return result
-1
0
1
2
-1
-1
i
left
right
3
Result

[-1, -1, 2]
[-1, 0, 1]

move right pointer backward

0 / 2

1x
What is the time complexity of this solution?
1

O(m * n)

2

O(n²)

3

O(n³)

4

O(n * logn)

Mark as read

Next: Triangle Numbers

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

(50)

Comment
Anonymous
​
Sort By
Popular
Sort By
Allen Liu (Hsin-tzu)
Top 5%
• 8 months ago

I made a couple of extra optimizations to end the program execution early and cut overall run time by about 25%.

(1) if, after sorting, the last (i.e. the biggest) element is negative, return an empty list right away. (if the largest element is negative, all elements must be negative. Therefore, there will never be a zero from additions of any elements.)

if sorted_input_array[-1] < 0: return []

(2) In the out for loop iteration over the soerted input list, if the current element is greater than 0, skip ahead to the next iteration.

if sorted_input_array[i] > 0:
    continue

This is because left and right are both greater than the index i, there is no likelihood for them to neutralize the latter to produce a 0 sum.

36

Reply
VK
Varun Kolanu
Top 10%
• 5 months ago

Wouldn't break be better in the point (2) rather than continue? Because we won't be finding the zero sum after the current index, if sorted_input_array[i] > 0

14

Reply
E
elapidae
Premium
• 4 days ago
• edited 4 days ago

Small suggestion for optimization (1):
Finding max of an input array takes O(n), whereas sorting it takes O(n*logn), so to check if all the elements are negative, rather iterate once then sorting first. Also, you don't even need to find max, it's more expensive(in terms of operations done, not in terms of O notation itself). Just suppose that they are all negative, and find first positive if it exists, to break from the loop. No need to store current maximum, and swap when you find bigger one.

0

Reply
P
PrincipalCoralOctopus997
Top 5%
• 1 year ago

wheres time and space complexity analysis?

8

Reply
O
oussama.023
• 1 year ago

brute force is O(N^3), this is O(N^2), with space complexity O(1).

1

Reply
G
GloriousLavenderLark534
• 1 year ago

For space complexity analysis following the derivation in the provided link (EDIT: added link mentioned after comment the included it went away), we can consider triplets of the form (-x, 0, x) and input as [-3, -2, -1, 0, 1, 2, 3] where (n = 7). Each of said triplets is unique, and can be identified by selecting its left most element. We observe there are up to n/2 of these distinct left-most elements (in the left half of the sorted input, growing linearly with input, i.e., O(n)). We can then further set the remaining two elements to sum to x, of which we again have up to n/2 distinct pairs (in the right half of the sorted input, growing linearly with input, i.e., O(n)) as "x" is just negating every "-x" (in the triplet). So O(n) selections of the left most triplet element are matched with O(n) selections of the remaining 2 triplet elements, leading to O(n^2) unique triplets in the worst case. For the visually inclined, we can expand the example twice (from x to x+2, to x+4) and chart the resulting growth of triplet count - specified explicitly below.

Unique Triplets Found in the original example input:
(-3, 0, 3)
(-3, 1, 2)
(-2, -1, 3)
(-2, 0, 2)
(-1, 0, 1)
Total Triplets = 5 for n = 7

We now increase n to 11:
[-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]  (n = 11)
Unique Triplets Found
(-5, 0, 5)
(-5, 1, 4)
(-5, 2, 3)
(-4, -1, 5)
(-4, 0, 4)
(-4, 1, 3)
(-3, -2, 5)
(-3, -1, 4)
(-3, 0, 3)
(-3, 1, 2)
(-2, -1, 3)
(-2, 0, 2)
(-1, 0, 1)
Total Triplets = 13 for n = 11

Now, we increase n to 15:
[-7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7]  (n = 15)
Unique Triplets Found
(-7, 0, 7)
(-7, 1, 6)
(-7, 2, 5)
(-7, 3, 4)
(-6, -1, 7)
(-6, 0, 6)
(-6, 1, 5)
(-6, 2, 4)
(-5, -2, 7)
(-5, -1, 6)
(-5, 0, 5)
(-5, 1, 4)
(-5, 2, 3)
(-4, -3, 7)
(-4, -2, 6)
(-4, -1, 5)
(-4, 0, 4)
(-4, 1, 3)
(-3, -2, 5)
(-3, -1, 4)
(-3, 0, 3)
(-3, 1, 2)
(-2, -1, 3)
(-2, 0, 2)
(-1, 0, 1)
Total Triplets = 25 for n = 15

Array Size (n)  vs. Total Triplets Found
7  5
11  13
15  25

We can see that the number of triplets grows quadratically.

Show More

3

Reply
A
akashp1712
Premium
• 8 months ago

This is very good explanation of space complexity. Thanks a lot for saving time and mental space! :)

2

Reply
D
divyansh.dit
Premium
• 1 year ago

The second duplicate check for the right pointer seems redundant. If the first and second numbers (pointed by left ) are unique, the triplet is guaranteed to be unique.

2

Reply
Abhay Singh
Top 1%
• 1 year ago

Java Solution

class Solution {
    public List<List<Integer>> threeSum(int[] nums) {
        Arrays.sort(nums);

        int n = nums.length;
        int desiredSum = 0;

        List<List<Integer>> ans = new ArrayList<>();

        int i=0;
        while(i < n-2){
            int j=i+1, k=n-1;
            while(j < k){
                int sum = nums[i] + nums[j] + nums[k];
                if(sum < desiredSum){
                    j++;
                }else if(sum > desiredSum){
                    k--;
                }else{
                    ans.add(Arrays.asList(nums[i], nums[j], nums[k]));

                    j++;
                    k--;

                    while(j <= k && nums[j] == nums[j-1]) j++;
                    while(j <= k && nums[k] == nums[k+1]) k--;
                }
            }
            i++;

            while(i<n-2 && nums[i] == nums[i-1]) i++;
        }

        return ans;
    }
}
Show More

2

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Solution

Explanation

Avoiding Duplicates

Avoiding Duplicates II

Termination
