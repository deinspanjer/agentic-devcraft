# Anthropic skills (anthropics/skills)
Source: https://github.com/anthropics/skills @ e4bb5d960d87126ff3b3a8af1a104b7db67560ba
Distribution (anthropics/skills): the Claude Code plugin marketplace `anthropic-agent-skills` (`/plugin marketplace add anthropics/skills`, then `/plugin install <plugin>@anthropic-agent-skills`). Skill directories are `skills/<skill>/`.
Curated records of remote catalog entries, not proof of installation: check at runtime that a skill is available in the current host and read its current SKILL.md before relying on any detail below.

Marketplace `anthropic-agent-skills` (`.claude-plugin/marketplace.json`; five plugin entries, all `source: "./"`, `strict: false`). Core-dev families first, then one-line pointers to families far from development.

## Family: claude-api
- source repo: https://github.com/anthropics/skills (entry `claude-api`: skills/claude-api)
- manifest notes: Claude marketplace manifest only. No MCP or app connector. The skill needs the user's own Anthropic credential (below) and the `ant` CLI for Managed Agents.
- router: none at family level (one skill). The skill is itself an entry router for Claude-API work (a Quick Task Reference plus subcommands migrate, prompt-audit, upgrade, cost-optimize, build-eval, hillclimb, preserved-thinking-migration, managed-agents-onboard), loading `shared/`, `{lang}/` and `curl/` files on demand.
- development distance: core-dev
- disclosure recommendation: simple. One skill; its full record belongs in the source catalog.

### claude-api
- id: claude-api:claude-api (source path: skills/claude-api/SKILL.md)
- description: "Reference for the Claude API / Anthropic SDK — model ids, pricing, params, streaming, tool use, MCP, agents, caching, token counting, model migration.
  TRIGGER — read BEFORE opening the target file; don't skip because it "looks like a one-liner" — whenever: the prompt names Claude/Anthropic in any form (Claude, Anthropic, Fable, Opus, Sonnet, Haiku, `anthropic`, `@anthropic-ai`, `claude-*`, `us.anthropic.*`, `[1m]`); the user asks about an LLM (pricing/model choice/limits/caching) — never answer from memory; OR the task is LLM-shaped with provider unstated (agent/MCP/tool-definition/multi-agent/RAG/LLM-judge/computer-use; generate/summarize/extract/classify/rewrite/converse over NL; debugging refusals/cutoffs/streaming/tool-calls/tokens).
  SKIP only when another provider is being worked on (overrides all triggers): OpenAI/GPT/Gemini/Llama/Mistral/Cohere/Ollama named in the query; OR `grep -rE 'openai|langchain_openai|google.generativeai|genai|mistralai|cohere|ollama'` over the project hits (run this grep FIRST if no provider named — don't Read the file)."
- use when: "Write, debug or migrate code that calls Claude", or an LLM-shaped task with no provider named. Subcommands: `migrate` (new model; asks scope first), `prompt-audit` (dated prompts or config; non-interactive report and diff), `upgrade` (Python SDK 0.x to 1.x), `cost-optimize`, `build-eval`, `hillclimb`, `preserved-thinking-migration`, `managed-agents-onboard`.
- not for: implementing another provider's API (skip/stop; `prompt-audit` instead reports provider markers without switching providers); `mcp-builder` (builds a server); `skill-creator` (skills); the Claude Agent SDK (it only points to docs). `academy-guide` can supplement learning questions.
- needs: credentials when making API calls (`ANTHROPIC_API_KEY`, auth token, `ant auth login` profile or WIF; Vertex uses GCP credentials); the language's official SDK, or raw HTTP when requested, in shell projects or without a supported SDK; web fetch for live docs; `ant` CLI for the recommended Managed Agents configuration flow. Usage/cost reports use raw HTTP with an Admin key or `org:admin` OAuth; cost analysis can instead use app logs or labeled code estimates.
- side effects: edits project code; `prompt-audit` and cost/migration diagnostics propose diffs by default and apply only on request. Model runs spend money; cost/eval workflows require approval. URL-based Managed Agents onboarding writes `agents/<name>/agent.md` and environment/vault/deployment YAML; `ant apply` synchronizes persistent remote agents, which scheduled deployments can then run unattended. The source defaults to `claude-opus-5-5`, adaptive thinking for complex work, and refusal fallbacks with user disclosure (server-side or client middleware depending on platform).
- part of: entry router for Claude API work. Source conflict (fetch SDK docs for undocumented bindings vs write first and fix from compiler errors): promise no doc lookup; expect write-first for missing type names and whenever the network is blocked, a fetch at most for other undocumented bindings.

## Family: example-skills
- router: none. No skill sequences the others; hand-offs are implicit (`theme-factory` styles what another skill built).
- covers: twelve skills. Core-dev: `mcp-builder` (MCP servers), `skill-creator` (writing, testing and benchmarking skills), `frontend-design` (distinctive UI design in any framework), `webapp-testing` (Playwright checks of a local web app), `doc-coauthoring` (PRDs, design docs, RFCs, specs). Adjacent: `web-artifacts-builder` (bundled claude.ai artifacts). Six far members (generative and static art, Slack GIFs, themes, Anthropic brand styling, internal comms) have one-line entries in the same file.
- Full records: families/example-skills.md

## Far from development (pointers only)
- document-skills (`docx`, `pdf`, `pptx`, `xlsx`: office-document file work chosen by file extension) -> far/documents.md
- academy-guide (post-answer Claude Academy recommendations for someone learning a Claude product) -> far/learning.md
- discernment-nudge (post-answer check-your-assumptions questions; reply-style behaviour) -> far/assistant-behaviour.md
- template (`template/SKILL.md`, id `template:template`, frontmatter name `template-skill`, description "Replace with description of the skill and when Claude should use it."; in no marketplace plugin): a six-line placeholder with no instructions. Never route to it; `skill-creator` is the real authoring skill.
