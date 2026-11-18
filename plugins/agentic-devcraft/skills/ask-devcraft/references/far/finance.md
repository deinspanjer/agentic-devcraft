# openai/plugins far from development: finance
Source: https://github.com/openai/plugins @ d420d13051bffe4543ed39e30fa46b87148e47dd
Distribution (openai/plugins): the Codex plugin marketplace `openai-curated` (`.agents/plugins/marketplace.json`); a plugin installs in Codex by name. Skill directories are `plugins/<plugin>/skills/<skill>/`. A "Codex-only" manifest note describes packaging, not where a skill can run: the skill's own `needs` line says what depends on Codex.
Curated records of remote catalog entries, not proof of installation: check at runtime that a skill is available in the current host and read its current SKILL.md before relying on any detail below.

Families far from software development, kept out of the catalogs. Pointers to this file are in openai-platforms.md. Families here: `public-equity-investing`.

## Family: public-equity-investing
- source path: `plugins/public-equity-investing` (plugin v0.1.31, proprietary licence). 23 skills: 1 router, 21 specialists, 1 setup skill. The plugin's own manifest names `openai/oai-maintained-plugins` as repository/homepage; the inspected copy is in openai/plugins.
- manifest notes: Codex manifest only (`.codex-plugin/plugin.json`); no Claude or Cursor manifest, no MCP server, hooks, commands or rules. `.app.json` declares 15 optional app connectors (Slack, PitchBook, FactSet, Morningstar, LSEG, S&P, Third Bridge, Daloopa, Quartr, Alpaca, Google Drive, Gmail, Outlook Email, SharePoint, Teams) by ID only; none is mandatory, and the declaration is not proof of installation, entitlement or access. The repo marketplace lists it as AVAILABLE / ON_USE. Only the router allows implicit invocation; the other 22 set `allow_implicit_invocation: false`. Uses Codex-style `agents/openai.yaml`, `request_user_input` and `request_plugin_install` with plain-chat fallbacks; HTML QA needs a local headless browser (not an in-app browser plugin). Python helpers and bundled XLSX templates; outputs are research, models and drafts, never trade execution or personal advice. Entry gate: explicit invocation or unmistakable listed-equity investor context; a bare ticker, earnings summary, model or document request does not activate it. Credit, private-company diligence, FP&A and banker work route out (sibling Credit Markets and other plugins, not inspected).
- router: `public-equity-investing` covers all 22 other skills. Sequence: invocation gate -> choose one lead owner and read that skill -> resolve missing artifact package/format/depth/audience with at most three questions before any source gathering -> resolve only needed source categories -> use support only for assigned workstreams (normalize financials before models, audit models, QC before circulation) -> first investor-facing artifact. Router-listed `test-public-equity-investing-workflows` is not shipped as a skill here; do not recommend it.
- development distance: far (listed-equity investment research, financial models, memos).
- disclosure: router-delegated; one router owns a gated routing map for all 22 specialists, so records stay one-liners for matching.
- settled conflicts: formal memos recommend real DOCX (`memo-builder`) even though the router's playbook says HTML; a focused sourced event overlay goes to `scenario-sensitivity-generator` while full event underwriting goes to `event-driven-analyzer`.

### catalyst-calendar
- id: public-equity-investing:catalyst-calendar (source path: plugins/public-equity-investing/skills/catalyst-calendar/SKILL.md)
- description: "Use when building public-equity-investing catalyst calendars. Do not use for full event underwriting; use event-driven-analyzer."
- use when: "What can change my view on this stock over the next 90 days, and when?": a dated or windowed catalyst register or tracker for one name, a portfolio or a sector.
- not for: event-driven-analyzer (computes payoff and probability for one event); thesis-tracker (enduring thesis evidence, not dates); earnings-preview (one upcoming print).
- side effects: writes local HTML/XLSX/optional ICS files only; not a live calendar integration. ICS only for confirmed exact dates
- part of: standalone; reached through the router or by naming it (implicit invocation is off); feeds event-driven-analyzer, earnings skills, thesis-tracker, portfolio-risk-management

