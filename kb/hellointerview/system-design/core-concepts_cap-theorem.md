# CAP Theorem

> Source: https://www.hellointerview.com/learn/system-design/core-concepts/cap-theorem
> Scraped: 2026-03-30



​
Sort By
Popular
Sort By
Hari Prasanna
Top 5%
• 7 months ago

The basic definition of partition tolerance could have been a little more detailed.
For those who've come to comments before searching about it.
Partition tolerance refers to the functioning of a cluster even if there is a "partition" (communication break) between two nodes (both nodes are up, but can't communicate).

61

Reply
vinay s
• 11 months ago

So I am trying to understand the difference in the way we understand consistency for "Event booking in ticketMaster" vs "2nd user getting matched in Tinder".

So this is my understanding for event booking in ticketMaster:
If a user is booking a ticket or booked a ticket , then 2nd user should not be able to book the same event. Specific event ticket being referred to as resource and we should ensure that it modified by only one person and that modification should be applicable for all users after that.

When it comes to Tinder Matching, I feel its a bit different. I mean its a mutual sharing of data between 2 users via tinder platform. I am unable to see this through the eyes of "consistency" because if 2nd user swipes right and he/she unable to see that its exact match but later get a notification or chats section in both users are enabled to show user match, it is still okay..

So can anyone help me understand the "consistency" concept incase of Tinder matching!

I feel tinder matching example for consistency is a bit ambiguous or forced..

15

Reply
C
CooperativeRedAntelope278
Top 5%
• 8 months ago

You are right, tinder matching is forced just for the sake of an example. Remember, we aren't designing real world systems here. We're just doing an interview. An interviewer might throw a wrench in your design just to see if you know what to do.

In the real world, tinder does not have strong consistency for matching, it's eventually consistent.

5

Reply
A
AvailableJadeCattle348
Top 5%
• 8 months ago

I get that perspective but at the same time, couldn't it be argued that a better example should be there then? There's a lot of applications that he could talk about instead of potentially stretching it to make it about Tinder.

2

Reply
S
schebruch
Premium
• 6 months ago

I think it's that if user A swipes right, but user B swipes right before the right swipe was updated for user A, then user B's client might think that user A swiped left and not match. This is not a good customer experience.

1

Reply
Harshil Raval
• 8 months ago

Agree with this. In other words - if interviewer dictates non functional requirement that "matching requires to be shown immediately" then it's a clue for consistency.

1

Reply
F
FashionableAzureAlpaca705
• 1 year ago

You mention "If you prioritize consistency, your design might include: Single-Node Solutions." Doesn't that take away from the partition tolerance part of CAP since if we are using a single node then our system is not partitioned/distributed?

10

Reply
NDS
• 11 months ago

I believe by partition he referred to servers. and by single node he referred to the database.

4

Reply
A
AbstractAmberGopher993
Premium
• 9 months ago

Can you add some details about PACELC

7

Reply
R
rebornzrd
Premium
• 1 year ago

In the above example of UserA and UserB, how would Europe Server knows that the replication functionality is down so that it might serve stale data? Let's say both USA Serve and Europe Server use DynamoDB for data storage and data replication, would DynamoDB takes care of the "replication down" notification to both server?

5

Reply

Evan King

Admin
• 1 year ago

Servers detect replication failures through heartbeats, timeout mechanisms, and monitoring replication lag metrics. During network partitions, regional servers continue operating independently with their local data, choosing to serve potentially stale information rather than errors. In DDBs case, yes, it handles this.

25

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

What is CAP Theorem?

Understanding CAP Theorem Through an Example

When to Choose Consistency

When to Choose Availability

CAP Theorem in System Design Interviews

Advanced CAP Theorem Considerations

Different Levels of Consistency

Conclusion

