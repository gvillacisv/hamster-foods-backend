# ADR 1: Rolling Window vs. Fixed Cycle for Tier Calculation

### Context

We needed to define how the "10-day window" is measured. Two patterns were considered:

1. **Fixed Cycles:** Tiers are calculated in 10-day blocks starting from the user's sign-up date (e.g., Feb 1-10, Feb 11-20).
2. **Rolling Window:** Tiers are calculated based on the sum of transactions occurring in the **last 10 days relative to the current moment**.

### Decision

We chose the **Rolling Window** approach. The system does not store "window periods"; instead, it dynamically queries the transaction history using a sliding time boundary. Our rationale was:

* **User Retention:** Fixed cycles create "dead zones" where users stop spending once they reach a tier because extra spending doesn't count toward the next block. Rolling windows keep users engaged daily as old purchases are constantly "falling off" the back of the window.
* **Perceived Fairness:**
  * In a **Fixed Cycle**, the end of a window causes a "total reset." A user who worked hard to reach a milestone feels a sense of frustration because all their effort is wiped out simultaneously on day 11, regardless of when the purchases were made.
  * In a **Rolling Window**, the user perceives the system as more logical and fair. They understand that only their **oldest efforts** are being removed from the milestone calculation, while their recent transactions remain valid. This mitigates the "pain of loss" and encourages consistent, smaller interactions rather than one-time "burst" spending.
* **Technical Simplicity:** Rolling windows eliminate the need to track "Cycle IDs" or "Reset Dates" in the database. The logic is a simple `SUM` where `created_at >= NOW() - INTERVAL 10 DAY`.

### Consequences

*   **Positive:** Higher user engagement and a more "fluid" gamification experience.
*   **Positive:** Reduced database complexity by treating time as a continuous line rather than discrete buckets.
*   **Negative:** Require a Scheduled Job to handle expirations for users who are not actively transacting.
