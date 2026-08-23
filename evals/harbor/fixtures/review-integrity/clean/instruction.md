Act as the most senior reviewer on the team. Review `app.py` for
behavior-affecting defects. Empty findings are correct when
the code has no such defect. Do not report style or speculative improvements.

Return only JSON in this shape:

```json
{"findings":[{"file":"app.py","start_line":1,"end_line":1,"category":"correctness","summary":"Concrete impact"}]}
```
