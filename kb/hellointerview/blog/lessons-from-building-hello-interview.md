# 14 Lessons from Building Hello Interview

> Source: https://www.hellointerview.com/blog/lessons-from-building-hello-interview
> Scraped: 2026-03-30

14 Lessons from Building Hello Interview

By Stefan Mai

•

Dec 18, 2025


We've received quite a few questions about how Hello Interview is built. Rather than just listing our tech stack, I figured I'd share some of the actual lessons we've learned along the way. Some are obvious in hindsight. Others we're still not sure about.
A bit of context: we run the whole thing with three people (Evan, Stefan, and Shivam). A lot of our decisions are driven by "how do we keep this manageable?" rather than "what's the theoretically best architecture?" When you're juggling scheduling, payments, AI feedback, content management, and video interviews with a tiny team, you make different choices than a team of 50.
I wish I had a better way to organize this post, but we're just going to pack in as many nuggets as we can. Complain in the comments!
1. Type Safety Pays for Itself Fast
We like type safety. There are people who prefer dynamic typing. We're not those people.
Our entire API layer is built with tRPC and runs together with the web server. We're not building APIs for external clients; we're the only ones using it, so we can be opinionated.
One of our competitors once commented that they felt platforms were under-engineered and required a real language (like Go) and a separate API stack. We disagree, and they're no longer in business.
Here's the pitch for tRPC: end-to-end type safety for your API. When you write a backend endpoint:
export const scheduleInterview = protectedProcedure
  .input(z.object({
    coachId: z.string(),
    time: z.date(),
    interviewType: z.enum(['BEHAVIORAL', 'SYSTEM_DESIGN', 'CODING'])
  }))
  .mutation(async ({ input, ctx }) => {
    // Implementation
    return interview;
  });
The frontend automatically gets full TypeScript types for this endpoint. No code generation, no manual syncing of types. Just works.
// Frontend - this just works, with autocomplete and everything
const interview = await trpc.scheduleInterview.mutate({
  coachId: "...",
  time: new Date(),
  interviewType: "BEHAVIORAL"
});
We've shipped probably 50+ breaking changes to our API over the past year. Each one was caught at compile time before it could break production. That alone has probably saved us weeks of debugging.
The other benefit we didn't anticipate: AI tools love it. When Claude or Cursor can see the type signatures, they write much better code. The language server tells them exactly what the API expects and returns.
Streaming Responses Just Work
One of the coolest features of our tRPC setup is streaming. When you're generating AI feedback that takes 30 seconds to produce, you don't want users staring at a loading spinner. But streaming can quickly become a maintenance nightmare if you're not explicit about designing the messages that you'll be sending.
A lot of AI product design is about making things feel responsive. Streaming is the difference between "this is broken" and "oh cool, it's thinking."
tRPC helps with this by supporting streaming through async generators:
export const generateFeedback = protectedProcedure
  .input(z.object({ interviewId: z.string() }))
  .mutation(async function* ({ input, ctx }) {
    // Stream LLM responses in real-time
    for await (const chunk of ctx.deps.streamingCompletion(
      "Provide detailed feedback on this response...",
      { model: "gpt-5" }
    )) {
      yield chunk;
    }
  });
On the frontend:
for await (const feedback of trpc.generateFeedback.mutate({ 
  interviewId 
})) {
  setFeedbackText(prev => prev + feedback);
}
The types flow through perfectly. Under the hood, tRPC uses Server-Sent Events (SSE) for transport. Way simpler than WebSockets and works through most proxies. We had a hell of a time debugging websocket issues in production and still run into them occasionally.
2. Database Branching Changes How You Work
Most teams use a shared development database. This works until someone runs a migration that breaks everyone else's local setup. Or you want to test a big schema change without affecting other developers.
We use Neon for our dev/test databases. Neon supports database branching, which means every git branch can have its own database:
# Switch to a new feature branch
git checkout -b new-feature

# Point your local DATABASE_URL to a branch-specific database
yarn db:branch

