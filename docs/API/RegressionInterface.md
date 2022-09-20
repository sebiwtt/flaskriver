# RegressionInterface

The `RegressionInterface` is the Interface to use for regression models. It inherits some core functionality from the [`Interface`](Interface.md) superclass. Therefore you will only find specifications of the methods which are overloaded here. For the other methods please look at the [`Interface`](Interface.md) page.

## Parameters

- **model** - defaults to `None`

    The instance of the River model that the app should serve.

- **metrics** - defaults to `None`

    A list of River metrics that will be used to evaluate the model.

## Endpoints

The URLs for the endpoint can be customized. Read more about this on the [`Interface`](Interface.md) page. The following documentation is valid if you keep the default naming setting for the URLs.

### /train
This endpoint is used for training the model.

**HTTP Method**: `POST`

**Request Payload**

- A JSON Object containing a list of features with the key "features", and a single target value with the key "target".
```json
{
    "features":{
        "x1":300,
        "x2":210
    },
    "target":false
}
```

**Response Payload** 

- No Payload, just a 201 response

### /predict
This endpoint is used for predicting a value.

**HTTP Method**: `POST`

**Request Payload**

- A JSON Object containing a list of features with no key specified.
```json
{
    "x1":300,
    "x2":210
}
```

**Response Payload** 

- A JSON Object containing the predicted value.
```json
{
    "y_pred":true
}
```

### /metric
This endpoint is used for monitoring the metrics of the model.

**HTTP Method**: `GET`

**Request Payload**

- None

**Response Payload** 

- A JSON Object containing the values of all specified metrics with a key corresponding to the name of the metric.

```json
{
    "MAE":0.0309120
}
```

## Methods

### predict()

The `predict()` method will be linked to the /predict endpoint. It does not receive any parameters but gets its inputs in form of the JSON payload from the request. The model will then predict a value which will be returned in the response. Since the model will perform a regression task, the prediction will return a numeric value.

**Method parameters**

- None

**Method returns**

- Nothing

## Example

```python
from flaskriver import RegressionInterface
from flask import Flask
from river import neighbors, metrics

model = neighbors.KNNRegressor()

mae = metrics.MAE()
accuracy = metrics.Accuracy()
metrics = [mae]

interface = RegressionInterface(model, metrics)

app = Flask(__name__)
interface.registerToApp(app)

if __name__ == "__main__":
    app.run(host="localhost", debug=True)

```
