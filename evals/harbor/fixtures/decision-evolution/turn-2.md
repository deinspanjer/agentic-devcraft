New controlling evidence: the signed vendor contract permits at most 7 days of
raw-event retention and prohibits exporting raw events elsewhere. Update the
decision record and every affected downstream conclusion.

Return only JSON:

```json
{
  "changed_basis": [{"id":"B1","from":"old fact","to":"new fact"}],
  "current_decision": {"id":"D2","value":"retain-7-days"},
  "history": [{"id":"D1","status":"superseded","replaced_by":"D2"}],
  "downstream": [
    {"id":"batch-window","value":"7-days-max"},
    {"id":"storage-estimate","value":"210-gb"}
  ]
}
```
