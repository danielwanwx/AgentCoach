# Distributed Cache

> Source: https://www.hellointerview.com/learn/system-design/problem-breakdowns/distributed-cache
> Scraped: 2026-03-30


A distributed cache is a system that stores data as key-value pairs in memory across multiple machines in a network. Unlike single-node caches that are limited by the resources of one machine, distributed caches scale horizontally across many nodes to handle massive workloads. The cache cluster works together to partition and replicate data, ensuring high availability and fault tolerance when individual nodes fail.
Functional Requirements
Core Requirements
Users should be able to set, get, and delete key-value pairs.
Users should be able to configure the expiration time for key-value pairs.
Data should be evicted according to Least Recently Used (LRU) policy.
Below the line (out of scope)
Users should be able to configure the cache size.
We opted for an LRU eviction policy, but you'll want to ask your interviewer what they're looking for if they weren't explicitly upfront. There are, of course, other eviction policies you could implement, like LFU, FIFO, and custom policies.
Non-Functional Requirements
At this point in the interview, you should ask the interviewer what sort of scale we are expecting. This will have a big impact on your design, starting with how you define the non-functional requirements.
If I were your interviewer, I would say we need to store up to 1TB of data and expect to handle a peak of up to 100k requests per second.
Core Requirements
The system should be highly available. Eventual consistency is acceptable.
The system should support low latency operations (< 10ms for get and set requests).
The system should be scalable to support the expected 1TB of data and 100k requests per second.
Below the line (out of scope)
Durability (data persistence across restarts)
Strong consistency guarantees
Complex querying capabilities
Transaction support
Note that I'm making quite a few strong assumptions about what we care about here. Make sure you're confirming this with your interviewer. Chances are you've used a cache before, so you know the plethora of potential trade-offs. Some interviewers might care about durability, for example, just ask.
The Set Up
Planning the Approach
For a problem like this, you need to show flexibility when choosing the right path through the Hello Interview Delivery Framework. In fact, this is a famous question that is asked very differently by different interviewers at different companies. Some are looking for more low-level design, even code in some instances. Others are more focused on how the system should be architected and scaled.
In this breakdown, we'll follow the most common path (and the one I take when I ask this question) where we balance low-level design with a high-level design that is scalable and handles the expected load.
I'm going to opt for documenting the core entities and the API, but in an actual interview I would not spend a lot of time on these two sections, recognizing they're largely trivial. I'd either skip them, or rush through them to spend time on my high-level design and deep dives.
Defining the Core Entities
The core entities are right there in front of our face! We're building a cache that stores key-value pairs, so our entities are keys and values.
In other words, the data we need to persist (in memory) are the keys and their associated values.
The API
According to our functional requirements, we have three key operations that we'll need to expose via an API: set, get, and delete.
These should each be rather straightforward, so we can breeze through this.
Identifying where to spend more and less time in a system design interview based on where the challenges are is an important skill to have. Spending time on simple, auxiliary, or otherwise less important parts of the system is a recipe for running out of time.
Setting a key-value pair:
POST /:key
{
  "value": "..."
}
Getting a key-value pair:
GET /:key -> {value: "..."}
Deleting a key-value pair:
DELETE /:key
High-Level Design
We start by building an MVP that works to satisfy the core functional requirements. This doesn't need to scale or be perfect. It's just a foundation for us to build upon later. We will walk through each functional requirement, making sure each is satisfied by the high-level design.
1) Users should be able to set, get, and delete key-value pairs
Let's start with the absolute basics. No fancy distributed systems yet - just a working cache that handles gets, sets, and deletes.
At its core, a cache is just a hash table. Every programming language has one: Python's dict, Java's HashMap, Go's map. They're perfect for this because they give us O(1) lookups and inserts.
Your interviewer may ask you to sketch out some pseudocode. Here is what that might look like:
class Cache:
    data = {}  # Simple hash table

    get(key):
        return self.data[key]

    set(key, value):
        self.data[key] = value

    delete(key):
        delete self.data[key]
