# WhatsApp

> Source: https://www.hellointerview.com/learn/system-design/problem-breakdowns/whatsapp
> Scraped: 2026-03-30


Whatsapp is a messaging service that allows users to send and receive encrypted messages and calls from their phones and computers. Whatsapp is famously built on Erlang and renowned for handling high scale with limited engineering and infrastructure outlay.
Functional Requirements
Apps like WhatsApp and Messenger have tons of features, but your interviewer doesn't want you to cover them all. The most obvious capabilities are almost definitely in-scope but it's good to ask your interviewer if they want you to move beyond. Spending too much time in requirements will make it harder for you to give detail in the rest of the interview, so we won't dawdle too long here!
Core Requirements
Users should be able to start group chats with multiple participants (limit 100).
Users should be able to send/receive messages.
Users should be able to receive messages sent while they are not online (up to 30 days).
Users should be able to send/receive media in their messages.
That third requirement isn't obvious to everyone (but it's interesting to design) and If I'm your interviewer I'll probably guide you to it.
Below the line (out of scope)
Audio/Video calling.
Interactions with businesses.
Registration and profile management.
Non-Functional Requirements
Before getting into non-functional requirements, it might make sense to ask your interviewer how the app is used by the majority of users if you haven't used it much. Are users mostly doing 1:1 chats, or is the app for large groups? How often are people sending messages? These questions will help you to understand the system that needs to be built and while they are not explicitly "requirements" they will dictate some design decisions that come later.
Core Requirements
Messages should be delivered to available users with low latency, < 500ms.
We should guarantee deliverability of messages - they should make their way to users.
The system should be able to handle billions of users with high throughput (we'll estimate later).
Messages should be stored on centralized servers no longer than necessary.
The system should be resilient against failures of individual components.
Below the line (out of scope)
Exhaustive treatment of security concerns.
Spam and scraping prevention systems.
Adding features that are out of scope is a "nice to have". It shows product thinking and gives your interviewer a chance to help you reprioritize based on what they want to see in the interview. That said, it's very much a nice to have. If additional features are not coming to you quickly (or you've already burned some time), don't waste your time and move on. It's easy to use precious time defining features that are out of scope, which provides negligible value for a hiring decision.
Requirements
The Set Up
Planning the Approach
Before you move on to designing the system, it's important to start by taking a moment to plan your strategy for the session. For this problem, we might first recognize that 1:1 messages are simply a special case of larger chats (with 2 participants), so we'll solve for that general case of group messages even while we focus on the 1:1 case. We can also reflect a little and acknowledge that part of the design will be able durably delivering messages to users, and another is about doing so in realtime.
After this, we should be able to start our design by walking through our core requirements and solving them as simply as possible. This will get us started with a system that is probably slow and not scalable, but a good starting point for us to optimize in the deep dives.
In our deep dives we'll address scaling, optimizations, and any additional features/functionality the interviewer might want to throw on the fire.
Defining the Core Entities
In the core entities section, we'll think through the main "nouns" of our system. The intent here is to give us the right language to reason through the problem and set the stage for our API and data model.
Interviewers aren't evaluating you on what you list for core entitites, they're an intermediate step to help you reason through the problem. That doesn't mean they don't matter though! Getting the entities wrong is a great way to start building on a broken foundation - so spend a few moments to get them right and keep moving.
We can walk through our functional requirements to get an idea of what the core entities are. We need:
Users
Chats (2-100 users)
Messages
Clients (a user might have multiple devices)
We'll use this language to reason through the problem.
API or System Interface
Next, we'll want to think through the API of our system. Unlike a lot of other products where a REST API is probably appropriate, for a chat app, we're going to have high-frequency updates being both sent and received. This is a perfect use case for a bi-directional socket connection!
Pattern: Real-time Updates
WebSocket connections and real-time messaging demonstrate the broader real-time updates pattern used across many distributed systems. Whether it's chat messages, live dashboards, collaborative editing, or gaming, the same principles apply: persistent connections for low latency, pub/sub for scaling across servers, and careful state management for reliability.
Learn This Pattern
For this interview, we'll use WebSockets (over TLS for security), although a custom protocol over a raw TLS-encrypted TCP connection would also work. The idea will be that users will open the app and connect to the server, opening this socket which will be used to send and receive commands which represent our API.
As we define our API, we'll specify the commands that are sent and received over the connection by the client.
First, let's be able to create a chat.
// -> createChat
{
    "participants": [],
    "name": ""
} -> {
    "chatId": ""
}
Now we should be able to send messages on the chat.
// -> sendMessage
{
    "chatId": "",
    "message": "",
    "attachments": []
} -> {
    "status": "SUCCESS" | "FAILURE",
    "messageId": ""
}
We need a way to create attachments (note: I'm going to amend this later in the writeup).
// -> createAttachment
{
    "body": ...,
    "hash": 
} -> {
    "attachmentId": ""
}
And we need a way to add/remove users to the chat.
// -> modifyChatParticipants
{
    "chatId": "",
    "userId": "",
    "operation": "ADD" | "REMOVE"
} -> "SUCCESS" | "FAILURE"
Each of these commands will have parallel commands that are sent to other clients. When the command has been received by clients, they'll send an ack command back to the server letting it know the command has been received (and it doesn't have to be sent again)!
The message receipt acknowledgement is a bit non-obvious but crucial to making sure we don't lose messages. By forcing clients to ack, we can know for certain that the message has been delivered all the way to the client.
When a chat is created or updated ...
// <- chatUpdate
{
    "chatId": "",
    "participants": [],
} -> "RECEIVED"
When a message is received ...
// <- newMessage
{
    "chatId": "",
    "userId": ""
    "message": "",
    "attachments": []
} -> "RECEIVED"
Etc ...
Note that enumerating all of these APIs can take time! In the actual interview, I might shortcut by only writing the command names and not the full API. It's also usually a good idea to summarize the API initially before you build out the high-level design in case things need to change. "I'll come back to this as I learn more" is completely acceptable!
Our whiteboard might look like this:
Commands Exchanged
Now that we have a base to work with let's figure out how we can implement them while we satisfy our requirements.
High-Level Design
1) Users should be able to start group chats with multiple participants (limit 100)
For our first requirement, we need a way for a user to create a chat. We'll start with a simple service behind an L4 load balancer (we're using Websockets) which can write Chat metadata to a database. Let's use DynamoDB for fast key/value performance and scalability here, although we have lots of other options.
Can we use an L7 load balancer? In many cases, yes. There is wide support for Websockets in many modern L7 load balancers. But the important thing is that we don't need any L7 capabilities for this service. L7 load balancers shine when we want to, for instance, route traffic with specific paths or headers to different services. They are also helpful when we may want to spread HTTP requests across many servers even behind a single client connection. But neither of these apply here!
So using an L4 load balancer is sufficient and will generally be higher performance than a L7 load balancer.
Create a Chat
The steps here are:
User connects to the service and sends a createChat message.
The service creates a Chat record in the database along with a ChatParticipant record for each user in the chat. For small chats this can be done in a single DynamoDB transaction (up to 100 items), but for chats near the 100-participant limit we may need to batch the writes.
The service returns the chatId to the user.
On the chat table, we'll usually just want to look up the details by the chat's ID. Having a simple primary key on the chat id is good enough for this.
For the ChatParticipant table, we'll want to be able to (1) look up all participants for a given chat and (2) look up all chats for a given user.
We can do this with a composite primary key where chatId is the partition key and participantId is the sort key. A Query on the chatId partition key will return all participants for a given chat.
We'll need a Global Secondary Index (GSI) with participantId as the partition key and chatId as the sort key. This will allow us to efficiently query all chats for a given user. The GSI will automatically be kept in sync with the base table by DynamoDB.
Great! We got some chats. How about messages?
2) Users should be able to send/receive messages.
To allow users to send/receive messages, we're going to need to start taking advantage of the websocket connection that we established. To keep things simple while we get off the ground, let's assume we have a single host for our Chat Server.
This is obviously a terrible solution for scale (and you might say so to your interviewer to keep them from itching), but it's a good starting point that will allow us to incrementally solve those problems as we go.
For infrastructure-style interviews, I highly recommend reasoning about a solution on a single node first. Oftentimes the path to scale is straightforward from there.
If you solve scale first without thinking about how the actual mechanics of your solution work underneath, you're more likely to back yourself into a corner.
When users make Websocket connections to our Chat Server, we'll want to keep track of their connection with a simple in-memory hash map which will map a user id to a websocket connection. This way we know which users are connected and can send them messages.
To send a message:
User sends a sendMessage message to the Chat Server.
The Chat Server looks up all participants in the chat via the ChatParticipant table.
The Chat Server looks up the websocket connection for each participant in its internal hash table and sends the message via each connection.
We're making some really strong assumptions here! We're assuming all users are online, connected to the same Chat Server, and that we have a websocket connection for each of them. But under those conditions this works! So let's keep going.
3) Users should be able to receive messages sent while they are not online (up to 30 days).
With our next requirement, we're going to need to start storing messages in our database so that we can deliver them to users even when they're offline. We'll take this as an opportunity to add some robustness to our system.
Let's keep an "Inbox" for each user which will contain all undelivered messages. When messages are sent, we'll write them to the inbox of each recipient user. If they're already online, we can go ahead and try to deliver the message immediately. If they're not online, we'll store the message and wait for them to come back later.
How much write throughput does this add? The vast majority of chats are 1:1, and the average user sends about 20 messages per day. With 200M active users, that's 4B messages/day or roughly 40K messages/second. For each message in a 1:1 chat, we write once to Messages and once to Inbox (for the recipient). Even accounting for group chats, we're looking at roughly 100K writes/second — well within DynamoDB's capabilities with userId as the partition key.
Send a Message
So, to send a message:
Sender sends a sendMessage message to the Chat Server.
The Chat Server looks up all participants in the chat via the ChatParticipant table.
The Chat Server (a) writes the message to our Message table and (b) creates an entry in our Inbox table for each recipient.
The Chat Server returns a SUCCESS or FAILURE to the sender with the final message id.
The Chat Server looks up the websocket connection for each participant and attempts to deliver the message to each of them via newMessage.
(For connected clients) Upon receipt, the client will send an ack message to the Chat Server to indicate they've received the message. The Chat Server will then delete the message from the Inbox table.
For clients who aren't connected, we'll keep their messages in the Inbox table for some time. Later, when the client decides to connect, we'll:
Look up the user's Inbox and find any undelivered message IDs.
For each message ID, look up the message in the Message table.
Write those messages to the client's connection via the newMessage message.
Upon receipt, the client will send an ack message to the Chat Server to indicate they've received the message.
The Chat Server will then delete the message from the Inbox table.
Finally, we'll need to periodically clean up the old messages in the Inbox and messages tables. We can do this by setting a TTL on the items of the tables.
Great! We knocked out some of the durability issues of our initial solution and enabled offline delivery. Our solution still doesn't scale and we've got a lot more work to do, so let's keep moving.
4) Users should be able to send/receive media in their messages.
Our final requirement is that users should be able to send/receive media in their messages.
Users sending and receiving media is annoying. It's bandwidth- and storage- intensive. While we could potentially do this with our Chat Server and database, it's better to use purpose-built technologies for this. This is in fact how Whatsapp actually works: attachments are uploaded via a separate HTTP service.

