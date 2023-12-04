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



function fetch_main() {
    event.preventDefault(); // Prevent default form submission

    var selectedCity = $('#cityDropdown').val(); // Get the selected city value

    $.ajax({
        type: 'POST',
        url: '/predict', // The Flask route to handle the prediction
        data: { city: selectedCity }, // Data to send to the server
        success: function (response) {
            // Handle the response here (e.g., update HTML with predictions)
            displayPredictions(response);
        },
        error: function (error) {
            console.log(error); // Handle errors if any
        }
    });
}

// Function to display predictions in the 'predictionResults' div
function displayPredictions(predictions) {
    var resultHTML = '<h3>Predictions:</h3><ul>';
    for (var key in predictions) {
        resultHTML += '<li>' + key + ': ' + predictions[key] + '</li>';
    }
    resultHTML += '</ul>';
    $('#predictionResults').html(resultHTML); // Display predictions in the 'predictionResults' div
}

