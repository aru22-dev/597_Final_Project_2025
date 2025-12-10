import pandas as pd
from typing import Dict, List, Tuple

def load_malawi_contacts(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df

def split_into_days(df: pd.DataFrame) -> Dict[int, pd.DataFrame]:
    """
    Your dataset already has a 'day' column.
    So we can group directly using that.
    """
    days = {day: group for day, group in df.groupby("day")}
    return days

def daily_edge_lists(days: Dict[int, pd.DataFrame]):
    """
    Convert per-day DataFrames into per-day edge lists with
    contiguous integer agent IDs starting from 0.

    The original 'id1' and 'id2' values are remapped into a dense
    range [0, N-1] based on all IDs observed across all days.

    :param days : dict[int, pandas.DataFrame]
        Mapping from day index to a DataFrame with columns 'id1' and 'id2'.

    :return daily_edges : dict[int, list[tuple[int, int]]]
        Mapping from day index to a list of (i, j) contact pairs, where
        i and j are remapped integer agent indices.

    >>> df = pd.DataFrame({
    ...     "day": [1, 1, 2],
    ...     "id1": [10, 11, 12],
    ...     "id2": [20, 21, 22],
    ...     "contact_time": [0, 40, 80],
    ... })
    >>> days = split_into_days(df)
    >>> edges = daily_edge_lists(days)
    >>> sorted(edges.keys())
    [1, 2]
    >>> len(edges[1])
    2
    >>> len(edges[2])
    1
    >>> all_ids = sorted({i for day_edges in edges.values() for pair in day_edges for i in pair})
    >>> all_ids
    [0, 1, 2, 3, 4, 5]
    """
    all_ids = set()
    for df_day in days.values():
        all_ids.update(df_day["id1"])
        all_ids.update(df_day["id2"])

    # Creating mapping: real_id to new_index
    id_map = {old: new for new, old in enumerate(sorted(all_ids))}

    daily_edges = {}
    for day, df_day in days.items():
        pairs = [
            (id_map[int(i)], id_map[int(j)])
            for i, j in zip(df_day["id1"], df_day["id2"])
        ]
        daily_edges[day] = pairs

    return daily_edges