Bad Solution: Keep attachments in DB

Good Solution: Send attachments via chat server

Great Solution: Manage attachments separately

Ok awesome, so we have a system which has real-time delivery of messages, persistence to handle offline use-cases, and attachments. It just doesn't scale ... yet!
Potential Deep Dives
With the core functional requirements met, it's time to dig into the non-functional requirements via deep dives and solve some of the issues we've earmarked to this point. This includes solving obvious scalability issues as well as auxiliary questions which demonstrate your command of system design.
The degree to which a candidate should proactively lead the deep dives is a function of their seniority. In this problem, all levels should be quick to point out that my single-host solution isn't going to scale. But beyond these bottlenecks, it's reasonable in a mid-level interview for the interviewer to drive the majority of the deep dives. However, in senior and staff+ interviews, the level of agency and ownership expected of the candidate increases. They should be able to proactively look around corners and identify potential issues with their design, proposing solutions to address them.
1) How can we handle billions of simultaneous users?
Our single-host system is convenient but unrealistic. Serving billions of users via a single machine isn't possible and it would make deployments and failures a nightmare. So what can we do? The obvious answer is to try to scale out the number of Chat Servers we have.
If we have 1b users, we might expect 200m of them to be connected at any one time. Whatsapp famously served 1-2m users per host, but this will require us to have hundreds of chat servers. That's a lot of simultaneous connections (!).
Note that I've included some back-of-the-envelope calculations here. Your interviewer will likely expect them, but you'll get more mileage from your calculations by doing them just-in-time: when you need to figure out a scaling bottleneck.
Adding more chat servers also introduces some new problems: now the sending and receiving users might be connected to different hosts. If User A is trying to send a message to User B and C via Chat Server 1, but User C is connected to Chat Server 2, we're going to have a problem.
Host Confusion
The issue is one of of routing: we need to route messages to the right Chat Servers in order to deliver them. We have a few options here which are discussed in greatest depth in the Realtime Updates Deep Dive.

