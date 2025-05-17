# 🧠 Diet Recommendor with EEG Integration

This project is a **Digital Twin-based Diet Recommender** system that integrates EEG data analysis and user inputs (meals, sleep) to provide personalized dietary suggestions. Built using **Flask (Python)** for the backend and **HTML/CSS/JavaScript** for the frontend, it visualizes live EEG data and dynamically updates recommendations.

## 🛠 Features

- Real-time EEG wave visualization (Alpha & Beta waves)
- Mood and energy state updates
- Meal logging and suggestion system
- Sleep adjustment tracking
- Responsive and visually styled frontend
- Chart.js integration for live graphing

## 📁 Project Structure

```
.
├── app.py               # Flask backend server
├── digital_twin.py      # Digital Twin logic
├── eeg.py               # EEG data handler
├── eeg_data.csv         # Sample EEG data
├── index.html           # Frontend interface
├── script.js            # Frontend logic
├── style.css            # Styling
└── README.md            # Project documentation
```

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Set Up the Python Environment

Make sure you have Python 3.7+ installed.

```bash
pip install flask pandas
```

### 3. Run the Flask Server

```bash
python app.py
```

The backend will start at: `http://127.0.0.1:5000/`

### 4. Open the Frontend

Open `index.html` in your browser to start using the application.

> Ensure the backend is running to enable full functionality (EEG graph, twin state, etc).

## 📊 Dependencies

- Flask
- pandas
- Chart.js (loaded via CDN)
- Vanilla JS, HTML5, and CSS3

## 🧪 Example Use

- Adjust your sleep hours and record meals.
- Watch your "Twin State" update based on interactions.



- EEG data updates live every second, charted on a line graph.
  
## SCREENSHOTS AND SCREEN RECORDING:

<img width="753" alt="Screenshot 2025-05-18 at 1 00 14 AM" src="https://github.com/user-attachments/assets/51f67db9-6472-4269-a4fc-0f9f2ff47ed9" />
<img width="753" alt="Screenshot 2025-05-18 at 1 00 20 AM" src="https://github.com/user-attachments/assets/8386416e-3297-4484-a860-866ed3753956" />





## 📌 Future Improvements

- Live EEG sensor integration
- User authentication
- Historical data tracking
- Mobile-responsive UI

## 📄 License

MIT License. See `LICENSE` file for details.

---

### 👤 Author

Haraks Duggal
GitHub: haraksduggal
