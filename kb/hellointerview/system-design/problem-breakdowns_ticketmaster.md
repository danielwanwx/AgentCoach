# Ticketmaster

> Source: https://www.hellointerview.com/learn/system-design/problem-breakdowns/ticketmaster
> Scraped: 2026-03-30


Watch Now
Understanding the Problem
🎟️ What is Ticketmaster?
Ticketmaster is an online platform that allows users to purchase tickets for concerts, sports events, theater, and other live entertainment.
Functional Requirements
Start your interview by defining the functional and non-functional requirements. For user facing applications like this one, functional requirements are the "Users should be able to..." statements whereas non-functional defines the system qualities via "The system should..." statements.
Prioritize the top 3 functional requirements. Everything else shows your product thinking, but clearly note it as "below the line" so the interviewer knows you won't be including them in your design. Check in to see if your interviewer wants to move anything above the line or move anything down. Choosing just the top 3 is important to ensuring you stay focused and can execute in the limited time window.
Core Requirements
Users should be able to view events
Users should be able to search for events
Users should be able to book tickets to events
Below the line (out of scope):
Users should be able to view their booked events
Admins or event coordinators should be able to add events
Popular events should have dynamic pricing
Non-Functional Requirements
Core Requirements
The system should prioritize availability for searching & viewing events, but should prioritize consistency for booking events (no double booking)
The system should be scalable and able to handle high throughput in the form of popular events (10 million users, one event)
The system should have low latency search (< 500ms)
The system is read heavy, and thus needs to be able to support high read throughput (100:1)
Below the line (out of scope):
The system should protect user data and adhere to GDPR
The system should be fault tolerant
The system should provide secure transactions for purchases
The system should be well tested and easy to deploy (CI/CD pipelines)
The system should have regular backups
Here's how it might look on your whiteboard:
Requirements
Adding features that are out of scope is a "nice to have". It shows product thinking and gives your interviewer a chance to help you reprioritize based on what they want to see in the interview. That said, it's very much a nice to have. If additional features are not coming to you quickly, don't waste your time and move on.
The Set Up
Planning the Approach
Before you move on to designing the system, it's important to start by taking a moment to plan your strategy. Fortunately, for these common user-facing product-style questions, the plan should be straightforward: build your design up sequentially, going one by one through your functional requirements. This will help you stay focused and ensure you don't get lost in the weeds as you go. Once you've satisfied the functional requirements, you'll rely on your non-functional requirements to guide you through the deep dives.
Defining the Core Entities
I like to begin with a broad overview of the primary entities. At this stage, it is not necessary to know every specific column or detail. We will focus on the intricacies, such as columns and fields, later when we have a clearer grasp. Initially, establishing these key entities will guide our thought process and lay a solid foundation as we progress towards defining the API.
To satisfy our key functional requirements, we'll need the following entities:
Event: This entity stores essential information about an event, including details like the date, description, type, and the performer or team involved. It acts as the central point of information for each unique event.
User: Represents the individual interacting with the system. Needs no further explanation.
Performer: Represents the individual or group performing or participating in the event. Key attributes for this entity include the performer's name, a brief description, and potentially links to their work or profiles. (Note: this could be artist, company, collective, or many other types of entities. The choice of "performer" is intending to be general enough to cover all possible groups)
Venue: Represents the physical location where an event is held. Each venue entity includes details such as address, capacity, and a specific seat map, providing a layout of seating arrangements unique to the venue.
Ticket: Contains information related to individual tickets for events. This includes attributes such as the associated event ID, seat details (like section, row, and seat number), pricing, and status (available or sold). When a new event is created, a ticket is generated for each seat in the venue based on the venue's seat map. The seat map itself is stored as part of the Venue entity (for example, a JSON structure or related table defining sections, rows, and seat numbers along with their coordinates for rendering). The client uses this seat map data combined with each ticket's status to render the interactive seat selection UI.
Booking: Records the details of a user's ticket purchase. It typically includes the user ID, a list of ticket IDs being booked, total price, and booking status (such as in-progress or confirmed). This entity is key in managing the transaction aspect of the ticket purchasing process.
You could arguably fold booking data into the Ticket entity itself, but a separate Booking entity is useful when a user purchases multiple tickets in one transaction since it groups them under a single order with a shared payment status and total price.
In the actual interview, this can be as simple as a short list like this. Just make sure you talk through the entities with your interviewer to ensure you are on the same page.
Entities
As you move onto the design, your objective is simple: create a system that meets all functional and non-functional requirements. To do this, I recommend you start by satisfying the functional requirements and then layer in the non-functional requirements afterward. This will help you stay focused and ensure you don't get lost in the weeds as you go.
API or System Interface
The API for viewing events is straightforward. We create a simple GET endpoint that takes in an eventId and return the details of that event.
GET /events/:eventId -> Event & Venue & Performer & Ticket[]