### company-tearsheet
- id: public-equity-investing:company-tearsheet (source path: plugins/public-equity-investing/skills/company-tearsheet/SKILL.md)
- description: "Use when creating source-backed public issuer tearsheets. Do not use for private diligence, fund diligence, vendors, or market maps."
- use when: "Give me a sourced baseline on this listed company before I decide whether to dig in": identity, drivers, key metrics, gaps, no recommendation.
- not for: initiating-coverage (full thesis and target); idea-generation (ranks many names); meeting-prep (conversation plan).
- part of: standalone; reached through the router or by naming it (implicit invocation is off); often the early baseline step before comps, DCF, earnings, initiation or memo work

### comps-valuation
- id: public-equity-investing:comps-valuation (source path: plugins/public-equity-investing/skills/comps-valuation/SKILL.md)
- description: "Produce Public Equity Investing comparable-company valuation in report or workbook mode. Use for peer selection, multiple analysis, valuation read-throughs, implied prices, comps dashboards, Excel or Sheets comps, refreshable peer tables, model updates, and comps workbook QA. Do not use for DCF-only, credit-security, or generic market commentary requests."
- use when: "Is this stock's premium to peers justified?" or "build or update a trading-comps workbook"; report mode or workbook mode (a supplied workbook selects workbook mode when the request changes or validates it).
- not for: dcf-model-builder (cash-flow valuation, not peer multiples); company-tearsheet (facts, no valuation); model-audit-tieout (standalone workbook review).
- part of: standalone; reached through the router or by naming it (implicit invocation is off); valuation step inside initiation, pitch, memo; hands to model-audit-tieout, then deck-report-qc before circulation

### dcf-model-builder
- id: public-equity-investing:dcf-model-builder (source path: plugins/public-equity-investing/skills/dcf-model-builder/SKILL.md)
- description: "Use when building public-equity DCF valuation workbooks. Default to the banker formula workbook path for new model builds; use deterministic exports only for controlled support calculations or explicit lightweight runs. Do not use for standalone workbook audits; use model-audit-tieout."
- use when: "Build or re-run a public-company DCF, reverse DCF or WACC/terminal-value sensitivity" as an Excel model.
- not for: three-statement-model-builder (integrated operating forecast); comps-valuation (peer multiples); equity-model-update (existing model); model-audit-tieout (review only).
- needs: valid plan JSON, sourced inputs, Python 3, bundled workbook template; formula mode is only claimable if its checks pass, else a labeled deterministic export
- part of: standalone; reached through the router or by naming it (implicit invocation is off); follows financials-normalizer, precedes model-audit-tieout; hands stress grids to scenario-sensitivity-generator

### deck-report-qc
- id: public-equity-investing:deck-report-qc (source path: plugins/public-equity-investing/skills/deck-report-qc/SKILL.md)
- description: "Use when running first-pass QC on Public Equity Investing decks or reports. Do not use as external-circulation certification."
- use when: "Check this equity deck or report and its model before it goes to the PM or client": issue log and circulation verdict.
- not for: model-audit-tieout (workbook mechanics and assumptions; this skill checks communicated figures and narrative).
- side effects: writes a separate QC report and support files; preserves reviewed artifacts (edits only if asked); it does not certify external circulation
- part of: standalone; reached through the router or by naming it (implicit invocation is off); final step before circulation of memo, initiation or pitch; sends model defects to model-audit-tieout

### earnings-deep-dive
- id: public-equity-investing:earnings-deep-dive (source path: plugins/public-equity-investing/skills/earnings-deep-dive/SKILL.md)
- description: "Use when analyzing public-company earnings after results, guidance, transcript, or call commentary. Do not use for pre-print previews."
- use when: "The company has reported: did the quarter change the thesis, estimates or valuation?": post-print beat/miss, guidance delta, EPS quality, transcript debate, read-throughs.
- not for: earnings-preview (before the print); equity-model-update (changes the model cells); thesis-tracker (longitudinal pillars).
- part of: step after earnings-preview, or standalone after results; one of three onboarding hero workflows; hands to equity-model-update, scenarios, risk, thesis-tracker, memo-builder

### earnings-preview
- id: public-equity-investing:earnings-preview (source path: plugins/public-equity-investing/skills/earnings-preview/SKILL.md)
- description: "Use when preparing full pre-earnings preview reports with executive summary, expectation bar, guidance credibility, KPI dashboard, scenarios, and call questions. Do not use after results or for short summaries unless the user explicitly asks for a summary/short version."
- use when: "Before this stock reports, what must it deliver, what could move the shares, what should we ask?": full pre-print report with expectation bar, KPIs, cases.
- not for: earnings-deep-dive (after results); meeting-prep (conversation only); catalyst-calendar (multi-event dates).
- needs: optional deterministic pack needs several CSV inputs and Python deps (pandas, numpy, openpyxl, PyYAML, python-dateutil)
- part of: standalone pre-print entry point; hands to earnings-deep-dive after results, equity-model-update, long-short-pitch, memo-builder

