# System Design Trackers from Netflix's Ad Tracking Launch

> Source: https://www.hellointerview.com/blog/system-design-trackers-from-netflix-ad-tracking-launch
> Scraped: 2026-03-30

System Design Trackers from Netflix's Ad Tracking Launch

By Evan King

•

May 15, 2025

System design interviews test your ability to solve ambiguous, large-scale problems under pressure. While textbook examples help, nothing beats learning from how tech giants tackle real engineering challenges at global scale.
When Netflix introduced ads in 2022, they confronted an immediate technical dilemma: how to accurately track ad impressions across 270+ million global viewers without a single hiccup in performance.
Rather than spending years building everything from scratch, Netflix made a practical decision. They leveraged Microsoft's existing ad infrastructure initially, then gradually developed their own in-house solution by 2024 when they better understood their specific needs.
This journey, from simple proxy to sophisticated event platform, showcases pragmatic engineering at its finest. Instead of over-engineering from the start, Netflix built incrementally, addressing real problems as they emerged.
Together we'll explore how their approach evolved and what system design lessons we can extract for your next interview.
Lesson 1: Start Simple, Scale Later
When Netflix launched their ad-supported tier in November 2022, they made a smart strategic decision: partner with Microsoft rather than building an ad platform from scratch. This let them focus on integration instead of reinventing the wheel.
The baseline architecture was deliberately simple but effective. It consisted of four main components:
Microsoft Ad Server: The core engine responsible for ad selection and delivery. This server determined which ads to show based on targeting parameters
Netflix Ads Manager: A middleware service that acted as the bridge between Netflix's ecosystem and Microsoft's ad platform. Its job was to parse the documents from Microsoft, extract relevant tracking information, and create a simplified structure that Netflix's playback systems could understand.
Ad Event Handler: A Kafka consumer responsible for processing ad events. When users viewed ads, this component read the event data, decrypted the payload, and forwarded tracking information back to Microsoft and other verification vendors.
Client Device Tracking: The final piece that ran on user devices (TVs, phones, tablets). During ad playback, the device tracked key events like impressions and sent them along with an encrypted token back to Netflix.
The data flow in this system was straightforward:
When a client device reached an ad break, it requested ads from Netflix's playback systems.
The Ads Manager decorated this request with additional information and sent it to Microsoft's Ad Server.
Microsoft returned ads in VAST format, which the Ads Manager parsed and simplified.
Crucial tracking info was encrypted into an opaque token and included in the response to the client.
During ad playback, the client device sent events with the token to Netflix's telemetry system.
These events were enqueued in Kafka for asynchronous processing by the Ad Event Handler.
The handler decrypted the payload and forwarded tracking data to Microsoft and other vendors.
Netflix Ad Tracking System Design
In interviews, don't overengineer your initial design. Start with a baseline that solves the core problem, then evolve. Ask whether external systems are available to integrate with before building everything yourself. This approach lets you validate assumptions with real users before committing to complex custom solutions.
Lesson 2: Use Indirection to Manage Complexity
In January 2024, Netflix decided to invest in their own in-house advertising platform. As they transitioned away from Microsoft's infrastructure, they encountered their first major challenge: token bloat.
The Problem
In the original system, encrypted tokens sent with each ad event contained all the tracking URLs and metadata needed for reporting to advertisers. As Netflix integrated more third-party verification vendors, these tokens grew substantially in size.
Since the tokens were cached on client devices, they began consuming significant memory. This started to cause issues, especially on low-end TVs and mobile devices with limited resources.
With plans to add even more capabilities like new ad formats and additional tracking partners, token bloat would only worsen. They needed a solution before device performance suffered.
The Solution: Ads Metadata Registry
Netflix introduced a cache called the Ads Metadata Registry. This service stored the complete metadata for each ad served.
The token now contained just three small pieces of information:
The Ad ID
A metadata record ID
The event name
When events occurred, the Event Handler would use these references to fetch the complete tracking information from the cache.
Netflix Ad Tracking System Design
When direct data transfer becomes unwieldy, introduce a layer of indirection. By replacing bulky data with lightweight references, you can maintain the same interface while dramatically reducing resource usage. Look for opportunities in your system design where replacing direct data with references can solve scaling problems. This pattern is especially valuable when dealing with constrained client devices or high-volume data transfers. We also see this a lot in message queues. Store only a reference to your data, while keeping the actual payload in a dedicated store like Redis, S3, or a database. This approach not only reduces the message size but also improves reliability and enables better scaling of your message processing infrastructure independently from your data storage needs.
Lesson 3: Unify Data Collection for Extensibility
The Problem
Moving away from Microsoft meant Netflix now needed to handle all aspects of ad serving themselves. This shift created several immediate requirements:
Implementing their own frequency capping to prevent showing the same ads repeatedly
Incorporating pricing information for billing advertisers
Building a robust reporting system to share campaign metrics
Scaling event handling across many different vendors
Making matters more complex, Netflix was planning to launch new ad formats beyond video ads, such as display ads and pause ads. These would use different logging frameworks, creating the risk of fragmented data pipelines for similar use cases.
The Solution: Centralized Ad Event Collection
Rather than building separate pipelines for each ad format and use case, Netflix designed a centralized event collection system. They built the Ads Event Publisher, a unified service responsible for collecting all ad telemetry and publishing standardized events to Kafka for all downstream systems.
This approach had several key advantages:
It consolidated common operations like token decryption, data enrichment, and identifier hashing into a single execution step
It provided a unified data contract to all consumers, making the system extensible regardless of ad server or media type
It created clean separation between upstream systems (ad delivery) and downstream consumers (reporting, billing, etc.)
Netflix Ad Tracking System Design
When facing multiple related data streams, resist the urge to build separate pipelines. Instead, design a unified collection system with a standardized output format. This pattern creates a clean abstraction layer that hides the complexity of different data sources from consumers. In system design interviews, emphasize the interfaces between components, not just the components themselves. A well-defined data contract enables independent evolution of producers and consumers, significantly reducing maintenance costs and allowing for faster iteration on new features.
Lesson 4: Specialized Components with Common Foundations
The Problem
With their centralized event system in place, Netflix needed to build specialized downstream components that would consume these events in real time. Each consumer needed to perform different functions while maintaining performance at Netflix's massive scale.
A traditional approach might involve building each consumer as a completely separate system with its own data processing logic. This would lead to duplicated code, inconsistent processing, and maintenance headaches.
Netflix needed to support multiple simultaneous use cases:
Frequency capping that tracked impressions in real time
Metrics generation for campaign health monitoring
Ad session tracking for accurate reporting
Event handling for third-party verification
Billing and revenue tracking
The Solution: Specialized Stream Processors with a Common Foundation
Netflix built a suite of realtime consumers, each optimized for its specific purpose but all consuming from the same unified event stream:
Frequency Capping: This component tracked impressions for each campaign and profile, providing critical data to the Ad Server during ad decision-making.
Ads Metrics: Implemented as an Apache Flink job, this transformed raw events into dimensions and metrics, writing to an OLAP database (Apache Druid).
Ads Sessionizer: Another Flink job that consolidated all events related to a single ad into an "Ad Session," creating a holistic view of ad playback.
Ads Event Handler: This service sent tracking information to third-party vendors by reading data from the event stream.
Billing/Revenue: These components curated impression data for financial processes.
By maintaining a consistent event schema upstream, each of these specialized components could focus on its core responsibility rather than worrying about data transformation or validation.
System Design Lesson: Practice separation of concerns by building specialized components that consume from a common data foundation. This allows individual teams to optimize their services independently while ensuring they all operate from the same source of truth. In system design interviews, demonstrate how a clean data architecture enables you to add new capabilities without disrupting existing functionality. This pattern is particularly powerful for systems that need to evolve rapidly, as Netflix experienced when integrating new features like display ads and QR code tracking.
Conclusion
Netflix's approach to building their ad tracking system demonstrates pragmatic architecture that evolves to meet real-world challenges. The key lessons — starting simple, using indirection, maintaining clear data contracts, and practicing separation of concerns — apply to any complex system design.
You may have even noticed quite a few similarities with our Ad Click Aggregator breakdown! The patterns of centralized event collection, specialized consumers, and lightweight references are recurring solutions in large-scale data systems.
Reading engineering blogs from top companies is one of the best ways to stay current with real-world solutions to complex problems. These case studies provide insights you simply can't get from textbooks or theoretical discussions alone.
Want to dive deeper into Netflix's ad tracking journey? Read their full write-up at Netflix Tech Blog.

