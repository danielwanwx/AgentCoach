# Ad Click Aggregator

> Source: https://www.hellointerview.com/learn/system-design/problem-breakdowns/ad-click-aggregator
> Scraped: 2026-03-30



​
Sort By
Popular
Sort By
Meng Tian
Top 10%
• 1 year ago

Hi Even, for the flink checkpointing, I would argue it's still needed for us to recover the offset in kafka, otherwise even though the number of events that needs to be processed is small, we wouldn't know where to pick up the left job

27

Reply
F
FormalMagentaPeacock964
Premium
• 4 months ago

I think when the article says we do not need checkpointing, it is referring to the checkpointing that Flink automatically does which involves taking a snapshot of the system and storing it somewhere such as S3. We do not need to do this every 30 seconds or 60 seconds because it is expensive, we do it maybe every 1 hour or so.

We however need to do manual checkpointing for each 1 minute intervals. This involves writing the data to db and committing the offset in Kafka atomically within a transaction. Then Flink can know where it left off.

2

Reply
D
DustyTurquoiseCardinal816
• 1 year ago

I agree actually. Otherwise, how does the Flink job know where to resume?

2

Reply
Priyansh Agrawal
• 5 months ago

The fink Kafka connector does it all. It stores the offsets till we read so far for each partition while check pointing. The entire check pointing is done atomically using 2PC as it involves external system (Kafka)

3

Reply
Manav Agrawal
Premium
• 4 months ago

When consumers, belonging to consumer groups, read the data, they move the offset stored in kafka, kafka stores it locally and in case while reading data, consumer goes down, kafka provides the last successful read. Flink can use this.

2

Reply
R
RulingTurquoisePelican381
Premium
• 3 months ago

No, Flink cannot rely solely on Kafka's consumer group offsets for fault tolerance in stateful jobs. Kafka commits provide at-least-once semantics but don't ensure consistency with downstream operator states (e.g., windows failing post-read). Flink checkpoints integrate Kafka offsets with all operator state for exactly-once guarantees.

0

Reply
S
SweetRoseQuail897
Premium
• 4 months ago

If you do not need state. Then you would not use flink

1

Reply
P
PlannedHarlequinHalibut334
Premium
• 1 month ago

This might clear up the confusion.

So the article mentions checkpoint is not required to replay for smaller intervals. That seems incorrect, right? It should mention that kafka offsets need to be saved somewhere.

You’re right to flag the nuance. You can skip Flink checkpoints for tiny windows and just replay from Kafka, but you still need a starting point which usually comes from the consumer group’s committed offsets or a chosen timestamp. The tradeoff is that those offsets are not aligned with operator state, so you accept reprocessing a small slice and rely on rebuilding state and an idempotent or upsert sink for correctness while checkpoints are what you’d use if you need state and offsets to line up exactly once.

0

Reply
I
IdeologicalCrimsonFly982
• 1 year ago

Amazing content as always, and thanks for fixing the dropdown click area ;)

One question on handling hot shards, if we further partition our ad-ids by adding randomness won't that split these ad_click_events onto different Flink hosts? Isn't it a requirement that events for the same ad_id end up being processed by the same consumer so it can calculate the total for a given ad_id? Or is the assumption that these random id suffixes end up in our database as well? Would we then need some async job to merge those together and remove the suffix to combine those aggregations with the same true ad_ids?

16

Reply

Evan King

Admin
• 1 year ago

Good callout, you can configure a Flink job to read from multiple partitions and still aggregate data effectively across those partitions.

18

Reply
U
UniversalCyanQuelea456
Top 1%
• 1 year ago

In that case we still have a hot shard in Flink though, right?

In Yelp's presentation on YouTube of their ad aggregation system, they update the record for the window in their database multiple times, once for each partition. Since that means they can't use IF NOT EXISTS logic anymore to ensure idempotence, they also store the Kafka offset for each partition within each record. The aggregated count and the latest offset are updated in an atomic write.

1

Reply
U
UniversalCyanQuelea456
Top 1%
• 1 year ago

Correction: just re-watched the video, they update the same record multiple times per partition. If they were just writing once, they wouldn't need to store the offset, just the partition ID.

1

Reply
D
DisciplinaryFuchsiaTuna318
• 1 year ago

is this the yelp video that you mentioned?
https://www.youtube.com/watch?v=hzxytnPcAUM

3

Reply
Neeraj jain
Top 5%
• 1 year ago

Thanks for the video... comment section of this website is goldmine

1

Reply
Amran Tomer
• 2 months ago
• edited 2 months ago

This video is great! It helps you connect the dots to real world problems. Thank you for sharing.

0

Reply
Mohammad Asif
Top 10%
• 1 year ago

In that case we still have a hot shard in Flink though, right?

Since the data has been buffered per [ad Id+random number] the volume of data that need further aggregation will be much lower. For example if we have limit the random number from 1-5 then for hot ad Id we'll only have 5 number to add after the first buffering.

I am concerned that these 5 numbers may reside across multiple flink node and would require to be shuffled across those nodes to be aggregated. Though we aren't super realtime it fine. We are absorbing a latency of 1 mins any way. this shouldn't add much.

0

Reply
I
IcyFuchsiaHookworm732
Premium
• 1 year ago

Hi, it is still hard to figure out for me. In the normal distribution, all the data with the same AdId goes to the same partition, so a Flink job reads and counts them. However, if we distribute this data to other partitions by adding a random number, all consumers would count the parts that they receive. If we add a Flink job that reads all partitions, it would count all AdIds and become overwhelmed. Additionally, other jobs would still count this AdId and write to the database. Could you give more detail about it, please?