- tickets are to render the seat map on the Client
In most instances, your interviewer will be able to read between the lines of your core entities and the requirement we're satisfying to understand the data returned by the API. They will either tell you or you can ask them if they'd like you to go into additional detail but be cautious about being over-verbose - you have a lot of ground to cover and enumerating the fields in the Event object may not be the best use of your time!
Next, for search, we just need a single GET endpoint that takes in a set of search parameters and returns a list of events that match those parameters.
GET /events/search?keyword={keyword}&start={start_date}&end={end_date}&pageSize={page_size}&page={page_number} -> Event[]
When it comes to purchasing/booking a ticket, we have a post endpoint that takes the list of tickets and payment details and returns a bookingId.
Later in the design, we'll evolve this into two separate endpoints - one for reserving a ticket and one for confirming a purchase, but this is a good starting point.
POST /bookings/:eventId -> bookingId
 {
   "ticketIds": string[], 
   "paymentDetails": ...
 }
It's ok to have simple APIs from the start that you evolve as your design progresses. As always, just communicate, "Here is a simple API to start, but as we get into the design, we'll likely need to evolve this to handle more complex scenarios."
High-Level Design
1) Users should be able to view events
When a user navigates to www.yourticketmaster.com/event/:eventId they should see details about that event. Crucially, this should include a seatmap showing seat availability. The page will also display the event's name, along with a description. Key information such as the location (including venue details), event dates, and facts about the performers or teams involved could be outlined.
We start by laying out the core components for communicating between the client and our microservices. We add our first service, "Event Service," which connects to a database that stores the event, venue, and performer data outlined in the Core Entities above. This service will handle the reading/viewing of events.
View Event Flow
Clients: Users will interact with the system through the clients website or app. All client requests will be routed to the system's backend through an API Gateway.
API Gateway: This serves as an entry point for clients to access the different microservices of the system. It's primarily responsible for routing requests to the appropriate services but can also be configured to handle cross-cutting concerns like authentication, rate limiting, and logging.
Event Service: Our first microservice is responsible for handling view API requests by fetching the necessary event, venue, and performer information from the database and returning the results to the client.
Events DB: Stores tables for events, performers, and venues.
Let's walk through exactly what happens when a user makes a request to www.yourticketmaster.com/event/:eventId to view an event.
The client makes a REST GET request with the eventId
The API gateway then forwards the request onto our Event Service.
The Event Service then queries the Events DB for the event, venue, and performer information and returns it to the client.
2) Users should be able to search for events
Sweet, we now have the core functionality in place to view an event! But how are users supposed to find events in the first place? When users first open your site, they expect to be able to search for upcoming events. This search will be parameterized based on any combination of keywords, artists/teams, location, date, or event type.
Let's start with the most basic thing you could do - we'll create a simple service which accepts search queries. This service will connect your DB and query it by filtering for the fields in the API request. This has issues, but it's a good starting point. We will dig into better options in the deep dives below.
Search Flow
When a user makes a search request, it's straightforward:
The client makes a REST GET request with the search parameters
Our load balancer accepts the request and routes it to the API gateway with the fewest current connections.
The API gateway then, after handling basic authentication and rate limiting, forward the request onto our Search Service.
The Search Service then queries the Events DB for the events matching the search parameters and returns them to the client.
3) Users should be able to book tickets to events
The main thing we are trying to avoid is two (or more) users paying for the same ticket. That would make for an awkward situation at the event! To handle this consistency issue, we need to select a database that supports transactions. This will allow us to ensure that only one user can book a ticket at a time.
While anything from MySQL to DynamoDB would be fine choices (just needs ACID properties), we'll opt for PostgreSQL. Additionally, we need to implement proper isolation levels and either row-level locking or Optimistic Concurrency Control (OCC) to fully prevent double bookings. More on this later in our deep dives.
Pattern: Dealing with Contention
This is a clear example of a place where high contention can lead to bad outcomes like double bookings. Dealing with contention is a pattern that shows up in a lot of system design interviews and is worth going deeper into.
Learn This Pattern
Simple Booking Flow
New Tables in Events DB: First we add two new tables to our database, Bookings and Tickets. The Bookings table will store the details of each booking, including the user ID, ticket IDs, total price, and booking status. The Tickets table will store the details of each ticket, including the event ID, seat details, pricing, and status. The Tickets table will also have a bookingId column that links it to the Bookings table.
Booking Service: This microservice is responsible for the core functionality of the ticket booking process. It interacts with databases that store data on bookings and tickets.
It interfaces with the Payment Processor (Stripe) for transactions. Once a payment is confirmed, the booking service updates the ticket status to "sold".
It communicates with the Bookings and Tickets tables to fetch, update, or store relevant data.
Payment Processor (Stripe): An external service responsible for handling payment transactions. Once a payment is processed, it notifies the booking service of the transaction status.
When a user goes to book a ticket, the following happens:
The user is redirected to a booking page where they can provide their payment details and confirm the booking.
Upon confirmation, a POST request is sent to the /bookings endpoint with the selected ticket IDs.
The booking server initiates a transaction to:
Check the availability of the selected tickets.
Update the status of the selected tickets to "booked".
Create a new booking record in the Bookings table.
If the transaction is successful, the booking server returns a success response to the client. Otherwise, if the transaction failed because another user booked the ticket in the meantime, the server returns a failure response and we pass this information back to the client.
Note, this means that when a new event is created we need to create a new ticket for each seat in the venue. Each of which will be available for purchase until it is booked.
You may notice that multiple services share the same database. The "database per service" rule gets repeated a lot, but it's not a hard-and-fast rule. Many of the world's largest companies share databases across services when it makes sense. Here, a shared database is the right call because the data is tightly coupled (bookings need tickets need events), we need ACID transactions for booking, and splitting databases would add complexity for no real benefit. In your interview, weigh the tradeoffs and make a decision instead of parroting architectural dogma.
You may have noticed there is a fundamental issue with this design. Users can get to the booking page, type in their payment details, and then find out that the ticket they wanted is no longer available. This would suck and is something that we are going to discuss how to avoid later on in our deep dives. For now, we have a simple implementation that meets the functional requirement.
Potential Deep Dives
With the core functional requirements met, it's time to dig into the non-functional requirements via deep dives. These are the main deep dives I like to cover for this question:
The degree to which a candidate should proactively lead the deep dives is a function of their seniority. For example, it is completely reasonable in a mid-level interview for the interviewer to drive the majority of the deep dives. However, in senior and staff+ interviews, the level of agency and ownership expected of the candidate increases. They should be able to proactively look around corners and address the system in ways that the interviewer may not have thought of.
1) How do we improve the booking experience by reserving tickets?
The current solution, while it technically works, results in a horrible user experience. No one wants to spend 5 minutes filling out a payment form only to find out the tickets they wanted are no longer available because someone else typed their credit card info faster.
If you've ever used similar sites to book event tickets, airline tickets, hotels, etc., you've probably seen a timer counting down the time you have to complete your purchase. This is a common technique to reserve the tickets for a user while they are checking out. Let's discuss how we can add something like this to our design.
We need to ensure that the ticket is locked for the user while they are checking out. We also need to ensure that if the user abandons the checkout process, the ticket is released for other users to purchase. Finally, we need to ensure that if the user completes the checkout process, the ticket is marked as sold and the booking is confirmed. Here are a couple ways we could do this:

Bad Solution: Long-Running Database Locks

Good Solution: Status & Expiration Time with Cron

Great Solution: Implicit Status with Status and Expiration Time

Great Solution: Distributed Lock with TTL

In this case, let's go with the great solution and use distributed lock. We can now update our design to support this flow.
Booking Flow
Now, when a user wants to book a ticket:
A user will select a seat from the interactive seat map. This will trigger a POST /bookings with the ticketId associated with that seat.
The request will be forwarded from our API gateway onto the Booking Service.
The Booking Service will lock that ticket by adding it to our Redis Distributed Lock with a TTL of 10 minutes (this is how long we will hold the ticket for).
The Booking Service will also write a new booking entry in the DB with a status of in-progress.
We will then respond to the user with their newly created bookingId and route the client to the payment page.
If the user stops here, then after 10 minutes the lock is auto-released and the ticket is available for another user to purchase.
The user fills out their payment details on the checkout page. The client uses Stripe.js to tokenize the card details — our server never sees raw credit card numbers (this is standard for PCI compliance). The client sends the resulting payment token along with the bookingId to our server, which creates a Stripe PaymentIntent. Stripe processes the payment and notifies our system via webhook that the payment was successful.
Upon successful payment confirmation from Stripe, our system's webhook retrieves the bookingId embedded within the Stripe metadata. With this bookingId, the webhook initiates a database transaction to concurrently update the Ticket and Booking tables. Specifically, the status of the ticket linked to the booking is changed to "sold" in the Ticket table. Simultaneously, the corresponding booking entry in the Booking table is marked as "confirmed." This webhook handler should be idempotent — Stripe can retry webhooks on failure, so processing the same event twice shouldn't result in duplicate state changes. Using the bookingId as an idempotency key and checking the current booking status before updating ensures safe retries.
Now the ticket is booked!
2) How is the view API going to scale to support 10s of millions of concurrent requests during popular events?
In our non-functional requirements we mentioned that our view and search paths need to be highly available, including during peak traffic scenarios. To accomplish this, we need a combination of load balancing, horizontal scaling, and caching.
Pattern: Scaling Reads
Event pages get absolutely hammered when tickets go on sale - thousands of users refresh the same event page waiting for availability. This extreme read load makes scaling reads crucial through aggressive caching of event details, venue information, and seating charts.
Learn This Pattern

