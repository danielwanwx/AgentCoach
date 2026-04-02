# Robinhood

> Source: https://www.hellointerview.com/learn/system-design/problem-breakdowns/robinhood
> Scraped: 2026-03-30



​
Sort By
Popular
Sort By
C
ConfidentialCrimsonFlamingo719
Top 5%
• 1 year ago

Great write up!

I don't really think you need the External Order Metadata DB. Most good external apis offer you a metadata field where you can pass in whatever you want, and they will return it to you in their webhooks. In this case, we can pass in a userId and orderId when we create an order from the exchange. When those webhooks come in, we receive back those ids and can look up our order directly in our Orders DB.

I would think most senior and all staff level folks have experience with this metadata field in apis that offer webhooks.

75

Reply
E
ElegantMoccasinSwan892
Premium
• 1 year ago

+1 I was about to write the same comment :)

Just something to consider — passing "internal" userId or orderId to third-party systems (like the Exchange) might not align with a company's security or privacy policy. I think a safer approach could be using indexable columns such as an externalUserId or externalOrderId that can be shared with third-party systems.

15

Reply
udit agrawal
Top 10%
• 9 months ago

can we not use redis instead of rocksdb, as redis is also a KV store and we need this mapping as long as order is not filled(success/failed) or till the time market closes, whichever happens first.

1

Reply
V
VerticalBlackFlea403
Premium
• 8 months ago

Redis can crash before the order is filled. besides, if it's limit order, it may not be filled for days

3

Reply
udit agrawal
Top 10%
• 7 months ago

That can be handled with high availability redis sentinal used in cluster setup.

1

Reply
Shantanu Pimprikar
Premium
• 4 months ago

But Redis' capacity is limited by RAM, while RocksDB's capacity can scale with disk, RocksDB is cheap and durable by default.

0

Reply
E
ExtensiveGoldOrangutan373
Premium
• 3 months ago

RocksDB is embedded DB, how are order service and tradeprocessor updating it, it can only be accessed by owning service. Also, if service crash, how will they recover rocksDB data. Is it stateful service using external disk mount points ?

5

Reply
umamahesh bodanapu
Premium
• 2 months ago

+1

0

Reply
Y
YeastyMoccasinHyena669
Premium
• 1 month ago

It's important to mention - you should never trust Robinhood when you pass orderID to them. There is a chance that they mutate your orderID during callback. You can either encrypt or sign the metadata and validate the callback md when continue processing

0

Reply
G
GlobalPinkLadybug365
Top 5%
• 1 year ago

+1

0

Reply
G
GiganticApricotSwordfish902
Top 5%
• 1 year ago

regarding the Good solution vs. Great solution with the Order Dispatch service and Order Gateway, I don't understand what the difference is? To me it seems the only difference is having a queue in between them.

41

Reply
A
AdvancedJadeJaguar381
• 4 months ago

I asked the Tutor here to clarify and this explanation from Tutor helped me a lot when I asked to explain the purpose of order service vs order dispatcher NAT gateway (outside the IP requirements).

The key difference is ownership. The order service owns user facing order lifecycle and truth, while the dispatcher owns exchange facing delivery and resilience.

Order service logic includes request auth, balance and risk checks, validating symbols and order types, reserving funds, creating the order row, managing state transitions like pending and submitted, idempotency of client requests, and audit logging. It should expose a clean API, keep the database consistent, and tell the user what happened.

Dispatcher logic focuses on getting orders to the exchange safely and fast. It handles per exchange rate limits, pacing and concurrency, retries with backoff, circuit breaking, mapping internal fields to exchange specific formats, deduping with client order ids, and partial failure handling. It can also do batching if the venue supports it and centralize telemetry for exchange calls.

Default approach. Keep exchange logic in the order service if you have one exchange and one caller. Split out a dispatcher when you have many internal producers, multiple exchanges, or you need tight centralized control of rate limits and retries across the fleet.

Show More

2

Reply
A
AdvancedJadeJaguar381
• 4 months ago

HelloInterview - it would be great if you can update the above explanation with more rationale if you agree with this response from the Tutor.

0

