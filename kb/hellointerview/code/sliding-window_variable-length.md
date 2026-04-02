# Variable Length Sliding Window

> Source: https://www.hellointerview.com/learn/code/sliding-window/variable-length
> Scraped: 2026-03-30

Variable Length Sliding Window
This technique refers to creating a window that "slides" through an input sequence (typically an array or string).
3
3
2
1
2
1
0
variable-length sliding window
Sliding windows can be either variable or fixed length. On this page, we'll cover variable-length sliding windows by looking at:
An example problem that illustrates the motivation for each type of sliding window, as well as how to implement it.
The types of problems for which each type of sliding window is useful, as well as templates you can use as a starting point.
A list of practice problems (with animated solutions and explanations!) for you to try to build upon the concepts covered here.
Problem: Fruit Into Baskets
DESCRIPTION (inspired by Leetcode.com)
Write a function to calculate the maximum number of fruits you can collect from an integer array fruits, where each element represents a type of fruit. You can start collecting fruits from any position in the array, but you must stop once you encounter a third distinct type of fruit. The goal is to find the longest subarray where at most two different types of fruits are collected.
Example:
Input: fruits = [3, 3, 2, 1, 2, 1, 0]
Output: 4
Explanation: We can pick up 4 fruit from the subarray [2, 1, 2, 1]
We'll walkthrough how to use the sliding window to solve this problem when fruits = [3, 3, 2, 1, 2, 1, 0].
3
3
2
1
2
1
0
The answer for the given input array is 4.
Naive Approach
To understand the motivation behind the sliding window pattern, let's start by looking at a naive approach to this problem, which considers every possible subarray in the input, and chooses the longest one with at most 2 distinct fruits.
SOLUTION
Python
Language
def fruit_into_baskets(fruits):

    max_length = 0

    # i and j are the start and end indices of the subarray
    for i in range(len(fruits)):
        for j in range(i, len(fruits)):
            if len(set(fruits[i:j + 1])) <= 2:
                max_length = max(max_length, j - i + 1)
            else:
                # the subarray starting at i is invalid
                # so we break and move to the next one
                break
    
    return max_length
This approach considers O(n2) subarrays. For each subarray, it checks if it contains at most 2 distinct fruits by converting it to a set and checking its length, which takes O(n) time, for a total a time complexity of O(n3). We'll gradually improve this approach until we reach the sliding window pattern, which solves this problem in O(n) time.
Improvement 1: Build Incrementally
The first improvement is to use a variable to store the contents of the current subarray. We'll use a dictionary state that maps each fruit in the current subarray to the number of times it appears.
This choice of state is key as it allows us to:
Build the contents of the subarray incrementally. Each time we expand the subarray to include a new fruit, we'll increment the count of that fruit in state, which reuses work from the previous subarray.
Check if the subarray is valid by checking if state has 2 keys or less.
Since both of these operations take O(1) time, we can now check if a new subarray is valid in O(1) time. This brings the total time complexity of the solution down to O(n2).
SOLUTION
Python
Language
def fruit_into_baskets(fruits):

    max_length = 0

    # i and j are the start and end indices of the subarray
    for i in range(len(fruits)):
        state = {}
        for j in range(i, len(fruits)):
            state[fruits[j]] = state.get(fruits[j], 0) + 1
            if len(state) <= 2:
                max_length = max(max_length, j - i + 1)
            else:
                # the subarray starting at i is invalid
                # so we break and move to the next one
                break
    
    return max_length
Improvement 2: Don't Blow It All Up!
In the above approach, we reset state each time we reach an invalid subarray and break from the inner loop. When the outer loop increments i, we end up rebuilding parts of the same subarray from the previous iteration, which we can see by visualizing the first few steps of the algorithm:
1
1
2
3
2
3
4
1
1
2
3
2
3
4
1
1
2
3
2
3
4
1
1
2
3
2
3
4
1
1
2
3
2
3
4
1
1
2
3
2
3
4
1
1
2
3
2
3
4
1
1
2
3
2
3
4
1
1
2
3
2
3
4
After incrementing i, we end up rebuilding the same subarrays ([1], [1, 2], [1, 2, 3]) from the previous iteration.
Rather than resetting the contents of state each time we reach an invalid subarray, we can instead think about removing fruits from the start of the subarray until it is valid again. This allows us to move onto the next valid subarray while also preserving work we've already done - which brings us to the sliding window pattern.
The Sliding Window
We now have enough context to understand the motivation behind the sliding window pattern. The "window" in the sliding window refers to a subarray we are considering to contain the maximum number of fruits we can collect.
Initialization
We use two pointers, start and end, to represent the start and end indices of the window. The window is initially empty, and so is the dictionary state that represents the contents of the window. We also initialize a variable max_fruit that represents the maximum amount of fruit we can collect.
VISUALIZATION
Full Screen
3
3
2
1
2
1
0

