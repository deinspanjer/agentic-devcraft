Add support for loading model prices from a user-supplied JSON file while retaining the built-in defaults when no file is supplied.

Use `--prices <path>`. The file contains USD prices per one million tokens in this shape:

```json
{
  "models": {
    "model-name": {
      "input": 1.0,
      "cached_input": 0.1,
      "cache_write": null,
      "output": 6.0
    }
  }
}
```

Each model entry must contain all four rate fields. A rate is either a non-negative number or `null` when no rate is published. File entries override or add model rates for the report being generated; models absent from the file keep their built-in rates. An unreadable file, malformed JSON, or invalid rate entry must exit unsuccessfully with a useful error. Without `--prices`, existing report behavior and JSON output remain unchanged.
