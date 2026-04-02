# Sort Colors

> Source: https://www.hellointerview.com/learn/code/two-pointers/sort-colors
> Scraped: 2026-03-30


Two Pointers
Sort Colors
medium
DESCRIPTION (inspired by Leetcode.com)

Write a function to sort a given integer array nums in-place (and without the built-in sort function), where the array contains n integers that are either 0, 1, and 2 and represent the colors red, white, and blue. Arrange the objects so that same-colored ones are adjacent, in the order of red, white, and blue (0, 1, 2).

Input:

nums = [2,1,2,0,1,0,1,0,1]

Output:

[0,0,0,1,1,1,1,2,2]
CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def sortColors(self, nums: List[int]) -> None:
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
We can understand this algorithm by looking at the invariants which hold true after each iteration:
All elements to the left of the left are 0s.
All elements between left and i - 1 are 1s.
All elements between i and right are unsorted.
All elements to the right of right are 2s.
0
0
1
1
0
1
2
0
2
2
2
Let's now see how we maintain these invariants as we iterate through the array.
Sorting 0s
When nums[i] is equal to 0, invariant 2 tells us there are two possible values for left: 0 or 1.
Let's consider the case when left == 1 first. We swap i with left. This allows us to increment the left pointer to maintain invariant 1. Since we know that the new item at i is a 1, we can also increment i to maintain variant 2.
0
0
1
1
0
1
2
0
2
2
2
i
left
right
zeroes
twos
unsorted
ones
Now let's consider what happens when left == 0, which happens when we haven't encountered any 1s yet and i == left. We swap i with left (which is itself) and increment left to maintain invariant 1. Since we still haven't encountered any 1s, we can increment i to maintain invariant 2. In other words, the "ones" region remains empty.
0
0
2
0
0
1
1
0
2
2
i
left
right
zeroes
twos
unsorted
Sorting 1s
When nums[i] == 1, we can simply increment i to maintain invariant 2.
0
0
0
1
1
1
2
0
2
2
2
i
left
right
zeroes
twos
unsorted
ones
Sorting 2s
When nums[i] == 2, we swap nums[i] with nums[right]. This allows us to decrement right to maintain invariant 4. But since the new item at i came from the unsorted region, the new item at i is still unsorted, so we have to go through another iteration to correctly sort it.
0
0
0
1
1
1
2
0
2
2
2
i
left
right
zeroes
twos
unsorted
ones
Termination
When i surpasses right the unsorted region is empty and the entire array is sorted.
0
0
0
1
1
1
0
2
2
2
2
i
left
right
zeroes
twos
unsorted
ones
Solution
nums
​
|
nums
comma-separated integers
Try these examples:
Short
Mixed
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def sortColors(nums):
  left, right = 0, len(nums) - 1
  i = 0

  while i <= right:
    if nums[i] == 0:
      nums[i], nums[left] = nums[left], nums[i]
      left += 1
      i += 1
    elif nums[i] == 2:
      nums[i], nums[right] = nums[right], nums[i]
      right -= 1
    else:
      i += 1

  return nums
2
1
2
0
1
0
1
0
1

sort colors

0 / 20

1x

Mark as read

Next: Trapping Rain Water

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

(59)

Comment
Anonymous
​
Sort By
Popular
Sort By
I
InterimWhiteOcelot253
Top 10%
• 1 year ago

Just one note:
In the explanation, it uses references such as 'When i == 2', when what it seems to mean is actually 'When nums[i] == 2', referring to the value rather than the index

23

Reply
G
gozeloglu
Premium
• 6 months ago

Yes, I didn't understand it until reading the code.

3

Reply
Abhineet Srivastava
• 1 year ago

should be a section for 3 pointer problems

17

Reply
Bhavik Shah
Premium
• 7 months ago

The question specifies that the possible values are only 0,1,2 - I just counted the occurrences of each and replaced the original array

public class Solution {
    public int[] sortColors(int[] nums) {
        // Your code goes here
        int[] count = new int[3];
        for(int i = 0; i < nums.length; i++) {
            count[nums[i]]++;
        }
        
        int color = 0;
        int i = 0;

        while(i < nums.length) {
            if(count[color] == 0) {
                color++;
                continue;
            }
            nums[i] = color;
            count[color]--;
            i++;

        }
        return nums;
    }
}
Show More

15

Reply
C
catspetsdogs
• 5 months ago

mee2

//O(n)
class Solution {
    sortColors(nums: number[]): number[] {

        let count0 = 0
        let count1 = 0
        let count2 = 0

        //count occurences:
        for (let i = 0; i < nums.length; i++) {
            if (nums[i] === 0) count0++
            else if (nums[i] === 1) count1++
            else if (nums[i] === 2) count2++
        }

        for (let i = 0; i < nums.length; i++) {
            if (count0 > 0) {
                nums[i] = 0
                count0--
            } else if (count1 > 0) {
                nums[i] = 1
                count1--
            } else if (count2 > 0) {
                nums[i] = 2
                count2--
            }
        }

        return nums
    }
}
Show More

2

Reply
E
elapidae
Premium
• 4 days ago

I've failed interview because of this approach as "it is using additional space, not sorting in place", which is little bit weird since this is O(1) space usage.

0

Reply
Hüseyin Merkit
• 25 days ago

yes, this is much easier. but this is an unstable sort

0

Reply
B
Binary.Beast
Premium
• 16 days ago

Even provided solution is not stable sort. I dont think that is an ask here.

0

Reply
C
ConstantCyanLemur986
Premium
• 8 months ago

This problem is also called as Dutch National Flag problem

10

Reply
Abhay Singh
Top 1%
• 1 year ago

Java Solution

class Solution {

    public void swap(int[] nums, int i, int j){
        int temp = nums[i];
        nums[i] = nums[j];
        nums[j] = temp;
    }

    public void sortColors(int[] nums) {
        int n = nums.length;

        // [0, i]: 0s, [i+1, k-1]: undeifned, [k, n-1]: 2s
        int i=-1, j=0, k=n;
        while(j<k){
            if(i<j && nums[j] == 0){
                i++;
                swap(nums, i, j);
            }else if(nums[j] == 2){
                k--;
                swap(nums, j, k);
            }else{
                j++;
            }
        }
    }
}
Show More

6

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

Sorting 0s

Sorting 1s

Sorting 2s

Termination

Solution