Reply
F
FastJadeGrouse442
• 1 year ago

I think the NAT gateway proxies the Order Service’s network requests to ensure all outgoing requests share the same IP address.

1

Reply
Magic Potato
• 1 year ago

Does sending requests from small set of IPs ensure we can handle high scale ?

2

Reply

Stefan Mai

Admin
• 1 year ago

The intent is less to ensure scale and more to ensure security. Financial systems frequently manage access via allowlists/whitelists (e.g. our bank requires a set of IPs to submit ACH transfers for our mock interview coaches).

21

Reply
E
ExcessBlackAardvark647
Top 5%
• 1 year ago

so the order gateway doesn't actually resolve order queue's problems and it also loses the benefits brought by the queue. the only benefit the "great solution" is hiding clients' real ip behind a "fake" one, right? if so, I don;t quite get why this is a great solution. if the requests have to be sent from an allowlisted IPs, then the "good solution" should not be called "good" as it is not working. but if there is no such requirement from the bank, then the so-called "great solution" doesn't look like "great" to me.
But PLEASE let me know if I understand the flow incorrectly and explain it more. Thanks!

42

Reply
Anirudh Kaki
• 1 year ago

The intent is to avoid queues between OrderService and OrderDispatcher to prevent delays. Direct communication ensures immediate order processing, allowing quick responses to market changes and instant order modifications.

5

Reply
nikhil singh
• 1 year ago

"Then how does the OrderDispatcher Gateway prevents the dispatch service from being overloaded" -> the post mentions that "we might make the auto-scaling criterion for this service quite sensitive (e.g. auto-scale when average 50% CPU usage is hit across the fleet) or we might over-provision this service to absorb trading spikes"

9

Reply
J
jokerchendi
Premium
• 1 year ago

Exactly!

A key architecture decision here is: if low latency is top priority, there's no point using a queue.

Think about it. If we add a queue in between, to ensure low latency, we must always keep the number of unprocessed messages in the queue low (close to zero). So, why use a queue in the first place?

8

Reply
Katie McCorkell
Top 10%
• 1 year ago

thank you guys for this discussion, I had all the same questions. very useful. I think the writing in that part of this blog is unclear.

17

Reply
M
MathematicalLimePuffin340
Premium
• 11 months ago

Not using a queue is trading off Reliability for lower latency. What if Exchange is down and orders have to be processed? What if Order Dispatch Gateway goes down?
From a usability standpoint, the enqueue + dequeue adds 100ms which seems a reasonable wait time if it adds reliability for stock transaction.

I would argue that we choose Reliabilty over Latency for Order Execution and prioritize latency for receiving stock price update information

19

Reply
Mike Choi
Top 5%
• 10 months ago

I think this a good discussion point in the interviews. However - if the exchange itself goes down, I think there are much larger problems at hand :) This will cause potentially millions in losses for the exchange. It also might not make sense to queue up these while the exchange is down since that will cause a huge build-up of orders (potentially causing an even longer latency).

The argument here for the queue may be to allow the user to fire and order and forget, which could be a valid point (since a lot of these brokerages allow you to schedule orders).

4

E
ExcessBlackAardvark647
Top 5%
• 1 year ago

Thanks for the reply.  Then how does the OrderDispatcher Gateway prevents the dispatch service from being overloaded, and what should be the metric to indicate the dispatch service to elastically scale off(these are the benefits brought by the queue)?

5

Reply
nikhil singh
• 1 year ago

We use queue instead of over provisioning of services because of cost factor as over provisioning of services is expensive but if the latency requirement is extremely low, then, over provisioning is a good idea rather than using queue

2

Reply
R
RepresentativeLimeHarrier694
Top 10%
• 1 year ago

true that, I believe queues are great when you want to avoid any load bringing down your infrastructure and also not wanting to lose any incoming requests. in this system design, as long as u scale ur own structure as a conduit of trade placement, the actual load is someone else's problem (i.e. exchange)

1

Reply
WH L
Premium
• 9 months ago

you didn't mention any security issue for your elastic ip solution.

0

Reply
Vankshu Bansal
Top 10%
• 7 months ago

Here's my understanding:

Good solution:
Pros-Durability, scalability, and fault tolerance
Cons-High latency during bursts of traffic and multiple connections from broker to exchange

Great solution:
Pros-Low latency and less connections from broker to exchange (NAT)
Cons-Increased cost due to lower scale-up thresholds, and no durability and fault tolerance

Why not mix both the solutions? ;) What's the harm?

0

Reply
CF
Cyan Fish
Top 5%
• 6 months ago

@evan, would be great if you can make a video for this one

40

Reply
U
uky
Premium
• 5 months ago

second on this. Pleaseeee

1

Reply
Y
YammeringTealBovid101
Top 10%
• 1 year ago

Wondering why to add a RocksDB instead of add index on externalOrderId in the Order DB? With 2 DBs, extra complexity is added to handle data consistency.

Or maybe this is a typo? The article mentions "externalTradeId", wondering whether it's the same thing with External Order ID or not? If we think about order partially filled case. it makes more sense to me that, 1 order can have 1 external order ID, but multiple external trade IDs. So we need a Trade table to store the trade IDs to order Id maping. But still, 1 DB with multiple tables seems enough here. Especially if we want to maintain the orderID and tradeID relation.

24

Reply
P
pssharma1699
• 1 year ago

I think externalTradeId and externalOrderId are the same. The main reason why we are using rocksDB is we cannot have index on externalTradeId as the data would be partitioned based on userId and we might have to go through all shards before we can update db.
Not sure if index work across shards.

4

Reply
O
OkIndigoTiger161
• 1 year ago

Even the database is partitioned based on the userId, we can have a GSI on the externalOrderId

7

Reply
B
BiologicalMoccasinTahr305
• 1 year ago

GSIs are in DynamoDB not postgres. You'd either create a new table within postgres and shard that by externalOrderId OR you'd use a separate db like the blog post does

5

Reply
C
ControlledTealParakeet247
Premium
• 9 months ago

THis is the real problem that not many databases support global secondary indexes.
the index that you create from external order id to order-id when partitioned by user-id will not have any global presence. which means you would have to query all the shards. Hence use an external store to simulate the GSI.

0

Reply
hardcorg
Top 10%
• 7 months ago

My take: Pick a distributed durable storage layer that supports cross-table/cross-partition propagation.

I would caution against maintaining fault tolerance in updating two distinct databases.

Consider this: the order is submitted to the exchange, the order db is updated, but the host process before rocksdb is updated.

You would need some persisted WAL for the process to come back up and restore state.

Or the more extreme case: The host dies and you need to provision a new one. RocksDB is local and embedded. You'd need to use something like TiKV to have fault tolerance. Otherwise, the rocksdb data is gone for good.

0

Reply
F
FastIvoryMink623
• 1 year ago

We have similar situation at work and but the external system will accept our custom key and response to us with that key, our key is "ourteamID_orderid_userid" so we just need to parse the key to get all these information.

6

Reply
R
RepresentativeLimeHarrier694
Top 10%
• 1 year ago

why rocksdb and why not redis?

4

Reply
P
pssharma1699
• 1 year ago

Dont think there is a hard rule to use rocks DB, some properties should be

persistent
fast Redis with persistent config should work imo.

2

Reply
R
RepresentativeLimeHarrier694
Top 10%
• 1 year ago

I don't know if we need persistent. it only needs to be saved until the trade is settled

1

Reply
Hello Interview
• 11 months ago

yes i also tthink so , since its embedded no extra network call , but how is the initial mapping getting created for an orderId -> externalOrderId , we wont have the external orderId unless we send it to exchange or rather exchange responds back with it

0

Reply
C
ConventionalTanBug802
Premium
• 6 months ago

Order submission is sequential. You already have the order ID before submitting to the exchange.

0

Reply
R
RunningVioletAphid451
Premium
• 10 months ago

Yes, i think in postgres. partition by user id might still work with index on externalOrderId. But sharding by user id will make index on externalOrderId not that efficient.

0

Reply
P
ProspectiveCoffeeRhinoceros457
Premium
• 8 months ago