Bad Solution: Naively horizontally scale

Bad Solution: Keep a kafka topic per user

Good Solution: Consistent Hashing of Chat Servers

Great Solution: Offload to Pub/Sub

Should We Partition By Chat Or By User?
You may have the idea: "why do we have the pub/sub topics/channels be per user rather than per chat?", or maybe your interviewer asks you about this! The right choice is going to depend on (a) the number of chats per user, and (b) the size of those chats. Let's consider two scenarios to make this clear:

Scenario 1: Users have 250 chats each, but each chat has 1 other participant (1:1 chats).

Scenario 2: Users have 1 chat each, but each chat has 100 participants.

So which is right for this problem? Whatsapp is dominated by 1:1 chats. Having hundreds of redundant channels stresses Redis for little benefit. We also explicitly put a limit on the number of participants per chat to 100.
For more senior candidates you might be asked to discuss additional efficiencies you can eke out here. This is an example of a "celebrity problem" where an uncommon edge case (large chats) is disproportionately impacting the system. If this is a problem you want to solve, a good solution is to adaptively change the partitioning strategy based on the size of the chat.
When users connect, we'll list out all the chats they are part of which are larger than some threshold (say, 25 users). They'll subscribe to channels for those chats specifically in addition to the user-level channels. When a message is sent, if the chat is larger than the threshold, we'll publish to the chat-level channel instead of the user-level channel. There's edge cases here: you need to be careful that you give time for the chat servers to subscribe when the chat size changes, so you might be publishing to both channels for a short time.
2) What do we do to handle multiple clients for a given user?
To this point we've assumed a user has a single device, but many users have multiple devices: a phone, a tablet, a desktop or laptop - maybe even a work computer. Imagine my phone had received the latest message but my laptop was off. When I wake it up, I want to make sure that all of the latest messages are delivered to my laptop so that it's in sync. We can no longer rely on the user-level "Inbox" table to keep track of delivery!
Having multiple clients/devices introduces some new problems:
First, we'll need to add a way for our design to resolve a user to 1 or more clients that may be active at any one time.
Second, we need a way to deactivate clients so that we're not unnecessarily storing messages for a client which does not exist any longer.
Lastly, we need to update our message delivery system so that it can handle multiple clients.
Let's see if we can account for this with minimal changes to our design.
We'll need to create a new Clients table to keep track of clients by user id.
When we look up participants for a chat, we'll need to look up all of the clients for that user.
We'll need to update our Inbox table to be per-client rather than per-user.
When we send a message, we'll need to send it to all of the clients for that user.
On the pub/sub side, nothing needs to change. Chat servers will continue to subscribe to a topic with the userId.
We'll probably want to introduce some limits (3 clients per account) to avoid blowing up our storage and throughput.
Adding clients
3) What happens if the WebSocket connection fails?
Users often sit on poor network connections. The WebSocket may technically be open, but the connection is functionally severed—we won't know until we try to send a message and it times out. TCP keepalives can take minutes to detect a dead connection, which is far too slow for a chat app. How can we make sure our users aren't impacted?

