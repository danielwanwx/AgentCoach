# Online Auction

> Source: https://www.hellointerview.com/learn/system-design/problem-breakdowns/online-auction
> Scraped: 2026-03-30


An online auction service lets users list items for sale while others compete to purchase them by
placing increasingly higher bids until the auction ends, with the highest bidder winning the item.
As is the case with all of our common question breakdowns, we'll walk through this problem step by step, using the Hello Interview System Design Framework as our guide. Note that I go into more detail here than would be required or possible in an interview, but I think the added detail is helpful for teaching concepts and deepening understanding.
Functional Requirements
Core Requirements
Users should be able to post an item for auction with a starting price and end date.
Users should be able to bid on an item. Where bids are accepted if they are higher than the current highest bid.
Users should be able to view an auction, including the current highest bid.
Below the line (out of scope):
Users should be able to search for items.
Users should be able to filter items by category.
Users should be able to sort items by price.
Users should be able to view the auction history of an item.
Non-Functional Requirements
Before diving into the non-functional requirements, ask your interviewer about the expected scale of the system. Understanding the scale requirements early will help inform key architectural decisions throughout your design.
Core Requirements
The system should maintain strong consistency for bids to ensure all users see the same highest bid.
The system should be fault tolerant and durable. We can't drop any bids.
The system should display the current highest bid in real-time so users know what they are bidding against.
The system should scale to support 10M concurrent auctions.
Below the line (out of scope):
The system should have proper observability and monitoring.
The system should be secure and protect user data.
The system should be well tested and easy to deploy (CI/CD pipelines)
On the whiteboard, this could be short hand like this:
Requirements
The Set Up
Defining the Core Entities
Let's start by identifying the core entities of the system. We'll keep the details light for now and focus on specific fields later. Having these key entities defined will help structure our thinking as we design the API.
To satisfy our key functional requirements, we'll need the following entities:
Auction: This represents an auction for an item. It would include information like the starting price, end date, and the item being auctioned.
Item: This represents an item being auctioned. It would include information like the name, description, and image.
Bid: This represents a bid on an auction. It would include information like the amount bid, the user placing the bid, and the auction being bid on.
User: This represents a user of the system who either starts an auction or bids on an auction.
While we could embed the Item details directly on the Auction entity, normalizing them into separate entities has some advantages:
Items can be reused across multiple auctions (e.g. if a seller wants to relist an unsold item)
Item details can be updated independently of auction details
We can more easily add item-specific features like categories or search
In an interview, I'm fine with either option - the key is to explain your reasoning.
Here is how it could look on the whiteboard:
Core Entities
API or System Interface
Let's define our API before getting into the high-level design, as it establishes the contract between our client and system. We'll go through each functional requirement and define the necessary APIs.
For creating auctions, we need a POST endpoint that takes the auction details and returns the created auction:
POST /auctions -> Auction & Item
{
    item: Item,
    startDate: Date,
    endDate: Date,
    startingPrice: number,    
}
For placing bids, we need a POST endpoint that takes the bid details and returns the created bid:
POST /auctions/:auctionId/bids -> Bid
{
    Bid
}
For viewing auctions, we need a GET endpoint that takes an auctionId and returns the auction and item details:
GET /auctions/:auctionId -> Auction & Item
High-Level Design
1) Users should be able to post an item for auction with a starting price and end date.
First things first, users need a way to start a new auction. They'll do this by POSTing to the /auctions endpoint with the auction details, including information about the item they are selling.
We start by laying out the core components for communicating between the client and our microservices. We add our first service, "Auction Service," which connects to a database that stores the auction and item data outlined in the Core Entities above. This service will handle the reading/viewing of auctions.
Create an Auction
Client Users will interact with the system through the clients website or app. All client requests will be routed to the system's backend through an API Gateway.
API Gateway The API Gateway handles requests from the client, including authentication, rate limiting, and, most importantly, routing to the appropriate service.
Auction Service The Auction Service, at this point, is just a thin wrapper around the database. It takes the auction details from the request, validates them, and stores them in the database.
Database The Database stores tables for auctions and items.
This part of the design is just a basic CRUD application. But let's still be explicit about the data-flow, walking through exactly what happens when a user posts a new auction.
Client sends a POST request to /auctions with the auction details.
API Gateway routes the request to the Auction Service.
Auction Service validates the request and stores the auction and item data in the database.
Database stores the auction and item data in tables.
Note that I don't mention anything about images here. This was intentional; it's not the most interesting part of the problem, so I don't want to waste time on it. In reality, we would store images in blob storage and reference them by URL in our items table. You can call this out in your interview to align on this not being the focus.
2) Users should be able to bid on an item. Where bids are accepted if they are higher than the current highest bid.
Bidding is the most interesting part of this problem, and where we will spend the most time in the interview. We'll start high-level and then dig into details on scale and consistency in our deep dives.
To handle the bidding functionality, we'll introduce a dedicated "Bidding Service" separate from our Auction Service. This new service will:
Validate incoming bids (e.g. check bid amount is higher than current max)
Update the auction with new highest bid
Store bid history in the database
Notify relevant parties of bid updates
We choose to separate bidding into its own service for several key reasons:
Independent Scaling: Bidding traffic is typically much higher volume than auction creation - we expect ~100x more bids than auctions. Having a separate service allows us to scale the bidding infrastructure independently.
Isolation of Concerns: Bidding has its own complex business logic around validation, race conditions, and real-time updates. Keeping it separate helps maintain clean service boundaries.
Performance Optimization: We can optimize the bidding service specifically for high-throughput write operations, while the auction service can be optimized for read-heavy workloads.
Place Bids
In the simple case, when a bid is placed, the following happens:
Client sends a POST request to /auctions/:auctionId/bids with the bid details.
API Gateway routes the request to the Bidding Service.
Bidding Service queries the database for the highest current bid on this auction. It stores the bid in the database with a status of either "accepted" (if the bid is higher than current highest) or "rejected" (if not). The service then returns the bid status to the client.
Database bids are stored in a new bids table, linked to the auction by auctionId.
When I ask this question, many candidates suggest storing just a maxBidPrice field on the auction object instead of maintaining a bids table. While simpler, this violates a core principle of data integrity: avoid destroying historical data.
Overwriting the maximum bid with each update means permanently losing critical information. This makes it impossible to audit the bidding process, investigate disputes, or analyze patterns of behavior. Inevitably, a user is going to complain that their bid was not recorded and that they should have won the auction. Without a complete audit trail, you have no way to prove them wrong.
3) Users should be able to view an auction, including the current highest bid.
Users need to be able to view an auction for two reasons:
They want to learn about the item in case they decide they're interested in buying it.
They want to place a bid, so they need to know the current highest bid that they need to beat.
These two are similar, but have different requirements. The first is a read-only operation. The second requires real-time consistency.
We'll offload the depth of discussion here to our deep dives, but let's outline the basic approach which ensures that the current highest bid is at least reasonably up-to-date.
View Auction
When a user first goes to view an auction, they'll make a GET request to /auctions/:auctionId which will return the relevant auction and item details to be displayed on the page. Great.
What happens next is more interesting. If we never refresh the maximum bid price, then the user will bid based on a stale amount and be confused (and frustrated) when they are told their bid was not accepted. Especially in an auction with a lot of activity, this is a problem. To solve this, we can simply poll for the latest maximum bid price every few seconds. While imperfect, this ensures at least some degree of consistency and reduces the likelihood of a user being told their bid was not accepted when it actually was.
Potential Deep Dives
With the high-level design in place, it's time to go deep. How much you lead the conversation here is a function of your seniority. We'll go into a handful of the deep dives I like to cover when I ask this question but keep in mind, this is not exhaustive.
1) How can we ensure strong consistency for bids?
Ensuring the consistency of bids is the most critical aspect of designing our online auction system. Let's look at an example that shows why proper synchronization is essential.
Pattern: Dealing with Contention
Online auctions are a classic example of the dealing with contention pattern. When multiple users bid on the same auction simultaneously, we face race conditions and need to ensure only one bid wins. This requires careful coordination using techniques like optimistic concurrency control, row locking, or caching strategies to manage competition for the same resource.
Learn This Pattern
Example:
The current highest bid is $10.
User A decides to place a bid of $100.
User B decides to place a bid of $20 shortly after.
Without proper concurrency control, the sequence of operations might unfold as follows:
User A's Read: User A reads the current highest bid, which is $10.
User A's Write: User A writes their bid of $100 to the database. The system accepts this bid because $100 is higher than $10.
User B's Read: User B reads the current highest bid. Due to a delay in data propagation or read consistency issues, they still see the highest bid as $10 instead of $100.
User B's Write: User B writes their bid of $20 to the database. The system accepts this bid because $20 is higher than $10 (the stale value they read earlier).
As a result, both bids are accepted, and the auction now has two users who think they have the highest bid.
A bid of $100 from User A (the actual highest bid).
A bid of $20 from User B (which should have been rejected).
This inconsistency occurs because User B's bid of $20 was accepted based on outdated information. Ideally, User B's bid should have been compared against the updated highest bid of $100 and subsequently rejected.
There is an answer to this question which asserts that strong consistency is actually not necessary. I see this argument periodically from staff candidates. Their argument is that it doesn't matter if we accept both bids. We just need to rectify the client side by later telling User B that a bid came in higher than theirs and they're no longer winning. The reality is, whether User A's or User B's bid came in first is not important (unless they were for the same amount). The end result is the same; User A should win the auction.
This argument is valid and requires careful consideration of client-side rendering and a process that waits for eventual consistency to settle before notifying any users of the ultimate outcome.
While this is an interesting discussion, it largely dodges the complexity of the problem, so most interviewers will still ask that you solve for strong consistency.
Great, we understand the problem, but how do we solve it?

