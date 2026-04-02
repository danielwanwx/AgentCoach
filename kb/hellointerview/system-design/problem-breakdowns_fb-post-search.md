# FB Post Search

> Source: https://www.hellointerview.com/learn/system-design/problem-breakdowns/fb-post-search
> Scraped: 2026-03-30



​
Sort By
Popular
Sort By
Eugene Myasyshchev
Top 5%
• 1 year ago

If we have 3.6T posts and we have postId of let's say 20bytes (at least), we will need an insane amount of memory for this. Also redis lists are limited to around 4B items, with 1B posts created daily there is a high chance that some very popular keyword will span more than 4B docs.

Yes, you mentioned to keep lists small  as storage optimisation, but I think it should be mentioned right away as a key design consideration, since the system will not handle this volume without it.

Also offloading to the cold storage, we will still need to update it if someone likes old post, and updating in S3 may be quite challenging, depending on how we organise the data there.

This is a great design anyway, thanks for your efforts, It helps a lot to prepare for the interviews!!!

43

Reply
Haris Osmanagić
Premium
• 3 months ago

Here's my take on this.

This is an artificial scenario, where we're expected to show how we'd organize the data in an index, and not build a full-text search engine. With that, it's expected we'll take some shortcuts. We won't be organizing directly on a disk, but using a K/V store. What I believe is important is to call this out.
I don't think we need to keep all the data in memory. All we need is a K/V store.
As for updating the cold storage when an old post is liked, that I believe is solved with the two-stage architecture, where the indexes are updated only when likes exceed a certain limit (e.g., a power of 2).

3

Reply
F
FederalHarlequinLamprey277
• 1 year ago

I think its assuming the postId is 8bytes(unsigned 64bits i.e. 2^64) and the redis is sharded by a hash of the keywords (using a 64bits non-cryptographic hash).
Yes, you're right the length of the Redis sorted list of post_ids need to be capped and less liked post can be stashed away in cold storage in small chunks identified by range keys for easier retrieval and update when needed.

0

Reply
F
FlutteringCrimsonKite231
Top 5%
• 1 year ago

In no way you can clear the interview with this design. You can't put all the index into memory, it's not practical in both ever increasing storage and astronomical cost. Also it doesn't make sense. You at least need a layer architecture by time. Say day / week / month / year index layers. A day's data in many cases give you more than 1000 posts, if not enough the pagination can always prefetch a week's post in the background while user scrolling. Day index can fit into memory, all the others should be in a read optimized DB.
Likes compares to index is exponentially smaller, it's a counter per post v.s. multiple terms per post. Even if you store the like userId in a list, it's still much smaller. You can easily put a whole year's worth of like data into memory, and use it during ranking not querying.

21

Reply

Stefan Mai

Admin
• 1 year ago

Always funny to get these kind of comments: this question was asked of me and I passed at the E6 level for Facebook.

You don’t need to keep post contents in memory, the indexes are smaller. Assume 500m keywords, with 1k posts you’re talking a few terabytes. Not a problem!

10

Reply
F
FlutteringCrimsonKite231
Top 5%
• 1 year ago

Ok if you made it, then my assertion is wrong. In real world, none of the companies I worked with design index this way, though with smaller scale than FB e.g. twitter.

If the system supports phrase queries, even if we skip the stop words etc., the index size is almost always larger relative to the raw posts for the following reasons:

The raw text stores the content as-is, while the index dissects it into smaller, structured components with metadata e.g. positions, term frequencies, and document IDs.
Multi-keyword query support necessitates storing positions and term-document mappings, which adds a significant overhead.

Sharding or tiered storage is key design element, in my opinion, of this system.

9

Reply

Stefan Mai

Admin
• 1 year ago

Makes sense to me!

Keep in mind that these questions aren't trying to ascertain whether you've designed an industrial search and retrieval stack - they're trying to get at whether you understand key fundamentals and have the skills to piece together solutions to problems that are digestible in a very short period of time.