Bad Solution: Rely on TCP Timeouts

Good Solution: ACK Timeouts with Server-Side Retry

Great Solution: Application-Level Heartbeats

4) What happens if Redis fails to deliver a message?
Redis Pub/Sub is "at most once"—if there's no subscriber listening or Redis has a transient failure, the message is lost. We've already handled durability by writing to the Inbox before publishing to Pub/Sub (importantly this means all messages will eventually get delivered), but how do we ensure connected clients quickly receive messages that Pub/Sub dropped?

Good Solution: Periodic Polling

Good Solution: Sequence Numbers per Chat with Gap Detection

Great Solution: Piggyback Sequence on Heartbeats

In practice, most production systems combine these strategies: heartbeats detect dead WebSocket connections, sequence numbers on to detect missed messages, and periodic polling serves as a final backstop.
5) How do we handle out-of-order messages?
The simple answer is: we don't, or at least not directly.
Out-of-order messages are a fact of life in distributed systems and engineering such that messages are processed in the exact order they were sent is actually a considerable amount of additional complexity. We'd need to have delays to ensure we have time for late messages to arrive and a re-ordering mechanism to handle them. You can see an example in our Flink deep dive where Flink's Bounded Out-Of-Orderness Watermark Strategy effectively waits for late messages to arrive before processing them.
But for apps like this, it's not how they work! Users would rather see new messages as quickly as possible than guarantee order. So what do we do?
All of the Chat Servers will sync their time over NTP (Network Time Protocol). This doesn't guarantee perfect time, but it's pretty good. When a message arrives on the Chat Server, we'll "stamp" it with the time it was received. Then, when clients retrieve messages, they'll have the timestamp that they were received by the server. When we display messages, we display them ordered by this time. Messages have a consistent ordering across all clients even if they arrive in a different order than they are displayed.
On occasion, this will mean a message will pop-in "above" another message that was actually sent later. Users find this acceptable!
6) How can we handle a "last seen" functionality?
Our interviewer asks "how can we add a 'last seen' functionality to chats, which shows you when the other person was last online?"
Ideally, we want a solution that is both efficient and scalable.