Great Solution: Caching, Load Balancing, and Horizontal Scaling

Caching
3) How will the system ensure a good user experience during high-demand events with millions simultaneously booking tickets?
With popular events, the loaded seat map will go stale quickly. Users will grow frustrated as they repeatedly click on a seat, only to find out it has already been booked. We need to ensure that the seat map is always up to date and that users are notified of changes in real-time.
Sometimes the best solution is actually not technically more challenging. The mark of a senior/staff engineer is their ability to solve business problems and sometimes that means thinking outside the box of presumed constraints. The below Good and Great solutions are illustrative of a common delta between senior and staff candidates.

Good Solution: SSE for Real-Time Seat Updates

Great Solution: Virtual Waiting Queue for Extremely Popular Events

Pattern: Real-time Updates
While we wouldn't pull the trigger on SSE for this use-case, many systems involve some aspect of pushing real-time updates to the client. We've outlined all of the approaches in the Real-time Updates pattern.
Learn This Pattern
Virtual Waiting Room
4) How can you improve search to ensure we meet our low latency requirements?
Our current search implementation is not going to cut it. Queries to search for events based on keywords in the name, description, or other fields will require a full table scan because of the wildcard in the LIKE clause. This can be very slow, especially as the number of events grows.
-- slow query
SELECT * 
FROM Events
WHERE name LIKE '%Taylor%' 
  OR description LIKE '%Taylor%'
Let's look at some strategies to improve search performance and ensure we meet our low latency requirements.

Good Solution: Indexing & SQL Query Optimization

Great Solution: Full-text Indexes in the DB

Great Solution: Use a Full-text Search Engine like Elasticsearch

Excalidraw
5) How can you speed up frequently repeated search queries and reduce load on our search infrastructure?

Good Solution: Implement Caching Strategies Using Redis or Memcached

Great Solution: Implement Query Result Caching and Edge Caching Techniques

