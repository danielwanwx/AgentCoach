# Instagram

> Source: https://www.hellointerview.com/learn/system-design/problem-breakdowns/instagram
> Scraped: 2026-03-30


Instagram is a social media platform primarily focused on visual content, allowing users to share photos and videos with their followers.
Designing Instagram is one of the most common system design interview questions asked not just at Meta, but across all FAANG and FAANG-adjacent companies. It has a lot of similarities with our breakdowns of FB News Feed and Dropbox, but given the popularity and demand, we decided this warranted its own breakdown.
Functional Requirements
Core Requirements
Users should be able to create posts featuring photos, videos, and a simple caption.
Users should be able to follow other users.
Users should be able to see a chronological feed of posts from the users they follow.
Below the line (out of scope):
Users should be able to like and comment on posts.
Users should be able to search for users, hashtags, or locations.
Users should be able to create and view stories (ephemeral content).
Users should be able to go live (real-time video streaming).
Non-Functional Requirements
If you're someone who often struggles to come up with your non-functional requirements, take a look at this list of common non-functional requirements that should be considered. Just remember, most systems are all these things (fault tolerant, scalable, etc) but your goal is to identify the unique characteristics that make this system challenging or unique.
Before defining your non-functional requirements in an interview, it's wise to inquire about the scale of the system as this will have a meaningful impact on your design. In this case, we'll be looking at a system with 500M DAU with 100M posts per day.
Core Requirements
The system should be highly available, prioritizing availability of photos/videos over consistency (eventual consistency is fine, up to 2 minutes).
The system should deliver feed content with low latency (< 500ms end-to-end response time for feed requests).
The system should render photos and videos instantly (low latency media delivery).
The system should be scalable to support 500M DAU.
Below the line (out of scope):
The system should be secure and protect user data (authentication, authorization, encryption).
The system should be fault-tolerant and highly reliable (no data loss).
The system should provide analytics on user behavior and engagement.
Here's how it might look on your whiteboard:
IG Requirements
Adding features that are out of scope is a "nice to have". It shows product thinking and gives your interviewer a chance to help you reprioritize based on what they want to see in the interview. That said, it's very much a nice to have. If additional features are not coming to you quickly, don't waste your time and move on.
The Set Up
Defining the Core Entities
Let's start by identifying the core entities we'll need. I prefer to begin with a high-level overview before diving into specifics - this helps establish the foundation we'll build upon. That said, if you're someone who finds value in outlining the complete schema upfront with all columns and relationships defined, that's perfectly fine too! There's no single "right" approach - do what works best for you. The key is to have a clear understanding of the main building blocks we'll need.
To satisfy our key functional requirements, we'll need the following entities:
User: This entity will store user information like username, profile details, etc. (We'll keep it minimal for now).
Post: This will include a reference to the media file, a caption, and the user who created it. Crucially, a single Post entity will handle BOTH photos and videos.
Media: Represents the actual bytes of the media file. We'll use S3 for this.
Follow: Represents the relationship between two users, where one user (the follower) is following another user (the followee). This captures the uni-directional "follow" relationship.
In the actual interview, this can be as simple as a short list like this. Just make sure you talk through the entities with your interviewer to ensure you are on the same page.
IG Entities
API or System Interface
The API is the main way users will interact with Instagram. Defining it early helps us structure the rest of our design. We'll start simple and, as always, we can add more detail as we go. I'll just create one endpoint for each of our core requirements.
First, users need to create posts. We'll use a POST request for that:
POST /posts -> postId
{
  "media": {photo or video bytes},
  "caption": "My cool photo!",
}
We're going to handle the actual upload of the photo or video separately, using a pre-signed URL. I'll get into the details of why we do that later, when we talk about handling large files. For now, I'm just focusing on the basic API to create the post metadata. We can assume the client gets a postId back, which it'll use later.
Next, users need to follow other users. We'll model this as a relationship resource:
POST /follows
{
  "followedId": "123"
}
The follower's ID will be extracted from the authentication token (JWT or session), so we don't need to specify it in the request body. This is both more secure and follows the principle of least privilege. In practice, it's fine to include here, you'll just need to compare it to the session before following.
Finally, users need to see their feed. This is a GET request:
GET /feed?cursor={cursor}&limit={page_size} -> Post[]
We'll use a cursor for pagination, and a limit to control the page size. I'm keeping the details of the posts array vague for now – we can fill that in later. The important thing is that we return an array of posts, and a next_cursor for getting the next page.
High-Level Design
For our high-level design, we're simply going to work one-by-one through our functional requirements.
1) Users should be able to create posts featuring photos, videos, and a simple caption
When a user is active on instagram, they should see a big button somewhere to create a post. Clicking it will take them to a new page or modal that asks for the media they want to upload and a caption which will trigger our POST /posts endpoint.
We can lay out the core components necessary to handle this request while making the initial assumption that our media is small enough to be uploaded directly via a single request.
Create Post
Clients: Users will interact with the system through the clients website or app. All client requests will be routed to the system's backend through an API Gateway.
API Gateway: This serves as an entry point for clients to access the different microservices of the system. It's primarily responsible for routing requests to the appropriate services but can also be configured to handle cross-cutting concerns like authentication, rate limiting, and logging.
Post Service: Our first microservice is responsible for handling post creation requests. It will receive the media and caption, store the post metadata in the database, the actual bytes on the media in a blob store, and return a postId to the client.
Posts DB: Stores metadata about each post including who created it, when it was created, the caption, and a link to the media in the blob store.
Blob Store: Stores the actual bytes of the media. We'll use S3 in our case as it's the most popular solution.
Quickly, let's go over what happens when a user uploads a post.
The client makes a POST request to the API Gateway with the media and caption.
The API Gateway routes the request to the Post Service.
The Post Service receives the media and caption, stores the post metadata in the database, and the actual bytes on the media in a blob store.
The Post Service returns a postId to the client.
Easy enough!
2) Users should be able to follow other users
Instagram is social! In order to see the posts of the people we follow, we need to be able to follow other users in the first place.
Importantly, this is a unidirectional relationship. For example, I follow @leomessi, but he (sadly) doesn't follow me back. Thus, I'll see his posts in my feed, but he won't see mine.
We can model this relationship with just a Followers table in our database that stores the followerId and followedId. Each time we receive a new POST /follows request, we'll insert a single new row into our table.
Followers
We've added a dedicated Follow Service to handle follow/unfollow operations separately from the Post Service. Since following users happens less frequently than posting and viewing content, this separation lets us optimize and scale each service based on its specific needs.
We get a lot of comments about people concerned about two services writing to the same database. While some claim that each service should own its data exclusively, this is arguably more academic than practical. Many production systems at FAANG and other large tech companies do have multiple services writing to the same database.
The tradeoffs are worth understanding:
Separate databases per service:
✅ Stronger encapsulation and isolation
✅ Independent scaling of database resources
✅ Freedom to choose different database technologies per service
❌ Requires distributed transactions or eventual consistency for cross-service operations
❌ Increases operational complexity (more databases to maintain)
❌ Potentially higher infrastructure costs
Shared database:
✅ Simpler transactions across domain boundaries
✅ Easier to maintain referential integrity
✅ Often simpler operationally and developmentally
❌ Tighter coupling between services
❌ Risk of one service's queries affecting another's performance
❌ Schema changes require more coordination
In practice, many organizations start with shared databases and evolve toward more isolated data stores as specific needs arise. For our Instagram design, having both the Post Service and Follow Service access the same database is a perfectly valid approach, especially since they're dealing with related domain concepts and the coupling between them is natural.
Show More
3) Users should be able to see a chronological feed of posts from the users they follow
Last up from our core functional requirements is the need to view a chronological feed of posts from the users we follow. Let's start with the simplest approach, and then we'll identify its limitations and improve it in our deep dives. Initially, we could:
Get followees: Query the Follow table to get a list of user_ids that the current user follows.
Get Posts: For each of those followed users, query the Post table to get their recent posts.
Merge and Sort: Combine all the retrieved posts and sort them chronologically (by timestamp or postId).
Return: Return the sorted posts to the client.
I'm going to opt to have the post service handle this for now rather than creating a new service, but there is no right or wrong answer. You're trading off between the complexity of the system and the cost of the operations.
Note that these queries would be incredibly slow if we needed to look through every single Followers row for every user and then search through every Post row to find the ones we want. To avoid these full table scans, we can add a few indexes to our database.
Since we're about to discuss indexing, it's an appropriate time to also choose a database technology. Given the scale, limited number of relationships, and the fact that eventual consistency is acceptable, I'm going to go with DynamoDB. That said, PostgreSQL or most other databases would be equally valid choices, you'll just want to be able to justify your decision.
Fun fact: Instagram uses PostgreSQL as its main Post metadata database. This is interesting because if you were following the SQL vs NoSQL debates of yesteryear you may be convinced that a SQL DB could not scale to support our 500M DAU. Clearly not the case!
Back to indexing, given we're opting for DynamoDB, we'll need to add a few indexes to our tables to avoid full table scans. For the Follower table, we'll make the partition key the followerId and the sort key the followedId. This allows us to efficiently query for all users that a given user follows.
For the Post table, we'll make the partition key the userId since most of our queries will be to get the posts of a given user. We can make the sort key a composite of createdAt and postId to ensure chronological ordering while maintaining uniqueness.
Feed Generation
So here is what happens with our simple approach.
The client makes a GET request to the API Gateway with the cursor and limit.
The API Gateway routes the request to the Post Service.
The Post Service queries the Follow table to get the followed users of the current user.
The Post Service queries the Post table for each followed user to get their recent posts.
The Post Service combines and sorts the posts and returns them to the client, limited by the cursor and limit.
You're probably thinking, "wait a minute, what if I'm following thousands of people? This will be crazy slow, even with indexes, right?" And you're right! This is exactly the kind of problem we'll solve in our deep dives.
Potential Deep Dives
At this point, we have a basic, functioning system that satisfies the core functional requirements of Instagram - users can upload photos/videos, follow other users, and view a chronological feed. However, our current design has significant limitations, particularly around feed generation performance and media delivery at scale. Let's look back at our non-functional requirements and explore how we can improve our system to handle 500M DAU with low latency and global distribution.
1) The system should deliver feed content with low latency (< 500ms )
We'll start our deep dives right where we left off with our high-level design -- feed generation. Our current "fan-out on read" approach could work for a small app, but it's not going to scale to 500M DAU.
Let's first understand why in the context of the database we chose.
Our first concern would be that for users following 1,000+ accounts, we need 1,000+ queries to the Posts table to get posts from each of their followed accounts.
DynamoDB does offer batch operations, but each batch is limited to 100 items and 16MB of data. For a user following 1,000 accounts, we'd need at least 10 separate batch operations to query recent posts. While these can operate in parallel, it still creates several major problems.
Read Amplification: Every time a user refreshes their feed, we generate a large number of database reads. With 500M daily active users refreshing their feeds multiple times per day, this quickly becomes unsustainable. This is going to get expensive fast.
Repeated Work: If two users follow many of the same accounts (which is common), we're repeatedly querying for the same posts. At Instagram's scale, popular posts might be retrieved millions of times.
Unpredictable Performance: The latency of a feed request would vary dramatically based on how many accounts a user follows and how active those accounts are. This makes consistent performance nearly impossible.
Let's put this in perspective with some numbers:
Each feed refresh might need to process 10,000 posts (1,000 followed accounts × 10 posts/day)
With 500M DAU, if each user refreshes their feed 5 times daily, that's 2.5 billion feed generations per day
During peak usage (e.g., evenings, major events), we might see 150,000+ feed requests per second
With these numbers, it's evident that even with a well-architected DynamoDB implementation, we'd struggle to maintain our 500ms latency target. We'd either:
Need to massively overprovision our database capacity, making the system prohibitively expensive, or
Accept higher latencies during peak usage, violating our requirements
This inefficiency is inherent to the fan-out on read model. The core issue is that we're postponing the computational work until read time, which is precisely when users expect immediate results.
Pattern: Scaling Reads
Instagram showcases the perfect scaling reads scenario - users view hundreds of posts daily but post only occasionally. This extreme read-to-write ratio demands sharding by user ID for posts, vertical partitioning for different data types (profiles, posts, analytics), and hierarchical storage for older content.
Learn This Pattern
Let's analyze some alternatives.