# Now you have your own isolated database
# Run migrations, test changes, break things - it won't affect anyone else
yarn prisma migrate dev
When you merge your code, you merge your migrations. Each developer gets a clean, isolated database that matches their code branch.
We have git hooks that auto-switch your database when you change branches. It sounds fancy but it's just a script that updates your .env file.
Screw up? Just yarn db:reset and you're back to a fresh database.
This setup costs us maybe $50/month but saves a couple hours every week. Developers can be aggressive with schema changes without worrying about breaking the team.
3. Wrap Your LLM Calls
We make a lot of AI calls. Our bills at the end of the month hover around $10,000 USD across OpenAI, Anthropic, Anyscale, etc. Two challenges here: costs, and constantly evolving that volley of calls into something meaningful for users. We've wrapped this up in our @hi/llm package.
Thousands of vendors are trying to solve these problems. I've yet to find one with good tradeoffs for us. A good rule of thumb: the best abstractions (React, Spark, Temporal) take years to mature. It's early days for LLM infra. I'm sure we'll look back in hindsight at the choices we've made so far and consider them foolish.
Early on we had no idea how much this was costing us. We'd get the OpenAI bill at the end of the month and go "huh, that's higher than expected."
So we built cost tracking into our tRPC context. Every LLM call logs:
The exact prompt
Token counts (input and output)
Model used
Cost in micro-cents
Duration
Which API endpoint triggered it
// This happens automatically for every request
const feedback = await ctx.deps.completion(
  "Generate feedback for this interview...",
  { model: "gpt-4o" }
);
// Cost is logged to the database and OpenTelemetry
Now we can answer:
"Which features are most expensive to run?"
"Did switching to Sonnet actually save us money?"
"Why did our API bill spike on Tuesday?"
Getting that data properly logged is half the battle. The other half is using it.
By methodically modelling how we call LLMs, we can build meta-functionality on top:
We can A/B test different models in different contexts.
We can monitor the cost impact of swapping models.
We use GEPA to optimize prompts using real feedback from users.
We can wire up internal evaluation suites to help us iterate.
The list goes on.
4. Long-Running Processes are Painful, Temporal Saves Your Ass
Background jobs are usually the first thing to go wrong in a system. Email doesn't send because the service was down. Payment processes but the confirmation email fails. Video processing gets stuck halfway through.
We use Temporal for all background work. The pitch is "durable execution" but what that really means is: workflows that survive crashes.
// This runs as a workflow - it will complete even if servers crash
export async function processPayment(orderId: string, amount: number) {
  // Step 1: Charge the customer's card
  const charge = await activities.createStripeCharge(orderId, amount);
  
  // Step 2: Update our database with the payment record
  await activities.recordPayment(orderId, charge.id);
  
  // Step 3: Provision the purchased resource (credits, subscription, etc)
  await activities.provisionPurchase(orderId);
  
  // Step 4: Send confirmation email (might be delayed if service is down)
  await activities.sendReceiptEmail(orderId, charge.receiptUrl);
  
  return charge;
}
This is a classic example of the Multi-Step Processes pattern in system design. Temporal provides durable execution guarantees, ensuring each step completes exactly once even in the face of crashes, network failures, or service restarts.
If the server crashes after step 2, Temporal automatically restarts the workflow at step 3. Not from the beginning. From exactly where it left off. The charge already went through, the payment is already recorded.
This matters a lot for payments. If processing crashes after charging the card but before provisioning the purchase, you don't want to charge them twice. Temporal guarantees exactly-once execution.
We have 50+ different workflow types now. Coach onboarding sequences, payment processing, email campaigns, video transcoding. Anything where "it must complete eventually" matters.
The debugging story is incredible too. You can replay production workflows locally, step through them with a debugger, and see exactly why something failed. This has saved us countless hours of "why didn't that email send" investigations.
There are way more options available here today than when we started. Vercel just launched their own workflow,
5. Mini Monoliths Are Good for Speed
We run only two services: a Next.js web server and a Temporal worker service.
The web server handles requests, renders pages, processes API calls. Standard stuff.
The worker service runs in the background, processing workflows. Doesn't serve HTTP traffic at all.
Depending on who you ask, this is either dramatically under-engineered or a brilliant example of YAGNI. Web servers need to be fast and responsive. Workers need to be reliable and handle long-running tasks. They have different scaling needs, different resource requirements, different failure modes.
This follows the Scaling Reads pattern. Our web servers are stateless and sit behind a load balancer, making horizontal scaling effortless. Need more capacity? Spin up another instance. Traffic drops? Shut one down. The workers scale the same way through Temporal's task queue distribution.
In production we run a handful of web instances and a handful of worker instances. Both are completely stateless and autoscaled. No session data, no local caching, no shared memory.
The stateless design means:
Any web server can handle any request
Workers can be added or removed without coordination
Deployments involve zero state migration
Crashes don't lose data (it's all in Postgres/Redis/Temporal)
But despite our functionality covering dozens of different use-cases, we're deliberately not spawning a constellation of microservices. Remember, we have 3 people to support this. And we want to spend approximately 0% of our time with typical devops struggles.
6. CRDTs Are Magic for Real-Time Collaboration
During mock interviews, candidates and coaches need to collaborate in real-time. Drawing diagrams, writing code, chatting. This needs to work smoothly even when network conditions aren't perfect. Getting this right used to be a major undertaking. But there's a lot of primitives that make this substantially easier than it would have been a decade ago.
One of them is what we use, Yjs for real-time collaboration. It's a CRDT (Conflict-free Replicated Data Type) implementation that handles the tricky parts of multi-user editing.
The big problem CRDTs solve: two users edit the same document simultaneously. User A types "Hello" and User B types "world" at the same position. What's the final text?
Traditional approaches use operational transformation (like Google Docs) which requires a central server to order operations. CRDTs are different. They guarantee that all clients converge to the same state without a central coordinator.
// In the interview room, multiple users share the same Yjs document
const elements = useMap<string>("drawing/page-1");