As you progress through the deep dives, you should be updating your design to reflect the changes you are making. After doing so, you could have a final design looks something like this:
Final Design
Visual communication is important! Your interviewer is busy. They are likely going to wrap up the interview, go into a long day of meetings, go home tired, and then come back the next morning to remember that they need to write feedback for the interview they conducted the day before. They're then going to pull up your design and try to remember what you said. Make their life easier and improve your own chances by making your visual design as clear as possible.
What is Expected at Each Level?
Ok, that was a lot. You may be thinking, "how much of that is actually required from me in an interview?" Let's break it down.
Mid-level
Breadth vs. Depth: A mid-level candidate will be mostly focused on breadth (80% vs 20%). You should be able to craft a high-level design that meets the functional requirements you've defined, but many of the components will be abstractions with which you only have surface-level familiarity.
Probing the Basics: Your interviewer will spend some time probing the basics to confirm that you know what each component in your system does. For example, if you add an API Gateway, expect that they may ask you what it does and how it works (at a high level). In short, the interviewer is not taking anything for granted with respect to your knowledge.
Mixture of Driving and Taking the Backseat: You should drive the early stages of the interview in particular, but the interviewer doesn't expect that you are able to proactively recognize problems in your design with high precision. Because of this, it's reasonable that they will take over and drive the later stages of the interview while probing your design.
The Bar for Ticketmaster: For this question, an E4 candidate will have clearly defined the API endpoints and data model, landed on a high-level design that is functional for at least viewing and booking events. They are able to solve the "No Double Booking" problem with at least the "Good Solution" which uses status field, timeout, and cron job. Any additional depth would be a bonus, but further deep dives wouldn't be expected.
Senior
Depth of Expertise: As a senior candidate, expectations shift towards more in-depth knowledge — about 60% breadth and 40% depth. This means you should be able to go into technical details in areas where you have hands-on experience. It's crucial that you demonstrate a deep understanding of key concepts and technologies relevant to the task at hand.
Advanced System Design: You should be familiar with advanced system design principles. For example, knowing how to use a search-optimized data store like Elasticsearch for event searching is essential. You're also expected to understand the use of a distributed lock for reserving tickets and to discuss detailed scaling strategies (it's ok if this took some probing/hints from the interviewer), including sharding and replication. Your ability to navigate these advanced topics with confidence and clarity is key.
Articulating Architectural Decisions: You should be able to clearly articulate the pros and cons of different architectural choices, especially how they impact scalability, performance, and maintainability. You justify your decisions and explain the trade-offs involved in your design choices.
Problem-Solving and Proactivity: You should demonstrate strong problem-solving skills and a proactive approach. This includes anticipating potential challenges in your designs and suggesting improvements. You need to be adept at identifying and addressing bottlenecks, optimizing performance, and ensuring system reliability.
The Bar for Ticketmaster: For this question, E5 candidates are expected to speed through the initial high level design so you can spend time discussing, in detail, optimizing search, handling no double booking (landing on a distributed lock or other quality solution), and even have a discussion on handling popular events, showcasing your depth of understanding in managing scalability and reliability under high load conditions.
Staff+
Emphasis on Depth: As a staff+ candidate, the expectation is a deep dive into the nuances of system design — I'm looking for about 40% breadth and 60% depth in your understanding. This level is all about demonstrating that, while you may not have solved this particular problem before, you have solved enough problems in the real world to be able to confidently design a solution backed by your experience.
You should know which technologies to use, not just in theory but in practice, and be able to draw from your past experiences to explain how they'd be applied to solve specific problems effectively. The interviewer knows you know the small stuff (REST API, data normalization, etc) so you can breeze through that at a high level so you have time to get into what is interesting.
High Degree of Proactivity: At this level, an exceptional degree of proactivity is expected. You should be able to identify and solve issues independently, demonstrating a strong ability to recognize and address the core challenges in system design. This involves not just responding to problems as they arise but anticipating them and implementing preemptive solutions. Your interviewer should intervene only to focus, not to steer.
Practical Application of Technology: You should be well-versed in the practical application of various technologies. Your experience should guide the conversation, showing a clear understanding of how different tools and systems can be configured in real-world scenarios to meet specific requirements.
Complex Problem-Solving and Decision-Making: Your problem-solving skills should be top-notch. This means not only being able to tackle complex technical challenges but also making informed decisions that consider various factors such as scalability, performance, reliability, and maintenance.
Advanced System Design and Scalability: Your approach to system design should be advanced, focusing on scalability and reliability, especially under high load conditions. This includes a thorough understanding of distributed systems, load balancing, caching strategies, and other advanced concepts necessary for building robust, scalable systems.
The Bar for Ticketmaster: For a staff+ candidate, expectations are high regarding depth and quality of solutions, particularly for the complex scenarios discussed earlier. Great candidates are diving deep into at least 2-3 key areas, showcasing not just proficiency but also innovative thinking and optimal solution-finding abilities. A crucial indicator of a staff+ candidate's caliber is the level of insight and knowledge they bring to the table. A good measure for this is if the interviewer comes away from the discussion having gained new understanding or perspectives.
Test Your Knowledge