### economic-impact-report
- id: public-equity-investing:economic-impact-report (source path: plugins/public-equity-investing/skills/economic-impact-report/SKILL.md)
- description: "Use when translating a specific event, policy change, macro shock, or industry development into public-equity issuer, sector, earnings, valuation, positioning, and portfolio implications. Do not use for standalone macro strategy, rates, FX, credit, futures, or generic market commentary."
- use when: "This tariff, policy change or commodity shock happened: how does it hit listed issuers and our equity exposures?": event-to-equity transmission report.
- not for: event-driven-analyzer (dated payoff for one security event); idea-generation (ranks candidates afterward); portfolio-risk-management (sizes or hedges); not a macro, rates, FX or credit service.
- part of: standalone entry point for shock analysis; hands to idea-generation, company-tearsheet, model owners, portfolio-risk-management

### equity-model-update
- id: public-equity-investing:equity-model-update (source path: plugins/public-equity-investing/skills/equity-model-update/SKILL.md)
- description: "Safely update public-company Excel model copies from source-to-model maps; emits XLSX as the hero artifact and CSV/log/manifest as support. Do not use for pure earnings notes or broad workbook audits."
- use when: "Flow the latest actuals, guidance and KPIs into my existing public-company model and show what changed".
- not for: earnings-deep-dive (interprets, does not edit); dcf-model-builder and three-statement-model-builder (new architecture); model-audit-tieout (review only).
- needs: sourced inputs mapped to model lines; copied-workbook updates additionally need an existing workbook and safe sheet/cell mappings; without a workbook, supports a mapping/log export
- side effects: writes a copied workbook or control pack; never mutates the original or overwrites formula cells
- part of: step inside the post-earnings or valuation workflow, or standalone; normalization first, model-audit-tieout after; rebuilds go to DCF, three-statement or comps skills

### event-driven-analyzer
- id: public-equity-investing:event-driven-analyzer (source path: plugins/public-equity-investing/skills/event-driven-analyzer/SKILL.md)
- description: "Use when analyzing dated public-equity event paths, probabilities, payoffs, and expected returns. Do not use for generic catalyst lists, risk sizing, hedges, capital structure, covenants, or credit recovery."
- use when: "Underwrite this merger, spin, tender or regulatory decision": conditions, timing, scenarios, payoff, probabilities, expected return.
- not for: catalyst-calendar (dates only); scenario-sensitivity-generator (bounded overlay when terms are known); portfolio-risk-management (sizing and hedges); credit recovery routes out.
- needs: primary deal or regulator documents and timestamped pricing; Python helper for the math
- part of: standalone event-underwriting entry point; feeds long-short-pitch, scenario-sensitivity-generator, portfolio-risk-management, thesis-tracker

### financials-normalizer
- id: public-equity-investing:financials-normalizer (source path: plugins/public-equity-investing/skills/financials-normalizer/SKILL.md)
- description: "Use when normalizing public-company financials from source materials. Do not use for private data rooms or non-financial cleanup."
- use when: "Turn these inconsistent filings, KPI disclosures or segment tables into schedules I can safely load into a model".
- not for: equity-model-update (applies values to a model); model-audit-tieout (checks integrity).
- part of: step before models, comps, earnings and trackers; standalone only when normalization is the job

### idea-generation
- id: public-equity-investing:idea-generation (source path: plugins/public-equity-investing/skills/idea-generation/SKILL.md)
- description: "Use when triaging public-equity idea candidates. Do not use for final trade recommendations, pitches, memos, or models."
- use when: "Screen this universe, theme or watchlist: which names deserve deeper work and which are false positives?": ranked research-priority funnel.
- not for: company-tearsheet (one issuer); initiating-coverage (full view on one name); long-short-pitch (trade expression).
- part of: entry point of a research sequence and one of three onboarding hero workflows; hands names to tearsheet, earnings, valuation, pitch, event or risk skills

