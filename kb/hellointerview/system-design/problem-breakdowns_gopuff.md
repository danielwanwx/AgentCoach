# Local Delivery Service

> Source: https://www.hellointerview.com/learn/system-design/problem-breakdowns/gopuff
> Scraped: 2026-03-30



​
Sort By
Popular
Sort By
Aleksey Klintsevich
Top 5%
• 2 years ago

I think it might be worth it to mention the Saga pattern, when you're ordering the items, as a possible solution

61

Reply
A
ApparentTomatoOx647
Top 10%
• 1 year ago

+1
We can utilize Change Data Capture (CDC) or Outbox pattern on the Order table using pglogical, allowing us to track changes in order status (Ordered, Confirmed, or Failed). By adding the Order table to a replication set via pglogical.replication_set_add_table, we can capture and process these updates in near real time.

When a new order is placed, it is initially recorded with the status "Ordered". These changes can be then streamed by Postgres trigger + separate Kafka producer to a Kafka message broker, where a consumer group of worker processes listens for updates. Each worker independently processes incoming order events and attempts to update the Inventory table, ensuring consistency through row-level locking (fine-grained locking).

If a worker successfully deducts the required quantities from inventory, the order status is updated to "Confirmed". If the inventory update fails due to insufficient stock, the order is marked as "Failed" (reconciliation step), and the customer is notified.

Although customers must wait briefly for their order status to be confirmed, this event-driven architecture greatly enhances scalability by decoupling the Order and Inventory systems. This means that both databases can reside on separate hosts, reducing contention and improving overall system performance while it increases the system complexity.

Show More

28

Reply
slrparser
Top 5%
• 9 months ago

It feels very overengineered to me, tbh.

59

Reply
udit agrawal
Top 10%
• 8 months ago

With the intention to partition inventory table by region_id, it makes sense to keep order table in a separate database maybe sharded by userid(to fetch all the orders of a user), above event driven architecture makes much more sense.

0

Reply
Max
• 10 months ago

I think it's very redundant to add CDC with Kafka, Kafka Connect to reduce transaction by this: "quantity =  quantity - 1".

10

Reply
Nguyen Tran Trung
• 3 months ago

Yes agreed. The most important part is the compensation flow. You would Saga: 1) ReserveOrder(itemId, dcId, amount) on the Inventory table and 2) INSERT INTO orders.
If the first step fails then great. If second step fails, in case the service is alive, we can RPC ReturnOrder(itemId, dcId, amount) (this API must be idempotent, we will discuss right later). Harder stuff is when the Saga coordinator (Order Service) crashes during INSERT or during compensation, then we never calls ReturnOrder. A good approach here is we can run scheduler service periodically to compensate failed orders. Since we failed the INSERT, we never knew which failed, so let's refactor the order flow by 1) INSERT INTO orders (state, expires) VALUES (InProgress, 1 hours); 2) the second Saga step be UPDATE orders SET state = Success. Then we can always know which order is expired and stuck in InProgress to compensate (CREATE INDEX idx_orders_state (expires, state) and run this query in read-only slave to speed things up).

