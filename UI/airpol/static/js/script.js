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

// Function to fetch temperature from the server
function fetchTemperature() {
    var city = $('#cityDropdown').val();

    console.log("City Name:", city);

    $.ajax({
        type: 'POST',
        url: '/get_temperature',
        data: JSON.stringify({ city: city}),
        contentType: 'application/json;charset=UTF-8',
        success: function(response) {


            let temp = response.temperature;
            $('#Temprature').html(`Current Temperature in ${city} is ${response.temperature}°C`);
            console.log(`Current Temperature in ${city} is ${response.temperature}°C`);
            let yourVariable2 = temp;
            let g2Element = document.querySelector('#g2');
        
            g2Element.style.setProperty('--fill-percentage', yourVariable2);
        
            document.querySelector('#g2 .progress-text').textContent = `${yourVariable2}°C`;
            document.querySelector('.temperature').textContent = `${yourVariable2}°C`;            

            updateWeatherIconAndTemperature(temp);
        },
        error: function(error) {
            $('#Temprature').html('Error fetching temperature. Please try again.');
            console.log('Error fetching temperature. Please try again.');
        }
    });

}

//
function displayHaiku(weather) {
    let description = weather.weather[0].description.toLowerCase();
    let haiku = '';

    // Conditions to associate haikus with weather descriptions
    if (description.includes('clear')) {
        haiku = "Golden rays embrace,\nNature's canvas painted bright,\nSerenade of warmth.";
    } else if (description.includes('clouds')) {
        haiku = "Whispers in the sky,\nVeiled hues, a misty ballet,\nSecrets softly told.";
    } else if (description.includes('rain')) {
        haiku = "Pitter-patter sounds,\nEarth's symphony in the rain,\nDance of life renewed.";
    } else if (description.includes('thunderstorm')) {
        haiku = "Thunder's booming voice,\nNature's grand electric show,\nPower in the sky.";
    } else if (description.includes('drizzle')) {
        haiku = "Gentle droplets fall,\nWhispering secrets softly,\nEarth's gentle lullaby.";
    } else if (description.includes('snow')) {
        haiku = "Silent flakes descend,\nBlanketing the world in white,\nSoftly kissing Earth.";
    } else if (description.includes('mist') || description.includes('fog')) {
        haiku = "Veiled in mystery,\nMist draped whispers through the air,\nNature's quiet cloak.";
    } else if (description.includes('haze')) {
        haiku = "Veil of smoky haze,\nSoftening edges of day,\nNature's tranquil breath.";
    } else {
        haiku = "Weather's mystery,\nNature's symphony of change,\nBeauty in motion.";
    }

    // Display the selected haiku in the HTML element
    document.getElementById('haikuElement').innerText = haiku;
}
function fetchWeather() {
    let city = $('#cityDropdown').val(); // Get the selected city value from the dropdown
    let firstWord = city.split(' ')[0]; // Extract the first word of the city name

    // Make an API call to fetch weather data for the first word of the city
    $.ajax({
        type: 'POST',
        url: '/get_weather', // Flask route to handle weather data retrieval
        data: { city: firstWord }, // Data to send to the server (first word of the city)
        success: function(response) {
            // Handle the weather data response here
            displayHaiku(response); // Display the haiku based on weather description
        },
        error: function(error) {
            console.log('Error fetching weather data. Please try again.');
        }
    });
}

//


// Function to update weather icon and temperature based on fetched temperature
function updateWeatherIconAndTemperature(temperature) {
    const weatherIconElement = document.querySelector('.weather-icon');
    const temperatureElement = document.querySelector('.temperature');

    // Default icon if temperature does not fall within defined ranges
    let selectedIcon = '☀️';

    // Find the appropriate weather icon based on the fetched temperature
    for (const icon in temperatureRanges) {
        if (temperature >= temperatureRanges[icon].min && temperature <= temperatureRanges[icon].max) {
            selectedIcon = icon;
            break;
        }
    }

    // Set the content of the "weather-icon" element to the selected icon
    weatherIconElement.textContent = selectedIcon;

    // Set the content of the "temperature" element to the fetched temperature
    temperatureElement.textContent = `${temperature}°C`;

    // Update any additional elements or styles based on the fetched temperature if needed
    // For example, modifying the color or styles based on temperature, etc.
}

///.....................................................................................



function savePredictionsToStorage(predictions) {
    // Convert predictions to JSON string
    const predictionsJSON = JSON.stringify(predictions);

    // Store in localStorage
    localStorage.setItem('predictedValues', predictionsJSON);
}

function getPredictionsFromStorage() {
    // Retrieve the JSON string from localStorage
    const predictionsJSON = localStorage.getItem('predictedValues');

    // Parse JSON string to object
    const predictions = JSON.parse(predictionsJSON);

    // Return the predictions object
    return predictions;
}




///.....................................................................................

let predictionsReceived = false; // Initialize boolean variable
let selectedCity = ''; // Initialize selectedCity variable


function fetchAndDisplayPredictions(selectedCity) {
    $.ajax({
        type: 'POST',
        url: '/predict',
        data: { city: selectedCity },
        success: function (response) {
            // Handle the received predictions
            displayPredictions(response);
        },
        error: function (error) {
            console.log(error); // Handle errors if any
        }
    });
}

function displayPredictions(predictions) {



// Store parsed values in variables
const parsedSO2 = parseFloat(predictions.SO2);
const parsedNO2 = parseFloat(predictions.NO2);
const parsedCO = parseFloat(predictions.CO);
const parsedPM25 = parseFloat(predictions['PM2.5']);
const parsedO3 = parseFloat(predictions.O3);
const parsedOverallAQI = parseFloat(predictions.Overall_AQI);

// Display parsed values in console
console.log(`Parsed SO2: ${parsedSO2}`);
console.log(`Parsed NO2: ${parsedNO2}`);
console.log(`Parsed CO: ${parsedCO}`);
console.log(`Parsed PM2.5: ${parsedPM25}`);
console.log(`Parsed O3: ${parsedO3}`);
console.log(`Parsed Overall AQI: ${parsedOverallAQI}`);

  $('#predictedSO2').text(`Predicted SO2: ${formatValue(predictions.SO2)}`);
  
  $('#predictedNO2').text(`Predicted NO2: ${formatValue(predictions.NO2)}`);

  $('#predictedCO').text(`Predicted CO: ${formatValue(predictions.CO)}`);
 
  $('#predictedPM25').text(`Predicted PM2.5: ${formatValue(predictions['PM2.5'])}`);

  $('#predictedO3').text(`Predicted O3: ${formatValue(predictions.O3)}`);

  $('#overallAQI').text(`Overall predicted AQI: ${formatValue(predictions.Overall_AQI)}`);

  
}

function showMainFrame() {
    const mainFrame = document.getElementById('main-frame');
    mainFrame.style.display = 'block'; // Show main frame
}

// Assuming this function is triggered when a city is selected
function fetch_main() {
    let selectedCity = $('#cityDropdown').val(); // Get the selected city value

    // Fetch and display predictions for the selected city
    fetchAndDisplayPredictions(selectedCity);
}
