from server.repositories.trades_repository import TradesRepository
from server.repositories.models_repository import ModelsRepository
from server.utils.singleton import singleton
from fastapi import HTTPException


@singleton
class PolicyService:
    def __init__(self):
        self.models_repository = ModelsRepository()
        self.repository = TradesRepository()

    @staticmethod
    def _raise_error():
        msg = f"No data found for prediction"
        raise HTTPException(status_code=404, detail=msg)

    def predict(self):
        data = self.get_data()
        if data.empty:
            self._raise_error()

        predictions = self.models_repository.predict(data)

        return {'predictions': predictions.tolist()}

    def policy(self):
        prediction = self.predict()['predictions'].pop()

        return {
            'open': prediction < 0.002,
            'close': prediction > 0.002
        }

    def get_data(self):
        return self.repository.df
