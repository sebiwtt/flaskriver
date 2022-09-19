from .Interface import Interface
from flask import request, Response
import json


class ClassificationInterface(Interface):
    def __init__(self, model, metrics, predictions="class"):
        super().__init__(model, metrics)
        self.predictions = predictions

    def predict(self):
        payload = request.json

        if self.predictions == "class":
            y_pred = self.model.predict_one(payload)

        if self.predictions == "proba":
            y_pred = self.model.predict_proba_one(payload)

        response = {"y_pred": y_pred}
        return Response(
            json.dumps(response), status=201, content_type="application/json"
        )
