from flask import request, jsonify, Response
import json


class FlaskRiver:
    def __init__(self, model, metrics, predictions="class"):
        self.model = model
        self.metrics = metrics
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

    def train(self):
        payload = request.json
        y = payload["target"]
        x = payload["features"]

        y_pred = self.model.predict_one(x)

        response = {"y_pred": y_pred, "y_actual": y}

        for metric in self.metrics:
            metric.update(y, y_pred)
            response.update({f"{metric.__class__.__name__}": metric.get()})

        self.model.learn_one(x, y)

        return Response(
            json.dumps(response), status=201, content_type="application/json"
        )

        self.model.learn_one(payload["features"], payload["target"])

    def registerToApp(
        self, app, prediction_route_url="predict", training_route_url="train"
    ):
        app.add_url_rule(
            f"/{prediction_route_url}", "predict", self.predict, methods=["GET"]
        )
        app.add_url_rule(
            f"/{training_route_url}", "train", self.train, methods=["POST"]
        )
