# Daily Temperatures

> Source: https://www.hellointerview.com/learn/code/stack/daily-temperatures
> Scraped: 2026-03-30


Stack
Daily Temperatures
medium
DESCRIPTION (inspired by Leetcode.com)

Given an integer array temps representing daily temperatures, write a function to calculate the number of days one has to wait for a warmer temperature after each given day. The function should return an array answer where answer[i] represents the wait time for a warmer day after the ith day. If no warmer day is expected in the future, set answer[i] to 0.

Inputs:

temps = [65, 70, 68, 60, 55, 75, 80, 74]

Output:

[1,4,3,2,1,1,0,0]
CODE EDITOR
Python
​
Full Screen
1
2
3
4
class Solution:
    def dailyTemperatures(self, temps: List[int]) -> List[int]:
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
This question uses a monotonically decreasing stack to find the next greatest temperature for each day in O(n) time, compared to the O(n2) time of the brute-force approach.
A monotonically decreasing stack stores indices, where the temperature values at those indices decrease from bottom to top of the stack. When pushing an index onto this stack, the temperature at that index must be smaller than the temperatures at all other indices currently on the stack.
73
72
72
68
stack
A montonically decreasing stack
First, we initialize our stack and our results array. Our stack holds indices of the temperatures in the input array that are waiting for a higher temperature, and our results array holds the number of days we have to wait after the ith day to get a warmer temperature.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def dailyTemperatures(temps):
  n = len(temps)
  result = [0] * n
  stack = []

  for i in range(n):
    while stack and temps[i] > temps[stack[-1]]:
      idx = stack.pop()
      result[idx] = i - idx
    stack.append(i)

  return result
73
74
75
71
69
72
76
73
0
1
2
3
4
5
6
7

daily temperatures

0 / 1

1x
Next, we iterate over each index in the array. For each index, we get the current temperature of that index, and compare it to the temperature of the top index in the stack.
Pushing To The Stack
If the current temperature is less than the top temperature in the stack (or if the stack is empty), we push the current index onto the stack to indicate that we are waiting to find a greater temperature for that index.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def dailyTemperatures(temps):
  n = len(temps)
  result = [0] * n
  stack = []

  for i in range(n):
    while stack and temps[i] > temps[stack[-1]]:
      idx = stack.pop()
      result[idx] = i - idx
    stack.append(i)

  return result
73
74
75
71
69
72
76
73
0
1
2
3
4
5
6
7
0
0
0
0
0
0
0
0
0
1
2
3
4
5
6
7
stack

initialize variables

0 / 2

1x
Pushing index 0 to the stack
Popping From The Stack
When the current temperature is greater than the top temperature in the stack, we have found the next highest temperature for not only the top index in the stack, but potentially other indices in the stack as well, which we can efficiently process due to the monotonically decreasing stack.
We first pop the top index from the stack and calculate the number of days we had to wait for that popped index to find a warmer temperature (current index minus the popped index), and store that number in the results array at the index of the popped element. To account for the fact that the current temperature might be the next greatest temperature for multiple indicies, we repeat this process in a while loop until the current temperature is less than the top temperature in the stack, or until the stack is empty.
After that is done, we push the current index onto the stack to indicate that we have not yet found the next greatest temperature for the current index.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def dailyTemperatures(temps):
  n = len(temps)
  result = [0] * n
  stack = []

  for i in range(n):
    while stack and temps[i] > temps[stack[-1]]:
      idx = stack.pop()
      result[idx] = i - idx
    stack.append(i)

  return result
73
74
75
71
69
72
76
73
0
1
2
3
4
5
6
7
i
0
0
0
0
0
0
0
0
0
1
2
3
4
5
6
7
0
stack

i = 1

0 / 2

1x
Popping index 0 from the stack
VISUALIZATION
Hide Code
Python
Language
Full Screen
def dailyTemperatures(temps):
  n = len(temps)
  result = [0] * n
  stack = []

  for i in range(n):
    while stack and temps[i] > temps[stack[-1]]:
      idx = stack.pop()
      result[idx] = i - idx
    stack.append(i)

  return result
73
74
75
71
69
72
76
73
0
1
2
3
4
5
6
7
i
1
1
0
0
0
0
0
0
0
1
2
3
4
5
6
7
2
3
stack