When asked to write pseudocode in a design interview, don't worry about the syntax. Just focus on the logic. You'll note that I don't handle corner cases like key not found or key already exists. No worries, that's not the point here.
That said, as always, it's worth confirming this with your interviewer. "I'm going to write some pseudocode, is it ok that it's not syntactically correct or missing some details?"
That's it. Three operations, all O(1). The hash table handles collision resolution and dynamic resizing for us.
We can host this code on a single server. When a user makes a API request, we'll parse the request, and then call the appropriate method on our Cache instance, returning the appropriate response.
Simple Cache
Now, this isn't production-ready. It'll fall over if we try to handle real traffic or store too much data. But it's a solid foundation that meets our core functional requirement: storing and retrieving key-value pairs.
2) Users should be able to configure the expiration time for key-value pairs
Let's add expiration functionality to our cache. We'll need to store a timestamp alongside each value and check it during reads. We'll also need a way to clean up expired entries.
The pseudocode below shows how we can modify our cache to support TTLs (Time To Live). The key changes are:
Instead of storing just values, we now store tuples of (value, expiry_timestamp)
The get() method checks if the entry has expired before returning it
The set() method takes an optional TTL parameter and calculates the expiry timestamp
This gives us the ability to automatically expire cache entries after a specified time period, which is necessary for keeping the cache fresh and preventing stale data from being served.
# Check the expiry time of the key on get
get(key):
    (value, expiry) = data[key]
    if expiry and currentTime() > expiry:
        # Key has expired, remove it
        delete data[key]
        return null
        
    return value

# Set the expiry time of the key on set
set(key, value, ttl):
    expiry = currentTime() + ttl if ttl else null
    data[key] = (value, expiry)
This handles the basic TTL functionality, but there's a problem: expired keys only get cleaned up when they're accessed. This means our cache could fill up with expired entries that nobody is requesting anymore.
To fix this, we need a background process (often called a "janitor") that periodically scans for and removes expired entries:
cleanup():    
    # Find all expired keys and delete
    for key, value in data:
        if value.expiry and current_time > value.expiry:
            delete data[key]
Simple Cache with TTLs
This cleanup process can run on a schedule (say every minute) or when memory pressure hits certain thresholds. The trade-off here is between CPU usage (checking entries) and memory efficiency (removing expired data promptly).
Now we have TTL support, but we still need to handle memory constraints. That's where our next requirement comes in: LRU eviction.
3) Data should be evicted according to LRU policy
Now we need to handle what happens when our cache gets full. We'll use the Least Recently Used (LRU) policy, which removes the entries that haven't been accessed for the longest time.
Make sure you've confirmed with your interviewer that you're implementing an LRU cache. They may have a different eviction policy in mind, or even ask that your implementation is configurable.
We have a challenge: we need to find items quickly AND track which items were used least recently. If we just used a hash table, we could find items fast but wouldn't know their access order. If we just used a list, we could track order but would be slow to find items.
The solution is to combine two data structures:
A hash table for O(1) lookups - This gives us instant access to any item in the cache
A doubly linked list to track access order - This lets us maintain a perfect history of which items were used when
Together, these structures let us build an efficient LRU cache where both get and set operations take O(1) time.
When we add or access an item:
We create a Node object containing the key, value, and expiry time
We add an entry to our hash table mapping the key to this Node
We insert the Node at the front of our doubly-linked list (right after the dummy head)
If we're at capacity, we remove the least recently used item from both the hash table and the linked list
The doubly-linked list maintains the exact order of access - the head of the list contains the most recently used items, and the tail contains the least recently used. When we need to evict an item, we simply remove the node right before our dummy tail.
For example, if we add items A, B, C to a cache with capacity 2:
Add A: [A]
Add B: [B -> A]
Add C: Cache is full, evict A (least recently used), resulting in [C -> B]
When we access an existing item, we:
Look up its Node in our hash table (O(1))
Remove the Node from its current position in the list (O(1))
Move it to the front of the list (O(1))
This way, frequently accessed items stay near the head and are safe from eviction, while rarely used items drift towards the tail where they'll eventually be removed when space is needed.
The hash table gives us O(1) lookups, while the doubly-linked list gives us O(1) updates to our access order. By combining them, we get the best of both worlds - fast access and efficient LRU tracking.
Here is some pseudocode for the implementation:
class Node # Node in our doubly-linked list storing values and expiry times

