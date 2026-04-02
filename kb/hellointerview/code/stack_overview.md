# Stack Overview

> Source: https://www.hellointerview.com/learn/code/stack/overview
> Scraped: 2026-03-30


V
VerbalOliveChicken339
Premium
• 8 months ago

Hi there!

Thank you for all the content and good work!
I just wanted to report a small typo on this page, in the description of "Problem: Valid Parentheses". There is "ok lol" somewhere in the middle of the problem's description.

Cheers!

3

Reply
Reina Duplin
Premium
• 9 months ago

Noticing a possible issue with the problem description above. In the description the braces/curly-brackets are not showing up. I see:

-> consisting solely of the characters '(', ')', ', ', '[' and ']', determine whether s is a valid string.

but is should be:

-> consisting solely of the characters '(', ')', '{', '}', '[' and ']', determine whether s is a valid string.

I'm using Chrome Version 137.0.7151.104

I see the same issue on the page dedicated to the Valid Parentheses problem.

2

Reply
brad mitch
• 1 year ago

Java~

class Solution {
public boolean isValid(String s) {
Stack<Character> stck = new Stack<>();

	if(s.trim() == "" || s.length() == 1)
        return false;
	
	for (char c : s.toCharArray()) {
		if (c == '{' || c == '(' || c == '[') {
			stck.push(c);
		} else if (c == '}') {
			if (stck.isEmpty() || stck.pop() != '{')
				return false;
		} else if (c == ')') {
			if (stck.isEmpty() || stck.pop() != '(')
					return false;
		} else if (c == ']') {
			if (stck.isEmpty() || stck.pop() != '[')
						return false;
		} 
	}

	return (stck.size() == 0) ? true : false;
}


}

Show More

0

Reply
Alexander Gordon
• 1 year ago

If we use the monotonic decreasing stack, it will be 0(n^2)
Also, I think you only use regular stack in your solution, and it should work.

0

Reply
Jimmy Zhang
Top 5%
• 1 year ago

Hey Alexander, which problem are you referring to here?

1

Reply
Vivek Vitthalrao Patil
• 1 year ago

The left side panel on this page seems to be ordered wrong as compared to the main page where 'Two-Pointer Technique' is the first topic.

Also, the accordion item which is opened and in the URL is not closing. Ignore if that's intentional.

I think most people struggle with visualizing BFS-DFS and backtracking so we are eagerly waiting for that.

0

Reply
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Fundamentals

Using an Array as a Stack

Nested Sequences

Problem: Valid Parentheses

Practice Problems
