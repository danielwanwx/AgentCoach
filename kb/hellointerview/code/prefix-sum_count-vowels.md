# Count Vowels in Substrings

> Source: https://www.hellointerview.com/learn/code/prefix-sum/count-vowels
> Scraped: 2026-03-30



​
Sort By
Popular
Sort By
F
FancyCopperHamster950
• 11 months ago

https://leetcode.com/problems/count-vowel-strings-in-ranges

14

Reply
A
AddedLimeCarp593
Top 1%
• 9 months ago

This problem is a bit different.

1

Reply
Atif Mansoor
Premium
• 9 months ago

true, but the solution differs only by 1 line. So you can just copy your solution over, modify that line, and increase your LC count if you're so inclined 😊

1

Reply
shantanu chauhan
Premium
• 10 months ago

Very helpful, I think they should also provide the LeetCode links to the questions.

1

Reply
M
MassiveYellowBlackbird284
• 3 months ago

public static int[] VowelStrings(string[] words, int[][] queries)
{
char[] vowels = ['a', 'e', 'i', 'o', 'u'];
var prefixSum = new int[words.Length + 1];

 for (int i = 0; i < words.Length; i++)
 {
     bool isVowel = vowels.Contains(words[i][0]) && vowels.Contains(words[i][^1]);
     prefixSum[i + 1] = prefixSum[i] + (isVowel ? 1 : 0);
 }

 var result = new int[queries.Length];

 for (int i = 0; i < queries.Length; i++)
 {
     int left = queries[i][0];
     int right = queries[i][1];
     int vowelCounts = prefixSum[right + 1] - prefixSum[left];
     result[i] = vowelCounts;
 }

 return result;


}

Show More

0

Reply
Tanya Sinha
Premium
• 10 months ago

Should support Java as a language for writing solutions

2

Reply
L
Luiz
Premium
• 6 months ago

Shouldn't the space complexity be only O(n) as the O(q) is used to store the actual result?

1

Reply
A
ashish
Premium
• 5 days ago
• edited 5 days ago

can be solved with a n sized prefix array as well, not necessarily, n+1


public class Solution {
    public int[] vowelStrings(String word, int[][] queries) {
        // Your code goes here
        if(word.length()==0||queries.length==0) {
            return new int[0];
        }
        Set<Character> vowels = new HashSet<>();
        vowels.add('a');
        vowels.add('e');
        vowels.add('i');
        vowels.add('o');
        vowels.add('u');        

        int[] vowelCount = new int[word.length()];
        if(vowels.contains(word.charAt(0))) {
            vowelCount[0] = 1;
        } else {
            vowelCount[0] = 0;
        }
        for(int i=1;i<vowelCount.length;i++) {
            if(vowels.contains(word.charAt(i))) {
                vowelCount[i] = vowelCount[i-1]+1;
            } else {
                vowelCount[i] = vowelCount[i-1];
            }
        }
        int[] ans = new int[queries.length];
        int counter = 0;
        for(int[] query:queries) {
            int i = query[0];
            int j = query[1];
            if(i == 0) {
                ans[counter++] = vowelCount[j];
            } else {
                ans[counter++] = vowelCount[j] - vowelCount[i - 1];
            }

        }
        return ans;
    }
}

Show More

0

Reply
Hippily Happyy
Premium
• 2 months ago

Why there is no support for Swift language in coder :( ?

0

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Explanation