class Cache:
    get(key):
        # get the node from the hash table
        node = data[key]
        
        # Check if the entry has expired
        if node.expiry and currentTime() > node.expiry:
            # Remove expired node from both hash table and linked list
            delete data[key]
            delete node
            return null
            
        # Move node to front of list
        move_to_front(node)
        return node.value

    set(key, value, ttl):
        # Calculate expiry timestamp if TTL is provided
        expiry = currentTime() + ttl if ttl else null
        
        if key in data:
            # Update existing entry
            node = data[key]
            node.value = value
            node.expiry = expiry
            move_to_front(node)
        else:
            # Add new entry
            node = Node(key, value, expiry)
            data[key] = node
            add_node(node)
            
            # If over capacity, remove least recently used item
            if size > capacity:
                lru = tail.prev
                delete lru
                delete data[lru.key]

    cleanup():
        expired_keys = []
        
        # Scan from LRU end towards head
        current = tail.prev
        while current != head:
            if current.expiry and currentTime() > current.expiry:
                expired_keys.add(current.key)
            current = current.prev
            
        # Remove expired entries
        for key in expired_keys:
            node = data[key]
            delete data[key]
            delete node
The code examples provided here are meant to illustrate core concepts and are intentionally simplified for clarity. A production implementation would need to handle many additional concerns including thread safety, error handling, monitoring, and performance optimizations.
Simple LRU Cache
The clever part about this implementation is that all operations (get, set, and even eviction) remain O(1). When we access or add an item, we move it to the front of the list. When we need to evict, we remove from the back.
Potential Deep Dives
Ok, truth be told, up until this point this has been more of a low level design interview than pure system design, but the deep dives is where that changes and we discuss how we turn our single, in-memory cache instance into a distributed system that can meet our non-functional requirements.
For these types of deeper infra questions, the same pattern applies where you should try to lead the conversation toward deep dives in order to satisfy your non-functional requirements. However, it's also the case that your interviewer will likely jump in and hit you with probing questions, so be prepared to be flexible.
Here are some of the questions I'll usually ask (or a candidate could do this proactively).
1) How do we ensure our cache is highly available and fault tolerant?
Our high-level design works great on a single node, but what happens when that node fails? In a production environment, we need our cache to stay available even when things go wrong. Let's look at how we can make that happen.
The key challenge here is data replication - we need multiple copies of our data spread across different nodes. But this opens up a whole new set of questions:
How many copies should we keep?
Which nodes should store the copies?
How do we keep the copies in sync?
What happens when nodes fail or can't communicate?
There are several well-established patterns for handling this. Each has its own trade-offs between consistency, availability, and complexity.
These patterns extend far beyond distributed caches - they're fundamental building blocks for achieving high availability and fault tolerance in any distributed system, from databases to message queues.

Bad Solution: Synchronous Replication

Good Solution: Asynchronous Replication

Good Solution: Peer-to-Peer Replication