Bad Solution: Simple Caching (Improvement on Fan-out on Read)

Good Solution: Precompute Feeds (Fan-out on Write)

Great Solution: Hybrid Approach (Precompute + Real-time)

Pattern: Managing Long Running Tasks
The fanout on write is a good example of the pattern managing long-running tasks. When a user posts, we need to update the feeds of all their followers. This is a long-running task that can take a while to complete and need to happen asynchronously.
Learn This Pattern
When proposing Redis as a feed storage solution in your system design, make sure to proactively address durability concerns. Some interviewers could rightfully question what happens if your Redis instances go down. Without proper persistence configuration, you could lose all cached feed data, causing service degradation and poor user experience.
In your interview, you could explain that you'd implement Redis Sentinel for high availability with automatic failover, potentially use Redis Cluster for data sharding across multiple nodes, and configure persistence options like AOF (Append-Only File) or RDB snapshots to recover data after failures. A thoughtful statement like "We'd implement Redis with AOF persistence and Sentinel for failover to handle node failures with minimal data loss" demonstrates you've considered potential failure modes and aren't treating Redis as a magical black box.
2) The system should render photos and videos instantly, supporting photos up to 8mb and videos up to 4GB
There are two key challenges to large media files.
Upload efficiency.
Download/viewing latency.
Lets take these one at a time.
First, as we discuss in both DropBox and YouTube, uploading large media files requires chunking. This is because a single HTTP request is usually constrained to a max payload size < 2GB. Thus, in order to upload a 4GB video, we would need to send at least 2 (in practice, more given metadata) requests.
A common solution is to use AWS S3's multipart upload API. At a high-level, here is how it works:
First, we will call POST /posts to create the post metadata and get a postId as before, but now it will also return a pre-signed URL that can be used to upload the media. This URL is valid for a limited time (e.g., 1 hour) and allows the user to upload directly to S3 without having to go through our servers.
Client side, we use the multipart upload API to upload the file in chunks to the pre-signed URL.
S3 will automatically handle reassembling the chunks and store the final file in S3.
Pattern: Handling Large Blobs
Instagram's approach to handling large media files demonstrates the large-blobs pattern used across many interviews. The combination of presigned URLs for direct uploads, chunked uploads for reliability, and CDN distribution for global access appears in many systems handling substantial file transfers, from video platforms to file storage services.
Learn This Pattern
When we initially uploaded the post metadata, we would include a media upload status field originally set to pending. Once the media is uploaded, we update the post metadata with the S3 object_key and update the media upload status to complete.
There are two main ways to handle the post metadata update after upload completion:
Client-driven approach: The client sends a PATCH request to update the post metadata with the S3 object_key and sets the media upload status to complete once the multipart upload finishes.
Server-driven approach: We configure S3 event notifications to trigger a Lambda function or background job when the multipart upload completes. This job then updates the post metadata automatically.
The client-driven approach (Option 1) is simpler to implement but less reliable since we have to trust clients to properly report upload completion. The server-driven approach (Option 2) is more complex but provides better data consistency guarantees since our backend maintains full control over the metadata updates. Most production systems opt for Option 2 despite the added complexity.
Upload
Now that we have all our media uploaded and in S3, let's talk about how we get it to render quickly when a user views it.

