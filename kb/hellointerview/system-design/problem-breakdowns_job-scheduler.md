# Job Scheduler

> Source: https://www.hellointerview.com/learn/system-design/problem-breakdowns/job-scheduler
> Scraped: 2026-03-30


A job scheduler is a program that automatically schedules and executes jobs at specified times or intervals. It is used to automate repetitive tasks, run scheduled maintenance, or execute batch processes.
There are two key terms worth defining before we jump into solving the problem:
Task: A task is the abstract concept of work to be done. For example, "send an email". Tasks are reusable and can be executed multiple times by different jobs.
Job: A job is an instance of a task. It is made up of the task to be executed, the schedule for when the task should be executed, and parameters needed to execute the task. For example, if the task is "send an email" then a job could be "send an email to john@example.com at 10:00 AM Friday".
The main responsibility of a job scheduler is to take a set of jobs and execute them according to the schedule.
Functional Requirements
Core Requirements
Users should be able to schedule jobs to be executed immediately, at a future date, or on a recurring schedule (ie. "every day at 10:00 AM").
Users should be able monitor the status of their jobs.
Below the line (out of scope)
Users should be able to cancel or reschedule jobs.
Non-Functional Requirements
Now is a good time to ask about the scale of the system in your interview. If I were your interviewer, I would explain that the system should be able to execute 10k jobs per second.
Core Requirements
The system should be highly available (availability > consistency).
The system should execute jobs within 2s of their scheduled time.
The system should be scalable to support up to 10k jobs per second.
The system should ensure at-least-once execution of jobs.
Below the line (out of scope)
The system should enforce security policies.
The system should have a CI/CD pipeline.
On the whiteboard, this might look like:
Requirements
The Set Up
Planning the Approach
For this question, which is less of a user-facing product and more focused on data processing, we're going to follow the delivery framework outlined here, focusing on the core entities, then the API, and then the data flow before diving into the high-level design and ending with deep dives.
Defining the Core Entities
We recommend that you start with a broad overview of the primary entities, even for questions more focused on infrastructure, like this one. It is not necessary to know every specific column or detail yet. We will focus on the intricacies, such as columns and fields, later when we have a clearer grasp of the system.
Just make sure that you let your interviewer know your plan so you're on the same page. I'll often explain that I'm going to start with just a simple list, but as we get to the high-level design, I'll document the data model more thoroughly.
To satisfy our key functional requirements, we'll need the following entities:
Task: Represents a task to be executed.
Job: Represents an instance of a task to be executed at a given time with a given set of parameters.
Schedule: Represents a schedule for when a job should be executed, either a CRON expression or a specific DateTime.
User: Represents a user who can schedule jobs and view the status of their jobs.
In the actual interview, this can be as simple as a short list like this. Just make sure you talk through the entities with your interviewer to ensure you are on the same page.
Entities
The API
Your goal is to simply go one-by-one through the core requirements and define the APIs that are necessary to satisfy them. Usually, these map 1:1 to the functional requirements, but there are times when multiple endpoints are needed to satisfy an individual functional requirement.
First, let's create a job:
POST /jobs
{
  "task_id": "send_email",
  "schedule": "0 10 * * *",
  "parameters": {
    "to": "john@example.com",
    "subject": "Daily Report"
  }
}
Next, let's query the status of our jobs:
GET /jobs?user_id={user_id}&status={status}&start_time={start_time}&end_time={end_time} -> Job[]
Data Flow
Before diving into the technical design, let's understand how data flows through our system. The data flow represents the journey from when a request enters our system to when it produces the final output.
Understanding this flow early in our design process serves multiple purposes. First, it helps ensure we're aligned with our interviewer on the core functionality before getting into implementation details. Second, it provides a clear roadmap that will guide our high-level design decisions. Finally, it allows us to identify potential bottlenecks or issues before we commit to specific architectural choices.
A user schedules a job by providing the task to be executed, the schedule for when the task should be executed, and the parameters needed to execute the task.
The job is persisted in the system.
The job is picked up by a worker and executed at the scheduled time.
If the job fails, it is retried with exponential backoff.
Update the job status in the system.
Note that this is simple, we will improve upon as we go, but it's important to start simple and build up from there.
High-Level Design
We start by building an MVP that works to satisfy the core functional requirements. This does not need to scale or be perfect. It's just a foundation for us to build upon later. We will walk through each functional requirement, making sure each is satisfied by the high-level design.
1) Users should be able to schedule jobs to be executed immediately, at a future date, or on a recurring schedule
When a user schedules a job, they'll provide the task to be executed, the schedule for when the job should be executed, and the parameters needed to execute the task. Let's walk through how this works:
The user makes a request to a /jobs endpoint with:
Task ID (which task to run)
Schedule (when to run it)
Parameters (what inputs the task needs)
We store the job in our database with a status of PENDING. This ensures that:
We have a persistent record of all jobs
We can recover jobs if our system crashes
We can track the job's status throughout its lifecycle
Schedule Jobs
When it comes to choosing a database, the hard truth is that any modern database will work. Given no need for strong consistency and our data has few relationships, I'm going to opt for a flexible key value store like DynamoDB to make scaling later on easier. If you're interviewing at a company that prefers open-source solutions, you might go with Cassandra instead. But, like I said, Postgres or MySQL would work just as well, you'd just need to pay closer attention to scaling later on.
Let's start with a simple schema for our Jobs table to see why this approach needs refinement:
{
  "job_id": "123e4567-e89b-12d3-a456-426614174000",
  "user_id": "user_123",
  "task_id": "send_email",
  "scheduled_at": 1715548800,
  "parameters": {
    "to": "john@example.com",
    "subject": "Daily Report"
  },
  "status": "PENDING"
}
This works fine for one-time jobs, but it breaks down when we consider recurring schedules. Consider a daily email report that needs to run at 10 AM every day. We could store the CRON expression (0 10 * * *) in our table, but then how do we efficiently find which jobs need to run in the next few minutes? We'd need to evaluate every single CRON expression in our database—clearly not scalable.
This brings us to a key insight: we need to separate the definition of a job from its execution instances. Think of it like a calendar: you might have an event that repeats every Monday, but in your calendar app, you see individual instances of that event on each Monday. This is exactly what we need.
Let's split our data into two tables. First, our Jobs table stores the job definitions:
{
  "job_id": "123e4567-e89b-12d3-a456-426614174000",  // Partition key for easy lookup by job_id
  "user_id": "user_123", 
  "task_id": "send_email",
  "schedule": {
    "type": "CRON" | "DATE" 
    "expression": "0 10 * * *"  // Every day at 10:00 AM for CRON, specific date for DATE
  },
  "parameters": {
    "to": "john@example.com",
    "subject": "Daily Report"
  }
}
Then, our Executions table tracks each individual time a job should run:
{
  "time_bucket": 1715547600,  // Partition key (Unix timestamp rounded down to hour)
  "execution_time": "1715548800-123e4567-e89b-12d3-a456-426614174000",  // Sort key (exact execution time + jobId to ensure the composite primary key is unique)
  "job_id": "123e4567-e89b-12d3-a456-426614174000",
  "user_id": "user_123", 
  "status": "PENDING",
  "attempt": 0
}
By using a time bucket (Unix timestamp rounded down to the nearest hour) as our partition key, we can efficiently query for upcoming jobs. We only need to query the current hour's bucket and possibly the next hour's bucket. The time bucket can be easily calculated:
time_bucket = (execution_time // 3600) * 3600  # Round down to nearest hour
This gives us efficient reads, since we only need to query 1-2 partitions to find all upcoming jobs. When a recurring job completes, we can easily schedule its next occurrence by calculating the next execution time and creating a new entry in the Executions table. The job definition stays the same, but we keep creating new execution instances.
Concentrating all writes for a given hour into a single partition could create a hot partition under heavy load. We'll address this with write sharding in the scaling deep dive.
This pattern of separating the definition of something from its instances is common in system design. You'll see it in calendar systems (event definition vs. occurrences), notification systems (template vs. individual notifications), and many other places. It's a powerful way to handle recurring or templated behaviors. See the GoPuff Breakdown for another example of this.
When a worker node is ready to execute jobs, it simply queries the Executions table for entries where:
execution_time is within the next few minutes
status is "PENDING"
The worker can then look up the full job details in the Jobs table and execute the task.
Execution
This simple approach is a great start, but don't stop reading here! We expand on this significantly later in the deep-dives in order to ensure the system is scalable, fault tolerant, and handles job failures gracefully.
2) Users should be able monitor the status of their jobs.
First, the obvious bit, when a job is executed we need to update the status on the Executions table with any of COMPLETED, FAILED, IN_PROGRESS, RETRYING, etc.
Monitoring
But how can we query for the status of all jobs for a given user?
With the current design, querying jobs by userId would require an inefficient two-step process:
Query the Jobs table to find all job_ids for a user (an inefficient full table scan)
Query the Executions table to find the status of each job
To solve this, we'll add a Global Secondary Index (GSI) on the Executions table:
Partition Key: user_id
Sort Key: execution_time + job_id
This GSI allows us to efficiently find all executions for a user, sort them by execution time, support pagination, and filter by status if needed. The index provides a fast and scalable way to query execution data from the user's perspective.
The GSI adds some write overhead and cost, but it's a worthwhile trade-off to support efficient user queries without compromising our primary access pattern of finding jobs that need to run soon.
This is a common pattern in DynamoDB (and similar NoSQL databases) where you maintain multiple access patterns through GSIs rather than denormalizing the data. The alternative would be duplicating the user_id in the base table, which would make the data model more complex and harder to maintain.
Now, users simply need to query the GSI by user_id and get a list of executions sorted by execution_time.
Potential Deep Dives
1) How can we ensure the system executes jobs within 2s of their scheduled time?
Our current design has some key limitations that prevent us from executing jobs at the precision we require.
The single, most obvious, limitation is that we are querying the database every few minutes to find jobs that are due for execution. The frequency with which we decide to run our cron that queries for upcoming jobs is naturally the upper bound of how often we can be executing jobs. If we ran the cron every 2 minutes, then a job could be executed as much as 2 minutes early or late.
The next consideration would be to run the cron more frequently. However, to meet our precision requirement, this would mean running it every 2 seconds or less. This won't work for a whole host of reasons.
With 10k jobs per second, each query would need to fetch and process around 20k jobs (jobs due in the next 2 seconds). This is a large payload to transfer and process frequently.
Even with proper indexing, querying for 20k jobs could take several hundred milliseconds. Add in network latency and serialization time, and we might spend 500ms just getting the job data.
After retrieving the jobs, we still need time to initialize them, distribute them to workers, and begin execution. This processing overhead further reduces our precision window.
Running such large queries every 2 seconds puts significant load on the database, which could impact other operations and overall system stability.
As you can see, this isn't the best idea. Instead, we can get more clever and introduce a two-layered scheduler architecture which marries durability with precision.
Phase 1: Query the database: Just like in our current design, we will query the Executions table for jobs that are due for execution in the next ~5 minutes (leaving some buffer for network latency, etc.).
Phase 2: Message queue: We'll take the list of jobs returned by our query and push them to a message queue, ordered by execution_time. Workers will then pull jobs from the queue in order and execute the job.
Low Latency
This two-layered approach provides significant advantages by decoupling the database querying from job execution. By running database queries just once every 5 minutes, we reduce database load while maintaining precision through the message queue. The message queue's high throughput means workers can pull and process jobs as fast as they become available, removing the upper bound on execution frequency that existed in our previous design.
Okay, we're making progress, but what about new jobs that are created and expected to run in less than 5 minutes? Currently, we'd write this job to the database, but the cron that runs every 5 minutes would never see it. We either missed it entirely, or we'd catch it the next time the cron runs, which could be as much as 5 minutes later.
We could try to put the job directly into the message queue, but this introduces a problem with log-based queues like Kafka. Kafka processes messages in order within a partition, so a new job would go to the end of the partition and wait behind all the jobs already queued — even if it's scheduled to run sooner. This would make it impossible to execute the job within our 2-second precision requirement.
Instead, we need a queue system that supports delayed delivery, so that jobs only become visible to workers at (or near) their scheduled execution time. Let's examine our main options:

Good Solution: Redis Sorted Sets

Good Solution: RabbitMQ

Great Solution: Amazon SQS

For our use case, SQS would be the best choice due to its native support for delayed message delivery (which lets us defer job visibility until close to their scheduled execution time), automatic handling of worker failures through visibility timeouts, and excellent scaling characteristics for our load of 10k jobs per second. Keep in mind that DelaySeconds is a minimum delay, not a precision guarantee — but since our workers are continuously polling the queue, any additional latency is typically negligible.
Timely Execution
To recap, our new two-layered scheduler architecture looks like this:
A user creates a new job which is written to the database.
A cron job runs every 5 minutes to query the database for jobs that are due for execution in the next ~5 minutes.
The cron job sends these jobs to SQS with appropriate delay values (SQS supports delays up to 15 minutes, so our 5-minute window fits comfortably).
Workers continuously poll SQS and process messages as they become visible.
If a new job is created with a scheduled time < 5 minutes from the current time, it's sent directly to SQS with the appropriate delay.
Keep in mind that many interviewers or companies will prefer that you avoid managed services like SQS. If this is the case, you can implement your own priority queue using Redis or a similar data store. Just check in with them to get a gauge on what is and isn't allowed.
2) How can we ensure the system is scalable to support up to 10k jobs per second?
In any interview, when you get to talking about scale my suggestion is to work left to right looking for any bottlenecks and addressing them one-by-one.
Job Creation
For us, this means starting with job creation. If job creation was evenly distributed with job execution, this would mean we have 10k jobs being created per second. This is unlikely, since we support recurring jobs, but it's an upper bound. I would likely ask my interviewer at this point if we have any expectations about what percent of jobs are recurring vs. one-time. If the proportion is small, meaning most jobs are one-time, then our Job Creation service might end up being a bottleneck.
To handle high job creation rates, we can introduce a message queue like Kafka or RabbitMQ between our API and Job Creation service. This queue acts as a buffer during traffic spikes, allowing the Job Creation service to process requests at a sustainable rate rather than being overwhelmed. The message queue also enables horizontal scaling by letting us add more Job Creation service instances as consumers, while providing durability to ensure no job creation requests are lost if the service experiences issues.
Adding a message queue between the API and Job Creation service is likely overcomplicating the design. The database should be able to handle the write throughput directly, and we'll always need some service in front of it that can scale horizontally. Unless there's expensive business logic in the Job Creation service that we want to isolate, it's better to keep the architecture simpler and just scale the service itself.
In an interview setting, while this pattern might impress some interviewers, it's worth noting that simpler solutions are often better. Focus on properly scaling your database and service layer before adding additional components. I'll leave it in the diagram but consider it optional.
Scalability
Jobs DB
As discussed earlier, we chose DynamoDB or Cassandra for our Jobs and Executions tables. This was a good choice for scale since DynamoDB supports up to 1,000 write capacity units (WCU) per partition, and with proper key design, our data naturally spreads across many partitions. Here's how our partition keys work:
Jobs table: Partitioned by job_id, which distributes writes evenly across partitions since each job has a unique ID.
Executions table: Partitioned by time_bucket. Since we use hourly buckets, we need to be thoughtful here — all writes for the current hour land on the same partition, which could become a hot partition under heavy load. To address this, we can add write sharding by appending a random suffix to the partition key (e.g., time_bucket#shard_3), spreading writes across multiple partitions. Workers would then query all shards for a given time bucket in parallel.
With proper provisioning and sharding, these tables should handle our load of 10k operations per second and scale to support an increasing number of jobs.
Notably, once a job has been executed, we need to keep it around for users to query. But once a reasonable amount of time has passed (say 1 year) we can move it off to a cheaper storage solution like S3.
Message Queue Capacity
Let's do some quick math to understand our SQS requirements. For each 5-minute window, we need to process around 3 million jobs (10k jobs/second * 300 seconds). While SQS messages can be up to 1MB in size, our messages will be quite small, around 200 bytes each containing just the job ID, execution time, and metadata. That's just 600MB of data per 5-minute window.
SQS automatically handles scaling and message distribution across consumers, which is one of its biggest advantages. We don't need to worry about manual sharding or partitioning — AWS handles all of that for us under the hood. With Standard queues, throughput is virtually unlimited, so our 10,000 messages per second requirement is well within its capabilities without any special configuration.
We might still want multiple queues, but only for functional separation (like different queues for different job priorities or types), not for scaling purposes.
Scale
Even if you went with the Redis priority queue, 3 million jobs would easily fit in memory, so there's nothing to worry about there. You would just end up being more concerned with fault tolerance in case Redis goes down.
Workers
For the worker layer, we need to carefully consider our compute options. The two main choices are containers (using ECS or Kubernetes) and Lambda functions.
Containers: tend to be more cost-effective for steady workloads and are better suited for long-running jobs since they maintain state between executions. However, they do require more operational overhead and don't scale as elastically as serverless options.
Lambda functions: are truly serverless with minimal operational overhead. They're perfect for short-lived jobs under 15 minutes and can auto-scale instantly to match workload. The main drawbacks are that cold starts could impact our 2-second precision requirement, and they tend to be more expensive for steady, high-volume workloads like ours.
Given our requirements - processing 10k jobs per second with 2-second precision in a steady, predictable workload - I'd use containers with ECS and auto-scaling groups, but there is no wrong answer here. Containers give us the best balance of cost efficiency and operational simplicity while meeting our performance needs. We can optimize this setup by using spot instances to reduce costs, configuring auto-scaling based on queue depth, pre-warming the container pool to handle our baseline load, and setting up scaling policies to handle any unexpected spikes in demand.
Workers
3) How can we ensure at-least-once execution of jobs?
Our main concern is how we process failures. If a worker fails to process a job for any reason, we want to ensure that the job is retried a reasonable number of times before giving up (let's say 3 retries per job).
Importantly, jobs can fail within a worker for one of two reasons:
Visible failure: The job fails visibly in some way. Most likely this is because of a bug in the task code or incorrect input parameters.
Invisible failure: The job fails invisibly. Most likely this means the worker itself went down.
Let's start with the easier of the two cases: Visible failures.
For visible failures, we are careful to wrap the task code in a try/catch block so that we can log the error and mark the job as failed. We can then retry the job a few times with exponential backoff before giving up. Upon failure, we'll write to the Executions table to update the job's status to RETRYING with the number of attempts made so far.
We can then put the job back into the Message Queue (SQS) with an increasing delay for each retry attempt. For example, the first retry might wait 5 seconds, the second 25 seconds, and the third 125 seconds. We implement this by setting the DelaySeconds parameter when re-enqueuing the message, using the attempt count to calculate the backoff. If a job is retried 3 times and still fails, we can mark its status as FAILED in the Executions table and the job will no longer be retried.
SQS provides the building blocks we need here — visibility timeouts ensure failed messages reappear, the ApproximateReceiveCount attribute tracks retry attempts, and dead-letter queues catch messages that exceed the retry limit. We just need to implement the backoff timing logic in our worker code.
Now let's consider the more interesting case: Invisible failures. When a worker crashes or becomes unresponsive, we need a reliable way to detect this and retry the job. Let's examine different approaches to handling these failures:

Bad Solution: Health Check Endpoints

Good Solution: Job Leasing

Great Solution: SQS Visibility Timeout

Retries
Lastly, one consequence of at-least-once execution is that we need to ensure our task code is idempotent. In other words, running the task multiple times should have the same outcome as running it just once.
Here are a few ways we can handle idempotency:

Bad Solution: No Idempotency Controls

Good Solution: Deduplication Table

Great Solution: Idempotent Job Design

What is Expected at Each Level?
Mid-level
Mid-level candidates are expected to be able to produce a reasonably high-level design with a clear and cohesive data model. From there, they should be able to respond appropriately to interviewer inquiries about durability, precise scheduling, and retries. I don't expect them to know the right answers to these questions without guidance, but I do expect to see strong problem-solving skills and an ability to work with me, the interviewer, to arrive at reasonable solutions.
Senior
For senior candidates, I expect much more autonomy. They should lead the conversation around two deep dives and show some hands-on experience with any of the relevant technologies. They should specifically be able to articulate the need for a two-phased architecture, even if they choose Redis or a different option for the priority queue. I want to see that they proactively identify issues and quickly adapt to scenarios I throw their way, like "what happens if a worker goes down mid-job execution."
Staff+
Staff candidates are the cream of the crop. I expect they breeze through the setup and the high-level design and spend most of their time leading deep dives. They should proactively lead the discussion and understand the major bottlenecks of the system, proposing well-justified solutions. Typically, they'll have a deep understanding of at least one technology in question and be able to explain, justified with hands-on experience, why one approach is better than another. As always, while not a strict requirement, the best staff candidates have the ability to teach the interviewer something, no matter how small.
Test Your Knowledge

Take a quick 15 question quiz to test what you've learned.

Start Quiz

Mark as read

Next: Web Crawler

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

(423)

Comment
Anonymous
​
Sort By
Popular
Sort By
Laura Kingsley
Top 5%
• 1 year ago

Evan, you are the best :)