All of the above approaches could be good depending on your specific use case and constraints. Redis, for example, uses asynchronous replication by default, though it does provide a WAIT command that allows clients to wait for replica acknowledgement if needed (sometimes called "semi-synchronous" behavior). Other distributed systems allow you to configure the replication type in order to choose the right trade-offs for your workload.
In your interview, I'd discuss the options with your interviewer. It's likely they care less about you making a decision here and more about seeing that you're aware of the options and trade-offs.
Given our requirements, I'd discuss two options with my interviewer:
Asynchronous replication for a good balance of availability and simplicity
Peer-to-peer for maximum scalability
The reality is, there is no single right answer here.
2) How do we ensure our cache is scalable?
Designing a reliable, single-node cache is a good start, but it won't meet the lofty non-functional requirements of handling 1TB of data or sustaining 100k requests per second. We need to spread the load across multiple machines to maintain low latency and high availability as we grow. This is where scaling strategies come into play, and one of the core tactics is to distribute data and requests intelligently.
We can't fit 1TB of data efficiently on a single node without hitting memory and performance limits. We need to split—or shard—our key-value pairs across multiple nodes. If done well, each node will hold a manageable portion of the dataset, allowing us to scale horizontally by simply adding more machines.
What is the difference between partitioning and sharding? Technically, partitioning refers to splitting data within a single database/system, while sharding specifically means splitting data across multiple machines/nodes. However, you'll hear these terms used interchangeably in practice - when someone mentions "partitioning" in a distributed systems context, they very likely mean distributing data across different nodes (sharding). The key thing is to understand the core concept of splitting data, regardless of which term is used.
We can estimate the number of nodes needed by considering both our throughput and storage requirements. Let's start with throughput. Let's assume we've benchmarked a single host to be able to perform 20,000 requests per second - we would need at least 100,000 / 20,000 = 5 nodes to handle our throughput requirements. Adding some buffer for traffic spikes and potential node failures, we should plan for around 8 nodes minimum to handle our throughput needs.
For storage requirements, we need to consider that a typical AWS instance with 32GB RAM can reliably use about 24GB for cache data after accounting for system overhead. Since we need to store 1TB (1024GB) of data, we would need approximately 1024GB / 24GB = 43 nodes just for storage. Adding some buffer for data growth and operational overhead, we should plan for about 50 nodes.
Note that the throughput (20k requests/second) and memory capacity (24GB usable from 32GB RAM) estimates used above are rough approximations for illustration. Actual performance will vary significantly based on hardware specs, cache configuration, access patterns, and the nature of your cached data. Always benchmark with your specific workload to determine true capacity needs.
Since our storage-based calculation (50 nodes) exceeds our throughput-based calculation (8 nodes), we should provision based on the storage needs. This higher node count actually works in our favor, as it gives us plenty of headroom for handling our throughput requirements. Of course, these are rough estimates and the actual numbers would vary based on several factors including our choice of instance types, the average size of our cached values, read/write ratio, replication requirements, and expected growth rate. But, for our purposes, we are going to say we'll have 50 nodes in our cluster!
So we have 50 nodes, but how do we know which node a given key-value pair should be stored on?
3) How can we ensure an even distribution of keys across our nodes?
The answer? Consistent hashing.
I'm sure you've read about consistent hashing before, but let's quickly review the core concept.
Without consistent hashing, the naive solution would be to use a simple modulo operation to determine which node a key-value pair should be stored on. For example, if you had 4 nodes, you could use hash(key) % 4 and the result would be the node number that that key-value pair should be stored on.
This works great when you have a fixed number of nodes, but what happens when you add or remove a node?
Consistent hashing is a technique that helps us distribute keys across our cache nodes while minimizing the number of keys that need to be remapped when nodes are added or removed. Instead of using simple modulo arithmetic (which would require remapping most keys when the number of nodes changes), consistent hashing arranges both nodes and keys in a circular keyspace.
So, instead of using hash(key) % 4, we use a consistent hashing function like MurmurHash to get a position on the circle. Given that position, we move clockwise around the circle until we find the first node. That is the node that should store the key-value pair on!
Consistent Hashing
Why go through all this trouble?
Because now if a node is added or removed, only the keys that fall within that node's range need to be remapped, rather than having to redistribute all keys across all nodes as would be the case if our modulo operation went from hash(key) % 4 to hash(key) % 5 or hash(key) % 3.
To read more about consistent hashing, I'd recommend checking out the Cassandra deep dive.
4) What happens if you have a hot key that is being read from a lot?
You're bound to get the classic interview follow up question: What about hot keys?
To be honest, this is usually a property of the client or user of the cache, not the cache itself. Still, it comes up frequently in interviews, so it's best to be prepared with a thoughtful answer.
Hot keys are a common challenge in distributed caching systems. They occur when certain keys receive disproportionately high traffic compared to others - imagine a viral tweet's data or a flash sale product's inventory count. When too many requests concentrate on a single shard holding these popular keys, it creates a hotspot that can degrade performance for that entire shard.
There are two distinct types of hot key problems we need to handle:
Hot reads: Keys that receive an extremely high volume of read requests, like a viral tweet's data that millions of users are trying to view simultaneously
Hot writes: Keys that receive many concurrent write requests, like a counter tracking real-time votes.
Pattern: Scaling Reads
Hot key scenarios in distributed caches perfectly demonstrate scaling reads challenges. When millions of users simultaneously request the same viral content, traditional caching assumptions break down.
Learn This Pattern
Let's first explore strategies for handling hot reads, then we'll discuss approaches for hot writes afterwards.

