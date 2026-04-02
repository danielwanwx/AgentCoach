# YouTube

> Source: https://www.hellointerview.com/learn/system-design/problem-breakdowns/youtube
> Scraped: 2026-03-30



​
Sort By
Popular
Sort By
G
GlobalPinkLadybug365
Top 5%
• 1 year ago

Can you please add system design for building a high scale logging/monitoring system

35

Reply
I
InclinedSapphireScallop143
• 1 year ago

you can check ad click aggregator, these two systems would be very similar

5

Reply
R
RepresentativeLimeHarrier694
Top 10%
• 1 year ago

if we split into chunks on client

how many presigned urls are created?
how many s3 urls are created?
do we merge these chunks into 1 video, and then split again into segments? or do we keep original chunks as segments

11

Reply
F
FluffyAmberTarsier784
Top 10%
• 1 year ago

"chunks" are referring to binary data for the upload to s3. for example, you can split a 10GB file into 1GB "chunks".

the client will have to calculate how many chunks it wants to upload to s3 (let's say "x" amount). it makes a call to our API, which will return "x" number of presigned urls for the client.

there's still only going to be 1 10GB file at the end of this and s3 will internally stitch those chunks together for you once you tell it that you're done doing the multipart upload.

chunks and segments sound similar but serve different use cases.

chunk = binary data for upload purposes. useful for resumeable uploading and throughput
segment = some part of a video that can be watched. useful for adaptive streaming

21

Reply
udit agrawal
Top 10%
• 5 months ago

From what I understand it will be a single S3 presigned URL returned by the video service.
Flow:
Client breaks down the file into chunks of specific size(let's say 5MB, decided by SDK based on conditions) -> client makes the call with the metadata of the file along with the chunks fingerprint(status : non uploaded) and persist in the DB -> client start uploading to S3 by sending chunks using multi part API -> S3 responds with success and an etag -> client send the etag info for the successfully uploaded chunk to video service -> video service makes call to S3 to check if actually uploaded (trust but verify) -> this continues for all the chunks -> once all chunks are uploaded client makes the complete upload call which tells the S3 to stich the parts -> once stitching is completed S3 will notify to Video service using S3 notifications -> video service will update the status to uploaded -> put an event in a queue to start video post processing -> consumer picks the event and kicks the video processing workflow -> {workflow generates the manifest files and video segments which are small playable clips} -> status of video updated to ready -> pushed to elastic search to allow video to be searchable.

5

Reply
H
HotChocolateSpider690
• 1 year ago

I've the same question.

2

Reply
Cosmos
• 7 months ago

Why endpoint for uploading video api is POST /upload not POST /videos ?

8

Reply
Umair Shabbir
Premium
• 19 days ago

It should not be a verb right?

0

Reply
Abhimanyu Sharma
Premium
• 26 days ago

I have the same question, POST /videos seems more inline with the best practices.

0

Reply
S
socialguy
Top 5%
• 1 year ago

Please do videos for premium content as well. Understandably, those videos will be behind a paywall, but having videos for free and not for premium users seems backward. I usually prefer reading up to listening to someone, but your YouTube content is worth making an exception.

8

Reply
V
Viresh
• 1 year ago

Thanks for the detailed writeup.
Some companies (like Google), expect candidates to not rely too much on external solutions, S3 multipart upload in this case. It'd be great to have the writeup without too much reliance on the S3 multipart specific functionality (like events notifications and Lambda) and just call out what functional assumptions are we making on this file uploading framework.

It'd also be ideal to explore 1 more alternative to S3 since they could ask about why S3 and not something else. A reasonable choice there could be tus.io

Love the callout to Temporal as the workflow orchestration choice.

Nit: there's a typo in "handleful of nodes" -> "handful of nodes"

8

Reply

Evan King

Admin
• 1 year ago

Good call out! Fixing the typo now, thanks for flagging

3

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

Background: Video Streaming

1) Users can upload videos

2) Users can watch videos

Potential Deep Dives

1) How can we handle processing a video to support adaptive bitrate streaming?

2) How do we support resumable uploads?

3) How do we scale to a large number of videos uploaded / watched a day?

Some additional deep dives you might consider

What is Expected at Each Level?

Mid-level

Senior

Staff+

