# Import necessary libraries
import pickle  # For loading the trained model and scaler
import pandas as pd  # For data manipulation
import numpy as np  # For numerical operations
from flask import Flask, request, render_template  # For deployement

# Load the trained model and scaler
selling_price_model = pickle.load(open("../model/finalprediction.model", "rb"))  # Load the trained selling price prediction model
scaler = pickle.load(open("../model/scaler.pkl", "rb"))  # Load the data scaler used for training

# Load the car data from the CSV file
car_data = pd.read_csv("../databases/cleaned_data.csv")  # Load data from csv

# Get distinct values for Model Name, Fuel Type, and Manufacture Year
distinct_model_names = car_data["name"].unique()  # Get unique car model names from the dataset
distinct_fuel_types = car_data["fuel"].unique()  # Get unique fuel types from the dataset
distinct_manufacture_years = car_data["year"].unique()  # Get unique manufacture years from the dataset

# Create a Flask web application instance
app = Flask(__name__)

# Function to predict selling price
def predict_selling_price(max_power, engine):
    # Create a sample dataframe with the input values
    sample = {
        "max_power": [max_power],
        "engine": [engine]
    }
    sample = pd.DataFrame(sample)

    # Scale the sample using the same scaler used for training
    scaled_sample = scaler.transform(sample)

    # Use the model to predict the selling price
    predicted_selling_price = selling_price_model.predict(scaled_sample)

    # As the target variable was log-transformed during training, we need to exponentiate it
    predicted_selling_price = np.exp(predicted_selling_price)

    return predicted_selling_price[0]

# Define the main route of the web application
@app.route("/", methods=["GET", "POST"])
def index():
    predicted_price = None

    if request.method == "POST":
        try:
            max_power = float(request.form["max_power"])  # Get max power input from the web form
            engine = float(request.form["engine"])  # Get engine size input from the web form
            predicted_price = predict_selling_price(max_power, engine)  # Predict selling price
        except ValueError:
            error_message = "Invalid input. Please enter numeric values for mileage, max power and engine size."

    return render_template("index.html", predicted_price=predicted_price,
                           model_names=distinct_model_names, fuel_types=distinct_fuel_types,
                           manufacture_years=distinct_manufacture_years)

# Run the Flask application if this script is executed directly
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)  # Start the web application with debugging enabled on port 80
