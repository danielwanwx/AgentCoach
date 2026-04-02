# Tinder

> Source: https://www.hellointerview.com/learn/system-design/problem-breakdowns/tinder
> Scraped: 2026-03-30


Tinder is a mobile dating app that helps people connect by allowing users to swipe right to like or left to pass on profiles. It uses location data and user-specified filters to suggest potential matches nearby.
Functional Requirements
Core Requirements
Users can create a profile with preferences (e.g. age range, interests) and specify a maximum distance.
Users can view a stack of potential matches in line with their preferences and within max distance of their current location.
Users can swipe right / left on profiles one-by-one, to express "yes" or "no" on other users.
Users get a match notification if they mutually swipe on each other.
Below the line (out of scope)
Users should be able to upload pictures.
Users should be able to chat via DM after matching.
Users can send "super swipes" or purchase other premium features.
It's worth noting that this question is mostly focused on the user recommendation "feed" and swiping experience, not on other auxiliary features. If you're unsure what features to focus on for an app like this, have some brief back and forth with the interviewer to figure out what part of the system they care the most about. It'll typically be the functionality that makes the app unique or the most complex.
Non-Functional Requirements
Core Requirements
The system should have strong consistency for swiping. If a user swipes "yes" on a user who already swiped "yes" on them, they should get a match notification.
The system should scale to lots of daily users / concurrent users (20M daily actives, ~100 swipes/user/day on average).
The system should load the potential matches stack with low latency (e.g. < 300ms).
The system should avoid showing user profiles that the user has previously swiped on.
Below the line (out of scope)
The system should protect against fake profiles.
The system should have monitoring / alerting.
Here's how it might look on a whiteboard:
Non-Functional Requirements
The Set Up
Planning the Approach
Before you move on to designing the system, it's important to start by taking a moment to plan your strategy. Fortunately, for these product design style questions, the plan should be straightforward: build your design up sequentially, going one by one through your functional requirements. This will help you stay focused and ensure you don't get lost in the weeds as you go.
Once we've satisfied the functional requirements, you'll rely on your non-functional requirements to guide you through the deep dives.
Defining the Core Entities
Let's start by defining the set of core entities. Initially, establishing these key entities will guide our thought process and lay a solid foundation as we progress towards defining the API. We don't need to know every field or column at this point, but if you have a good idea of what they might be, feel free to jot them down.
For Tinder, the primary entities are pretty straightforward:
User: This represents both a user using the app and a profile that might be shown to the user. We typically omit the "user" concept when listing entities, but because users are swiping on other users, we'll include it here.
Swipe: Expression of "yes" or "no" on a user profile; belongs to a user (swiping_user) and is about another user (target_user).
Match: A connection between 2 users as a result of them both swiping "yes" on each other.
In the actual interview, this can be as simple as a short list like this. Just make sure you talk through the entities with your interviewer to ensure you are on the same page.
Defining the Core Entities
As you move onto the design, your objective is simple: create a system that meets all functional and non-functional requirements. To do this, I recommend you start by satisfying the functional requirements and then layer in the non-functional requirements afterward. This will help you stay focused and ensure you don't get lost in the weeds as you go.
The API
The API is the primary interface that users will interact with. You'll want to define the API early on, as it will guide your high-level design. We just need to define an endpoint for each of our functional requirements.
The first endpoint we need is an endpoint to create a profile for a user. Of course, this would include images, bio, etc, but we're going to focus just on their match preferences for this question.
POST /profile
{
  "age_min": 20,
  "age_max": 30,
  "distance": 10,
  "interestedIn": "female" | "male" | "both",
  ...
}
Next we need an endpoint to get the "feed" of user profiles to swipe on, this way we have a "stack" of profiles ready for the user:
GET /feed?lat={}&long={}&distance={} -> User[]
We don't need to pass in other filters like age, interests, etc. because we're assuming the user has already specified these in the app settings, and we can load them server-side.
Unless you pay for the premium version (out of scope), Tinder will show users within a specific radius of your current location. Given that this can always change, we pass it in client-side as opposed to persisting server-side.
You might be tempted to proactively consider pagination for the feed endpoint. This is actually superfluous for Tinder b/c we're really generating recommendations. Rather than "paging", the app can just hit the endpoint again for more recommendations if the current list is exhausted.
We'll also need an endpoint to power swiping:
POST /swipe/{userId}
Request:
{
  decision: "yes" | "no"
}
With each of these requests, the user information will be passed in the headers (either via session token or JWT). This is a common pattern for APIs and is a good way to ensure that the user is authenticated and authorized to perform the action while preserving security. You should avoid passing user information in the request body, as this can be easily manipulated by the client.
In the interview, you may want to just denote which endpoints require user authentication and which don't. In our case, all endpoints will require authentication.
High-Level Design
We'll start our design by going one-by-one through our functional requirements and designing a single system to satisfy them. Once we have this in place, we'll layer on depth via our deep dives.
1) Users can create a profile with preferences (e.g. age range, interests) and specify a maximum distance.
The first thing we need to do in a dating site like Tinder is allow users to tell us about their preferences. This way we can increase the probability of them finding love by only showing them profiles that match these preferences.
We'll need to take the post request to POST /profile and persist these settings in a database.
We can do this with a simple client-server-database architecture.
Users can create a profile with preferences (e.g. age range, interests) and specify a maximum distance.
Client: Users interact with the system through a mobile application.
API Gateway: Routes incoming requests to the appropriate services. In this case, the Profile Service.
Profile Service: Handles incoming profile requests by updating the user's profile preferences in the database.
Database: Stores information about user profiles, preferences, and other relevant information.
When a user creates a profile:
The client sends a POST request to /profile with the profile information as the request body.
The API Gateway routes this request to the Profile Service.
The Profile Service updates the user's profile preferences in the database.
The results are returned to the client via the API Gateway.
2) Users can view a stack of potential matches
When a user enters the app, they are immediately served a stack of profiles to swipe on. These profiles abide by filters that the user specified (e.g. age, interests) as well as the user's location (e.g. < 2 miles away, < 5 miles away, < 15 miles away).
Serving up this feed efficiently is going to be a key challenge of the system, but we'll start simple and optimize later during the deep dive.
The easiest thing we can do it just query the database for a list of users that match the user's preferences and return them to the client. We'll need to also consider the users current location as to make sure they only get serves profiles close to them.
The simple query would look something like this:
SELECT * FROM users
WHERE age BETWEEN 18 AND 35
AND interestedIn = 'female'
AND lat BETWEEN userLat - maxDistance AND userLat + maxDistance
AND long BETWEEN userLong - maxDistance AND userLong + maxDistance
Users can view a stack of potential matches
When a user requests a new set of profiles:
The client sends a GET request to /feed with the user's location as a query parameter.
The API Gateway routes this request to the Profile Service.
The Profile Service queries the User Database for a list of users that match the user's preferences and location.
The results are returned to the client via the API Gateway.
If you read any of our other write-ups you know this by now, this query would be incredibly inefficient. Searching by location in particular, even with basic indexing, would be incredibly slow. We'll need to look into more sophisticated indexing and querying techniques to improve the performance during our deep dives.
3) Users can swipe right / left on profiles one-by-one, to express "yes" or "no" on other users
Once users have their "stack" of profiles they're ready to find love! They just need to swipe right if they like the person and left if they don't. The system needs to record each swipe and tell the user that they have a match if anyone they swipe right on has previously swiped right on them.
We need a way to persist swipes and check if they're a match. Again, we'll start with something simple and inefficient and improve upon it during our deep dives.
We'll introduce two new components:
Swipe Service: Persists swipes and checks for matches.
Swipe Database: Stores swipe data for users.
Notice how we opt for a separate service and a separate DB this time, why?
My justification here would be that profile view and creation happens far less frequently than swipe writes. So by separating the services, we allow for the swipe service to scale up independently. Similarly, for the database, this is going to be a lot of swipe data. With 20M DAU x 100 swipes/day x 100 bytes per swipe we're looking at ~200GB of data a day! Not only will this do best with a write optimized database like Cassandra (maybe not the right fit for our profile database), but this allows us to scale and optimize swipe operations independently. It also enables us to implement swipe-specific logic and caching strategies without affecting the profile service.
Separating isn't the right choice for all systems, but for this one the pros outweigh the cons.
Given that the swipe interaction is so effortless, we can assume we're going to get a lot of writes to the DB. Additionally, there is going to be a lot of swipe data. If we assume 20M daily active users doing 200 swipes a day on average, that nets us 4B swipes a day. This certainly means we'll need to partition the data.
Cassandra is a good fit as a database here. We can partition by swiping_user_id. This means an access pattern to see if user A swiped on user B will be fast, because we can predictably query a single partition for that data. Additionally, Cassandra is extremely capable of massive writes, due to its write-optimized storage engine (CommitLog + Memtables + SSTables). A con of using Cassandra here is the element of eventual consistency of swipe data we inherit from using it. We'll discuss ways to avoid this con in later deep dives.
Users can swipe right / left on profiles one-by-one, to express "yes" or "no" on other users
When a user swipes:
The client sends a POST request to /swipe with the profile ID and the swipe direction (right or left) as parameters.
The API Gateway routes this request to the Swipe Service.
The Swipe Service updates the Swipe Database with the swipe data.
The Swipe Service checks if there is an inverse swipe in the Swipe Database and, if so, returns a match to the client.
4) Users get a match notification if they mutually swipe on each other
When a match occurs, both people need to be notified that there is a match. To make things clear, let's call the first person who like the other Person A. The second person will be called Person B.
Notifying Person B is easy! In fact, we've already done it. Since they're the second person to swipe, immediately after they swipe right, we check to see if Person A also liked them and, if they did, we show a "You matched!" graphic on Person B's device.
But what about Person A? They might have swiped on Person B weeks ago. We need to send them a push notification informing them that they have a new connection waiting for them.
To do this, we're just going to rely on device native push notifications like Apple Push Notification Service (APNS) or Firebase Cloud Messaging (FCM).
Users get a match notification if they mutually swipe on each other
APNS and FCM are both push notification services that we can use to send push notifications to user devices. They both have their own set of native APIs and SDKs that we can use to send users push notifications.
Let's quickly recap the full swipe process again, now that we've introduced push notifications into the flow.
Some time in the past, Person A swiped right on Person B and we persisted this swipe in our Swipe DB.
Person B swipes right on Person A.
The server checks for an inverse swipe and finds that it does, indeed, exist.
We display a "You Matched!" message to Person B immediately after swiping.
We send a push notification via APNS or FCM to Person A informing them that they have a new match.
Since this design is less concerned with the after-match flow, we can avoid diving into the match storage details. Additionally, we can make an assumption that an external service can support push notifications. Be sure to clarify these assumptions with your interviewer!
Potential Deep Dives
At this point, we have a basic, functioning system that satisfies the functional requirements. However, there are a number of areas we could dive deeper into to improve the system's performance, scalability, etc. Depending on your seniority, you'll be expected to drive the conversation toward these deeper topics of interest.
1) How can we ensure that swiping is consistent and low latency?
Let's start by considering the failure scenario. Imagine Person A and Person B both swipe right (like) on each other at roughly the same time. Our order of operations could feasibly look something like this:
Person A swipe hits the server and we check for inverse swipe. Nothing.
Person B swipe hits the server and we check for inverse swipe. Nothing.
We save Person A swipe on Person B.
We save Person B swipe on Person A.
Now, we've saved the swipe to our database, but we've lost the opportunity to notify Person A and Person B that they have a new match. They will both go on forever not knowing that they matched and true love may never be discovered.
It's worth mentioning that you could solve this problem without strong consistency. You could have some reconciliation process that runs periodically to ensure all matching swipes have been processed as a match. For those that haven't, just send both Person A and Person B a notification. They won't be any the wiser and will just assume the other person swiped on them in that moment. This would allow you to prioritize availability over consistency and would be an interesting trade-off to discuss in the interview. It makes the problem slightly less challenging, though, so there is a decent chance the interviewer will appreciate the conversation but suggest you stick with prioritizing consistency.
Given that we need to notify the last swiper of the match immediately, we need to ensure the system is consistent. Here are a few approaches we could take to ensure this consistency:

Bad Solution: Database Polling for Matches

Good Solution: Transactions

Great Solution: Sharded Cassandra with Single-Partition Transactions

Great Solution: Redis for Atomic Operations

2) How can we ensure low latency for feed/stack generation?
When a user open the app, they want to immediately start swiping. They don't want to have to wait for us to generate a feed for them.
As we discussed in our high-level design, our current design has us running a slow query every time we want a new stack of users.
SELECT * FROM users
WHERE age BETWEEN 18 AND 35
AND interestedIn = 'female'
AND lat BETWEEN userLat - maxDistance AND userLat + maxDistance
AND long BETWEEN userLong - maxDistance AND userLong + maxDistance
This certainly won't meet our non-functional requirement of low latency stack generation. Let's see what else we can do.

Good Solution: Use of Indexed Databases for Real-Time Querying

Good Solution: Pre-computation and Caching

Great Solution: Combination of Pre-computation and Indexed Database

Astute readers may realize that by pre-computing and caching a feed, we just introduced a new issue: stale feeds.
How do we avoid stale feeds?
Caching feeds of users might result in us suggesting "stale" profiles. A stale profile is defined as one that no longer fits the filter criteria for a user. Below are some examples of the ways a profile in a feed might become stale:
A user suggested in the feed might have changed locations and is no longer close enough to fit the feed filter criteria.
A user suggested in the feed might change their profile (e.g. changed interests) and no longer fits the feed filter criteria.
The above are real problems that might lead to a bad UX if the user sees a profile that doesn't actually match their preferred filters. To solve this issue, we might consider having a strict TTL for cached feeds (< 1h) and re-compute the feed via a background job on a schedule. We also might pre-computing feeds only for truly active users, vs. for all users. Doing upfront work for a user feed several times a day will be expensive at scale, so we might "warm" these caches only for users we know will eventually use the cached profiles. A benefit of this approach is that several parameters are tunable: the TTL for cached profiles, the number of profiles cached, the set of users we are caching feeds for, etc.
When designing a system, it's very useful if the system has parameters that can be tuned without changing the overall logic of the system. These parameters can be modified to find an efficient configuration for the scale / use-case of the system and can be adjusted over time. This gives the operators of the system strong control over the health of the system without having to rework the system itself.
A few user-triggered actions might also lead to stale profiles in the feed:
The user being served the feed changes their filter criteria, resulting in profiles in the cached feed becoming stale.
The user being served the feed changes their location significantly (e.g. they go to a different neighborhood or city), resulting in profiles in the cached feed becoming stale.
All of the above are interactions that could trigger a feed refresh in the background, so that the feed is ready for the user if they choose to start swiping shortly after.
3) How can the system avoid showing user profiles that the user has previously swiped on?
It would be a pretty poor experience if users were re-shown profiles they had swiped on. It could give the user the impression that their "yes" swipes were not recorded, or it could annoy users to see people they previously said "no" to as suggestions again.
We should design a solution to prevent this bad user experience.