Take a quick 15 question quiz to test what you've learned.

Start Quiz

Mark as read

Next: FB News Feed

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

(547)

Comment
Anonymous
​
Sort By
Popular
Sort By
Mallik Hassan
Top 5%
• 7 months ago

This.. is a gem note!

Visual communication is important! Your interviewer is busy. They are likely going to wrap up the interview, go into a long day of meetings, go home tired, and then come back the next morning to remember that they need to write feedback for the interview they conducted the day before. They're then going to pull up your design and try to remember what you said. Make their life easier and improve your own chances by making your visual design as clear as possible.

52

Reply
M
MutualTurquoiseGoat727
Top 10%
• 2 years ago

This is super useful. But what happens if the lock goes down?

28

Reply

Evan King

Admin
• 2 years ago

Good question. Realistically, you'd immediately bring a new instance up and then you'd have a 10 minute period where multiple users can progress to the payment page for the same ticket. Given we still have our status in the DB and writes are atomic, we will not fail our consistency guarantee, instead, those unlucky users will get an error and have a bad experience. This is a good trade off to discuss with the interviewer though. Slight bad experience vs. larger consistency challenge in replicating lock.

63

Reply
L
LowCyanGoldfish857
• 2 years ago

Isn't lock relying on consensus of multiple nodes (e.g. Redis Raft)? In that case, even if one node goes down, other nodes know there is a lock.

6

Reply
C
CompatiblePeachPorpoise868
• 1 year ago

If I'm not mistaken, Redis Raft is still under development and not intended for production. Redlock, on the other hand, does not use a consensus mechanism. Martin Kleppmann has an article about that in his blog: "How to do distributed locking." Solutions like "Consul" and "Etcd" provide consistent distributed locking backed by consensus protocol and are highly available. Zookeeper is similar, but AFAIK, there's no locking functionality out of the box, but rather a set of primitives, so you must build your own.

4

Reply

Evan King

Admin
• 1 year ago

I actually link to Martin's article in one of the comments below. Also share my opinion in the video. In short your right, but it should not matter :)

4

Reply
L
LatinIvoryDormouse166
Premium
• 9 months ago

How do we pick a DB for the bookings? What are the tradeoffs to consider?

0

Reply
אור סהר
• 11 months ago

Not exactly. If the #of nodes is such that the "leader election" is still available, then you can assume that the consequences on locking wouldn't be affected by node failure, in reality

0

Reply
Priyansh Agrawal
• 5 months ago

Redlock is a client side algorithm to acquire and release lock and there is no leader election happen in the naive setup which requires majority node responses for acquiring the lock. Due to distributed leaderless setup where all the nodes act as primary /master, availability could be tolerated up to certain node failures, for e.g. with 3 it is 1 and for 5 it is 2.

0

Reply
Yasir Mukhtar
Premium
• 3 months ago

You can reserve the tickets in DyanmoDB Lock table with ttl.

1

Reply
Victor
Premium
• 1 year ago

You can use Redis Cluster to have HA lock. Pay attention on the distributed lock implementation to acquire the lock. as ConcreteBlushMastodon771 mentioned, using official lib to acquire the almost node lock like quorum protocol.

1

Reply
Shubham Sinnarkar
• 1 year ago

Isn't it better to use Versioning instead of the overhead of distributed locks and redis? Versioning ensures safe concurrent ticket booking by storing a version number in the database, and allowing an update only if the version hasn't changed, preventing race conditions and double booking.

0

Reply