You're right about arbitrary search indexes! But this problem has greatly simplified functionality which we can exploit in such a way that the index size << contents.

7

Reply
F
FlutteringCrimsonKite231
Top 5%
• 1 year ago

Agreed. I might fall into my past experience trap .. Design interviews are very different animals with the real-world products given the 45 minutes limit lol. Thanks for sharing your insight!

5

Reply
K
kstarikov
Top 5%
• 10 months ago

Assume 500m keywords, with 1k posts you’re talking a few terabytes

I guess 500m keywords comes mostly from bigrams. But where does the '1k posts' come from?

0

Reply

Stefan Mai

Admin
• 10 months ago

We are limiting the size of each index item.

0

Reply
Tarun Anand
• 1 year ago

How are we making sure that likes are idempotent, to ensure that a user can like a post only once?

8

Reply

Stefan Mai

Admin
• 1 year ago

Probably wouldn't be in scope for this question (though an interviewer might turn it into a deep-dive). The Likes Service would need a strongly consistent store of userId-postId to be able to serve its clients, making it responsible for de-duping makes sense!

9

Reply
pradeep jawahar
• 1 year ago

Similar to Ad Click Aggregator.

13

Reply
S
SafeJadeCrawdad811
• 1 year ago

It is very simple. Just look up likes data and if there is, just return that, otherwise insert a new one and return it, all in the same transaction.

1

Reply
C
core2extremist
Top 10%
• 5 days ago

With the proposed architecture the like events are stored in Kafka. In addition to storing the actual events, Kafka also stores consumer offsets for each topic-partition.

In practice this gives you idempotence 99.99% of the time:

consumer polls the broker, broker responds with <= batchSize messages since the consumer's last committed offset
hit backend APIs for incrementing like count, updating indices every time or in logarithmic steps
commit new offsets
goto 1

If a failure happens in step 2 then O(batchSize) likes are duplicated. But crashes are (or should be) rare, the "blast radius" is contained to that O(batchSize) likes, and failures outside that critical region will not affect idempotence. If workers crash once per day (yikes) causing 50 excess likes on average, and each handles 10k likes/second ~ 1B likes/day the error rate is a minor 0.000005%. That's darn good for social media.

For full exactly-once processing I agree with Stefan, you would atomically do something like this in a transaction for each like:

update a likes table to add the (user_id, post_id) where user liked the post
update the posts table, setting likes = likes + 1 if and only if (user_id, post_id) was added

From some reading elsewhere a common pattern seems to be

store (user_id, post_id) interactions in a strongly consistent way, full accuracy
approximately store total likes for each post separately, accepting some rare missed/duplicate writes in favor of very high throughput and low latency
use batch processing to periodically recompute exact likes counts
Show More

0

Reply
M
MagneticBlueAnt398
Top 10%
• 1 year ago

If the index is in memory (Redis) already, how would the Redis cache be of any help? If time complexity of looking for a value in a hash map is O(1) anyway, what benefit would that cache bring as compared to the case when we have cache vs DB?

7

Reply
Z
ztan5362
• 1 year ago

Is there a reason to be using Redis as primary storage and not sql/nosql databases? Do sql/nosql support inverted indexinga and sorted sets?

4

Reply
D
DistinguishedPlumBoar695
Premium
• 8 months ago

I think the reason is because databases store data in the filesystem (slow I/O) and Redis stores it in memory (fast I/O)

1

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

Scale estimations

The Set Up

Planning the Approach

Defining the Core Entities

API or System Interface

High-Level Design

1) Users should be able to create and like posts.

2) Users should be able to search posts by keyword.

3) Users should be able to get search results sorted by recency or like count.

Potential Deep Dives

1) How can we handle the large volume of requests from users?

2) How can we handle multi-keyword, phrase queries?

3) How can we address the large volume of writes?

4) How can we optimize storage of our system?

What is Expected at Each Level?

Mid-Level

Senior

Staff+

