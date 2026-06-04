-- ==============================================================================
-- PROJECT: Silph Co. Supply Chain & Manufacturing Quality Analytics
-- AUTHOR: Data Analyst Portfolio Project
-- ENGINE: SQL Server (T-SQL)
-- DESCRIPTION: Database schema initialization, data quality audits, 
--              and advanced logistical/manufacturing insight queries.
-- ==============================================================================

-- ==========================================
-- 1. DATABASE & SCHEMA INITIALIZATION
-- ==========================================

-- Create the relational database sandbox
CREATE DATABASE SilphCo_Logistics;
GO
USE SilphCo_Logistics;
GO

-- Table 1: Manufacturing Batches (Staging Table)
CREATE TABLE manufacturing_batches (
    Batch_ID VARCHAR(50) PRIMARY KEY,
    Item_Type VARCHAR(50),
    Production_Line VARCHAR(50),
    Manufacture_Date DATE,
    Machine_Temperature_C DECIMAL(5,2),
    Silicon_Purity_Pct DECIMAL(5,2)
);

-- Table 2: Quality Control Item Ledger
CREATE TABLE item_ledger (
    Item_Serial_ID VARCHAR(50) PRIMARY KEY,
    Batch_ID VARCHAR(50),
    Quality_Control_Status VARCHAR(50),
    Defect_Type_Code VARCHAR(50)
);

-- Table 3: Regional Distribution Centers
CREATE TABLE distribution_centers (
    Center_ID VARCHAR(50) PRIMARY KEY,
    Region VARCHAR(50),
    City VARCHAR(50),
    Max_Capacity_Units INT,
    Operating_Cost_Per_Day DECIMAL(10,2)
);

-- Table 4: Regional League Events
CREATE TABLE league_events (
    Event_ID VARCHAR(50) PRIMARY KEY,
    Event_Name VARCHAR(100),
    Region VARCHAR(50),
    Event_Start_Date DATE,
    Event_End_Date DATE,
    Expected_Attendance INT
);

-- Table 5: Fulfillment Orders
CREATE TABLE fulfillment_orders (
    Order_ID VARCHAR(50) PRIMARY KEY,
    Batch_ID VARCHAR(50),
    Center_ID VARCHAR(50),
    Quantity_Shipped INT,
    Transport_Mode VARCHAR(50),
    Shipping_Cost DECIMAL(10,2),
    Ship_Date DATE,
    Delivery_Date DATE
);
GO

-- ==========================================
-- 2. DATA QUALITY AUDIT & ANOMALY DETECTION
-- ==========================================

-- AUDIT 01: Isolate the "Zero-Hour / Negative-Hour" manual data entry overrides
-- Identifies records where the delivery timestamp predates or matches the shipment date
SELECT
    Order_ID,
    Ship_Date,
    Delivery_Date,
    DATEDIFF(day, Ship_Date, Delivery_Date) AS Days_To_Deliver
FROM fulfillment_orders
WHERE Delivery_Date <= Ship_Date;


-- AUDIT 02: Verification filter for raw machine glitches
-- Confirms the footprint of the seeded temperature spikes and purity degradation
SELECT * FROM manufacturing_batches 
WHERE Silicon_Purity_Pct < 85.0;

-- ==========================================
-- 3. ADVANCED ANALYTICS & BUSINESS INSIGHTS
-- ==========================================

-- INSIGHT 01: Manufacturing Defect Root-Cause Analysis
-- Summarizes tests and failures across production lines to isolate systemic line failures
SELECT 
    m.Production_Line,
    m.Item_Type,
    COUNT(*) AS Total_Items_Tested,
    SUM(CASE WHEN i.Quality_Control_Status = 'Failed' THEN 1 ELSE 0 END) AS Total_Failed_Items
FROM item_ledger i
INNER JOIN manufacturing_batches m 
    ON i.Batch_ID = m.Batch_ID
GROUP BY 
    m.Production_Line, 
    m.Item_Type
ORDER BY 
    Total_Failed_Items DESC;


-- INSIGHT 02: Freight Cost & Logistics Mode Optimization
-- Leverages a Common Table Expression (CTE) to aggregate regional shipping performance metrics
WITH RegionalShipping_CTE AS (
    SELECT 
        dc.City,
        fo.Transport_Mode,
        AVG(fo.Shipping_Cost) AS Avg_Shipping_Cost,
        SUM(fo.Shipping_Cost) AS Total_Shipping_Cost
    FROM fulfillment_orders fo
    INNER JOIN distribution_centers dc 
        ON fo.Center_ID = dc.Center_ID
    GROUP BY 
        dc.City, 
        fo.Transport_Mode
)
SELECT 
    City,
    Transport_Mode,
    CAST(Avg_Shipping_Cost AS DECIMAL(10,2)) AS Avg_Shipping_Cost,
    CAST(Total_Shipping_Cost AS DECIMAL(10,2)) AS Total_Shipping_Cost
FROM RegionalShipping_CTE
ORDER BY 
    City, 
    Total_Shipping_Cost DESC;
GO