101

Reply
F
FitBlackPython669
Premium
• 9 months ago

+1

1

Reply
Shubham Sharma
Top 10%
• 8 months ago

I was asked this exact question yesterday. There are a couple of things that stood out from the interview:

The design decision to create the next entry for the recurring job execution when the previous execution completes is completely dependent on the fact that the job will finish in less time than the recurring schedule. Ex: if a cron runs every 5 minutes and the job takes more time than the same (let's say 10 mins) - then the above design won't work properly and we'll miss out on jobs or lag behind.
The above design completely relies on the fact that we'll do at least once execution. What if we were required to handle exactly once execution
If let's say the scale is very high i.e 50k RPS, keeping a single instance of watcher service just won't work. How would you handle different instances of watcher getting different job executions to be able to scale this up
The interviewer said that our design relies on SQS a lot completely - what if the company doesn't have the budget or familiarity with SQS

22

Reply
Sourabh Upadhyay
Premium
• 8 months ago

I think the next entry needs to be created as soon as the latest entry has started processing and not once it has completed since each execution is independent.

7

Reply
R
RelatedCrimsonAlpaca687
Premium
• 7 months ago

Very interested in this as well since I was also recently asked this, and was asked to support up to 1M jobs scheduled at any given time as part of the NFR which would create an extremely hot partition and/or thundering herd type problem.

I'm wondering if you can partition on time and add some sort of coordinated consistent hashing to it. Then Watcher instances register with ZooKeeper and you can effectively have each instance query a manageable range. So if you have 1M or more jobs all scheduled for exactly noon then you can still distribute the poll load across multiple watchers and you get better durability on Watcher. Admittedly, I'm not 100% sure how crashes mid-poll would work (one of the watchers would need to catch up on the crash instance's range).

For #4 - you can use Kafka or RabbitMQ here, but Apache Pulsar actually has a lot of similar SQS type semantics needed for some of these problems (ack timeouts, delays).

4

Reply
nguyen bao
Premium
• 4 months ago

For #1, I think it depends on design choice. If you want schedule next run of a job only after previous one finishes, then you would create a entry in Execution table only a job finishes. If you want exact schedule (strict cron) regardless of job failures, you don't need to do that.

2

Reply
E
ExtendedTurquoiseRodent893
Premium
• 26 days ago
• edited 26 days ago

For #3, my solution was to utilize Postgres's row-level locks with SKIP LOCKED i.e. SELECT ... FOR UPDATE SKIP LOCKED which ensures mutual exclusion of each watcher instance.

0

Reply
Shiksha Sharma
Top 10%
• 8 months ago

Hi , can we discuss more about these questions? send me your e mail

0

Reply
N
NeutralAmethystUnicorn745
Top 10%
• 1 year ago

What happens if the watcher fails/restarts? First of all, the watcher needs to be distributed to avoid single point failure. And most likely it will be a lead-follower set up as only one watcher instance should be doing the polling. Now the leader goes dead or restarted/redeployed, we either need to wait for leader election to complete or wait for the restart/redeployment to finish. If the wait is longer than 5 minutes, we will miss "The system should execute jobs within 2s of their scheduled time" for the jobs that are scheduled to happen in the past 5-min window.

18

Reply
Kunal Singhal
Premium
• 4 months ago

You will need a separate column in Job Store and use Compare and Set to track whether the job was polled by watcher or not. This is covered in airbnb article https://medium.com/airbnb-engineering/dynein-building-a-distributed-delayed-job-queueing-system-93ab10f05f99. There could still be a case where watcher fails after updating the column and before pusing into the queue. For that having a separate lease column in job store like good solution of at-least-once execution of jobs section of this artcile will help.

8

Reply
A
aniu.reg
Top 5%
• 1 year ago
If a watcher fails, a stand by watcher can re-do the poll in the most recent 5 minute window and insert all the messages into the SQS. SQS can dedupe potential messages from old and new watcher (some dedupe logic needs to be added to SQS)
How long is a typical leader election? Is 5 minutes enough for a leader election? If this is a concern the watcher extend its window to match the election SLA.

0

Reply
P
PossibleLavenderBison719
• 6 months ago

A better design in my opinion would be to shard / partition the execution table and then assign a watcher service with a standby/secondary in case the primary watcher fails.

Taking this concept further we can apply consistent hashing technique and distribute the executionId over N nodes.

7

Reply
H
hellointerview
• 1 year ago

In the Executions table example, wouldn't there be a key collision if two executions were scheduled for the exact same time?

{
  "time_bucket": 1715547600,  // Partition key (Unix timestamp rounded down to hour)
  "execution_time": 1715548800,  // Sort key (exact execution time)
  "job_id": "123e4567-e89b-12d3-a456-426614174000",
  ....
}


If so, perhaps a solution could be to concatenate the job_id to the end of the execution_time so that it is still sorted by execution_time in a partition but avoids a collision. Any thoughts on this?

{
  "time_bucket": 1715547600,  // Partition key (Unix timestamp rounded down to hour)
  "execution_time_job_id": "1715548800#123e4567-e89b-12d3-a456-426614174000",  // Sort key (execution time + job ID)
  "execution_time": 1715548800,  // Exact execution time for querying
  "job_id": "123e4567-e89b-12d3-a456-426614174000",  // Unique job ID
  ...
}


13

Reply

Evan King

Admin
• 1 year ago

Yeah, good catch. So the partition key is used in DDB to determine the shard, so that needs to remain the time bucket, but the sort key can be time-jobId, and then we can use begins_with when searching.

15

Reply
A
ArtisticHarlequinKiwi700
• 1 year ago

I do not understand the use of execution time as the partition key for the Executions table since it is unclear how this key is hashed into underlying partitions (meaning that you will likely end up reading from all shards anyways)

12

Reply

Evan King

Admin
• 1 year ago

Great question. You can use the rounded Unix time as the partition key so that all jobs for, say, the same hour are hashed together. Then, have the actual execution time be the sort key.

16

Reply
Yiju Fang
Top 10%
• 1 year ago

But, wouldn't the current hour partition become hot partition since all new created job in the the current hour will write to that partition?

21

Reply
foram mehta
Premium
• 11 months ago

True it can become a hot partition. I had same question we can work around that by adding a random to generate the partition_key. example :- partition_key = time_bucket + "#" + hash(job_id)

2

Reply
I
ImmediateIvoryAngelfish117
Premium
• 10 months ago

How would you fetch all jobs for the current hour? there is no prefix matching in get by partition.

7

Reply

Evan King

Admin
• 1 year ago

Good question, maybe. It depends on what our write throughput is, which would depend on how many jobs are recurring versus single execution. If it becomes a problem, we could batch our writes with a message queue.

2

Reply
Yiju Fang
Top 10%
• 1 year ago

Yeah, think of a Black Friday flash sales in the 1st hours. We will probably see a spike of place order jobs created during that hour and all these jobs will write to the same hour key/partition. But you are right, we can use a queue to batch write these jobs.

6

Reply
Arunprasaath S
• 10 months ago

Each and every order should not be a job. These are async workflows. Probably one execution should process multiple orders.
There will be spikes but generally Job schedulers should not be having same number of increase corresponding to site traffic.

1

Reply
B
BlondeSilverBison603
Premium
• 5 months ago

Even if the write traffic isn't creating a hot partition, why laser all the read requests towards one or few partitions? feels odd setup to have most of the read at any point on one partition while all the other partitions are mostly dead...?

3

Reply
R
RoundBrownEgret745
Premium
• 3 months ago

If you had millions of jobs over the span of years, it's infeasible to scan through all job entries. Partitioning it by time buckets is reasonable since most, if not all job schedulers have pagination views and time sortable listings.

0

Reply
indavarapu aneesh
Premium
• 9 months ago

we could instead create the partition key on a 15 minute window basis.
for example: 0-14 -> 1, 15-29 -> 2, 30-44 -> 3, 45-59 -> 4
so the partition key would 177474747-1 (unix timestamp in hour + window key).

0

Reply
A
ArtisticHarlequinKiwi700
• 1 year ago

Yeah, I that's a valid point. I'd probably lean towards a more explicit sharding scheme (eg just mysql) and then process in parallel by shard.

2

Reply
W
WillingOliveSwordfish412
Premium
• 2 months ago
• edited 2 months ago

The way I understand it is that the timebucketed partition key will route all updates to jobs in an hour to a single partition. These will be periodic read queries by the watcher ~12 of those and all of the updates to job status by execution workers. Every second there will be 10k jobs in p50, and lets say it's 100k jobs in p100. A single DDB partition cannot handle this traffic. The specific limits are 3000 RCU and 1000 WCU per partition (lesser if we use conditional PUTs). Will get throttled.

But I think it's solvable. We can fanout each timebucket in 100 sub-partitions. Further partitioning in 15 mins intervals (as recommended in the thread) may not help as all of the writes for small jobs will still go on the same partition.

So for instance:

partitionkey = str(execution_time//3600)*3600 + '-' + hash(job_id)%100


That way the scatter gather during search will be limited to 100 partitions where as the writes can distribute over a much wider area. This is a ok tradeoff as Watcher can take a bit longer for the scatter gather to complete.

2

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

1) Users should be able to schedule jobs to be executed immediately, at a future date, or on a recurring schedule

2) Users should be able monitor the status of their jobs.

Potential Deep Dives

1) How can we ensure the system executes jobs within 2s of their scheduled time?

2) How can we ensure the system is scalable to support up to 10k jobs per second?

3) How can we ensure at-least-once execution of jobs?

What is Expected at Each Level?

Mid-level

Senior

Staff+