Bad Solution: Direct S3 Serving

Good Solution: Global CDN Distribution

Great Solution: CDN with Dynamic Media Optimization

3) The system should be scalable to support 500M DAU
We've been keeping scale in mind throughout our deep dives, but let's summarize the key design choices that enable us to efficiently serve 500M daily active users while maintaining performance and reliability.
Precomputed Feeds (Hybrid Approach): The cornerstone of our scalable feed generation is the hybrid approach. By precomputing feeds for the vast majority of users (those following accounts with fewer than our defined threshold of followers), we drastically reduce read-time load. The real-time merging for "celebrity" posts is a carefully considered trade-off to manage write amplification.
Content Delivery Network (CDN): Using a CDN like CloudFront for media delivery is essential for global scalability and low-latency access. Dynamic media optimization further improves performance for diverse devices and network conditions.
Chunked Uploads: For large files (especially videos), chunking uploads improves reliability and user experience, and allows for parallel uploads.
Database Choice and Indexing: Our choice of DynamoDB (or a similarly scalable NoSQL database) provides horizontal scalability for metadata storage. The careful use of partition keys and sort keys ensured efficient queries.
Let's do some math and determine whether our existing scaling strategies are sufficient.
For the media files themselves, we can assume an average media size of ~2MB, so 100M * 2MB = 200TB of binary data each day.
Starting with the media, this is about 750 PB of data over 10 years. S3 can handle this, but it's not cheap. If we worry about cost, we can always move the media that has not been accessed in a long time to cheaper storage like Glacier.
For the metadata, we're looking at 100M * 1KB = 100GB of new (non-binary) data created each day. Similarly, if we grow concerned about the price of DynamoDB, we can move infrequently accessed data over to S3.
This is a common pattern. The warmer the storage, the more expensive it is. Working back from CDN -> Cache/Memory -> SSD -> HDD -> Tape, we can always take data that is infrequently accessed and move it "down a level" to save money.
When it comes to throughput, as always, we can dynamically horizontally scale our microservices to handle the load. This happens automatically with most cloud providers and is triggered based on either CPU or memory usage thresholds. Each set of horizontally scaled microservices thus implicitly has a load balancer in front of it to distribute the traffic.
After all is said and done, you might have a design that looks something like this:
Final Design
What is Expected at Each Level?
So, what am I looking for at each level?
Mid-level
At mid-level, I'm looking for a candidate's ability to create a working, high-level design that addresses the core requirements of Instagram. They should understand the basic components needed for photo/video upload, user follows, and feed generation. I expect them to propose a simple database schema and explain how posts would be stored and retrieved. While they might initially suggest a naive fan-out on read approach, with some hints they should be able to recognize its limitations and arrive at a fan-out on write solution. I want to see them problem-solve through performance bottlenecks when prompted. They should also grasp basic media storage concepts like using S3 and understand why a CDN might be necessary, even if they don't dive into the details of media optimization.
Senior
For senior candidates, I expect you to nail the majority of the deep dives, particularly around feed generation optimization and media delivery. You should understand the tradeoffs between fan-out on read, fan-out on write, and hybrid approaches, and be able to articulate why Instagram would choose a hybrid model to solve the "celebrity problem." I expect knowledge of efficient media upload handling for large files, and strong justifications for your technology choices. You should be able to discuss database indexing strategies in detail and understand how to optimize for our read-heavy workload. You likely would not have time to cover all the deep dives we did here, but if asked, you should be able to articulate the key tradeoffs and arrive at a reasonable solution.
Staff+
For staff candidates, I'm evaluating your ability to identify the true scalability bottlenecks and propose elegant solutions that balance complexity against real needs. You should quickly recognize that feed generation and media delivery are the key challenges and focus your design accordingly. I expect you to discuss system evolution over time - how would we handle growing from 1M to 500M users? Rather than immediately jumping to complex distributed systems, you should be able to articulate where simpler solutions suffice and precisely when we'd need to evolve to more sophisticated approaches. Staff candidates demonstrate a keen understanding of operational concerns, anticipate failure modes, and propose robust solutions that prioritize user experience above all.
Test Your Knowledge