Bad Solution: DB Query + Contains Check

Great Solution: Cache + DB Query + Contains Check

Great Solution: Cache + Contains Check + Bloom Filter

Final Design
Final Design
What is Expected at Each Level?
Ok, that was a lot. You may be thinking, “how much of that is actually required from me in an interview?” Let’s break it down.
Mid-level
Breadth vs. Depth: A mid-level candidate will be mostly focused on breadth (80% vs 20%). You should be able to craft a high-level design that meets the functional requirements you've defined, but many of the components will be abstractions with which you only have surface-level familiarity.
Probing the Basics: Your interviewer will spend some time probing the basics to confirm that you know what each component in your system does. For example, if you add an API Gateway, expect that they may ask you what it does and how it works (at a high level). In short, the interviewer is not taking anything for granted with respect to your knowledge.
Mixture of Driving and Taking the Backseat: You should drive the early stages of the interview in particular, but the interviewer doesn’t expect that you are able to proactively recognize problems in your design with high precision. Because of this, it’s reasonable that they will take over and drive the later stages of the interview while probing your design.
The Bar for Tinder: For this question, an E4 candidate will have clearly defined the API endpoints and data model, landed on a high-level design that is functional for all of feed creation, swiping, and matching. I don't expect candidates to know in-depth information about specific technologies, but I do expect the candidate to design a solution that supports traditional filters and geo-spatial filters. I also expect the candidate to design a solution to avoid re-showing swiped-on profiles.
Senior
Depth of Expertise: As a senior candidate, expectations shift towards more in-depth knowledge — about 60% breadth and 40% depth. This means you should be able to go into technical details in areas where you have hands-on experience. It's crucial that you demonstrate a deep understanding of key concepts and technologies relevant to the task at hand.
Advanced System Design: You should be familiar with advanced system design principles (different technologies, their use-cases, how they fit together). Your ability to navigate these advanced topics with confidence and clarity is key.
Articulating Architectural Decisions: You should be able to clearly articulate the pros and cons of different architectural choices, especially how they impact scalability, performance, and maintainability. You justify your decisions and explain the trade-offs involved in your design choices.
Problem-Solving and Proactivity: You should demonstrate strong problem-solving skills and a proactive approach. This includes anticipating potential challenges in your designs and suggesting improvements. You need to be adept at identifying and addressing bottlenecks, optimizing performance, and ensuring system reliability.
The Bar for Tinder: For this question, E5 candidates are expected to quickly go through the initial high-level design so that they can spend time discussing, in detail, how to handle feed efficient / scalable feed generation and management and how to ensure successful match creation. I expect an E5 candidate to be proactive in calling out the different trade-offs for feed building and to have some knowledge of the type of index that could be used to successfully power the feed. I also expect this candidate to be aware of when feed caches might become "stale".
Staff+
Emphasis on Depth: As a staff+ candidate, the expectation is a deep dive into the nuances of system design — I'm looking for about 40% breadth and 60% depth in your understanding. This level is all about demonstrating that, while you may not have solved this particular problem before, you have solved enough problems in the real world to be able to confidently design a solution backed by your experience.
You should know which technologies to use, not just in theory but in practice, and be able to draw from your past experiences to explain how they’d be applied to solve specific problems effectively. The interviewer knows you know the small stuff (REST API, data normalization, etc.) so you can breeze through that at a high level so you have time to get into what is interesting.
High Degree of Proactivity: At this level, an exceptional degree of proactivity is expected. You should be able to identify and solve issues independently, demonstrating a strong ability to recognize and address the core challenges in system design. This involves not just responding to problems as they arise but anticipating them and implementing preemptive solutions. Your interviewer should intervene only to focus, not to steer.
Practical Application of Technology: You should be well-versed in the practical application of various technologies. Your experience should guide the conversation, showing a clear understanding of how different tools and systems can be configured in real-world scenarios to meet specific requirements.
Complex Problem-Solving and Decision-Making: Your problem-solving skills should be top-notch. This means not only being able to tackle complex technical challenges but also making informed decisions that consider various factors such as scalability, performance, reliability, and maintenance.
Advanced System Design and Scalability: Your approach to system design should be advanced, focusing on scalability and reliability, especially under high load conditions. This includes a thorough understanding of distributed systems, load balancing, caching strategies, and other advanced concepts necessary for building robust, scalable systems.
The Bar for Tinder: For a staff-level candidate, expectations are high regarding the depth and quality of solutions, especially for the complex scenarios discussed earlier. Exceptional candidates delve deeply into each of the topics mentioned above and may even steer the conversation in a different direction, focusing extensively on a topic they find particularly interesting or relevant. They are also expected to possess a solid understanding of the trade-offs between various solutions and to be able to articulate them clearly, treating the interviewer as a peer.
Test Your Knowledge