Bad Solution: Row Locking with Bids Query

Good Solution: Cache max bid externally

Great Solution: Cache max bid in database

2) How can we ensure that the system is fault tolerant and durable?
Dropping a bid is a non-starter. Imagine telling a user that they lost an auction because their winning bid was "lost" - that would be catastrophic for trust in the platform. We need to guarantee durability and ensure that all bids are recorded and processed, even in the face of system failures.
The best approach here is to introduce a durable message queue and get bids into it as soon as possible. This offers several benefits:
Durable Storage: When a bid comes in, we immediately write it to the message queue. Even if the entire Bid Service crashes, the bid is safely stored and won't be lost. Think of it like writing your name on a waiting list at a restaurant - even if the host takes a break, your place in line is secured.
Buffering Against Load Spikes: Imagine a popular auction entering its final minutes. We might suddenly get thousands of bids per second - far more than our Bid Service can handle. Without a message queue, we'd have to either:
Drop bids (unacceptable)
Crash under the load (also unacceptable)
Massively over-provision our servers (expensive)
With a message queue, these surge periods become manageable. The queue acts like a buffer, storing bids temporarily until the Bid Service can process them. It's like having an infinitely large waiting room for your bids.
Ordering Within an Auction: Kafka guarantees message ordering within a single partition. By partitioning our topic by auctionId, all bids for the same auction land on the same partition and are processed in the order they were received. This is important for fairness - if two users bid the same amount, we want to ensure the first bid wins.
Fault tolerant system
For implementation, we'll use Kafka as our message queue. While other solutions like RabbitMQ or AWS SQS would work, Kafka is well-suited for our needs because:
High Throughput: Kafka can handle millions of messages per second, perfect for high-volume bidding periods.
Durability: Kafka persists all messages to disk and can be configured for replication, ensuring we never lose a bid.
Partitioning: We can partition our queue by auctionId, ensuring that all bids for the same auction are processed in order while allowing parallel processing of bids for different auctions.
Here's how the flow works:
User submits a bid through our API
API Gateway routes to a producer which immediately writes the bid to Kafka
Kafka acknowledges the write, and we can tell the user their bid was received
The Bid Service consumes the message from Kafka at its own pace
If the bid is valid, it's written to the database
If the Bid Service fails at any point, the bid remains in Kafka and can be retried
While message queues do add some latency (typically 2-10ms under normal conditions), this tradeoff for durability is usually worth it. There are also multiple patterns for maintaining responsive user experiences while using queues, though each comes with different consistency/latency tradeoffs. For fear of going too deep here, we'll leave it at that. But I will discuss bid broadcasting later on when we discuss scale, which solves the asynchronous notification problem.
3) How can we ensure that the system displays the current highest bid in real-time?
Going back to the functional requirement of 'Users should be able to view an auction, including the current highest bid,' or current solution using polling, which has a few key issues:
Too slow: We're updating the highest bid every few seconds, but for a hot auction, this may not be fast enough.
Inefficient: Every client is hitting the database on every request, and in the overwhelming majority of cases, the max bid hasn't changed. This is wasteful.
Pattern: Real-time Updates
Keeping clients updated in real-time about the current highest bid is a perfect example of how to apply the real-time updates pattern.
Learn This Pattern
We now need to expand the solution to satisfy the non-functional requirement of 'The system displays the current highest bid in real-time'.
Here is how we can do it:

