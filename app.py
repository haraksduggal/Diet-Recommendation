# app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
from digital_twin import DigitalTwin, load_eeg_data  # Import both DigitalTwin class and load_eeg_data function

app = Flask(__name__)
CORS(app)

# Initialize the Digital Twin
# Use the load_eeg_data function to get initial EEG data
initial_eeg_data = load_eeg_data()  # Load initial data using the function from digital_twin.py
twin = DigitalTwin(initial_eeg_data)  # Pass it to the DigitalTwin

# Store recorded meals (in-memory list for this example)
recorded_meals = []

# --------------------------------------------------------------------------------
#  Helper Functions (YOU NEED TO IMPLEMENT THESE with your actual logic)
# --------------------------------------------------------------------------------

def get_initial_mood():
    """
    Returns the initial mood value. Replace this with your actual logic.
    """
    return twin.state.get('mood', 50)  # Get from Digital Twin

def get_initial_energy():
    """
    Returns the initial energy value. Replace this with your actual logic.
    """
    return twin.state.get('energy', 50)  # Get from Digital Twin

def get_suggested_meals():
    """
    Returns the initial suggested meals. Replace with your actual logic.
    """
    return twin.suggested_meals  # Get from Digital Twin

def get_current_mood():
    """
    Returns the current mood value. Replace with your actual logic.
    This is called periodically to update the front-end.
    """
    return twin.get_current_mood()  # Get from Digital Twin instance

def get_current_energy():
    """
    Returns the current energy value. Replace with your actual logic.
    This is called periodically to update the front-end.
    """
    return twin.get_current_energy()  # Get from Digital Twin instance

def get_current_eeg_data():
    """
    Returns the current EEG data. Replace this with your actual logic.
    This is called periodically to update the front-end.
    """
    return twin.get_current_eeg_data()  # Get from Digital Twin

def record_meal(meal):
    """
    Records a meal and returns the updated list of meals.
    """
    print(f"Meal recorded: {meal}")
    recorded_meals.append(meal)
    twin.record_meal(meal) # Update the Digital Twin
    return {"message": f"Meal '{meal}' recorded successfully!", "meals": recorded_meals}

def adjust_sleep(hours):
    """
    Adjusts sleep and returns the hours. Replace with your actual logic.
    """
    print(f"Sleep adjusted by {hours} hours")
    twin.adjust_sleep(hours)  # Update the Digital Twin
    return {"message": f"Sleep adjusted by {hours} hours!", "hours": hours}

# --------------------------------------------------------------------------------
#  Routes (These handle the requests from your front-end)
# --------------------------------------------------------------------------------

@app.route('/initial_data')
def get_initial_data():
    """
    Sends the initial data (mood, energy, meals) when the page loads.
    """
    initial_data = {
        "state": {
            "mood": get_initial_mood(),
            "energy": get_initial_energy()
        },
        "suggested_meals": get_suggested_meals()
    }
    return jsonify(initial_data)

@app.route('/twin_state')
def get_twin_state():
    """
    Sends the current twin state (mood, energy) for updating the UI.
    """
    current_state = {
        "mood": get_current_mood(),
        "energy": get_current_energy()
    }
    return jsonify({"state": current_state})

@app.route('/eeg_data')
def get_eeg_data():
    """
    Sends the current EEG data for the graph.
    """
    eeg_data = get_current_eeg_data()
    return jsonify({"eeg": eeg_data})

@app.route('/record_meal', methods=['POST'])
def record_meal_route():
    """
    Handles recording a meal entered by the user.
    """
    data = request.get_json()
    meal = data.get('meal')
    if not meal:
        return jsonify({"error": "Meal is required"}), 400
    result = record_meal(meal)
    return jsonify(result)

@app.route('/adjust_sleep', methods=['POST'])
def adjust_sleep_route():
    """
    Handles adjusting sleep hours entered by the user.
    """
    data = request.get_json()
    hours = data.get('hours')
    if hours is None:
        return jsonify({"error": "Hours is required"}), 400
    try:
        hours = float(hours)
    except ValueError:
        return jsonify({"error": "Invalid hours value"}), 400
    result = adjust_sleep(hours)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
