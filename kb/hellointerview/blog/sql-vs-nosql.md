# SQL vs NoSQL: How to Answer This Interview Question in 2025

> Source: https://www.hellointerview.com/blog/sql-vs-nosql
> Scraped: 2026-03-30


rocky panchal
• 8 months ago

so here we say " is scale really a concern"- what is that scale for reads and writes where it make sense for NOSQL just for scale

and also if scale is concern why not use sharded SQL??

8

Reply
Eric Li
Premium
• 5 months ago

also if scale is concern why not use sharded SQL??

I think this is just not a binary decision of use vs not use (same for other similar questions). You could certainly use sharded SQL but it comes with significant larger operational and architectural complexity that are simply abstracted away if you use NoSQL. If you still pick SQL to support massive scale there must be one or a set of concrete reasons for picking it over NoSQL that overweights the additional overhead and complexity inherently comes with SQL, and you should highlight that in your interview.

1

Reply
Hieronim Kubica
Premium
• 8 months ago

Good read, very well put together, cheers!

3

Reply
Alex Butera
Premium
• 7 months ago

"Maybe DynamoDB for specific high-volume write patterns"

Why? This isn't mentioned in the DynamoDB deep dive either.

2

Reply
Yash Garg
• 8 months ago

great article!!
what would that scale be""?

2

Reply
R
RoundBrownEgret745
Premium
• 8 months ago

Something that is overlooked for seniors and above is also the ability to factor in cost efficiency for your decision-making. It's not always about which technology X solves problem Y, but also Z, the ability to quantify costs for cloud provisioned hardware and services and how much cost savings you get from transitioning from one place to another.

1

Reply
Show All Comments
Reading Progress

On This Page

A Quick History Lesson (Because Context Matters)

Where We Are Today

What This Means for Your Interview

Be Wary of the False Dichotomy

The Bottom Line

Recent Posts

Kafka vs RabbitMQ: How to know which one to use

Mar 23, 2026

LinkedIn's AI-Enabled Coding Interview: How to Prepare

Feb 20, 2026

Shopify's AI Coding Interview: How to Prepare

Feb 20, 2026

Meta's AI-Enabled Coding Interview: How to Prepare

Feb 17, 2026

How to Prepare for a Low-Level Design Interview

Jan 14, 2026

