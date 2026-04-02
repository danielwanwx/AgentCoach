# Container With Most Water

> Source: https://www.hellointerview.com/learn/code/two-pointers/container-with-most-water
> Scraped: 2026-03-30


Two Pointers
Container With Most Water
medium
DESCRIPTION (inspired by Leetcode.com)

Given an array heights where each element represents the height of a vertical line, pick two lines to form a container. Return the maximum area (amount of water) the container can hold.

What is area? Width × height, where width is the distance between walls, and height is the shorter wall (water overflows at the shorter wall).

Example 1:

max (21)
3
4
1
2
2
4
1
3
2
heights = [3, 4, 1, 2, 2, 4, 1, 3, 2]

Output:

21  # walls at indices 0 and 7 (both height 3): width=7, height=3, area=21

Example 2:

heights = [1, 2, 1]

Output:

2  # walls at indices 0 and 2: width=2, height=min(1,1)=1, area=2
CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def max_area(self, heights: List[int]) -> int:
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

8 chapters • 3 interactive checkpoints
Understanding the Problem
Picture vertical lines on a graph—each line's height comes from the array. You pick any two lines to act as the walls of a container (like a fish tank). The "area" is simply how much water this container can hold.
What is area? Just width × height:
Width: How far apart the two walls are (right_index - left_index)
Height: The shorter wall's height (min(heights[left], heights[right]))
Why the shorter wall? Imagine filling the container with water—it would overflow at the level of the shorter wall. If one wall is height 10 and the other is height 3, water only fills up to height 3 before spilling over.
Area formula: width × min(left_height, right_height)
Why Does Two-Pointer Work Here?
Two-pointers are generally perceived to work on sorted arrays and that's a common pattern, but not a strict rule. Two-pointer works whenever we can eliminate possibilities by moving pointers intelligently.
In this problem, the array isn't sorted—but we don't need it to be. We start with the widest possible container (pointers at both ends) and can eliminate suboptimal containers based on a simple observation: moving the taller wall inward can never help us because:
The width decreases
The height is still limited by the shorter wall
So we always move the pointer pointing to the shorter wall, hoping to find a taller one.
Solution
heights
​
|
heights
comma-separated integers
Try these examples:
Short
Wide Basin
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def max_area(heights):
    left, right = 0, len(heights) - 1
    current_max = 0
    
    while left < right:
        width = right - left
        height = min(heights[left], heights[right])
        current_area = width * height
        
        current_max = max(current_max, current_area)
        
        if heights[left] < heights[right]:
            left += 1
        else:
            right -= 1
    
    return current_max
3
4
1
2
2
4
1
3
2

container with most water

0 / 26

1x
Explanation
We can solve this in linear time because we systematically eliminate containers that can't possibly be better. Starting with pointers at opposite ends, the current container (outlined in blue) can hold 16 units of water.
The calculation: width is 8 - 0 = 8, height is min(3, 2) = 2 (limited by the shorter wall on the right), so area is 8 × 2 = 16.
3
4
1
2
2
4
1
3
2
left
right
But, which pointer should we move?
The right wall (height 2) is shorter than the left wall (height 3). If we move the left pointer inward, we'd get a narrower container but the height would still be capped at 2 (by the right wall). That can only make things worse or equal—never better.
So we should move the shorter wall's pointer (right), hoping to find a taller wall that could increase our area.
What if both walls are the same height? Then it doesn't matter which one you move — both are equally "the shorter wall." Neither side can produce a better container with the other wall held fixed, because the width would shrink while the height stays the same (or drops). So moving either pointer is safe. In our code, the else branch handles this by moving the right pointer, but moving the left would work just as well.
Let's verify this intuition. Here are all containers ending at the right pointer (current container = 16):
3
4
1
2
2
4
1
3
2
right
And the areas of all other containers starting at the left pointer:
3
4
1
2
2
4
1
3
2
left
Notice that every container ending at the right pointer (with smaller width) holds ≤16 units of water. This confirms our intuition: keeping the shorter wall and narrowing the container can't help. So we move the right pointer inward, eliminating all these suboptimal containers in one step.
3
4
1
2
2
4
1
3
2
left
right
This gives us a new container with a area of 21, which becomes the new maximum.

Mark as read

Next: Two Sum (Sorted Array)

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

(73)