Take a quick 15 question quiz to test what you've learned.

Start Quiz

Mark as read

Next: LeetCode

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

(236)

Comment
Anonymous
​
Sort By
Popular
Sort By
Tanuj Gupta
Top 10%
• 1 year ago

Why do need consistency checks while swiping and matching

The whole problem occurs only when we check for a reversed swipe before inserting the current swipe.

What if we first insert a -> b swipe, and then check if b also swiped on a?
In that case, even if 2 threads do these operations simultaneously,
One of them will see an insert of the other.

And will successfully notify A, and B for a match

36

Reply
hellointerview
Premium
• 6 months ago

I totally concur, I have been scratching my head looking for why do we need a write and immediately read txn ? In fact we are creating a problem by creating such a txn - in cases where they happen parallely and the txn type is set to READ_COMMITTED, both txns wont see each other and would not return the match

If we split these into independent steps, the granularity allows for at least one match

Aw Ar Bw Br
Bw Br Aw Ar => are only two sequences that ensure only one of them get a match, in all the remaining cases, both of them see the match

2

Reply
ConsistencyKing
Premium
• 1 month ago

Even with “write then check”, you can still miss in practice if:

reads are not strongly consistent (eventual replication / read from stale replica),

or the system chooses availability over consistency (the writeup explicitly calls out this tradeoff).