Good Solution: Long polling for max bid

Great Solution: Server-Sent Events (SSE)

4) How can we ensure that the system scales to support 10M concurrent auctions?
When it comes to discussing scale, you'll typically want to follow a similar process for every system design question. Working left to right, evaluate each component in your design asking the following questions:
What are the resource requirements at peak? Consider storage, compute, and bandwidth.
Does the current design satisfy the requirement at peak?
If not, how can we scale the component to meet the new requirement?
We can start with some basic throughput assumptions. We have 10M concurrent auctions, and each auction has ~100 bids over its lifetime. If the average auction runs for a week, then we get 10M auctions * 100 bids / 7 days ≈ 140M bids per day. 140M / 100,000 (rounded seconds in day) ≈ 1,400 bids per second. To account for peak traffic (popular auctions ending, evening surges), we should design for roughly 10x this, or about ~15K bids per second at peak.
Message Queue
Let's start with our message queue for handling bids. As discussed earlier, we partition our Kafka topic by auctionId to maintain ordering guarantees per auction. At ~15K requests per second at peak, a modest number of Kafka partitions can handle this throughput comfortably. Partitioning by auctionId also gives us natural parallelism, since different consumer instances can process bids for different auctions concurrently.
Bid Service
Next, we consider both the Bid Service (consumer of the message queue) and Auction Service. As is the case with almost all stateless services, we can horizontally scale these by adding more servers. By enabling auto-scaling, we can ensure that we're always running the right number of servers to handle the current load based on memory or CPU usage.
Database
Let's consider our persistence layer. Starting with storage, we can round up and say each Auction is 1kb. We'll say each Bid is 500 bytes. If the average auction runs for a week, we'd have 10M * 52 = 520M auctions per year. That's 520M * (1kb + (0.5kb * 100 bids per auction)) = 25 TB of storage per year.
That is a decent amount for sure, but nothing crazy. Modern SSDs can handle 100+ TBs of storage. While we'd want to ensure the basics with regards to some hot replication, we're not going to run out of storage any time soon. We'd be wise to shard, but the more pressing constraint is with regards to write throughput.
At ~15K writes per second during peak, we're pushing past what a single well-provisioned Postgres instance can handle. If we want to stick to our current solution for handling consistency, we'll need to shard our database by auction ID so that we can spread the write load across multiple instances. We don't have any worries about scatter-gathers since all reads/writes for a single auction are on the same shard.
SSE
Lastly, we talked about how our SSE solution for broadcasting new bids to users would not scale well. To recap, the problem is that when a new bid comes in, we need to broadcast it to all the clients that are watching that auction. If we have 10M auctions and 100M users, we could have 100M connections. That's a lot of connections and they wont fit on the same server. So we need a way for Bid Service servers to coordinate with one another.
The solution is Pub/Sub. Whether using a technology like Redis Pub/Sub, Kafka, or even a custom solution, we need to broadcast the new bid to all relevant servers so they can push the update to their connected clients. The way this works is simple: when Server A receives a new bid, it publishes that bid to the pub/sub system, essentially putting it on a queue. All other instances of the Bid Service are subscribed to the same pub/sub channel and receive the message. If the bid is for an auction that one of their current client connections is subscribed to, they send that connection the new bid data.
If you want to learn more about Pub/Sub checkout the breakdown of FB Live Comments where I go into more detail.
Scale
Some additional deep dives you might consider
There are a lot of possible directions and expansions to this question. Here are a few of the most popular.
Dynamic auction end times: How would you end an auction dynamically such that it should be ended when an hour has passed since the last bid was placed? For this, there is a simple, imprecise solution that is likely good enough, where you simply update the auction end time on the auction table with each new bid. A cron job can then run periodically to look for auctions that have ended. If the interviewer wants something more precise, you could use a delayed task scheduler: when a new bid arrives, schedule a task to fire one hour later (using something like a database-backed job queue, a Redis sorted set with timestamps, or a service like AWS Step Functions with a Wait state). When the task fires, check if that bid is still the latest. If yes, end the auction.
Purchasing: Send an email to the winner at the end of the auction asking them to pay for the item. If they fail to pay within N minutes/hours/days, go to the next highest bidder.
Bid history: How would you enable a user to see the history of bids for a given auction in real-time? This is basically the same problem as real-time updates for bids, so you can refer back to the solution for that.
What is Expected at Each Level?
Mid-level
This is a more challenging question for a mid-level candidate, and to be honest, I don't typically ask it in mid-level interviews. That said, I'd be looking for a candidate who can create a high-level design and then reasonably respond to inquiries about consistency, scaling, and other non-functional requirements. It's likely I'm driving the conversation here, but I'd be evaluating a candidate's ability to problem-solve, think on their feet, and come up with reasonable solutions despite not having hands-on experience. For example, they may propose the caching solution without understanding the downsides of distributed transactions.
Senior
For senior candidates, I expect that they recognize that consistency and real-time broadcasting on bids are foundational to the problem and that they lead the conversation toward a solution that meets the requirements. They may not go into detail in all places, but they should be able to adequately arrive at a solution for the consistency problem and explain how bids will be kept up to date on the client. While they may not have time to discuss scale in depth, I expect they recognize many of the problems their system introduced.
Staff
For staff engineers, I expect them to demonstrate mastery of the core challenges around consistency and real-time updates while also proactively surfacing additional complex considerations. A strong candidate might, unprompted, discuss how ending auctions presents unique distributed systems challenges. They'd explain that while fixed end times seem straightforward, implementing dynamic endings (where auctions extend after late bids) requires careful orchestration to handle clock drift, concurrent termination attempts, and delayed valid bids. They might propose a dedicated scheduling service using tools like Apache Airflow or a custom queue-based solution to manage auction completions reliably. This kind of unprompted deep dive into adjacent problems—whether it's auction completion, fraud prevention, or system failure handling—demonstrates the technical breadth and leadership thinking expected at the staff level. Ultimately, the most important thing is that they lead the conversation, go deep, and show technical accuracy and expertise.
Test Your Knowledge