Bad Solution: Write to DB on every heartbeat

Great Solution: Utilize Active Connections

What is Expected at Each Level?
Ok, that was a lot. You may be thinking, “how much of that is actually required from me in an interview?” Let’s break it down.
Mid-level
Breadth vs. Depth: A mid-level candidate will be mostly focused on breadth (80% vs 20%). You should be able to craft a high-level design that meets the functional requirements you've defined, but many of the components will be abstractions with which you only have surface-level familiarity.
Probing the Basics: Your interviewer will spend some time probing the basics to confirm that you know what each component in your system does. For example, if you use websockets, expect that they may ask you what it does and how they work (at a high level). In short, the interviewer is not taking anything for granted with respect to your knowledge.
Mixture of Driving and Taking the Backseat: You should drive the early stages of the interview in particular, but the interviewer doesn’t expect that you are able to proactively recognize problems in your design with high precision. Because of this, it’s reasonable that they will take over and drive the later stages of the interview while probing your design.
The Bar for Whatsapp: For this question, an E4 candidate will have clearly defined the API, landed on a high-level design that is functional and meets the requirements. Their scaling solution will have rough edges but they'll have some knowledge of its flaws.
Senior
Depth of Expertise: As a senior candidate, expectations shift towards more in-depth knowledge — about 60% breadth and 40% depth. This means you should be able to go into technical details in areas where you have hands-on experience. It's crucial that you demonstrate a deep understanding of key concepts and technologies relevant to the task at hand.
Advanced System Design: You should be familiar with advanced system design principles. For example, knowing about the consistent hashing for this problem is essential. You’re also expected to understand the mechanics of long-running sockets. Your ability to navigate these advanced topics with confidence and clarity is key.
Articulating Architectural Decisions: You should be able to clearly articulate the pros and cons of different architectural choices, especially how they impact scalability, performance, and maintainability. You justify your decisions and explain the trade-offs involved in your design choices.
Problem-Solving and Proactivity: You should demonstrate strong problem-solving skills and a proactive approach. This includes anticipating potential challenges in your designs and suggesting improvements. You need to be adept at identifying and addressing bottlenecks, optimizing performance, and ensuring system reliability.
The Bar for Whatsapp: For this question, E5 candidates are expected to speed through the initial high level design so you can spend time discussing, in detail, scaling and robustness issues in the design. You should also be able to discuss the pros and cons of different architectural choices (like partitioning by chat or user), especially how they impact scalability, performance, and maintainability.
Staff+
Emphasis on Depth: As a staff+ candidate, the expectation is a deep dive into the nuances of system design — I'm looking for about 40% breadth and 60% depth in your understanding. This level is all about demonstrating that, while you may not have solved this particular problem before, you have solved enough problems in the real world to be able to confidently design a solution backed by your experience.
You should know which technologies to use, not just in theory but in practice, and be able to draw from your past experiences to explain how they’d be applied to solve specific problems effectively. The interviewer knows you know the small stuff so you can breeze through that at a high level so you have time to get into what is interesting.
High Degree of Proactivity: At this level, an exceptional degree of proactivity is expected. You should be able to identify and solve issues independently, demonstrating a strong ability to recognize and address the core challenges in system design. This involves not just responding to problems as they arise but anticipating them and implementing preemptive solutions. Your interviewer should intervene only to focus, not to steer.
Practical Application of Technology: You should be well-versed in the practical application of various technologies. Your experience should guide the conversation, showing a clear understanding of how different tools and systems can be configured in real-world scenarios to meet specific requirements.
Complex Problem-Solving and Decision-Making: Your problem-solving skills should be top-notch. This means not only being able to tackle complex technical challenges but also making informed decisions that consider various factors such as scalability, performance, reliability, and maintenance.
Advanced System Design and Scalability: Your approach to system design should be advanced, focusing on scalability and reliability, especially under high load conditions. This includes a thorough understanding of distributed systems, load balancing, caching strategies, and other advanced concepts necessary for building robust, scalable systems.
The Bar for Whatsapp: For a staff+ candidate, expectations are high regarding depth and quality of solutions, particularly for the complex scenarios discussed earlier. Great candidates are going 2 or 3 levels deep to discuss failure modes, bottlenecks, and other issues with their design. There's ample discussion to be had around fault tolerance, database optimization, regionalization and cell-based architecture and more.
References
What Happens When You Make a Move in Lichess
Test Your Knowledge