fruit into baskets

0 / 1

1x
Iteration
Next we repeatedly extend the current window incrementing end. Each time we do so, we add the fruit at end to state by incrementing its count in the dictionary, and then we compare the length of the window to the current value of max_fruit, and update it if its greater.
VISUALIZATION
Full Screen
{}
state
3
3
2
1
2
1
0
0
max_fruit

start: 0 | end: -

initialize variables

0 / 6

1x
Contracting the Window
Eventually, we reach a window that is invalid because it contains 3 distinct fruits. Here, we contract the window by decrementing the count of the fruit at start in state, and then incrementing start to contract the window. We contract the window until it is valid again.
VISUALIZATION
Full Screen
{3:2, 2:1}
state
3
3
2
1
2
1
0
3
max_fruit

start: 0 | end: 2

update max_fruit

0 / 3

1x
At this point, our window is ready to expand again, so we continue iterating until we reach the end of the array, at which point we return max_fruit.
VISUALIZATION
Full Screen
{2:1, 1:1}
state
3
3
2
1
2
1
0
3
max_fruit

start: 2 | end: 3

contract window

0 / 11

1x
Solution
Here's what the final solution looks like:
fruits
​
|
fruits
comma-separated integers
Try these examples:
Two Types
Switching
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def fruit_into_baskets(fruits):
  start = 0
  state = {}
  max_fruit = 0

  for end in range(len(fruits)):
    state[fruits[end]] = state.get(fruits[end], 0) + 1

    while len(state) > 2:
      state[fruits[start]] -= 1
      if state[fruits[start]] == 0:
        del state[fruits[start]]
      start += 1

    max_fruit = max(max_fruit, end - start + 1)

  return max_fruit
3
3
2
1
2
1
0

fruit into baskets

0 / 21

1x
The length of the window at any time is end - start + 1.
When we decrement the count of a fruit in state as part of contracting the window, we need to delete the fruit from state if its count is 0. This is because we rely on the number of keys in state to check if the window is valid.
Complexity
The time complexity of this algorithm is O(n), where n is the length of the input array. end iterates through the array once, and start iterates through the array at most once. Each time either moves, we arrive at a new window, which requires O(1) time to check if its valid.
The space complexity of this algorithm is O(1), since state never contains more than 3 keys.
Template
Here's a template you can use as a starting point for solving problems with a variable-length sliding window.
SOLUTION
Python
Language
def variable_length_sliding_window(nums):
  state = # choose appropriate data structure
  start = 0
  max_ = 0

  for end in range(len(nums)):
    # extend window
    # add nums[end] to state in O(1) in time

    while state is not valid:
      # repeatedly contract window until it is valid again
      # remove nums[start] from state in O(1) in time
      start += 1

    # INVARIANT: state of current window is valid here.
    max_ = max(max_, end - start + 1)

  return max_
When Do I Use This?
Consider using the sliding window pattern for questions that involve searching for a continuous subarray/substring in an array or string that satisfies a certain constraint.
If you know the length of the subarray/substring you are looking for, use a fixed-length sliding window. Otherwise, use a variable-length sliding window.
Examples:
Finding the largest substring without repeating characters in a given string (variable-length).
Finding the largest substring containing a single character that can be made by replacing at most k characters in a given string (variable-length).
Finding the largest sum of a subarray of size k without duplicate elements in a given array (fixed-length).
Practice Problems
When practicing these problems, it is important to think about the appropriate data structure state to store the contents of the current window. Make sure it supports both:
Adding and removing elements from the window in O(1) time.
Checking if the window is valid in O(1) time.
Dictionaries and sets are often the best choices.
Done
	