Take a quick 15 question quiz to test what you've learned.

Start Quiz

Mark as read

Next: YouTube Top K

How would you rate the quality of this article?

0.5 Stars
1 Star
1.5 Stars
2 Stars
2.5 Stars
3 Stars
3.5 Stars
4 Stars
4.5 Stars
5 Stars
Empty
Comments

(217)

Comment
Anonymous
​
Sort By
Popular
Sort By
Jingyu Yao
Top 5%
• 1 year ago

This is not medium at all lol, this is like the final boss after you cleared

Facebook live feeds
Youtube
Dropbox

GG.

97

Reply

Evan King

Admin
• 1 year ago

Lol! Maybe you're right, if this gets some upvotes I'll update it to hard ;)

47

Reply
Ivan Atroshchenko
Premium
• 11 months ago

Basically it's medium it's just twitter + dropbox + media convertions

6

Reply
V
VoluntarySalmonCondor836
Top 1%
• 2 months ago

Bruh you literally listed out 3 subproblems for this question itself. That is more than enough to place this question under hard! xD

1

Reply
M
mattchiou001
Top 10%
• 1 year ago

Great content! Really love it.

One small callout (I assume you omitted this for simplicity) is that you actually need multiple pre-signed URLs to do multipart uploads (https://aws.amazon.com/blogs/compute/uploading-large-objects-to-amazon-s3-using-multipart-upload-and-transfer-acceleration/). The logic is still conceptually correct but might be worth explaining it in the actual interviews to showcase the depth.

24

Reply
D
DiverseMagentaBug254
Premium
• 1 month ago

This blog is actually helpful to understand that we can do a CDC(change-data-capture) on the server side and also upload multiple chunk information in a batch to avoid too many Write calls to dynamoDB. https://gemini.google.com/share/007d3746d10a

0

Reply
Aman Thakkar
Top 10%
• 1 year ago

I believe you could also decide on the client side about how many parts/chunks you want to have, then repeatedly query the service for the url for "next part to be uploaded". Pls correct me if I am wrong.

0

Reply
M
mattchiou001
Top 10%
• 1 year ago

I think you most likely would want to avoid doing that even if you could.

Here are two reasons that I can think of:

Latency: you will have to do unnecessary round trips (between your client and server) to retrieve pre-signed urls and you actually have to generate the pre-signed url from the server by calling S3 as well. Instead, it is much more efficient to just have your client tell you the file size, server decides the number of segments, call S3 in parallel for each segment pre-sign url generation, return the list of pre-signed urls. The size of the urls should be small enough that it won't make any meaningful difference in the latency.
While apps like instagram has control over the client, you don't have control over how frequently your users update the app. If you have a bug on core logic like this, you would want to patch them immediately and it would be much faster to do it on the sever side.

Generally, I would avoid doing client side logic unless it's much simpler to do (and way harder to do the same thing on server side).

4

Reply
M
mattchiou001
Top 10%
• 1 year ago

The number of chunks is determined by how you want to split the file (e.g. the max size per chunk). This number is going to affect how efficient your client upload is. While app like instagram does have control on the client, you don't have control on "when" your client decide to update the app. This means if you get the chunk size wrong (or simply just want to adjust it due to xyz reasons), there's going to be some delay. I think this type of trade-off usually only makes sense if the logic would have been pretty complex on the server side and pretty simple on client side (such as client side metrics) but I don't think this would be one of those cases.

I would also argue that the implementing some pagination logic (or do it on the fly as requested) is pretty overkill and without a lot of benefit. I think just having the client send you the file size and return list of pre-signed url probably makes the most sense.

2

Reply
I
InnerHarlequinFirefly879
Premium
• 1 year ago

This is great! Thank you!
Please upload a video for it :)

