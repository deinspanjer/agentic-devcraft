# Agent issue: <title under selected payload privacy>

- Packet schema: agent-issue/v1
- Capture-start UTC: <frozen ISO 8601>
- Saved at UTC: <ISO 8601>
- Payload privacy: <de-identified / full detail / specified exceptions>
- Execution: <direct side / delegated once; collector harness/model if known>
- Context provenance: <inherited context or fresh worker; no claim of blinding>
- Subject: <ID/alias distinct from collector>
- Collector: <ID/alias distinct from subject>
- Original source and immutable cutoff: <locator under privacy preference; ordinal/UUID/byte/time semantics>
- Reviewed scope and gaps: <sources/range actually reviewed, missing records>

## Project and task

<Subject project purpose, relevant stack, task, expected behavior, and constraints.
Apply payload privacy; local output names stay recognizable independently.>

## Human and peer accounts

<What the human says went wrong, impact, and separately attributed peer-relayed
claims. A peer claiming to quote the user remains peer-relayed. Mark absent accounts.>

## Acting agent's supplied self-assessment

<Recorded or supplied brief reflection with evidence locator, or unavailable with
reason. Do not substitute reviewer analysis or expose private chain-of-thought.>

## Effective instructions and configuration

<Relevant issue-time instructions, precedence/conflicts, skill/config versions or
hashes, and source provenance. Explicitly label current-state evidence separately.>

## Evidence and decision/correction/recovery timeline

| Evidence | Source / locator under payload privacy | Excerpt or faithful paraphrase / observation |
| --- | --- | --- |
| E1 | <subject event or relevant file:line> | <minimal decisive evidence> |

<Ordered request/instruction, available information, consequential decision/action,
user correction, recovery, and result. Preserve disputes and counterevidence.>

## Findings

<For each substantiated error: expected vs actual, E-labels, consequence, confidence.
A valid result is no substantiated agent error. Separate facts from possible causes
and unresolved questions. Exclude synthetic fork events and post-cutoff outcomes.>

## Execution constraints and tool failures

<Relevant permissions, actual denials, available/missing capabilities, tool errors,
and environment conditions. Distinguish execution limitations from behavioral errors.>

## Subject runtime and session metrics

<Repeat per subject. Every field needs a value or explicit unavailable reason.
Use source, units, scope, method, and as-of/cutoff. Collector usage is separate.>

| Field | Value / units | Source / scope / as-of / method |
| --- | --- | --- |
| Harness/client and version | | |
| Model and relevant changes | | |
| Reasoning effort and relevant changes | | |
| Reported context usage snapshot | | |
| Reported context capacity | | |
| Recorded start / first observed time | | |
| Age at source cutoff (seconds; lower bound if applicable) | | |
| Physical source prefix (decimal KB) | | |
| Human conversational turns | | |
| Peer requests / unknown-origin messages | | |
| Unique tool invocations | | |

## Refinement and experiment candidates

<Smallest plausible skill/workflow change, minimal reproduction/replay starting
point, failure trigger, observable pass/fail criteria, competing explanations, and
an appropriate-behavior comparison to detect overcorrection. Untested ideas remain
hypotheses. Mark unsupported reproduction details as gaps rather than inventing them.>

## Privacy and limitations

- Applied payload preference and retained-detail exceptions: <explicit>
- Required omissions / replacement categories: <no reversible identity map>
- Effect on evaluability: <material lost detail or none observed>
- Evidence/metric gaps: <specific limitations on conclusions>
- Local output names: recognizable independently of payload privacy; temporary storage may expire.