Take a quick 15 question quiz to test what you've learned.

Start Quiz

Mark as read

Next: FB Live Comments

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

(343)

Comment
Anonymous
​
Sort By
Popular
Sort By
Mert Akozcan
Top 5%
• 1 year ago

I think using Kafka somewhat contradicts with what you said in the strong consistency discussion. After writing the bid to Kafka, we are telling user that their bid is received. However, we don't know whether that bid is actually valid, and we can only understand this after consuming the bid from Kafka and trying to update the database.

In the end, I think we will have an eventually consistent system and it's not much different than accepting all bids and figuring out which one is the highest asynchronously.

And maybe one more thing: When we go with a Kafka-based approach, we probably won't need OCC, because there will only be one consumer responsible for a given Kafka partition, and since all bids for a given auction are flowing through the same partition, we won't have any race conditions while updating the database with highest bid price.

65

Reply
Y
YawningPlumGiraffe943
• 5 months ago

For your point of not needing OCC, when the bid from Kafka lands on a different instance of the service, serialization is still necessary.

Kafka may send bids to different instances, each instance may process each bid at different latencys which may result in race conditions.

I believe it's still necessary to have locking or OCC.

8

Reply
xiles xiles
Premium
• 4 months ago

My understanding is that we would partition by auctionId in Kafka, therefore the bids should not fall into the premise "bid from Kafka lands on a different instance", and if it does due to a crash it would reprocess in order.
Is there a case you see this happening?
btw, I am really curious to hear Evans opinion on locking/OCC.
Mine is that I would keep OCC as it wont impact the performance (response time), and works as a double protection on this system. And I would defend that I didn't add Message Queue for it as this instead increases the response time.

