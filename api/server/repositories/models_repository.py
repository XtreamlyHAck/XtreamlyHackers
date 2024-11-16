import joblib
import pandas as pd
from pathlib import Path
from server.utils.singleton import singleton


@singleton
class ModelsRepository:
    def __init__(self):
        model_name = 'model_xgb_y_std_60sec.joblib'
        path = Path(f"./server/models/{model_name}")
        self.model = joblib.load(path)

    def predict(self, df: pd.DataFrame) -> dict:
        features = self.model.feature_names_in_
        df = df[df.columns.intersection(features)]
        return self.model.predict(df)