Take a quick 15 question quiz to test what you've learned.

Start Quiz

Mark as read

Next: Yelp

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

(657)

Comment
Anonymous
​
Sort By
Popular
Sort By
N
NavalMaroonOtter533
• 1 year ago

Thank you SO much for these incredible answer keys. I have a question about handling when clients go offline. I see you mentioned:

Since our clients can go offline, we'll need to be able to "sync" state between the client and server. For convenience, let's just assume the server will buffer events sent while the client is offline and, when the client connects, it receives all unsent messages.

In the pub/sub solution, will this mean that messages will stay in a Redis event topic for that user until they come back online? If so won't that cause some sort of back pressure on Redis if a user accumulates a ton of unseen messages? Or maybe there's a separate message sync queue that the messages get moved to? I'm so curious!

14

Reply
W
WorldwideBrownMollusk575
• 1 year ago

I can take a stab at this. Perhaps one thing would be that these messages are only via the redis pub/sub to online clients. For example if a client disconnects, that particular instance of the chat server no longer maintains connectionId of the respective client to send to.

When a client comes online, it will fetch all events from the DB with a state of not_delivered for example (perhaps via HTTP or we can use our websocket connection to send these on connect). Since we're offering message guarantees through our backend, the client can confirm that they've received this on the next online connection.

14

Reply
R
RainyCyanHippopotamus256
Top 10%
• 1 year ago

How will we handle scenarios when the client is online but the persistent connection between the server and redis cluster breaks for a while and then reestablishes again? At this point , we will have undelievered messages and also live messages hitting through pub-sub simultaneously after the connection is restablished. How will we consolidate both these type of messages while ensuring ordering guarantees?

4

Reply

Stefan Mai

Admin
• 1 year ago

Stamp the messages on ingestion. Order them on the client. Good enough for chat.

5

Reply
R
RainyCyanHippopotamus256
Top 10%
• 1 year ago

Yes, we can offload ordering on the client side by having the messages stamped with timestamp. But, still the low-level implementation or handling of the above scenario looks non-trivial atleast to me.

