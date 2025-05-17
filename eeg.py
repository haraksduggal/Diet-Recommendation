# eeg.py
import time
import random

def simulate_eeg_data():
    """Simulates EEG band power values."""
    delta = 1.0 + random.uniform(-0.2, 0.2)
    theta = 2.5 + random.uniform(-0.5, 0.5)
    alpha = 5.0 + random.uniform(-1.0, 1.0)
    beta = 4.0 + random.uniform(-0.8, 0.8)
    gamma = 1.5 + random.uniform(-0.3, 0.3)
    return {
        'Delta': delta,
        'Theta': theta,
        'Alpha': alpha,
        'Beta': beta,
        'Gamma': gamma
    }

if __name__ == "__main__":
    while True:
        simulated_bands = simulate_eeg_data()
        print("Simulated EEG Bands:", simulated_bands)
        time.sleep(1)  # Simulate data coming in every second