### initiating-coverage
- id: public-equity-investing:initiating-coverage (source path: plugins/public-equity-investing/skills/initiating-coverage/SKILL.md)
- description: "Use when building public-equity-investing initiating coverage reports. Do not use for trade pitches, memos, earnings notes, models, or tearsheets."
- use when: "Launch coverage on this listed company": thesis, forecasts, target-price framework, industry position, catalysts and risks as a full report.
- not for: company-tearsheet (baseline only); memo-builder (formal written synthesis); long-short-pitch (expression and action rules).
- part of: entry point coordinating baseline -> normalization -> models, comps, scenarios, catalysts -> synthesis and QA; hands to thesis-tracker, earnings skills, equity-model-update, long-short-pitch

### long-short-pitch
- id: public-equity-investing:long-short-pitch (source path: plugins/public-equity-investing/skills/long-short-pitch/SKILL.md)
- description: "Use when building PM-facing Public Equity Investing trade pitches, including sparse-context or partial-section requests. Do not use for formal memos; use memo-builder."
- use when: "Pitch this long, short or pair": variant view, why now, expression, scenario skew, catalysts and add/cover/exit rules; a single requested section is allowed.
- not for: memo-builder (formal memo; it takes unresolved trade construction back here); portfolio-risk-management (binding size and hedge); event-driven-analyzer (deal or event payoff).
- needs: shorts need borrow and squeeze inputs; pairs need hedge ratio and liquidity
- side effects: writes local HTML pitches and optional scenario support files; proposed research, not trade execution or personal advice
- part of: entry point for trade construction and one of three onboarding hero workflows; hands to portfolio-risk-management, thesis-tracker, memo-builder

### meeting-prep
- id: public-equity-investing:meeting-prep (source path: plugins/public-equity-investing/skills/meeting-prep/SKILL.md)
- description: "Use when creating Public Equity Investing meeting prep briefs. Do not use for private diligence, IB, FP&A, legal, or scheduling-only tasks."
- use when: "Help me use this management, expert, sell-side or committee meeting to resolve a thesis question": must-ask questions and follow-up tracker.
- not for: earnings-preview (whole print setup); company-tearsheet (background). Scheduling-only tasks route out.
- needs: email, chat or calendar connectors only if callable and only optionally
- side effects: creates briefs and proposed/importable trackers; drafts follow-ups, sending only if explicitly instructed and allowed; direct production-record writes only on explicit request
- part of: standalone; reached through the router or by naming it (implicit invocation is off); step after tearsheet, earnings, thesis or event work; hands evidence back to model, memo or tracker skills

### memo-builder
- id: public-equity-investing:memo-builder (source path: plugins/public-equity-investing/skills/memo-builder/SKILL.md)
- description: "Use when drafting or reviewing formal public-equity investment memos. Do not use for live trade construction or credit-first memos; use long-short-pitch or Credit Markets as appropriate."
- use when: "Turn this equity research into an IC memo, client note or PM update", or rewrite or pressure-test one; formal circulation recommends real DOCX.
- not for: long-short-pitch (builds the trade view first); initiating-coverage (launches coverage); credit-first memos route to Credit Markets.
- part of: synthesis step in the research sequence; unresolved trade construction goes to long-short-pitch first, circulation to deck-report-qc

### model-audit-tieout
- id: public-equity-investing:model-audit-tieout (source path: plugins/public-equity-investing/skills/model-audit-tieout/SKILL.md)
- description: "Use when auditing existing Public Equity Investing models or spreadsheets. Do not use to build a new model from scratch."
- use when: "Can this existing equity model support the decision? Trace formulas, sources, assumptions and scenarios": verdict Ready / Ready with caveats / Not ready / Not assessable.
- not for: dcf-model-builder and three-statement-model-builder (build); equity-model-update (edits inputs); deck-report-qc (communicated claims).
- needs: workbook inspection helper requires openpyxl>=3.1; the skill instructs installation from local requirements in a fresh environment
- side effects: writes a separate audit report; diagnoses only, repairs only when asked
- part of: standalone; reached through the router or by naming it (implicit invocation is off); step after model build or update, before portfolio reliance or circulation; hands repairs to builders and presentation checks to deck-report-qc

