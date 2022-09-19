# Flask-River:

<p align="center">
    <img height="220px" src="docs/img/text.png" alt="logo">
</p>

<p align="center">
    This is a repository for the open-source project flaskriver. Flaskriver combines the lightweight web-framework "flask" with the online-ML library <a href="https://github.com/online-ml/river">"river"</a>. For more info on online-ML check out the river repository or the official website.
</p>

## Introduction

First you will have to install the package via pip:

```sh
pip install flaskriver
```

The following code will spin up a developement server which is providing a logistic regression model. You can reach it's endpoints at:
- http://localhost/predict:5000
- http://localhost/train:5000
- http://localhost/metric:5000

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

At these endpoints the app will wait for training data in the json format (since river models work with dictionaries). A JSON body for training the model could look something like this:

```json
{
    "features":{
        "x1":1238,
        "x2":891
    },
    "target":false
}
```

And the JSON body for predicting a value would then just look like this:

```json
{
    "x1":100,
    "x2":150
}
```

With the following code you can set up small client which goes through an entire dataset (the "Phising" dataset which comes with river) and incrementally trains the model and evaluates it's metrics.

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

## Documentation
You can find more detailed documentation for flaskriver at <a href="https://flaskriver.ml">flaskriver.ml</a>.

## Contributing
If you would like to contribute something to the project fell free to share your ideas in form of an issue. You can also reach out to me directly via e-mail or you add me on LinkedIn.