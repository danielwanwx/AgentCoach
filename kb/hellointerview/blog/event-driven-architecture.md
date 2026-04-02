# When to Use Event Driven Architecture In System Design Interviews

> Source: https://www.hellointerview.com/blog/event-driven-architecture
> Scraped: 2026-03-30


​
Sort By
Popular
Sort By
P
ParentalRedSole744
Premium
• 8 months ago

Once again, I can't believe you've distilled a complicated topic into such an insightful well-articulated article. It's almost humorous now.

13

Reply

Evan King

Admin
• 8 months ago

haha appreciate you!

1

Reply
D
dhruva.alam
Premium
• 6 months ago

Is there a reason why this is part of the blog and not the patterns section of Systems Design content?

4

Reply
D
DistinctAmaranthCaterpillar447
Premium
• 2 months ago

In the ED architecture, how do we ensure email(through email service) is not sent out before the payment service has finished processing payment?

1

Reply
Micheal Ojemoron
Premium
• 19 days ago

We should only send emails when the payment service has completed updating its state, then we dispatch the PaymentSucceed event, which the email service subscribes to

1

Reply
SAHIL AHMAD LONE
• 8 months ago

Also important thing to consider is EDA can be utilized for scaling- which I belive you have already touch based here. But I also look at user pattern, like if they dont need to wait for response or if its an action that can be performed later(perhaps after order processing like ratings etc), should be decoupled with EDA.

1

Reply
Daniel Mai
Premium
• 8 months ago

Love this, very insightful analysis of EDA

1

Reply
Show All Comments
Reading Progress

On This Page

The Solution: Event Driven Architecture (EDA)

When to Use in Interviews

What doesn't need events

Making the decision

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