18

Reply

Evan King

Admin
• 1 year ago

Just added!

9

Reply
W
WoodenAquamarineSnipe931
Top 10%
• 1 year ago

Anyway to be notified when 'Premium Only' content is added or changes?

4

Reply

Evan King

Admin
• 1 year ago

Working on that right now! Hopefully end of week you'll start seeing emails :)

8

Reply
O
Omkar
Premium
• 11 months ago

Also, is it possible to add auto-generated subtitles for premium videos? I'm sure some off-the-shelf  tool would be able to do that in our "AI powered" world.

0

Reply
W
WoodenAquamarineSnipe931
Top 10%
• 1 year ago

yay!

0

Reply
Will Shang
• 1 year ago

For the facebook news feed breakdown, there is a feed table introduced in the dynamoDB vs here the feed is stored in the redis cache. How could we weight the tradeoffs?

11

Reply
M
MarriedMoccasinSpoonbill355
• 1 year ago

I just had an on-site with Meta and there was a reverse shadow. I proposed the Redis solution for feeds and I used Postgres for the user table and the post table. The interviewer had a hard time understanding how the feeds can be generated in this way. After I explained it 3 times, he asked with a confused face "So no feed table? You are only going to store it in a cache? I ... am not sure if it works." I think when proposing solutions, we not only need to consider tradeoffs, but also the interviewer's competency, especially when a reverse shadow is present.

