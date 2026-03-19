import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_cluster_data(records=1000):
    np.random.seed(42)
    start_time = datetime.now() - timedelta(days=2)
    
    data = []
    nodes = 5
    
    for i in range(records):
        timestamp = start_time + timedelta(minutes=5 * i)
        
        # Simulate a "Flash Sale" event mid-way through the data
        is_event = 1 if (records // 3 < i < records // 2) else 0
        reach = np.random.randint(5000, 10000) if is_event else 0
        
        # Metrics influenced by the event
        base_load = 0.3 + (is_event * 0.5)
        cpu_util = np.clip(base_load + np.random.normal(0, 0.05), 0, 1)
        
        # Tracing data: Latency spikes when CPU is high or Event is active
        base_latency = 100 # ms
        latency = base_latency + (is_event * 400) + (cpu_util * 200) + np.random.normal(0, 20)
        
        # Label: Required Nodes (What we *should* have had)
        # If latency > 250ms, we needed more nodes
        req_nodes = 5 + (2 if is_event else 0) + (1 if latency > 300 else 0)
        
        data.append({
            "event_timestamp": timestamp,
            "cluster_id": "ocp-prod-01",
            "cpu_utilization": round(cpu_util, 3),
            "p99_latency_ms": round(latency, 2),
            "event_type": "flash_sale" if is_event else "none",
            "expected_reach": reach,
            "required_node_count": int(req_nodes) # The LABEL for training
        })
        
    return pd.DataFrame(data)

# Generate and save
df = generate_cluster_data()
df.to_parquet("cluster_metrics.parquet")
print("Sample Data Generated: cluster_metrics.parquet")
print(df.head())
