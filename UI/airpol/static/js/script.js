const weatherIcons = ["☀️", "🌦️", "🌧️", "❄️", "🌪️", "🌞", "⛈", "🌨", "🌤", "🌫", "🌬", "🌥", "🌛", "🔥", "⚡", "💥", "🌈", "☔", "🌊", "🌌"];

// Define a temperature range for each weather icon
const temperatureRanges = {
    "☀️": { min: 20, max: 35 },
    "🌦️": { min: 15, max: 30 },
    "🌧️": { min: 10, max: 25 },
    "❄️": { min: -5, max: 5 },
    "🌪️": { min: 15, max: 25 },
    "🌞": { min: 25, max: 40 },
    "⛈": { min: 10, max: 20 },
    "🌨": { min: -2, max: 3 },
    "🌤": { min: 22, max: 30 },
    "🌫": { min: 18, max: 28 },
    "🌬": { min: 15, max: 30 },
    "🌥": { min: 20, max: 32 },
    "🌛": { min: 15, max: 25 },
    "🔥": { min: 50, max: 150 },
    "⚡": { min: 15, max: 30 },
    "💥": { min: 150, max: 400 },
    "🌈": { min: 15, max: 25 },
    "☔": { min: 10, max: 20 },
    "🌊": { min: 12, max: 25 },
    "🌌": { min: 10, max: 20 }
};

// Function to change the weather icon and temperature to random values
function changeRandomWeatherIconAndTemperature() {
    const weatherIconElement = document.querySelector('.weather-icon');
    const temperatureElement = document.querySelector('.temperature');

    // Generate a random index to select a weather icon from the array
    const randomIndex = Math.floor(Math.random() * weatherIcons.length);
    const randomIcon = weatherIcons[randomIndex];

    // Get the temperature range for the selected icon
    const temperatureRange = temperatureRanges[randomIcon];

    // Generate a random temperature within the specified range
    const randomTemp = Math.floor(Math.random() * (temperatureRange.max - temperatureRange.min + 1)) + temperatureRange.min;

    // Set the content of the "weather-icon" element to the randomly selected icon
    weatherIconElement.textContent = randomIcon;

    // Set the content of the "temperature" element to the random temperature
    temperatureElement.textContent = randomTemp + "°C";
}

// Assuming yourVariable1 and yourVariable2 contain the new percentage values you want to set for g1 and g2 respectively


