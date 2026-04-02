# Sharding

> Source: https://www.hellointerview.com/learn/system-design/core-concepts/sharding
> Scraped: 2026-03-30



​
Sort By
Popular
Sort By
Vinayak Borhade
Top 10%
• 5 months ago

Apparently DynamoDB does provide support of ACID transactions in distributed setup. It also doesn't use pessimistic concurrency control but rather an optimistic approach where in the rows involved in transactions are not locked (which happens in 2PC protocol mentioned). If we have low contention workload and our system needs to have a distributed database do you think it's worth mentioning this feature of DDB in an interview when countering the point regarding having transactions support in sharded databases?

paper - https://www.usenix.org/system/files/atc23-idziorek.pdf
blog - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/transaction-apis.html

9

Reply

Evan King

Admin
• 5 months ago

It's great to show off practical knowledge like this! I'd be careful about leaning on it in interviews without appropriate caveats. DDB transactions have strict limits (25 items max, 4MB total, same region only - this is off top of my head, so these numbers may be outdated but point stands) and OCC means high contention workloads will see lots of transaction failures and retries so its not right for every workflow

20

Reply
Vinayak Borhade
Top 10%
• 5 months ago

Nice catch, that definitely is something to keep in mind when using these kind of managed technologies!

BTW there are many applications of this in real world and quite a few tech companies have built and published blogs for workarounds in relational / non-relational DBs pertaining to cross shard transactions, pasting one such example that I'm aware about from dropbox - https://dropbox.tech/infrastructure/cross-shard-transactions-at-10-million-requests-per-second.

6

Reply
Owen
Premium
• 1 month ago

Plus one to Evan. DynamoDB is not BORN with transaction, the feature is added around 2019/2020 with lots of limitations. One big difference between DDB TX and Postgress is - DDB does not use MVCC, thus the transaction efficiency (esp for repeatable read) is not as good as PG.

The use-case of DDB TX focuses more on the Atomic of the ACID with bunch of limitation that Evan mentioned.

1

Reply
C
ChemicalBlushNarwhal953
Premium
• 20 days ago

MVCC is for single node transaction to achieve serializable snapshot isolation. DDB's is a distributed transaction. I think they are different.

0

Reply
Y
YeastyMoccasinHyena669
Premium
• 20 days ago

MVCC is for single node transaction

Not necessarily MVCC is a technology, speaking in english, keep multiple versions throughout mutation history. Spanner a distributed DB, for example, uses MVCC

1

Reply
C
ChemicalBlushNarwhal953
Premium
• 20 days ago

Thank you for clarifying. I did some extra research and found my understanding incorrect.

1

Reply
VV
Vidit Virmani
Premium
• 4 months ago

partitioned

sharded?

4

Reply
R
RemarkableHarlequinDragonfly196
Premium
• 2 months ago

How does having a dedicated celebrity shard help with the hot spot problem? Wouldn't putting popular celebrity accounts onto the same shard make that shard get even more traffic than other shards?

3

Reply
A
antomasini98
Premium
• 2 months ago
• edited 2 months ago

I think he might mean putting just some celebrities in one shard, maybe if it is a "big whale" have just one shard for that celebrity (?) or something like that.

1

Reply
Tyler Gaugler
Premium
• 4 days ago

He mentions in the youtube video that you might end up vertically scaling the celebrity shard. So I guess the point is isolating the "hot" partition keys and putting them on a dedicated shard that can scale with throughput spikes.

0

Reply
vikas tiwari
Premium
• 1 month ago

I think this is more of a 'trending' scenario. It’s rare for multiple keys to trend simultaneously. Since today’s trending data likely won't be trending tomorrow, the load should shift, preventing any single node from becoming a permanent hot spot.

0

Reply
canigetyourhoiya
Premium
• 1 month ago

wondered this too, isn't the dedicated celebrity shard going to "the" hot spot? at least i think one benefit of doing this is that the other data in the same shard is less impacted.

however, still, the dedicated celebrity shard sounds like hella busier than others

0

Reply
Arun
• 3 months ago

Great tutorials! Thank you!!

Please consider the following two statement from the text above:

Statement 1: Aligns with queries: Your most common queries should ideally hit just one shard. If you shard users by user_id, queries like "get user profile" or "get user's orders" hit a single shard. Queries that span all shards become expensive.

Statement 2: Use compound shard keys: Instead of sharding just by user_id, combine it with another dimension like hash(user_id + date). This spreads a single user's data across multiple shards over time, which helps if the hot spot is both high volume and spans time periods.

In a compound shard key of hash(user_id + date), what is/are the efficient ways to serve user-centric queries, e.g., find all orders of an user, find all friends of an user, find all files of an user, etc.?

2

Reply
R
raphael.licha2
Premium
• 5 months ago

Are the shards hosted in containers and managed by Kubernetes? If so, is it fine to have such big containers (>10TB and lot of CPU)?  Or do they live in separate, dedicated instances? And in this case, how are they managed?

2

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

First, what is Partitioning?

What is Sharding?

How to Shard Your Data

Choosing Your Shard Key

Sharding Strategies

Challenges of Sharding

Hot Spots and Load Imbalance

Cross-Shard Operations

Maintaining Consistency

Sharding in Modern Databases

Sharding in System Design Interviews

When to Mention Sharding

What to Say

Conclusion