Will we always check for undelivered messages from the DB in the method which gets the redis pub-sub messages so that we always deliever the undelievered messages? This is sub-optimal. Also, polling at regular intervals won't work. I think it would be easier to implement this via redis streams which allows us to send ACKs and start from the previously left offset.

1

Reply
C
ChemicalCopperIguana997
Top 10%
• 1 year ago

We can add some id on ingestion and when client gets real time messages from redis , it might find some ids missing based on last message received. It can query db for missed messages.
On every reconnection, client can have a db call

1

Reply
YOUNG M
• 1 year ago

can we checkpointing each client on the servers-side, and upon the new/reconnection, it will have a separate service read all the messages since that checkpoint and push to clients via the websocket?

2

Reply
P
ProperLimePython690
• 2 months ago

We can buffer the new messages from redis on chat server once the connection with redis is reestablished, at the same time we can query dynamo to get all the messages from a given timestamp. We can create a in memory priority queue on the chat servers for these messages and return the messages in order to the client.

0

Reply
N
NavalMaroonOtter533
• 1 year ago

Ahhh ok that makes sense, thank you! I think I was mistakenly thinking of pub/sub as more of a queue than publisher subscriber model. Thanks!

3

Reply

Stefan Mai

Admin
• 1 year ago

Thanks ZerothIndigoSalamander112 and great question ContinuedBeigeSwift112. The pub/sub solution is indeed "at most once" delivery - so we use it as a fast path but we need a secondary path to make sure messages are eventually delivered in the degenerate case. But nothing is stored on the pub/sub server besides a socket map.

3

Reply
T
TechnicalScarletJellyfish241
• 1 year ago

Thanks for the reply Stefan, spent some time thinking and read this comment and it makes complete sense.

0

Reply
M
MotionlessLavenderPelican114
• 1 year ago

Thanks for this comment! I also mistaken pub/sub as message queue , and had the same question. It makes total sense to me now knowing that pub/sub does not retain messages

0

Reply
he she
• 1 year ago

Not sure if my understanding it right here. Please correct me if it is wrong!

It seems the main difference between the BAD solution keep a KAFKA topic per user vs GREAT solution offload to Pub/Sub is using KAFKA or Redis??

Because it looks like both solutions are very similar which need to:
1 create a topic per users
2 subscribe to the topics of the users who are connected to the chat sever.
3 publish the message to the users' topics
4 send the message to users via the websockets.

Also, since a user(assuming no multiple clients) can connect to one chat server at a time, does it mean for each user Id topic, it only can have one subscriber which is the chat server that the user is connected to?  Although multiple chat servers may publish message there to that user.

am I missing something else?

12

Reply
L
LogicalAmethystToad166
Top 5%
• 11 months ago

Topic per user is simply impossible. In production, we would most likely have a "live-messages" topic or something and it would have multiple partitions where users would map to these partitions via some sort of consistent hashing.. Topic per user in Kafka, with millions of active people at a time, is simply not possible, beyond Kafka's or many modern queue'ing technologies scope.. Correct me if I'm wrong here

13

Reply
P
ProperLimePython690
• 2 months ago

Kafka can only handle around 10k-20k topics. Redis pub sub can scale to million of topics as Redis treats each channel as a lightweight pointers in RAM.

3

Reply
Dmitry Oksenchuk
• 2 months ago

https://stackoverflow.com/questions/32950503/can-i-have-100s-of-thousands-of-topics-in-a-kafka-cluster

Update March 2021: With Kafka's new KRaft mode, which entirely removes ZooKeeper from Kafka's architecture, a Kafka cluster can handle millions of topics/partitions. See https://www.confluent.io/blog/kafka-without-zookeeper-a-sneak-peek/ for details.

1

Reply
Pranav Cool
• 1 month ago

subscribing is something consumers do, not producers.

0

Reply
A
AddedLimeCarp593
Top 1%
• 10 months ago

Not super clear on why Redis pubsub is the preferred solution here instead of consistent hashing w/ Zookeeper. They both suffer from the same problems:

Hot nodes
Need to carefully redistribute connections on a scaling event

Plus Redis suffers from additional latency, weak at-most-once delivery and MxN connections which are problems the Zookeeper solution doesn't have.

7

Reply

Stefan Mai