Question
	
Difficulty


	
Longest Substring Without Repeating Characters
	
Medium


	
Longest Repeating Character Replacement
	
Medium

Mark as read

Next: Longest Substring Without Repeating Characters

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

(19)

Comment
Anonymous
​
Sort By
Popular
Sort By
Mickey Mouse
• 1 year ago

awesome content!!

15

Reply
MM
Minnie Mouse
Top 5%
• 5 months ago

I agree!

3

Reply
KC
Karapakkam coders
Premium
• 2 days ago

Agreed

1

Reply
Abhishek Sharma
• 1 year ago
public int totalFruit(int[] fruits) {
    int maxFruit = 0, start = 0, i = 0;
    Map state = new HashMap<String, String>();
    for (int end = 0; end < fruits.length; end++) {

        if (!state.containsKey(fruits[end])) {
            state.put(fruits[end], 1);
        } else {
            state.put(fruits[end], state.get(fruits[end] + 1));
        }
        if (state.size() > 2) {
            state = new HashMap();
            start = end - 1;
        }
        maxFruit = Math.max(maxFruit, end - start + 1);
    }
    return maxFruit;
}

2

Reply
Daniel Guo
Premium
• 2 months ago

The improvement process which leads to the sliding window option is awesome!

1

Reply
Mahesh Singh
Premium
• 10 days ago

public static void Main(string[] args)
{
int[] arr = new int[]{3,3,2,1,2,1,0};
Slide(arr);
}

public static void Slide(int[] arr)
{
    int start = 0, maxSum = 0;
    Dictionary<int,int> op = new Dictionary<int,int>();
    
    for(int end=0; end < arr.Length; end++)
    {
        if(op.ContainsKey(arr[end]))
        {
          op[arr[end]] = op[arr[end]] + 1;
        }
        else
        {
            op[arr[end]] = 1;
        }
        

        while(op.Count() > 2)
        {
          op[arr[start]] = op[arr[start]] - 1;
          
          if(op[arr[start]] == 0)
          {
              op.Remove(arr[start]);
          }
          start++;
        }
        
        maxSum = Math.Max(maxSum, end - start + 1);
    }
    
    Console.WriteLine (maxSum);
}

Show More

0

Reply
srot sinha
Premium
• 25 days ago
• edited 25 days ago
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Basket:

    def __post_init__(self):
        self._count: int = 0
        self._last_indices: dict[str, int] = {}

    def add_fruit(self, fruit: str, index: int) -> bool:
        if fruit not in self._last_indices and len(self._last_indices) == 2:
            return False
        self._count += 1
        self._last_indices[fruit] = index
        return True

    @property
    def count(self) -> int:
        return self._count

    def replace_basket_with_one_fruit(self) -> Basket:
        new_basket = Basket()
        fruit_to_keep = None
        for f, i in self._last_indices.items():
            if fruit_to_keep is None or i > self._last_indices[fruit_to_keep]: # keep the latest fruit
                fruit_to_keep = f
        
        if fruit_to_keep:
            new_basket._last_indices[f] = self._last_indices[f]

            fruit_to_remove = next(f for f in self._last_indices.keys() if f != fruit_to_keep)
            new_basket._count = self._last_indices[fruit_to_keep] - self._last_indices[fruit_to_remove]

        return new_basket

    def __lt__(self, other: Basket):
        return self.count < other.count

    def __gt__(self, other: Basket):
        return self.count > other.count

def fruit_into_baskets(fruits: list[str]):

    basket = Basket()
    largest_basket = Basket()

    for i, fruit in enumerate(fruits):
        if not basket.add_fruit(fruit, i):
            largest_basket = max(largest_basket, basket)
            basket = basket.replace_basket_with_one_fruit()
            basket.add_fruit(fruit, i)

    largest_basket = max(largest_basket, basket)

    return largest_basket.count

print(fruit_into_baskets(["A", "B", "C", "A", "C"]))
print(fruit_into_baskets(["B", "A", "B", "B", "C", "B", "B", "C"]))

Show More

0

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Problem: Fruit Into Baskets

Naive Approach

The Sliding Window

Solution

Complexity

Template

When Do I Use This?

Practice Problems