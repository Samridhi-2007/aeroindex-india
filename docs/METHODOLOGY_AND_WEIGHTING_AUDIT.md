# Research Audit: Official Indian Domestic Airfare Weighting Sources

## Executive Summary

An exhaustive research audit of official Indian statistical and aviation datasets was conducted to verify whether an authoritative government source provides **route-level domestic airfare expenditure weights** (e.g. DEL–BOM vs BOM–BLR).

**Finding**: No official Indian government source (MoSPI or DGCA) provides route-level economic expenditure weights for domestic air travel in the Consumer Price Index (CPI). 

As a result, production APIx aggregation remains **`BLOCKED`** with **`reason = ROUTE_WEIGHTS_MISSING`** and **`weighting_status = MISSING_INPUT`**, strictly preserving economic statistical governance.

---

## 1. Official Sources Audited

### A. MoSPI (Ministry of Statistics and Programme Implementation)
*   **Dataset**: Consumer Price Index (CPI Base 2024=100 & Base 2012=100), Household Consumption Expenditure Survey (HCES).
*   **Item Weight Available**: Official macro item-level weight for domestic airfare (`Item Code 07.3.3.1.2.01`, Weight = `0.01166625043306` in 2024 Rural CPI basket).
*   **Route-Level Weights**: **NOT PUBLISHED**. MoSPI compiles inflation for the airfare commodity as a single national item. It does not publish route-specific expenditure weight distributions across domestic city pairs.

### B. DGCA (Directorate General of Civil Aviation)
*   **Dataset**: Monthly & Annual Scheduled Domestic Passenger Traffic Reports (City-Pair Statistics).
*   **Data Available**: Physical passenger volume counts per city pair (e.g., number of passengers flying DEL–BOM vs BOM–BLR).
*   **Methodology Rationale**: DGCA traffic statistics measure **physical passenger volume**, not consumer expenditure shares. Converting physical traffic volume directly into price index weighting violates CPI methodology without an official MoSPI expenditure weighting matrix.

---

## 2. Production Pipeline Status

| Component | Status | Production Implementation |
| :--- | :--- | :--- |
| **Elementary Index ($J_r$)** | **OPERATIONAL** | Jevons geometric mean calculated across matched genuine EaseMyTrip BASE & CURRENT snapshots. |
| **CPI Airfare Item Weight** | **OPERATIONAL** | Kept separate as reference macro item weight (`0.01166625043306`). |
| **Route Weights ($W_r$)** | **UNAVAILABLE** | Route weights remain unconfigured (`{}`). No demo weights, equal weights, or fabricated weights are inserted. |
| **Final APIx** | **BLOCKED** | `calculation_status = BLOCKED`, `reason = ROUTE_WEIGHTS_MISSING`, `apix = null`. |

---

## 3. Required Input to Unblock Production APIx

To legitimately finalize an `OFFICIAL-WEIGHTED` APIx aggregate index:
1. **MoSPI / Government Expenditure Matrix**: An official government expenditure weighting matrix assigning explicit basket weights ($W_r$) across domestic routes where $\sum W_r = 1.0$.
2. **Metadata Citation**: Official publication reference and `status = "official"`.
