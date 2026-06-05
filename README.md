# Silph Co. Supply Chain & Manufacturing Quality Analytics

## Executive Summary
This project analyzes manufacturing anomalies and distribution cost inefficiencies across Silph Co.’s regional logistics network (Kanto/Johto). By leveraging Python for data simulation, SQL (SSMS 21) for relational database modeling and auditing, and Tableau for executive dashboards, this analysis identifies a major mechanical failure point on Production Line B and proposes an inventory pre-positioning strategy to reduce premium shipping spend by tracking regional tournament demand spikes.

👉 [View the Interactive Tableau Dashboard Here](YOUR_TABLEAU_PUBLIC_LINK_HERE)

## Key Insights & Business Impact
1. **Manufacturing Defects Identified:** Production Line B exhibits a **47.6% failure rate** specifically when manufacturing Great Balls, driven by an intentional data-seeded machine overheating anomaly (>215°C) resulting in silicon purity drops. 
   * *Recommendation:* Halt Great Ball production on Line B for calibration of heating elements; reallocate Great Ball volume to Line A/C.
2. **Logistical Cost Spikes:** Premium freight (`Pidgeot Express`) drives average shipping costs up to **$1,702 per order** during major tournament windows, whereas baseline rail transport (`Magnet Train`) averages **$731 per order** in high-volume hubs like Goldenrod City.
   * *Recommendation:* Implement a 21-day inventory pre-positioning cycle prior to known League events to utilize bulk rail transport, reducing reliance on emergency expedited shipping.

## Technical Tool Stack & Architecture
* **Python (Pandas, NumPy):** Simulated 5 relational tables with injected operational anomalies (date-override errors, manufacturing glitches).
* **SQL Server (T-SQL, SSMS 21):** Modeled database architecture, enforced relational joins, and utilized Common Table Expressions (CTEs) for multi-layered aggregations.
* **Tableau:** Developed multi-page dashboards for localized root-cause analysis and operational tracking.

## Repository Structure
* `generate_data.py`: Python data generation engine.
* `silph_co_analysis.sql`: T-SQL relational schema setup, data quality audits, and analytical CTE queries.