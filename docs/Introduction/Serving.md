# Quickstart

When the package is installed on your system you can quickly deploy your first models to a developement server.

## Serving models locally
Let's look at the code below:

```python
from flaskriver import ClassificationInterface
from flask import Flask
from river import linear_model, metrics

model = linear_model.LogisticRegression()

mae = metrics.MAE()
accuracy = metrics.Accuracy()
metrics = [mae, accuracy]

interface = ClassificationInterface(model, metrics)

app = Flask(__name__)
interface.registerToApp(app)

if __name__ == "__main__":
    app.run(host="localhost", debug=True)
```

After importing all the necessary packages you first have to specify your model along with the metrics you would like to track. For more information on this please look at the [River documentation](https://riverml.xyz).

You can now instantiate a new interface with your model and a list of the metrics to be used. In our case this instance is a ClassificationInterface.

All there is left to do now is to create a Flask app (more information on that can be found on the [Flask website](https://flask.palletsprojects.com/)) and register your Interface to the app object. You can now run the app to spin up the [Werkzeug](https://werkzeug.palletsprojects.com/en/2.2.x/) developement server.

## Sending requests
With the developement server running, your Flask app will now serve three endpoints regarding the model.

- /train
- /predict
- /metric

These endpoints can be reached via an HTTP request. For sending such a request you can either use a GUI-based client like [Postman](https://www.postman.com/) or directly send requests from within python code.

### Training
River models expect the training data in form of a dictionary. This is convenient since the JSON payload of a HTTP request is modeld as a dictionary in python. So when you want to train the model on one data point you will have to send a `POST` request to the /train endpoint with a JSON payload that looks something like this:

```json
{
    "features":{
        "x1":300,
        "x2":210
    },
    "target":false
}
```

The important thing to note is that the keys need to be "features" and "target". The target will obviously be a single value (either a class or a number based on the task you are working on) and the features can consist of many values (based on the data you are working with). When the request is send you will receive a response which will not contain a payload. It will just be a 201 response.

### Predicting
When predicting values with the model you will also have to send a `POST` request. But this time you send it to the /predict endpoint and it will also contain a slightly different payload:

```json
{
    "x1":150,
    "x2":270
}
```

This time you will just send all the features with no key defined. The model will then predict the value and return a response containing the prediction:

```json
{
    "y_pred":false
}
```

### Metrics
For a query of the metrics specified earlier, there is the /metric endpoint. For this one you will have to send a `GET` request and provide no payload. Based on the metrics you specified the response payload may look something like this:

```json
{
    "MAE":0.03009182,
    "Accuracy":0.8912
}
```

Note that these values represent the metrics at this specific point in time. After training on another data point these values will be differen. This enables you to keep track of the metrics live.

## Client example
If you have a dataset ready for training, or got live data coming in you can build a small client for your hosted model pretty easily. The following code is a barebone example using one of the datasets which ship with river:

```python
import requests
from river import datasets

dataset = datasets.Phishing()

train_url = f"http://localhost:5000/train"
metric_url = f"http://localhost:5000/metric"

for x, y in dataset:
    payload = {"features": x, "target": y}
    response = requests.post(train_url, json=payload)

    response = requests.get(metric_url)
    print(response.json())
```

If you run the code the client will iterate through the dataset and send the features along with the target to the /train endpoint. With every iteration it will also retrieve the current values for all the specified metrics and print them on the screen.