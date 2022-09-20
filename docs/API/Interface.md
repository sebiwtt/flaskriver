# Interface
The `Interface` class is the superclass for the different kinds of use case-specific interfaces. The `Interface` class itself will not be used by a casual user of this package. 

Classes like [`RegressionInterface`](RegressionInterface.md) will inherit the core functionality from it. `Interface` implements the methods `train()`, `metric()`, `registerToApp()` as well as the `super().__init__()` for the subclasses. If the features of a subclass differ from the superclass implementation the subclass will just overload them. 

The `predict()` method is not implemented in the superclass since this differs in all the use case-specific Interfaces which are implemented for now. This is why it is not specified here.

## Parameters

- **model** - defaults to `None`

    The instance of the River model that the app should serve.

- **metrics** - defaults to `None`

    A list of River metrics that will be used to evaluate the model.

## Methods
The following methods described here are the ones used at the different endpoints.

### train()

The `train()` method will be linked to the /train endpoint. It does not receive any parameters but gets its inputs in form of the JSON payload from the request. The method will update all the metrics by comparing a predicted value with the actual value and then learn the given example. 

**Method parameters**

- None

**Method returns**

- Nothing

### metric()

The `metric()` method will be linked to the /metric endpoint. It does not receive any parameters and no JSON payload from the request. It will iterate over all specified metrics and return them with the response. 

**Method parameters**

- None

**Method returns**

- Nothing

---
The following method is not linked to any endpoint instead it is used to link the methods mentioned above to the corresponding endpoints.

### registerToApp()

The `registerToApp()` method is used to link the different methods of the class to the corresponding endpoints so that they will be served by the Flask application.
It specifies the URLs at which the methods will be available as well as the HTTP Methods which will be used to access them. The URLs can be customized using the `_route_url` parameters. 

**Method parameters**

- **app** (flask.app.Flask)

- **prediction_route_url** (str) - defaults to `"predict"`

- **training_route_url** (str) - defaults to `"train"`

- **metric_route_url** (str) - defaults to `"metric"`

**Method returns**

- Nothing