To make ReturnOrder idempotent - simply have a "compensated_reservation" table (orderId, amount) and check if the compensation is completed before adding amount to the items table during a transaction. This table can be vacuumed periodically during off hours (it's very small!)

This design allows decoupling orders and items/inventory table and shard them freely.

This is what I could came up with, any suggestions/simplification?

Show More

2

Reply
N
NecessaryMoccasinEchidna420
Top 5%
• 1 year ago

The whole inventory reservation thing feels more like an engineers' solution than a business goals solution.

Of course if the interviewer says you must never ever let someone place an order if you aren't 100% sure that you have stock, that's fine. Do it.

But if you're at a senior+ level and expected to show some business thinking beyond technical implementation and come up with that as one of the most important above-the-line requirements on your own... is it really? What business goal are we fulfilling?

The business goal is to get people to spend money.

If you block them from checking out with 20 other items because a bag of chips in their cart went out of stock before they hit the "Place Order" button... if a 100ms latency increase on Amazon triggers a 1% drop in sales, what's the drop going to be for refusing to accept the order? The business will see the analytics funnel and tell you to remove this feature immediately.

The real-world business solution on these apps for items which might be out stock, but we don't know because of concurrency and also just-in-time supply chains is to give the customer a choice of substitution (preferable!) or refund for that one item.

Show More

38

Reply
N
NecessaryMoccasinEchidna420
Top 5%
• 1 year ago

Good Solution: Use Redis to "lock" items
Great Solution: Use a new status flag

Isn't this basically identical to the Ticketmaster ticket inventory solution, where the DB-based status lock with cron-process to release locks was considered sub-optimal and the Redis-based lock with TTL was considered "great"?

One last comment: this solution looks a lot more like a hotel reservation system than a grocery app, to be honest.

Although in real-life hotels and airlines allow overbooking, as business-wise to be "optimistic" and sell as much inventory as possible and disappoint some customers.

8

Reply
C
ChemicalCopperIguana997
Top 10%
• 10 months ago

In grocery apps, most SKUs are mass-quantity items, so the chance of inventory going to zero between "add to cart" and "checkout" is low. Retailers accept the small trade-off of occasional stock-outs at checkout in exchange for system simplicity and performance. Fulfillment can often be adjusted using substitution logic (e.g., offering a different brand of milk if one is unavailable), which keeps the customer experience smooth.

In contrast, systems like Ticketmaster or hotel booking platforms deal with scarce, uniquely identifiable resources (e.g., a specific concert seat or hotel room). In these cases, losing a booking due to concurrency issues is unacceptable to users. That's why these systems require strict lock management, race condition prevention, and mechanisms like Redis-based locks with TTL or DB row locking to ensure fairness and consistency.

25

Reply
Neethi Elizabeth Joseph
• 1 year ago

I wanted to ask about the same thing: TicketMaster vs GoPuff
The Distributed Lock is not considered great here.
I think leveraging the powers of the RDBMS is being prioritized here and we are leaning further into using RDBMS. I hope interviewers accept it.

4

Reply
Kevin Blast
• 1 year ago

I think the difference is the ticketMaster locks down an unique resource (a ticket with unique seat) vs the inventory is a shared resource. Locking the inventory item isn't appropriate.

5

Reply
Abhishek Agrawal
• 1 year ago

but we could be locking inventoryInstance. so yes, would be great to understand why Redis based lock with TTL is not great here.

1

Reply
I
InstitutionalPurpleMollusk746
• 1 year ago

I have same question here.. why is redis lock solution not considered a great solution here? Hope Stefan sees these comments and reply the reasoning.

1

Reply
I
InstitutionalPurpleMollusk746
• 1 year ago

Unlike Ticketmaster, when a user places an item for reservation in this application, they are more likely to complete the order rather than abandon the cart, since grocery items are typically needed sooner and the amount of money involved is smaller compared to ticket purchases. Therefore, periodic jobs to clean up the database for items with a 'reserved' status, allowing for some lag, are not a significant issue.

Additionally, unlike the singular quantity of a specific seat in Ticketmaster, this application usually deals with multiple quantities of item instances. As a result, if the count of item instances isn’t perfectly accurate (e.g., 9 instead of 10), it won’t matter as much to the user as long as there is more than 1 in stock. In contrast, for Ticketmaster, it's a binary situation where the seat is either available (1) or not (0).

Considering these trade-offs and the cost of maintaining Redis, I believe the second approach is better in this case.

Hope my reasoning makes sense!

3

Reply
Tommy Loalbo
• 1 year ago

I see your point about multiple in the inventory but potentially seeing something is out of or on hold by someone else or just lower in stock because of that could increase the scarcity effect and potentially drive up sales. I feel like it depends on the analytics.

0

Reply
E
EasyCopperOtter704
Premium
• 11 months ago

I had the same question. Maybe it is because inventory is usually not low (near zero) most of the time? You do not want double bookings, but it does not make sense to reserve items as your inventory is not low. Contrast that to the Ticketmaster problem where each event has only a few hundred tickets, and many people tend to book the same seats that they consider "best"

0

Reply
A
AliveJadeAntelope452
• 1 year ago

I was going to say the same thing about the similarities between this and hotel booking systems. Based on my understanding, they are roughly 90% the same, with only a few key differences:
1.Date Range: A hotel system query will always include a date range. Ensuring inventory item availability within a date range requires adjustments to the design. The inventory table will differ. Instead of handling multiple items per order, we primarily deal with one item per order, but with an associated date range. A significant challenge is maintaining consistent room availability throughout the booked dates (i.e., preventing users from changing rooms during their stay).
2. Location/nearby service requirements is different. Hotel booking systems typically involve searching for remote locations, often by location name, rather than using the user's current lat/lng coordinates. Determining the correct location presents a unique challenge. However, we don't need to consider how current traffic impacts commute time.
3.Traffic and Concurrency: Hotel booking systems often exhibit much higher spike ratios. Traffic can surge significantly near vacation seasons. High concurrency is also common for "hot items" (certain hotels on specific dates). This may necessitate infrastructure changes to handle the increased demand, such as implementing booking queues.

Show More

3

Reply

Stefan Mai

Admin
• 1 year ago

Ha, this is a fair point. Most interviews are going to be synthetic in nature, you only have 1 hour after all. But if you were designing this in the real world you're right, you'd probably want to design some partial checkout functionality.

3

Reply
N
NecessaryMoccasinEchidna420
Top 5%
• 1 year ago

Yep, that makes sense. Tbh, if I were an interviewer and someone used this prompt as an opportunity to show how they would design a real-time inventory system, it's probably fine.

But as someone who has a Meta interview coming up in a couple of weeks for E6, this blog post makes me mildly anxious wondering if an interviewer who asks this particular question would ding me because I only designed a "best effort" stock system and prioritized other goals

1

Reply

Stefan Mai

Admin
• 1 year ago

System design questions don't have 1 right answer: the important piece is you being able to demonstrate that you can think on your feet, use your body of experience to make tradeoffs, and creatively build a solution.

This question isn't appropriate for an E6 interview, FWIW. Keep in mind that for E6 you'll want to go deeper than most of the guides on this site cover.

1

Reply

Stefan Mai

Admin
• 1 year ago

We'll have to work on that next. Much smaller audience!

4

Reply
N
NecessaryMoccasinEchidna420
Top 5%
• 1 year ago

True, but then most prep material is focused at a lower level, it's very hard to find good examples of staff-level system design that's also digestible as a refresher within a limited time window! I haven't interviewed in 5 years at this point. I read through DDIA and some of its references to get a bit more depth. Still feel pretty unprepared though.

2

Reply
L
LooseCopperConstrictor421
• 1 year ago

I think best effort solution makes sense here because of the delivery constraint of 1 hour. Had it been like amazon where its a matter of couple of days or a week in some cases, overbooking makes sense.

0

Reply
N
NecessaryMoccasinEchidna420
Top 5%
• 1 year ago

Also am I reading the design correctly that we have a ItemInstance row in the database for each individual item? If we have 1 million packs of gum in inventory we have 1 million rows?

0

Reply
Dota Warning
• 1 year ago

If one row signifies one item, why do we have quantity in inventory schema?

6

Reply

Stefan Mai

Admin
• 1 year ago

Yes.

0

Reply
E
EquivalentPurpleMarmoset761
Premium
• 1 year ago

Why not using a quantity field for each item instance?

1

Reply
Sheraz Khan
• 1 year ago

If I understand your proposal correctly, you are saying to have a table say "Reservation" which will hold a row per item that is added to cart. While the item is added in this reservation table, inventory is reduced by same quantity. Once the order is confirmed, we remove the row from reservation table and insert in Order table. If order is cancelled, we remove row reservation table and update inventory table. That's what I first thought when I read the article.

0

Reply
Wang lei
• 1 year ago

It is not scalable then, if they are not sold, they are waste of space then just with a quantity. Per my experience, we can delay its creation when it is purchased.

0

Reply
E
ExtraAmaranthDuck389
Top 10%
• 10 months ago

This feels a bit too high level.

Should all items be available/ordered from a single DC?  Once the neabyService provides a list of DC_ID, are we checking if all items are available in any single DC or across DCs?

For available, how do we cache in Redis?

How are we syncing DC data from DB to our application server in-memory cache?

Partition: IIUC, the DC_ID will contain a prefix of Zip Code. And we partition our table on that.

Let's say there is a single application server which can server 20K search qps. But DB can only do like 5K. So then we will have 4 partitions based on zip code. Then the single application server will call the DB and the DB has the knowledge of which of the 4 partition to call?

Replicas: Can you go in more detail how replication works in this case? How many replicas to use? How long does it take for the replicas to be updated with the master? How do we check if they are actually getting updated?

24

Reply
R
RightBlueHippopotamus746
• 5 months ago

Should all items be available/ordered from a single DC?  Once the neabyService provides a list of DC_ID, are we checking if all items are available in any single DC or across DCs?

Seems like a requirements clarification question, which you should align with your interviewer based on the problem focus.

For available, how do we cache in Redis?

The article has been updated with the flow:
-Check cache for availability.
-If unavailable, check DB and write to cache.
-Cache items with a TTL of 1 min to keep them fresh.
-Revoke cache items when Order updates inventory values.

How are we syncing DC data from DB to our application server in-memory cache?

The app servers can periodically read the values from the DB, and update the in memory cache.

Let's say there is a single application server which can server 20K search qps. But DB can only do like 5K. So then we will have 4 partitions based on zip code. Then the single application server will call the DB and the DB has the knowledge of which of the 4 partition to call?

-Why do you have 4 partitions based on zip code? Assuming a zip code prefix of the first three digits, you can have 1000 unique values. If you hash the first three digits, then you can reduce them to a reasonable number of partitions.
-Each app server first checks the cache, else checks the db. The DB routes the app request to the correct partition based on hashing the first three digits of the zip code.

Show More

0

Reply
A
akakhilkumbar
• 11 months ago

need a back to top button, Please

12

Reply
G
GothicCopperPanther728
Premium
• 6 months ago

Command + up arrow

5

Reply
Adil Hussain
Premium
• 3 months ago

For mobile readers this won’t work.

0

Reply
C
CivicBlackAsp163
• 1 year ago

Why not use a queue like Kafka or SQS? The order processing can be async, and it will just have more logic as time goes on.

7

Reply
Abhishek singh
Premium
• 2 months ago
• edited 2 months ago

I think order processing should not be async as customer will like to know instantly that the order is placed or not . Almost all the quick commerce apps I have seen till now show the order is placed or not right away

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

Set Up

Planning the Approach

Defining the Core Entities

Defining the API

High-Level Design

1) Customers should be able to query availability of items

2) Customers should be able to order items.

Putting it all Together

Deep Dives

1) Make availability lookups incorporate traffic and drive time

2) Make availability lookups fast and scalable

What is Expected at Each Level?

Mid-Level

Senior

Staff+

