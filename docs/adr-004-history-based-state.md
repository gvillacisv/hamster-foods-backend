# ADR 4: History-Based State Persistence

### Context

The system requires a persistent history of tier changes, but the `customers` table is treated as a legacy, read-only resource that cannot be modified probably because our "Loyalty Domain" (assumption) could not have ownership over this model.

### Decision

We adopted a **Log-Based State** approach. The `tier_history` table serves as the Source of Truth. The "Current Tier" is determined by querying the most recent record for a specific `customer_id`.

### Consequences

*   **Positive:** Zero impact on existing legacy schemas.
*   **Positive:** Audit-ready trail of all tier transitions with associated "reasons" (Transaction vs. Expiration).
*   **Negative:** Requires an indexed query to find the current state, which is slightly more expensive than reading a direct column in the `customers` table.