push to stack

0 / 9

1x
Popping multiple indexes from the stack. 75 is a higher temperature for 55, 60, 68 and 70.
This continues until we have iterated over the entire input array. At the end, we return the results array.
Efficency of the Monotonically Decreasing Stack
This is more efficient than the brute-force approach because it reduces the number of comparisons we have to make. For example, consider the state of the stack when we are at the 3rd index in the input array.
VISUALIZATION
Hide Code
Python
Language
Full Screen
def dailyTemperatures(temps):
  n = len(temps)
  result = [0] * n
  stack = []

  for i in range(n):
    while stack and temps[i] > temps[stack[-1]]:
      idx = stack.pop()
      result[idx] = i - idx
    stack.append(i)

  return result
73
74
75
71
69
72
76
73
0
1
2
3
4
5
6
7
i
1
1
0
0
0
0
0
0
0
1
2
3
4
5
6
7
stack

result[1] = 2 - 1

0 / 1

1x
Because the stack is monotonically decreasing, we only have to compare the temperature at i (60) to the temperature of the index at the top of the stack (68), to know that it cannot be a higher temperature for the other remaining items on the stack (70), which avoids a comparision between 60 and 70. But in the brute-force approach, 60 and 70 are compared when finding the next greatest temperature after 70.
Solution
temperatures
​
|
temperatures
comma-separated integers
Try these examples:
Decreasing
Small Zigzag
Reset
VISUALIZATION
Hide Code
Python
Language
Full Screen
def dailyTemperatures(temps):
  n = len(temps)
  result = [0] * n
  stack = []

  for i in range(n):
    while stack and temps[i] > temps[stack[-1]]:
      idx = stack.pop()
      result[idx] = i - idx
    stack.append(i)

  return result
73
74
75
71
69
72
76
73
0
1
2
3
4
5
6
7

daily temperatures

0 / 30

1x
What is the time complexity of this solution?
1

O(n)

2

O(n log n)

3

O(n * logn)

4

O(m * n * 4^L)

Mark as read

Next: Largest Rectangle in Histogram

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
Lisul Elvitigala
• 2 months ago

Result variable is hidden for playback of solution.

4

Reply
vaibhav aggarwal
Premium
• 1 month ago

We will fix

0

Reply
M
MeltedAmberPiranha299
Top 10%
• 4 months ago

"Because the stack is monotonically decreasing, we only have to compare the temperature at i (60) to the temperature of the index at the top of the stack (68), to know that it cannot be a higher temperature for the other remaining items on the stack (70), which avoids a comparision between 60 and 70. But in the brute-force approach, 60 and 70 are compared when finding the next greatest temperature after 70."

The written explanation has different numbers than the visual. (see first sentence, specifically, "at i (60)", when the visual example has i at 75.

4

Reply
Abhay Singh
Top 1%
• 1 year ago

Java Solution:

class Solution {
    public int[] dailyTemperatures(int[] temp) {
        int n = temp.length;
        int[] nearestGreaterRight = new int[n];

        Stack<Pair<Integer, Integer>> st = new Stack<>();
        for(int i=n-1;i>=0;i--){
            while(!st.isEmpty() && st.peek().getValue() <= temp[i]){
                st.pop();
            }

            nearestGreaterRight[i] = st.isEmpty() ? 0:st.peek().getKey()-i;
            st.add(new Pair(i, temp[i])); 
        }

        return nearestGreaterRight;
    }
}
Show More

3

Reply
Lisul Elvitigala
• 2 months ago

indicies

Typo in section "Popping From the Stack"

1

Reply
vaibhav aggarwal
Premium
• 1 month ago
• edited 1 month ago
public class Solution {
    public int[] dailyTemperatures(int[] temps) {
        // Your code goes here

        Stack<Integer> st = new Stack<>();
        int [] n = new int[temps.length];

        for(int i=0; i<temps.length; i++) {

            while(!st.isEmpty() && temps[st.peek()] < temps[i]) {
                    n[st.peek()] = i - st.peek();
                    st.pop();     
            }

            st.push(i);

        
        }

        return n;
    }
}
Show More

0

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

Pushing to the Stack

Popping from the Stack

Solution