Admin
• 2 months ago

I've added some clarifications here. The pub/sub solution is preferred for an interview because it works and it sidesteps a bunch of incidental complexity that you need to be able to handle with a consistent hashing solution (e.g. orchestrating node removals or additions, mitigating the all-to-all challenges, etc). But the consistent hashing approach is valid and if you have the depth to be able to answer those questions it can work.

1

Reply
A
AssistantVioletCardinal950
Top 10%
• 1 year ago

Hi Stefan,
The article was good and very helpful, particularly the Redis approach. I have one clarification.

The reading from Inbox, we have messageId. So querying the Message table will be scatter and gather the result. This will increase the IOPS. What if we do some tradeoff on storage and store the message content in the Inbox itself. Anyway we are going to purge the data once delivered to the client. Let me know your opinion on this.

5

Reply

Stefan Mai

Admin
• 1 year ago

It's a good question (one your interviewer might ask). What do you think the tradeoffs are?

1

Reply
A
AssistantVioletCardinal950
Top 10%
• 1 year ago

The tradeoff are as follows

Message table - Scatter and Gather:
Pros: Storage is optimized - that is the message content is stored only once.
Cons: a) Two queries - one to get the messageId from Inbox and other to get content from Messages. More IOPS, query is expensive - it has to execute in multiple shards and merge the results.

Message content in Inbox:
Pros: Only one query and if the sort key is clientId - then mostly probably one disk seek is enough. It can improve the p99.
Cons: Storage is high. Message content is duplicated for all offline members.

My take: I will go with storing the message content in Inbox - because the storage cost is less than compute cost (anyway we are going to purge the data) and one query is enough to fetch the message.
May be hybrid approach might work - larger message size store it in the Message table and store the content in Inbox for shorter message. But not sure whether this is over engineering.

Please let me know your opinion on this.

Show More

10

Reply

Stefan Mai

Admin
• 1 year ago

Good discussion. I think you're right, having all the messages colocated in the Inbox saves a lot of random access. The one exception would be if the majority of users are connected and messages are larger than 4kb, in which case we can minimize the write throughput. But if we assume messages are small, the overall bandwidth is irrelevant from Dynamo's perspective.

I'll earmark this to make updates to the guide. Appreciate the thinking here!

6

Reply
E
ElectricRedOwl923
• 1 year ago

Instead of inbox message partitioned by user, why not message table partitioned by chatId (unique globally)? I assume when a user loads historical messages, he would load one chat at a time by opening the chat window. So he will just access the partition containing the chatId, load the unseen messages.

0

Reply
A
AssistantVioletCardinal950
Top 10%
• 1 year ago

Thank you!!

0

Reply
R
RepresentativeLimeHarrier694
Top 10%
• 1 year ago

i am still not convinced how you are fanning out efficiently.
so on each message; the chat server has to

save the new message to messages table
look up chat participants from cache, and save up to 100 new rows in events table
send a msg on redis channels for 100 subscribers. how is this scaling?

3

Reply
Stan
Premium
• 5 months ago

how is this scaling?

I guess the N=100 is selected intentionally and it's somehow a threshold for which fan-out on write still works. For larger rooms, Telegram might be a great architectural example. -> fan-out on Read using pointers (e.g. tracking last_seen_message_id for every Room, fetch delta on reconnect, etc)

0

Reply
C
CommonAmaranthBird910
Premium
• 6 months ago

You could have a MessageCreated topic and have all of these operations be handled by workers reading from that topic and scale out that way, none of those things need to be done synchronously in the new message flow

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

Defining the Core Entities

API or System Interface

High-Level Design

1) Users should be able to start group chats with multiple participants (limit 100)

2) Users should be able to send/receive messages.

3) Users should be able to receive messages sent while they are not online (up to 30 days).

4) Users should be able to send/receive media in their messages.

Potential Deep Dives

1) How can we handle billions of simultaneous users?

2) What do we do to handle multiple clients for a given user?

3) What happens if the WebSocket connection fails?

4) What happens if Redis fails to deliver a message?

5) How do we handle out-of-order messages?

6) How can we handle a "last seen" functionality?

What is Expected at Each Level?

Mid-level

Senior

Staff+

References
