# ADR 3: Pessimistic Locking for Concurrency Control

### Context

A "Race Condition" exists where the Scheduled Job might attempt a "Passive Downgrade" at the exact millisecond a user completes a transaction. Without locking, a stale downgrade could overwrite a real-time upgrade.

### Decision

We chose **Pessimistic Locking** over Optimistic Row Versioning.

### Consequences

*   **Positive:** Ensures the "Read-Calculate-Write" cycle is atomic.
*   **Positive:** Avoids the complexity of implementing retry-loops in Python (required for Optimistic locking).
*   **Negative:** Slightly higher database resource usage during the lock duration (milliseconds).
