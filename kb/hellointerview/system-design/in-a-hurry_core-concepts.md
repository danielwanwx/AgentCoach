# Core Concepts

> Source: https://www.hellointerview.com/learn/system-design/in-a-hurry/core-concepts
> Scraped: 2026-03-30



​
Sort By
Popular
Sort By
David Shimon
Top 10%
• 1 year ago

Regarding the "optimistic update" flow diagram:
Would it be better to place the version check after processing the update but before writing the new version?

28

Reply
Neeraj jain
Top 5%
• 1 year ago

Can you add detail dive on optimistic locking

39

Reply
Aashray Jain
Premium
• 3 months ago

Sorry, where are we seeing this "optimistic update" flow diagram??
I did not find it in the current article.

10

Reply
T
TenderPlumChipmunk617
• 1 year ago

+1 here. Is this really optimistic locking if you are checking the value and updating separately? Feels like this diagram could be updated for clarity.

8

Reply
S
SovietApricotCrab448
• 1 year ago

I asked Claude and got the following answer:
Optimistic Concurrency Control (OCC) is a strategy used in database management systems and distributed systems to handle concurrent access to shared resources. Here's a concise explanation:
Key concepts:

Assumption: Conflicts between transactions are rare.
Execution phases: Read, Validate, Write.

How it works:

Read phase:

Transaction reads data without acquiring locks.
Local copies of data are made.

Compute phase:

Transaction performs computations using local copies.

Validate phase:

System checks if any conflicts occurred during execution.
Typically involves comparing timestamps or version numbers.

Write phase:

If validation succeeds, changes are committed.
If conflicts are detected, the transaction is aborted and restarted.

Advantages:

Reduced lock overhead
Higher concurrency in low-conflict scenarios
Deadlock-free

Disadvantages:

Potential for wasted work if conflicts occur
Higher abort rate in high-contention environments

Comparison to pessimistic concurrency control:

Pessimistic: Assumes conflicts are likely and uses locks.
Optimistic: Assumes conflicts are rare and detects them later.

Show More

14

Reply
cst labs
Top 5%
• 1 year ago

Let me add more colors to this. The optimistic concurrency control is very much like CAS (Compare and Swap operations) that are synchronization primitives without any locking. The idea is to compare and then swap if true. Otherwise, go back to the loop and try again until you succeed. Note that this is why the recommendation is to not use optimistic concurrency control when the contention is high. In that scenario, there may be several retries and that may lead to starvation.

Now back to the database concurrency control: a good example of this is while using ETag. Remember, Etags are version numbers that identify a particular version of a database entry. So the caller will set a modification when Etag version is known to itself. SO the caller will write a query where it may say : update the value if the etag version is <> and if it fails, retry. In this case, the caller is doing that logic while making API calls. However, if the logic resides at the server side, it will fetch the records using MVCC (lock free), do certain things as needed and then use a transaction to make the change if etag or any version identifier matches.

12

Reply
Rishit Ratan
• 1 year ago

+1 The optimistic locking diagram could be updated for better clarity. We can make it clear that the check version step happens on the DB side.

1

Reply
R
ResponsibleScarletScorpion732
• 1 year ago

Usually the version check, record update and version increment is done in a single step. The diagram might present them separately just for clarity.

If the steps are indeed separate, the check version would need to acquire an exclusive lock on the record so it doesn't introduce a window of opportunity between the version check and the actual record update during which another transaction can modify the data. In this scenario I don't think the order of operations would make any difference because the exclusive lock is held until the end of the transaction no matter what operation is first to acquire it.

6

Reply
G
GenerousCoralSilverfish391
Premium
• 8 months ago

The whole point of "optimistic locking" is to NOT acquire a lock.

4

Reply
M
MolecularHarlequinWhippet976
• 1 year ago

I just want to say the work you all put out is easily some of the best content out there. It is straight to the point and at the same time makes no assumptions of prior knowledge. This makes it easy for a beginner like myself to get up to speed. Thanks for all your hard work please keep it up

17

Reply
C
CentralVioletBear276
• 10 months ago

How important is monitoring and what would a deeper dive look like? I ask this because from the question breakdown writeups/videos I've seen, monitoring essentially isn't covered at all. However, I'm currently in some interview loops and with Datadog specifically, I've been told ahead of time that there will be a strong focus on monitoring during the sys design round bc Datadog's product has to do with monitoring. Unsure the level of detail I should be going into here, past talking about what to monitor and what tool I would use.

6

Reply
Luke Li
Premium
• 1 month ago

IMO It's a must-have for every real-world system, but it's also less interesting to talk about. Like, we'll use CloudWatch/Prometheus/..., and run some kind of agents on each node to collect and publish logs/metrics, usually there are existing products to use and they generally works fine and don't need much attention unless the goal is to design the monitoring system itself.

0

Reply
chetan sahu
Premium
• 4 months ago

Hi Stefan and Evan, I can no longer find the topic scalability in the core concepts sections, if i'm not wrong earlier the core concepts page had scalability as a topic and can we have a dedicated section for scalability if it seems significantly useful ?

4

Reply
Abhaya Shankar
• 3 months ago

For a user-centric app like Instagram, sharding by user_id means all of a user's posts, likes, and comments live on one shard.

Sharding by user_id is actually one of the best practical strategies for a user-centric app like Instagram — but it comes with trade-offs you must be aware of.

Hotspot users = Hot shards
Celebrities with millions of followers create massively skewed read/write traffic.

Rebalancing users can be expensive
If a shard gets full, you must move users from one shard to another — heavy operation.

3

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Networking Essentials

API Design

Data Modeling

Database Indexing

Caching

Sharding

Consistent Hashing

CAP Theorem

Numbers to Know

