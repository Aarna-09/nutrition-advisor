import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle

# Generate synthetic data for demonstration
def create_data():
    data = {
        "age": [20, 25, 30, 35, 40, 45, 50],
        "weight": [60, 65, 70, 75, 80, 85, 90],
        "height": [160, 165, 170, 175, 180, 185, 190],
        "activity_level": [1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8],  # Example activity multipliers
        "calories": [2000, 2200, 2400, 2600, 2800, 3000, 3200]
    }
    return pd.DataFrame(data)

# Load dataset
df = create_data()

# Features and target
X = df[["age", "weight", "height", "activity_level"]]
y = df["calories"]

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a simple regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Save the model to a file
with open('ml_model/calorie_predictor.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Model trained and saved as 'calorie_predictor.pkl'")