11

Reply
Z
ZealousFuchsiaLeopon345
Premium
• 11 months ago

Lets assume the interviewers are competent, and you need to work on your communication / influencing skill.

If someone tells me they are going to store the feed only in the cache, without clearly explaining the durability considerations and fault modes, I'd count it against them.

Its on you, not them.

5

Reply
Y
YummyTurquoiseNightingale482
Premium
• 11 months ago

yeah, have to agree with you on this. The redis can also offer durablity like AOF or RDB.

2

Reply

Evan King

Admin
• 11 months ago

+1 to the above. There isn't a right or wrong answer. As always, it's about trade offs. Redis can be plenty durable for this use case. Worth me adding a little callout to this in the write up though. Will do.

7

Reply

Evan King

Admin
• 1 year ago

TLDR: no right or wrong answer.

Redis gives you blazing-fast in-memory feed access but is volatile and memory-constrained, while DynamoDB offers persistence and unlimited storage at slightly higher latency. Your choice depends on whether real-time performance (Redis) or data durability (DynamoDB) matters more for your feed experience.

5

Reply
Amit Kumar
• 1 year ago

Can we not use both? DynamoDB to persist feeds and redis as an in-memory cache on top of it?
For Cache miss, we can enrich the redis with DynamoDB?

Is it okay or an overkill?

