from river import neighbors, metrics, datasets
from flaskriver import RegressionInterface
from flask import Flask
from time import sleep
import threading as th
import requests
import pytest


PREDICT_URL = "http://localhost:5001/predict"
TRAIN_URL = "http://localhost:5001/train"
METRIC_URL = "http://localhost:5001/metric"
URL = "127.0.0.1"
PORT = 5001


class Webserver:
    def __init__(self, app):
        self.app = app

    def run(self):
        self.app.run(debug=False, host=URL, port=PORT)


@pytest.fixture(scope="session", autouse=True)
def testSetup():
    model = neighbors.KNNRegressor()

    metric_list = [metrics.MAE()]

    interface = RegressionInterface(model, metric_list)

    app = Flask(__name__)
    interface.registerToApp(app)

    server = Webserver(app)
    Webserver_Thread = th.Thread(target=server.run, daemon=True)
    Webserver_Thread.start()

    sleep(5)


def send_predict_request():
    test_payload = {"x1": 100, "x2": 150}
    return requests.post(PREDICT_URL, json=test_payload)


def send_train_request(x, y):
    test_payload = {"features": x, "target": y}
    return requests.post(TRAIN_URL, json=test_payload)


def send_metric_request_and_assert():
    response = requests.get(METRIC_URL)
    assert_201(response.status_code)

    return response.json()


def assert_201(status):
    assert status == 201, f"Status not matching. Expected: 201, Received {status}"


# --- Testcases ---#


def test_metric_regression():

    dataset = datasets.TrumpApproval()

    before_response = send_metric_request_and_assert()
    assert before_response["MAE"] == 0

    for x, y in dataset:
        send_train_request(x, y)

    after_response = send_metric_request_and_assert()
    assert after_response["MAE"] < 0.5


def test_prediction_regression():

    response = send_predict_request()
    assert_201(response.status_code)


def test_trainig_regression():

    dataset = datasets.TrumpApproval()
    x, y = next(iter(dataset))

    response = send_train_request(x, y)
    assert_201(response.status_code)