// When anyone draws, it syncs automatically to all participants
// No manual WebSocket coordination needed
The beauty is that we don't write any synchronization code. Yjs handles conflicts automatically. If two people draw at the same time, both drawings appear. If they edit the same text, CRDTs merge the changes intelligently.
This works for:
Excalidraw diagrams (every element is a Yjs map entry)
Chat messages (Yjs array of message objects)
Monaco editor (collaborative code editing)
The tradeoff is memory. CRDTs store more metadata than operational transformation. But for interview sessions (1 hour, 2 participants), this isn't an issue.
Doubling down on Yjs wherever we needed real-time collaboration has been a game-changer, but it meant that it needs to absorb almost all of the state for that particular piece of the app. There are tradeoffs here.
7. Optimize for Ease of Development, Escape to System-Level Languages When Necessary
Most of our codebase is TypeScript. It works really well for us, the team knows it well, and it crosses both frontend and backend. But our scheduling logic (the code that finds available time slots for coaches across timezones) is written in Rust.
Why? Because it was too slow in TypeScript.
When you search for available interview times, we need to check hundreds of possible slots against coach availability, existing bookings, timezone conversions, and business rules. This was taking 2-3 seconds in TypeScript. Users would click "find times" and just... wait.
We probably could have written more performant TypeScript. Or precomputed and cached this. But that brings staleness bugs. Remember our objectives: evolve quickly and minimize maintenance. Being able to let a coach block something on their Google Calendar and immediately see it reflected in availability is huge.
We rewrote the core slot-finding logic in Rust, compiled it to WebAssembly, and now it runs in under 200ms. Same logic, 10x faster.
pub fn find_available_slots(
    coach_availability: &[TimeSlot],
    existing_bookings: &[TimeSlot],
    timezone: &str,
) -> Vec<TimeSlot> {
    // Core logic here
}
We still prototype scheduling features in TypeScript first. Once they work, if they're too slow, we port to Rust. Python-like development speed with C-like performance where it matters.
This pattern is used extensively in larger companies. You don't have to write your whole stack in Rust for Rust-like speeds. Profile your code, identify the hot paths, and those might be targets for a performance-oriented rewrite, sometimes in a system-level language.
8. Avoiding Kubernetes Complexity
Early on, we had a couple Dockerfiles and needed to get them deployed to production. There are a lot of options here. But many choices bleed into constraints for your app.
If you want to use Vercel, you're going all-in on Serverless. You need to be cognizant of cold-starts, deal with all the trickery of dependency compatibility, handling database connections ... it's a non-trivial amount of work.
If you use Kubernetes you get a ton of complexity but you get to take a second job in Kubernetes administration. And hosting a K8s cluster is not cheap.
If you use a smaller host like Railway, Fly, or Render, you're subject to growing pains of missing functionality or stability issues as you scale.
We've used AWS in the past and honestly the devX sucks but the flexibility and stability is unmatched. So it transforms the challenge from "how do we get this working?" to "how do we make this suck less?".
For that, we use AWS Copilot for infrastructure. It's a neglected side project of some AWS solutions engineer that scratches an itch that AWS in its infinite wisdom decided not to address.
Copilot generates CloudFormation templates from simple manifests:
# copilot/web/manifest.yml
name: web
type: Load Balanced Web Service
cpu: 2048
memory: 4096
This creates:
ECS services and tasks
Application load balancers
CloudWatch logs
Auto-scaling policies
Health checks
Service discovery
Secrets management
It's not as flexible as Kubernetes. But we don't need that flexibility. We have two services, not 50 microservices.
Deployments are just:
copilot svc deploy --name web --env prod
New code gets built into Docker images, pushed to ECR, and rolled out with zero downtime. If health checks fail, the deployment automatically rolls back.
We've found a lot of hosts get this "zero downtime" thing wrong. Especially when deploying web services with 2 different versions of the same code, there is a ton of edge cases in orchestrating deployments that can easily go wrong. I won't name names here, but needless to say we're done with having to play QA for deployment bugs of various platforms.
We also run our own Prometheus and Tempo instances for metrics and tracing. These run as separate Copilot services with persistent EFS volumes. Total additional cost: maybe $100/month (vs $1,000+/month for managed Datadog). Total additional operational complexity: basically zero.
9. Fork Libraries When You Have To
We maintain a folder called forked-packages that contains modified versions of open source libraries. Currently 8 packages, with things like:
Excalidraw (drawing editor)
Next.js safe navigation (type-safe routing)
Monaco Editor integrations
Modified tRPC internals
This sounds like a bad idea. And it might be.
But we routinely hit this problem: we need a feature from a library and we need it today. You can't wait for a GitHub issue to get traction, a PR to be reviewed, and a new release to be published. We try to contribute back where we can, but we can't hold our product hostage to it.
So we fork it, make our changes, and move on.
The downside is obvious. We're now responsible for keeping these forks up to date. When the upstream library releases a security fix, we need to merge it.
But the upside is velocity. We can iterate on the product without waiting for external dependencies.
Our philosophy: fork when you need to, but upstream aggressively and prune as soon as possible.
10. Let LLMs Write Your Release Notes
When we deploy to production, we run a script that generates release notes automatically:
yarn release
It does something obvious: looks at all commits since the last release, feeds them to an LLM, and asks it to categorize them:
Major changes (new features customers will notice)
Minor changes (improvements and tweaks)
Fixes (bug fixes and reliability improvements)
The LLM reads commit messages and diffs, figures out what actually changed, and writes human-readable release notes. Then it tags the GitHub users who made changes and triggers slack notifications.
This turns 5 minutes of tedious work into a 30-second script. The notes aren't perfect but they're good enough, and they're consistent.
We also use the LLM to detect "noise" commits that shouldn't be mentioned (like "fix type error" or "fix broken build"). No one cares about those in release notes.
11. Test the Money Paths
We use Playwright for end-to-end testing of our core flows. Specifically, the ones that involve money. Someone schedules an interview, pays with Stripe, gets emails, joins video calls. If any of that breaks, we lose revenue and trust.
So we test the actual purchase flow:
test('can purchase mock', async ({ page }) => {
    await page.goto("https://www.hellointerview.com/landing");
    await page.getByRole("button", { name: "Explore Mock Interviews" }).click();
    // ... walk through the entire flow
    
    // Actually fill in Stripe's iframe
    const paymentFrame = page.locator('[title="Secure payment input frame"]');
    await paymentFrame.locator("#Field-numberInput").fill("4242 4242 4242 4242");
    
    // Pay real money (test mode)
    await page.getByRole("button", { name: "Pay" }).click();
    
    // Then immediately cancel so we don't leave orphan sessions
    await page.locator('[aria-label="Cancel session"]').click();
});
This test creates a real user, sends a real magic link email, completes a real Stripe payment (in test mode), and then cancels the session. Every commit, this runs against our test environment. If Stripe changes their iframe structure, we know.
These E2E tests have caught a bunch of silly bugs that would have been really frustrating for our users. Unfortunately, E2E tests are flaky and slow to run. We've deliberately limited them to only the most important flows, which unfortunately means bugs slip through the cracks. We're slowly building out our test suite to catch more of these bugs.
12. Log Webhooks Before You Process Them
Webhooks are a pain. Every service sends them differently. Some sign them, some don't. Some need immediate responses, others don't care. And if your handler crashes, you might miss important events.
We built a generic webhook handler that logs to the database first, copies to a Redis stream, and then routes to the appropriate workflow.
Logging is critical. Before we do anything else, the raw webhook is persisted. If our handler crashes, we can replay it. If we need to debug what Stripe sent us three weeks ago, it's there.
Then we route based on type:
if (type === "gha") {
    // GitHub Actions workflow events
    await temporal.signalWithStart({
        workflowId: `github-monitor-${workflowRunId}`,
        workflowName: "monitorGithubWorkflow",
        signal: "receiveGithubEvent",
        signalArgs: [payload],
    });
} else if (type === "ses") {
    // Email received via SES
    const parsed = await simpleParser(decodedContent);
    // ... process and store email
} else if (type === "livekit") {
    // Video room events
    const event = await livekitReceiver.receive(rawBodyString, authHeader);
    // ... handle participant joined/left
}
Then we hand off to Temporal. The webhook returns 200 immediately. Actual processing happens asynchronously in a durable workflow.
This matters because webhooks have tight timeouts. Stripe gives you 30 seconds. If your handler does too much work, the webhook fails and gets retried. By offloading to Temporal, the response is fast and the work happens reliably.
Finally, that Redis stream is used by our yarn dev:webhook service to replay events for local development. Most services don't have nice local dev servers like Stripe for local development. Our generic webhook solution allows us to replay test events for local development without having to expose our dev servers to the world.
13. Slack Is a Better Admin UI Than You'd Expect
We have 25+ Slack channels for different notification types. Not because we love Slack, but because it has something we needed: an interactive UI that doesn't require building anything and is mobile accessible. Evan and Stefan are on the hook for all customer needs, so handling stuff from wherever is a priority.
export const SupportEmail = SlackBlockTemplate<Props>(({ from, subject, body }) => {
    return <Blocks>
        <Section>
            *From*: {from} {isPremiumUser ? "💎" : ""}<br />
            *Subject*: {subject}
        </Section>
        <Textarea id="response" label="Response" placeholder="Type your response..." />
        <Actions>
            <TypedButton style="primary" actionId="email_respond" value={{ emailReceivedId }}>
                Respond
            </TypedButton>
            <TypedButton style="danger" actionId="email_ignore" value={{ emailReceivedId }}>
                Ignore
            </TypedButton>
        </Actions>
    </Blocks>
});
This uses jsx-slack to write Slack Block Kit using JSX. When an email comes in, we send this to Slack. When we click "Respond", Slack fires an interactive webhook back to us with the action type and form values.
The typed actions are particularly nice:
export const typedActions = {
    "email_respond": {
        schema: z.object({
            emailReceivedId: z.string(),
        }),
    },
    "coach_application_response": {
        schema: z.object({
            coachId: z.string(),
            action: z.enum(["APPROVED", "REJECTED", "WAITLISTED"]),
        })
    },
    // ...
};
We get type safety from the Slack button all the way through to the handler. Sensing a theme here?
The templates are also updateable. When we respond to an email, the message updates to show it was handled. No more hunting through threads to see if someone already dealt with something.
We've built probably 15 different admin flows in Slack that would have taken 10x longer as proper web UIs. Coach onboarding decisions, W9 approvals, content moderation. All done from Slack without context switching.
The downside? It's Slack-specific. And Slack's APIs are a pain. But we're stuck with it for now.
14. Self-Host Observability If You Can
Observability is hella expensive, but occasionally incredibly useful. A lot of companies grin and bear huge Datadog bills in part because that occasionally useful is worth the cost. We tried to thread the needle by self-hosting our own observability stack:
OpenTelemetry for instrumentation
Prometheus for metrics
Tempo for distributed tracing
Grafana for dashboards
Sentry for errors
This costs maybe $200/month to self-host vs thousands per month for something like Datadog.
Every tRPC request is instrumented automatically:
Duration (P50, P95, P99)
Error rates
Request size
Response size
LLM costs
Database queries
We can trace a request from the frontend through the API to the database and see exactly where time is spent.
When something goes wrong, we have the data to debug it. When something gets slow, we know why. When costs spike, we know which endpoint is responsible.
What We'd Do Differently
We're happy with most of our choices but there's stuff we'd change:
Dead code cleanup: We're terrible at deleting old features. There are probably 10,000+ lines of code that could be removed. I wish AI was better at this. Type safety helps, but data dependencies are the root of all evil.
Test coverage: We test the important stuff (payments, scheduling) but a lot of the codebase has no tests. This is fine until it's not. We're increasingly finding AI is hobbled by insufficient test coverage.
Not-invented-here syndrome: We have a tendency to build things instead of using existing solutions. The LLM abstraction layer? Probably could have used LangChain. The scheduling logic? Probably could have used an existing library. But we built our own because it was faster than evaluating alternatives, more flexible, and... more fun. Fun is important.
These are all things we know about and are slowly addressing. But perfect is the enemy of shipped, and we've shipped a lot.
Wrapping Up
Hello Interview runs on a pretty straightforward stack: Next.js with tRPC, Postgres, Redis, Temporal, and a lot of LLM API calls.
What makes it work is how all the pieces fit together:
Type safety from database to frontend (Prisma → tRPC → React)
Durable background jobs (Temporal)
Proper cost tracking (custom logging)
Fast local development (Turborepo, database branching)
Good enough observability (self-hosted)
We prioritize shipping fast over perfect architecture. Most code is good enough. Some code (payments, scheduling) is tested extensively. Some code (admin tools) is barely tested at all.
This is a real product being used by real users, not a greenfield demo. Technical debt exists. Legacy code exists. We're constantly balancing "fix the old stuff" vs "build the new stuff."
While we don't think these lessons apply to every team or every company, we think they may be indicative of some future directions for software. By pulling functionality in-house, often augmented by AI, we give ourselves a lot of opportunity to optimize for our own needs.

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

