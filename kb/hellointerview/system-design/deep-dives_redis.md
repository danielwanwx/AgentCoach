# Redis

> Source: https://www.hellointerview.com/learn/system-design/deep-dives/redis
> Scraped: 2026-03-30



​
Sort By
Popular
Sort By
Muhammad Ahmad
Top 5%
• 1 year ago

Redis distributed lock (including the one from Redlock protocol) is not safe, because it is not fenced.

Consider this use case:

Client 1 acquires a TTL lock (SUCCESS)
Client 1 experiences a GC pause
TTL lock expires
Client 2 acquires a TTL lock (SUCCESS, because of step 3 above)
Client 2 writes to shared resource (SUCCESS)
Client 1 resumes from GC pause and does not know that the lock has expired
Client 1 writes to shared resource (SUCCESS, because shared resource does not know lock has expired).

You cannot make shared resource check Redis for status of lock, because network is unreliable etc.

Instead, the right way to do distributed locking is to use a fencing token/lock, which is a monotonically increasing integer number. This is discussed here:

Client 1 acquires a TTL fencing token (SUCCESS) Let's say, Token: 37
Client 1 experiences a GC pause
TTL lock expires
Client 2 acquires a TTL lock (SUCCESS, because of step 3 above). Let's say, Token: 38 (token increases monotonically).
Client 2 writes to shared resource (SUCCESS). Shared resource keeps track of the highest fencing token it has seen so far.
Client 1 resumes from GC pause and does not know that the lock has expired
Client 1 writes to shared resource (FAILED). Because locks increase monotonically, client can simply perform an equality comparison to determine which lock is newer and does not need to contact the lock server. Since Client 1 is writing with Token: 37 and Client 2 has already written with Token: 38 and 37 < 38, therefore shared resource can reject the write.
Show More

92

Reply
huayang lyu
Premium
• 6 months ago

This is a great share! And I think that any distributed lock system cannot handle the issue that GC pause happens after the client gets the lock. And the clock drift could cause the same issue. The distributed lock + fencing token might be always a safer strategy when distributed lock is needed

9

Reply
H
HollowGreenAlpaca227
Premium
• 2 months ago

Isn't this the called as "optimistic locking"?

7

Reply
Prachiti Parkar
Premium
• 15 days ago

Refer to martin kelpmann post for more details -> https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html

1

Reply
P
PastBrownPerch475
Top 5%
• 1 year ago

I feel this guide (like most sys design content about Redis) is severely lacking in discussions around durability issues. You mention you don't want to use Redis when you need durability, but then propose it as a solution for multiple problems like distributed locking and leaderboard computation.

There should be discussion around what happens in those use-cases when the Redis master goes down. What are the options and tradeoffs: do requests block until you restore from a backup, how do you gracefully handle lost locks in the middle of a distributed locking controlled flow, do you recompute the leaderboard and return error responses until you have completed the work? Etc...

41

Reply

Stefan Mai

Admin
• 1 year ago

Fair, though I think I mention this directly right under Redis Basics. If you have durability as a requirement, there are alternative implementations that provide better guarantees. For everyone else, replication and fsyncing at higher frequency is the best you're going to get.

The reality is most applications aren't going to be absolutely hosed by failing/corrupting a few requests. If they will, Redis is likely not a good solution!

16

Reply
P
PersistentMoccasinTortoise870
Premium
• 2 months ago

You mentioned AOF and RDB for durability mitigation. Can you have a video to put it in practice? Or one that uses technology alternative to Redis for solving problems like Instagram feed? Thanks!

1

Reply
H
HomelessAquamarineTrout494
Top 10%
• 2 months ago

+1 to this concern, it'd be great to fill in this gap by providing an alternative deep dive of AWS MemoryDB and how/when it can help when durability is required and how it compares with Redis (with RDB and AOF turned on).

0

