<p align="center">
    <img src="docs/img/text.png" alt="logo">
</p>

<p align="center">
    This is a repository for the open-source project Flaskriver. It combines the lightweight web-framework <a href="https://flask.palletsprojects.com/en/2.2.x/">Flask</a> with the online-ML library <a href="https://github.com/online-ml/river">River</a>. With this project, I want to make deploying online-ML models to the web easier and quicker.
</p>

## Introduction
### Installation
First, you will have to install the package via pip:

```sh
pip3 install flaskriver
```

### Hosting a model
The following code will spin up a development server which is providing a logistic regression model. You can reach its endpoints at:
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

At these endpoints, the app will await the training data as the JSON payload of the request (since river models work with dictionaries). The payload for training the model could look something like this:

```json
{
    "features":{
        "x1":300,
        "x2":210
    },
    "target":false
}
```

The most important thing about the payload for training is the keys "features" and "target". Without these, the model won't know what to learn. Training a model will not return anything but a 201 response (no payload).

The Payload for predicting a value would then look like this:

```json
{
    "x1":100,
    "x2":150
}
```

A request to the prediction endpoint along with a payload like the one shown above would result in a response containing the predicted value under the key "y_pred".

### Sending data to the model
With the following code, you can set up a small client which goes through an entire dataset (the "Phishing" dataset which comes with River) and incrementally trains the model. While training the model the specified metrics will be updated constantly. These metrics can be queried using the /metric endpoint. A request to this endpoint will result in a response containing all the metrics under an identically named key. So in this example, the response payload would contain the two keys "MAE" and "Accuracy" along with their values at this point in time.

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

## More information
### Documentation
You can find more detailed documentation for Flaskriver at <a href="https://flaskriver.ml">flaskriver.ml</a>

### Package
The Package source and build is available on <a href="https://pypi.org/project/flaskriver/">PyPI</a> so that it can be insalled via pip.

### Repository
If you're wondering why there is a .gitlab-ci.yml file in the repository, don't worry. I did not mix up GitLab-CI and GitHub Actions ;) Since I am far more familiar with GitLab-CI I decided to create a repository there for running the automated CI-Pipeline. But with each push/merge to the main branch, all the code will be uploaded to this public GitHub repo as well. There is no extra code in the GitLab repository.

## Contributing
If you would like to contribute something to the project feel free to share your ideas in form of an issue. You can also reach out to me directly via e-mail.