# Caching

> Source: https://www.hellointerview.com/learn/system-design/core-concepts/caching
> Scraped: 2026-03-30



​
Sort By
Popular
Sort By
Khánh Trần Duy
Premium
• 5 months ago

Always asking about this topic in details. Suddenly it comes out. Great!

15

Reply
SunflowersInaVase
Top 5%
• 2 months ago

Write-through makes sense when you need strong consistency

But in the write-through section it's also mentioned:

...dual-write problem. If the cache update succeeds but the database write fails, or vice versa, the systems can end up inconsistent

So, does it make sense to ever go with write-through without distributed transactions?

8

Reply
Pavan Rangudu
Premium
• 16 days ago

I don't think so.

0

Reply
F
FastPinkJunglefowl305
Premium
• 21 days ago

It will be great if we can come up with a cheat-sheet kind of a thing for quick overview before interviews.

7

Reply

Stefan Mai

Admin
• 21 days ago

It's a good idea. Let me see what we can do.

7

Reply
I
InnocentScarletAntelope232
Premium
• 16 days ago

yes, please do it

0

Reply
Ernesto Cejas
Premium
• 3 months ago

You should have a section for Cache Invalidation. Like, how to do cache versioning to deal with cache invalidation.

7

Reply
C
CuteBlackBadger226
Premium
• 28 days ago

It's mentioned in the scaling reads

https://www.hellointerview.com/learn/system-design/patterns/scaling-reads#application-level-caching

0

Reply
M
MinimumOrangeParrotfish132
• 2 months ago

Under Cache Consistency — “Short TTLs for stale tolerance: Let slightly stale data live temporarily if eventual consistency is acceptable.”
If eventual consistency is tolerable, wouldn’t you use longer TTLs rather than shorter ones?

2

Reply
SunflowersInaVase
Top 5%
• 2 months ago

It's dependent upon how much staleness we can tolerate. User profile updates should be visible in 1/5/10 mins?
Depends on the particular scenario

1

Reply
Show All Comments
The best mocks on the market.

Now up to 15% off

Learn More
Reading Progress

On This Page

Where to Cache

External Caching

CDN (Content Delivery Network)

Client-Side Caching

In-Process Caching

Cache Architectures

Cache-Aside (Lazy Loading)

Write-Through Caching

Write-Behind (Write-Back) Caching

Read-Through Caching

Cache Eviction Policies

LRU (Least Recently Used)

LFU (Least Frequently Used)

FIFO (First In First Out)

TTL (Time To Live)

Common Caching Problems

Cache Stampede (Thundering Herd)

Cache Consistency

Hot Keys

Caching in System Design Interviews

When to Bring Up Caching

How to Introduce Caching

Conclusion

