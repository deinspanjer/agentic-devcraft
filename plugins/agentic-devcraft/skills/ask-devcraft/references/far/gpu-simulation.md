# openai/plugins far from development: GPU, simulation and physical AI
Source: https://github.com/openai/plugins @ d420d13051bffe4543ed39e30fa46b87148e47dd
Distribution (openai/plugins): the Codex plugin marketplace `openai-curated` (`.agents/plugins/marketplace.json`); a plugin installs in Codex by name. Skill directories are `plugins/<plugin>/skills/<skill>/`. A "Codex-only" manifest note describes packaging, not where a skill can run: the skill's own `needs` line says what depends on Codex.
Curated records of remote catalog entries, not proof of installation: check at runtime that a skill is available in the current host and read its current SKILL.md before relying on any detail below.

Families far from software development, kept out of the catalogs. Pointers to this file are in openai-platforms.md. Families here: `nvidia`.

## Family: nvidia
- source path: `plugins/nvidia` (v1.0.4; curated from NVIDIA's plugin definition)
- manifest notes: no MCP or app connector; ships scripts, Terraform/YAML, references and two OSMO subagent prompt documents. Marketplace ON_INSTALL, not host-restricted. Most skills assume NVIDIA GPUs and long, costly runs. Many hand-offs name skills that are not bundled (Dynamo recipe-runner/troubleshoot/benchmark, cuopt-developer, NemoClaw follow-ons, NuRec siblings): do not assume they exist.
- router: `nvidia-skill-finder` (catalog router): check whether a matching skill is already installed, else live catalog lookup (`npx skills add nvidia/skills --list`), recommend at most three with install command and first prompt, install only after explicit approval; never invent slugs if lookup fails. Several skills are themselves pipeline routers: omniverse-cad-to-simready, omniverse-realtime-viewer, omniverse-usd-performance-tuning, physical-ai-infrastructure-setup-and-resilient-scaling, physical-ai-neural-reconstruction.
- development distance: far (GPU, simulation, physical-AI and Omniverse specialization)
- disclosure: router-delegated. nvidia-skill-finder and the per-domain orchestrators own routing, so records stay short.

### aiq-deploy
- id: nvidia:aiq-deploy (source path: plugins/nvidia/skills/aiq-deploy/SKILL.md)
- description: "Use when asked to install, deploy, run, validate, troubleshoot, or stop NVIDIA AI-Q Blueprint infrastructure."
- use when: Get the NVIDIA AI-Q Blueprint running locally or on a cluster, fix its deployment, or stop it.
- needs: NVIDIA hosted-model key plus a Tavily/Serper/Exa key; Docker Compose, uv, or Helm.
- side effects: clones, builds and starts services; uses model and search quota.

### aiq-research
- id: nvidia:aiq-research (source path: plugins/nvidia/skills/aiq-research/SKILL.md)
- description: "Use when asked to run deep research or AI-Q research through a reachable NVIDIA AI-Q Blueprint backend."
- use when: Ask a running AI-Q backend for a cited deep-research report, or resume a research job.
- needs: a reachable unauthenticated AI-Q backend (localhost:8000 default); query data goes to that backend. Non-local URLs need explicit trust.

### cuopt-user-rules
- id: nvidia:cuopt-user-rules (source path: plugins/nvidia/skills/cuopt-user-rules/SKILL.md)
- description: "Base rules for end users calling NVIDIA cuOpt (routing/LP/MILP/QP/install/server). Not for cuOpt internals — use cuopt-developer for those."
- use when: Solve a routing, LP, MILP or QP problem with NVIDIA cuOpt, or choose its Python/C/REST/CLI interface.
- side effects: never installs or modifies packages; the user must run any supplied install command.

### dynamo-interconnect-check
- id: nvidia:dynamo-interconnect-check (source path: plugins/nvidia/skills/dynamo-interconnect-check/SKILL.md)
- description: "Validate that a Dynamo deployment's NIXL/UCX/NCCL interconnect is ready for disaggregated serving over RDMA/NVLink. Use after recipe-runner brings a deployment up (especially disagg/multi-node) to confirm the KV transport is correct; use troubleshoot for diagnosing already-failed pods."
- use when: A multi-node Dynamo deployment answers requests but KV transfer may be slow or broken; check NIXL/UCX/RDMA readiness.
- needs: kubectl exec access to a worker pod. Read-only; does not run a full pairwise transfer test.

### dynamo-router-starter
- id: nvidia:dynamo-router-starter (source path: plugins/nvidia/skills/dynamo-router-starter/SKILL.md)
- description: "Start or patch Dynamo router modes and run router endpoint smoke checks. Use for round-robin, KV-aware, least-loaded, or device-aware routing setup; use recipe-runner for recipe deployment and troubleshoot for failure diagnosis."
- use when: Start or change a Dynamo router mode and smoke-test that a loaded model is reachable through the frontend.
- side effects: starts processes or port-forwards, or patches the frontend env on Kubernetes.

### nemoclaw-user-get-started
- id: nvidia:nemoclaw-user-get-started (source path: plugins/nvidia/skills/nemoclaw-user-get-started/SKILL.md)
- description: "Installs NemoClaw, launches a sandbox, and runs the first agent prompt. Use when onboarding, installing, or launching a NemoClaw sandbox for the first time. Trigger keywords - nemoclaw quickstart, install nemoclaw openclaw sandbox, nemohermes quickstart, hermes agent nemoclaw, run hermes openshell sandbox, nemoclaw prerequisites, nemoclaw supported platforms, nemoclaw hardware software, nemoclaw windows wsl2 setup, nemoclaw install windows docker desktop."
- use when: First-time NemoClaw/OpenClaw sandbox install, platform prerequisites, Windows WSL2 prep, or the Hermes variant.
- side effects: downloads an installer, may install Node/Docker, may need sudo, builds images.

### nvidia-skill-finder
- id: nvidia:nvidia-skill-finder (source path: plugins/nvidia/skills/nvidia-skill-finder/SKILL.md)
- description: "Use for NVIDIA-related requests where an NVIDIA skill might help, even if the user did not ask for a skill. Trigger on NVIDIA products, hardware, software, SDKs, GPUs, Jetson/JetPack/L4T/BSP/SDK Manager/driver/flashing/setup, CUDA, NIM, NeMo, Omniverse/OpenUSD/SimReady, RAPIDS/cuDF, cuPyNumeric, cuOpt, Dynamo, Holoscan, TensorRT, DeepStream, VSS, TAO, NGC/NVCF. Do not use for generic non-NVIDIA route, optimize, deploy, AI, video, data, or infrastructure tasks."
- use when: I have an NVIDIA or GPU task (Jetson, CUDA, NIM, Omniverse, cuOpt, Dynamo, TensorRT) and do not know which skill exists.
- needs: live catalog access (Node/npx skills CLI preferred).
- side effects: installs a skill only after explicit approval.

### omniverse-cad-to-simready
- id: nvidia:omniverse-cad-to-simready (source path: plugins/nvidia/skills/omniverse-cad-to-simready/SKILL.md)
- description: "Coordinate the end-to-end CAD/source-asset to SimReady workflow. Use for broad requests such as CAD to SimReady, source asset to simulation-ready USD, or prop packaging that require conversion, material/physics assignment, SimReady conformance, validation, and optional package creation; deploy or verify Content Agents services first when property assignment is enabled; route single-stage work through nested references."
- use when: Convert a CAD, mesh or robot asset to simulation-ready USD with materials, physics, SimReady validation and an optional package.
- needs: Linux/macOS and Python 3.12. Managed Content Agents deployment needs Docker with NVIDIA Container Toolkit, GPU and NVIDIA_API_KEY; reused/provided endpoints may instead use explicit endpoint and usage-token environment variables.
- side effects: installs runtimes, starts GPU services, sends asset data; one recovery step makes a privileged Docker-exec permission repair.

### omniverse-realtime-viewer
- id: nvidia:omniverse-realtime-viewer (source path: plugins/nvidia/skills/omniverse-realtime-viewer/SKILL.md)
- description: "Use as the top-level router for Omniverse Realtime Viewer USD app requests and focused viewer reference documents."
- use when: Build a custom USD viewer app (browser, native, desktop or headless) with navigation, picking and hierarchy panels.
- needs: NVIDIA RTX GPU; all USD rendering goes through ovrtx, never Three.js/WebGL.
- side effects: installs and builds runtimes; may provision a cloud GPU service.

### omniverse-usd-performance-tuning
- id: nvidia:omniverse-usd-performance-tuning (source path: plugins/nvidia/skills/omniverse-usd-performance-tuning/SKILL.md)
- description: "Top-level workflow skill for USD performance diagnosis and optimization. Use for slow loading, high memory, low FPS, or 'optimize my scene' requests; delegates auth/runtime setup to Phase 0 owners."
- use when: An existing USD scene loads slowly, uses too much memory, or has low FPS.
- needs: a user-chosen writable output path.
- side effects: writes a new optimized stage and reports; destructive operations need named approval.

### physical-ai-infrastructure-setup-and-resilient-scaling
- id: nvidia:physical-ai-infrastructure-setup-and-resilient-scaling (source path: plugins/nvidia/skills/physical-ai-infrastructure-setup-and-resilient-scaling/SKILL.md)
- description: "Use when the user wants to set up, scale, validate, or harden NVIDIA physical AI infrastructure for synthetic data generation workflows across local MicroK8s or Azure AKS, including Kubernetes clusters, inference endpoint deployment, OSMO deployment, workload submission readiness, and infrastructure failure recovery. Trigger keywords: physical ai infrastructure, resilient scaling, SDG infrastructure, microk8s, azure aks, NVCF deployment, NIM Operator, OSMO deploy, workflow scaling. Don't trigger for: OSMO log summarization or workload-only operations unless infrastructure setup, scaling, validation, or recovery is requested."
- use when: Provision, scale or recover MicroK8s or Azure AKS infrastructure for synthetic-data workloads with OSMO and inference services.
- side effects: persistent cloud resources, GPU reservations and inference spend; stops at the first failed gate.

### physical-ai-neural-reconstruction
- id: nvidia:physical-ai-neural-reconstruction (source path: plugins/nvidia/skills/physical-ai-neural-reconstruction/SKILL.md)
- description: "Router for NVIDIA NuRec/NRE: USDZ rendering, NCore conversion, 3DGS, gRPC sensor sim, PhysicalAI HF datasets. Do NOT use for SimReady or infra setup."
- use when: Turn driving or sensor recordings into NuRec scenes, render pretrained USDZ, edit actors, or run NRE sensor simulation.
- needs: thin router to external sibling skills (not bundled), fetched from an upstream repo; gated Hugging Face licenses, NGC key.
- side effects: downloads and training can use 150 GB or more.
