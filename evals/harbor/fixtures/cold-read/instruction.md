Verify every load-bearing claim in `decision.md` against the repository, then
decide whether its concurrency design still holds. Return only JSON:

```json
{
  "claims": [
    {"id": "C1", "status": "true|false|unknown", "evidence": "file:line and fact"}
  ],
  "design": {
    "status": "keep|change",
    "replacement": "keep-etag-plan|serialize-writes|other",
    "reason": "evidence-based reason"
  }
}
```
