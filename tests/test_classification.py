from river import linear_model, metrics, datasets
from flaskriver import ClassificationInterface
from flask import Flask
from time import sleep
import threading as th
import requests
import pytest


PREDICT_URL = "http://localhost:5000/predict"
TRAIN_URL = "http://localhost:5000/train"
METRIC_URL = "http://localhost:5000/metric"
URL = "127.0.0.1"
PORT = 5000


class Webserver:
    def __init__(self, app):
        self.app = app

    def run(self):
        self.app.run(debug=False, host=URL, port=PORT)


@pytest.fixture(scope="session", autouse=True)
def testSetup():
    model = linear_model.LogisticRegression()

    metric_list = [metrics.MSE(), metrics.Accuracy()]

    interface = ClassificationInterface(model, metric_list, predictions="proba")

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


def test_metric_classification():

    dataset = datasets.Phishing()

    before_response = send_metric_request_and_assert()
    assert before_response["MSE"] == 0
    assert before_response["Accuracy"] == 0

    for x, y in dataset:
        send_train_request(x, y)

    after_response = send_metric_request_and_assert()
    assert after_response["MSE"] < 0.5
    assert after_response["Accuracy"] > 0.5


def test_prediction_classification():

    response = send_predict_request()
    assert_201(response.status_code)


def test_trainig_classification():

    dataset = datasets.Phishing()
    x, y = next(iter(dataset))

    response = send_train_request(x, y)
    assert_201(response.status_code)
