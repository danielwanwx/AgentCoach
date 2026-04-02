# Managing Long Running Tasks

> Source: https://www.hellointerview.com/learn/system-design/patterns/long-running-tasks
> Scraped: 2026-03-30



​
Sort By
Popular
Sort By
H
HeadBrownGayal101
Top 5%
• 8 months ago

Can you please add a way for us to add notes and/or highlight the content?

47

Reply
C
ChristianPlumTakin500
Top 5%
• 8 months ago

@Evan King, Notes would be super helpful! These articles are great refreshers to go through before interviews, rather than going through a lot of questions. I'm making notes separately based on these articles, but would love to have

Notes per article
List of all my notes across the site
Notes not tied to any article

This would allow users to stay within your website. And you can further use AI to analyze these notes as feedback loop to improve the posts

Note
- note_id
- user_id
- post_id
- content_s3_url
- created_at
- updated_at
Show More

15

Reply

Evan King

Admin
• 8 months ago

Are you thinking Medium style or have something else in mind?

3

Reply
H
HeadBrownGayal101
Top 5%
• 8 months ago

Anything's fine as long as I have a way to keep notes so that I can come back to it and quickly revise before the interview.

20

Reply
F
FullTealTrout477
Top 10%
• 7 months ago

there are text highlighting chrome extensions

0

Reply
I
InvisiblePinkChipmunk238
Premium
• 8 months ago

@Evan Suggestion for highlight & notes: Highlight any sentences and as next step add comment - Google doc style would be awesome.

0

Reply
U
UnderlyingYellowCat786
Premium
• 2 months ago

Just use Notion??

What's the point of implementing Notion inside Hello Interview?

0

Reply
C
CooperativeRedAntelope278
Top 5%
• 8 months ago

Love the new patterns you've recently added. Thank you so much for all the hard work.

27

Reply

Evan King

Admin
• 8 months ago

Thrilled you like them! More on the way soon

35

Reply
C
CasualAquamarineRhinoceros625
Premium
• 8 months ago

Can't wait!

1

Reply
Ian Chen
Premium
• 5 months ago

In "Putting It Together", I feel we should use CDC with the outbox pattern to avoid crashes between "insert into the database" and "add a job to the queue".

5

Reply
S
StandardCopperLobster574
• 4 months ago

yes upvoting this

0

Reply
C
ClosedSapphireLeopon316
Premium
• 6 months ago

One interesting case is what happens if write to DB succeeds and then to queue fails. There are multiple ways to solve like using transactional outbox pattern or kafka streams etc.

5

Reply
mj r
Premium
• 4 months ago

Yes, the dual write problem is another good deep dive topic.

0

Reply
E
ExoticPeachBobolink928
Premium
• 8 months ago

Hi
In the "Putting It Together" section,  Would it be better to create the job queue on top of CDC from DB, rather than having server store the message into queue?
The idea is to have better fault tolerance.

If the DB crashes, WAL can be used to re-construct it, and message is pushed to queue regardless.
If the server crashes after writing to DB, but before writing to queue, we are left in an inconsistent state, where the operation is never processed, unless
2.1 user retries
2.2 or some scheduled job checks the DB

Maybe you can add a section about this under "handling failures"

5

Reply
Roman Kravtsov
Premium
• 2 months ago

Had same question.
AWS suggests indeed transactional outbox pattern:
https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html

Two approaches highlighted in the link above:

Polling in conjunction with relational db
Change data capture in conjunction with DynamoDB.

1

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

The Problem

The Solution

Trade-offs

What you gain

What you lose

How to Implement

Message Queue

Workers

Putting It Together

When to Use in Interviews

For Example

Common Deep Dives

Handling Failures

Handling Repeated Failures

Preventing Duplicate Work

Managing Queue Backpressure

Handling Mixed Workloads

Orchestrating Job Dependencies

Conclusion

