import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

# ==========================================
# 1. MANUFACTURING BATCHES (Table 1)
# ==========================================
num_batches = 100
batch_data = []
lines = ['Line A', 'Line B', 'Line C']
item_types = ['Poké Ball', 'Great Ball', 'Ultra Ball', 'Potion', 'Super Potion']
start_date = datetime(2026, 1, 1)

for i in range(num_batches):
    batch_id = f"BATCH_{100 + i}"
    item_type = np.random.choice(item_types)
    line = np.random.choice(lines)
    mfg_date = start_date + timedelta(days=int(np.random.randint(0, 90)))
    
    temperature = float(np.random.randint(180, 195))
    silicon_purity = round(float(np.random.uniform(95.0, 99.9)), 2)
    
    if line == 'Line B' and item_type == 'Great Ball':
        temperature = float(np.random.randint(215, 231))
        silicon_purity = round(float(np.random.uniform(75.0, 84.9)), 2)
    
    batch_data.append({
        "Batch_ID": batch_id, "Item_Type": item_type, "Production_Line": line,
        "Manufacture_Date": mfg_date.strftime('%Y-%m-%d'),
        "Machine_Temperature_C": temperature, "Silicon_Purity_Pct": silicon_purity
    })
df_batches = pd.DataFrame(batch_data)

# ==========================================
# 2. ITEM LEDGER (Table 2)
# ==========================================
ledger_data = []
item_serial_counter = 1000
for index, row in df_batches.iterrows():
    batch_id = row['Batch_ID']
    purity = row['Silicon_Purity_Pct']
    for _ in range(3):
        serial_id = f"SN_{item_serial_counter}"
        item_serial_counter += 1
        qc_status = np.random.choice(['Passed', 'Failed'], p=[0.60, 0.40]) if purity < 85.0 else np.random.choice(['Passed', 'Failed'], p=[0.99, 0.01])
        defect_code = 'DF02' if qc_status == 'Failed' else 'None'
        ledger_data.append({
            "Item_Serial_ID": serial_id, "Batch_ID": batch_id,
            "Quality_Control_Status": qc_status, "Defect_Type_Code": defect_code
        })
df_ledger = pd.DataFrame(ledger_data)

# ==========================================
# 3. DISTRIBUTION CENTERS (Table 3)
# ==========================================
centers_data = [
    {"Center_ID": "DC_101", "Region": "Kanto", "City": "Saffron City", "Max_Capacity_Units": 50000, "Operating_Cost_Per_Day": 1200.0},
    {"Center_ID": "DC_102", "Region": "Kanto", "City": "Fuchsia City", "Max_Capacity_Units": 30000, "Operating_Cost_Per_Day": 850.0},
    {"Center_ID": "DC_103", "Region": "Johto", "City": "Goldenrod City", "Max_Capacity_Units": 60000, "Operating_Cost_Per_Day": 1500.0},
    {"Center_ID": "DC_104", "Region": "Johto", "City": "Violet City", "Max_Capacity_Units": 25000, "Operating_Cost_Per_Day": 700.0}
]
df_centers = pd.DataFrame(centers_data)

# ==========================================
# 4. LEAGUE EVENTS (Table 4)
# ==========================================
events_data = [
    {"Event_ID": "EV_01", "Event_Name": "Indigo Plateau Finals", "Region": "Kanto", "Event_Start_Date": "2026-02-10", "Event_End_Date": "2026-02-15", "Expected_Attendance": 25000},
    {"Event_ID": "EV_02", "Event_Name": "Goldenrod Cup", "Region": "Johto", "Event_Start_Date": "2026-03-20", "Event_End_Date": "2026-03-25", "Expected_Attendance": 18000}
]
df_events = pd.DataFrame(events_data)

# ==========================================
# 5. FULFILLMENT ORDERS (Table 5)
# ==========================================
orders_data = []
modes_transport = ['Magnet Train', 'Lapras Cargo', 'Pidgeot Express']

for i in range(100):
    order_id = f"ORD_{5000 + i}"
    linked_batch = df_batches.iloc[np.random.randint(0, len(df_batches))]
    destination_center = df_centers.iloc[np.random.randint(0, len(df_centers))]
    
    ship_date = start_date + timedelta(days=int(np.random.randint(5, 80)))
    days_to_deliver = np.random.randint(2, 6)
    delivery_date = ship_date + timedelta(days=days_to_deliver)
    
    quantity = int(np.random.randint(10, 50)) * 100
    base_shipping_cost = round(float(quantity * np.random.uniform(0.15, 0.30)), 2)
    transport = np.random.choice(modes_transport, p=[0.50, 0.35, 0.15])
    
    # DEMAND SPIKE LOGIC: Connect timelines to events
    is_kanto_spike = (destination_center['Region'] == 'Kanto' and datetime(2026, 2, 1) <= ship_date <= datetime(2026, 2, 12))
    is_johto_spike = (destination_center['Region'] == 'Johto' and datetime(2026, 3, 10) <= ship_date <= datetime(2026, 3, 22))
    
    if is_kanto_spike or is_johto_spike:
        transport = 'Pidgeot Express'  # Emergency rush
        base_shipping_cost = round(base_shipping_cost * np.random.uniform(2.5, 4.0), 2)  # Cost multiplier
        
    # THE DATE TRAP: Injecting the manual "zero/negative hour" entry override error
    if np.random.rand() < 0.06:
        delivery_date = ship_date - timedelta(days=np.random.randint(0, 2))
        
    orders_data.append({
        "Order_ID": order_id, "Batch_ID": linked_batch['Batch_ID'], "Center_ID": destination_center['Center_ID'],
        "Quantity_Shipped": quantity, "Transport_Mode": transport, "Shipping_Cost": base_shipping_cost,
        "Ship_Date": ship_date.strftime('%Y-%m-%d'), "Delivery_Date": delivery_date.strftime('%Y-%m-%d')
    })
df_orders = pd.DataFrame(orders_data)

# Save tables to CSV files so we can load them into SQL Server
df_batches.to_csv('manufacturing_batches.csv', index=False)
df_ledger.to_csv('item_ledger.csv', index=False)
df_centers.to_csv('distribution_centers.csv', index=False)
df_events.to_csv('league_events.csv', index=False)
df_orders.to_csv('fulfillment_orders.csv', index=False)

print("SUCCESS: All 5 tables generated and saved to CSV files!")