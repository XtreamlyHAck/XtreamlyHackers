import os
import pandas as pd
from server.utils.singleton import singleton

TRADES_FILE_FEATURES = 'trades_features.feather'


@singleton
class TradesRepository:
    def __init__(self) -> None:
        data_path = os.environ.get("SHARED_DATA_PATH", "./data")
        path = f"{data_path}/{TRADES_FILE_FEATURES}"
        self.df = pd.read_feather(path) if os.path.exists(path) else pd.DataFrame()
        print(f"Loaded {len(self.df)} records from {path}.")