So the deeper point is: you need an atomic read-modify-write over a single “shared record” for the pair, not “two independent writes + best-effort reads.”

1

Reply
P
PastAmberElk808
• 1 year ago

this makes sense. The cons I can think of though is doing two round-trips to db: 1 for insert and one for checking the reversed swipe but we are doing it anyway with the missed-match approach.

1

Reply
P
PastAmberElk808
• 1 year ago

Oh actually, even if we do a write first, there still might be a match-miss because we use Cassandra and it is eventually consistent. The A->B insert might be on different partitions than the B->A, when B->A happens it checks for A->B but the data on the shards where it check can be stale, thus returns in a miss. This eventual consistent can be resolved as written with either putting those 2 swipes on same partition for strong consistent or using redis for atomic ops.

17

Reply
slrparser
Top 5%
• 9 months ago

If you use partition key: smaller_id:larger_id to put them in the same partition, then how would you power this search - Give me all matches of a user? You would have to go to each shard to gather this, right?

3

Reply
Priyansh Agrawal
• 4 months ago

Based on the explanation provided in the article, Cassandra should not store data with partition key smaller_id:larged_id but rather store data in model swipe_from_user_id, swiper_to_user_id, swipe_type (left or right). Here partition key would be the swiper_from_user_id and PK should be (swipe_from_user_id, swipe_to_user_id). This would give all the match of the user for which we are generating the feed cache to remove profiles which the user has already swiped.