Maybe we could count it on Redis so all counts would go to the same point, but after the time window ends, which process can get it from there and write it to the database?

Thanks

0

Reply
J
jokerchendi
Premium
• 1 year ago

The Flink consumers can have its own calculation topology and shuffle data around to finally aggregate by adId. So it doesn't matter click events are distributed across Kafka/Kensis partitions.

4

Reply
R
RulingTurquoisePelican381
Premium
• 3 months ago

To avoid hotspots in Flink, aggregation can be performed in two stages.

Stage 1 (load distribution): For hot IDs, we aggregate using a partitionKey that expands a single logical key (such as an adId) into multiple deterministic physical keys (for example, adA#0 to adA#15). Aggregating on this expanded key distributes the workload across multiple parallel tasks, preventing any single task from becoming a bottleneck.

Stage 2 (correctness merge): After partial aggregation, we regroup the results by the original logical key (adId) and merge the partial results. Because the data volume has already been reduced, this merge is lightweight and restores the correct global aggregation without reintroducing hotspots.

2

Reply
Lazy Dog
Premium
• 4 months ago

You just need 2 streams in Flink, one to do local aggregation and the second one is to aggregate on the results from the first stream.

2

Reply
I
IdeologicalCrimsonFly982
• 1 year ago

Understood, thanks for the reply!

0

Reply
C
ConcreteBlushMastodon771
Top 5%
• 1 year ago

Would you ask someone without data pipeline experiences this question? The great solution requires knowledge of Flink / Spark, which can be foreign to people outside of the data processing domain. Wouldn’t it stop you from collecting proper signals? A staff engineer in other infra spaces might not be familiar with these tools.

12

Reply

Stefan Mai

Admin
• 1 year ago

There are other great solutions which don't require a stream processing framework. The underlying concepts are basically the same. Let us know if you have questions about this!

1

Reply
C
ConcreteBlushMastodon771
Top 5%
• 1 year ago

I see. Flink is basically an event aggregator in this design, right? It groups the events by ad id then by timestamps at minute granularity. If I am not familiar with Flink and suggested we could use a queue worker that does this, I assume it’s still a good answer?

4

Reply

Stefan Mai

Admin
• 1 year ago

Yeah - just be prepared to talk about how that grouping happens logistically. Talking about consistent hashes, fault-tolerance, etc.

3

Reply
C
ConcreteBlushMastodon771
Top 5%
• 1 year ago

Thank you. I was recently asked this question in my interview, and I aced it with this key and all the discussions in comments! You guys rock!

3

Reply
B
BoldBrownHeron815
• 1 year ago

Hey, which company was that

3

Reply
T
TechnicalScarletJellyfish241
• 1 year ago

Why cant we use a time series database for this. wouldnt that be super fast?

9

Reply

Evan King

Admin
• 1 year ago

Could replace the OLAP db with timeseries, yah. Especially since in our simplified requirements there are not many dimensions.

1

Reply
Rahman Mustafayev
Premium
• 26 days ago

doesn't this contradict with the fact that it's recommended to use TimeSeriesDB for metrics monitoring? I expect metrics to have more dimensions that Ads.

0

Reply

2 replies hidden which refer to old versions of the article. Expand them.

Clinton Donghui
• 1 year ago

How to ensure each ad click is aggregated into DB exactly once? For example, what happens if the "flush to DB" succeeded but the task crashed before committing the offsets back to Kafka? Re-processing the same input would cause double counting. It appears the OLAP db must support and participate in a two-phase commit protocol coordinated by Flink.

6

Reply
V
VerticalBlackFlea403
Premium
• 8 months ago

one way is let Kafka-Flink-OLAP do end-to-end exactly-once processing to avoid duplicated write https://flink.apache.org/2018/02/28/an-overview-of-end-to-end-exactly-once-processing-in-apache-flink-with-apache-kafka-too/. this is two phase commit.

another way is to add a version number on the aggregated table to record the last processed Kafka offset. This allows Flink to do idempotent writes

1

Reply
Priyansh Agrawal
• 5 months ago

Great answer. However, the first approach will not work with persistent aggregation storage because it is not considered in 2PC and is external to the 2PC boundary. What we could do, IMO, is we could publish (sharded by ad_id) the aggregated data for each ad_id into another topic of Kafka and then leverage the second approach to update into DB optimistically. The only problem here is will the DB supports conditional check like Cassandra/MySQL .

0

Reply
A
AddedLimeCarp593
Top 1%
• 10 months ago

We could make writes to the DB idempotent by checking if a particular adId-minute combo has already been written to the DB.

0

Reply
Priyansh Agrawal
• 5 months ago

Would you store time series data with window formed from event time or processing time.  We should choose event time for accurate representation of the historical data, but must handle the case when an event comes out of order wrt to time (delayed)

0

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Understanding the Problem

Functional Requirements

Non-Functional Requirements

The Set Up

Planning the Approach

System Interface

Data Flow

High-Level Design

1) Users can click on ads and be redirected to the target

2) Advertisers can query ad click metrics over time at 1 minute intervals

Potential Deep Dives

1) How can we scale to support 10k clicks per second?

2) How can we ensure that we don't lose any click data?

3) How can we prevent abuse from users clicking on ads multiple times?

4) How can we ensure that advertisers can query metrics at low latency?

Final Design

What is Expected at Each Level?

Mid-level

Senior

Staff+

