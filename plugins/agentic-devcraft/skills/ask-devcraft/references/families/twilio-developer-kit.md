# openai/plugins family: twilio-developer-kit (Twilio Developer Kit)
Source: https://github.com/openai/plugins @ d420d13051bffe4543ed39e30fa46b87148e47dd
Distribution (openai/plugins): the Codex plugin marketplace `openai-curated` (`.agents/plugins/marketplace.json`); a plugin installs in Codex by name. Skill directories are `plugins/<plugin>/skills/<skill>/`. A "Codex-only" manifest note describes packaging, not where a skill can run: the skill's own `needs` line says what depends on Codex.
Curated records of remote catalog entries, not proof of installation: check at runtime that a skill is available in the current host and read its current SKILL.md before relying on any detail below.

Full records for the `twilio-developer-kit` family. The catalog entry is in openai-platforms.md.

## Family: twilio-developer-kit
- source path: `plugins/twilio-developer-kit` (manifest declares upstream https://github.com/twilio/ai). Plugin version 0.2.2, author Twilio, MIT, 55 skills.
- manifest notes: Codex manifest only (.codex-plugin/plugin.json; capabilities Read and Write). No MCP server, app connector, hooks, commands or subagents, and no Claude/Cursor manifest; no skill needs a host-specific tool, so skills work wherever SKILL.md files load. No manifest auth policy: skills tell the user to set TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN (or API key/secret) in environment variables and install the twilio SDK; SendGrid skills use a separate SG. key and the sendgrid SDK; webhooks need public HTTPS. Only twilio-ai-agent-architect sets allow_implicit_invocation: true. The skills README groups skills as Setup, Planner, Product, Guardrail; its install link points at an absent plugin README. Official Twilio MCP, Segment, Flex, AWS and Microsoft are advice in the skill text, not bundled.
- router: none formal. Eight planner skills act as sub-entry points by outcome (they qualify, then name product skills; high-level request gets discovery, mid-level validation, specific request goes straight to the product skill): twilio-messaging-overview and twilio-messaging-channel-advisor (messaging onboarding and channel), twilio-marketing-promotions-advisor, twilio-notifications-alerts-advisor, twilio-identity-verification-advisor, twilio-customer-support-architect, twilio-ai-agent-architect, twilio-agent-augmentation-architect. The one stated lifecycle is twilio-numbers-senders, then twilio-compliance-onboarding, then twilio-compliance-traffic, then twilio-security-hardening. Handoff names that are not skills in this plugin (never recommend them): twilio-conversations-api (use twilio-conversations-classic-api), twilio-sendgrid-email (use twilio-sendgrid-email-send), twilio-voice-insights and twilio-media-streams (no equivalent here; say so); twilio-agent-connect-aws and -microsoft are packages described inside twilio-agent-connect. Three-way email split by credential: Twilio Email (comms.twilio.com) versus SendGrid (SG. key); ask when unclear.
- development distance: core-dev (adds messaging, voice, verification, email and AI-agent integrations to application code).
- disclosure: rich. No router covers the skills, and they span genuinely different scenarios (messaging, compliance, email, voice, verification, AI conversations).
- note on names: two host-visible names differ from the directory: conversation-intelligence (directory twilio-conversation-intelligence, the name sibling skills use) and twilio-isv-sms-best-practices (directory twilio-sms-isv-setup). Records use the host-visible name as heading and the directory in the id.

### twilio-messaging-overview
- id: twilio-developer-kit:twilio-messaging-overview (source path: plugins/twilio-developer-kit/skills/twilio-messaging-overview/SKILL.md)
- description: "Twilio Messaging channel overview and onboarding guide. Covers all channels (SMS, WhatsApp, RCS, Facebook Messenger), the unified Messages API, channel selection guidance, and the recommended setup sequence from first message to production monitoring. Start here before choosing a specific messaging channel."
- use when: I'm new to Twilio messaging: which channels exist and what do I set up, in what order, before production?
- not for: twilio-messaging-channel-advisor (deeper channel choice for a specific use case).
- needs: nothing to read; its example sends need Twilio credentials and a sender.
- side effects: none; read-only (example code sends live messages if run).
- part of: entry for the messaging onboarding sequence: account-setup, first send, messaging-services, compliance-onboarding then compliance-traffic, WhatsApp/templates, messaging-webhooks. First SMS precedes registration, but US 10DLC registration still gates traffic. Names twilio-sms-send-message for sending; use twilio-send-message.

### twilio-messaging-channel-advisor
- id: twilio-developer-kit:twilio-messaging-channel-advisor (source path: plugins/twilio-developer-kit/skills/twilio-messaging-channel-advisor/SKILL.md)
- description: "Planning skill that helps the developer pick the right Twilio messaging channel — SMS, MMS, RCS, or WhatsApp — for a given use case. Qualifies intent across content type, geography, use case (marketing / notifications / OTP / support), cost model, and brand presence. Use when the developer asks "which channel should I use", "SMS vs RCS vs WhatsApp", mentions a country or region, asks about branded messaging, rich content, or fallback — and proactively when the developer says "send SMS" but their use case (rich content, international reach, branded experience) would benefit from a different channel."
- use when: Should this be SMS, WhatsApp or RCS? Or: I said 'send SMS' but I need logos, buttons, or users in Brazil/India.
- not for: twilio-messaging-overview (general onboarding); twilio-send-message (does the send); twilio-verify-send-otp (OTP).
- needs: nothing to advise; implementation needs a registered sender and consent.
- side effects: none; read-only. Does not send.
- part of: planner. Asks content, geography, use case, cost, brand; outputs primary channel, fallback, next skill, trade-offs. Hands to twilio-send-message, twilio-messaging-services, twilio-content-template-builder.

### twilio-marketing-promotions-advisor
- id: twilio-developer-kit:twilio-marketing-promotions-advisor (source path: plugins/twilio-developer-kit/skills/twilio-marketing-promotions-advisor/SKILL.md)
- description: "Planning skill for marketing and promotional messaging. Qualifies the developer's campaign needs across channel selection, compliance, audience segmentation, and delivery tracking to recommend the right Twilio messaging architecture. Handles both "set up a promotional SMS campaign" and "build a multi-channel engagement pipeline with Segment integration.""
- use when: Plan a promotional SMS, WhatsApp or email campaign: win-back, drip, or offers triggered from Segment audiences.
- not for: twilio-notifications-alerts-advisor (event-driven transactional); twilio-messaging-channel-advisor (only picks a channel).
- needs: audience, consent records, sender/template readiness; implementation needs Twilio or SendGrid credentials (Segment optional).
- side effects: none while planning; the campaigns it hands off send billable bulk traffic.
- part of: planner, entry for promotions. L1 single channel plus Messaging Service; L2 WhatsApp templates; L3 Segment and twilio-lookup-phone-intelligence. US: Brand, Campaign, link to Messaging Service. Pairs with twilio-compliance-traffic; bulk adds twilio-reliability-patterns.

### twilio-notifications-alerts-advisor
- id: twilio-developer-kit:twilio-notifications-alerts-advisor (source path: plugins/twilio-developer-kit/skills/twilio-notifications-alerts-advisor/SKILL.md)
- description: "Planning skill for transactional notifications, alerts, and reminders. Qualifies the developer's needs across urgency, channel selection, delivery confirmation, and fallback patterns to recommend the right Twilio notification architecture. Handles both "send shipping updates to customers" and "build a multi-channel alert system with delivery confirmation and fallback.""
- use when: Send shipping or appointment reminders, or alert on system failures and escalate from SMS to voice or email if undelivered.
- not for: twilio-marketing-promotions-advisor (promotional requests are redirected there); twilio-identity-verification-advisor (authentication).
- needs: event source, urgency, failure policy, volume; implementation needs credentials, senders and a callback host.
- side effects: none while planning; handed-off sends and calls are billable.
- part of: planner, entry for transactional notifications. Urgency: critical SMS plus voice in parallel; high SMS then voice after 5 min; medium SMS/WhatsApp then email; low email. Always status callbacks and deduplication.

### twilio-identity-verification-advisor
- id: twilio-developer-kit:twilio-identity-verification-advisor (source path: plugins/twilio-developer-kit/skills/twilio-identity-verification-advisor/SKILL.md)
- description: "Planning skill for identity verification and fraud prevention. Qualifies the developer's needs across authentication method, channel selection, fraud risk level, and user experience to recommend the right Twilio Verify + Lookup architecture. Handles login, signup, password reset, and risk-adaptive verification."
- use when: Add signup or login OTP/MFA, choose fallback channels, or block SIM-swap and SMS-pumping fraud before a high-value action.
- not for: twilio-verify-send-otp (the implementation); twilio-lookup-phone-intelligence (number data only, no proof of possession).
- needs: nothing to plan; implementation needs account, Verify Service, optional Lookup carrier packages.
- side effects: none while planning.
- part of: planner, entry for verification. L1 twilio-verify-send-otp; L2 adds fallback (SMS, wait 30 s, then call); L3 adds Lookup before Verify, recent SIM swap blocking SMS. Prefers managed Verify over homegrown OTP. Its output template says Level 1-4 but only three are defined: plan with Levels 1-3.

### twilio-customer-support-architect
- id: twilio-developer-kit:twilio-customer-support-architect (source path: plugins/twilio-developer-kit/skills/twilio-customer-support-architect/SKILL.md)
- description: "Planning skill for building customer service and support systems. Qualifies the developer's needs across the support ladder (self-service → AI agents → contact center), channel mix, and scale to recommend the right Twilio architecture. Handles both "build me a call center" and "add an IVR to my existing support line.""
- use when: Build a support line or call center: phone tree, queues, transfers, and whether I need Flex or TaskRouter.
- not for: twilio-ai-agent-architect (autonomous AI agent); twilio-agent-augmentation-architect (AI assisting human agents).
- needs: direction, channels, volume, CRM/PBX details; implementation needs account, numbers, webhooks.
- side effects: none while planning.
- part of: planner, entry for support. Level 1 IVR via twilio-voice-twiml; 2 AI self-service, hands to twilio-ai-agent-architect; 3 twilio-taskrouter-routing, twilio-conference-calls, twilio-call-recordings; 4 hands to twilio-agent-augmentation-architect. References nonexistent twilio-conversations-api.

### twilio-ai-agent-architect
- id: twilio-developer-kit:twilio-ai-agent-architect (source path: plugins/twilio-developer-kit/skills/twilio-ai-agent-architect/SKILL.md)
- description: "Planning skill for AI-powered conversational agents. Qualifies the developer's use case across outcome sophistication, entry point, and customer profile to recommend the right Twilio Conversations architecture and implementation skills. Handles both high-level requests ("build me a voice AI assistant") and specific ones ("integrate ConversationRelay with my OpenAI backend")."
- use when: Build an AI phone assistant or bot with memory and handoff to humans, or connect my LLM to Twilio.
- not for: twilio-agent-augmentation-architect (AI helps humans); twilio-customer-support-architect (queues/IVR); twilio-agent-connect (the SDK fast path once decided).
- needs: outcome, channels, memory/monitoring/escalation needs; voice implementation needs Twilio account, number, LLM account, public WebSocket. agents/openai.yaml allows implicit invocation.
- side effects: none while planning.
- part of: planner, entry for AI-agent sequence; stops at the level matching the outcome. L1 ConversationRelay + LLM (twilio-agent-connect, or manual twilio-voice-conversation-relay); L2 twilio-customer-memory; L3 conversation-intelligence; L4 twilio-taskrouter-routing. Always adds hardening and debugging.

### twilio-agent-augmentation-architect
- id: twilio-developer-kit:twilio-agent-augmentation-architect (source path: plugins/twilio-developer-kit/skills/twilio-agent-augmentation-architect/SKILL.md)
- description: "Planning skill for augmenting human agents with real-time AI intelligence. Qualifies the developer's use case across coaching, compliance, QA, and routing to recommend the right Conversation Intelligence + Conversation Memory + TaskRouter architecture. Handles both "I want to add AI coaching to my call center" and "configure Conversation Intelligence operators for script adherence.""
- use when: Coach my human call-center agents live, score script adherence after calls, or route frustrated callers using AI signals.
- not for: twilio-ai-agent-architect (autonomous agent); twilio-customer-support-architect (contact-center basics); conversation-intelligence (the operator/API skill).
- needs: goals, channels, current contact-center stack, budget; implementation needs transcription/recording, webhook backend, agent UI.
- side effects: none while planning.
- part of: planner, entry for human augmentation; step after support-architect Level 4. L1 listen (twilio-call-recordings), L2 coach (conversation-intelligence), L3 context (twilio-customer-memory, twilio-conversation-orchestrator), L4 route (twilio-taskrouter-routing). Flex context is summary-only; no silent copilot.

### twilio-account-setup
- id: twilio-developer-kit:twilio-account-setup (source path: plugins/twilio-developer-kit/skills/twilio-account-setup/SKILL.md)
- description: "Create and configure a Twilio account from scratch. Covers free trial signup, trial limitations, getting credentials (Account SID and Auth Token), buying a phone number, verifying recipient numbers for trial use, SDK installation, first API call, subaccount management (creation, inheritance, credential isolation, limits), and enabling specific products (AI Assistants, Conversations, Verify, ConversationRelay, WhatsApp). Use this skill before any other Twilio skill if you do not yet have a Twilio account or need to enable a product. For Organization-level governance (SSO, SCIM, multi-team), see `twilio-organizations-setup`."
- use when: I have no Twilio account, my trial can't message this number, or I need to enable ConversationRelay, Verify or WhatsApp, or give each customer a subaccount.
- not for: twilio-iam-auth-setup (credential types and rotation); twilio-organizations-setup (SSO/SCIM governance).
- needs: email and phone for signup, Console access; payment details to upgrade.
- side effects: buying numbers and the first send are billable; upgrading needs payment.
- part of: entry point before any other Twilio skill when access is the blocker; step 1 of messaging overview. Hands to twilio-iam-auth-setup, twilio-compliance-onboarding, twilio-organizations-setup.

### twilio-numbers-senders
- id: twilio-developer-kit:twilio-numbers-senders (source path: plugins/twilio-developer-kit/skills/twilio-numbers-senders/SKILL.md)
- description: "Choose the right Twilio number type and sender BEFORE building. Covers phone numbers (local, toll-free, short code, mobile), alphanumeric sender IDs, WhatsApp senders, RCS agents, international availability, and regulatory bundles. Each number type has its own compliance program — choosing wrong means rebuilding. Use this skill first."
- use when: Which kind of number or sender do I get before I build: local, toll-free, short code, alphanumeric, WhatsApp, RCS, or branded calling?
- not for: twilio-regulatory-compliance-bundles (non-US paperwork once chosen); twilio-compliance-onboarding (does the registration).
- needs: nothing beyond the repo.
- side effects: none; read-only reference.
- part of: step 1 of the stated lifecycle: choose, then twilio-compliance-onboarding, then twilio-compliance-traffic, then twilio-security-hardening. Hands to twilio-messaging-services and twilio-whatsapp-manage-senders.

### twilio-regulatory-compliance-bundles
- id: twilio-developer-kit:twilio-regulatory-compliance-bundles (source path: plugins/twilio-developer-kit/skills/twilio-regulatory-compliance-bundles/SKILL.md)
- description: "Manage regulatory compliance for international phone numbers. Covers what bundles are, which countries require them, how to create End-Users and Supporting Documents, evaluate and submit bundles, fix evaluation failures, update bundles when regulations change, and ISV multi-account patterns. Use this skill when provisioning numbers outside the US."
- use when: Buy phone numbers outside the US that need identity or address verification, or fix a failed bundle evaluation.
- not for: twilio-compliance-onboarding (A2P/toll-free sender registration after provisioning).
- needs: Account SID and Auth Token, identity documents, Python requests or twilio SDK.
- side effects: creates and submits regulatory records, then provisions paid numbers.
- part of: step in international number provisioning after twilio-numbers-senders and before twilio-compliance-onboarding. Flow: Regulation, End-User, Supporting Documents, Bundle, evaluate and submit, provision with bundle_sid.

### twilio-compliance-onboarding
- id: twilio-developer-kit:twilio-compliance-onboarding (source path: plugins/twilio-developer-kit/skills/twilio-compliance-onboarding/SKILL.md)
- description: "Registrations required BEFORE Twilio traffic works. Covers messaging programs (A2P 10DLC, toll-free verification, WhatsApp WABA, RCS, short code, alphanumeric sender) and voice trust programs (STIR/SHAKEN, Voice Integrity, Branded Calling, CNAM). Each number/sender type has its own program — registration blocks traffic until complete."
- use when: My new US SMS sender is blocked, or what must I register before launch (A2P 10DLC, toll-free, WhatsApp, RCS, voice trust)?
- not for: twilio-compliance-traffic (ongoing rules once registered); twilio-isv-sms-best-practices (multi-tenant SaaS onboarding); twilio-content-template-builder (message-template approval).
- needs: business identity/EIN, Trust Hub profile, sample messages, public opt-in evidence; paid account for toll-free.
- side effects: submits business data to external reviewers; approval delays can block launch.
- part of: mandatory pre-traffic step after twilio-numbers-senders, before twilio-compliance-traffic; step 3 of messaging overview. Verify is exempt. A2P: Customer Profile, Brand, Campaign, Messaging Service.

### twilio-isv-sms-best-practices
- id: twilio-developer-kit:twilio-sms-isv-setup (source path: plugins/twilio-developer-kit/skills/twilio-sms-isv-setup/SKILL.md)
- description: "Best practices for ISVs (Independent Software Vendors) building SMS features into multi-tenant SaaS platforms using Twilio. Covers customer onboarding for A2P and toll-free compliance, subaccount architecture, sender management, billing patterns, and common ISV pitfalls. Use this when building SMS capabilities that your customers will use to message their end users."
- use when: Build SMS into a multi-tenant SaaS where each customer messages their own users under their own brand, and onboard each one for A2P or toll-free.
- not for: twilio-compliance-onboarding (direct customers sending under one brand); twilio-organizations-setup (user governance, separate billing).
- needs: Twilio parent account on a paid plan, customer business data, SDK.
- side effects: none beyond registration steps; no executable code.
- part of: specialization of the SMS compliance path for ISVs. Subaccount per customer; per-customer Secondary Profile, Brand, Campaign. Do not share campaigns across customers. Hands to twilio-compliance-onboarding, twilio-messaging-services, twilio-iam-auth-setup.

### twilio-compliance-traffic
- id: twilio-developer-kit:twilio-compliance-traffic (source path: plugins/twilio-developer-kit/skills/twilio-compliance-traffic/SKILL.md)
- description: "Rules you must follow for Twilio messaging and voice traffic. Covers TCPA (consent tiers, quiet hours, DNC), GDPR (EU consent, right to deletion), PCI DSS (payment recording, Pay verb), HIPAA (BAA, PHI), FDCPA (debt collection limits), CAN-SPAM, WhatsApp policies, SHAKEN/STIR, and consent management patterns. Use this skill proactively when developers have working traffic to ensure they follow the rules."
- use when: Messages and calls already work; how do I handle consent, opt-outs, quiet hours, recordings, healthcare or collections correctly?
- not for: twilio-compliance-onboarding (pre-launch registration); twilio-security-compliance-hipaa (HIPAA specifics).
- needs: geography, message purpose, consent records, your own DNC/deletion tracking.
- side effects: none; read-only guidance (its patterns can suppress traffic or delete data).
- part of: guardrail step after twilio-compliance-onboarding; run alongside marketing, notifications, support and AI workflows. US and EU focus; verify current regulations before launch.

### twilio-iam-auth-setup
- id: twilio-developer-kit:twilio-iam-auth-setup (source path: plugins/twilio-developer-kit/skills/twilio-iam-auth-setup/SKILL.md)
- description: "Set up and manage Twilio authentication credentials: Auth Tokens, API keys (Standard, Main, Restricted), Access Tokens for client-side SDKs, and credential rotation. Use this skill as a prerequisite foundation before making any Twilio API calls."
- use when: Create or rotate Twilio credentials: restricted or messaging-only API key, leaked-credential replacement, browser Voice/Chat tokens.
- not for: twilio-security-api-auth (choosing a method, OAuth2); twilio-account-setup (signup).
- needs: existing account, Console, privileged credentials, secret storage.
- side effects: creates and revokes credentials; can invalidate sessions and clients.
- part of: foundation step before API use; procedures skill. Rotation: secondary token, switch app, confirm, promote. Restricted keys cannot sign Access Tokens. Hands to twilio-security-hardening.

### twilio-security-api-auth
- id: twilio-developer-kit:twilio-security-api-auth (source path: plugins/twilio-developer-kit/skills/twilio-security-api-auth/SKILL.md)
- description: "Choose the right Twilio authentication method and implement it correctly. Covers Auth Token (testing only), API Keys (production standard), OAuth2 client_credentials (time-limited bearer tokens), Access Tokens (client-side SDKs), and test credentials. Use this skill before making any Twilio API calls in production."
- use when: Which Twilio auth method fits production: Auth Token, API key, OAuth2 client credentials, Access Token, or test credentials?
- not for: twilio-iam-auth-setup (procedures: create, rotate, replace); twilio-security-hardening (signature validation, fraud).
- needs: Twilio account and Console to create keys.
- side effects: creates credentials.
- part of: standalone decision table, the only skill covering OAuth2 bearer tokens. Overlaps twilio-iam-auth-setup on API keys and test credentials; decisions go here, procedures there.

### twilio-organizations-setup
- id: twilio-developer-kit:twilio-organizations-setup (source path: plugins/twilio-developer-kit/skills/twilio-organizations-setup/SKILL.md)
- description: "Set up and manage Twilio Organizations for centralized account and user governance. Covers the Organization > Account > Subaccount hierarchy, roles (Owner/Admin/Standard), managed vs independent accounts, domain registration, SSO enforcement, SCIM provisioning, and Organization merging. Use this skill when managing multiple Twilio accounts or users across teams."
- use when: Manage several Twilio accounts or users across teams: Organization versus subaccount, SSO, SCIM, domain verification, merging.
- not for: twilio-account-setup (single-account and subaccount mechanics).
- needs: an Organization with Owner or Admin rights; Console only.
- side effects: documented Console procedures create accounts, transfer ownership, change domain/SSO access, reset passwords/2FA, and merge Organizations (the Candidate ceases to exist).
- part of: standalone governance. Organizations give users/SSO with separate billing; subaccounts give programmatic multi-tenancy with consolidated billing.

### twilio-security-hardening
- id: twilio-developer-kit:twilio-security-hardening (source path: plugins/twilio-developer-kit/skills/twilio-security-hardening/SKILL.md)
- description: "Secure Twilio applications against common attacks. Covers credential management (API keys vs auth tokens), request validation (webhook signature verification), PCI DSS compliance, HIPAA account requirements, SMS pumping prevention, geo-permissions, and account isolation patterns. Use this skill when developers are building or deploying Twilio apps."
- use when: Secure my Twilio app: credential leaks, webhook signature validation, SMS pumping and geo-permissions, key rotation, PCI mode.
- not for: twilio-security-api-auth (choose method); twilio-webhook-architecture (full webhook validation); twilio-security-compliance-hipaa (HIPAA depth).
- needs: Twilio account and credentials.
- side effects: PCI Mode, if enabled, is irreversible and account-wide.
- part of: last step of lifecycle choose, register, follow traffic rules, secure. Always recommended by the planners. Hands to twilio-iam-auth-setup, twilio-webhook-architecture, twilio-lookup-phone-intelligence.

### twilio-security-compliance-hipaa
- id: twilio-developer-kit:twilio-security-compliance-hipaa (source path: plugins/twilio-developer-kit/skills/twilio-security-compliance-hipaa/SKILL.md)
- description: "Configure Twilio accounts for HIPAA compliance. Covers BAA requirements, HIPAA Project designation (self-service and support), eligible services list, per-product requirements (Voice, SMS, ConversationRelay, Conversation Intelligence, Flex, Verify), message redaction, and what is NOT eligible. Use this skill when developers are building healthcare workflows on Twilio."
- use when: Build healthcare workflows (PHI) on Twilio: BAA, HIPAA account designation, which services are eligible, message redaction.
- not for: twilio-security-hardening (only a short generic HIPAA section); twilio-organizations-setup (flagging accounts).
- needs: BAA signed via a Twilio representative, linked Organization, Editions package; manual Console and Support steps.
- side effects: none; guidance only.
- part of: specialist guardrail. Order: execute BAA, designate HIPAA projects, use only eligible services, follow per-product rules. Excludes WhatsApp, SendGrid email, Verify Fraud Guard and email channel, non-US area codes. Intelligence v3 is not HIPAA eligible.

### twilio-send-message
- id: twilio-developer-kit:twilio-send-message (source path: plugins/twilio-developer-kit/skills/twilio-send-message/SKILL.md)
- description: "Send messages via Twilio's Programmable Messaging API across all channels — SMS, MMS, RCS, and WhatsApp. Covers text messages, media, rich content (cards, carousels, buttons), template-based sends, Messaging Services, status callbacks, and WhatsApp's 24-hour service window. Use when the user wants to send a message — whether they say "send SMS", "text message", "branded message", "rich message", "WhatsApp message", "RCS message", "notification", or "alert". For picking the right channel for a use case, first consult twilio-messaging-channel-advisor."
- use when: Send a text, SMS, MMS, WhatsApp or RCS message, notification or alert through one API.
- not for: twilio-sms-send-message (SMS delivery debugging only); twilio-whatsapp-send-message (WhatsApp window and sandbox); twilio-rcs-messaging (RCS onboarding); twilio-verify-send-otp (OTP).
- needs: Account credentials, a number, channel sender or Messaging Service, twilio SDK.
- side effects: sends real, billable messages; the skill has no confirmation gate, so advise confirming recipient and content first (as twilio-email-send requires).
- part of: consolidated send entry point; deep-dive siblings defer to it. Consult twilio-messaging-channel-advisor first when the channel is undecided. Cannot send cross-channel in one call.

### twilio-sms-send-message
- id: twilio-developer-kit:twilio-sms-send-message (source path: plugins/twilio-developer-kit/skills/twilio-sms-send-message/SKILL.md)
- description: "SMS and MMS deep-dive reference. Covers SMS-specific error codes, message filtering troubleshooting ("Messages Being Filtered or Blocked?" diagnostic checklist), MMS media support (US/CA/AU only), and SMS pumping indicators. For sending SMS, use twilio-send-message instead. Use this skill only when debugging SMS delivery issues or needing SMS-specific details not in the consolidated send skill."
- use when: SMS or MMS isn't delivering: filtered, blocked, errors 30034/30007/21610/21408, or SMS-specific details.
- not for: twilio-send-message (plain sends; this skill says to use it instead); twilio-debugging-observability (cross-product triage).
- needs: account credentials, an SMS-capable number, SDK.
- side effects: none beyond normal send cost.
- part of: debugging reference step. Do not retry after 21610 (opted out). MMS only US/CA/AU. Messaging overview lists it as the first-SMS step; prefer twilio-send-message for that.

### twilio-whatsapp-send-message
- id: twilio-developer-kit:twilio-whatsapp-send-message (source path: plugins/twilio-developer-kit/skills/twilio-whatsapp-send-message/SKILL.md)
- description: "WhatsApp messaging deep-dive reference. Covers the 24-hour service window rules (free-form vs template mode), sandbox setup for testing, template approval workflow, production sender requirements, and WhatsApp-specific error handling. For sending WhatsApp messages, use twilio-send-message instead. Use this skill when setting up WhatsApp for the first time or debugging WhatsApp-specific delivery behavior."
- use when: Set up WhatsApp for the first time, use the sandbox, or debug the 24-hour window, templates, errors 63003/63018/63020.
- not for: twilio-send-message (plain sends); twilio-whatsapp-manage-senders (production sender registration).
- needs: WhatsApp enabled on the account; recipient opt-in; for production, a registered sender and approved template.
- side effects: sandbox and production sends are billable.
- part of: first step of the WhatsApp sequence (sandbox, then twilio-whatsapp-manage-senders, then send). Free-form outside the window fails silently. Names nonexistent twilio-conversations-api.

### twilio-whatsapp-manage-senders
- id: twilio-developer-kit:twilio-whatsapp-manage-senders (source path: plugins/twilio-developer-kit/skills/twilio-whatsapp-manage-senders/SKILL.md)
- description: "Create, configure, and manage WhatsApp Business senders via Twilio's Channels Senders API. Covers programmatic sender registration, profile setup, webhook configuration, sender lifecycle statuses, and ISV flows. Use this skill to register and manage production WhatsApp senders at scale."
- use when: Register or manage a production WhatsApp Business sender through the Channels Senders API, including ISV/WABA flows.
- not for: twilio-whatsapp-send-message (sandbox and sending rules); twilio-numbers-senders (short overview only).
- needs: upgraded (not trial) account, a number that is not already on WhatsApp and can receive an OTP, Meta Business Manager invitation for ISV flow.
- side effects: registers a WhatsApp Business sender on the account.
- part of: step 2 of WhatsApp sequence, after sandbox. Sender cap: 2 until Meta Business Verification. Hands to twilio-whatsapp-send-message, twilio-content-template-builder, twilio-verify-send-otp.

### twilio-rcs-messaging
- id: twilio-developer-kit:twilio-rcs-messaging (source path: plugins/twilio-developer-kit/skills/twilio-rcs-messaging/SKILL.md)
- description: "Send RCS Business Messages via Twilio. Covers compliance onboarding (7-part US process), sender profile setup, sending rich cards and carousels, SMS fallback, device support (Android + iOS 18 caveats), and common errors. Use this skill when building RCS messaging or onboarding an RCS sender."
- use when: Send branded RCS messages with rich cards or carousels, or onboard an RCS sender.
- not for: twilio-send-message (generic send, including forced rcs: addressing); twilio-content-template-builder (templates).
- needs: paid account, Messaging Service, Console-created RCS sender, Content Template for rich cards; multi-week carrier review.
- side effects: sends are billable; onboarding submits business data for review.
- part of: step in messaging onboarding (channels). Cannot send RCS without a Messaging Service; profile changes after approval need re-review. Hands to twilio-content-template-builder, twilio-messaging-services, twilio-compliance-onboarding.

### twilio-content-template-builder
- id: twilio-developer-kit:twilio-content-template-builder (source path: plugins/twilio-developer-kit/skills/twilio-content-template-builder/SKILL.md)
- description: "Create, manage, and send message templates using Twilio's Content API. Covers template creation for WhatsApp, SMS, RCS, and MMS; variable usage; WhatsApp Meta approval; and sending templates via ContentSid. Use this skill when building structured messages that require pre-approval or consistent formatting across channels."
- use when: Create an approved WhatsApp reminder template, send a reusable personalized message, or give rich RCS cards an SMS fallback.
- not for: twilio-compliance-onboarding (sender registration, not templates); twilio-messaging-services (pools and fallback config).
- needs: credentials, SDK, active WhatsApp sender for that channel, template text and sample variables.
- side effects: creates and deletes remote templates, submits to Meta, sends billable messages.
- part of: step 5 of messaging overview and marketing Level 2. Tell the user to plan 24-48 hours for Meta approval (the skill says under 1 hour typical and up to 24; the planners say 24-48).

### twilio-messaging-services
- id: twilio-developer-kit:twilio-messaging-services (source path: plugins/twilio-developer-kit/skills/twilio-messaging-services/SKILL.md)
- description: "Create and configure Twilio Messaging Services for production messaging. Covers sender pools, geo-match, sticky sender, message scheduling, compliance toolkit, SMS pumping protection, link shortening, and intelligent alerts. Use this skill when setting up production-ready messaging infrastructure."
- use when: Move from one sender to production: sender pools, scheduling, pumping protection, quiet hours, link shortening, or delivery alerts.
- not for: twilio-compliance-onboarding (campaign registration); twilio-content-template-builder (content); twilio-verify-send-otp (Verify has its own Fraud Guard).
- needs: credentials, SDK, one SMS-capable number; DNS for branded links.
- side effects: changes production routing, schedules and cancels real messages, can block recipients.
- part of: steps 2, 4 and 6 of messaging overview; infrastructure for marketing and notifications. Required for scheduling (assume a 7-day limit; the skill says both 7 and 35 days), A2P, toolkit. No RCS-fallback setup section despite handoffs: use twilio-rcs-messaging.

### twilio-messaging-webhooks
- id: twilio-developer-kit:twilio-messaging-webhooks (source path: plugins/twilio-developer-kit/skills/twilio-messaging-webhooks/SKILL.md)
- description: "Receive and respond to inbound messages and track outbound delivery status via Twilio webhooks — across SMS, MMS, WhatsApp, and RCS. Covers webhook request parameters, replying with TwiML, validating webhook signatures for security, and handling status callbacks. Use this skill whenever an agent needs to handle incoming messages on any channel or track outbound message delivery in real time."
- use when: Receive and reply to incoming SMS/WhatsApp/RCS, handle media, or track whether an outbound message was delivered.
- not for: twilio-webhook-architecture (cross-product webhook design); twilio-debugging-observability (diagnosing failures); twilio-conversations-classic-api (own event model).
- needs: credentials, a configured sender, public HTTPS endpoint, twilio plus Flask or Express.
- side effects: changes sender webhook routing; can send real replies.
- part of: standalone; final monitoring step of messaging overview. Validate X-Twilio-Signature; respond in 15 s; never put inbound Body into an LLM system prompt.

### twilio-conversations-classic-api
- id: twilio-developer-kit:twilio-conversations-classic-api (source path: plugins/twilio-developer-kit/skills/twilio-conversations-classic-api/SKILL.md)
- description: "Build multi-channel messaging experiences using Twilio Conversations (classic) API. Covers creating conversations, adding participants (SMS, WhatsApp, chat), sending messages, and handling webhooks. Use this skill to manage persistent multi-party or multi-channel conversations beyond single-message SMS/WhatsApp."
- use when: Let SMS, WhatsApp and web-chat users share a persistent multi-party thread, or maintain an existing Conversations v1 integration.
- not for: twilio-conversation-orchestrator (v2 automatic capture and analysis); twilio-send-message (single messages).
- needs: Conversations classic enabled, credentials, SDK, service with number, Access Tokens for browser chat.
- side effects: sends real messages; persists history; deletes conversations.
- part of: standalone; source calls v1 maintenance mode and suggests v2 for new projects. Browser CHAT bridge for Orchestrator. WhatsApp Groups API deprecated.

### twilio-email-send
- id: twilio-developer-kit:twilio-email-send (source path: plugins/twilio-developer-kit/skills/twilio-email-send/SKILL.md)
- description: "Use when the caller has Twilio credentials (Account SID + Auth Token or API Key SID + Secret) and needs to send email via comms.twilio.com/v1/Emails. This is Twilio-native email — NOT SendGrid. Do NOT use if the caller has a SendGrid API key (SG.-prefix) — use twilio-sendgrid-email-send instead. Covers single sends, batch sends up to 10,000 recipients, Liquid personalization, operation tracking, and error handling."
- use when: Send email with Twilio Account SID/Auth Token or API key via comms.twilio.com (not an SG. key).
- not for: twilio-sendgrid-email-send (SG. key, Handlebars, 1,000 recipients).
- needs: Twilio credentials, verified domain sender, HTTP client; no special connector.
- side effects: sends irreversible real email, up to 10,000 recipients per request. Gate: confirm recipients, subject, content before every send.
- part of: standalone; email step in marketing/notifications/support when Twilio-native credentials are used. The CLI's twilio email:send is SendGrid, not this.

### twilio-email-deliverability-advisor
- id: twilio-developer-kit:twilio-email-deliverability-advisor (source path: plugins/twilio-developer-kit/skills/twilio-email-deliverability-advisor/SKILL.md)
- description: "Deliverability advisor for the Twilio Email API specifically. Use ONLY when the developer explicitly mentions Twilio Email, comms.twilio.com, or a Twilio (non-SendGrid) email program. For all other deliverability questions — including generic ones — use twilio-sendgrid-deliverability-advisor."
- use when: My Twilio-native (comms.twilio.com) email goes to spam or bounces.
- not for: twilio-sendgrid-deliverability-advisor (generic, unclear or SendGrid deliverability: recommend that one, as the description says; it asks the platform first).
- needs: domain authentication and list metrics; DNS/Console access for fixes.
- side effects: none; fixes may change DNS or sending behavior.
- part of: narrow entry; self-described work in progress with limited tooling. Hands SendGrid cases to twilio-sendgrid-deliverability-advisor and sending to twilio-email-send.

### twilio-sendgrid-account-setup
- id: twilio-developer-kit:twilio-sendgrid-account-setup (source path: plugins/twilio-developer-kit/skills/twilio-sendgrid-account-setup/SKILL.md)
- description: "Set up a SendGrid account for email delivery. Covers API key creation (SG.-prefix), domain authentication (DKIM/SPF via CNAME records), Single Sender Verification for testing, SDK installation, and the relationship between SendGrid and Twilio credentials. Use before any other SendGrid skill. This skill is for SendGrid only — not the Twilio Email API (comms.twilio.com)."
- use when: First-time SendGrid email setup: SG. API key, domain authentication (DKIM/SPF CNAMEs), Single Sender Verification, SMTP relay.
- not for: twilio-email-send (Twilio Email API at comms.twilio.com).
- needs: separate SendGrid account and key (Twilio credentials do not work), DNS write access.
- side effects: setup creates credentials, installs an SDK and changes DNS authentication records. Never display or log a user's API key.
- part of: entry point of the SendGrid group, use before other SendGrid skills. Hands to twilio-sendgrid-email-send, twilio-sendgrid-email-settings, twilio-sendgrid-webhooks.

### twilio-sendgrid-email-send
- id: twilio-developer-kit:twilio-sendgrid-email-send (source path: plugins/twilio-developer-kit/skills/twilio-sendgrid-email-send/SKILL.md)
- description: "Send transactional and bulk email via the SendGrid v3 Mail Send API. Covers single sends, personalized batch sends with dynamic templates, scheduled sends with cancellation, attachments, and sandbox mode for testing. Use this skill when the caller has a SendGrid API key (SG.-prefix). Do NOT use this skill if the caller is using the Twilio Email API (comms.twilio.com) — that is a separate product with different credentials."
- use when: Send transactional or bulk email through SendGrid with an SG. key: templates, scheduled sends, attachments, sandbox mode.
- not for: twilio-email-send (Twilio-native comms.twilio.com).
- needs: SENDGRID_API_KEY with Mail Send permission, verified sender or authenticated domain, SDK.
- side effects: sends irreversible real email; can schedule and cancel sends with a pre-assigned batch ID; sandbox validates without delivery. Gate: always confirm recipients, subject, content before sending, batches especially.
- part of: core send step after twilio-sendgrid-account-setup; then twilio-sendgrid-webhooks, twilio-sendgrid-suppressions. Limits: 1,000 recipients per call, send_at within 72 h.

### twilio-sendgrid-deliverability-advisor
- id: twilio-developer-kit:twilio-sendgrid-deliverability-advisor (source path: plugins/twilio-developer-kit/skills/twilio-sendgrid-deliverability-advisor/SKILL.md)
- description: "Diagnostic and advisory skill for email deliverability problems. Use when a developer asks why emails are going to spam, not reaching the inbox, getting blocked, bouncing, or how to improve sender reputation — with or without a specified platform. Covers SendGrid-specific tooling: SPF, DKIM, DMARC, BIMI, IP warmup, list hygiene, bounce/spam rate thresholds, and Engagement Quality Score (SEQ). Do NOT use for Twilio Email (comms.twilio.com / Account SID + Auth Token) — use twilio-email-deliverability-advisor instead. Do NOT use for general email sending questions — use twilio-sendgrid-email-send (SendGrid) or twilio-email-deliverability-advisor instead."
- use when: My emails go to spam, bounce or are blocked; how do I improve sender reputation, warm IPs, set up SPF/DKIM/DMARC?
- not for: twilio-email-deliverability-advisor (Twilio Email); twilio-sendgrid-engagement-quality (SEQ API mechanics); twilio-sendgrid-suppressions (list management).
- needs: a SendGrid account; SEQ needs Pro or Premier.
- side effects: none; recommendations only.
- part of: advisor, correct front door for generic email deliverability. Identifies platform first (asks if no signal), then triage, audit or foundation. Hands to twilio-sendgrid-account-setup, twilio-sendgrid-suppressions, twilio-sendgrid-webhooks.

### twilio-sendgrid-email-settings
- id: twilio-developer-kit:twilio-sendgrid-email-settings (source path: plugins/twilio-developer-kit/skills/twilio-sendgrid-email-settings/SKILL.md)
- description: "Configure SendGrid dynamic templates (Handlebars), tracking settings (opens, clicks, subscriptions), link branding for custom tracking domains, and content types (HTML, plain text, AMP). Use when customizing SendGrid email content, tracking behavior, or branded links. Requires a SendGrid API key (SG.-prefix) — not applicable to the Twilio Email API (comms.twilio.com)."
- use when: Customize SendGrid dynamic templates (Handlebars), open/click tracking, link branding, or content types.
- not for: twilio-sendgrid-email-send (actually sending); twilio-sendgrid-account-setup (domain authentication, not link branding).
- needs: SendGrid API key; DNS CNAME for link branding.
- side effects: applying the guidance changes templates, per-message or account-wide tracking, and link-branding DNS.
- part of: standalone configuration reference supporting twilio-sendgrid-email-send. Custom Handlebars helpers unsupported; undefined variables fail silently.

### twilio-sendgrid-engagement-quality
- id: twilio-developer-kit:twilio-sendgrid-engagement-quality (source path: plugins/twilio-developer-kit/skills/twilio-sendgrid-engagement-quality/SKILL.md)
- description: "Monitor email program health with SendGrid Engagement Quality (SEQ) scores. Covers the SEQ API endpoints, the 5 scoring metrics (engagement recency, open rate, bounce classification, bounce rate, spam rate), eligibility requirements, and interpreting scores for deliverability improvement. Use when diagnosing SendGrid deliverability issues or monitoring sender reputation. Requires a SendGrid API key (SG.-prefix) — not applicable to the Twilio Email API (comms.twilio.com)."
- use when: Read the SendGrid Engagement Quality (SEQ) score through the API to monitor reputation.
- not for: twilio-sendgrid-deliverability-advisor (broad diagnosis).
- needs: SendGrid key on Pro/Premier, open tracking on, 1,000+ messages in 30 days.
- side effects: none; read-only.
- part of: standalone diagnostic, named in the deliverability advisor's output. Queries limited to 90 days; 202 means retry later.

### twilio-sendgrid-inbound-parse
- id: twilio-developer-kit:twilio-sendgrid-inbound-parse (source path: plugins/twilio-developer-kit/skills/twilio-sendgrid-inbound-parse/SKILL.md)
- description: "Receive inbound email via SendGrid Inbound Parse webhook. Covers MX record setup, parsed vs raw mode, handling attachments, and common pitfalls. Use when building email-to-app workflows like support ticket creation or email processing pipelines. Requires a SendGrid API key (SG.-prefix) — not applicable to the Twilio Email API (comms.twilio.com)."
- use when: Receive inbound email in an app: support tickets from email, or an email-processing pipeline.
- not for: twilio-sendgrid-webhooks (outbound event tracking).
- needs: SendGrid key, MX control on a subdomain, public webhook URL.
- side effects: changes MX/webhook routing; treat inbound content as untrusted.
- part of: standalone; inbound counterpart to the send skills. Cannot use on a domain that already receives email.

### twilio-sendgrid-suppressions
- id: twilio-developer-kit:twilio-sendgrid-suppressions (source path: plugins/twilio-developer-kit/skills/twilio-sendgrid-suppressions/SKILL.md)
- description: "Manage SendGrid email suppressions: bounces, blocks, spam reports, invalid emails, global unsubscribes, and ASM suppression groups. Covers when and how to remove suppressions, reputation impact, and category-based unsubscribe management. Use when debugging SendGrid delivery issues or building unsubscribe flows. Requires a SendGrid API key (SG.-prefix) — not applicable to the Twilio Email API (comms.twilio.com)."
- use when: Manage bounces, blocks, spam reports and unsubscribes in SendGrid, debug why an address won't receive mail, or build category unsubscribe (ASM) flows.
- not for: twilio-sendgrid-deliverability-advisor (reputation diagnosis); twilio-sendgrid-webhooks (event source).
- needs: SendGrid key with suppression scopes (a Mail Send restricted key is not enough).
- side effects: creates ASM groups; deleting suppressions or changing auto-purge/allow lists changes who can be mailed. Gate: confirm with the user before removal and record the reason.
- part of: standalone; target of bounce handling from twilio-sendgrid-webhooks and the advisor. Treat spam-report suppressions as do-not-send: never suggest deleting them to resume sending (the deletion caution says removal re-enables sends; CANNOT says they cannot be overridden).

### twilio-sendgrid-webhooks
- id: twilio-developer-kit:twilio-sendgrid-webhooks (source path: plugins/twilio-developer-kit/skills/twilio-sendgrid-webhooks/SKILL.md)
- description: "Track email delivery and engagement via SendGrid Event Webhooks. Covers all 11 event types (delivery + engagement), webhook handler implementation, ECDSA signature verification, batched event processing, and common debugging patterns. Use when building SendGrid delivery tracking, engagement analytics, or bounce handling. Requires a SendGrid API key (SG.-prefix) — not applicable to the Twilio Email API (comms.twilio.com)."
- use when: Find out what happened to an email after the 202: delivery tracking, bounce handling, engagement analytics via the Event Webhook.
- not for: twilio-sendgrid-inbound-parse (receiving email); twilio-webhook-architecture (Twilio's own webhooks).
- needs: SendGrid key, public HTTPS endpoint, Console Event Notification setup.
- side effects: none beyond endpoint exposure; enable signing, since webhooks are unauthenticated by default.
- part of: step after twilio-sendgrid-email-send; feeds twilio-sendgrid-suppressions. SendGrid posts batched arrays; dedupe on sg_event_id.

### twilio-verify-send-otp
- id: twilio-developer-kit:twilio-verify-send-otp (source path: plugins/twilio-developer-kit/skills/twilio-verify-send-otp/SKILL.md)
- description: "Send and verify one-time passcodes (OTPs) via Twilio Verify over SMS, RCS, voice, email, or WhatsApp. Covers creating a Verify Service, sending tokens, checking submitted codes, automatic WhatsApp-to-SMS fallback, and service configuration. TOTP is supported via the Factors API (a separate family from channel-based OTP). Use this skill to add phone or email verification or two-factor authentication to any application."
- use when: Add phone or email verification or two-factor authentication with OTP codes (SMS, voice, email, WhatsApp, RCS).
- not for: twilio-send-message (custom OTP on messaging; needs A2P registration); twilio-identity-verification-advisor (planning and fraud design).
- needs: account (trial OK for limited destinations), credentials, Verify Service SID (created by the quickstart), SDK; WhatsApp needs a registered production sender; email needs Mailer configuration.
- side effects: creates Verify Services, sends codes and checks verification state; billed per confirmed verification plus channel fee.
- part of: standalone product; implementation step of twilio-identity-verification-advisor. Verify is exempt from A2P 10DLC. Wrong code returns status pending, not an exception.

### twilio-lookup-phone-intelligence
- id: twilio-developer-kit:twilio-lookup-phone-intelligence (source path: plugins/twilio-developer-kit/skills/twilio-lookup-phone-intelligence/SKILL.md)
- description: "Look up phone number intelligence via Twilio Lookup v2 API. Covers number validation, line type detection (mobile/landline/VoIP), SIM swap detection, caller name, identity match, and SMS pumping risk scoring. Use this skill to validate numbers or assess fraud risk before sending messages or calls."
- use when: Is this phone number valid, mobile or VoIP; check SIM swap before OTP; clean numbers before a bulk send.
- not for: twilio-verify-send-otp (proves possession; Lookup does not); twilio-identity-verification-advisor (whole risk design).
- needs: credentials, SDK, one number per call; SIM swap needs carrier approval; paid packages.
- side effects: none; read-only apart from Line Type Override POST/DELETE. Paid per request.
- part of: standalone enrichment; Level 3 pre-Verify step and pre-bulk step in marketing Level 3. US-only CNAM and reassignment data.

### twilio-voice-twiml
- id: twilio-developer-kit:twilio-voice-twiml (source path: plugins/twilio-developer-kit/skills/twilio-voice-twiml/SKILL.md)
- description: "Build voice call logic using TwiML (Twilio Markup Language). Covers the core verbs (Say, Play, Gather, Dial, Record, Conference), generating TwiML with Python and Node.js SDKs, and a complete inbound call IVR example. Use this skill to define call behavior for inbound or outbound calls."
- use when: Define what a call does, inbound or outbound: IVR menu, voicemail, dial, conference, collect payment.
- not for: twilio-voice-outbound-calls (starts the call); twilio-voice-conversation-relay (AI instead of scripted); twilio-call-recordings (two-party recording).
- needs: voice-capable number, webhook returning text/xml, SDK; for <Pay>, a Console-only Pay Connector and dedicated subaccount.
- side effects: PCI Mode, if enabled for <Pay>, is irreversible and account-wide.
- part of: shared step for inbound and outbound voice; Level 1 of twilio-customer-support-architect. Respond within 15 s; no ngrok in production.

### twilio-voice-outbound-calls
- id: twilio-developer-kit:twilio-voice-outbound-calls (source path: plugins/twilio-developer-kit/skills/twilio-voice-outbound-calls/SKILL.md)
- description: "Make outbound phone calls via Twilio's Programmable Voice REST API. Covers the full voice platform: calls.create(), answering machine detection (AMD), conference-based agent bridging, call recording, status tracking, and SIP Trunking. Use this skill for outbound calls, sales dialers, or when asking what voice APIs are available."
- use when: Place outbound calls by REST: sales dialer, answering-machine detection, agent bridging via conference, call status tracking.
- not for: twilio-voice-twiml (what the call does once answered); twilio-voice-conversation-relay (AI variant).
- needs: voice-capable number, credentials, SDK; trial can call only verified numbers.
- side effects: places real, billable, irreversible calls. Gate: confirm recipient number and intent with the user first; TCPA consent and quiet hours apply.
- part of: standalone; hands to twilio-voice-twiml, twilio-voice-conversation-relay, twilio-numbers-senders. AMD cannot be used with SIP Trunking.

### twilio-voice-conversation-relay
- id: twilio-developer-kit:twilio-voice-conversation-relay (source path: plugins/twilio-developer-kit/skills/twilio-voice-conversation-relay/SKILL.md)
- description: "Build AI-powered voice agents using Twilio ConversationRelay. Handles real-time speech recognition (ASR), text-to-speech (TTS), and bidirectional audio streaming via WebSocket. Covers TwiML setup, WebSocket message types, LLM integration, streaming responses, and voice provider configuration. Use this skill to build voice bots, IVR replacements, or real-time AI voice assistants on Twilio calls."
- use when: Build an AI voice agent or voice bot on a phone call: speech in, my LLM, speech out, over a WebSocket; replace an IVR.
- not for: twilio-agent-connect (SDK middleware over the same path); twilio-voice-twiml (non-AI IVR); twilio-ai-agent-architect (planning).
- needs: upgraded account with ConversationRelay onboarding approved, voice number, wss:// server, your own LLM and TTS/ASR choice.
- side effects: processes caller speech through ASR and the developer's LLM and speaks responses on billable calls; can end a call. Call placement is handed to twilio-voice-outbound-calls.
- part of: manual path of twilio-ai-agent-architect Level 1; used by twilio-taskrouter-routing for escalation. ConversationRelay supplies transport, not an LLM, memory or content safety; the skill shows BYO-LLM integration. Despite the description's "audio streaming", the app-facing WebSocket is text-only, with no raw audio access. Cannot mix with Media Streams.

### twilio-call-recordings
- id: twilio-developer-kit:twilio-call-recordings (source path: plugins/twilio-developer-kit/skills/twilio-call-recordings/SKILL.md)
- description: "Record Twilio voice calls correctly. Covers the critical distinction between Record verb (voicemail) and Dial record (call recording), dual-channel for QA, mid-call pause for PCI, Conference recording, and the ConversationRelay workaround. Use this skill whenever you need to capture call audio for compliance, QA, or analytics."
- use when: Record both sides of a call, separate agent and caller audio for QA, pause during payment, or fix a missing ConversationRelay recording.
- not for: twilio-conference-calls (multi-party control); conversation-intelligence (analysis, not capture).
- needs: voice number, credentials, SDK, recording callback, consent review.
- side effects: stores sensitive audio; deletion is permanent. Never record card numbers; use <Pay>.
- part of: standalone; augmentation Level 1 and support Level 3 step. <Record> is voicemail; use <Dial record> for both parties.

### twilio-conference-calls
- id: twilio-developer-kit:twilio-conference-calls (source path: plugins/twilio-developer-kit/skills/twilio-conference-calls/SKILL.md)
- description: "Build multi-party calls using Twilio Conference. Covers warm transfer, cold transfer, coaching (whisper), hold vs mute, participant modes, and supervisor barge. Use this skill for any contact center, support line, or scenario requiring transfers, holds, or multi-party calls."
- use when: Warm-transfer a caller, hold them while agents talk, or let a supervisor whisper or barge into a support call.
- not for: twilio-taskrouter-routing (picks the agent); twilio-call-recordings (audio capture).
- needs: voice number, credentials, SDK, callback endpoints.
- side effects: starts billable outbound legs, alters live calls, can disconnect everyone.
- part of: support-architect Level 3 implementation step. Start transferable calls as a Conference. Coach audio is excluded from recordings.

### twilio-taskrouter-routing
- id: twilio-developer-kit:twilio-taskrouter-routing (source path: plugins/twilio-developer-kit/skills/twilio-taskrouter-routing/SKILL.md)
- description: "Route tasks to agents using Twilio TaskRouter. Covers Workers, Task Queues, Workflows, Reservations, skills-based routing, and common gotchas (hyphen attributes, HAS operator, reservation cascade). Use this skill for any multi-agent contact center, support queue, or AI agent escalation routing."
- use when: Build a support queue with skills-based agent routing, or route an AI agent's escalation to a human.
- not for: twilio-voice-twiml (IVR before routing); twilio-conference-calls (transfers); twilio-voice-conversation-relay (the AI front end).
- needs: credentials, public assignment-callback URL (5 s response); a webhook-configured number for voice.
- side effects: creates Workspace resources; multiTaskEnabled is irreversible.
- part of: standalone; Level 3/4 step of the support and AI planners. Always include a default_filter; attribute names cannot contain hyphens.

### twilio-agent-connect
- id: twilio-developer-kit:twilio-agent-connect (source path: plugins/twilio-developer-kit/skills/twilio-agent-connect/SKILL.md)
- description: "Use when building or integrating Twilio Agent Connect (TAC) to connect third-party LLM agent runtimes with Twilio Voice, Messaging, ConversationRelay, Conversation Memory, Conversation Orchestrator, or Enterprise Knowledge."
- use when: Connect my existing OpenAI, Bedrock or Foundry agent to Twilio voice, SMS or WhatsApp with one callback and customer context.
- not for: twilio-voice-conversation-relay (manual protocol path); twilio-conversation-orchestrator (capture only).
- needs: Python 3.10+ or Node 22.13+, twilio >=9.8.3, SDK from GitHub (TypeScript built locally), credentials, public voice domain, LLM credentials.
- side effects: setup wizard creates a Memory Store, configuration and credential-bearing .env; custom tools can send messages or place calls.
- part of: implementation step of twilio-ai-agent-architect fast path. Middleware, not an agent runtime; the aws/microsoft packages are described inside, not separate skills.

### twilio-customer-memory
- id: twilio-developer-kit:twilio-customer-memory (source path: plugins/twilio-developer-kit/skills/twilio-customer-memory/SKILL.md)
- description: "Store and retrieve customer context using Twilio Conversation Memory. Covers Memory Store provisioning, profile management, traits, observations, conversation summaries, and semantic Recall. Use this skill to give AI agents or human agents persistent memory of customer interactions across sessions and channels."
- use when: Recognize a returning caller and remember their issues and preferences, or retrieve relevant history before answering.
- not for: twilio-enterprise-knowledge (shared company content); twilio-conversation-orchestrator (capture and lifecycle).
- needs: Conversation Memory enabled, Twilio credentials, raw JSON HTTP; max 15 stores per account.
- side effects: stores personal data in Twilio; profile deletion is irreversible.
- part of: Level 2 of twilio-ai-agent-architect, Level 3 of augmentation. Create the Memory Store before an Orchestrator Configuration. Its /v1/Services examples differ from sibling /v1/ControlPlane/Stores: have the user confirm the store-creation path in current Twilio docs before running either.

### twilio-conversation-orchestrator
- id: twilio-developer-kit:twilio-conversation-orchestrator (source path: plugins/twilio-developer-kit/skills/twilio-conversation-orchestrator/SKILL.md)
- description: "Configure automatic conversation capture and routing with Twilio Conversation Orchestrator. Covers Configuration creation, channel capture rules, grouping types, status timeouts, Memory Store linkage, Intelligence linkage, and conversation lifecycle. Use this skill to automatically capture SMS, voice, WhatsApp, RCS, and web chat traffic into unified conversations without manually creating conversations or participants."
- use when: Capture existing calls and messages automatically into unified customer conversations, grouped across channels, linked to memory and analysis.
- not for: twilio-conversations-classic-api (manual v1 threads); twilio-agent-connect (runtime middleware); twilio-customer-memory (persistence).
- needs: existing Memory Store, credentials, JSON HTTP, traffic sources.
- side effects: captures customer data, provisions transcription, runs paid operators, can close conversations.
- part of: foundation step after Memory Store, beneath conversation-intelligence. Use active TwiML or passive VOICE capture for the same traffic, not both. TwiML attribute is conversationConfiguration; a misspelling is silently ignored.

### conversation-intelligence
- id: twilio-developer-kit:twilio-conversation-intelligence (source path: plugins/twilio-developer-kit/skills/twilio-conversation-intelligence/SKILL.md)
- description: "Twilio Conversation Intelligence development guide. Use when building real-time or post-call conversation analysis, language operator pipelines, sentiment analysis, agent assist, cross-channel analytics, or querying aggregated conversation insights (sentiment trends, escalation rates, dashboards)."
- use when: Summarize or score completed conversations, suggest responses or detect escalation live, or chart sentiment across conversations.
- not for: twilio-conversation-orchestrator (capture); twilio-customer-memory (context); Voice Intelligence v2 (raw recordings, not a skill here).
- needs: credentials, Memory Store, Orchestrator capture, webhook destination; operators bill by characters.
- side effects: downstream webhook actions can mutate other systems. Not PCI or HIPAA eligible: no payment data or PHI.
- part of: Level 3 of twilio-ai-agent-architect, Level 2 of augmentation. Cannot ingest standalone. Directory twilio-conversation-intelligence; frontmatter name conversation-intelligence; siblings use the directory name.

### twilio-enterprise-knowledge
- id: twilio-developer-kit:twilio-enterprise-knowledge (source path: plugins/twilio-developer-kit/skills/twilio-enterprise-knowledge/SKILL.md)
- description: "Add knowledge retrieval to AI agents using Twilio's Enterprise Knowledge product. Enterprise Knowledge is a centralized, searchable repository of your organization's documents, websites, and content — FAQs, support policies, warranty terms, product catalogs. Current models don't have access to how you run your business today. Enterprise Knowledge gives agents a way to query this repository during a conversation and ground their responses in your actual approved source material. This skill covers provisioning a Knowledge Base and uploading knowledge sources from web URLs, PDFs, and raw text, and running semantic search to retrieve relevant chunks at runtime. Enterprise Knowledge is shared across your organization — it captures what your organization knows and how it is meant to run. It is distinct from Conversation Memory (twilio-customer-memory), which is scoped to individual end-customers and captures what you know about a specific person. The two are designed to be combined: enterprise content for business practices, customer memory for personalization."
- use when: Ground a support bot in current company policies, manuals, product catalogs or approved call scripts.
- not for: twilio-customer-memory (per-person memory); conversation-intelligence (operators on conversations).
- needs: Enterprise Knowledge enabled, credentials, approved URLs or PDF/CSV/Markdown files.
- side effects: uploads organizational content; may crawl sites periodically.
- part of: standalone enrichment for AI agents and Intelligence. Order: create KB, wait ACTIVE, add source, wait COMPLETED, search. Do not store customer-specific data in it.

### twilio-debugging-observability
- id: twilio-developer-kit:twilio-debugging-observability (source path: plugins/twilio-developer-kit/skills/twilio-debugging-observability/SKILL.md)
- description: "Debug Twilio integrations and set up production observability. Covers the Console Debugger, Monitor Alerts API, Event Streams for error log streaming, status callback tracking, common error codes, and a systematic debugging workflow. Use this skill whenever a Twilio integration produces errors, messages fail to deliver, calls drop unexpectedly, or you need to set up monitoring for a production deployment."
- use when: SMS failed, calls drop, webhook error 11200, who changed this setting, or set up production monitoring.
- not for: twilio-cli-reference (command syntax); twilio-messaging-webhooks (handlers); twilio-compliance-onboarding (registration fixes found by triage).
- needs: credentials, affected SID, error and time range; Console access.
- side effects: reads account and audit data; sink setup creates event delivery; test sends generate traffic.
- part of: standalone triage entry; mandatory companion in AI and augmentation recommendations. Order: status callbacks, REST state, sender reputation, Debugger, webhook reachability, Monitor/Event Streams.

### twilio-webhook-architecture
- id: twilio-developer-kit:twilio-webhook-architecture (source path: plugins/twilio-developer-kit/skills/twilio-webhook-architecture/SKILL.md)
- description: "Design, secure, and operate Twilio webhook endpoints. Covers inbound event handling, status callbacks, signature validation, connection overrides for retry and timeout tuning, local development tunneling, and production hardening. Use this skill whenever an agent needs to receive HTTP callbacks from Twilio for any product -- messaging, voice, verify, or event streams."
- use when: Receive HTTP callbacks from any Twilio product: signature validation, retry and timeout tuning, local tunnels, Event Streams sink.
- not for: twilio-messaging-webhooks (message-specific); twilio-sendgrid-webhooks (different ECDSA signing); twilio-reliability-patterns (load).
- needs: credentials, HTTPS endpoint (ngrok for dev), SDK.
- side effects: updates live messaging/voice webhook URLs, creates Event Streams sinks/subscriptions, and includes billable sends, calls and automatic SMS replies.
- part of: cross-product reference; hands to twilio-messaging-webhooks, twilio-voice-twiml, twilio-debugging-observability. Always use the SDK validator. 15 s voice ceiling.

### twilio-reliability-patterns
- id: twilio-developer-kit:twilio-reliability-patterns (source path: plugins/twilio-developer-kit/skills/twilio-reliability-patterns/SKILL.md)
- description: "Handle rate limits, retries, and failures when building on Twilio at scale. Covers 429 exponential backoff with jitter, per-number throughput limits, StatusCallback resilience, thin-receiver pattern, and fallback chains. Use this skill whenever sending messages or making calls at volume, or when building production-grade Twilio integrations."
- use when: Sending messages or placing calls at volume: 429 errors, callback overload, fallback chains, production readiness.
- not for: twilio-webhook-architecture (callback security); twilio-security-hardening (fraud, credentials).
- needs: a working integration, expected volume, callback URLs, a queue stack.
- side effects: none; advice with code.
- part of: guardrail applied after any send or voice skill. Backoff with jitter, thin-receiver idempotency, voice concurrency. Cannot raise per-number throughput.

### twilio-cli-reference
- id: twilio-developer-kit:twilio-cli-reference (source path: plugins/twilio-developer-kit/skills/twilio-cli-reference/SKILL.md)
- description: "Twilio CLI reference for managing Twilio resources from the terminal. Covers installation, credential profiles, phone number provisioning, sending SMS and email, webhook configuration, local development with a tunneling service, debugging with watch and logs, serverless deployment, and plugin ecosystem. Use when the developer asks to "just do it", "set this up", "run a command", mentions "CLI", "command line", or "terminal", or when an AI agent can execute a task directly instead of writing application code."
- use when: Run the Twilio command, buy or configure a number from the terminal, or deploy a Twilio Function instead of writing code.
- not for: twilio-account-setup (signup); product skills (application integration); twilio-debugging-observability (diagnosis).
- needs: installed Twilio CLI and authenticated profile; SENDGRID_API_KEY for email; optional plugins and a separate tunnel.
- side effects: commands can buy numbers, send real SMS/email, change webhook URLs, deploy Functions; the source declares no per-command approval, so advise confirming each such command with the user first.
- part of: standalone operational alternative to SDK code. twilio email:send uses SendGrid, never Twilio Email. Avoid auth token as a shell argument.
