# System Design Interview Fundamentals: Mastering Estimation

> Source: https://www.hellointerview.com/blog/mastering-estimation
> Scraped: 2026-03-30


​
Sort By
Popular
Sort By
W
WillingOliveSwordfish412
Premium
• 1 year ago

I have checked some of the high res JPEGs from my iphone 7MP UW camera and HIEC from 12 MP main camera. They are both O(1 MB).

I this post are you referring to Bytes or bits with 'b'? Asking because it will cause an 10x error in estimates, which in some cases can lead to different design decisions.

6

Reply
SC
Sam Cooper
• 11 months ago

+1 for this, the lowercase units are confusing: I'm pretty sure the storage sizes are intended to be bytes, but iirc the SI convention is b => bit, B => byte

4

Reply
M
MusicalLimeHamster840
• 5 months ago

I think he is referring to an internet high resolution image and not phone or camera thing, a 7mb photo is too high for internet browsing

1

Reply
N
nezudevv
Premium
• 8 months ago

I am also confused by this. I just assumed bytes, hope I assumed correctly.

0

Reply
Nitish Jain
• 1 year ago

Thanks for this blog post, really helpful.

3

Reply
I
InterimBlueDove307
• 1 year ago

Using an approach called Dimensional Analysis you can create a mental graph of the quantities/dimensions you have to the quantities/dimenions you need to develop.

Typo on "dimenions" (dimensions)

2

Reply
Vikash Mitruka
• 1 year ago

Hi
Thanks for this.
I need some handy recommendation for :

When to horizontally scale db like 1TB store and 100k request per sec
When to scale service eg 1k req per sec

Any handy recommendation?

1

Reply
ASHOK E
• 1 year ago

Either you scale to manage size of data or traffic you handle!

You know you can easily get handy 2TB SSD Disks nowadays. That gives you some insight. Scale it horizontally when you need handle 10s or 100s of TB.

For traffic, are they empty HTTP requests? are these requests totally handled in memory? Do they require external I/O? based on that come up with QPS a single server can handle. Then decide based on NFR goals you have

2

Reply
A
AS3
Premium
• 1 month ago

ballpark

a

0

Reply
Show All Comments
Reading Progress

On This Page

Why Estimate?

The Interviewer's Assessment

How to Estimate Like an Engineer

What to Estimate

Break it Down

Facts to Know

Common Mistakes

Building Your Estimation Muscle

The Bottom Line

Recent Posts

Kafka vs RabbitMQ: How to know which one to use

Mar 23, 2026

LinkedIn's AI-Enabled Coding Interview: How to Prepare

Feb 20, 2026

Shopify's AI Coding Interview: How to Prepare

Feb 20, 2026

Meta's AI-Enabled Coding Interview: How to Prepare

Feb 17, 2026

How to Prepare for a Low-Level Design Interview

Jan 14, 2026