12

Reply
L
LikeAmberDove772
Premium
• 9 months ago

redis + DynamoDB  (or any disk based persistent storage) is a more solid solution here I would say. And It's not overkill. Considering the scale of instagram, the redis cluster storage soon becomes "Not Enough".  Solely using redis as storage without backing by a persistent storage layer could be a red flag in the interview. Though redis introduces fancy feature to make it behave like a "persistent storage",  for most of the cases, it's still an layer for optimizing the reads.

1

Reply
F
FascinatingTurquoiseHeron669
Premium
• 2 months ago

One argument for not storing the feed in Database is that feeds are temporary in nature and do not need to be persisted in Database for long term. For example, a feed generated a month ago (for power users assuming they load the feed every other day or more frequently) is mostly not going to be accessed by the user. Users always want latest feed, even with infinite scrolling at most we would past 2-3 days of posts to generate the feed.

1

Reply
G
GiantCoralHyena757
Premium
• 1 month ago

I'm not sure if this argument holds. We have to maintain feed per user and frequently update it though. I'd rather use Cassandra to have maintain durable feed. Read vs write is usually skewed towards writes here, something in territory of Cassandra. Also, Cassandra has nice clustering key feature to maintain sorted post ids per user. Redis can work as a cache that stores the fully hydrated feed metadata for a user. We can limit the post ids to 500 or so, assuming 90+% user don't go beyond that in a single session.

0

Reply
S
SpecialPlumKrill871
• 1 year ago

Not sure what’d be the best place for this, I wanted to say thank you to HelloInterview team for the high quality system design sessions. I’ve been learning the entire system design section here since Christmas last year, and I got an offer two weeks back. HelloInterview system design is the best resource in the market!

10

Reply

Stefan Mai

Admin
• 1 year ago

Major congrats on your offer! Glad we could be a small part of it (let's be real, you did the hard work) and thanks for sharing the good news with us :)

4

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

Defining the Core Entities

API or System Interface

High-Level Design

1) Users should be able to create posts featuring photos, videos, and a simple caption

2) Users should be able to follow other users

3) Users should be able to see a chronological feed of posts from the users they follow

Potential Deep Dives

1) The system should deliver feed content with low latency (< 500ms )

2) The system should render photos and videos instantly, supporting photos up to 8mb and videos up to 4GB

3) The system should be scalable to support 500M DAU

What is Expected at Each Level?

Mid-level

Senior

Staff+
