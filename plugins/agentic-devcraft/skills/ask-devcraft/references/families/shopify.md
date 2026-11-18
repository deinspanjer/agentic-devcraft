# openai/plugins family: shopify (Shopify)
Source: https://github.com/openai/plugins @ d420d13051bffe4543ed39e30fa46b87148e47dd
Distribution (openai/plugins): the Codex plugin marketplace `openai-curated` (`.agents/plugins/marketplace.json`); a plugin installs in Codex by name. Skill directories are `plugins/<plugin>/skills/<skill>/`. A "Codex-only" manifest note describes packaging, not where a skill can run: the skill's own `needs` line says what depends on Codex.
Curated records of remote catalog entries, not proof of installation: check at runtime that a skill is available in the current host and read its current SKILL.md before relying on any detail below.

Full records for the `shopify` family. The catalog entry is in openai-platforms.md.

## Family: shopify
- source path: `plugins/shopify` (Codex plugin v3.0.0, author Shopify). 20 skills.
- manifest notes: Codex manifest only (no Claude/Cursor manifest, hooks, commands or subagents). HTTP MCP server `shopify` at https://setup.shopify.com/mcp with an unfilled OAuth `client_id` placeholder (no bundled credentials) and an app connector; most skills ignore both and work through local scripts and the Shopify CLI. No plugin-wide install approval policy. Skill frontmatter `compatibility` varies: the two onboarding skills and shopify-app-store-review declare Claude Code/Desktop/Cursor; onboarding-dev has no Codex install path; ucp says "Requires UCP CLI"; the rest say "Requires Node.js". S1 (shared code-generation contract, 13 skills: admin, customer, partner, payments-apps, storefront-graphql, functions, hydrogen, liquid, the four polaris-*, pos-ui): needs Node.js and bash; every answer first runs the skill's `scripts/search_docs.mjs`, writes code, then runs `scripts/validate.mjs` (extension skills need an exact `--target`). All S1 records also have docs-search network calls and search/validation telemetry side effects to shopify.dev (queries, and on validation the generated code, file names, artifact ID); opt out with `OPT_OUT_INSTRUMENTATION=true`. The source says both "return code only after validation passes" and "after 3 failures return the best attempt": do not promise validated code; tell the user it may arrive unvalidated, with an explanation, after 3 failed attempts. Names referenced but absent (never recommend): storefront-web-components (no skill here covers it), shopify-admin-graphql (use shopify-admin), shopify-checkout-extensions (use shopify-polaris-checkout-extensions), `validate_graphql_codeblocks` (a tool no manifest supplies).
- router: none for the family. shopify-onboarding-dev is the entry for developer setup (detect client, check/install CLI, install AI toolkit, then hand off to the API skill); shopify-onboarding-merchant is the entry for store owners (CLI 3.93.0+, OAuth connect, menu, import); shopify-dev is a docs fallback "only when no API-specific skill applies". Precedence rules: metafield/metaobject prompts go to shopify-custom-data first; any Hydrogen mention stays in shopify-hydrogen (no tie-break for Hydrogen metafields); authoring GraphQL is shopify-admin, executing it or validating TOML is shopify-use-shopify-cli. UI surface: app's own pages -> shopify-polaris-app-home (also the default for a bare "Polaris"); existing Admin pages -> shopify-polaris-admin-extensions; checkout/thank-you -> shopify-polaris-checkout-extensions; customer accounts -> shopify-polaris-customer-account-extensions; retail -> shopify-pos-ui.
- development distance: core-dev (apps, themes, storefronts, Functions, extensions). Outliers: shopify-onboarding-merchant and ucp are merchant/shopper operations rather than development; both can write to live stores or place orders.
- disclosure: rich; no router, and the 20 skills cover different scenarios (store owner, API authoring, UI surfaces, backend Functions, CLI execution, shopper).