Unlike dynamo DB, Cassandra don't have global index and so query by swipe_from_user_id will be slow compared to the denormalized format explained above.

Only Redis should have the key with smaller_id:larged_id.

0

Reply
Ayush Shukla
Premium
• 3 months ago

But if we put both thing in same partition still there replicas are not synonymous and and lead to inconsistency ?

0

Reply
Priyansh Agrawal
• 4 months ago

If we are storing the original swipe data in the Casandra for durability, then should we keep only smaller_user_id:larger_user_id string as redis key and its value could be user who makes the swipe ?. Doing this could eliminate the redis Lua script requirement as it will block any redis operations until it gets finished, thereby will consume slightly more resources compare to simple redis SETNX operation (this leverage redis single threaded architecture).

def handle_swipe_right(from_user, to_user):
    key = get_sorted_key(from_user, to_user)  # "123:456"
    result = redis.setnx(key, from_user, ex = 1 week may be )
    if result == 0:  # Key already exists
        # Get the existing value to check who set it
        existing_user = redis.get(key)
        if existing_user == to_user:
            # The other user set it → MATCH!
            insert_swipe_to_cassandra(from_user, to_user, 'right')
            notify_users([from_user, to_user])
            redis.delete(key)  # Clean up
        elif existing_user == from_user:
            # If client retries results in false positives
            pass
       else:
             # key is deleted, may be due to elapsed TTL . 
             # if there is right swipe from to_user to from_user
             iinsert_swipe_to_cassandra(from_user, to_user, 'right')
    else: result == 1:
       insert_swipe_to_cassandra(from_user, to_user, 'right')
        # if right swipe exists between to_user to from_user  
       notify_users([from_user, to_user])
       redis.delete(key)  
Show More

0

Reply
Abhijit Shankhdhar
• 1 month ago

Can we have the double notify problem if we write first and then check. Let's say both (A->B, B->A) wrote parallelly and then  they both checked and got the entry and notification is send from both sides. We can prevent this by storing that is user is notified about a match or not . But it will be too complex to manage and again we can get stuck into the concurrency trap

0

Reply
A
alnataraw
• 1 year ago

Great write up,