But if you are building an index on externalOrderId, that doesn't necessarily help you that much, as you have to still query potentially all Postgres write shards (because the corresponding order could be in any of them) if I understand correctly

0

Reply
S
socialguy
Top 5%
• 1 year ago

The gateway avoids the delay of having a queue, but it doesn't alleviate the excessive communication problem. I don't know if the IP thing is important, because the services would run in a VPC with a limited number of IPs. But I'm no AWS networking expert, so, not sure about that. In order to truly reduce the number of calls, the orders will have to be batched; this is mentioned in additional deep dives. But then we're back to the delay similar to the queue, so, this writeup never really addresses the NFR #4.

Why not just create a unique index on external order id instead of introducing a KV store?

9

Reply
I
ian.ornstein
Premium
• 1 year ago

Regarding the unique index on external order id:

Adding a secondary index was my original thought. I think the important thing is to make sure you are able to discuss tradeoffs of each approach.

Some drawbacks of adding a secondary index is that every new index slows down writes. We already have a delay of responding to the user via purchases because we have write one to our order DB, write 2 to the exchange itself, then write 3 to the order DB. Adding a local index slows down the final write. The other approach allows a 4th write to the key-value database to happen in parallel with this final write, so it speeds up this process a bit.

In addition, now when we get an update, we receive external order Id and we get to look it up in the DB. Your approach is fine if we have a single node, since the local secondary index secondary on external order id lets us look it up lightening fast.

But if our database is horizontally scaled this becomes a problem. Because now we have to either a) check every shard for the presence of the external order id or b) have to use a global secondary index (which now means all writes have to go to at least two nodes, using two phase commit to ensure they both update, which will definitely slow down the writes)

Then again, will the Orders DB ever need to scale horizontally?

20M users * 5 trades/day *365trades/year ~ 36B orders a year. in 3 years we get 100B orders.
what is the size of each order?
orderId - 8bytes
userId - 4bytes
externalOrderId - 8bytes
symbol - 1byte
shares - 4 bytes
price - 4 bytes
state - 1 byte
... more data timestamps, etc? - 20bytes
so a total of around 50bytes per order
5000B = 1 TB every 3 years.

This is definitely manageable for a single large db node, so we wouldn't have to scale.

The other drawback of the unique secondary index on external order id is that your DB has to support it being null for the first write. Which postgres does allow, so that is fine.

Show More

7

Reply
Mike Choi
Top 5%
• 10 months ago

Just to clarify, RDMBS doesnt use a GSI or LSI - thats for NoSQL DBs.

The addition of a nonclustered index on the ordersDB for the externalOrderID will likely be fine in practice (typically issues with indexing comes from a huge number of indexes and the amount of data).

Depending on how many rows in the table, partitioning may be a better option since all of the data will live on the same node, and honestly, sharding a RDBMS comes with its own set of challenges (managing cross-node transactions, 2 phase commits, etc).

As some other people mentioned, its entirely possible to pass in metadata to a webhook such that when the Exchange makes a request through the webhook, it can return the metadata key back so we dont necessarily need the second database.

4

Reply
D
djmo0000
Premium
• 10 months ago

Since the data records for orders are pretty narrow, in an RDBMS, your index can often already contain all the fields you need for your query. You can always add additional small fields to your index to never have to go to the table. The downsides are (1) less records get pulled into memory when a block of the index is retrieved and (2) updates to those added fields will require changes to the index. An example is updating a status field we don't need in the index, but we want the index to span our query pattern. But if the status field is the last field in the index, changing the value likely won't actually change the sort order.

If it actually changes sort order, it would likely be to a location in the same block of the index already in memory, making the update really fast. You might just be changing the value in a single location of that block while impacting nothing around it.

0

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Understanding the Problem

Background: Financial Markets

Functional Requirements

Non-Functional Requirements

The Set Up

Planning the Approach

Defining the Core Entities

The API

High-Level Design

1) Users can see live prices of stocks

2) Users can manage orders for stocks

Potential Deep Dives

1) How can the system scale up live price updates?

2) How does the system track order updates?

3) How does the system manage order consistency?

Some additional deep dives you might consider

What is Expected at Each Level?

Mid-level

Senior

Staff+

