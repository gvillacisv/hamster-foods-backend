## RFC: Unified Currency and Tiering Service Integration

**Status:** Draft

**Author:** Gabriel Villacis

**Date:** February 2026

### 1. Objective

To centralize financial and loyalty configurations by moving the **base currency**, **exchange rate logic**, and **tier thresholds** from local constants to a unified external service provider.


### 2. Core Assumptions

* **Unified Financial Service:** We assume a single service manages the relationship between the `BASE_CURRENCY` and the current `RATES_TO_BASE`. This prevents "split-brain" scenarios where the base currency might change without updating the corresponding exchange table.
* **External Threshold Service:** We assume the `TIER_THRESHOLDS` are requested from an independent service, allowing thresholds to be modified dynamically based on marketing or seasonal requirements without affecting the currency logic.


### 3. Proposed Logic & Implementation

#### A. Centralized Currency & Tier Mapping

The local constants are replaced by a service call that returns the entire financial context. The tiering logic is then applied to the normalized "Base" values.

#### B. Unified Data Relation

The system will now treat the configuration as a cohesive object, ensuring the thresholds and currency rates are always in sync:

```python
# Conceptual response from the Financial Service
{
  "baseCurrency": "EUR",
  "rates": [
    { "currency": "GBP", "rate": 1.18},
    { "currency": "USD", "rate": 0.93}
  ]
}
```

```python
# Conceptual response from the Loyalty Service
{
  "thresholds": [
    { "tier": "CHAMPION", "threshold": 23},
    { "tier": "LOYAL", "threshold": 15},
    { "tier": "ROOKIE", "threshold": 7}
  ]
}
```

### 4. Implementation Constraints

1. **Transactional Integrity:** When an order is placed, the system must fetch the specific rate and threshold set associated with the `baseCurrency` defined *at that moment*.
2. **Tier Independence:** Tier calculations will only occur *after* the currency has been normalized, ensuring a customer spending 23 USD is evaluated fairly against a customer spending 23 EUR based on the exchange rate.