Bad Solution: Vertical Scaling all Nodes

Good Solution: Dedicated Hot Key Cache

Good Solution: Read Replicas

Great Solution: Copies of Hot Keys

The key takeaway for your interviewer is demonstrating that you understand hot keys are a real operational concern that can't be ignored. By proactively discussing these mitigation strategies, you show that you've thought through the practical challenges of running a distributed cache at scale and have concrete approaches for addressing them. This kind of operational awareness is what separates theoretical knowledge from practical system design experience.
5) What happens if you have a hot key that is being written to a lot?
Hot writes are a similar problem to hot reads, but they're a bit more complex and have a different set of trade-offs.

Great Solution: Write Batching

Great Solution: Sharding Hot Key With Suffixes

6) How do we ensure our cache is performant?
Our single-node design started off simple and snappy—lookups and writes were O(1) and served straight out of memory. But as we grow our system into a large, distributed cache spanning dozens or even hundreds of nodes, the problem changes. Suddenly, performance isn’t just about how fast a hash table runs in memory. It’s about how quickly clients can find the right node, how efficiently multiple requests are bundled together, and how we avoid unnecessary network chatter.
Once we start scaling out, we can no longer rely solely on local performance optimizations. Even if each individual node is blazing fast, the interaction between nodes and clients, and the overhead of network hops, can introduce significant latency. It’s not unusual for a request that was once served in microseconds to slow down when it has to traverse the network multiple times, deal with connection setups, or handle many small requests individually.
The good news is, we already solved this problem with each of our previous solutions. Request batching, which helped us with our hot writes, is also an effective general technique for reducing latency since it reduces the number of round trips between the client and server.
Consistent hashing, which we talked about in our sharding solution, is also an effective general technique for reducing latency since it means we don't need to query a central routing service to find out which node has our data -- saving us a round trip.
The only other thing I may consider mentioning in an interview if asking this question is connection pooling. Constantly tearing down and re-establishing network connections between the client and servers is a recipe for wasted time. Instead of spinning up a fresh connection for every request, clients should maintain a pool of open, persistent connections. This ensures there’s always a ready-to-use channel for requests, removing expensive round-trip handshakes and drastically reducing tail latencies (like those p95 and p99 response times that can make or break user experience).
Tying it all together
Ok, tying it all together, on each node, we'll have two data structures:
A hash table for storing our key-value pairs
A linked list for our LRU eviction policy
When it comes to scaling, it depends on which of the above approaches you choose, as you can end up with a slightly different design. Assuming you opted for:
Asynchronous replication for high availability and handling hot key reads.
Consistent hashing for sharding and routing.
Random suffixes for distributing hot key writes across nodes.
Write batching and connection pooling for decreasing network latency/overhead.
Your final design might look something like this:
Final Design
What is Expected at Each Level?
Mid-level
For mid-level candidates, we'll typically spend more time on the high-level design section (aka the low-level design) and less time on the scale section. I expect that they can reason about the right combination of data structures to achieve our latency requirements and that they can problem-solve their way to basic answers about scalability and availability. For example, understanding the need for replication and figuring out the different ways that could be implemented.
Senior
For senior candidates, I expect that the low-level design portion is relatively straightforward and that we instead spend most of our time talking about scale. I want to see their ability to weigh tradeoffs and make decisions given the requirements of our system. They should know basic strategies for handling hot reads/writes and be able to talk about things like consistent hashing as if they are second nature.
Staff
I don't typically ask this of staff engineers because, by the time you are staff, these concepts likely come naturally, which means it isn't the best question to evaluate a staff engineer.
Test Your Knowledge

