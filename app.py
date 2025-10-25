
from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load the dataset
dataset = pd.read_csv('perfect_diet_plan_dataset.csv')

@app.route('/', methods=['GET', 'POST'])
def input_page():
    if request.method == 'POST':
        # Collect user input
        name = request.form['name']
        age = int(request.form['age'])
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        activity_level = float(request.form['activity_level'])
        diabetic = 'diabetic' in request.form
        high_bp = 'high_bp' in request.form
        liver_disease = 'liver_disease' in request.form

        # Determine health condition
        if diabetic:
            health_condition = "diabetic"
        elif high_bp:
            health_condition = "high_bp"
        elif liver_disease:
            health_condition = "liver_disease"
        else:
            health_condition = "healthy"

        # Match user input with dataset
        diet_plan = get_diet_plan(age, weight, height, activity_level, health_condition)

        return render_template('result.html', name=name, diet_plan=diet_plan)

    return render_template('input.html')


def get_diet_plan(age, weight, height, activity_level, health_condition):
    """
    Finds the best matching diet plan from the dataset based on user input
    and recommends fitness activities.
    """
    # Filter dataset by health condition
    filtered_data = dataset[dataset['health_conditions'] == health_condition]

    # Calculate distance metric for matching (age, weight, height, activity_level)
    filtered_data['distance'] = (
        (filtered_data['age'] - age).abs() +
        (filtered_data['weight'] - weight).abs() +
        (filtered_data['height'] - height).abs() +
        (filtered_data['activity_level'] - activity_level).abs()
    )

    # Find the best match (minimum distance)
    best_match = filtered_data.loc[filtered_data['distance'].idxmin()]

    # Recommend fitness activities based on activity level and health condition
    fitness_activities = recommend_fitness_activities(activity_level, health_condition)

    # Return the diet plan and fitness activities
    return {
        "calorie_needs": best_match['calorie_needs'],
        "breakfast": best_match['breakfast_plan'],
        "lunch": best_match['lunch_plan'],
        "dinner": best_match['dinner_plan'],
        "fitness_activities": fitness_activities
    }


def recommend_fitness_activities(activity_level, health_condition):
    """
    Suggests fitness activities based on activity level and health condition.
    """
    # Base activities
    activities = {
        "low": ["Walking (30 min)", "Yoga (gentle)", "Stretching"],
        "moderate": ["Jogging (30 min)", "Cycling (45 min)", "Bodyweight exercises"],
        "high": ["Running (45 min)", "Swimming", "Strength training"]
    }

    # Adjust activities based on health condition
    if health_condition == "diabetic":
        return activities["low"] + ["Low-impact aerobics", "Light jogging"]
    elif health_condition == "high_bp":
        return activities["low"] + ["Meditation", "Tai Chi"]
    elif health_condition == "liver_disease":
        return activities["low"] + ["Pilates", "Brisk walking"]
    else:  # Healthy
        if activity_level <= 1.375:
            return activities["low"]
        elif activity_level <= 1.55:
            return activities["moderate"]
        else:
            return activities["high"]


if __name__ == '__main__':
    app.run(debug=True)
