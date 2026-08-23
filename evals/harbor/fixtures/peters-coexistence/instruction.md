Create `plan.md` for adding a batch-save operation to `service.py`. Use the
installed workflow skills that apply, verify load-bearing source facts, and
avoid repeating equivalent phases.

Also create `evaluation-record.json` containing the phase names used, invoked
skill names, number of conversational turns, and whether the final plan
correctly preserves `save`'s no-return-value contract:

```json
{
  "phases": ["design", "review", "plan"],
  "invocations": ["skill-name"],
  "turns": 1,
  "outcome": {"preserves-save-contract": true}
}
```
