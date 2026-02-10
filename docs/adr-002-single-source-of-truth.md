# ADR 2: Single Source of Truth

### Context

The system requires tier updates from two distinct entry points: real-time transactions (Active) and a daily expiration job (Passive). Duplicating the threshold logic (7, 15, 23) and the 10-day window calculation in both places creates a risk of "logic drift" and maintenance debt.

### Decision

We implemented a **Service Layer Pattern** centered around a single function: `sync_user_tier()`.

### Consequences

*   **Positive:** Guaranteed consistency across all system artifacts. Any change to business rules (e.g., changing a threshold) is made in one location.
*   **Positive:** Simplified testing; only one core business engine needs unit testing.
*   **Negative:** Expose an endpoint or develop a message listener to make this logic accessible to a scheduled job.