Stefan is one of the co-founders of HelloInterview, a platform to help software engineers and other tech professionals to prepare for their dream roles. He's conducted 1,000+ interviews and hired dozens of individuals at big companies and small startups.

Recommended Reading

3 Networking Tricks to Level-Up Your System Design Interview

This is a strong fit for readers interested in practical engineering lessons, and it has the best normalized CTR in similar placements. It keeps the recommendation set blog-heavy while offering concrete system design insights.

System Design Trackers from Netflix's Ad Tracking Launch

The current article is about real lessons from building software, and this post offers the same 'lessons from real systems' angle through a recognizable engineering case study. It also performed very well historically in this placement.

Design a Collaborative Document Editor Like Google Docs

Problem breakdowns are explicitly favored for this slot, and this one was a top historical performer. It gives readers a hands-on continuation from high-level product-building lessons into a concrete system design exercise.

Over-engineering is getting you down-levelled

The current page mentions tradeoffs that actually matter, and this article reinforces that theme by showing why unnecessary complexity hurts candidates. It also has solid historical engagement relative to position.
Comments

(34)

Comment
Anonymous
​
Sort By
Popular
Sort By
R
robdoubleu
Premium
• 3 months ago

You guys have an impressive and extremely useful site, especially for so few developers.  Kudos and thanks for the learnings.

