# digital_twin.py
import time
import random
import numpy as np

class DigitalTwin:
    def __init__(self, initial_eeg_data):
        self.initial_eeg_data = initial_eeg_data  # Store initial_eeg_data as an attribute
        self.state = self.initialize_from_eeg(initial_eeg_data)
        self.suggested_meals = {"breakfast": "Oatmeal with berries", "lunch": "Salad with grilled chicken", "dinner": "Baked salmon with vegetables"}
        self.recorded_meals_history = []
        self.sleep_history = []

    def initialize_from_eeg(self, eeg_data):
        beta_theta_ratio = eeg_data.get('Beta', 1) / eeg_data.get('Theta', 1)
        alpha_delta_ratio = eeg_data.get('Alpha', 1) / eeg_data.get('Delta', 1)

        initial_energy = 50 + (beta_theta_ratio - 1) * 10
        initial_mood = 50 + (alpha_delta_ratio - 1) * 10
        return {"energy": max(0, min(100, initial_energy)), "mood": max(0, min(100, initial_mood))}

    def adjust_sleep(self, hours):
        self.sleep_history.append({"time": time.time(), "duration": hours})
        if 6 <= hours <= 9:
            self.state['energy'] = min(100, self.state['energy'] + (hours - 7) * 15)
            self.state['mood'] = min(100, self.state['mood'] + (hours - 7) * 10)
        elif hours < 6:
            self.state['energy'] = max(0, self.state['energy'] - (7 - hours) * 20)
            self.state['mood'] = max(0, self.state['mood'] - (7 - hours) * 15)
        elif hours > 9:
            self.state['energy'] = max(0, self.state['energy'] - (hours - 9) * 10)
            self.state['mood'] = max(0, self.state['mood'] - (hours - 9) * 5)
        print(f"Energy after sleep adjustment: {self.state['energy']}, Mood: {self.state['mood']}")

    def record_meal(self, meal):
        self.recorded_meals_history.append({"time": time.time(), "meal": meal})
        meal = meal.lower()
        if "salad" in meal or "vegetable" in meal:
            self.state['energy'] = min(100, self.state['energy'] + 5)
            self.state['mood'] = min(100, self.state['mood'] + 3)
        elif "burger" in meal or "fries" in meal:
            self.state['energy'] = max(0, self.state['energy'] - 10)
            self.state['mood'] = max(0, self.state['mood'] - 5)
        elif "oatmeal" in meal or "berries" in meal:
            self.state['energy'] = min(100, self.state['energy'] + 8)
            self.state['mood'] = min(100, self.state['mood'] + 6)
        print(f"Energy after meal: {self.state['energy']}, Mood: {self.state['mood']}")

    def get_current_mood(self):
        return self.state['mood'] + random.uniform(-2, 2)

    def get_current_energy(self):
        return self.state['energy'] + random.uniform(-5, 5)

    def get_current_eeg_data(self):
        """Simulates slightly changing EEG data."""
        current_eeg = {}
        for band, value in self.initial_eeg_data.items():  # Now you can access it
            current_eeg[band] = value + random.uniform(-0.5, 0.5)
        return current_eeg

    def suggest_meal(self):
        if self.state['energy'] < 40:
            return "Consider a high-energy snack like nuts or a banana."
        elif self.state['mood'] < 40:
            return "Maybe try some comfort food or something you enjoy."
        else:
            return random.choice(list(self.suggested_meals.values()))

    def suggest_sleep(self):
        if self.state['energy'] < 30 or self.state['mood'] < 30:
            return "You might need more rest. Aim for 7-9 hours of sleep."
        else:
            return "Your sleep seems adequate."

def load_eeg_data():
    """Loads EEG data from a file."""
    try:
        data = np.loadtxt("eeg_data.csv", delimiter=",", skiprows=1)
        if data.ndim == 1:
            eeg_data = {
                "Alpha": data[0],
                "Beta": data[1],
                "Delta": data[2],
                "Theta": data[3],
            }
        else:
            eeg_data = {
                "Alpha": data[0, 0],
                "Beta": data[0, 1],
                "Delta": data[0, 2],
                "Theta": data[0, 3],
            }
        print("Loaded EEG data from CSV:", eeg_data)
        return eeg_data
    except FileNotFoundError:
        print("Error: eeg_data.csv not found. Using dummy data.")
        eeg_data = {
            "Alpha": 8.5,
            "Beta": 22.0,
            "Delta": 2.5,
            "Theta": 5.8,
        }
        return eeg_data
    except Exception as e:
        print(f"Error loading EEG data: {e}. Using dummy data.")
        eeg_data = {
            "Alpha": 8.5,
            "Beta": 22.0,
            "Delta": 2.5,
            "Theta": 5.8,
        }
        return eeg_data

if __name__ == "__main__":
    initial_data = load_eeg_data()
    twin_instance = DigitalTwin(initial_data)
    print("Initial Twin State:", twin_instance.state)

    twin_instance.adjust_sleep(7.5)
    print("State after sleep:", twin_instance.state)

    twin_instance.record_meal("Healthy Salad")
    print("State after meal:", twin_instance.state)
