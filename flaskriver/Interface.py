from flask import request, Response
import json


class Interface:
    def __init__(self, model, metrics):
        self.model = model
        self.metrics = metrics

    def predict(self):
        pass

    def train(self):
        payload = request.json
        y = payload["target"]
        x = payload["features"]

        y_pred = self.model.predict_one(x)

        for metric in self.metrics:
            metric.update(y, y_pred)

        self.model.learn_one(x, y)

        return Response({}, status=201, content_type="application/json")

    def metric(self):
        response = {}

        for metric in self.metrics:
            response.update({f"{metric.__class__.__name__}": metric.get()})

        return Response(
            json.dumps(response), status=201, content_type="application/json"
        )

    def registerToApp(
        self,
        app,
        prediction_route_url="predict",
        training_route_url="train",
        metric_route_url="metric",
    ):
        app.add_url_rule(
            f"/{prediction_route_url}", "predict", self.predict, methods=["POST"]
        )
        app.add_url_rule(
            f"/{training_route_url}", "train", self.train, methods=["POST"]
        )
        app.add_url_rule(f"/{metric_route_url}", "metric", self.metric, methods=["GET"])
