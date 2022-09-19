from .Interface import Interface
from flask import request, Response
import json


class RegressionInterface(Interface):
    def __init__(self, model, metrics):
        super().__init__(model, metrics)

    def predict(self):
        payload = request.json

        y_pred = self.model.predict_one(payload)

        response = {"y_pred": y_pred}
        return Response(
            json.dumps(response), status=201, content_type="application/json"
        )
