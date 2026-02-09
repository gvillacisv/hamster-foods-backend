# ADR 3: Currency Stability

### Context

Tier progress is calculated in EUR (assumption), but transactions can be in any currency. Runtime conversion using live rates makes tiers unstable; a user could lose a tier overnight because of a change in exchange rates, even without spending changes.

### Decision

We implemented **Base Currency Snapshotting**. The EUR value and the exchange rate used are stored in the `orders` table at the moment of the transaction.

### Consequences

*   **Positive:** Tiers are deterministic and stable for the full 10-day window.
*   **Positive:** Improved performance; the system performs a simple `SUM(amount_eur)` without joining an exchange rate table at runtime.
