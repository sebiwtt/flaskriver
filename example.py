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

if __name__ == "__main__":
    app.run(host="localhost", debug=True)

# This is a test