I was wondering why do we need two separate rows for swiping two users and also cassandra transaction is only atomic in row-level, right? even we use lightweight transaction, we can only do that in one clause of update or insert (e.g IF NOT EXIST)

why not just attach the swipe info in MATCH table?

partition_key -> MATCH:USER_SMALLER_ID:USER_BIGGER_ID
user_smaller_id
user_bigger_id
smaller_to_bigger_swipe_status
bigger_to_smaller_swipe_status
version -> as fencing update

this schema allow us to do atomic update as Cassandra atomic update is row-level, right?

10

Reply
slrparser
Top 5%
• 9 months ago

If you use partition key: smaller_id:larger_id to put them in the same partition, then how would you power this search - Give me all matches of a user? You would have to go to each shard to gather this, right?

1

Reply
N
nabajyoti.techfest
Premium
• 6 months ago

why do we need all matches of a user??

0

Reply
Aman Mahajan
• 1 year ago

This is excellent. I was thinking the same. Solves everything.

0

Reply
H
HandsomeIvoryCrow799
Top 10%
• 11 months ago

A Cassandra BATCH cannot include SELECT statement per the official document. In fact, mixing LWT operation (INSERT) and non-LWT operation (SELECT), the non-LWT operation may return the old data.

In order to read the latest data after the user invoked a LWT operation, we'd need to set the read consistency level to SERIAL.

8

Reply
Kevin Jonaitis
Premium
• 7 months ago

You're right the BATCH cannot support select. I really didn't like that whole section on consistency in cassandra.

I don't think LWT nor SERIAL is a good idea at all because it'd slow down Cassandra to the point of it not being a useful choice of DB(the whole point of using Cassandra is fast writes and these options increase latency by10-100x).

You could get away with setting local quorum for reads/writes(which is fast enough i.e. sub 5ms for read/writes), IF you only had 1 datacenter. I'll explain here:

With local quorum, we are promised "strong consistency", which means "Every read always returns the most recent write.".

To recap, in the example, we are writing one row for each swipe.

If our write/read pattern is:
add swipe from 123 ->456
check for match by checking for swipe 456 -> 123

and another write/read:
add swipe 456 -> 123
check for match by checking for swipe  123 -> 456

with local quorum, we're always guaranteed to see writes after reads, and we're guaranteed that at least ONE of those checks would return true.

Show More

6

Reply
H
HandsomeIvoryCrow799
Top 10%
• 5 months ago

You're right. I'm working on this problem again the second time and I totally align with your points. It does not really make sense to use LWT with SERIAL consistency level (which is equivalent to QUORUM consistency level essentially).

Just one note though: It seems when we have multiple data centers in a cluster, Cassandra would attempt to write to all data centers regardless, while LOCAL_QUORUM read only guarantees consistent read within the same data center as the coordinator node. So if users 123 and 456 are not geographically close, there's a high chance they will write to and read from different data centers.

However, if we limit the maximum distance preference specified by the user then there's a high chance they will write to and read from the same data center, in which case the LOCAL_QUORUM consistency level would work perfectly.

Regardless, we should not need LWT.

0

Reply
H
HandsomeIvoryCrow799
Top 10%
• 5 months ago

And actually, I'm not even sure if Cassandra is the best database for this problem considering that it's possible for us to traverse through multiple on-disk SSTables before we can find the swipe record. In this problem, I think Dynamo might be a better option considering it uses B-Tree under the hood and it does offer strongly consistent reads.

6

Reply
Priyansh Agrawal
• 4 months ago

If users across region right swipes concurrently then because the replication across DC is asynchronously done, it might be possible that returned reads are stale under LOCAL_QUORUM CL. This could result in recording the right swipes by users but missed match notification.  Even we use LWT we can't solve it because LWT only checks in local DC which might not has data from other user swipe. We should limit user feed to have profiles from region where user belongs

0

Reply
A
AddedLimeCarp593
Top 1%
• 10 months ago

I'm confused... The BATCH in the single-partition Cassandra solution doesn't seem to be using LWTs because there's no IF clause and everything I'm reading online says LWTs always have that IF.

0

Reply
Aaditya Rangarajan
• 1 year ago