4

Reply
I
IndirectApricotPuma559
Premium
• 3 months ago

We can't partition kafka by auctionId, as it will lead to 10M partitions which is not suitable for kafka. Instead we partition by hash of the auctionId (hash(auctionId)%N), hence bids for same auction can land on different partitions.

4

Reply
R
RemarkableHarlequinDragonfly196
Premium
• 1 month ago

Partitioning is by hash(auctionId)%N where N is the number of partitions. The result of this is deterministic; the same auctionId with the same N value will always give the same result. So bids for the same auction are always on the same partition. And your selected N will be much smaller than 10M of course.

1

Reply
P
PassingTealCapybara707
Premium
• 1 month ago

Right but we can choose partitioning key as auctionId so all the request for same auction goes to same partition and single server will handle all the request for that auction.
Then request will be handled serially and  transactions wont be required.

0

Reply
R
RoundBrownEgret745
Premium
• 4 months ago

If all instances are within the same consumer group, it won't land on multiple instances. One consumer would be responsible for a bid at a time, hence guaranteeing serializability.

0

Reply
Dawid Kałuża
Premium
• 4 months ago

I think that even tho Kafka does guarantee the ordering, it's based on message timestamp value determined on server side (producer or gateway in the example), since clients can't be trusted there. Due to delays on network between user and system, there can be a case when:

user A starts sending a bid=100$
user B starts sending a bid=120$
system receives the bid from user B, puts it on Kafka with timestamp=1000
system receives the bid from user A, puts it on Kafka with timestamp=1005

In this case, even though user A clicked "submit" button on the app first, their bid will be after the bid from user B. This is why optimistic locking is also required.
Regarding the locking, I think can be simply limited to: UPDATE auctions SET max_bid = :bid WHERE id = :id AND max_bid < :bid and inserting new bid within "read committed" transaction that would be rejected if UPDATE query returned 0 as a number of impacted rows. However, this is rather a cosmetic change.

6

Reply
ash25says
Premium
• 4 months ago

I think even with kafka we are satisfying "no two bids can ever simultaneously be marked as the highest" so it is still strongly consistent

1

Reply
Hikaru
Premium
• 11 months ago

It seems to me there must be some tradeoff for this problem.

If we don't use Kafka (or if we only use Kafka to record bids history, and use a Redis to record highest bids without going to Kafka), there is risk of dropping bids, especially for popular auctions. The the fault tolerant and durable requirement might not be satisfied.

Also, if we only use Redis, Redis will still need to propagate the new data to other replicas, which takes time (especially Redis replicas are deployed in different data centers). Therefore, in the meantime, some read requests will still get stale highest bid sometimes if they read from those read replicas. Unless we force all read requests to go to the leader node, which breaks our scalability requirement.

What do you think? Any idea how to solve the issue?

1

Reply
Luke Li
Premium
• 17 minutes ago

OCC is still needed as a safe guard as Kafka may "rebalance" consumers in the same group if new consumers are added or removed.

0

Reply
Y
YeastyMoccasinHyena669
Premium
• 1 month ago

Kafka somewhat contradicts with what you said in the strong consistency discussion

+1

When we go with a Kafka-based approach, we probably won't need OCC

I would keep Kafka and OCC separate decision. You can use Kafka today and switch to Kinesis or SQS. Even if you stay in kafka, I remember partition increase can cause temporary chaos.

0

Reply
Dolly Singh
Premium
• 8 months ago

Thats correct that this is not Stongly consistent, but i beleive this is Sequentially consistent meaning relaxed and preserving predictable behavior.
Link: https://hazelcast.com/blog/navigating-consistency-in-distributed-systems-choosing-the-right-trade-offs/
Evan's thought would be helpful.

0

Reply
L
LogicalAmethystToad166
Top 5%
• 11 months ago

This is a valid point actually.. I would be interested in hearing what Evan has to say here as it may help many readers. Thank you!

0

Reply
T
ThoughtfulEmeraldPheasant808
Top 10%
• 1 year ago

This solution does not address synchronous responses to the user when they submit a bid. If we put bids in Kafka they will be processed at their own pace and the response to the user ( if their bid is the winning bid or not) will most likely be not in in the same session making it a bad user experience. I think a better solution is to have an in memory hash table for the highest bid on the bid service in the critical path and then write the bid to Kafka (for record keeping). The user should respond to the user only after writing to Kafka so we do not lose any bids in case the service goes down.