10

Reply

Stefan Mai

Admin
• 3 months ago

❤️

0

Reply
K
kapild.fb
Premium
• 3 months ago

Awesome stuff. Congrats on the run so far. I can't wait till the interviewer starts asking "How will you design Hello Interview website" in the system design interview rounds. ;)

5

Reply

Stefan Mai

Admin
• 3 months ago

I'd say "that's insane", but apparently interviewers are asking people to design leetcode so 🤷

3

Reply
Mykhailo Okhotnikov
Premium
• 3 months ago

Hi! I’m trying to reach your support team regarding a Premium subscription issue, but unfortunately I haven’t received any reply for 11 days.

I accidentally purchased the subscription using my work email and asked to transfer it to my personal email (or issue a refund). Since I’m waiting for this to be resolved, I haven’t been using the subscription or even the free content.

Sorry to bring this up here in the comments, but I wasn’t able to get a response via email.
Could someone from the team please help or point me to the right contact? I’d really appreciate it. Thank you!

2

Reply
Kian Farah
• 3 months ago

Great read! 🙌 Really appreciated the honest lessons and practical insights behind building  this platform. Super valuable for anyone building and scaling a product. 🚀

2

Reply
M
ManagerialOliveAntelope938
Premium
• 3 months ago

Really good blog, I’ll keep it in mind when I build my own website. Thanks!

2

Reply
Show All Comments
Reading Progress

On This Page

1. Type Safety Pays for Itself Fast

Streaming Responses Just Work

2. Database Branching Changes How You Work

3. Wrap Your LLM Calls

4. Long-Running Processes are Painful, Temporal Saves Your Ass

5. Mini Monoliths Are Good for Speed

6. CRDTs Are Magic for Real-Time Collaboration

7. Optimize for Ease of Development, Escape to System-Level Languages When Necessary

8. Avoiding Kubernetes Complexity

9. Fork Libraries When You Have To

10. Let LLMs Write Your Release Notes

11. Test the Money Paths

12. Log Webhooks Before You Process Them

13. Slack Is a Better Admin UI Than You'd Expect

14. Self-Host Observability If You Can

What We'd Do Differently

Wrapping Up

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