In the first deep dive section, I don't see how any of the solutions help address the problem that was raised. If my understanding is correct, the issue with the design up till this point is that if 2 users swipe right on each other in really short time intervals, neither one of them will get a notification of the match. How does using transactions address this? As I understand, each swipe has it's own unique row, so both the transaction could still occur concurrently, in which case we end up back where we started. I would appreciate your guidance.

6

Reply
D
DizzyJadePerch635
• 11 months ago

My thought was that transactions would guarantee ordering of the events. So swipe 1 will be persisted first, and then swipe 2 will be able to find it and can report a match. I think as part of the transaction it would search for a matching swipe.

2

Reply
E
EasternChocolateLimpet925
Premium
• 6 months ago

In the POSTGRES design we just create one row, where we store the decision for both users. POSTGRES will automatically lock rows if we are making updates to the same row.
For redis we use a LUA script that would solve our problem.

0

Reply
F
FascinatingAmethystMarsupial369
Top 1%
• 6 months ago

Where is this POSTGRES design you talk about? I cannot find it in the article

0

Reply
Priyansh Agrawal
• 4 months ago

I think he meant that if we use POSTGRES instead of cassandra then how the concurrent right swipes by two different users will be handled

0

Reply
Larry
• 1 year ago

Hi, in terms of swiping consistency, does the assumed order matter?

<- Our order of operations could feasibly look something like this:

Person A swipe hits the server and we check for inverse swipe. Nothing.
Person B swipe hits the server and we check for inverse swipe. Nothing.
We save Person A swipe on Person B.
We save Person B swipe on Person A.

Question - if we first save (write self), then check (read the other), do we still need transaction? (inside the transaction, seems you have this order).

6

Reply
F
FastJadeGrouse442
• 1 year ago

I think write self then read other would help, but the 'read other' could still hit a stale replica machine due to eventual consistency.

1

Reply
Larry
• 1 year ago

Yes that is how I feel. If there exists replication lag, having transactions or not matters?

1

Reply
P
PerfectTomatoGibbon866
• 1 year ago

It might actually be better to not use LWT, and directly do a normal write query and then read query, both with quorum consistency. This might be better latency wise as LWT uses 4 phase commit which does not seem required in this case

1

Reply
F
FastJadeGrouse442
• 1 year ago

Yes, my understanding is that Redis atomicity and single threaded ensure transactions are executed sequentially on the primary nodes (If Redis has replication setup then I think we'd suffer from replication lag all over again, choosing good partition key should avoid the need for replication)

0

Reply
Larry
• 1 year ago

Before talking about Redis, in the "good solution" that uses transaction, the author claimed we won't miss any match. I do not think this is accurate given replication lag. How do you think? @Evan King

0

Reply

Evan King

Admin
• 1 year ago

Kind of. We need either a distributed database with consensus protocols to guarantee read-after-write consistency (trading speed for consistency) or a centralized in-memory store like Redis.

1

Reply
P
panaali2
Top 10%
• 1 year ago

I initially thought Cassandra's timestamp based last write wins could be an issue but thinking more about it, We only have one write for each userId pair so that should not be an issue if use quorum for both read and writes. What are other issues with using consensus?

0

Reply
Priyansh Agrawal
• 4 months ago

based on the schema given for the same partition key there would be 2 rows right ?

0

Reply
Priyansh Agrawal
• 4 months ago

I couldn't think of the scenerio where CL = LOCAL_QUORUM for both read and write could result in missed match notification for the given schema in this article . This assume that user could only see feed local to his region

0

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Understand the Problem

Functional Requirements

Non-Functional Requirements

The Set Up

Planning the Approach

Defining the Core Entities

The API

High-Level Design

1) Users can create a profile with preferences (e.g. age range, interests) and specify a maximum distance.

2) Users can view a stack of potential matches

3) Users can swipe right / left on profiles one-by-one, to express "yes" or "no" on other users

4) Users get a match notification if they mutually swipe on each other

Potential Deep Dives

1) How can we ensure that swiping is consistent and low latency?

2) How can we ensure low latency for feed/stack generation?

3) How can the system avoid showing user profiles that the user has previously swiped on?

Final Design

What is Expected at Each Level?

Mid-level

Senior

Staff+