Take a quick 15 question quiz to test what you've learned.

Start Quiz

Mark as read

Next: YouTube

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

(195)

Comment
Anonymous
​
Sort By
Popular
Sort By
Tejas Venky
Top 5%
• 1 year ago

damn I rlly thought this problem was super hard, legit just scaling the leetcode problem lru cache lolzzz thx for the article big boss

49

Reply

Evan King

Admin
• 1 year ago

Ez as 1,2,3!

28

Reply
lloyd lasrado
Top 10%
• 1 year ago

Thanks for documenting most common problems. Is it possible for you to upload videos for all the common problems to paid members. I understand more well watching your videos and the way you explain in depth.

25

Reply

Evan King

Admin
• 1 year ago

Noted. Balancing videos with more content. But will keep this in mind :)

7

Reply
Katie McCorkell
Top 10%
• 1 year ago

Chiming in with one vote from me preferring blogs over videos!

4

Reply
lloyd lasrado
Top 10%
• 1 year ago

Thank you for replying. One suggestion I have if you can do videos at least for Infra design as they are more complicated. Also may be pick unique ones like Distributed cache or Notification service etc. Product design interviews are mostly similar in many ways.

3

Reply
R
RadicalBlackBeetle554
• 1 year ago

There aren’t separate videos for premium members yet, right? Could you please confirm, Evan? Additionally, does your team have any plans for this in the near future? If so, I’d love to hear an update.

1

Reply

Evan King

Admin
• 1 year ago

Nope, not yet. And not sure. Still weighing the tradeoffs between videos on existing premium content vs net new content.

0

Reply
S
SecureTomatoLynx933
• 1 year ago

Thanks for the write-up! In this example, it appears that the client seems to know a lot of things:

It knows about the multiple hot key copies (with random suffixes)
It knows to batch writes
It also has the a map of the consistent hashing scheme and thus sends a request to the appropriate shard.

But how does the client come to know all of this information? Is there a master broker in our Cache that is relaying all of this information to the client?

19

Reply

Evan King

Admin
• 1 year ago

The client here is a bit different than the client we're used to seeing in other designs. It's not an end user, it's a service within your application. Typically, this would be a client library (like redis-py for Redis or memcached for Memcached) that handles all this complexity.

Some managed systems like Redis Enterprise or AWS ElastiCache abstract this away completely, but for a custom implementation, you'd just use a client library.

13

Reply
S
socialguy
Top 5%
• 1 year ago

SecureTomatoLynx933 asked what I was about to! My thought on this is that the client that did the write could receive the sharded keys to use for future requests, but other clients will have to make an initial request to the primary key server before coming to know about the existence of sharded keys. Same logic applies if the client application is restarted.

Is this what you had in mind? Perhaps this point should be clarified a little more in the deep dives for hot reads and writes, since it's an important question.

5

Reply
M
ManagerialCyanSawfish581
Premium
• 10 months ago

Great Article, Can we use the approach for answering other questions like system design for memcached?

0

Reply

Evan King

