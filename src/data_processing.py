import pandas as pd
from typing import Dict, List, Tuple

def load_malawi_contacts(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # Ensure columns are properly named
    # Should be: ["contact_time", "day", "id1", "id2"]
    return df

def split_into_days(df: pd.DataFrame) -> Dict[int, pd.DataFrame]:
    """
    Your dataset already has a 'day' column.
    So we can group directly using that.
    """
    days = {day: group for day, group in df.groupby("day")}
    return days

def daily_edge_lists(days: Dict[int, pd.DataFrame]):
    all_ids = set()
    for df_day in days.values():
        all_ids.update(df_day["id1"])
        all_ids.update(df_day["id2"])

    # Create mapping: real_id → new_index
    id_map = {old: new for new, old in enumerate(sorted(all_ids))}

    daily_edges = {}
    for day, df_day in days.items():
        pairs = [
            (id_map[int(i)], id_map[int(j)])
            for i, j in zip(df_day["id1"], df_day["id2"])
        ]
        daily_edges[day] = pairs

    return daily_edges