19

Reply

Evan King

Admin
• 1 year ago

We have an open SSE connection to the user! We're broadcasting all incoming bids to connected clients. We can also ensure we broadcast rejected bids back to the creator. Then the client can update accordingly.

9

Reply
T
ThoughtfulEmeraldPheasant808
Top 10%
• 1 year ago

This will still make this asynchronous. When they are placing the bid that is not over SSE so it will not be in the same session. My understanding is that SSE is for checking the highest bid which is an independent operation. I think the user should be informed in the same session when they place the bid.

9

Reply

Evan King

Admin
• 1 year ago

Correct, this is asynchronous, technically. But the user should be none the wiser. See the comment about latency added by a message queue in the callout above. We can still show a "processing bid" message and then a result. While it was asynchronous, to the user, it felt like a synchronous response to their action.

You can response synchronously, you're just losing the message queue, so need another option for ordering, scaling, and durability that it offers.

25

Reply
W
WoodenAquamarineSnipe931
Top 10%
• 1 year ago

So a queue effectively is the last resort within the context of this problem. I read in another question breakdown (can’t recall which one at the moment) that queues usually mask performance problems of your service; is there a principle or criteria that you use to decide when it is okay to use a queue as a tradeoff?

2

Reply

Evan King

Admin
• 11 months ago

Yah, generally it depends on the priority on fault tolerance. If dropping a request is tolerable (like adding a like, if it fails, we can tell the client to try again), then the message queue may not be a good idea. On the other hand, for financial systems where fault tolerance is critical (we can't drop a bid!) then it's worth the trade off.

14

Reply
J
JollyYellowGrouse728
Premium
• 11 months ago

Isn't the result of not being able to write to Kafka the same as not being able to write to a database in this case?

If we accept the request but cannot write to Kafka because of a hardware fault on our server, we will have still dropped the bid and expect the client to retry. I don't understand why that's fundamentally different than failing to write it to our database with the exception that there's a smaller probability of that happening.

15

Reply
Garvit Chugh
Premium
• 10 months ago

Accepting a bid ideally means that the write operation to kafka succeeded. Think of the POST API call we are making to write post a bid. The response will be 200 OK only when the bid gets written onto kafka. If it fails before that, then we would return proper error via that API itself to the client and they can retry if they wish to.
This is different from failing while writing to the DB because once a bid is accepted, it is the system's responsibility to persist it and have high fault tolerance. Now, if anything goes wrong after accepting the bid(i.e, writing to kafka), we need to have a way to be able to retain that bid which is where kafka becomes important. It helps with two things - one is to retain the bid well, the other is that will have it in the order it was supposed to be and provides capability to replay the bids in that order.

3

Reply
udit agrawal
Top 10%
• 9 months ago

I have query on the ordering part, though we have queue partitioned by the auctionId but there are multiplt Bid Service instances running, so IMO this order would have been maintained if there was a single Bid Service instance but with multiple consumers how we are managing the ordering or are we saying all the Bid Service instances are part of a consumer group where only one of the instances will read the bid for a particular auction?

5

Reply
Y
YeastyMoccasinHyena669
Premium
• 1 month ago
• edited 1 month ago

It's fine to call bid API and get a 5xx or 4xx. However, it's not fine to get 200 but the bid failed in the background. For example, I try to send 5 dollar on Venmo and Venmo crashed, it's good. But Venmo should not tell me send successful but crash internally later.

IMO, the message queue amplifies the chance of "responding 200 then crash silently". I would rather shard the database to try to achieve over 100k bid TPS. I would also rather relax the latency requirement (2-3 seconds bid api call should be fine) to trade better consistency cx.

Another issue with Kafka is - user lost visibility of the bid request between bid submission and bid written to postgres. All the Async system that I have worked on provides a get API (immediately) to fetch request status after submission. While Kafka delivery can be super fast - I would not say this is a robust system.

3

Reply
W
WoodenAquamarineSnipe931
Top 10%
• 11 months ago

Ah. That makes sense. Thanks!

0

Reply
Garvit Chugh
Premium
• 10 months ago

The operation would be async in only the literal sense. If you think about most of the online auction or bidding systems, they have a separate tab where you can view your bids, that is what this will support. The idea being that once you write it to kafka, assuming it gets written onto the DB and gets communicated to your client via the SSE, the  client knows your userID and can easily handle the responsibility to segregate that bid from the others. So, once you place a bid, you get a sync response in the same session, which says Bid initiated. And then you can head over to the My Bids section and see the response. Kafka scales extremely well with such a small throughput and you should get the result of your bid to your client in virtually no time and then you could place another bid. This would seem real time when thought of from the perspective of human perception. And that is very important in this system because it will only be the human (user) of the app who will initiate the bid again.

3

Reply
Alfred Gui
• 1 year ago

The bid qps is just 10k per sec, so we don't need further optimizations to the architecture in this article. But if the throughput is unrealistically high (like 1 billion per sec), we will need more extensive caching of the highest bid, including the bid cache on each bid server. Early rejections could reduce downstream load. (We will still need to push all bids to the message queue for book keeping, but that's not the critical path).

