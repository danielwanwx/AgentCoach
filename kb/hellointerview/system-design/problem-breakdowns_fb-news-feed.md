# FB News Feed

> Source: https://www.hellointerview.com/learn/system-design/problem-breakdowns/fb-news-feed
> Scraped: 2026-03-30



​
Sort By
Popular
Sort By
P
PassingIndigoDragon169
Top 1%
• 9 months ago

I see you are trying a new short video format like you did the youtube video for this problem but I kindly request please go back to the long format. In the beginning I did find the long format video was too much of information overloading my brain and could not even finish the video but now as I am reading more content, I am really seeing the value in the long format video where you explain the real depth of certain choices and that is really very helpful because that is we should be explaining the reasoning behind each choice in the interview.

As usual thanks for the amazing content and effort!

218

Reply
P
ParticularAquamarineCat800
Top 5%
• 6 months ago

Vote for this!

6

Reply
M
MagnificentCrimsonKangaroo965
Premium
• 4 months ago

What you said was absolutely true. This video is like recorded that it's END OF THE WORLD!

4

Reply
Tomer Lieber
• 5 months ago

Vote for this as well!

1

Reply
Tony Kuo
Premium
• 15 days ago

Please upload the longer version

0

Reply
Marat Sultangareev
Top 5%
• 1 year ago

I have failed today at my first-ever System Design interview. The problem was straightforward but compact—just had to design the user’s feed view and a message-posting feature. I hadn't really looked at this type of problem before and was just starting to practice. The high-level design went fast, and the interviewer made it seem simple. So, I decided to skip the Non-Functional Requirements (NFRs) and circle back to them later—bad idea.

The interviewer then asked how the feed would be formed, so I explained it almost the same as I’d seen elsewhere—by querying the list of user IDs the current user follows, then fetching the top posts from those users and sorting by timestamp. On second thought, a reversed timestamp (something like a 'max timestamp' set to 2050-12-31T00:00:00Z minus the current timestamp) could have been better. Anyway, the interviewer didn’t seem too happy with this solution, so I started thinking about something more compute-efficient, like using CDC to stream updates into a Kafka-like in-memory queue, partitioned by user ID with each user’s last N messages. Then, using a MapReduce job, I’d collect posts by the followee IDs in a HashSet and reduce them to the Top K latest posts, ordered.

Honestly, I got so wrapped up in designing the feed that I completely missed the hints the interviewer was giving about scalability. Toward the end, he pointed out that I forgot about scalability and had been trying to nudge me in that direction (right around the time I zoned out). First rule for next time: DON’T FORGET NFRs!

Show More

44

Reply
IN
Itai Noam
Top 1%
• 9 months ago

A few questions that came to mind as I studied. Hopefully I didn't get it too wrong.
Q: Why does the POSTS table use userId as the partition key, even though the main read pattern is to fetch all posts by a user? That makes it impossible to run a simple query like that.
A: Because using userId as the partition key would create a hot partition — all of a popular user's posts would land on the same partition, which can hurt performance and scalability.

Q: Okay, but now we’ve created a GSI with userId as the partition key — didn’t we just move the hotspot problem there?
A:Yes, GSIs can also become hot, but they’re easier to scale, replicate, or shard than base tables. If the base table gets overloaded, it can cause catastrophic write failures, so it's safer to offload this kind of read-heavy access to a GSI.

Q: Why doesn’t the Posts GSI include the post content?
A: To avoid write amplification. Including full content in the GSI would duplicate large amounts of data, which slows down writes. It's common practice to include only the minimal necessary fields in a GSI.

Q: In the naive feed implementation, we load all posts from all followed users, then sort them in memory. But could that be thousands of posts?
A: Yes, it could be. A temporary workaround is to limit the number of posts per user (not ideal), or use a min-heap or priority queue to keep just the most recent 200 posts. The in-memory sort then becomes O(n log k) instead of O(n log n). Eventually, this will be solved more efficiently using fan-out architecture.

Q: Why does UserFollows have a sort key? It’s just using a random ID.
A: Because DynamoDB requires each item to have a unique primary key, and followerId alone isn’t unique. By adding a sort key (like a random or followed user ID), we get a composite key that ensures uniqueness.
Reasons for having a sort key:
Allows O(1) lookup of a unique record.
Enables pagination over multiple items under the same partition key.
Enforces uniqueness, preventing duplicates.

Show More

31

Reply
V
VitalLimeKoi227
Premium
• 22 days ago

For Q1 - you mean, why are we using postID as the PK right? Also thank you so much for this post, this answered many of my lingering questions!

1

Reply
Test User
• 2 years ago

Could we also use PostGres here as the tables have relationship with each other?

15

Reply

Stefan Mai

Admin
• 2 years ago

You could definitely use Postgres but it wouldn’t be because a relationship exists. While relational databases do excel in analytic queries with joins of highly related data, you can model relational data with a nosql database easily (as shown here!).

If you do opt to use Postgres or Mysql be prepared to talk about partitioning and replication strategies. Same concepts, different toolset.

25

Reply
R
RequiredIvoryPeacock357
Premium
• 1 year ago

How so? I don't see how you would model getting posts from a certain userId which would definitely normally require joins

0

Reply
Sergei Bogachev
• 1 year ago

With NoSQL, instead of joins on database level, you first load the list of followerId from the Follower table, and then use it as a filter for Post table. It's the same join, but done in the code and the memory space of your application instead of database's.

6

Reply
Sameer Sood
• 1 year ago

Practically, you will need to batch/paginate no sql db using hashes.

0

Reply
M
MilitaryIndigoWarbler600
• 1 year ago

Rather than join, simply lookup?

1

Reply
S
SingleAmaranthMagpie897
Premium
• 8 months ago

I see this problem similar to the Instagram system design question excluding the handling of media. I'm curious why in one we're precomputing the feed in dynamodb (News Feed) and in another one we store the precomputed feed in a Redis cache (Instagram). Would it be okay to handle the precompute in a Redis cache for this problem?

14

Reply
D
Donny
Premium
• 5 months ago

In the video, Stefan mentions you could put the precomputed feed in a cache, but he put it in DynamoDB for simplicity.

9

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

1. Users should be able to create posts.

2. Users should be able to friend/follow people.

3. Users should be able to view a feed of posts from people they follow.

4. Users should be able to page through their feed.

Potential Deep Dives

1) How do we handle users who are following a large number of users?

2) How do we handle users with a large number of followers?

3) How can we handle uneven reads of Posts?

What is Expected at Each Level?

Mid-level

Senior

Staff+

