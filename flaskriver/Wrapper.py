from flask import request


class FlaskRiver:
    def __init__(self, model):
        self.model = model

    def predict(self):
        payload = request.json
        return self.model.predict(payload)

    def train(self):
        payload = request.json
        self.model.learn_one(payload["features"], payload["target"])
        return {}, 201

    def registerToApp(self, app):
        app.add_url_rule("/predict", "predict", self.predict)
        app.add_url_rule("/train", "train", self.train)