Admin
• 10 months ago

Of course! That's the point!

2

Reply
M
ManagerialCyanSawfish581
Premium
• 9 months ago

Thank you, reason being I had been asked in an interview to do system design for a single node memcached as I do not have much expertise with distributed systems but I had this article in my mind as I had practiced this article so many times, I answered exactly what you had given here in this article hoping it suffices. Thank you

1

Reply
S
SecureTomatoLynx933
• 1 year ago

Thanks for the reply. So can we assume that the client library is communicating with one (or more) of the Cache nodes to get all this information? Similar to how (I believe) Kafka Consumers stay up to date on the configurations of Kafka Brokers.

0

Reply
D
Danny
Premium
• 11 months ago

The batch writes section is ambiguous about the client being involved. I think that deserves updating. As for the connections maintained between the client and nodes, that is a lot more detail that would add a lot of complexity to the interview. Might require a separate write up.

3

Reply
Apoorv Gupta
Premium
• 8 months ago

I think this solution hand-waived a lot of implementation details, like:

How do clients know the ring hashing function
How does the system detect the hot keys and split them across replicas?
How do you tell the clients that this specific key is split across multiple shards and they need to read all of them to calculate the number of views?

In an interview, I would expect the candidate to explain them and include them in the system diagram.

I think that Zookeeper's notification feature solves (1) & (3) well, but I'm not sure if we're allowed to use it here.

14

Reply
Jose
• 8 months ago

Agree. Things I'd have liked to see:

Solve using a client wrapper of the cache maybe. It's not only about knowing the shard, but what about Membership ? Either Zookeeper here as you mentioned aftewards, or via Gossip.
My hunch is we could say hot are those keys that are at the tail of the doubly linked list.
+1, maybe each node could have a background worker putting those hot keys on a sorted set which gets periodically propagated to the client wrapper, then it becomes transparent to the user the need to fan-out.

4

Reply
Vankshu Bansal
Top 10%
• 7 months ago

So this becomes like a service mesh architecture here? The control plane is our distributed cache and the client library is like a sidecar? Is this the gossip protocol you're talking about?

1

Reply
V
VeryEmeraldBird248
Premium
• 10 months ago

This article lacks too many details and is very hypothetical. I don't have too much depth into Cache but would not pass anyone who presents these 10k feet level details about a system.

It explains sharding to distribute load but doesn't explain how multiple read instances for each shard will work together in case of failure and writes.
Hot key: doesn't explain how writes will work and which component will do what.
Doesn't explain how all nodes will have consistent values for keys when key is suffixed to distribute across nodes.
Doesn't explain how write batching will work and which layer or component it'll exist on.
Hot key writes: you are distributing writes but lacking details in how those writes will be consolidated across multiple nodes.

I hope a paid version of this article is re-written as I'd like to pay and learn depth rather than jargon.

13

Reply
T
texasrulesw
Premium
• 2 months ago

I feel like it explains it reasonably well.  They do talk about hot key writes and batching.

Let's start with those.  what parts do you feel are missing?

0

Reply
M
ManagerialCyanSawfish581
Premium
• 9 months ago

I had been asked in an interview to do system design for a single node memcached as I do not have much expertise with distributed systems but I had this article in my mind as I had practiced this article so many times, I answered exactly what had been given here in this article hoping it suffices?? Thank you

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

The API

High-Level Design

1) Users should be able to set, get, and delete key-value pairs

2) Users should be able to configure the expiration time for key-value pairs

3) Data should be evicted according to LRU policy

Potential Deep Dives

1) How do we ensure our cache is highly available and fault tolerant?

2) How do we ensure our cache is scalable?

3) How can we ensure an even distribution of keys across our nodes?

4) What happens if you have a hot key that is being read from a lot?

5) What happens if you have a hot key that is being written to a lot?

6) How do we ensure our cache is performant?

Tying it all together

What is Expected at Each Level?

Mid-level

Senior

Staff