### shopify-admin
- id: shopify:shopify-admin (source path: plugins/shopify/skills/shopify-admin/SKILL.md)
- description: "Write or explain **Admin GraphQL** queries and mutations for apps and integrations that extend the Shopify admin. Use when the user wants to **understand, design, or generate** the operation itself—even before deciding how to run it. Do **not** choose `admin` first for **app or extension config validation** —use **`use-shopify-cli`**. Do **not** choose `admin` first to **execute** Admin GraphQL **now via Shopify CLI** or for CLI setup/troubleshooting on store workflows—use **`use-shopify-cli`** (store auth/execute, handle/SKU/location lookups, inventory changes)."
- use when: Write or explain an Admin GraphQL query/mutation ("write the mutation to create a product", "explain this query") before deciding how to run it.
- not for: shopify-use-shopify-cli (run it against a store now, validate TOML, SKU/location lookups); shopify-customer (a signed-in buyer's own data); shopify-custom-data (metafield/metaobject modeling comes first).
- needs: Node.js, bash; shared search-then-validate scripts (family note S1). No store credentials just to author.
- side effects: writes local code; docs-search and telemetry calls to shopify.dev.
- part of: standalone; destination of shopify-onboarding-dev; hands execution to shopify-use-shopify-cli.

### shopify-app-store-review
- id: shopify:shopify-app-store-review (source path: plugins/shopify/skills/shopify-app-store-review/SKILL.md)
- description: "Run a pre-submission compliance check against your Shopify app's codebase. Reviews App Store requirements and surfaces likely issues before you submit for official review."
- use when: "Check my Shopify app against App Store requirements before I submit": checks the code-checkable subset, likely pass/fail/needs-review/skipped.
- not for: shopify-use-shopify-cli (config schema validation only). Official review still follows; nothing is submitted.
- needs: local app codebase; web fetch of the live requirements page (fetched every run). Declares Claude Code, Claude Desktop, Cursor.
- side effects: none; read-only review.
- part of: standalone pre-submission checkpoint.

### shopify-custom-data
- id: shopify:shopify-custom-data (source path: plugins/shopify/skills/shopify-custom-data/SKILL.md)
- description: "MUST be used first when prompts mention Metafields or Metaobjects. Use Metafields and Metaobjects to model and store custom data for your app. Metafields extend built-in Shopify data types like products or customers, Metaobjects are custom data types that can be used to store bespoke data structures. Metafield and Metaobject definitions provide a schema and configuration for values to follow."
- use when: Add app-owned custom fields or structured content (product care instructions, author records); any prompt mentioning metafields or metaobjects.
- not for: shopify-admin (general queries; this decides schema/ownership first). For Hydrogen metafield work run this first (its description: "MUST be used first" for metafields) for the data model, then shopify-hydrogen for storefront code.
- needs: Node.js; shopify.app.toml, owner IDs/types; Shopify CLI for scaffolding; Admin API context to write values.
- side effects: writes local TOML/code; CLI scaffolding (command list includes deploy). Stops at implementation guidance.
- part of: entry for the custom-data flow (definitions, then writes, then reads); hands CLI trouble to shopify-use-shopify-cli.

### shopify-customer
- id: shopify:shopify-customer (source path: plugins/shopify/skills/shopify-customer/SKILL.md)
- description: "The Customer Account API allows customers to access their own data including orders, payment methods, and addresses."
- use when: Build a signed-in customer's order history, address editing, payment-method management or profile preferences with the Customer Account API.
- not for: shopify-admin (merchant-wide customer data); shopify-polaris-customer-account-extensions (UI inside hosted account pages); shopify-hydrogen (Hydrogen integration).
- needs: Node.js, bash; shared search-then-validate scripts (family note S1); customer authentication to execute (customers see only their own records).
- side effects: writes local code; payment-method examples carry PCI/privacy duties.
- part of: standalone.

### shopify-dev
- id: shopify:shopify-dev (source path: plugins/shopify/skills/shopify-dev/SKILL.md)
- description: "Search Shopify developer documentation across all APIs. Use only when no API-specific skill applies."
- use when: A Shopify developer question spans APIs or has no matching specialist: search the docs and answer.
- not for: every API- or surface-specific shopify-* skill supersedes it when one applies.
- needs: Node.js, shell, network; bundled docs-search script (telemetry; opt out OPT_OUT_INSTRUMENTATION=true). No validator.
- side effects: docs-search network calls and query/response telemetry to shopify.dev; no store writes.
- part of: standalone fallback, not a router. Its examples name skills absent here (shopify-admin-graphql, shopify-checkout-extensions).

### shopify-functions
- id: shopify:shopify-functions (source path: plugins/shopify/skills/shopify-functions/SKILL.md)
- description: "Shopify Functions allow developers to customize the backend logic that powers parts of Shopify. Available APIs: Discount, Cart and Checkout Validation, Cart Transform, Pickup Point Delivery Option Generator, Delivery Customization, Fulfillment Constraints, Local Pickup Delivery Option Generator, Order Routing Location Rule, Payment Customization"
- use when: Implement a discount rule, cart/checkout validation, cart transform, payment or delivery customization, or fulfillment/order-routing logic that runs inside Shopify.
- not for: shopify-polaris-checkout-extensions (checkout UI, not backend rules); shopify-payments-apps (provider integration, not payment-method ordering).
- needs: Node.js, bash; shared search-then-validate scripts (family note S1); Shopify app and CLI; Rust by default, JS/TS on request.
- side effects: writes local function code and tests; never runs `shopify app deploy`.
- part of: standalone; destination of shopify-onboarding-dev; hands tooling to shopify-use-shopify-cli.

### shopify-hydrogen
- id: shopify:shopify-hydrogen (source path: plugins/shopify/skills/shopify-hydrogen/SKILL.md)
- description: "Hydrogen storefront implementation cookbooks. Some of the available recipes are: B2B Commerce, Bundles, Combined Listings, Custom Cart Method, Dynamic Content with Metaobjects, Express Server, Google Tag Manager Integration, Infinite Scroll, Legacy Customer Account Flow, Markets, Partytown + Google Tag Manager, Subscriptions, Third-party API Queries and Caching. MANDATORY: Use this API for ANY Hydrogen storefront question - do NOT use Storefront GraphQL when 'Hydrogen' is mentioned."
- use when: Add a feature to a Hydrogen storefront (B2B, subscriptions, bundles, cart, markets, metaobject content, analytics, infinite scroll, cached third-party data).
- not for: shopify-storefront-graphql (framework-free GraphQL; any Hydrogen mention stays here); shopify-liquid (hosted themes).
- needs: Node.js, bash; shared search-then-validate scripts (family note S1); Hydrogen/React Router project. Storefront and Customer Account credentials only for real-store features.
- side effects: writes local code.
- part of: standalone mandatory specialist; overlaps shopify-custom-data on Hydrogen metafields with no tie-break.

### shopify-liquid
- id: shopify:shopify-liquid (source path: plugins/shopify/skills/shopify-liquid/SKILL.md)
- description: "Liquid is an open-source templating language created by Shopify. It is the backbone of Shopify themes and is used to load dynamic content on storefronts. Keywords: liquid, theme, shopify-theme, liquid-component, liquid-block, liquid-section, liquid-snippet, liquid-schemas, shopify-theme-schemas"
- use when: Change a Shopify theme: product section, block, snippet, translations or merchant-editable settings in Liquid/HTML/CSS/JS.
- not for: shopify-hydrogen (headless React storefront); shopify-use-shopify-cli (commands, not authoring).
- needs: Node.js, bash; shared search-then-validate scripts (family note S1); theme-check packages; theme directory or stateless code blocks.
- side effects: writes local theme files.
- part of: standalone; destination of shopify-onboarding-dev.

### shopify-onboarding-dev
- id: shopify:shopify-onboarding-dev (source path: plugins/shopify/skills/shopify-onboarding-dev/SKILL.md)
- description: "Get started building on Shopify. Use when a developer asks to build an app, build a theme, create a dev store, set up a partner account, scaffold a project, or get started developing for Shopify. NOT for merchants managing stores."
- use when: "I want to build my first Shopify app/theme": install CLI/toolkit, link to developer signup, then hand off for dev-store/scaffolding or implementation work.
- not for: shopify-onboarding-merchant (store owners); shopify-use-shopify-cli (a focused CLI problem).
- needs: shell, npm or macOS Homebrew. Install paths exist only for Claude Code, Cursor, VS Code and Gemini CLI; other clients, Codex included, stop.
- side effects: installs the Shopify CLI and AI toolkit with no extra confirmation step.
- part of: entry for the developer-setup sequence; hands off to shopify-admin, shopify-liquid, shopify-functions and other API skills.

### shopify-onboarding-merchant
- id: shopify:shopify-onboarding-merchant (source path: plugins/shopify/skills/shopify-onboarding-merchant/SKILL.md)
- description: "Set up and connect a Shopify store from your AI assistant. Use when the user wants to: set up my Shopify store, connect my store, install Shopify plugin, get started with Shopify, manage my store, add products to my store, merchant onboarding, start selling online, Shopify setup help, create my first store, how do I set up an online store, import products, migrate from Square, migrate from WooCommerce, migrate from Etsy, migrate from Amazon, migrate from eBay, migrate from Wix, import from Google Merchant Center, migrate from Clover, migrate from Lightspeed, move products to Shopify, import catalog, replatform to Shopify. This is for store owners — not developers."
- use when: As a store owner: start or connect a store, add products, manage stock/orders, or import a catalog from Square, WooCommerce, Etsy, Wix, Amazon, eBay, Clover, Lightspeed or Google Merchant Center.
- not for: shopify-onboarding-dev (building apps/themes); shopify-use-shopify-cli (one named operation with minimum scopes); ucp (acts as a shopper).
- needs: CLI 3.93.0+, browser OAuth, store URL; CSV and HTTPS image URLs for import. Declares Claude Code, Claude Desktop, Cursor; `context: fork`.
- side effects: global CLI install (announced, not paused), broad read/write store scopes, real store and stock writes; imports gated on preview approval and always DRAFT.
- part of: entry for merchant setup and import.

### shopify-partner
- id: shopify:shopify-partner (source path: plugins/shopify/skills/shopify-partner/SKILL.md)
- description: "The Partner API lets you programmatically access data about your Partner Dashboard, including your apps, themes, and affiliate referrals."
- use when: Query Partner Dashboard data: app installs and revenue, theme associations, affiliate referrals, transactions, payouts.
- not for: shopify-admin (a store's operational data); shopify-onboarding-dev (first account/tool setup).
- needs: Node.js, bash; shared search-then-validate scripts (family note S1); partner-level auth and organization context (not store credentials) to execute.
- side effects: writes local code.
- part of: standalone; niche.

### shopify-payments-apps
- id: shopify:shopify-payments-apps (source path: plugins/shopify/skills/shopify-payments-apps/SKILL.md)
- description: "The Payments Apps API enables payment providers to integrate their payment solutions with Shopify's checkout."
- use when: A payment provider integrating its processor into Shopify checkout: payment sessions, authorization/capture, refund, void, confirmation.
- not for: shopify-functions (reorder or hide payment methods); shopify-polaris-checkout-extensions (checkout UI); stripe-best-practices (a Stripe integration, not the Shopify provider API).
- needs: Node.js, bash; shared search-then-validate scripts (family note S1); payment-provider authentication and PCI/compliance context. Approval and credential acquisition procedures are not supplied.
- side effects: writes local code; guidance only, no payment execution.
- part of: standalone; niche.

### shopify-polaris-admin-extensions
- id: shopify:shopify-polaris-admin-extensions (source path: plugins/shopify/skills/shopify-polaris-admin-extensions/SKILL.md)
- description: "Add custom actions and blocks from your app at contextually relevant spots throughout the Shopify Admin. Admin UI Extensions also supports scaffolding new adminextensions using Shopify CLI commands."
- use when: Add a contextual action, block, link or print action to existing Shopify Admin pages (product, order and similar).
- not for: shopify-polaris-app-home (the app's own pages); shopify-admin (data operations without UI).
- needs: Node.js, bash; shared search-then-validate scripts (family note S1); Shopify app and CLI; exact Admin target (e.g. admin.product-details.block.render).
- side effects: writes local extension files; merchant must add or pin blocks manually.
- part of: standalone; CLI scaffold first.

### shopify-polaris-app-home
- id: shopify:shopify-polaris-app-home (source path: plugins/shopify/skills/shopify-polaris-app-home/SKILL.md)
- description: "Build your app's primary user interface embedded in the Shopify admin. If the prompt just mentions `Polaris` and you can't tell based off of the context what API they meant, assume they meant this API."
- use when: Build the app's own embedded admin UI: dashboard, index/detail/settings views, navigation, save bar, resource picker; also any ambiguous "Polaris" request.
- not for: shopify-polaris-admin-extensions (UI placed in Shopify-owned pages); checkout, customer-account and POS extension skills.
- needs: Node.js, bash; shared search-then-validate scripts (family note S1); App Bridge and Polaris type packages.
- side effects: writes local code.
- part of: standalone; default Polaris surface when context is unclear.

### shopify-polaris-checkout-extensions
- id: shopify:shopify-polaris-checkout-extensions (source path: plugins/shopify/skills/shopify-polaris-checkout-extensions/SKILL.md)
- description: "Build custom functionality that merchants can install at defined points in the checkout flow, including product information, shipping, payment, order summary, and Shop Pay. Checkout UI Extensions also supports scaffolding new checkout extensions using Shopify CLI commands."
- use when: Add buyer-facing content or behavior at checkout (shipping, payment, order summary, Shop Pay) or the thank-you page.
- not for: shopify-functions (backend rules); shopify-polaris-customer-account-extensions (account pages); shopify-payments-apps (provider processing).
- needs: Node.js, bash; shared search-then-validate scripts (family note S1); Shopify app and CLI; exact target in shopify.extension.toml.
- side effects: writes local extension files.
- part of: standalone; CLI `checkout_ui` scaffold first; shopify-custom-data first if metafields are involved.

### shopify-polaris-customer-account-extensions
- id: shopify:shopify-polaris-customer-account-extensions (source path: plugins/shopify/skills/shopify-polaris-customer-account-extensions/SKILL.md)
- description: "Build custom functionality that merchants can install at defined points on the Order index, Order status, and Profile pages in customer accounts. Customer Account UI Extensions also supports scaffolding new customer account extensions using Shopify CLI commands."
- use when: Add UI in customer accounts: order-history block, order action, full page, profile/address info or B2B company details.
- not for: shopify-customer (data queries, not hosted UI); shopify-polaris-checkout-extensions (purchase/thank-you pages).
- needs: Node.js, bash; shared search-then-validate scripts (family note S1); Shopify app and CLI; exact `customer-account.*` target.
- side effects: writes local extension files.
- part of: standalone.

### shopify-pos-ui
- id: shopify:shopify-pos-ui (source path: plugins/shopify/skills/shopify-pos-ui/SKILL.md)
- description: "Build retail point-of-sale applications using Shopify's POS UI components. These components provide a consistent and familiar interface for POS applications. POS UI Extensions also supports scaffolding new POS extensions using Shopify CLI commands. Keywords: POS, Retail, smart grid"
- use when: Add a cashier smart-grid tile or modal, loyalty action, order/product/register screen block, receipt customization or POS event observer.
- not for: shopify-polaris-admin-extensions (browser Admin pages); shopify-polaris-checkout-extensions (online checkout); shopify-polaris-app-home (embedded app UI).
- needs: Node.js, bash; shared search-then-validate scripts (family note S1); CLI and interactive scaffolding; precise POS target. Stops and prints the exact command if the CLI fails or the host is noninteractive.
- side effects: writes a new local extension only; never edits existing ones.
- part of: entry for the POS scaffold sequence; hands CLI install/upgrade to shopify-use-shopify-cli.

### shopify-storefront-graphql
- id: shopify:shopify-storefront-graphql (source path: plugins/shopify/skills/shopify-storefront-graphql/SKILL.md)
- description: "Use for custom storefronts requiring direct GraphQL queries/mutations for data fetching and cart operations. Choose this when you need full control over data fetching and rendering your own UI. NOT for Web Components - if the prompt mentions HTML tags like <shopify-store>, <shopify-cart>, use storefront-web-components instead."
- use when: Write Storefront API product, search and cart queries/mutations for a custom storefront where you own fetching and rendering.
- not for: shopify-hydrogen (any Hydrogen context); shopify-liquid (themes). `<shopify-store>` web components go to storefront-web-components, absent from this plugin.
- needs: Node.js, bash; shared search-then-validate scripts (family note S1). Storefront token setup is not described.
- side effects: writes local code; no UI, no purchase.
- part of: standalone.

### shopify-use-shopify-cli
- id: shopify:shopify-use-shopify-cli (source path: plugins/shopify/skills/shopify-use-shopify-cli/SKILL.md)
- description: "Choose when the user needs **Shopify CLI** to run or fix something now: validate app or extension config on disk (`shopify.app.toml`, `shopify.app.<name>.toml`, `shopify.extension.toml`); run or troubleshoot store workflows (`shopify store auth`, `shopify store execute`); inventory or product changes by handle, SKU, or location name; or CLI setup, auth, upgrade issues. Emphasize **commands and operational steps**, not only authoring GraphQL. Skip for API-only understanding or codegen with no CLI execution. Examples: validate configuration before deploy; run an existing query via CLI; list products; missing `shopify store execute`."
- use when: "Validate this app TOML before deploy", "run this query on my store", "change stock for SKU X at warehouse Y", or fix missing/auth/upgrade CLI problems.
- not for: shopify-admin (authoring/explaining GraphQL only); shopify-onboarding-merchant (guided, broad-scope store setup).
- needs: Node.js, @shopify/cli (installs or upgrades it), store domain and OAuth scopes. Store flow depends on a `validate_graphql_codeblocks` tool neither manifest supplies: without it, tell the user the operation and scopes are unvalidated and to review them before `--allow-mutations`.
- side effects: CLI install/upgrade, browser auth, store mutations (`--allow-mutations`), deployment if asked; no general approval gate stated.
- part of: standalone; shared handoff target for the developer, custom-data, functions and POS skills.

### ucp
- id: shopify:ucp (source path: plugins/shopify/skills/ucp/SKILL.md)
- description: "Use when the user wants to use the UCP CLI to find, compare, buy, or track products from online merchants, or to set up and troubleshoot the local UCP profile required for merchant-scoped operations. Covers global catalog search ("find me X under $Y"), named-merchant transactions ("buy this from Z.com"), order tracking, `ucp profile init`, `ucp doctor`, carts, checkout, orders, and UCP setup/help. Falls back to merchant-hosted handoff when direct in-protocol checkout isn't available."
- use when: As a shopper: "find me X under $Y", compare products, buy from a named merchant, track an order, or fix local UCP setup.
- not for: shopify-onboarding-merchant (the seller's own store); stripe-directory (finds businesses, software and pay-per-call API endpoints, not merchant products).
- needs: `ucp` binary (no installer supplied); local profile before any merchant-scoped call; buyer details and payment data per merchant schema.
- side effects: creates a profile, sends buyer data, builds carts, can place paid orders; unlike stripe-directory it has no universal confirm-final-price step.
- part of: standalone buyer journey; hands off to the merchant's continue URL when in-protocol checkout fails.
