"""Deterministic learning harness for coach-led study sessions.

The harness turns a topic into small executable learning units. It is not
trying to be a chatbot; it is the control loop around the chatbot:

teach one slice -> wait -> check -> evaluate -> repair or advance.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any

from agentcoach.content.compiler import EditorialUnit, compile_editorial_units


PROJECT_ROOT = Path(__file__).resolve().parents[2]

HELLOINTERVIEW_NETWORKING_URL = (
    "https://www.hellointerview.com/learn/system-design/core-concepts/"
    "networking-essentials"
)
HELLOINTERVIEW_NETWORKING_KB_PATH = (
    "kb/hellointerview/system-design/core-concepts_networking-essentials.md"
)

NETWORKING_UNIT_SOURCE_SECTIONS: dict[str, list[str]] = {
    "networking.mental_model": [
        "Networking 101",
        "Networking Layers",
        "Example: A Simple Web Request",
        "Wrapping Up",
    ],
    "networking.layers": [
        "Networking Layers",
        "Example: A Simple Web Request",
    ],
    "networking.network_layer": [
        "Network Layer Protocols",
    ],
    "networking.tcp_udp": [
        "Transport Layer Protocols",
        "UDP: Fast but Unreliable",
        "TCP: Reliable but with Overhead",
        "When to Choose Each Protocol",
    ],
    "networking.protocol_choice": [
        "Application Layer Protocols",
        "REST: Simple and Flexible",
        "GraphQL: Flexible Data Fetching",
        "gRPC: Efficient Service Communication",
    ],
    "networking.realtime_protocols": [
        "Application Layer Protocols",
        "Server-Sent Events (SSE): Real-Time Push Communication",
        "WebSockets: Real-Time Bidirectional Communication",
    ],
    "networking.webrtc": [
        "Application Layer Protocols",
        "WebRTC: Peer-to-Peer Communication",
    ],
    "networking.http_api": [
        "HTTP/HTTPS: The Web's Foundation",
        "REST: Simple and Flexible",
    ],
    "networking.latency": [
        "Example: A Simple Web Request",
        "Regionalization and Latency",
        "Content Delivery Networks (CDNs)",
        "Regional Partitioning",
    ],
    "networking.load_balancing": [
        "Load Balancing",
        "Types of Load Balancing",
    ],
    "networking.lb_client_side": [
        "Types of Load Balancing",
        "Client-Side Load Balancing",
    ],
    "networking.lb_dedicated": [
        "Types of Load Balancing",
        "Dedicated Load Balancers",
        "Layer 4 Load Balancers",
        "Layer 7 Load Balancers",
        "Health Checks and Fault Tolerance",
        "Load Balancing Algorithms",
    ],
    "networking.failures": [
        "Common Deep Dives and Challenges",
        "Handling Failures and Fault Modes",
        "Timeouts And Retries With Backoff",
        "Idempotency",
        "Circuit Breakers",
    ],
}

NETWORKING_COVERAGE_KEY_SECTIONS: list[str] = [
    "Networking 101",
    "Networking Layers",
    "Example: A Simple Web Request",
    "Network Layer Protocols",
    "Transport Layer Protocols",
    "UDP: Fast but Unreliable",
    "TCP: Reliable but with Overhead",
    "When to Choose Each Protocol",
    "Application Layer Protocols",
    "HTTP/HTTPS: The Web's Foundation",
    "REST: Simple and Flexible",
    "GraphQL: Flexible Data Fetching",
    "gRPC: Efficient Service Communication",
    "Server-Sent Events (SSE): Real-Time Push Communication",
    "WebSockets: Real-Time Bidirectional Communication",
    "WebRTC: Peer-to-Peer Communication",
    "Load Balancing",
    "Types of Load Balancing",
    "Client-Side Load Balancing",
    "Dedicated Load Balancers",
    "Layer 4 Load Balancers",
    "Layer 7 Load Balancers",
    "Health Checks and Fault Tolerance",
    "Load Balancing Algorithms",
    "Common Deep Dives and Challenges",
    "Regionalization and Latency",
    "Content Delivery Networks (CDNs)",
    "Regional Partitioning",
    "Handling Failures and Fault Modes",
    "Timeouts And Retries With Backoff",
    "Idempotency",
    "Circuit Breakers",
    "Wrapping Up",
]

NETWORKING_AGENTIC_BLUEPRINT: dict[str, dict[str, list[str]]] = {
    "networking.mental_model": {
        "card_points": [
            "Start from a browser request so the learner can see DNS, IP, TCP, and HTTP in order.",
            "One conceptual request hides several network exchanges, including lookup, connection setup, response, and possible teardown or reuse.",
            "Protocol choices land better once the learner can say which layer is doing which job.",
        ],
        "quiz_dimensions": [
            "simple web request narration",
            "DNS to IP to TCP to HTTP ordering",
            "connection setup and teardown overhead",
            "layer responsibility synthesis",
        ],
        "dynamic_insert_rules": [
            "If the learner starts with service boxes, ask them to trace the browser request from URL to HTTP response.",
            "If the learner mixes layer jobs, insert the DNS/IP/TCP/HTTP separation card.",
        ],
    },
    "networking.layers": {
        "card_points": [
            "A simple browser request is enough to see several layers working together.",
            "DNS gives the client a destination to try before a transport connection can carry an HTTP request.",
            "Connection setup and teardown are not usually interview deep dives, but they explain hidden latency.",
            "Persistent connections matter because repeated setup can become expensive.",
        ],
        "quiz_dimensions": [
            "DNS to transport to HTTP ordering",
            "browser request walkthrough",
            "connection setup overhead",
            "transport versus application intent",
        ],
        "dynamic_insert_rules": [
            "If the learner mixes DNS, transport, and HTTP jobs, insert a layer-separation card.",
            "If they describe a request as one instant hop, ask where setup latency enters.",
        ],
    },
    "networking.network_layer": {
        "card_points": [
            "IP is the layer that handles addressing and routing toward a destination.",
            "Private addresses can be perfectly useful inside your own network, but public traffic needs a routable entry point.",
            "TCP, UDP, and QUIC sit above IP and decide what delivery guarantees the application can lean on.",
            "Most system design interviews only need the practical distinction: what can be reached publicly, and what stays private.",
        ],
        "quiz_dimensions": [
            "IP routing responsibility",
            "public address versus private service boundary",
            "public versus private IP routing",
        ],
        "dynamic_insert_rules": [
            "If the learner skips addressing and routing, ask what the client can actually reach.",
            "If they expose every service publicly, ask what should stay on a private network.",
        ],
    },
    "networking.tcp_udp": {
        "card_points": [
            "Most interview designs can quietly assume TCP unless the product really benefits from a different tradeoff.",
            "UDP is useful when staying current matters more than recovering every old packet.",
            "QUIC is worth knowing as a modernized TCP-like option, but it is rarely the center of most designs.",
            "A good protocol choice explains what the product can tolerate: loss, reordering, setup cost, and browser support.",
        ],
        "quiz_dimensions": [
            "safe HTTPS baseline",
            "UDP fit and non-fit",
            "delivery guarantee trade-off",
            "QUIC and HTTP/3 caveat",
        ],
        "dynamic_insert_rules": [
            "If the learner says UDP is simply faster TCP, insert the loss-tolerance card.",
            "If they mention HTTP/3, ask what QUIC adds on top of UDP.",
        ],
    },
    "networking.protocol_choice": {
        "card_points": [
            "REST is the boring, useful default for public request-response APIs.",
            "GraphQL helps when clients need flexible shapes, but the backend still pays for query execution and resolver complexity.",
            "gRPC shines more often inside a service fleet, where typed contracts and efficient binary payloads are worth the tooling cost.",
            "For interviews, GraphQL and gRPC are tools to justify from requirements, not upgrades to mention by default.",
        ],
        "quiz_dimensions": [
            "REST public API default",
            "GraphQL under-fetch and resolver complexity",
            "gRPC internal contract",
            "public versus internal API boundary",
        ],
        "dynamic_insert_rules": [
            "If they choose GraphQL, ask where resolver fan-out and authorization are handled.",
            "If they choose gRPC for public clients, ask who controls the clients and tooling.",
        ],
    },
    "networking.realtime_protocols": {
        "card_points": [
            "SSE is a practical one-way push trick on top of HTTP; WebSocket is for a long-lived two-way channel.",
            "SSE can reconnect and resume from the last message, but real networks and proxies can still make it annoying.",
            "WebSocket starts with an HTTP upgrade, then leaves you with a persistent channel and an application protocol to define.",
            "WebSockets are powerful, but stateful connections shape load balancing, deploys, and fanout.",
        ],
        "quiz_dimensions": [
            "SSE reconnect and one-way push",
            "WebSocket stateful infra cost",
            "realtime protocol justification",
        ],
        "dynamic_insert_rules": [
            "If the learner chooses WebSocket for every realtime feature, compare SSE and WebSocket.",
            "If the learner proposes WebSocket without stateful connection handling, ask where sockets live.",
        ],
    },
    "networking.webrtc": {
        "card_points": [
            "WebRTC is mostly for audio/video calling in interviews, not a default collaboration answer.",
            "It still needs signaling so peers can discover each other before trying a direct connection.",
            "STUN helps peers learn routable addresses; TURN relays traffic when the direct path fails.",
            "The happy path is peer-to-peer, but production WebRTC needs fallbacks for failed connections.",
        ],
        "quiz_dimensions": [
            "WebRTC fit",
            "signaling server role",
            "STUN and TURN fallback",
            "peer-to-peer operational caveat",
        ],
        "dynamic_insert_rules": [
            "If they choose WebRTC without mentioning signaling or TURN, insert the WebRTC guardrail card.",
            "If they choose WebRTC for a normal collaborative doc, ask why WebSocket plus a server is not enough.",
        ],
    },
    "networking.http_api": {
        "card_points": [
            "HTTP gives the shared vocabulary most web APIs are built from: methods, paths, headers, bodies, and status codes.",
            "Stateless HTTP handlers are pleasant to scale because the next request can usually land on any healthy replica.",
            "HTTPS protects the bytes in transit, but the server still has to validate who is allowed to do what.",
            "REST works best when the resources and operations are easy to read from the endpoint itself.",
        ],
        "quiz_dimensions": [
            "HTTP operation shape",
            "stateless scaling",
            "REST endpoint meaning",
            "TLS security boundary",
        ],
        "dynamic_insert_rules": [
            "If the learner treats HTTPS as full application security, insert the TLS boundary card.",
            "If they keep session state in one replica, ask how the load balancer can fail over.",
        ],
    },
    "networking.latency": {
        "card_points": [
            "A single request hides many small waits: DNS, connection setup, distance, queues, services, and dependencies.",
            "Tail latency is where users feel the pain that averages tend to hide.",
            "A CDN is most useful when nearby edge servers can answer from cache instead of sending everyone back to origin.",
            "Regional partitioning can make local queries fast, but only if the data and users really have regional shape.",
        ],
        "quiz_dimensions": [
            "latency budget",
            "p95 and p99 interpretation",
            "CDN fit",
            "regional partitioning trade-off",
            "connection setup and pooling",
        ],
        "dynamic_insert_rules": [
            "If the learner only says make it faster, ask them to allocate a latency budget.",
            "If they add regions casually, ask what data becomes local and how failover works.",
        ],
    },
    "networking.load_balancing": {
        "card_points": [
            "Load balancing starts with a plain problem: once you add more servers, clients need a sensible way to find one.",
            "The first fork is whether clients participate in choosing a server or a dedicated balancer sits on the path.",
            "The choice changes update speed, operational control, and how quickly unhealthy servers stop receiving traffic.",
        ],
        "quiz_dimensions": [
            "core load-balancer job",
            "client-side versus dedicated routing",
            "health and update speed tradeoff",
        ],
        "dynamic_insert_rules": [
            "If the learner says add servers without routing, ask how clients find healthy capacity.",
            "If they say DNS only, ask how quickly updates propagate.",
        ],
    },
    "networking.lb_client_side": {
        "card_points": [
            "Client-side and DNS-based approaches can be fast, but updates move at the speed of discovery or TTLs.",
            "Client-side balancing works well when clients are under your control, such as gRPC services or Redis Cluster clients.",
            "DNS is a kind of client-side balancing for the public internet, but cached records make failure updates slower.",
            "The practical interview point is to mention endpoint discovery and what happens when the chosen server is wrong.",
        ],
        "quiz_dimensions": [
            "client-side and DNS load balancing",
            "service registry and controlled clients",
            "DNS TTL and stale endpoint risk",
        ],
        "dynamic_insert_rules": [
            "If they mention DNS, ask about TTL and stale routing.",
            "If they mention client-side balancing, ask how clients receive server-list updates.",
        ],
    },
    "networking.lb_dedicated": {
        "card_points": [
            "A dedicated load balancer adds a hop, but gives the system quick health updates and much finer routing control.",
            "L4 is closer to the transport connection; L7 understands HTTP-level details like path, headers, and cookies.",
            "The routing algorithm matters more when requests or connections are uneven, especially with SSE and WebSockets.",
        ],
        "quiz_dimensions": [
            "health checks",
            "sticky-session risk",
            "L4 versus L7",
            "algorithm fit",
        ],
        "dynamic_insert_rules": [
            "If the learner says load balancer without health checks, insert the health-gated routing card.",
            "If they choose sticky sessions, ask how failover works when that backend dies.",
            "If they use WebSockets behind L7, ask what happens after the upgrade.",
        ],
    },
    "networking.failures": {
        "card_points": [
            "The dangerous assumption is that the network is reliable; real systems need a plan for delay and failure.",
            "Timeouts keep callers from hanging forever, but retries need backoff and jitter so recovery does not become load.",
            "Idempotency is what keeps a retry from turning one payment into two.",
            "Circuit breakers are the oncall-won pattern for failing fast when a dependency is already in trouble.",
            "The best answers connect failure policy to user experience: wait, retry, fall back, or fail clearly.",
        ],
        "quiz_dimensions": [
            "timeout purpose",
            "retry budget and backoff",
            "idempotency for side effects",
            "jitter and retry storms",
            "circuit breaker behavior",
            "end-to-end failure policy",
        ],
        "dynamic_insert_rules": [
            "If the learner says retry until success, insert the retry-storm card.",
            "If they retry writes without idempotency, insert the duplicate-side-effect card.",
            "If one dependency failure can consume all callers, insert the circuit-breaker card.",
        ],
    },
}


@dataclass(frozen=True)
class LearningUnit:
    id: str
    title: str
    objective: str
    body: str
    example: str
    coach_script: str
    key_points: list[str]
    check_prompt: str
    options: list[dict[str, str]]
    correct_option_id: str
    expected_keywords: list[str]
    repair: str
    flash_body: str = ""
    source_path: str = ""
    source_url: str = ""
    source_sections: list[str] = field(default_factory=list)
    source_paragraphs: list[dict[str, Any]] = field(default_factory=list)
    draft: dict[str, Any] = field(default_factory=dict)
    quizzes: list[dict[str, Any]] = field(default_factory=list)


NETWORKING_UNITS: list[LearningUnit] = [
    LearningUnit(
        id="networking.mental_model",
        title="Start with the browser request",
        objective="Trace one simple web request before choosing protocols or optimizations.",
        body=(
            "Let's start small. Imagine you type a URL into the browser and press enter. DNS "
            "turns that human-readable name into an IP address. IP routes packets toward that "
            "destination. TCP sets up a reliable, ordered connection. HTTP carries the page "
            "request and response. The diagram below follows that path. The important lesson "
            "is that one visible page load is really several exchanges, including connection "
            "setup and possible teardown or reuse. Once you can say which layer owns which job, "
            "protocol choices stop feeling like memorized trivia."
        ),
        example=(
            "When a browser opens a page, DNS gets an address, the client starts "
            "a TCP handshake to that server over IP, the browser sends an HTTP GET, the server "
            "responds, and the connection is closed or kept alive. If the page feels slow, the "
            "delay may be in lookup, connection setup, routing distance, server processing, or "
            "the extra packets around the request."
        ),
        coach_script=(
            "First bite: use one browser request as your anchor. DNS finds the address, "
            "IP routes packets, TCP gives a reliable ordered stream, and HTTP carries the app request."
        ),
        key_points=[
            "DNS: name -> IP",
            "IP: route packets",
            "TCP: reliable ordered stream",
            "HTTP: request + response",
            "Latency: setup, packets, reuse",
        ],
        check_prompt="Why do we care about networking in a system design interview?",
        options=[
            {
                "id": "a",
                "label": "Request path",
            },
            {
                "id": "b",
                "label": "Database schema",
            },
            {
                "id": "c",
                "label": "Packet trivia",
            },
        ],
        correct_option_id="a",
        expected_keywords=["dns", "ip", "tcp", "http", "latency"],
        repair=(
            "Use this order: DNS resolves the name, IP routes packets, TCP establishes "
            "a reliable stream, HTTP carries the request and response, and the connection is "
            "closed or reused."
        ),
    ),
    LearningUnit(
        id="networking.layers",
        title="Tell the layer story without reciting OSI",
        objective="Place DNS, IP, TCP/UDP/QUIC, and HTTP in the right part of the request story.",
        body=(
            "The full networking stack is fascinating, but most interviews only need a few "
            "anchors. A browser request is a good way to keep them straight: resolve the domain, "
            "reach an address, establish transport when needed, send the application request, "
            "and eventually close or reuse the connection. The point is not to recite OSI trivia. "
            "The point is to know which layer is responsible for which kind of work so your answer "
            "does not turn into a vague cloud of protocols."
        ),
        example=(
            "For a simple web page, the browser resolves the domain, packets are routed toward "
            "the destination, a reliable connection is established, and then the HTTP request "
            "is sent. You rarely need the packet-level mechanics, but the order keeps your "
            "answer from getting mushy."
        ),
        coach_script=(
            "Second bite: layers are a way to stay organized. DNS finds the address, IP routes "
            "packets, transport defines delivery behavior, and HTTP carries the app request."
        ),
        key_points=[
            "DNS: find destination",
            "IP: move packets",
            "Transport: choose guarantees",
            "Application: express product intent",
        ],
        check_prompt="Which sequence best matches a basic browser request?",
        options=[
            {"id": "a", "label": "DB -> HTTP -> DNS"},
            {"id": "b", "label": "DNS -> TCP -> HTTP"},
            {"id": "c", "label": "Cache -> IP -> Login"},
        ],
        correct_option_id="b",
        expected_keywords=["dns", "tcp", "http", "ip", "route"],
        repair=(
            "The safe interview order is: resolve the name with DNS, establish the "
            "transport connection if needed, then send the application request."
        ),
    ),
    LearningUnit(
        id="networking.network_layer",
        title="Ask who is allowed to reach this service",
        objective="Separate private addressing, public reachability, and routing from API behavior.",
        body=(
            "Keep the network layer simple: IP is about addressing and routing. Machines can have "
            "private addresses that only mean something inside your own "
            "network, but public internet traffic needs a routable entry point that the wider routing "
            "infrastructure knows how to reach. In interviews, this matters because not every service "
            "should be directly exposed. Usually you expose an edge, gateway, load balancer, or public "
            "service, then keep the rest of the fleet on private addresses behind it."
        ),
        example=(
            "Your API gateway may have a public address and DNS name. The application services, cache, "
            "and database behind it can live on private addresses. The user reaches the public entry "
            "point; internal calls stay inside the private network."
        ),
        coach_script=(
            "Network layer bite: IP handles addressing and routing. Public traffic needs a routable entry "
            "point; internal services can stay private behind that boundary."
        ),
        key_points=[
            "IP: address + route",
            "Private IP: internal boundary",
            "Public IP: internet-routable entry",
            "Expose edge: hide internals",
        ],
        check_prompt="Why not give every backend service a public internet-facing address?",
        options=[
            {"id": "a", "label": "Most services can stay private behind a public entry point"},
            {"id": "b", "label": "Private IPs make retries impossible"},
            {"id": "c", "label": "HTTP only works on database machines"},
        ],
        correct_option_id="a",
        expected_keywords=["private", "public", "edge", "gateway", "routable", "ip"],
        repair=(
            "Separate reachability from implementation. Public traffic should enter through a small "
            "set of routable entry points, while internal services can use private addresses."
        ),
    ),
    LearningUnit(
        id="networking.tcp_udp",
        title="Use TCP by default; defend UDP when freshness wins",
        objective="Know when reliable delivery matters, when loss is acceptable, and where QUIC/TLS fit.",
        body=(
            "For most system design interviews, TCP is the quiet default. It gives the application "
            "a reliable, ordered stream, so the rest of the design can spend attention elsewhere. "
            "UDP is the exception you should be able to defend: it is lighter and has no connection "
            "setup, but it also gives up delivery, ordering, and duplicate protection. That can be "
            "exactly right for media or games, where stale data may be worse than missing data. "
            "QUIC is the modern wrinkle: useful to know, but usually not where the interview should "
            "spend most of its time."
        ),
        example=(
            "A payment charge wants reliability and clear duplicate protection, so HTTPS is the "
            "natural baseline. A live audio call can often tolerate a tiny dropout better than it "
            "can tolerate waiting for old audio to be retransmitted, so a UDP-based media path is "
            "much easier to justify."
        ),
        coach_script=(
            "Third bite: TCP is the default because it is reliable and ordered. UDP is a choice "
            "you defend when freshness matters more than perfect delivery. QUIC is the modern "
            "HTTP/3 path, and TLS is your in-transit encryption layer."
        ),
        key_points=[
            "TCP: default reliability",
            "UDP: freshness over perfection",
            "Loss: tolerate or repair",
            "TLS: encrypt in transit",
            "QUIC/HTTP3: modern note",
        ],
        check_prompt="Which case is the best UDP-style fit?",
        options=[
            {"id": "a", "label": "Credit card"},
            {"id": "b", "label": "Live audio"},
            {"id": "c", "label": "Password update"},
        ],
        correct_option_id="b",
        expected_keywords=["udp", "loss", "latency", "stream", "webrtc", "gaming", "voip"],
        repair=(
            "Use TCP when correctness matters more than latency. Use UDP-style "
            "delivery when the product can tolerate small loss, like voice, video, "
            "games, or high-volume telemetry. Mention TLS when data crosses an untrusted network."
        ),
    ),
    LearningUnit(
        id="networking.protocol_choice",
        title="Let the product choose the protocol",
        objective="Choose REST, GraphQL, gRPC, SSE, WebSocket, or WebRTC from the product's communication shape.",
        body=(
            "Here is the pleasantly boring coach answer: REST is a strong baseline for public APIs, "
            "and you should only reach for something else when the product asks for it. GraphQL is "
            "about flexible client-shaped reads, but the backend can still pay for complexity. gRPC "
            "is more compelling inside a service fleet where typed contracts, deadlines, streaming, "
            "and binary payloads help. The mistake to avoid is treating these as upgrades. They are "
            "answers to different constraints."
        ),
        example=(
            "A profile API can start as REST and be perfectly fine. A backend fleet with strict internal "
            "contracts might use gRPC. A mobile client with many overlapping page shapes may justify "
            "GraphQL, but then you should be ready to talk about resolver fan-out, caching, and authorization."
        ),
        coach_script=(
            "Fourth bite: ask what kind of conversation the product needs. One request and one response "
            "is REST. Flexible client data is GraphQL. Typed internal calls can be gRPC. One-way push can "
            "be SSE. Two-way live updates can be WebSocket. Media calls point to WebRTC."
        ),
        key_points=[
            "REST: public API baseline",
            "GraphQL: flexible reads, backend cost",
            "gRPC: typed internal calls",
            "Realtime: choose by direction",
        ],
        check_prompt="Which protocol shape best fits live chat message delivery?",
        options=[
            {"id": "a", "label": "WebSocket"},
            {"id": "b", "label": "One nightly batch job"},
            {"id": "c", "label": "Database index only"},
        ],
        correct_option_id="a",
        expected_keywords=["websocket", "bidirectional", "persistent", "chat", "realtime"],
        repair=(
            "Live chat wants the server to push updates to a connected client. A long-lived "
            "bidirectional channel like WebSocket usually fits better than repeated polling."
        ),
    ),
    LearningUnit(
        id="networking.realtime_protocols",
        title="Check the direction before you say WebSocket",
        objective="Choose SSE or WebSocket based on directionality, persistence, and infrastructure cost.",
        body=(
            "A lot of designs jump straight from 'realtime' to WebSocket. Slow down and check direction first. "
            "If the server mostly pushes updates and the client listens, SSE can be a nice HTTP-based "
            "hack: one response streams many events over time, and EventSource can reconnect with the "
            "last event ID. If both sides need to speak whenever they want, WebSocket is the stronger fit. "
            "But WebSocket is not free. It is a persistent, stateful connection, and your load balancers, "
            "proxies, deploys, and fanout plan all have to respect that."
        ),
        example=(
            "Auction price updates can often use SSE because bidders mainly receive events. A chat room "
            "usually wants WebSocket because clients and server both send messages. In either case, you "
            "still need to explain how connections are held, reconnected, and balanced."
        ),
        coach_script=(
            "Realtime bite: SSE is server push over HTTP; WebSocket is a persistent two-way channel. Pick by "
            "directionality, then discuss connection management."
        ),
        key_points=[
            "SSE: server -> client",
            "Reconnect: resume event stream",
            "WebSocket: two-way persistent",
            "Infra: balance long connections",
        ],
        check_prompt="When is SSE a cleaner answer than WebSocket?",
        options=[
            {"id": "a", "label": "Server pushes updates and the client mostly listens"},
            {"id": "b", "label": "Peer-to-peer video with NAT traversal"},
            {"id": "c", "label": "A one-time password update"},
        ],
        correct_option_id="a",
        expected_keywords=["sse", "server", "push", "one-way", "event", "reconnect"],
        repair=(
            "Use SSE when the client mainly listens to a server event stream. Use WebSocket when both "
            "client and server need a long-lived two-way channel."
        ),
    ),
    LearningUnit(
        id="networking.webrtc",
        title="Only reach for WebRTC when media really needs it",
        objective="Use WebRTC for peer media paths while remembering signaling, STUN, TURN, and fallback.",
        body=(
            "WebRTC is the most tempting protocol to overuse. It enables browsers to exchange media or "
            "data directly, which sounds magical until you remember that most clients cannot simply accept "
            "inbound connections. A real WebRTC design still needs a signaling server so peers can find each "
            "other, STUN so they can discover public address information, and TURN as a relay fallback when "
            "a direct path fails. So keep WebRTC narrow in interviews: mostly audio/video calls and cases "
            "where a peer media path is actually worth the extra moving parts."
        ),
        example=(
            "For a video call, REST or WebSocket can handle login and signaling, then WebRTC carries the "
            "audio/video stream. If the direct peer path fails, TURN relays the media. For a normal shared "
            "document, a central server with WebSocket is often simpler to explain."
        ),
        coach_script=(
            "WebRTC bite: use it mainly for audio and video calls. Mention signaling, STUN, TURN, and fallback "
            "or the answer sounds too magical."
        ),
        key_points=[
            "WebRTC: audio/video media",
            "Signaling: peers find each other",
            "STUN: discover public path",
            "TURN: relay fallback",
        ],
        check_prompt="What should you mention when choosing WebRTC?",
        options=[
            {"id": "a", "label": "Signaling plus STUN/TURN and fallback"},
            {"id": "b", "label": "Only a REST endpoint named /call"},
            {"id": "c", "label": "A larger SQL index"},
        ],
        correct_option_id="a",
        expected_keywords=["webrtc", "signaling", "stun", "turn", "nat", "fallback"],
        repair=(
            "Do not make WebRTC sound magic. Pair it with signaling, NAT traversal, TURN fallback, "
            "and a narrow use case like audio/video calling."
        ),
    ),
    LearningUnit(
        id="networking.http_api",
        title="Make the API easy to say out loud",
        objective="Use methods, paths, headers, bodies, and status codes to describe web API operations.",
        body=(
            "HTTP is useful because it gives everyone in the room a shared language. Methods, paths, "
            "headers, bodies, and status codes are enough to describe most public API operations "
            "without inventing a custom protocol. REST leans on that vocabulary by treating many API "
            "calls as operations on resources. HTTPS then protects the traffic in transit, but it does "
            "not make the request body trustworthy; the server still validates identity, authorization, "
            "and input."
        ),
        example=(
            "GET /users/{id} reads one user resource. POST /users creates a user. PUT /users/{id} "
            "updates that resource. If a client sends a user ID in the body, HTTPS keeps that body "
            "private on the wire, but your server still has to verify the caller is allowed to use it."
        ),
        coach_script=(
            "Fifth bite: HTTP gives you a clean vocabulary. Method, path, headers, body, status code. "
            "Then connect it to scaling: stateless HTTP handlers are easier to replicate behind a "
            "load balancer."
        ),
        key_points=[
            "Method: operation verb",
            "Path: resource identity",
            "Status: outcome signal",
            "Stateless: any replica can serve",
            "HTTPS: encrypt, still validate",
        ],
        check_prompt="Why is stateless HTTP useful for scalable services?",
        options=[
            {"id": "a", "label": "Any replica can serve"},
            {"id": "b", "label": "No indexes needed"},
            {"id": "c", "label": "No auth needed"},
        ],
        correct_option_id="a",
        expected_keywords=["stateless", "server", "load balancer", "scale", "replica"],
        repair=(
            "Stateless means the service can usually treat each request independently. "
            "That makes it easier for a load balancer to send any request to any "
            "healthy replica."
        ),
    ),
    LearningUnit(
        id="networking.latency",
        title="Budget the path before you optimize it",
        objective="Break latency into DNS, connection setup, network distance, service time, and queueing.",
        body=(
            "Latency is not only server processing time. A request can spend time resolving a name, "
            "setting up or reusing a connection, crossing physical distance, waiting in queues, and "
            "calling dependencies. For global products, physics starts to show up in the architecture. "
            "CDNs help when nearby edge servers can answer from cache. Regional partitioning helps when "
            "users mostly need local data, like a ride request in one city."
        ),
        example=(
            "Static images for users around the world are a CDN-shaped problem. Matching riders and drivers "
            "inside one city is a regional-data problem. A checkout path with high p99 during spikes may be "
            "a queue, connection pool, or dependency problem rather than a pure networking problem."
        ),
        coach_script=(
            "Sixth bite: latency is a budget, not a wish. Split it into lookup, connection, distance, "
            "service work, dependency calls, and queueing. Use p95 or p99 when you mean user pain."
        ),
        key_points=[
            "Lookup: DNS time",
            "Setup: connection cost",
            "Distance: physics matters",
            "Tail: p95/p99 pain",
            "Move closer: CDN or region",
        ],
        check_prompt="Which metric best catches slow experiences hidden by the average?",
        options=[
            {"id": "a", "label": "p95 or p99 latency"},
            {"id": "b", "label": "Button count"},
            {"id": "c", "label": "Table name length"},
        ],
        correct_option_id="a",
        expected_keywords=["p95", "p99", "tail", "latency", "percentile"],
        repair=(
            "Average latency can hide the users who are waiting the longest. In interviews, "
            "say p95 or p99 when you care about real user pain."
        ),
    ),
    LearningUnit(
        id="networking.load_balancing",
        title="When you add servers, explain who picks one",
        objective="Explain health checks, L4/L7 choice, routing policy, failover, and sticky-session risk.",
        body=(
            "Horizontal scaling sounds easy on a whiteboard: add more boxes. The missing sentence is how "
            "clients learn which box to call. That is the core load-balancing problem. The first fork is "
            "where the routing decision lives. Clients can sometimes choose from a registry or DNS answer. "
            "A dedicated load balancer can sit in the path and choose on every new request or connection. "
            "The rest of the discussion is really about freshness and control: how fast unhealthy backends "
            "disappear, how much latency the routing layer adds, and how much application information it can see."
        ),
        example=(
            "DNS can spread users across load balancers or regions, but stale cached records mean failover is "
            "bounded by TTLs. A dedicated load balancer adds a hop but can quickly stop sending new traffic to "
            "a backend that fails health checks."
        ),
        coach_script=(
            "Seventh bite: a load balancer is traffic control. It chooses healthy capacity. Mention health "
            "checks, L4 versus L7, routing policy, failover, and why stateless services are easier to balance."
        ),
        key_points=[
            "Question: who picks server?",
            "Health: remove bad backends",
            "Client-side: freshness risk",
            "Dedicated: central policy",
            "State: stateless is easier",
        ],
        check_prompt="Why do stateless services work better behind a load balancer?",
        options=[
            {"id": "a", "label": "Any healthy replica can handle the request"},
            {"id": "b", "label": "The database disappears"},
            {"id": "c", "label": "Network latency becomes zero"},
        ],
        correct_option_id="a",
        expected_keywords=["stateless", "replica", "healthy", "load balancer", "route"],
        repair=(
            "If each request carries enough context, the load balancer can send it to any healthy "
            "replica. Sticky sessions reduce that freedom and make failover messier."
        ),
    ),
    LearningUnit(
        id="networking.lb_client_side",
        title="If the client picks, plan for stale endpoints",
        objective="Explain client-side load balancing, service discovery, DNS rotation, and TTL trade-offs.",
        body=(
            "Client-side load balancing is easy to miss because there may be no obvious load balancer box "
            "on the diagram. The client asks some registry or directory which servers exist, then chooses "
            "one directly. This is great when clients are under your control, as with internal services, "
            "gRPC client-side balancing, or Redis Cluster clients. DNS is the public-internet cousin of this "
            "idea: resolvers return different IPs, but cached records and TTLs mean updates are not instant."
        ),
        example=(
            "A Redis Cluster client can learn the shard map and send a key to the right node. A browser using "
            "DNS may get a rotated list of IPs, but if one endpoint dies, some clients may keep stale records "
            "until the TTL expires."
        ),
        coach_script=(
            "Client-side load balancing bite: it is fast when clients are controlled, but you must explain "
            "server-list freshness and stale choices."
        ),
        key_points=[
            "Client picks: no central hop",
            "Registry: fresh endpoints",
            "DNS TTL: stale records linger",
            "Retry route: handle wrong node",
        ],
        check_prompt="What is the main risk of DNS-based load balancing?",
        options=[
            {"id": "a", "label": "Clients can keep stale endpoints until TTLs expire"},
            {"id": "b", "label": "HTTP methods disappear"},
            {"id": "c", "label": "Every backend becomes public by default"},
        ],
        correct_option_id="a",
        expected_keywords=["dns", "ttl", "stale", "cache", "endpoint", "resolver"],
        repair=(
            "DNS can spread traffic, but cached records make updates slow. Mention TTLs and what clients "
            "do when an endpoint is stale or unhealthy."
        ),
    ),
    LearningUnit(
        id="networking.lb_dedicated",
        title="Choose L4 or L7 by what the balancer can see",
        objective="Choose L4 or L7 balancing, health checks, and routing algorithms for the traffic shape.",
        body=(
            "Dedicated load balancers are the familiar server-side option. They add another hop, but in exchange "
            "they can keep health information fresh and centralize routing policy. L4 balancers work closer to "
            "the transport connection, so they are natural for high-throughput or persistent-connection traffic. "
            "L7 balancers understand HTTP-level details such as host, path, headers, and cookies, which makes "
            "them better for application-aware routing. Algorithms matter too: round robin is fine for even "
            "stateless requests, but least-connections is often better when connections stay open."
        ),
        example=(
            "For normal HTTP APIs, an L7 balancer can route /api to one fleet and static pages elsewhere. For "
            "WebSockets, the balancing decision mostly happens when the connection is established, so L4 plus "
            "least-connections is easier to justify."
        ),
        coach_script=(
            "Dedicated balancer bite: L4 sees connections, L7 sees HTTP. Add health checks and choose an algorithm "
            "that matches whether requests are short or connections are long."
        ),
        key_points=[
            "Health checks: stop new traffic",
            "L4: transport connection",
            "L7: HTTP-aware routing",
            "Algorithm: match traffic shape",
        ],
        check_prompt="Why might WebSocket traffic push you toward L4 or least-connections?",
        options=[
            {"id": "a", "label": "Connections are long-lived, so active connection count matters"},
            {"id": "b", "label": "WebSocket removes all backend failures"},
            {"id": "c", "label": "L7 can rebalance every message for free"},
        ],
        correct_option_id="a",
        expected_keywords=["websocket", "l4", "least", "connection", "persistent", "long"],
        repair=(
            "After a WebSocket upgrade, the connection is long-lived. Balance new connections carefully and "
            "track active connection counts instead of assuming short independent HTTP requests."
        ),
    ),
    LearningUnit(
        id="networking.failures",
        title="Make retries safe before you automate them",
        objective="Connect latency, timeout, retry, idempotency, and observability.",
        body=(
            "The most dangerous networking assumption is that the network is reliable. Sometimes the call "
            "fails. Sometimes it is merely slow. Sometimes the answer arrives after the caller already gave "
            "up. Retrying can help with transient failures, but it can also duplicate side effects or create "
            "a synchronized wave of load. This is why a good interview answer pairs timeouts and retries with "
            "backoff, jitter, idempotency for writes, and circuit breakers when a dependency is already failing."
        ),
        example=(
            "If a payment charge times out, blindly trying again can turn one charge into two. A safer API "
            "uses an idempotency key so repeated attempts map to the same logical operation. If the payment "
            "provider is failing repeatedly, a circuit breaker can fail fast for a while instead of feeding "
            "the dependency more traffic while it is trying to recover."
        ),
        coach_script=(
            "Final bite for this block: recovery needs guardrails. Say timeout, retry with backoff and jitter, "
            "idempotency for side effects, and circuit breakers when a dependency keeps failing."
        ),
        key_points=[
            "Timeout: bound waiting",
            "Retry: backoff + jitter",
            "Idempotency: no duplicate writes",
            "Circuit breaker: fail fast",
            "Observe: watch tail failures",
        ],
        check_prompt="What must be true before safely retrying a payment request?",
        options=[
            {"id": "a", "label": "Idempotency key"},
            {"id": "b", "label": "Retry faster"},
            {"id": "c", "label": "UDP database"},
        ],
        correct_option_id="a",
        expected_keywords=["idempot", "duplicate", "retry", "backoff", "budget", "timeout"],
        repair=(
            "The safe answer is: retry only with duplicate protection. For payments, "
            "that usually means an idempotency key so the same logical operation is "
            "not applied twice."
        ),
    ),
]


NETWORKING_QUIZ: dict[str, list[dict[str, Any]]] = {
    "networking.mental_model": [
        {
            "id": "mental_model.request_path",
            "title": "Trace the browser request",
            "prompt": "Which sequence best matches a simple browser request?",
            "options": [
                {
                    "id": "a",
                    "label": "DNS -> IP routing -> TCP -> HTTP response -> reuse or teardown",
                },
                {"id": "b", "label": "To choose database indexes first"},
                {"id": "c", "label": "The server renders HTML before the client has an address"},
            ],
            "correct_option_id": "a",
            "expected_keywords": [
                "dns",
                "ip",
                "route",
                "tcp",
                "http",
                "response",
                "teardown",
                "reuse",
            ],
            "rationale": (
                "Right: a simple request starts by resolving the name, routing "
                "toward the address, setting up transport, carrying HTTP, and then closing "
                "or reusing the connection."
            ),
            "repair": (
                "Keep the opening order tight: DNS gives the client an address, IP moves "
                "packets toward it, TCP establishes the connection, HTTP returns the response, "
                "and the connection is either reused or torn down."
            ),
        },
        {
            "id": "mental_model.diagram",
            "title": "Read the simple path",
            "prompt": "What should the opening diagram for this request emphasize?",
            "options": [
                {"id": "a", "label": "Browser -> DNS -> IP routing -> TCP -> HTTP response"},
                {"id": "b", "label": "Only inside the database schema"},
                {"id": "c", "label": "Only the final server render time"},
            ],
            "correct_option_id": "a",
            "expected_keywords": ["browser", "dns", "ip", "tcp", "http"],
            "rationale": (
                "Right: the first mental model is the browser request path across layers, "
                "not a generic distributed-system box diagram."
            ),
            "repair": (
                "Use this path: browser enters a URL, DNS resolves it, IP routes "
                "packets, TCP establishes the stream, HTTP gets the response, and the "
                "connection is closed or reused."
            ),
        },
        {
            "id": "mental_model.tradeoff",
            "title": "Notice the hidden cost",
            "prompt": "Why should you care that one browser request involves several exchanges?",
            "options": [
                {"id": "a", "label": "Lookup, connection setup, packets, and state can add latency"},
                {"id": "b", "label": "Button color and typography"},
                {"id": "c", "label": "Only SQL normalization"},
            ],
            "correct_option_id": "a",
            "expected_keywords": ["latency", "setup", "connection", "packet", "state"],
            "rationale": (
                "Right: the useful observation is that a single conceptual request hides "
                "lookup, transport setup, many packets, and connection state."
            ),
            "repair": (
                "Do not flatten it into one instant hop. DNS, routing, TCP setup, HTTP work, "
                "response packets, and connection reuse or teardown all affect the path."
            ),
        },
        {
            "id": "mental_model.scenario_recap",
            "title": "Narrate the browser path",
            "prompt": (
                "In one or two sentences, trace the simple browser request from URL entry "
                "to HTTP response, and name one place latency can appear."
            ),
            "options": [],
            "expected_keyword_groups": [
                ["browser", "client", "url"],
                ["dns", "domain", "name"],
                ["ip", "route", "routing"],
                ["tcp", "handshake", "connection"],
                ["http", "response", "get"],
                ["latency", "setup", "teardown", "reuse", "packet"],
            ],
            "required_keyword_groups": 5,
            "expected_keywords": ["browser", "dns", "ip", "tcp", "http", "latency"],
            "rationale": (
                "Right: a strong answer follows the request path and notices that lookup, "
                "connection setup, routing, or extra packets can affect latency."
            ),
            "repair": (
                "Use this shape: browser URL -> DNS address lookup -> IP routing -> TCP "
                "connection -> HTTP request and response -> connection close or reuse. "
                "Then name lookup, setup, distance, or packets as a latency source."
            ),
        },
    ],
    "networking.layers": [
        {
            "id": "layers.sequence",
            "title": "Order the path",
            "prompt": "Which sequence best matches a basic browser request?",
            "options": [
                {"id": "a", "label": "DNS resolves, transport connects, HTTP sends the request"},
                {"id": "b", "label": "Database writes, then DNS resolves, then UI paints"},
                {"id": "c", "label": "Cache evicts, then login starts, then IP routes"},
            ],
            "correct_option_id": "a",
            "expected_keywords": ["dns", "tcp", "transport", "http"],
            "rationale": (
                "Right: DNS finds the address, the transport layer carries bytes with a "
                "specific reliability model, and HTTP expresses the application request."
            ),
            "repair": (
                "Keep the interview version simple: DNS finds the destination, IP routes "
                "packets, TCP or UDP defines delivery behavior, and HTTP carries app intent."
            ),
        },
        {
            "id": "layers.ip",
            "title": "Use the layer for the right job",
            "prompt": "What is the interview-level job of IP?",
            "options": [
                {"id": "a", "label": "Address and route packets across networks"},
                {"id": "b", "label": "Define REST endpoint names"},
                {"id": "c", "label": "Guarantee every request is retried safely"},
            ],
            "correct_option_id": "a",
            "expected_keywords": ["route", "address", "packet", "network"],
            "rationale": (
                "Right: IP is the addressing and routing layer. It helps packets move "
                "toward the destination, but it is not your API contract."
            ),
            "repair": (
                "Do not overload one layer. IP gets packets routed; transport handles "
                "delivery behavior; HTTP or another app protocol carries product intent."
            ),
        },
        {
            "id": "layers.http",
            "title": "Separate transport from intent",
            "prompt": "What does HTTP add on top of lower network layers?",
            "options": [
                {"id": "a", "label": "Methods, paths, headers, bodies, and status codes"},
                {"id": "b", "label": "Physical cables and radio signals"},
                {"id": "c", "label": "B-tree storage on disk"},
            ],
            "correct_option_id": "a",
            "expected_keywords": ["method", "path", "header", "status", "body"],
            "rationale": (
                "Right: HTTP is where the application says what it wants: GET this "
                "resource, POST this command, here is the response status."
            ),
            "repair": (
                "Transport answers how bytes move. HTTP answers what the client is asking "
                "the service to do."
            ),
        },
        {
            "id": "layers.dns_ip_boundary",
            "title": "Reach the right boundary",
            "prompt": "What is DNS doing before packets can be routed with IP?",
            "options": [
                {"id": "a", "label": "Mapping a human-readable name to a reachable address or endpoint"},
                {"id": "b", "label": "Choosing SQL indexes for a user table"},
                {"id": "c", "label": "Guaranteeing every POST is idempotent"},
            ],
            "correct_option_id": "a",
            "expected_keywords": ["dns", "domain", "address", "endpoint", "ip"],
            "rationale": (
                "Right: DNS gives the client a destination. IP then helps route packets "
                "toward that destination."
            ),
            "repair": (
                "Keep the jobs separate: DNS answers where the name points; IP routes packets; "
                "transport and HTTP handle the connection behavior and application request."
            ),
        },
        {
            "id": "layers.public_ip",
            "title": "Public routes matter",
            "prompt": "Why should you distinguish private IPs from public, routable IPs?",
            "options": [
                {"id": "a", "label": "Private addresses can work inside your network, but internet traffic needs routable public addresses"},
                {"id": "b", "label": "Private addresses make HTTP methods unnecessary"},
                {"id": "c", "label": "Public IPs guarantee TCP never retransmits"},
            ],
            "correct_option_id": "a",
            "expected_keywords": ["private", "public", "routable", "internet", "ip"],
            "rationale": (
                "Right: inside a private network, addresses mean what your network says "
                "they mean. For public internet traffic, routing infrastructure has to know "
                "where that public address lives."
            ),
            "repair": (
                "The interview-level version is simple: IP handles addressing and routing. "
                "Private IPs can be useful inside your system, but public traffic needs a "
                "publicly routable address or an entry point that has one."
            ),
        },
    ],
    "networking.tcp_udp": [
        {
            "id": "tcp_udp.default",
            "title": "Pick the safe default",
            "prompt": "For a normal web API where correctness and security matter, what is the baseline?",
            "options": [
                {"id": "a", "label": "HTTPS over reliable transport, usually TCP/TLS"},
                {"id": "b", "label": "UDP because every request must be fastest"},
                {"id": "c", "label": "No transport protocol is needed"},
            ],
            "correct_option_id": "a",
            "expected_keywords": ["tcp", "tls", "https", "reliable", "ordered"],
            "rationale": (
                "Right: most web APIs start with HTTPS because correctness, ordered delivery, "
                "and encryption are usually more important than shaving every millisecond."
            ),
            "repair": (
                "Default to the boring reliable and encrypted option first. Only move away from it "
                "when the product can tolerate loss or implements recovery elsewhere."
            ),
        },
        {
            "id": "tcp_udp.udp_fit",
            "title": "Spot the exception",
            "prompt": "Which product is the best UDP-style fit?",
            "options": [
                {"id": "a", "label": "Live voice or game state where stale packets are worse than lost packets"},
                {"id": "b", "label": "A payment charge request"},
                {"id": "c", "label": "A password reset update"},
            ],
            "correct_option_id": "a",
            "expected_keywords": ["live", "voice", "game", "loss", "latency", "udp"],
            "rationale": (
                "Right: real-time media often prefers staying current over waiting for "
                "old packets to be retransmitted."
            ),
            "repair": (
                "UDP-style delivery is not just faster TCP. It means you accept loss, "
                "reordering, or app-level recovery because low latency matters more."
            ),
        },
        {
            "id": "tcp_udp.tradeoff",
            "title": "Say the trade-off",
            "prompt": "What trade-off are you making when you choose UDP-style delivery?",
            "options": [
                {"id": "a", "label": "Lower latency and overhead, but weaker delivery guarantees"},
                {"id": "b", "label": "Stronger transactions, but slower database indexes"},
                {"id": "c", "label": "More UI polish, but fewer API routes"},
            ],
            "correct_option_id": "a",
            "expected_keywords": ["latency", "overhead", "loss", "order", "guarantee"],
            "rationale": (
                "Right: the trade is speed and simplicity in the network path for more "
                "responsibility in the application."
            ),
            "repair": (
                "The sentence to practice: UDP can reduce latency, but packets may be lost "
                "or out of order, so the product or protocol must tolerate that."
            ),
        },
        {
            "id": "tcp_udp.quic_http3",
            "title": "Do not flatten QUIC into UDP",
            "prompt": "Why is it misleading to say HTTP/3 is just unreliable UDP?",
            "options": [
                {"id": "a", "label": "QUIC uses UDP underneath but adds reliability, encryption, streams, and faster setup"},
                {"id": "b", "label": "HTTP/3 means the database stops needing replication"},
                {"id": "c", "label": "UDP automatically gives exactly-once delivery"},
            ],
            "correct_option_id": "a",
            "expected_keywords": ["quic", "udp", "reliable", "tls", "stream", "http/3"],
            "rationale": (
                "Right: QUIC runs over UDP but builds a richer transport with encryption, "
                "multiplexed streams, and connection setup improvements."
            ),
            "repair": (
                "Say QUIC carefully: it uses UDP as the substrate, then adds the transport "
                "features HTTP/3 needs instead of exposing raw lossy UDP to the app."
            ),
        },
    ],
    "networking.protocol_choice": [
        {
            "id": "protocol_choice.default",
            "title": "Choose the shape",
            "prompt": "Which protocol shape is the safest default for public request-response APIs?",
            "options": [
                {"id": "a", "label": "HTTP/REST"},
                {"id": "b", "label": "WebRTC"},
                {"id": "c", "label": "Raw database sockets from the browser"},
            ],
            "correct_option_id": "a",
            "expected_keywords": ["http", "rest", "request", "response", "api"],
            "rationale": (
                "Right: public web APIs usually start with HTTP/REST because it is familiar, "
                "debuggable, and broadly supported."
            ),
            "repair": (
                "Use the interaction pattern. Normal request-response APIs default to HTTP/REST; "
                "you need a reason to pick something more specialized."
            ),
        },
        {
            "id": "protocol_choice.websocket",
            "title": "Live updates",
            "prompt": "Which protocol family best fits a live chat channel after the user connects?",
            "options": [
                {"id": "a", "label": "WebSocket for a long-lived two-way channel"},
                {"id": "b", "label": "One HTTP request per hour"},
                {"id": "c", "label": "Only DNS records"},
            ],
            "correct_option_id": "a",
            "expected_keywords": ["websocket", "long", "bidirectional", "chat", "push"],
            "rationale": (
                "Right: WebSocket keeps a connection open so either side can send updates "
                "without repeated request setup."
            ),
            "repair": (
                "Live chat is not just fetching a static resource. You usually want the server "
                "to push new messages through a persistent channel."
            ),
        },
        {
            "id": "protocol_choice.grpc",
            "title": "Internal services",
            "prompt": "When might gRPC be a better fit than plain REST?",
            "options": [
                {"id": "a", "label": "Typed internal service calls with efficient payloads or streaming"},
                {"id": "b", "label": "Changing button colors"},
                {"id": "c", "label": "Replacing all databases"},
            ],
            "correct_option_id": "a",
            "expected_keywords": ["grpc", "typed", "internal", "stream", "binary"],
            "rationale": (
                "Right: gRPC is often useful for internal services that value typed contracts, "
                "efficient serialization, and streaming."
            ),
            "repair": (
                "REST is easy to expose publicly. gRPC shines when controlled services need "
                "strong contracts and efficient service-to-service communication."
            ),
        },
        {
            "id": "protocol_choice.graphql_resolvers",
            "title": "Flexible reads have a cost",
            "prompt": "What risk should you mention when choosing GraphQL for flexible client reads?",
            "options": [
                {"id": "a", "label": "Resolver fan-out, authorization, and backend complexity can move behind one query"},
                {"id": "b", "label": "GraphQL removes all need for caching"},
                {"id": "c", "label": "GraphQL is only useful for packet routing"},
            ],
            "correct_option_id": "a",
            "expected_keywords": ["graphql", "resolver", "fan", "complex", "authorization", "cache"],
            "rationale": (
                "Right: GraphQL can reduce client under-fetching or over-fetching, but "
                "the backend still has to control resolver cost, authorization, and caching."
            ),
            "repair": (
                "Do not sell GraphQL as free flexibility. Say where query complexity, "
                "resolver fan-out, auth checks, and caching will be controlled."
            ),
        },
        {
            "id": "protocol_choice.sse_one_way",
            "title": "One-way server push",
            "prompt": "When is SSE a cleaner fit than WebSocket?",
            "options": [
                {"id": "a", "label": "Server-to-client updates like notifications where the client mostly listens"},
                {"id": "b", "label": "Peer-to-peer video with NAT traversal"},
                {"id": "c", "label": "A database transaction log read by SQL only"},
            ],
            "correct_option_id": "a",
            "expected_keywords": ["sse", "server", "push", "one-way", "notification", "reconnect"],
            "rationale": (
                "Right: SSE keeps an HTTP-based stream for server push, with simpler "
                "semantics than a fully bidirectional channel."
            ),
            "repair": (
                "Use SSE when the server pushes events and the browser mainly listens. "
                "Use WebSocket when both sides need a long-lived interactive channel."
            ),
        },
        {
            "id": "protocol_choice.websocket_infra",
            "title": "Stateful channel cost",
            "prompt": "What infrastructure cost should you mention with WebSockets?",
            "options": [
                {"id": "a", "label": "Long-lived stateful connections affect load balancing, fanout, and failover"},
                {"id": "b", "label": "They remove all server memory usage"},
                {"id": "c", "label": "They make health checks unnecessary"},
            ],
            "correct_option_id": "a",
            "expected_keywords": ["websocket", "long", "stateful", "load", "fanout", "failover"],
            "rationale": (
                "Right: WebSockets are powerful, but persistent connections change routing, "
                "capacity planning, deploys, and failure behavior."
            ),
            "repair": (
                "A good WebSocket answer includes connection management: which server holds "
                "the socket, how messages fan out, and what happens when that server dies."
            ),
        },
        {
            "id": "protocol_choice.webrtc_nat",
            "title": "Peer-to-peer is not magic",
            "prompt": "What must you mention before choosing WebRTC for realtime media?",
            "options": [
                {"id": "a", "label": "Signaling plus STUN/TURN for NAT traversal and fallback"},
                {"id": "b", "label": "Only a REST endpoint named /video"},
                {"id": "c", "label": "A sticky SQL primary"},
            ],
            "correct_option_id": "a",
            "expected_keywords": ["webrtc", "signaling", "stun", "turn", "nat", "fallback"],
            "rationale": (
                "Right: WebRTC can create a peer media path, but the system still needs "
                "signaling and traversal/fallback plans."
            ),
            "repair": (
                "Use WebRTC for peer media or data channels only when you can explain "
                "signaling, STUN/TURN, fallback, and the operational complexity."
            ),
        },
        {
            "id": "protocol_choice.scenario_mix",
            "title": "Mix protocols by interaction",
            "prompt": (
                "For a collaborative dashboard with initial page load, server alerts, "
                "two-way chat, and an optional video call, name a reasonable protocol choice for each."
            ),
            "options": [],
            "expected_keyword_groups": [
                ["rest", "http", "request"],
                ["sse", "server-sent", "notification", "alert"],
                ["websocket", "chat", "bidirectional"],
                ["webrtc", "video", "media"],
            ],
            "required_keyword_groups": 3,
            "expected_keywords": ["rest", "sse", "websocket", "webrtc"],
            "rationale": (
                "Right: strong protocol answers map each interaction shape to a protocol "
                "instead of forcing one protocol onto the whole product."
            ),
            "repair": (
                "Start with HTTP/REST for initial request-response, SSE for one-way alerts, "
                "WebSocket for two-way chat, and WebRTC only for the media call."
            ),
        },
    ],
    "networking.http_api": [
        {
            "id": "http_api.shape",
            "title": "Name the API surface",
            "prompt": "What does HTTP give you for describing a web API operation?",
            "options": [
                {"id": "a", "label": "Method, path, headers, body, and status code"},
                {"id": "b", "label": "Only TCP retransmission settings"},
                {"id": "c", "label": "Only database table names"},
            ],
            "correct_option_id": "a",
            "expected_keywords": ["method", "path", "header", "body", "status"],
            "rationale": (
                "Right: HTTP gives a common shape for request-response APIs, so interviewers "
                "can quickly understand what operation the client is calling."
            ),
            "repair": (
                "For API design, say the method, path, input body if any, response shape, "
                "and likely status codes."
            ),
        },
        {
            "id": "http_api.stateless",
            "title": "Connect it to scaling",
            "prompt": "Why is stateless HTTP useful behind a load balancer?",
            "options": [
                {"id": "a", "label": "Any healthy replica can handle the next request"},
                {"id": "b", "label": "It removes all need for authentication"},
                {"id": "c", "label": "It guarantees the database is consistent"},
            ],
            "correct_option_id": "a",
            "expected_keywords": ["stateless", "replica", "load", "balancer", "server"],
            "rationale": (
                "Right: if the server does not keep per-user session state in memory, "
                "a load balancer has more freedom to route requests to healthy replicas."
            ),
            "repair": (
                "Stateless does not mean no state exists. It means each request carries "
                "enough context for any service replica to process it."
            ),
        },
        {
            "id": "http_api.rest",
            "title": "Read the endpoint",
            "prompt": "What does GET /users/{id} usually mean?",
            "options": [
                {"id": "a", "label": "Read one user resource"},
                {"id": "b", "label": "Create a new user every time"},
                {"id": "c", "label": "Open a WebRTC audio stream"},
            ],
            "correct_option_id": "a",
            "expected_keywords": ["get", "read", "user", "resource"],
            "rationale": (
                "Right: GET is the read operation in the common REST mental model, and "
                "the path identifies the resource."
            ),
            "repair": (
                "A clean REST-ish answer is easy to scan: method says action, path says "
                "resource, body carries input for writes, status code reports the result."
            ),
        },
        {
            "id": "http_api.https_tls_boundary",
            "title": "Security boundary",
            "prompt": "What does HTTPS give you, and what does it not give you by itself?",
            "options": [
                {"id": "a", "label": "Encrypted transport and server authentication, not business-level request validity"},
                {"id": "b", "label": "Automatic authorization for every user action"},
                {"id": "c", "label": "Guaranteed idempotency for all POST requests"},
            ],
            "correct_option_id": "a",
            "expected_keywords": ["https", "tls", "encrypt", "authentic", "validate", "authorization"],
            "rationale": (
                "Right: TLS protects the transport, but the application still validates "
                "identity, authorization, input, and business rules."
            ),
            "repair": (
                "Phrase it cleanly: HTTPS protects data in transit and helps authenticate "
                "the server. Your app still has to validate who can do what."
            ),
        },
    ],
    "networking.latency": [
        {
            "id": "latency.budget",
            "title": "Budget the path",
            "prompt": "What is a latency budget for?",
            "options": [
                {"id": "a", "label": "Deciding where request time is allowed to go"},
                {"id": "b", "label": "Choosing table names"},
                {"id": "c", "label": "Skipping monitoring"},
            ],
            "correct_option_id": "a",
            "expected_keywords": ["budget", "time", "request", "latency", "path"],
            "rationale": (
                "Right: a budget lets you reason about DNS, connection setup, network distance, "
                "service work, dependency calls, and queueing."
            ),
            "repair": (
                "Do not say only 'make it fast'. Split the request path into time buckets and "
                "decide which bucket is too large."
            ),
        },
        {
            "id": "latency.tail",
            "title": "Use tail latency",
            "prompt": "Why do interviewers care about p95 or p99 latency?",
            "options": [
                {"id": "a", "label": "It reveals the slow user experiences hidden by averages"},
                {"id": "b", "label": "It proves the database has no data"},
                {"id": "c", "label": "It replaces authentication"},
            ],
            "correct_option_id": "a",
            "expected_keywords": ["p95", "p99", "tail", "average", "slow"],
            "rationale": (
                "Right: average latency can look fine while a meaningful slice of users waits "
                "too long."
            ),
            "repair": (
                "Use p95 or p99 when you care about the painful edge cases users actually feel."
            ),
        },
        {
            "id": "latency.reduction",
            "title": "Pick the right lever",
            "prompt": "Which change most directly reduces distance and repeated origin work for static assets?",
            "options": [
                {"id": "a", "label": "CDN caching near users"},
                {"id": "b", "label": "More retry loops"},
                {"id": "c", "label": "Longer table names"},
            ],
            "correct_option_id": "a",
            "expected_keywords": ["cdn", "cache", "near", "edge", "distance"],
            "rationale": (
                "Right: CDNs move cached content closer to users and remove repeated trips to origin."
            ),
            "repair": (
                "Match the lever to the bottleneck. CDNs help distance and repeated static reads; "
                "connection pooling helps setup overhead; database indexes help query work."
            ),
        },
        {
            "id": "latency.regionalization_tradeoff",
            "title": "Regions are a trade-off",
            "prompt": "What trade-off comes with putting users and services in multiple regions?",
            "options": [
                {"id": "a", "label": "Lower user distance, but harder data locality, consistency, and failover"},
                {"id": "b", "label": "All data becomes instantly consistent everywhere for free"},
                {"id": "c", "label": "Health checks are no longer needed"},
            ],
            "correct_option_id": "a",
            "expected_keywords": ["region", "latency", "data", "consistency", "failover"],
            "rationale": (
                "Right: regionalization can reduce round-trip distance, but it introduces "
                "data placement, replication, routing, and failover decisions."
            ),
            "repair": (
                "Do not add regions as decoration. Say which users go where, what data is local, "
                "what is replicated, and what happens during regional failure."
            ),
        },
        {
            "id": "latency.connection_setup",
            "title": "Setup overhead",
            "prompt": "Which lever helps when repeated connection setup is a meaningful part of latency?",
            "options": [
                {"id": "a", "label": "Connection reuse, pooling, keep-alive, or a lower-setup transport"},
                {"id": "b", "label": "Infinite retries"},
                {"id": "c", "label": "Changing every endpoint to POST"},
            ],
            "correct_option_id": "a",
            "expected_keywords": ["connection", "reuse", "pool", "keep-alive", "setup", "quic"],
            "rationale": (
                "Right: setup overhead is different from service work. Reusing connections "
                "or choosing a transport with faster setup can reduce that bucket."
            ),
            "repair": (
                "Use the latency budget: if setup is expensive, look at keep-alive, pooling, "
                "connection reuse, or a protocol with faster setup."
            ),
        },
    ],
    "networking.load_balancing": [
        {
            "id": "load_balancing.job",
            "title": "Route to capacity",
            "prompt": "What is the core job of a load balancer?",
            "options": [
                {"id": "a", "label": "Route traffic to healthy backend capacity"},
                {"id": "b", "label": "Store every user record"},
                {"id": "c", "label": "Encrypt passwords by itself"},
            ],
            "correct_option_id": "a",
            "expected_keywords": ["route", "traffic", "healthy", "backend", "capacity"],
            "rationale": (
                "Right: the load balancer sits on the request path and chooses eligible backends."
            ),
            "repair": (
                "Say it plainly: it routes incoming requests across healthy replicas, using a policy "
                "and health checks."
            ),
        },
        {
            "id": "load_balancing.health",
            "title": "Avoid dead replicas",
            "prompt": "Why do load balancers need health checks?",
            "options": [
                {"id": "a", "label": "To stop sending traffic to unhealthy instances"},
                {"id": "b", "label": "To make every query faster"},
                {"id": "c", "label": "To remove all retries"},
            ],
            "correct_option_id": "a",
            "expected_keywords": ["health", "unhealthy", "traffic", "instance", "fail"],
            "rationale": (
                "Right: health checks decide which instances should receive new requests."
            ),
            "repair": (
                "Without health checks, a load balancer can keep sending users to broken capacity."
            ),
        },
        {
            "id": "load_balancing.sticky",
            "title": "Spot sticky-session risk",
            "prompt": "What is the downside of sticky sessions?",
            "options": [
                {"id": "a", "label": "They make failover and scaling harder"},
                {"id": "b", "label": "They guarantee zero latency"},
                {"id": "c", "label": "They replace all caches"},
            ],
            "correct_option_id": "a",
            "expected_keywords": ["sticky", "session", "failover", "scale", "hard"],
            "rationale": (
                "Right: sticky sessions tie a user to a backend, which reduces routing freedom."
            ),
            "repair": (
                "Prefer stateless services when possible. Sticky sessions can be necessary, but "
                "they make replacement, failover, and load spreading harder."
            ),
        },
        {
            "id": "load_balancing.l4_l7",
            "title": "Choose the layer",
            "prompt": "What is the practical difference between L4 and L7 load balancing?",
            "options": [
                {"id": "a", "label": "L4 routes with transport-level data; L7 can use HTTP-level data like path or headers"},
                {"id": "b", "label": "L4 is for databases only and L7 is for CSS only"},
                {"id": "c", "label": "L7 means health checks are impossible"},
            ],
            "correct_option_id": "a",
            "expected_keywords": ["l4", "l7", "transport", "http", "path", "header"],
            "rationale": (
                "Right: L4 routing is lower-level and cheaper to reason about; L7 routing "
                "can make application-aware decisions."
            ),
            "repair": (
                "Use L4 when transport-level routing is enough. Use L7 when path, host, "
                "headers, cookies, or application behavior should influence routing."
            ),
        },
        {
            "id": "load_balancing.client_side_dns",
            "title": "Routing can move outward",
            "prompt": "What extra concern appears with DNS-based or client-side load balancing?",
            "options": [
                {"id": "a", "label": "Clients or resolvers can keep stale choices because of TTLs and cached endpoints"},
                {"id": "b", "label": "The database automatically shards itself"},
                {"id": "c", "label": "Every request becomes exactly once"},
            ],
            "correct_option_id": "a",
            "expected_keywords": ["client-side", "dns", "ttl", "cache", "stale", "endpoint"],
            "rationale": (
                "Right: DNS and client-side balancing can reduce central routing pressure, "
                "but stale endpoint choices and discovery health become part of the design."
            ),
            "repair": (
                "Mention endpoint discovery, health, TTLs, and what a client does when its "
                "chosen backend becomes unhealthy."
            ),
        },
        {
            "id": "load_balancing.algorithm_fit",
            "title": "Policy matters",
            "prompt": "Why might least-connections beat simple round robin for some services?",
            "options": [
                {"id": "a", "label": "Requests may have uneven duration, so active load matters more than count"},
                {"id": "b", "label": "It removes all tail latency automatically"},
                {"id": "c", "label": "It makes every backend stateful"},
            ],
            "correct_option_id": "a",
            "expected_keywords": ["least", "connection", "round robin", "duration", "active", "load"],
            "rationale": (
                "Right: if requests differ in length or connection count, policy affects "
                "hot spots and fairness."
            ),
            "repair": (
                "Round robin is simple; least-connections can be better when active work "
                "varies. Weighted policies help when replicas have different capacity."
            ),
        },
    ],
    "networking.failures": [
        {
            "id": "failures.timeout",
            "title": "Stop waiting deliberately",
            "prompt": "What is the job of a timeout?",
            "options": [
                {"id": "a", "label": "Stop waiting after a budget so the caller can recover"},
                {"id": "b", "label": "Make the remote service faster"},
                {"id": "c", "label": "Prevent all duplicate requests automatically"},
            ],
            "correct_option_id": "a",
            "expected_keywords": ["stop", "waiting", "budget", "recover", "timeout"],
            "rationale": (
                "Right: a timeout is a boundary. It prevents one slow dependency from "
                "holding the caller forever."
            ),
            "repair": (
                "Timeouts do not fix the remote service. They let your caller choose a "
                "fallback, retry policy, or user-facing error after a bounded wait."
            ),
        },
        {
            "id": "failures.retry",
            "title": "Retry without causing harm",
            "prompt": "What should come with retries in a healthy design?",
            "options": [
                {"id": "a", "label": "Backoff, limits, and a retry budget"},
                {"id": "b", "label": "Infinite retry loops"},
                {"id": "c", "label": "More database columns only"},
            ],
            "correct_option_id": "a",
            "expected_keywords": ["backoff", "limit", "budget", "retry"],
            "rationale": (
                "Right: retries can help transient failures, but uncontrolled retries can "
                "amplify outages."
            ),
            "repair": (
                "Mention retry backoff and a cap. Otherwise, thousands of clients can all "
                "retry at once and turn a small incident into a retry storm."
            ),
        },
        {
            "id": "failures.idempotency",
            "title": "Protect side effects",
            "prompt": "What must you add before safely retrying a payment charge?",
            "options": [
                {"id": "a", "label": "An idempotency key for the logical operation"},
                {"id": "b", "label": "A faster retry interval only"},
                {"id": "c", "label": "UDP between the API and database"},
            ],
            "correct_option_id": "a",
            "expected_keywords": ["idempot", "key", "duplicate", "payment", "retry"],
            "rationale": (
                "Right: idempotency lets repeated attempts map to the same logical charge, "
                "which protects the user from duplicate side effects."
            ),
            "repair": (
                "For operations that must happen once, retries need duplicate protection. "
                "The standard interview phrase is: use an idempotency key."
            ),
        },
        {
            "id": "failures.jitter_storm",
            "title": "Avoid retry storms",
            "prompt": "Why add jitter to retry backoff?",
            "options": [
                {"id": "a", "label": "To spread retries out so clients do not stampede together"},
                {"id": "b", "label": "To make every request skip authentication"},
                {"id": "c", "label": "To guarantee the dependency is healthy"},
            ],
            "correct_option_id": "a",
            "expected_keywords": ["jitter", "backoff", "spread", "retry", "storm", "stampede"],
            "rationale": (
                "Right: jitter avoids synchronized retry waves that can overload a recovering service."
            ),
            "repair": (
                "Backoff slows retries; jitter spreads them out. Together they reduce the "
                "chance that all callers hammer the dependency at the same moment."
            ),
        },
        {
            "id": "failures.circuit_breaker",
            "title": "Stop feeding a failing dependency",
            "prompt": "What does a circuit breaker do in a distributed system?",
            "options": [
                {"id": "a", "label": "Temporarily stops calls to a failing dependency and lets it recover"},
                {"id": "b", "label": "Retries every request forever"},
                {"id": "c", "label": "Turns UDP into exactly-once delivery"},
            ],
            "correct_option_id": "a",
            "expected_keywords": ["circuit", "breaker", "dependency", "fail", "recover", "open"],
            "rationale": (
                "Right: a circuit breaker opens when failures cross a threshold, fails fast, "
                "and later probes recovery instead of flooding the dependency."
            ),
            "repair": (
                "Use the standard shape: closed while healthy, open to fail fast when errors spike, "
                "half-open to test whether the dependency has recovered."
            ),
        },
        {
            "id": "failures.scenario_policy",
            "title": "Design the recovery policy",
            "prompt": (
                "A checkout call to payments times out during a spike. Give a safe recovery "
                "policy that avoids duplicate charges and avoids a retry storm."
            ),
            "options": [],
            "expected_keyword_groups": [
                ["timeout", "deadline", "budget"],
                ["retry", "backoff", "jitter", "limit"],
                ["idempotency", "idempotent", "duplicate", "key"],
                ["circuit", "breaker", "fail fast"],
            ],
            "required_keyword_groups": 3,
            "expected_keywords": ["timeout", "retry", "backoff", "jitter", "idempotency", "circuit"],
            "rationale": (
                "Right: strong failure policy combines bounded waiting, careful retries, "
                "duplicate protection, and circuit breaking when the dependency is unhealthy."
            ),
            "repair": (
                "Say: set a timeout, retry only within a budget using exponential backoff "
                "and jitter, require an idempotency key for the charge, and open a circuit "
                "breaker if payments keeps failing."
            ),
        },
    ],
}


_LAYER_QUIZ = NETWORKING_QUIZ["networking.layers"]
NETWORKING_QUIZ["networking.layers"] = [
    question for question in _LAYER_QUIZ
    if question["id"] in {"layers.sequence", "layers.http", "layers.dns_ip_boundary"}
]
NETWORKING_QUIZ["networking.network_layer"] = [
    question for question in _LAYER_QUIZ
    if question["id"] in {"layers.ip", "layers.public_ip"}
] + [
    {
        "id": "network_layer.private_boundary",
        "title": "Keep internals private",
        "prompt": "Which design keeps internal services off the public internet?",
        "options": [
            {"id": "a", "label": "Expose an edge or gateway publicly, keep app services on private addresses"},
            {"id": "b", "label": "Give every database shard its own public browser endpoint"},
            {"id": "c", "label": "Put user IDs in the DNS record"},
        ],
        "correct_option_id": "a",
        "expected_keywords": ["private", "public", "edge", "gateway", "service"],
        "rationale": (
            "Right: public reachability usually belongs at a small set of entry points; "
            "internal services can stay private behind that boundary."
        ),
        "repair": (
            "Expose the entry point the user needs, then keep backend services on private "
            "addresses unless there is a clear reason to make them public."
        ),
    },
]

_PROTOCOL_CHOICE_QUIZ = NETWORKING_QUIZ["networking.protocol_choice"]
NETWORKING_QUIZ["networking.protocol_choice"] = [
    question for question in _PROTOCOL_CHOICE_QUIZ
    if question["id"] in {
        "protocol_choice.default",
        "protocol_choice.grpc",
        "protocol_choice.graphql_resolvers",
    }
]
NETWORKING_QUIZ["networking.realtime_protocols"] = [
    question for question in _PROTOCOL_CHOICE_QUIZ
    if question["id"] in {
        "protocol_choice.websocket",
        "protocol_choice.sse_one_way",
        "protocol_choice.websocket_infra",
        "protocol_choice.scenario_mix",
    }
] + [
    {
        "id": "realtime.sse_reconnect",
        "title": "Reconnect the stream",
        "prompt": "What practical detail makes SSE more than just one long response?",
        "options": [
            {"id": "a", "label": "EventSource can reconnect and resume from the last received event ID"},
            {"id": "b", "label": "SSE automatically creates peer-to-peer media paths"},
            {"id": "c", "label": "SSE removes all load balancers from the path"},
        ],
        "correct_option_id": "a",
        "expected_keywords": ["sse", "reconnect", "eventsource", "last", "id"],
        "rationale": (
            "Right: SSE streams can close, so reconnect behavior and missed-message replay "
            "are part of the practical design."
        ),
        "repair": (
            "Mention that SSE is an HTTP stream with reconnect semantics. The server may need "
            "to remember recent events so a reconnecting client can catch up."
        ),
    },
]
NETWORKING_QUIZ["networking.webrtc"] = [
    question for question in _PROTOCOL_CHOICE_QUIZ
    if question["id"] == "protocol_choice.webrtc_nat"
] + [
    {
        "id": "webrtc.fit",
        "title": "Use it narrowly",
        "prompt": "Which interview scenario is the strongest WebRTC fit?",
        "options": [
            {"id": "a", "label": "Browser audio/video call with peer media streams"},
            {"id": "b", "label": "A normal read-only profile API"},
            {"id": "c", "label": "A daily batch analytics export"},
        ],
        "correct_option_id": "a",
        "expected_keywords": ["webrtc", "video", "audio", "peer", "media"],
        "rationale": (
            "Right: WebRTC is strongest for audio/video calling and conferencing, where "
            "a peer media path is worth the extra complexity."
        ),
        "repair": (
            "Keep WebRTC narrow in interviews. Use it for audio/video or peer-heavy data paths, "
            "and remember signaling plus STUN/TURN."
        ),
    },
]

_LOAD_BALANCING_QUIZ = NETWORKING_QUIZ["networking.load_balancing"]
NETWORKING_QUIZ["networking.load_balancing"] = [
    question for question in _LOAD_BALANCING_QUIZ
    if question["id"] in {"load_balancing.job", "load_balancing.health"}
]
NETWORKING_QUIZ["networking.lb_client_side"] = [
    question for question in _LOAD_BALANCING_QUIZ
    if question["id"] == "load_balancing.client_side_dns"
] + [
    {
        "id": "lb_client_side.registry",
        "title": "Who owns discovery?",
        "prompt": "When is client-side load balancing especially reasonable?",
        "options": [
            {"id": "a", "label": "Internal clients you control can keep a fresh server list or shard map"},
            {"id": "b", "label": "Anonymous browsers need instant failover with no caching"},
            {"id": "c", "label": "The backend has no health information"},
        ],
        "correct_option_id": "a",
        "expected_keywords": ["client-side", "registry", "internal", "server list", "shard"],
        "rationale": (
            "Right: client-side balancing works best when clients are controlled and can "
            "receive fresh discovery or shard information."
        ),
        "repair": (
            "Tie client-side balancing to controlled clients and fresh discovery. DNS is useful "
            "too, but cached TTLs make updates slower."
        ),
    },
]
NETWORKING_QUIZ["networking.lb_dedicated"] = [
    question for question in _LOAD_BALANCING_QUIZ
    if question["id"] in {
        "load_balancing.sticky",
        "load_balancing.l4_l7",
        "load_balancing.algorithm_fit",
    }
] + [
    {
        "id": "lb_dedicated.websocket_l4",
        "title": "Persistent connections",
        "prompt": "Why are L4 load balancers often easier to justify for WebSocket-heavy traffic?",
        "options": [
            {"id": "a", "label": "After upgrade, the connection is persistent and transport-like"},
            {"id": "b", "label": "WebSocket messages can be freely rebalanced midstream"},
            {"id": "c", "label": "L4 understands every JSON message body"},
        ],
        "correct_option_id": "a",
        "expected_keywords": ["l4", "websocket", "persistent", "connection", "upgrade"],
        "rationale": (
            "Right: after the HTTP upgrade, a WebSocket behaves like a persistent connection; "
            "you generally balance when the connection is established."
        ),
        "repair": (
            "For WebSockets, explain where the connection lands, how long it lives, and how "
            "new connections are spread across healthy backends."
        ),
    },
]


@lru_cache(maxsize=8)
def _compiled_networking_units() -> tuple[LearningUnit, ...]:
    editorial_units = [
        EditorialUnit(
            id=unit.id,
            source_path=HELLOINTERVIEW_NETWORKING_KB_PATH,
            source_sections=NETWORKING_UNIT_SOURCE_SECTIONS.get(unit.id, []),
            title=unit.title,
            objective=unit.objective,
            body=unit.body,
            example=unit.example,
            coach_script=unit.coach_script,
            key_points=unit.key_points,
            check_prompt=unit.check_prompt,
            options=unit.options,
            correct_option_id=unit.correct_option_id,
            expected_keywords=unit.expected_keywords,
            repair=unit.repair,
            flash_body=_flash_body(unit),
            quizzes=NETWORKING_QUIZ.get(unit.id, []),
        )
        for unit in NETWORKING_UNITS
    ]
    compiled_units = compile_editorial_units(
        editorial_units,
        kb_root=PROJECT_ROOT,
        project_root=PROJECT_ROOT,
        source_label="HelloInterview",
    )
    return tuple(
        LearningUnit(
            id=unit.id,
            title=unit.title,
            objective=unit.objective,
            body=unit.body,
            example=unit.example,
            coach_script=unit.coach_script,
            key_points=unit.key_points,
            check_prompt=unit.check_prompt,
            options=unit.options,
            correct_option_id=unit.correct_option_id,
            expected_keywords=unit.expected_keywords,
            repair=unit.repair,
            flash_body=unit.flash_body,
            source_path=unit.source_path,
            source_url=unit.source_url,
            source_sections=unit.source_sections,
            source_paragraphs=unit.source_paragraphs,
            draft=unit.draft,
            quizzes=unit.quizzes,
        )
        for unit in compiled_units
    )


def _networking_unit_blueprint(unit_id: str) -> dict[str, list[str]]:
    return deepcopy(NETWORKING_AGENTIC_BLUEPRINT.get(unit_id, {}))


def _networking_detail_points(unit: LearningUnit) -> list[str]:
    points: list[str] = []
    for point in unit.key_points:
        if point and point not in points:
            points.append(point)
    return points


def networking_coverage_summary() -> dict[str, Any]:
    """Return a deterministic coverage blueprint for networking cards and quizzes."""
    units = list(_compiled_networking_units())
    unit_summaries: list[dict[str, Any]] = []
    card_sections: set[str] = set()
    quiz_sections: set[str] = set()
    source_missing_sections: set[str] = set()
    section_quiz_index: dict[str, list[str]] = {
        section: [] for section in NETWORKING_COVERAGE_KEY_SECTIONS
    }

    for unit in units:
        sections = list(unit.source_sections)
        questions = _quiz_questions_for_unit(unit)
        quiz_ids = [question.get("id", "") for question in questions if question.get("id")]
        quiz_count = len(questions)
        blueprint = _networking_unit_blueprint(unit.id)
        has_card = bool(unit.body.strip() and unit.key_points)
        has_quiz = quiz_count > 0
        if has_card:
            card_sections.update(sections)
        if has_quiz:
            quiz_sections.update(sections)
            for section in sections:
                section_quiz_index.setdefault(section, []).extend(quiz_ids)
        source_missing_sections.update(unit.draft.get("missing_sections", []))
        unit_summaries.append({
            "id": unit.id,
            "title": unit.title,
            "sections": sections,
            "has_card": has_card,
            "quiz_count": quiz_count,
            "quiz_ids": quiz_ids,
            "knowledge_point_count": len(blueprint.get("card_points", [])),
            "quiz_dimensions": blueprint.get("quiz_dimensions", []),
            "dynamic_insert_rules": blueprint.get("dynamic_insert_rules", []),
            "paragraph_count": unit.draft.get("paragraph_count", 0),
            "missing_source_sections": list(unit.draft.get("missing_sections", [])),
        })

    key_sections = list(NETWORKING_COVERAGE_KEY_SECTIONS)
    return {
        "topic_id": "system_design.networking",
        "source_path": HELLOINTERVIEW_NETWORKING_KB_PATH,
        "source_url": HELLOINTERVIEW_NETWORKING_URL,
        "key_sections": key_sections,
        "interaction_model": (
            "Dialogue first: the coach chooses cards, quiz checks, repairs, and follow-up "
            "prompts from learner behavior instead of serving a fixed flashcard stack."
        ),
        "unit_count": len(units),
        "quiz_count": sum(len(_quiz_questions_for_unit(unit)) for unit in units),
        "units": unit_summaries,
        "agentic_blueprint": deepcopy(NETWORKING_AGENTIC_BLUEPRINT),
        "section_quiz_index": {
            section: list(dict.fromkeys(ids))
            for section, ids in section_quiz_index.items()
        },
        "covered_sections": {
            "cards": [section for section in key_sections if section in card_sections],
            "quizzes": [section for section in key_sections if section in quiz_sections],
        },
        "missing_sections": {
            "cards": [section for section in key_sections if section not in card_sections],
            "quizzes": [section for section in key_sections if section not in quiz_sections],
            "source": [section for section in key_sections if section in source_missing_sections],
        },
    }


def new_learning_state(topic_id: str, topic_name: str, source: str = "hellointerview") -> dict[str, Any]:
    units = _units_for_topic(topic_id, topic_name)
    return {
        "topic_id": topic_id,
        "topic_name": topic_name,
        "source": source or "hellointerview",
        "unit_index": 0,
        "phase": "teach",
        "attempts": 0,
        "quiz_index": 0,
        "quiz_correct": 0,
        "completed_units": [],
        "mastered_units": [],
        "units": [u.id for u in units],
    }


def initial_learning_frame(state: dict[str, Any]) -> dict[str, Any]:
    state["phase"] = "teach"
    return _teach_frame(state)


def handle_learning_step(
    state: dict[str, Any],
    *,
    action: str = "",
    user_text: str = "",
    option_id: str = "",
) -> dict[str, Any]:
    action = (action or "").strip()
    user_text = (user_text or "").strip()
    option_id = (option_id or "").strip()

    if action == "source_hellointerview":
        state["source"] = "hellointerview.networking_essentials"
        state["phase"] = "teach"
        return _teach_frame(state)
    if action == "restart":
        state["unit_index"] = 0
        state["phase"] = "teach"
        state["attempts"] = 0
        state["quiz_index"] = 0
        state["quiz_correct"] = 0
        return _teach_frame(state)

    if action in ("quiz", "read", "start_check"):
        state["quiz_index"] = 0
        state["quiz_correct"] = 0
        state["phase"] = "check"
        return _check_frame(state)

    if action == "retry":
        state["phase"] = "check"
        return _check_frame(state)

    if action == "next_question":
        unit = _current_unit(state)
        total = len(_quiz_questions_for_unit(unit))
        state["quiz_index"] = min(total - 1, int(state.get("quiz_index") or 0) + 1)
        state["phase"] = "check"
        return _check_frame(state)

    if action == "simpler":
        state["phase"] = "repair"
        return _repair_frame(state, "simpler")

    if action == "example":
        state["phase"] = "repair"
        return _repair_frame(state, "example")

    if action == "ask_card":
        state["phase"] = "repair"
        return _answer_question_frame(state, user_text or "Can you explain this card?")

    if action == "continue":
        _advance_unit(state)
        if _is_complete(state):
            state["phase"] = "complete"
            return _complete_frame(state)
        state["phase"] = "teach"
        return _teach_frame(state)

    if action == "answer_option":
        return _evaluate_frame(state, option_id=option_id)

    if action == "submit_answer" or user_text:
        if _looks_like_question(user_text):
            return _answer_question_frame(state, user_text)
        return _evaluate_frame(state, user_text=user_text)

    return _teach_frame(state)


def frame_coach_text(frame: dict[str, Any]) -> str:
    return frame.get("coach_text") or frame.get("spoken_script") or ""


def _units_for_topic(topic_id: str, topic_name: str) -> list[LearningUnit]:
    if topic_id == "system_design.networking":
        return list(_compiled_networking_units())
    if topic_id == "system_design.rate_limiting":
        return [
            LearningUnit(
                id=f"{topic_id}.llm_gateway",
                title="Rate limiting for an LLM gateway",
                objective="Connect classic rate limiting to tenant budgets, retry storms, and customer rollout.",
                body=(
                    "For an AI Engineer or FDE interview, rate limiting is not just about returning 429. "
                    "On an LLM gateway it protects tenant token budgets, controls model cost, prevents "
                    "retry storms, and gives customers predictable rollout behavior. Place it at the API "
                    "gateway or model gateway, decide which dimensions matter -- tenant, user, model, tokens, "
                    "and requests -- then explain the failure mode: bad retries can amplify load and spend."
                ),
                example=(
                    "A customer launches an internal assistant and traffic spikes. A weak answer limits only "
                    "requests per IP. A stronger FDE answer adds per-tenant token budgets, burst handling, "
                    "backoff guidance, dashboard visibility, and an escalation path for rollout exceptions."
                ),
                coach_script=(
                    "First bite: translate rate limiting from generic API protection into LLM gateway control. "
                    "Say tenant token budget, retry storm, cost guardrail, and customer rollout."
                ),
                key_points=[
                    "Budget: tokens per tenant",
                    "Placement: model/API gateway",
                    "Failure: retry storms raise cost",
                    "FDE: explain rollout safety",
                ],
                check_prompt="Explain rate limiting for an LLM gateway in one tight sentence.",
                options=[],
                correct_option_id="",
                expected_keywords=["tenant", "token", "gateway", "retry", "cost", "backoff", "quota"],
                repair=(
                    "Use this sentence frame: At the LLM gateway, rate limiting protects ___ by controlling ___, "
                    "and it must handle ___ with ___."
                ),
            )
        ]
    if topic_id == "ai_engineering.agent_tool_use":
        return [
            LearningUnit(
                id=f"{topic_id}.runtime",
                title="Agent tool use as a production workflow",
                objective="Explain tool calling with permissions, traces, failure handling, and evals.",
                body=(
                    "Agentic engineering is not 'give the model more tools.' A production agent needs a bounded "
                    "loop: plan, call a permitted tool with a schema, observe the result, decide the next step, "
                    "and leave a trace. Strong interview answers mention allowlists, budgets, human approval for "
                    "risky actions, tool error handling, and evals that catch regressions."
                ),
                example=(
                    "For a support agent that can refund users, do not let the model call anything freely. "
                    "Use scoped tools, approval thresholds, audit logs, and tests for wrong-customer or "
                    "duplicate-refund failures."
                ),
                coach_script=(
                    "First bite: talk about the agent as an observable workflow. Tool schema, permission, trace, "
                    "failure recovery, and evals are the core nouns."
                ),
                key_points=[
                    "Tools: schema and allowlist",
                    "Trace: plan/tool/observation",
                    "Guardrail: approval or budget",
                    "Eval: catch tool failures",
                ],
                check_prompt="Explain one guardrail for an agent that can call external tools.",
                options=[],
                correct_option_id="",
                expected_keywords=["allowlist", "permission", "approval", "trace", "budget", "eval", "sandbox"],
                repair=(
                    "Name the risky tool, the permission boundary, the trace you would log, and the eval that "
                    "would catch a bad call."
                ),
            )
        ]
    return [
        LearningUnit(
            id=f"{topic_id}.mental_model",
            title=f"{topic_name}: mental model",
            objective="Understand the responsibility, request-path position, and first trade-off.",
            body=(
                f"This first pass treats {topic_name} as one system design building "
                "block. The coach will ask what it is responsible for, where it sits "
                "in the request path, and what failure or trade-off it introduces."
            ),
            example=(
                "For any topic, place it in the path: client, edge, service, cache, "
                "database, queue, worker, or storage."
            ),
            coach_script=(
                f"First bite for {topic_name}: do not memorize a definition yet. "
                "Place it in the request path, name what it is responsible for, "
                "and name one trade-off."
            ),
            key_points=[
                "Responsibility: what job does it do?",
                "Placement: where does it sit in the system?",
                "Trade-off: what gets better and what gets harder?",
            ],
            check_prompt=f"Give one sentence: what is {topic_name} responsible for?",
            options=[],
            correct_option_id="",
            expected_keywords=[],
            repair=(
                "Use this sentence frame: It is responsible for ___, it sits near ___, "
                "and it trades ___ for ___."
            ),
        )
    ]


def _current_unit(state: dict[str, Any]) -> LearningUnit:
    units = _units_for_topic(state["topic_id"], state["topic_name"])
    index = max(0, min(int(state.get("unit_index") or 0), len(units) - 1))
    return units[index]


def _quiz_questions_for_unit(unit: LearningUnit) -> list[dict[str, Any]]:
    questions = unit.quizzes or NETWORKING_QUIZ.get(unit.id)
    if questions:
        return deepcopy(questions)
    return [
        {
            "id": f"{unit.id}.check",
            "title": "Mastery check",
            "prompt": unit.check_prompt,
            "options": deepcopy(unit.options),
            "correct_option_id": unit.correct_option_id,
            "expected_keywords": deepcopy(unit.expected_keywords),
            "rationale": _flash_body(unit),
            "repair": unit.repair,
        }
    ]


def _current_quiz_index(state: dict[str, Any], unit: LearningUnit) -> int:
    questions = _quiz_questions_for_unit(unit)
    return max(0, min(int(state.get("quiz_index") or 0), len(questions) - 1))


def _current_quiz_question(state: dict[str, Any], unit: LearningUnit) -> dict[str, Any]:
    questions = _quiz_questions_for_unit(unit)
    return questions[_current_quiz_index(state, unit)]


def _base_frame(state: dict[str, Any], kind: str) -> dict[str, Any]:
    units = _units_for_topic(state["topic_id"], state["topic_name"])
    unit = _current_unit(state)
    index = max(0, min(int(state.get("unit_index") or 0), len(units) - 1))
    source = _source_for_state(state)
    return {
        "version": 1,
        "kind": kind,
        "mode": "learn",
        "topic_id": state["topic_id"],
        "topic_name": state["topic_name"],
        "source": source,
        "unit": {
            "id": unit.id,
            "index": index + 1,
            "total": len(units),
            "title": unit.title,
            "objective": unit.objective,
            "estimated_read_seconds": 45,
        },
        "progress": {
            "unit_index": index + 1,
            "total_units": len(units),
            "completed_units": len(state.get("completed_units") or []),
            "mastered_units": len(state.get("mastered_units") or []),
        },
        "actions": [],
        "check": None,
        "evaluation": None,
        "input": {
            "enabled": True,
            "placeholder": "Ask or answer",
        },
    }


def _teach_frame(state: dict[str, Any]) -> dict[str, Any]:
    unit = _current_unit(state)
    frame = _base_frame(state, "teach")
    frame.update({
        "card": {
            "eyebrow": "Card",
            "title": unit.title,
            "body": _card_preview_body(unit),
            "example": "",
            "key_points": [],
            "detail": _unit_detail(unit),
        },
        "coach_text": (
            f"One card: {unit.title}. When it lands, start the check."
        ),
        "spoken_script": _flash_script(unit),
        "actions": [
            {"id": "play", "label": "Listen", "kind": "local"},
            {"id": "ask", "label": "Ask", "kind": "local"},
            {"id": "quiz", "label": "Start quiz", "kind": "step"},
            {"id": "continue", "label": "Finish block" if _is_last_unit(state) else "Next card", "kind": "step"},
        ],
    })
    return frame


def _check_frame(state: dict[str, Any]) -> dict[str, Any]:
    unit = _current_unit(state)
    question = _current_quiz_question(state, unit)
    question_index = _current_quiz_index(state, unit)
    quiz_total = len(_quiz_questions_for_unit(unit))
    frame = _base_frame(state, "check")
    options = deepcopy(question.get("options") or [])
    if options:
        check = {
            "type": "multiple_choice",
            "prompt": question.get("prompt") or unit.check_prompt,
            "options": options,
        }
    else:
        check = {
            "type": "free_text",
            "prompt": question.get("prompt") or unit.check_prompt,
            "options": [],
        }
    frame.update({
        "card": {
            "eyebrow": f"Quiz {question_index + 1} / {quiz_total}",
            "title": question.get("title") or "Mastery check",
            "body": question.get("prompt") or unit.check_prompt,
            "example": "",
            "key_points": [],
            "detail": _unit_detail(unit),
        },
        "check": check,
        "coach_text": f"Quiz question {question_index + 1} of {quiz_total}. Pick one, or type your own answer.",
        "spoken_script": _check_card_script(unit, question),
        "actions": [
            {"id": "play", "label": "Listen", "kind": "local"},
            {"id": "ask", "label": "Ask", "kind": "local"},
        ],
        "input": {
            "enabled": True,
            "placeholder": "Type answer",
        },
    })
    return frame


def _repair_frame(state: dict[str, Any], style: str) -> dict[str, Any]:
    unit = _current_unit(state)
    frame = _base_frame(state, "repair")
    body = unit.repair if style == "simpler" else unit.example
    title = "Simpler" if style == "simpler" else "Example"
    frame.update({
        "card": {
            "eyebrow": title,
            "title": unit.title,
            "body": _shorten(body, 150),
            "example": "",
            "key_points": [],
            "detail": _unit_detail(unit, body=body),
        },
        "coach_text": (
            "Let's slow it down and make it smaller. Read this version, then try the same tiny check."
            if style == "simpler"
            else "Here is the concrete version. Use this example as the shape of your answer."
        ),
        "spoken_script": body,
        "actions": [
            {"id": "play", "label": "Listen", "kind": "local"},
            {"id": "ask", "label": "Ask", "kind": "local"},
            {"id": "quiz", "label": "Start quiz", "kind": "step"},
            {"id": "continue", "label": "Finish block" if _is_last_unit(state) else "Next card", "kind": "step"},
        ],
    })
    return frame


def _answer_question_frame(state: dict[str, Any], user_text: str) -> dict[str, Any]:
    unit = _current_unit(state)
    frame = _base_frame(state, "repair")
    body = unit.repair
    frame.update({
        "card": {
            "eyebrow": "Coach answer",
            "title": unit.title,
            "body": _shorten(body, 150),
            "example": "",
            "key_points": [],
            "detail": _unit_detail(unit, body=body),
        },
        "coach_text": "I heard your question. I will answer it first, then we will retry the tiny check.",
        "spoken_script": body,
        "actions": [
            {"id": "play", "label": "Listen", "kind": "local"},
            {"id": "ask", "label": "Ask", "kind": "local"},
            {"id": "quiz", "label": "Start quiz", "kind": "step"},
            {"id": "continue", "label": "Finish block" if _is_last_unit(state) else "Next card", "kind": "step"},
        ],
    })
    return frame


def _evaluate_frame(
    state: dict[str, Any],
    *,
    option_id: str = "",
    user_text: str = "",
) -> dict[str, Any]:
    unit = _current_unit(state)
    question = _current_quiz_question(state, unit)
    question_index = _current_quiz_index(state, unit)
    quiz_total = len(_quiz_questions_for_unit(unit))
    passed = False
    heard = ""
    if option_id:
        selected = next((o for o in (question.get("options") or []) if o["id"] == option_id), None)
        heard = selected["label"] if selected else option_id
        passed = option_id == question.get("correct_option_id")
    else:
        heard = user_text
        lowered = user_text.lower()
        groups = question.get("expected_keyword_groups") or []
        if groups:
            group_hits = sum(
                1 for group in groups
                if any(str(keyword).lower() in lowered for keyword in group)
            )
            required_groups = int(question.get("required_keyword_groups") or min(2, len(groups)))
            passed = group_hits >= max(1, min(required_groups, len(groups)))
        else:
            keywords = question.get("expected_keywords") or unit.expected_keywords
            if keywords:
                hits = sum(1 for kw in keywords if str(kw).lower() in lowered)
                passed = hits >= max(1, min(2, len(keywords)))
            else:
                passed = len(user_text.split()) >= 7

    state["attempts"] = int(state.get("attempts") or 0) + 1
    verdict = "solid" if passed else "not_yet"
    is_last_question = question_index >= quiz_total - 1
    if passed:
        state["quiz_correct"] = int(state.get("quiz_correct") or 0) + 1
        if is_last_question:
            _mark_unit_mastered(state, unit.id)
            next_text = (
                "Unit mastered. Next card when you are ready."
                if not _is_last_unit(state)
                else "Unit mastered. This block is complete."
            )
        else:
            next_text = f"Good. Question {question_index + 2} is next."
    else:
        next_text = "Almost. Repair this idea, then retry this question."

    frame = _base_frame(state, "feedback")
    repair_text = question.get("repair") or unit.repair
    rationale = question.get("rationale") or _feedback_body(unit, heard, passed)
    feedback_text = _naturalize_feedback(rationale)
    frame.update({
        "card": {
            "eyebrow": "Feedback",
            "title": (
                "Unit mastered"
                if passed and is_last_question
                else "Good"
                if passed
                else "Repair"
            ),
            "body": feedback_text if passed else _shorten(repair_text, 180),
            "example": "",
            "key_points": [],
            "detail": _unit_detail(unit, body=feedback_text if passed else repair_text),
        },
        "evaluation": {
            "verdict": verdict,
            "label": (
                "Ready for next card"
                if passed and is_last_question
                else "Ready for next question"
                if passed
                else "Needs one repair pass"
            ),
            "heard": heard,
            "missing": "" if passed else repair_text,
            "next": next_text,
        },
        "coach_text": (
            "Good. That part is stable. Let's keep the quiz moving."
            if passed and not is_last_question
            else "Good. I heard the core idea. We can move on."
            if passed and is_last_question
            else "I heard your answer, but the core idea is not stable yet. Let's repair it before moving on."
        ),
        "spoken_script": next_text,
        "actions": (
            [{"id": "continue", "label": "Next card", "kind": "step"}]
            if passed and is_last_question else
            [
                {"id": "play", "label": "Listen", "kind": "local"},
                {"id": "ask", "label": "Ask", "kind": "local"},
                {"id": "next_question", "label": "Next question", "kind": "step"},
            ]
            if passed else
            [
                {"id": "play", "label": "Listen", "kind": "local"},
                {"id": "ask", "label": "Ask", "kind": "local"},
                {"id": "retry", "label": "Retry", "kind": "step"},
            ]
        ),
    })
    return frame


def _complete_frame(state: dict[str, Any]) -> dict[str, Any]:
    frame = _base_frame(state, "complete")
    frame.update({
        "card": {
            "eyebrow": "Block complete",
            "title": "Networking base is warmed up",
            "body": (
                "You now have the minimum interview frame: request path, layers, "
                "transport choices, protocol choices, HTTP APIs, latency budgets, "
                "load balancing, and timeout/retry failure policy."
            ),
            "example": "Next best step: train this with a short recap, then use it inside API Design.",
            "key_points": [
                "Place components on the request path.",
                "Default to HTTPS/HTTP unless the product needs a different protocol trade-off.",
                "Use p95/p99, health checks, timeouts, retries, backoff, idempotency, and monitoring.",
            ],
        },
        "coach_text": "Nice work. This learning block is complete. Train mode is the right next step.",
        "spoken_script": (
            "Nice work. The base is not finished forever, but it is stable enough "
            "to train. Next, we should do a short recap drill."
        ),
        "actions": [
            {"id": "restart", "label": "Review again", "kind": "step"},
            {"id": "go_train", "label": "Start Train", "kind": "local"},
        ],
    })
    return frame


def _source_for_state(state: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": "hellointerview.networking_essentials",
        "label": "HelloInterview Networking Essentials",
        "url": HELLOINTERVIEW_NETWORKING_URL,
        "note": (
            "Canonical reading for this networking lesson. The coach teaches in its own voice."
        ),
        "resources": [
            {
                "label": "HelloInterview Networking Essentials",
                "url": HELLOINTERVIEW_NETWORKING_URL,
            },
        ],
    }


def _unit_sources(unit: LearningUnit) -> list[dict[str, Any]]:
    sections = unit.source_sections or NETWORKING_UNIT_SOURCE_SECTIONS.get(unit.id, [])
    if not sections:
        return []
    return [
        {
            "label": "HelloInterview Networking Essentials",
            "role": "primary",
            "url": unit.source_url or HELLOINTERVIEW_NETWORKING_URL,
            "local_path": unit.source_path or HELLOINTERVIEW_NETWORKING_KB_PATH,
            "sections": sections,
            "paragraphs": deepcopy(unit.source_paragraphs),
        },
    ]


def _visible_card_script(unit: LearningUnit) -> str:
    parts = [
        unit.title,
        unit.body,
        f"Example: {unit.example}",
    ]
    if unit.key_points:
        parts.append("Key points: " + "; ".join(unit.key_points))
    return " ".join(part for part in parts if part).strip()


def _flash_body(unit: LearningUnit) -> str:
    if unit.flash_body:
        return unit.flash_body
    flash_bodies = {
        "networking.mental_model": (
            "Start with one browser request: DNS finds an address, IP routes packets, TCP establishes a reliable stream, and HTTP carries the response."
        ),
        "networking.layers": (
            "The layers are just shortcuts for thinking. DNS finds a destination, IP routes toward it, transport gives delivery behavior, and HTTP or WebSocket carries the application conversation."
        ),
        "networking.tcp_udp": (
            "Most designs can quietly lean on TCP. UDP is for cases where old packets are less useful than fresh ones, and QUIC is the modern wrinkle worth knowing without over-centering."
        ),
        "networking.protocol_choice": (
            "Protocol choice is mostly about the shape of the conversation: a normal request, a flexible client query, an internal RPC, a one-way stream, a two-way channel, or media."
        ),
        "networking.http_api": (
            "HTTP is the familiar web vocabulary. The useful part is not trivia; it is knowing what the method, path, headers, body, and status code let you express."
        ),
        "networking.latency": (
            "Latency is hiding in more places than server code: lookup, connection setup, distance, queues, dependencies, and the long tail users actually feel."
        ),
        "networking.load_balancing": (
            "Once you add more servers, you need a way to decide where traffic goes. The interesting parts are health, update speed, L4 versus L7, and persistent connections."
        ),
        "networking.failures": (
            "The network will be slow, weird, or down at exactly the wrong time. Timeouts, retries, idempotency, and circuit breakers are how the design stays calm."
        ),
    }
    return flash_bodies.get(unit.id, _shorten(unit.body, 130))


def _card_preview_body(unit: LearningUnit) -> str:
    return _shorten(unit.body, 620)


def _flash_script(unit: LearningUnit) -> str:
    return f"{unit.title}. {_flash_body(unit)}"


def _feedback_body(unit: LearningUnit, heard: str, passed: bool) -> str:
    if passed:
        return _flash_body(unit)
    return _shorten(unit.repair, 150)


def _interview_script(unit: LearningUnit) -> str:
    scripts = {
        "networking.mental_model": (
            "I start with one browser request: DNS resolves the name, IP routes packets, "
            "TCP gives a reliable ordered stream, and HTTP carries the request and response."
        ),
        "networking.layers": (
            "I separate the jobs by layer: DNS finds the destination, IP routes packets, "
            "transport chooses delivery guarantees, and the application protocol carries intent."
        ),
        "networking.network_layer": (
            "I expose a public edge or load balancer, then keep internal services on private "
            "addresses. IP is reachability and routing, not API behavior."
        ),
        "networking.tcp_udp": (
            "I assume TCP or HTTPS unless freshness matters more than perfect delivery. "
            "UDP only fits if the product can tolerate loss or repair it."
        ),
        "networking.protocol_choice": (
            "I start with REST for public request-response APIs, use GraphQL for flexible "
            "client reads, and use gRPC for controlled internal service calls."
        ),
        "networking.realtime_protocols": (
            "If the server mostly pushes, I use SSE. If both sides send frequently, I use "
            "WebSocket and then talk about reconnects, balancing, and fanout."
        ),
        "networking.webrtc": (
            "For audio or video, I use WebRTC for the media path, plus signaling, STUN, "
            "and TURN fallback. For normal collaboration, a server path is simpler."
        ),
        "networking.http_api": (
            "I describe the API with methods, paths, headers, bodies, and status codes. "
            "Then I keep handlers stateless so any healthy replica can serve."
        ),
        "networking.latency": (
            "I budget latency across DNS, connection setup, distance, queues, service work, "
            "and dependencies, then optimize the p95 or p99 pain."
        ),
        "networking.load_balancing": (
            "Once I add replicas, I explain who chooses a healthy backend, how health is checked, "
            "and whether L4, L7, DNS, or client-side routing fits."
        ),
        "networking.lb_client_side": (
            "If clients choose servers, I need fresh endpoint lists. DNS TTLs and cached records "
            "can be stale, so retries and refresh behavior matter."
        ),
        "networking.lb_dedicated": (
            "A dedicated load balancer centralizes health and policy. L4 sees connections, "
            "L7 sees HTTP details, and the algorithm should match the traffic shape."
        ),
        "networking.failures": (
            "For unreliable calls, I set timeouts, retry with capped backoff and jitter, require "
            "idempotency for writes, and use circuit breakers for failing dependencies."
        ),
    }
    return scripts.get(unit.id, unit.coach_script)


def _unit_detail(unit: LearningUnit, *, body: str | None = None) -> dict[str, Any]:
    blueprint = _networking_unit_blueprint(unit.id)
    return {
        "body": body or unit.body,
        "example": unit.example,
        "visual": _unit_visual(unit),
        "key_points": _networking_detail_points(unit),
        "interview_script": _interview_script(unit),
        "knowledge_points": blueprint.get("card_points", []),
        "quiz_dimensions": blueprint.get("quiz_dimensions", []),
        "dynamic_insert_rules": blueprint.get("dynamic_insert_rules", []),
        "coverage": {
            "source_sections": list(unit.source_sections),
            "knowledge_points": blueprint.get("card_points", []),
            "quiz_dimensions": blueprint.get("quiz_dimensions", []),
            "dynamic_insert_rules": blueprint.get("dynamic_insert_rules", []),
        },
        "origin": (
            "Source-grounded editorial summary. The wording is paraphrased for AgentCoach; "
            "source sections are listed for traceability."
        ),
        "sources": _unit_sources(unit),
        "source_paragraphs": deepcopy(unit.source_paragraphs),
        "draft": deepcopy(unit.draft),
    }


def _unit_visual(unit: LearningUnit) -> dict[str, Any]:
    if unit.id != "networking.mental_model":
        return {}
    return {
        "type": "request_path",
        "title": "Simple browser request",
        "nodes": [
            {"label": "Browser URL", "note": "user enters name"},
            {"label": "DNS lookup", "note": "name -> IP"},
            {"label": "IP routing", "note": "packets move"},
            {"label": "TCP handshake", "note": "reliable stream"},
            {"label": "HTTP response", "note": "request + page"},
            {"label": "Reuse / teardown", "note": "connection state"},
        ],
        "caption": (
            "One visible page request can hide lookup time, connection setup, packet exchanges, "
            "and connection state."
        ),
    }


def _naturalize_feedback(text: str) -> str:
    clean = " ".join((text or "").split())
    lowered = clean.lower()
    if lowered.startswith("right:"):
        return "Yes. " + clean.split(":", 1)[1].strip()
    return clean


def _check_card_script(unit: LearningUnit, question: dict[str, Any]) -> str:
    parts = [
        question.get("prompt") or unit.check_prompt,
        "Pick the best answer, or answer in your own words.",
    ]
    for index, option in enumerate(question.get("options") or unit.options, start=1):
        parts.append(f"Option {index}: {option['label']}")
    return " ".join(parts).strip()


def _shorten(text: str, limit: int) -> str:
    clean = " ".join((text or "").split())
    if len(clean) <= limit:
        return clean
    trimmed = clean[:limit].rsplit(" ", 1)[0].rstrip(" ,;:")
    return f"{trimmed}."


def _advance_unit(state: dict[str, Any]) -> None:
    unit = _current_unit(state)
    completed = state.setdefault("completed_units", [])
    if unit.id not in completed:
        completed.append(unit.id)
    state["unit_index"] = int(state.get("unit_index") or 0) + 1
    state["attempts"] = 0
    state["quiz_index"] = 0
    state["quiz_correct"] = 0


def _mark_unit_mastered(state: dict[str, Any], unit_id: str) -> None:
    mastered = state.setdefault("mastered_units", [])
    if unit_id not in mastered:
        mastered.append(unit_id)


def _is_last_unit(state: dict[str, Any]) -> bool:
    units = _units_for_topic(state["topic_id"], state["topic_name"])
    return int(state.get("unit_index") or 0) >= len(units) - 1


def _is_complete(state: dict[str, Any]) -> bool:
    units = _units_for_topic(state["topic_id"], state["topic_name"])
    return int(state.get("unit_index") or 0) >= len(units)


def _looks_like_question(text: str) -> bool:
    lowered = (text or "").lower().strip()
    if not lowered:
        return False
    starters = (
        "what", "why", "how", "when", "where", "explain", "describe",
        "can you", "could you", "什么", "为什么", "怎么", "如何", "解释",
    )
    return lowered.endswith("?") or any(lowered.startswith(s) for s in starters)


__all__ = [
    "NETWORKING_AGENTIC_BLUEPRINT",
    "NETWORKING_QUIZ",
    "frame_coach_text",
    "handle_learning_step",
    "initial_learning_frame",
    "networking_coverage_summary",
    "new_learning_state",
]
