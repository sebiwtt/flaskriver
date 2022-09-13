import threading as th
from time import sleep
import pytest


URL = "127.0.0.1"
PORT = 5000


class KillableWebserver:
    def __init__(self, app):
        self.app = app

    def run(self):
        self.app.run(debug=False, host=URL, port=PORT)

    def terminate(self):
        self.__del__()


@pytest.fixture(scope="session", autouse=True)
def testSetup():
    from flaskriver.Wrapper import FlaskRiver
    from flask import Flask
    from river import linear_model, metrics

    model = linear_model.LogisticRegression()

    mse = metrics.MSE()
    accuracy = metrics.Accuracy()
    metrics = [mse, accuracy]

    flaskriver = FlaskRiver(model, metrics, predictions="proba")

    app = Flask(__name__)
    flaskriver.registerToApp(app)

    server = KillableWebserver(app)

    Webserver_Thread = th.Thread(target=server.run, daemon=True)
    Webserver_Thread.start()

    sleep(5)


def test_prediction_classification():
    import requests

    test_url = f"http://localhost:{PORT}/predict"
    test_payload = {"x1": 100, "x2": 150}

    response = requests.post(test_url, json=test_payload)

    status = response.status_code

    assert (
        status == 201
    ), f"Status not matching. Expected: 201, Received {response.status_code}"


def test_trainig_classification():
    import requests
    from river import datasets

    dataset = datasets.Phishing()

    test_url = f"http://localhost:{PORT}/train"

    mse = 1

    for x, y in dataset:
        test_payload = {"features": x, "target": y}
        response = requests.post(test_url, json=test_payload)

        status = response.status_code
        assert (
            status == 201
        ), f"Status not matching. Expected: 201, Received {response.status_code}"

        response_json = response.json()
        mse = response_json["MSE"]
        assert mse

    assert mse < 0.5