1 reply hidden which refers to old versions of the article. Expand them.

I
InterestedSalmonSquirrel845
Top 10%
• 1 year ago

Please assess my response in interview setting - "We can enable AOF on Redis, so that the new instance can initialize its memory with previous instance's logs? This will sacrifice a bit of its low-latency guarantee in favor of improving the consistency. But considering that we will use replication in Redis, the chances of Redis going down are lower hence it would be better to have that bad experience for rare times rather than having high latency all the time".

0

Reply

7 replies hidden which refer to old versions of the article. Expand them.

C
ConcreteBlushMastodon771
Top 5%
• 1 year ago

There is a paper on the Redlock algorithm which Redis discusses how to mitigate the single point of failure, and how to work around the issue where Redis replication being async:
https://redis.io/docs/manual/patterns/distributed-locks/

I don't believe any interviewer would expect you to know this algorithm, but if you can bring it up, you can certainly impress the interviewer!

6

Reply
Victor
Premium
• 1 year ago

Alternatively, you can use Redis Sentinel HA cluster, which will guarantee the HA and strong consistency.

0

Reply
Priyansh Agrawal
• 5 months ago

IMO, it will involve master-slave replication and due to replication lag and when leader fails the lock might not replicated to new leader elected from slaves . Correct me if im wrong here

2

Reply
P
PositiveEmeraldParakeet596
• 1 year ago

Nice one!

0

Reply
Syed Bilal
Top 5%
• 1 year ago

There are some really good discussions here down in the discussion section.

I would recommend you to add feature to pin the favourite comments and beside anonymous button, a filter feature can be added to show only favourite comments for a particular user.
It will help you to pin some of the important comments or mark it for future easy reference instead of reading all the threads to search for that comment.

11

Reply

Evan King

Admin
• 1 year ago

Agreed :) I will add it to the list and hopefully get to it soon. The comment became a bit unwieldy in length.

1

Reply
R
RollingCyanWren150
Top 5%
• 1 year ago

Thanks King ;)

0

Reply
L
LimitedEmeraldKoi758
• 1 year ago

Wouldn't we want the virtual waiting queue to queue users accessing the Event CRUD service? Not the booking service?

The booking service has two APIs (reserve and confirm) but don't we want to bar users from seeing the event with live updates to the seatmap first (i.e. /GET event/:event_id)?

9

Reply

Evan King

Admin
• 1 year ago

Yes actually! Good point

1

Reply
M
MeaningfulGreenFerret245
Premium
• 9 months ago

hi Evan i also have same question, so for users to see the updated seatmap, can we use server sent events ,where the seat map will be updated, if other users are selecting the seats.
also is reserve  and confirm api called at once ?

0

Reply
L
LimitedEmeraldKoi758
• 1 year ago

Also a HUGE thank you for putting this resource together. The videos in particular are very useful :)

0

Reply

1 reply hidden which refers to old versions of the article. Expand them.

Castulo J. Martinez
• 1 year ago

When designing an application using a micro-service architecture, when is it better to access directly a database shared by another service so both services end up using the same database, and when is preferable to call the other service to request this info so only one service can access the database and pass the requested information to the service that requested it?

5

Reply

Stefan Mai

Admin
• 1 year ago

There's options here. A "true" microservice architecture will have each service own its own data - but this creates a bunch of new problems around data integrity and synchronization. Generally speaking the larger the org the more likely you want to move toward data isolations to prevent issues.

If this was in an interview I'd discuss the tradeoffs with my interviewer. "I think for our purposes I'll use a single database here but if this was a real project I'd evaluate the tradeoff of complexity for extensibility." Prepare to explain yourself :)

2

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

1) Users should be able to view events

2) Users should be able to search for events

3) Users should be able to book tickets to events

Potential Deep Dives

1) How do we improve the booking experience by reserving tickets?

2) How is the view API going to scale to support 10s of millions of concurrent requests during popular events?

3) How will the system ensure a good user experience during high-demand events with millions simultaneously booking tickets?

4) How can you improve search to ensure we meet our low latency requirements?

5) How can you speed up frequently repeated search queries and reduce load on our search infrastructure?

What is Expected at Each Level?

Mid-level

Senior

Staff+