### portfolio-risk-management
- id: public-equity-investing:portfolio-risk-management (source path: plugins/public-equity-investing/skills/portfolio-risk-management/SKILL.md)
- description: "Use when sizing Public Equity Investing positions, finding equity hedges, or building an integrated position-and-hedge risk plan from a listed-equity thesis. Do not use for thesis construction, standalone event underwriting, trade execution, personal investment advice, or credit-instrument risk."
- use when: "How big should the position be, what should we hedge, or is trimming better?": position_sizing, hedge_design or an integrated risk plan for a listed-equity thesis.
- not for: long-short-pitch (builds the thesis); event-driven-analyzer (event payoff); scenario-sensitivity-generator (assumption grids). Credit hedges route out.
- needs: size, price, constraints and implementation data; shorts need borrow, locate and exit capacity
- side effects: writes local HTML risk reports and calculation/audit support files; no trade execution or personal advice
- part of: step after long-short-pitch or an established earnings, event or model view, or standalone for an existing position; hands monitoring to thesis-tracker

### public-equity-investing
- id: public-equity-investing:public-equity-investing (source path: plugins/public-equity-investing/skills/public-equity-investing/SKILL.md)
- description: "Route Public Equity Investing workflows for listed-company and public-security research, earnings analysis, valuation, model updates, long/short pitches, catalysts, thesis tracking, ETF/index and constituent diligence, position sizing, hedging, dashboards, and investment memos. Use when the user is evaluating a public company, ticker, sector, portfolio position, event, earnings setup, or investment thesis through an investor lens, including what is priced in, what is mispriced, what proves or kills the thesis, and what to watch next. Do not use for private-company diligence, credit-first analysis, personal financial advice, generic company summaries, or generic document drafting with no public-equity investment context."
- use when: Broad or ambiguous investor request about a listed issuer, ticker, position, earnings setup, valuation, thesis, catalyst or PM artifact, where the right specialist must be chosen; it picks one lead owner, then hands off.
- needs: Codex-oriented harness (request_user_input and request_plugin_install, with plain-chat fallbacks); investor context, since a bare ticker or company question does not activate it. No vendor account required by the router itself.
- side effects: none by itself; read-only routing, and it asks before installing or authorizing any source
- part of: entry router for public-equity-investing and the only implicit skill; ordinary sequence: invocation gate -> pick one lead owner -> artifact intake (max three questions) -> source categories -> specialist work -> QC; hands off to every skill here and to user-context for explicit setup

### scenario-sensitivity-generator
- id: public-equity-investing:scenario-sensitivity-generator (source path: plugins/public-equity-investing/skills/scenario-sensitivity-generator/SKILL.md)
- description: "Use when turning a public-equity base case, model, thesis, event, or catalyst into scenario skew, sensitivity, breakpoint, and PM action-threshold analysis. Do not use for first-pass model builds, credit-security valuation, or generic planning."
- use when: "From this base case, what breaks at which assumptions, and what does today's price imply?": scenario skew, sensitivity matrices, breakpoints and action thresholds. A focused, sourced event overlay may start directly; full event underwriting stays with event-driven-analyzer.
- not for: dcf-model-builder and three-statement-model-builder (create the base); event-driven-analyzer (full event process); portfolio-risk-management (size or hedge).
- needs: a sourced base case/model or verified event terms and current price for decision-ready analysis; probability-weighted rows need complete probabilities summing to 100%; missing inputs permit labeled shells or illustrative outputs
- part of: step inside other workflows after DCF, three-statement, comps, earnings, event or thesis work; hands narrative to memo-builder or long-short-pitch, exposure to portfolio-risk-management

### thesis-tracker
- id: public-equity-investing:thesis-tracker (source path: plugins/public-equity-investing/skills/thesis-tracker/SKILL.md)
- description: "Use when building or updating Public Equity Investing thesis trackers. Do not use for generic news summaries, trade pitches, or first-pass memos."
- use when: "Update our thesis or watchlist after new evidence: which pillars changed and what is the next proof point?": append-only evidence and decision ledger, usually XLSX.
- not for: catalyst-calendar (dated events); earnings-deep-dive (explains one print); idea-generation (new names).
- needs: optional openpyxl for XLSX
- side effects: writes new CSV support and optional XLSX; helper does not edit existing trackers in place; no implicit scheduled monitoring or silent rewriting of the original thesis
- part of: monitoring step after initiation, pitch or risk adoption, or standalone refresh; hands model changes to equity-model-update and new hedges to portfolio-risk-management