8

Reply
F
FancyTanGoldfish347
Premium
• 11 months ago

With 1 billion bids per second that means we are assuming 100 trillion concurrent auctions at peak time. Sure this is an interesting though experiment but this seems very unrealistic.

0

Reply
Neeraj jain
Top 5%
• 11 months ago

What are you planning to reject even if your bid is not the winning bid you need to store the bid entry into the DB right ?

0

Reply
E
ElectricRedOwl923
• 1 year ago

why not just maintain a in-memory copy of maxPrice? this way we do not need to hit distant redis or database

0

Reply
W
WorthyApricotHarrier535
• 1 year ago

Bid Service is horizontally scaled and each instance will have it's own maxPrice in memore for a given auction

4

Reply
C
CloudyGrayAnt409
• 1 year ago

In some other guides you've mentioned how we don't want to lock the database row because if the service locking it goes down, we'll be stuck in that state. Instead it was recommended to use a distributed cache like Redis that allows for TTL. Is this not a concern here? Or did you not consider it mainly because OCC was a possibility in this case.

Another thought - do we need to update the bid in a transaction? We could make the write to the bid DB async possibly using the same queue as the SSE queue. It might add some delay for the bid to reach the bids DB but I don't think we care about what's in the bids DB since we're not using it to read.

9

Reply
S
sherry-dash-shower
Premium
• 19 days ago

In some other guides you've mentioned how we don't want to lock the database row because if the service locking it goes down, we'll be stuck in that state. Instead it was recommended to use a distributed cache like Redis that allows for TTL. Is this not a concern here?

Postgres releases most locks (including row locks discussed here, but not advisory locks) held by a session once it terminates. There is some amount of lag between losing connection and postgres realizing it (handled by various ttl settings).

0

Reply
Priyankar Raj gupta
Premium
• 8 months ago

Not able to understand how concurrency control is needed when later we introduced the queue for sequential processing?

8

Reply

3 replies hidden which refer to old versions of the article. Expand them.

Ruizhen Mai
Premium
• 1 year ago

I'm not sure if others mentioned this. But if we have an ordered messages within each auctionId (partition key), we shouldn't need row lock since we're always updating with the highest price?

on BidService / BidProducer, we always send the message, let frontend guards bids < highestBid, this has latency, no problem
on BidConsumer, we update the highestBid = bidPrice (in auction table) iff bidPrice > highest bid; this is not concurrent in terms of auctionId bc of ordered messages is partitioned by auctionId
notify users on bid's success/failure based on the condition check on step2

8

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

1) Users should be able to post an item for auction with a starting price and end date.

2) Users should be able to bid on an item. Where bids are accepted if they are higher than the current highest bid.

3) Users should be able to view an auction, including the current highest bid.

Potential Deep Dives

1) How can we ensure strong consistency for bids?

2) How can we ensure that the system is fault tolerant and durable?

3) How can we ensure that the system displays the current highest bid in real-time?

4) How can we ensure that the system scales to support 10M concurrent auctions?

Some additional deep dives you might consider

What is Expected at Each Level?

Mid-level

Senior

Staff
