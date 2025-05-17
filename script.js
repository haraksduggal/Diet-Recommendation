<script>
        let eegChartInstance;

        async function fetchInitialData() {
            try {
                const response = await fetch("http://127.0.0.1:5000/initial_data");
                const data = await response.json();
                console.log("Initial data fetched:", data);
                updateTwinState(data.state.mood, data.state.energy);
                updateSuggestions(data.suggested_meals);
            } catch (error) {
                console.error("Error fetching initial data:", error);
            }
        }

        async function fetchAndUpdateTwinState() {
            try {
                const response = await fetch("http://127.0.0.1:5000/twin_state");
                const data = await response.json();
                if (data && data.state) {
                    document.getElementById("mood").textContent = data.state.mood;
                    document.getElementById("energy").textContent = data.state.energy;
                }
            } catch (error) {
                console.error("Error fetching twin state:", error);
            }
        }

        async function fetchAndUpdateEEGData() {
            try {
                const response = await fetch('http://127.0.0.1:5000/eeg_data');
                const data = await response.json();
                console.log("EEG Data received:", data);

                if (data && data.eeg && data.eeg.Alpha !== undefined && data.eeg.Beta !== undefined) {
                    const alphaValue = data.eeg.Alpha;
                    const betaValue = data.eeg.Beta;
                    const timestamp = new Date().toLocaleTimeString();

                    // Get the existing chart instance
                    const eegChart = Chart.getChart('eegChart');

                    if (eegChart) {
                        // Chart exists, update its data
                        eegChart.data.labels.push(timestamp); // Add new timestamp
                        eegChart.data.datasets[0].data.push(alphaValue); // Add Alpha value
                        eegChart.data.datasets[1].data.push(betaValue); // Add Beta value
                        eegChart.update(); // Update the chart to re-render
                        console.log("Chart data updated:", { timestamp, alphaValue, betaValue });
                    } else {
                        // Chart doesn't exist, create it (this should only happen once on initial load)
                        const canvas = document.getElementById('eegChart');
                        const eegCtx = canvas.getContext('2d');
                        eegChartInstance = new Chart(eegCtx, {
                            type: 'line',
                            data: {
                                labels: [timestamp], // Start with the first timestamp
                                datasets: [{
                                    label: 'Alpha Wave',
                                    data: [alphaValue], // Start with the first Alpha value
                                    borderColor: 'rgba(75, 192, 192, 1)',
                                    borderWidth: 1,
                                    fill: false,
                                    pointRadius: 5,
                                    pointHoverRadius: 7
                                }, {
                                    label: 'Beta Wave',
                                    data: [betaValue], // Start with the first Beta value
                                    borderColor: 'rgba(255, 99, 132, 1)',
                                    borderWidth: 1,
                                    fill: false,
                                    pointRadius: 5,
                                    pointHoverRadius: 7
                                }]
                            },
                            options: {
                                scales: {
                                    y: {
                                        beginAtZero: true
                                    }
                                },
                                animation: false // Keep animation off for real-time data
                            }
                        });
                        console.log("Chart created with initial data:", { timestamp, alphaValue, betaValue });
                    }
                } else {
                    console.warn("Alpha or Beta wave data not found in the response.");
                }
            } catch (error) {
                console.error("Error fetching EEG data:", error);
            }
        }


        function recordMeal() {
            const meal = document.getElementById("meal-input").value;
            const messageDiv = document.getElementById("meal-message");
            const mealList = document.getElementById("meal-list");
            document.getElementById("meal-input").value = "";

            fetch("http://127.0.0.1:5000/record_meal", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ meal: meal }),
            })
            .then((response) => response.json())
            .then((data) => {
                console.log("Meal recorded:", data);
                messageDiv.textContent = data.message || "Meal recorded!";
                messageDiv.style.color = "green";
                messageDiv.classList.add("show-message");
                setTimeout(() => {
                    messageDiv.textContent = "";
                    messageDiv.classList.remove("show-message");
                }, 3000);

                if (data.meals && Array.isArray(data.meals)) {
                    mealList.innerHTML = "";
                    data.meals.forEach(recordedMeal => {
                        const listItem = document.createElement("li");
                        listItem.textContent = recordedMeal;
                        mealList.appendChild(listItem);
                    });
                } else {
                    const listItem = document.createElement("li");
                    listItem.textContent = meal;
                    mealList.appendChild(listItem);
                }
            })
            .catch((error) => {
                console.error("Error recording meal:", error);
                messageDiv.textContent = "Error recording meal.";
                messageDiv.style.color = "red";
                messageDiv.classList.add("show-message");
                setTimeout(() => {
                    messageDiv.textContent = "";
                    messageDiv.classList.remove("show-message");
                }, 3000);
            });
        }

        function adjustSleep() {
            const sleepHours = document.getElementById("sleep-input").value;
            const messageDiv = document.getElementById("sleep-message");
            const currentSleepSpan = document.getElementById("current-sleep");
            document.getElementById("sleep-input").value = "";

            fetch("http://127.0.0.1:5000/adjust_sleep", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ hours: sleepHours }),
            })
            .then((response) => response.json())
            .then((data) => {
                console.log("Sleep adjusted:", data);
                messageDiv.textContent = data.message || "Sleep adjusted!";
                messageDiv.style.color = "green";
                messageDiv.classList.add("show-message");
                setTimeout(() => {
                    messageDiv.textContent = "";
                    messageDiv.classList.remove("show-message");
                }, 3000);

                if (data.hours !== undefined) {
                    currentSleepSpan.textContent = data.hours;
                } else if (data.sleep !== undefined) {
                    currentSleepSpan.textContent = data.sleep;
                } else {
                    currentSleepSpan.textContent = sleepHours;
                }
            })
            .catch((error) => {
                console.error("Error adjusting sleep:", error);
                messageDiv.textContent = "Error adjusting sleep.";
                messageDiv.style.color = "red";
                messageDiv.classList.add("show-message");
                setTimeout(() => {
                    messageDiv.textContent = "";
                    messageDiv.classList.remove("show-message");
                }, 3000);
            });
        }

        function updateTwinState(mood, energy) {
            document.getElementById("mood").textContent = mood;
            document.getElementById("energy").textContent = energy;
        }

        function updateSuggestions(meals) {
            const mealsContainer = document.getElementById("meals");
            mealsContainer.innerHTML = "";

            if (meals && typeof meals === 'object') {
                if (meals.breakfast) {
                    const breakfastPara = document.createElement("p");
                    breakfastPara.textContent = `Breakfast: ${meals.breakfast}`;
                    mealsContainer.appendChild(breakfastPara);
                }
                if (meals.lunch) {
                    const lunchPara = document.createElement("p");
                    lunchPara.textContent = `Lunch: ${meals.lunch}`;
                    mealsContainer.appendChild(lunchPara);
                }
                if (meals.dinner) {
                    const dinnerPara = document.createElement("p");
                    dinnerPara.textContent = `Dinner: ${meals.dinner}`;
                    mealsContainer.appendChild(dinnerPara);
                }
                if (meals.snacks && Array.isArray(meals.snacks)) {
                    const snacksPara = document.createElement("p");
                    snacksPara.textContent = `Snacks: ${meals.snacks.join(", ")}`;
                    mealsContainer.appendChild(snacksPara);
                }
            } else if (typeof meals === 'string') {
                mealsContainer.textContent = meals;
            }
        }

        // Fetch initial data when the page loads
        fetchInitialData();

        // Periodically update Twin State data (every 3 seconds)
        setInterval(fetchAndUpdateTwinState, 3000);

        // Periodically update EEG data (every 1 second)
        setInterval(fetchAndUpdateEEGData, 1000);
    </script>
