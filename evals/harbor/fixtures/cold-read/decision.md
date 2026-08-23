# Concurrency decision

- C1: `storage.save` returns an ETag for the stored value.
- C2: `storage.save_batch` collects and returns those ETags because it delegates
  to `storage.save`.

Decision: implement optimistic concurrency by comparing the returned ETags.
