# Numbers to Know

> Source: https://www.hellointerview.com/learn/system-design/core-concepts/numbers-to-know
> Scraped: 2026-03-30



​
Sort By
Popular
Sort By
C
CuddlyCopperWildebeest704
Top 5%
• 1 year ago

Could you also add section for numbers to know for pub/sub (Redis pub/sub), AWS SQS, Flink?

85

Reply
Y
YabberingGreenCheetah563
Premium
• 6 months ago

+1 yes this is needed

7

Reply
E
ExtraAmaranthDuck389
Top 10%
• 10 months ago

@evan, could you please? Thank you!

5

Reply
Sanzhar Seidigapbar
Top 5%
• 6 months ago

Would be nice to have a date for this article to make sure those are still relevant numbers

53

Reply
O
OldG
Premium
• 4 months ago

Right. At some point the numbers will be obsolete. I think working with assumptions is a better approach in an interview instead of trying to keep up with constantly changing real world numbers. Cost is also a significant factor too. Those high-capacity machines don't come cheap.

6

Reply
VB
vishal bajoria
Top 5%
• 1 year ago

Thank you for this excellent article! I truly appreciate the effort in putting this together. I have a question regarding modern hardware capabilities and caching best practices. With modern RAM capacities reaching up to 24 TB, why is it recommended to limit Redis cache to 1 TB and shard when memory usage approaches 80% of this limit? Should we consider leveraging higher RAM capacities for Redis, or are there specific constraints that justify the 1 TB recommendation?

18

Reply

Evan King

Admin
• 1 year ago

No strict rule here, but large instances become harder to back up, replicate, or recover from failures

33

Reply

Stefan Mai

Admin
• 1 year ago

Also remember for Redis specifically that it's single-threaded! You'll probably be CPU-bound first. Other implementations can help with this (e.g. Dragonfly) but otherwise you'll need to shard anyways to increase CPU utilization.

38

Reply
VB
vishal bajoria
Top 5%
• 1 year ago

thank you. it makes sense.

2

Reply
A
aditya.bhardwaja
• 1 year ago

Excellent article! I can relate to this from my current work experience. About five years ago, we developed certain features to optimize caching under the assumption that our instances couldn't handle data > 200GB , spent lot of effort in eviction strategies and hot/cold reload. However, those features have become irrelevant due to modern hardware limits

16

Reply

Evan King

Admin
• 1 year ago

It's wild how quickly things change, right!

5

Reply
T
ThoughtfulPeachGull276
• 1 year ago

Regarding read throughput for in-memory caching, the 100k RPS for ElastiCache Redis on Graviton seems low. Doesn't ElastiCache for Redis enable something like a million RPS with 7.1?

Genuinely just trying to understand. AWS' post from 2023 states that "for example on r7g.4xlarge, you can achieve over 1 million requests per second (RPS) per node, and 500M RPS per cluster."

Is the 100k RPS posted here on a base Graviton node?

Links or references to sources for many of the numbers posted would really help in diving deeper into them/building a stronger mental model.

Thanks, guys! Love all the content!

9

Reply

Evan King

Admin
• 1 year ago

They can get up to 1M with the right conditions and small value sizes. I would not necessarily optimize for 1M in an interview, I'd stick in the 100k order of magnitude, but you're not wrong. Agree on references. Can try to bolster

6

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Modern Hardware Limits

Applying These Numbers in System Design Interviews

Caching

Databases

Application Servers

Message Queues

Cheat Sheet

Common Mistakes In Interviews

Premature sharding

Overestimating latency

Over-engineering given a high write throughput

What about costs?

Conclusion