Reply
Darshil Bhayani
Premium
• 11 months ago
TL;DR Summary with Pros, Cons, and Practical Redis Use Cases

Pros of Using Redis
1. High Performance: Sub-millisecond latency and ability to handle 100k+ writes/sec make Redis ideal for real-time applications.
2. Versatile Data Structures: Supports strings, hashes, sets, sorted sets, streams, geospatial indexes, etc., enabling diverse use cases.
3. Ease of Use: Simple commands and intuitive syntax make implementation straightforward.
4. Scalability: Redis can scale horizontally with clustering and replication.
5. Durability Options: Persistence mechanisms (RDB and AOF) minimize data loss risks while maintaining performance.
6. Wide Applications: Used for caching, session storage, real-time analytics, leaderboards, rate limiting, event sourcing, etc.

Cons of Using Redis
1. Memory-Intensive: Stores data in RAM, which can be costly for large datasets.
2. Potential Data Loss: Without persistence configured, data loss can occur during crashes.
3. Manual Memory Management: Developers need to configure eviction policies for memory overflow scenarios.
4. Limited Query Capabilities: Not suitable for complex queries or relational data needs.

Practical Usage of Redis in Real Problems
Redis is widely used across industries to solve real-world problems efficiently. Here are some examples:
1. Caching:
    * Example: E-commerce platforms cache product details to improve page load times and reduce backend strain.
    * Implementation: Use SET and GET commands with TTL for automatic eviction.
2. Session Management:
    * Example: Gaming platforms store user sessions to scale stateless servers during traffic spikes.
    * Implementation: Store session data as hashes (HSET) with expiry times (EXPIRE).
3. Real-Time Analytics:
    * Example: Retailers track website visits and user behavior instantly for actionable insights.
    * Implementation: Use streams (XADD, XREAD) for continuous event logging.
4. Leaderboards:
    * Example: Gaming platforms rank players based on scores using ZADD and retrieve top players with ZRANGE.
    * Implementation: Periodically remove low-ranked entries (ZREMRANGEBYRANK) to save space.
5. Rate Limiting:
    * Example: API gateways limit requests per user by incrementing counters (INCR) with expiry times (EXPIRE).
    * Implementation: Reject requests if the counter exceeds the limit.
6. Proximity Search:
    * Example: Ride-sharing apps find nearby drivers using GEOADD and GEORADIUS.
    * Implementation: Store driver locations as geospatial data and query within a radius.
7. Event Sourcing & Message Queues:
    * Example: Chat applications use Pub/Sub (PUBLISH, SUBSCRIBE) for real-time notifications.
    * Implementation: Workers claim unprocessed tasks from streams (XCLAIM) in case of failures.
8. Fraud Detection:
    * Example: Financial institutions monitor suspicious activities in real time to prevent fraud.
    * Implementation: Use hashes or streams for quick data aggregation.
Redis is a powerful tool for solving real-world problems requiring low-latency data access and scalability across industries such as retail, gaming, ride-hailing, and finance.

Show More

13

Reply
Aditya Jain
• 2 years ago

Wow! So well written and to the point. This was very helpful. Thank you for putting this together :)

12

Reply

Stefan Mai

Admin
• 2 years ago

Our pleasure Aditya, glad it was useful. Let us know if you have any feedback or questions - always looking to improve!

10

Reply
A
ashrock1970
• 1 year ago

Thanks Stefan for this well written doc. I had an ask, you did mention about Redis as a Pub/Sub, but can you provide any good reference blogs which cover Redis Pub/Sub in higher details and how it is different from Kafka.

5

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Redis Basics

Commands

Infrastructure Configurations

Performance

Capabilities

Redis as a Cache

Redis as a Distributed Lock

Redis for Leaderboards

Redis for Rate Limiting

Redis for Proximity Search

Redis for Event Sourcing

Redis for Pub/Sub

Shortcomings and Remediations

Hot Key Issues

Summary

