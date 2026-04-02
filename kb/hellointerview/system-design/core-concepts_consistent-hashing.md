# Consistent Hashing

> Source: https://www.hellointerview.com/learn/system-design/core-concepts/consistent-hashing
> Scraped: 2026-03-30



​
Sort By
Popular
Sort By
B
BeneficialBrownBarnacle904
Top 10%
• 1 year ago

Example and diagram is unclear on how virtual nodes helped balance load from failed database.

If the positions of the nodes on ring follow the same order "Db1, Db2.. Db5", in case of Db2 failure wouldn't the load from Db2 always go to Db3 ?
In practice, how is the location of virtual nodes on the ring determined? Do we need to use multiple hash functions here?

21

Reply

Evan King

Admin
• 1 year ago

Good catch folks. Updating the image in the next release to make this clearer :)

18

Reply
Ravindra
• 1 year ago
Nice catch, the distribution of virtual nodes would not be same
Most of the real world applications using consistent hashing like Cassandra, DynamoDB and memCached use a single hash function. But for each virtual node, the hash key to identify the location would be (physical_node_identifier + virtual_node_identifier).

10

Reply
N
NakedIndigoBug723
• 1 year ago

How will the keys already present in db be transferred to other nodes if db is removed or down from the hash ring? Also, is consistent hashing used in replication, load balancing?

5

Reply

Evan King

Admin
• 1 year ago

When a DB node fails, the data isn't automatically transferred - you need a separate replication/backup strategy to handle that. Consistent hashing just tells you where new requests should go (to the next node clockwise). For actual data transfer, you'd typically maintain replicas and promote those when a node fails. As for your second question - consistent hashing isn't used for replication (that's handled by separate replication protocols), but it is used in load balancing scenarios where you need to distribute requests across a set of servers.

13

Reply
vinay s
• 11 months ago

If its a managed service/system like dynamodb.. in the event of node failures or node additions, we don't need to do anything right? Infact the node failure becomes abstracted to users like application developers and there is not impact seen to us right?

0

Reply
P
PassingAmberDeer979
Premium
• 16 days ago

Key-space salting: Append a random suffix to hot keys (e.g., taylor-swift-{0..9}) so they hash to different nodes. Reads then scatter across those nodes and get aggregated

how is this useful? can someone pls explain? This increases the read qps, so in which way can this help? Also during aggregation how can we find out the latest version of data and eliminate stale data. Does this help in only write-heavy scenario for hot keys, were we write each update randomly to a node and then aggreagate during read.

2

Reply
M
MinisterialPurpleSwallow414
• 5 months ago

This is really the best article that I have read for consistent hashing.

2

Reply

Evan King

Admin
• 5 months ago

🫡

1

Reply
Vikas Ray
Premium
• 2 months ago

In the Virtual Nodes section, could you add an example explaining what happens when we add a new database node to the hash ring with a diagram? Specifically, how are the existing virtual nodes redistributed, and how does consistent hashing ensure that data remains evenly balanced after the new node is introduced.

1

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Consistent Hashing via an Example

First Attempt: Simple Modulo Hashing

Consistent Hashing

Addressing Hot Spots

Data Movement in Practice

Consistent Hashing in the Real World

When to use Consistent Hashing in an Interview

Conclusion

