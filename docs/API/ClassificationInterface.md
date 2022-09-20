# ClassificationInterface
The `ClassificationInterface` is the Interface to use for classification models. It inherits some core functionality from the [`Interface`](Interface.md) superclass. Therefore you will only find specifications of the methods which are overloaded here. For the other methods please look at the [`Interface`](Interface.md) page.

## Parameters

- **model** - defaults to `None`

    The instance of the River model that the app should serve.

- **metrics** - defaults to `None`

    A list of River metrics that will be used to evaluate the model.

- **predictions** - defaults to `"class"`

    A string defining how to predict values. For classification tasks a model can either predict the class or the probabilities for all the possible classes. 
    
    Options: `"class"`, `"proba"` 

## Endpoints

The URLs for the endpoint can be customized. Read more about this on the [`Interface`](Interface.md) page. The following documentation is valid if you keep the default naming setting for the URLs.

### /train
This endpoint is used for training the model.

**HTTP Method**: `POST`

**Request Payload**

- A JSON Object containig a list of features with the key "features", and a single target value with the key "target".
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

- A JSON Object containig a list of features with no key specified.
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
    "MSE":0.0309120,
    "Accuracy":0.8910812
}
```

## Methods

### predict()

The `predict()` method will be linked to the /predict endpoint. It does not receive any parameters, but gets its inputs in form of the JSON payload from the request. The model will then predict a value which will be returned in the response. Since the model will perform a classification task it will either return one value in form of the predicted class or it will return the probabilites for all the possible classes. You can specify this when instantiating the model by passing the `predictions` parameter.

**Method parameters**

- None

**Method returns**

- Nothing

## Example

```python
from flaskriver import ClassificationInterface
from flask import Flask
from river import linear_model, metrics

model = linear_model.LogisticRegression()

mse = metrics.MSE()
accuracy = metrics.Accuracy()
metrics = [mse, accuracy]

interface = ClassificationInterface(model, metrics, predictions="proba")

app = Flask(__name__)
interface.registerToApp(app)

if __name__ == "__main__":
    app.run(host="localhost", debug=True)

```