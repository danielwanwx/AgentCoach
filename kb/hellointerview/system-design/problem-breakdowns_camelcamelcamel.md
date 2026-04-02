# Price Tracking Service

> Source: https://www.hellointerview.com/learn/system-design/problem-breakdowns/camelcamelcamel
> Scraped: 2026-03-30



​
Sort By
Popular
Sort By
Ahmad Awad
Top 5%
• 9 months ago

Thanks for the great and detailed content!

But my concern is, without a prior knowledge or seeing this problem before, I doubt if I could solve this problem in a real interview.

34

Reply
S
Spaceman
Premium
• 3 months ago

Same feeling like you, this problem is not more general questions from the micro services, distributed systems. I think all the points concentrate to one consensus is we need to use hybrid solution to this kind of complicated and big problem.

1

Reply
Y
YeastyMoccasinHyena669
Premium
• 1 month ago

Same feeling. I almost feel the answer is crafted first, then the question. Lots of questions are like brain-teaser or domain-specific exam

0

Reply
D
DarkSalmonGoose801
Top 10%
• 9 months ago

Great content, you guys rock!

23

Reply
ShinyArceus493
Top 10%
• 9 months ago

You guys are doing God's work at Hello Interview! Thanks a ton on behalf of everyone here.

11

Reply

Evan King

Admin
• 9 months ago

🫶🏻

4

Reply
Pankaj Bhambani
Premium
• 9 months ago

Hey, just a quick suggestion, during one of my interviews, I received feedback that I didn’t discuss the trade-offs between different technologies. For example, I mentioned using Postgres without explaining why it would be better or comparing it to alternatives like NoSQL. It might help to include the trade-offs between options when discussing tech choices.

9

Reply

Evan King

Admin
• 9 months ago

Good shout. I did that less in this one than normal (aside from the DB choice). Oftentimes, when this is the case, it's because the decision matters less. But let me go through and call out a couple of places for next release.

23

Reply
F
FederalOliveReptile537
Premium
• 8 months ago

How do we decide if we want to use time series database or OLAP database?

e.g. In AdClick aggregator we used OLAP db whereas here we used time series db.

8

Reply
Akhil Mittal
Premium
• 5 months ago

A time series database is optimised for real-time, high-frequency data ingestion and analysis of time-stamped data, while OLAP (Online Analytical Processing) is built for complex, multidimensional queries over historical data.

Time series databases excel at handling the continuous write-heavy workloads common in IoT, system monitoring, and finance, whereas OLAP systems are designed for read-heavy analysis and reporting using aggregated, multidimensional "data cubes".

11

Reply
Priyangshu Roy
Premium
• 2 months ago

The adclick aggregation system needs to execute multidimensional queries, if i can recall its not just storing clicks, we also store additional metadata like region, client id, browsers , ip's demography and so on. We may want to slice and dice those clicks by 20 different dimensions (browser, country, ad group). For a use case like this clickhouse or redshift would be preferred.

In this case the query is almost always: "Give me the value of this specific ID over this specific time range." TSDBs use time-partitioning (chunks) and indexes on IDs to make this retrieval nearly instantaneous.

2

Reply
H
HungryTomatoVole404
Top 10%
• 4 months ago

@Evan Please help us here

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

Data Flow

High-Level Design

1) Users should be able to view price history for Amazon products (via website or Chrome extension)

2) Users should be able to subscribe to price drop notifications with thresholds (via website or Chrome extension)

Potential Deep Dives

1) How do we efficiently discover and track 500 million Amazon products?

2) How do we handle potentially malicious price updates from Chrome extension users?

3) How do we efficiently process price changes and notify subscribed users?

4) How do we serve fast price history queries for chart generation?

Final Design

What is Expected at Each Level?

Mid-level

Senior

Staff+

