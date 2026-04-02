# Common Patterns

> Source: https://www.hellointerview.com/learn/system-design/in-a-hurry/patterns
> Scraped: 2026-03-30



​
Sort By
Popular
Sort By
M
matchaLatte
Top 1%
• 8 months ago

It would be interesting to add a (now) common pattern on designing production-ready Gen AI / LLM products (e.g. including online eval, offline eval, golden data sets, prompt engineering, RAG, 3rd party APIs, etc)

108

Reply
I
InitialSalmonPanther511
Premium
• 1 month ago

isnt this ml design interview in a hurry?

1

Reply
Pratik Agarwal
Top 10%
• 1 year ago

CQRS will be a great addition here!

22

Reply
Haris Osmanagić
Premium
• 5 months ago

It's certainly a great pattern, but it appears to have limited use-cases: https://martinfowler.com/bliki/CQRS.html.

2

Reply
C
ClearYellowScallop568
Premium
• 2 months ago

good call out! I've definitely seen patterns get unwound when the original implementer left the team / company, due to the pattern's lack of solving a practical problem and adding significant maintenance burden.

1

Reply
Tim
• 1 year ago

I introduced temporal to my company. it is very wonderful.

7

Reply

Evan King

Admin
• 1 year ago

Nice, we use it a lot here at Hello Interview and love it.

1

Reply
Vishal Wagh
Premium
• 2 months ago

@Evan King, can you pls share the use case here at HelloInterview? I would love to know more about it.

0

Reply

Stefan Mai

Admin
• 2 months ago

On the blog! #4

1

Reply
A
Abhi
Top 10%
• 9 months ago

Kafka gives you many of the same guarantees as SQS, but since the requests are written to an append-only log, you can replay the log to reprocess events if something goes wrong.

We should add that SQS can also replay failed messages from a dead letter queue (DLQ) by moving it back to the main queue via a Lambda for processing.

I think the difference of Kafka vs SQS really depends on the throughput and FIFO requirements instead of the cited ability to replay messages, for example, SQS can only support 300 messages/sec for a FIFO queue, whereas Kafka is much more scalable for high throughput message load.

6

Reply
Arunprasaath S
• 1 year ago

How about adding video upload/download & processing as a pattern. Services similar to dropbox, youtube, instagram all have this pattern.

For the Async job worker pool model you have added a data base is this used for managing the state of Job? or you have added it to store the output? . I feel having a database to manage the state of the job will be useful. This can help with Idempotencey, re-queuing  of job runs or with reporting.

5

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Pushing Realtime Updates

Managing Long-Running Tasks

Dealing with Contention

Scaling Reads

Scaling Writes

Handling Large Blobs

Multi-Step Processes

Proximity-Based Services

Pattern Selection

