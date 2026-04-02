# Move Zeroes

> Source: https://www.hellointerview.com/learn/code/two-pointers/move-zeroes
> Scraped: 2026-03-30


Two Pointers
Move Zeroes
easy
DESCRIPTION (inspired by Leetcode.com)

Given an integer array nums, write a function to rearrange the array by moving all zeros to the end while keeping the order of non-zero elements unchanged. Perform this operation in-place without creating a copy of the array.

Input:

nums = [2,0,4,0,9]

Output:

[2,4,9,0,0]
CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
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
We can solve this problem by keeping a pointer i that iterates through the array and another pointer nextNonZero that points to the position where the next non-zero element should be placed. We can then swap the elements at i and nextNonZero if the element at i is non-zero. This way, we can maintain the relative order of the non-zero elements while moving all the zeroes to the end of the array.
Solution
nums
​
|
nums
comma-separated integers
Try these examples:
All Zeros
Mixed
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def moveZeroes(nums):
    nextNonZero = 0
    for i in range(len(nums)):
        if nums[i] != 0:
            nums[nextNonZero], nums[i] = nums[i], nums[nextNonZero]
            nextNonZero += 1
2
0
4
0
9

move zeros

0 / 13

1x

Mark as read

Next: Sort Colors

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

(58)

Comment
Anonymous
​
Sort By
Popular
Sort By
S
ShinyTealVulture423
Top 5%
• 1 year ago

The name "nextNonZero" seems strange to me, as this pointer always indicates the next zero entry, while i marches onward to look for nonzero entries.

In other words, the pattern taught here is, "one pointer iterates unconditionally, while a second pointer lags behind conditionally."

68

Reply
R
ruslan.zinovyev
Premium
• 15 days ago

Same confusion here, it points to the next available slot where a non-zero element should be placed, probably insertPosition would be the better name.

1

Reply
P
PlannedMagentaTrout950
Premium
• 5 days ago

I call it "firstZero" since it's the location of the first zero we encounter in the array.

0

Reply
G
GenerousMaroonPony103
Top 10%
• 8 months ago

Isn't this a fast/slow pointers problem rather than a two-pointers problem?

27

Reply
Shivam Chauhan
• 8 months ago

Technically yes, you can consider this as a fast/slow pointers problem which is actually a subset of two-pointer pattern.

13

Reply
N
NarrowCoralStarfish749
• 9 months ago
class Solution:
    def moveZeroes(self, nums: list[int]):
        for i in range(len(nums)-1):
            if nums[i] != 0:
                continue
            left = i + 1
            while nums[left] == 0 and left < len(nums)-1:
                left += 1
            nums[i] = nums[left]
            nums[left] = 0
            
        return nums

4

Reply
E
ElegantAquaMouse760
• 1 month ago

I did that too. but it has O(N square) complexity because of the inner while loop. so not ideal compared to the actual solution.

0

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

    public void moveZeroes(int[] nums) {
        int n = nums.length;

        // [0,i] : region of non-zeroes, [i+1, n-1] : undefined
        int i=-1, j=0;
        while(j<n){
            if(i!=j && nums[j] != 0){
                i++;
                swap(nums, i, j);
            }else{
                j++;
            }
        }
    }
}
Show More

4

Reply
Hasnat Safder
• 2 months ago
• edited 2 months ago

No need to keep j++ in else, waste a loop

if(i!=j && nums[j] != 0){
   i++;
   swap(nums, i, j);
}
j++

One more thing, why not increment j in the if check.
It will have to come

0

Reply
G
GloriousLavenderLark534
• 1 year ago

This can be thought of as "compacting" the non-zero elements to the left, which can be done in 2 separate (but easy to understand) passes. In the first pass, whenever we encounter a non-zero element we copy it over to index nextNonZero (pointing to the immediately available index in the compacted, or result array), and increment that. Then, in a second pass we (read: pad the right part of the array with zeroes) overwrite elements from nextNonZero to the end of the array with zeroes. In Java:

public void moveZeroes(int[] nums) {
    // key here is that the order of all the non-zero elements
    // has meaning as we can distinguish between them. All zeroes
    // on the otherhand are indistinguishable from one another.
    // we can compact non-zeroes to the left and fill remainng 
    // elements with zeroes
    int rightmostNonZeroIndex = 0; 
    
    // move all non-zero elements left in order of occurrence 
    for (int i = 0; i < nums.length; i++) {
        if (nums[i] != 0) {
            nums[rightmostNonZeroIndex++] = nums[i];
        }
    }
    
    // fill remaining positions with zeros
    while (rightmostNonZeroIndex < nums.length) {
        nums[rightmostNonZeroIndex++] = 0;
    }
}
Show More

3

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

Solution
