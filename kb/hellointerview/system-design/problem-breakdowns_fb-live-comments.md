# FB Live Comments

> Source: https://www.hellointerview.com/learn/system-design/problem-breakdowns/fb-live-comments
> Scraped: 2026-03-30



​
Sort By
Popular
Sort By
L
LogicalAmethystToad166
Top 5%
• 1 year ago

Hey Evan!
Thanks for such good content! We really appreciate it. I think there is a slight mistake in the DynamoDB schema... You have

Comments
commentId (PK)
videoId (shard)
content
author
createdAt (sort key)

I understand that we want to shard it or partition it based on videoId so that all comments of a video go to the same partition and we avoid any scatter gather anti-pattern etc.  However, you put "commentId" as the PK (partition key), and thats whats gonna be used as sharding, so different comments from the same video will go to different partitions... I think you meant to make "VideoId" the Partition Key (PK) here...

so, from DynamoDB technical standpoint it should have been like the following:

Comments
videoId (PK) --> e.g., shard
commentId (Sort Key)
content
author
createdAt

VideoID -- PK (partition key) is what guarantees that we put the comments from the same video to the same partition. And most likely you meant the "commentId" to be the SK (sort-key), which we can do through some timestamp in the id (e.g., Twitters Snowflake like id). Let me know if I'm wrong here in my understanding.

Note: throughout the article, you do indeed use "videoId" as the PK for proper sharding, so there is no issue there.. It's just that the DynamoDB schema in the image is contradictory, that's all!

Thanks again!

Show More

21

Reply
S
stevenjern
• 11 months ago

I don't think you can use videoId in this table as primary key because it's not unique.

0

Reply
CoffeeLover
Premium
• 5 months ago

VideoId is the partition key, and along with commentId as sort key to guarantee uniqueness. Partition key alone doesn't have to be unique

3

Reply
Rick Sanchez
Top 10%
• 8 months ago

This talk by a LinkedIn engineer explains dispatcher mechanism for live video reactions very well (Streaming a Million Likes/Second: Real-Time Interactions on Live Video) https://www.youtube.com/watch?v=yqc3PPmHvrA

13

Reply
L
LabourIvoryPython699
Premium
• 3 months ago

thanks for sharing!

0

Reply
Justin Schulz
• 1 year ago

Sorry to be that guy in the comments, but... Even though I agree that RESTful semantics are not the most important thing, and you've accounted for pluralization, wouldn't it be more like the following?
POST /liveVideos/:liveVideoId/comments
Great video as always, though, just a minor nitpick I wanted to clarify since you brought it up

12

Reply

Evan King

Admin
• 1 year ago

yah probably :)

0

Reply
Mohammad Asif
Top 10%
• 1 year ago

All components (streams, db, RMS) are partitioned based on VideoId. How are we handling a uneven distribution of load(hot key) issue here i.e. one video having millions of live comments coming in concurrently while other have hundreds ?

Switching to userId based partitioning wouldn't be great either because it would lead to scatter gather pattern queries across all partitions to fetch all comments for a video.

Another approach could be adding a random suffix to videoIds for popular videos lets between (1 and 5) and that way we increase the capacity for a popular videos by 5x. This will help with hot key issue at the cost of more complexity.

Are there other solutions for handling hot key issue in this problem.

12

Reply
Mohammad Asif
Top 10%
• 1 year ago

Another soln could be like adding a queue to buffer incoming comments before they are published to storage. Downside is this would increase the delay at which the comments will be available to readers.

This will not solve the traffic skewness problem. but prevent it from browning out our systems.

5

Reply

Evan King

Admin
• 1 year ago

You nailed it! You listed off the main considerations I would raise in an interview. I'd avoid the queue given the realtime requirement and instead opt for further sharding.

2

Reply
O
OlympicBlackLynx843
Top 1%
• 1 year ago

Seems like we might be overlooking the scale and throughput involved - I didn't see any back of the envelope math.  Quoting from NFR: "The system should scale to support millions of concurrent videos, and thousands of comments, per second, per live video".

That's 1B writes per second (incoming new comments).  How does the http/RESTful 'comment CRUD' service handle the writes to DB at this rate?  Assuming our service is stateless, even with 1000+  nodes, with a round-robin LB in front of it, each node will receive 1M new comment writes per second.

We also need 1000 nodes in a sharded DynamoDB deployment - even with that, can a single DynamoDB node handle 1M writes/sec?  Likely not in my estimation - 100k writes/second might be a stretch.

To make matter worse, the reads are 1000x the writes (assuming 1000 viewers for each live video on average, peaks could be more like 1M viewers for one live video!).  That's 1 Trillion updates over SSE per second.  How big does the pub/sub server farm and SSE server farm need to be, even if its sharded (by videoId as suggested), to handle 1 Trillion reads/second total?

Am I doing something wrong in the math above?

Show More

13

Reply
O
OlympicBlackLynx843
Top 1%
• 1 year ago

I did some more research so wanted to add that something like Zoom for e.g is known to have (by some estimates) 150k servers globally!  So proposing that we might need 10k or even 100k servers for massive scales like in this case ('youtube - live comments') is probably quite reasonable.  Google can afford it.
And a startup that is aspiring for that kind of scale can scale up slowly.

That said, I am sure they also use other creative techniques to throttle the reads (using CDN with polling as some have suggested here?) as well as the writes (using queues or data streaming platforms?) in the real-world - where you are not designing systems in theory; you are actually expected to design, build, run and operationalize!  Any comments or perspective on this from Stefan, Evan and team would be greatly appreciated.

2

Reply
Z
ZealousScarletCobra427
• 1 year ago

Right - but increasing the shards at runtime would require manual intervention, since we won't know beforehand which videos can become popular.

0

Reply
S
SurvivingCrimsonMarten169
Premium
• 1 year ago

Appending number if fine but make sure you think about the read path. Let's use ddb for comment table as example. Each partition has a hard limit on 1K WCU. If we want to add a random number and support 50k/sec write, we will add 0-50. The read part needs to query 50 partitions and merge the result. It could be time consuming.

1

Reply
Mohammad Asif
Top 10%
• 1 year ago

We could also batch comments to handle high volume comments for popular live videos

0

Reply
Ryan Zhang
• 11 months ago

So if we added a random suffix for popular videos, and a comment came in from a client connected to partition 3, how would we know how to fan that comment out the clients connected to partitions 1 through 5?

0

Reply
A
ApparentGrayVole549
• 1 year ago

Nice and detailed article. Thanks! I also wanted to link up this article about how LinkedIn handles real-time updates which also covers the Dispatcher part in more detail. I think it will be very useful for the readers.

https://www.infoq.com/presentations/linkedin-play-akka-distributed-systems/

5

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

Defining the Core Entities

API or System Interface

High-Level Design

1) Viewers can post comments on a Live video feed

2) Viewers can see new comments being posted while they are watching the live video.

3) Viewers can see comments made before they joined the live feed

Potential Deep Dives

1) How can we ensure comments are broadcasted to viewers in real-time?

2) How will the system scale to support millions of concurrent viewers?

3) How do we handle client disconnections and ensure viewers don't miss comments?

What is Expected at Each Level?

Mid-level

Senior

Staff+