### three-statement-model-builder
- id: public-equity-investing:three-statement-model-builder (source path: plugins/public-equity-investing/skills/three-statement-model-builder/SKILL.md)
- description: "Use when building public-equity three-statement operating model workbooks. Default to the banker formula workbook path for new model builds; use deterministic exports only for controlled support calculations or explicit lightweight runs. Do not use for standalone workbook audits."
- use when: "Build or rebuild an integrated public-company forecast": income statement, balance sheet, cash flow, working capital, PP&E and debt schedules in a formula-first workbook.
- not for: dcf-model-builder and comps-valuation (valuation); equity-model-update (existing model inputs); model-audit-tieout (review). Corporate budgets and LBO models route out.
- needs: valid plan JSON, normalized historicals, Python 3, bundled workbook template; formula mode only if its checks pass
- part of: standalone; reached through the router or by naming it (implicit invocation is off); step after financials-normalizer and before model-audit-tieout; valuation goes to dcf-model-builder

### user-context
- id: public-equity-investing:user-context (source path: plugins/public-equity-investing/skills/user-context/SKILL.md)
- description: "Initialize, inspect, save, update, forget, export, or explicitly reset the Public Equity Investing plugin's local user context, source setup, or optional automation setup. Use only when the user explicitly asks to manage Public Equity Investing saved preferences, source pointers, context storage, or recurring automation."
- use when: Explicit asks only: "remember my equity research defaults", "set up sources", "onboard me", "inspect, export or reset saved context", "schedule a recurring watchlist check".
- not for: thesis-tracker (stores thesis evidence, not user preferences). Not part of ordinary research.
- needs: Codex-oriented state under $CODEX_HOME/state/plugins/...; Python 3 helpers; automation needs automation_update, discovered with tool_search only if not already available
- side effects: writes local user-context.md and onboarding-state.json; may, after asking, install or authorize source plugins and create a weekday automation; reset backs up first
- part of: standalone setup; entry of a four-step onboarding (defaults -> connectors -> optional automation -> hero workflow); ends by handing off to earnings-deep-dive, long-short-pitch or idea-generation

# cursor/plugins far from development: finance
Source: https://github.com/cursor/plugins @ e559e62b729e040186bc9d573e71255e5a96f50d
Distribution (cursor/plugins): the Cursor marketplace `cursor-plugins` (`.cursor-plugin/marketplace.json`); in Cursor, `/add-plugin <plugin>`. The same repository holds a Claude Code marketplace (`.claude-plugin/marketplace.json`; `/plugin marketplace add cursor/plugins`) that lists only `pstack` and `origin-apps`. Skill directories are `<plugin>/skills/<skill>/`. A "Cursor packaging only" manifest note describes packaging, not where a skill can run: the family header names the Cursor features (Task subagents, hooks, Canvas, rules) a skill depends on.
Curated records of remote catalog entries, not proof of installation: check at runtime that a skill is available in the current host and read its current SKILL.md before relying on any detail below.

Families far from software development, kept out of the catalogs. Pointers to this file are in cursor.md. Families here: `x-money`.

## Family: x-money (cursor/plugins)
- source repo: https://github.com/cursor/plugins, path `third_party/x-money/`
- manifest: Marked `cursor: "never"` (Grok Bot and Sand only, 0.52.0+). Bundles MCP server `x-money` at `https://mcp.money.x.com/mcp`; connection is a code plus passkey approval in the X app. US-eligible accounts only. Directory is `x-money-guide`; host-visible name is `X Money guide`.
- router: none
- development distance: far (finance)
- disclosure recommendation: simple: one guide; far from development.

### X Money guide
- id: x-money:x-money-guide (source path: third_party/x-money/skills/x-money-guide/SKILL.md)
- description: "Read this before the first X Money action in a session and again on any X Money error, refusal, or missing capability. Covers the approval rule for every action that moves money (always ask, every time, no exceptions), how the connection works (connection code plus passkey in the X app), how to guide the user through connect, reconnect, and revoke at x.com/i/money/settings/connections, and what each failure message means."
- use when: Before the first X Money action in a session and on any X Money error or refusal.
- needs: an X Money account connected through Grok Bot; not usable in Cursor.
- side effects: sends real money, requests money, or creates a card to pay a merchant. Approve/Cancel prompt for each exact action; never retry a refusal, unconfirmed payment or limit result. Explicit exception: one retry of transient card-creation failure may reuse the same purchase approval. Balances and transactions are read-only.