Mark as read

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
About The Author

Evan, Co-founder of Hello Interview and former Staff engineer at Meta, possesses a unique vantage point having been on both sides of the tech hiring process. With a track record of conducting hundreds of interviews and securing offers from top tech companies himself, he is now on a mission to help others do the same.

Recommended Reading

Counting Events at Scale: Netflix's Counter Abstraction

This is the strongest fit both contextually and historically: it stays in the Netflix/events domain and was the best-performing blog recommendation in similar placements. It extends the ad-tracking article with concrete counter and aggregation patterns for high-scale event systems.

When to Use Event Driven Architecture In System Design Interviews

Netflix ad tracking is fundamentally an event pipeline problem, so this article is a natural conceptual follow-up. It also showed strong normalized CTR in this placement, suggesting users viewing this kind of content engage with architecture-pattern articles.

Design an Ad Click Aggregator

This is the closest hands-on problem breakdown to the current article, covering ad event ingestion, aggregation, and analytics. It also has strong historical performance here, making it a high-confidence recommendation.

Kafka Deep Dive for System Design Interviews

Kafka is a core technology behind many high-throughput tracking and analytics pipelines like the one discussed in the Netflix article. It also performed exceptionally well in similar recommendation slots, making it a strong technical deep dive to include.
Comments
Comment
Anonymous
Reading Progress

On This Page

Lesson 1: Start Simple, Scale Later

Lesson 2: Use Indirection to Manage Complexity

The Problem

The Solution: Ads Metadata Registry

Lesson 3: Unify Data Collection for Extensibility

The Problem

The Solution: Centralized Ad Event Collection

Lesson 4: Specialized Components with Common Foundations

The Problem

The Solution: Specialized Stream Processors with a Common Foundation

Conclusion

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

Schedule a mock interview

Meet with a FAANG senior+ engineer or manager and learn exactly what it takes to get the job.

Schedule A Mock Interview
Questions
Meta SWE Interview Questions
Amazon SWE Interview Questions
Google SWE Interview Questions
OpenAI SWE Interview Questions
Engineering Manager (EM) Interview Questions
Learn
Learn System Design
Learn DSA
Learn Behavioral
Learn ML System Design
Learn Low Level Design
Guided Practice
Links
FAQ