Comment
Anonymous
​
Sort By
Popular
Sort By
L
LengthyGrayNightingale776
Top 5%
• 1 year ago

I think one of the thing that is very important for any 2 pointer question is how to decide which pointer (left or right) will move. In this, although example helps shows that but sometime it is very difficult to visualize such things.

In this problem, the way I think why the small height pointer should be the one to move is: With small height pointer, we already got the max area we could achieve as any wall we may we use with that, it would always be less than that as height would never be more than small height.

78

Reply
Luis Uceta
• 1 year ago

That's right. The small height of a bar is the bottleneck for any rectangle's height, thus we want to maximize the height. When faced with a small height and a big height, we discard the small height with the hope we can find a bigger height.

5

Reply
Prashant Gupta
Premium
• 9 months ago

When faced with a small height and a big height, we discard the small height with the hope we can find a bigger height.
Good explanation. But I am still not able to reconcile (intuition) since we are not taking distance into account into moving the pointer.

Shorter height * greater distance (between them) could be more than taller * shorter distance.

But I can see that the given algorithm works!

2

Reply
Luis Uceta
• 9 months ago

But I am still not able to reconcile (intuition) since we are not taking distance into account into moving the pointer.

Whether you discard the small height or choose it, it will be the same distance. Thus the only decision you can make is based on the height, not the width.

Shorter height * greater distance (between them) could be more than taller * shorter distance.

How would you devise the algorithm based on width (distance)? With height, you can say "I want to maximize the height and I move the pointers accordingly". However with width, how do you decide what pointer to move?

For example:

[3,4,1,2,2,4,1,3,2]
  l                        r

Both l and r determine the width but there's not something like a goal G, for example, where we can say we move l right because its distance to G is less than r distance to G?

Show More

2

Reply
Srivatsan Venkatesan
Top 5%
• 9 months ago

I think the idea is, no matter which pointer you move (left pointer to the right or right pointer to the left) You are decreasing the distance. You already start off with the max distance between points possible. So then your only hope is to optimize on height.

42

Reply
Alexander Pugachev
Top 10%
• 8 months ago

It's impossible to understand what is the task given the description as it is today. I had to follow to leetcode and their illustration and description finally made sense. Please improve the description.

31

Reply
Azat Nurzhanuly
Premium
• 7 months ago

agree! I've done the same, and also looked at the discussions.

1

Reply
Mark Mullins
Premium
• 4 months ago

Agreed, thought I was going crazy until I went to leetcode

0

Reply

Stefan Mai

Admin
• 4 months ago

Oof, I had updated the description with visuals since this comment. Still not clear?

1

Reply
C
chris.d.hanson
Premium
• 3 months ago

From the statement of the problem, and without looking at leetcode, it sounded like I needed to calculate the volume between the two heights taking into account what was between them, i.e. the walls take up space.

1

Reply
Joshua Lin
• 1 day ago

I think it would be good to have an example where you are calculating the area of two different heights.

0

Reply
shubham kukreja
Top 10%
• 1 year ago

very minor optimization can be

if height[left] == height[right]:
    left += 1
    right -= 1

17

Reply
A
austinkassman
Premium
• 5 months ago

not necessary. code should be as simple as possible and no simpler. the path is already covered without the explicit coverage.

2

Reply
P
ProudAmethystKiwi382
Premium
• 1 year ago

This looks good, but at the cost of an additional branching statement.

1

Reply
I
InnocentLavenderCamel378
Premium
• 2 months ago

Besides the cost of branching, I can't wrap my head around which one to move when they are equal easily. So I like this branch because of that.

0

Reply
Abhay Singh
Top 1%
• 1 year ago

Java Solution

class Solution {
    public int maxArea(int[] height) {
        int n = height.length;
        int i=0, j=n-1;

        int ans = 0;
        while(i<j){
            int h = Math.min(height[i], height[j]);
            int w = j-i;
            ans = Math.max(h*w, ans);

            if(height[i] < height[j]){
                i++;
            }else{
                j--;
            }
        }

        return ans;
    }
}
Show More

3

Reply
Kwizera Jean Luc
• 27 days ago

Very helpful material, alot of thanks to the hello interview team,concepts a re getting clearer for me. God bless you guys

2

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Understanding the Problem

Why Does Two-Pointer Work Here?

Solution

Explanation
