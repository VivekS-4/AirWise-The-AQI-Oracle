const weatherIcons = ["☀️", "🌦️", "🌧️", "❄️", "🌪️", "🌞", "⛈", "🌨", "🌤", "🌫", "🌬", "🌥", "🌛", "🔥", "⚡", "💥", "🌈", "☔", "🌊", "🌌"];

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

function fetchTemperature() {
    let city = $('#cityDropdown').val();

    $.ajax({
        type: 'POST',
        url: '/get_temperature',
        data: JSON.stringify({ city: city }),
        contentType: 'application/json;charset=UTF-8',
        success: function (response) {
            let temp = response.temperature;
            $('#Temprature').html(`Current Temperature in ${city} is ${response.temperature}°C`);
            let yourVariable2 = temp;
            let g2Element = document.querySelector('#g2');

            g2Element.style.setProperty('--fill-percentage', yourVariable2);
            document.querySelector('#g2 .progress-text').textContent = `${yourVariable2}°C`;
            document.querySelector('.temperature').textContent = `${yourVariable2}°C`;

            updateWeatherIconAndTemperature(temp);
        },
        error: function (error) {
            $('#Temprature').html('Error fetching temperature. Please try again.');
            console.log('Error fetching temperature. Please try again.');
        }
    });
}

function getWeatherForCity() {

    const weatherData = {
        "weather": [
          {
            "description": "clear"
          },
          {
            "description": "overcast clouds"
          },
          {
            "description": "rain"
          },
          {
            "description": "thunderstorm"
          },
          {
            "description": "drizzle"
          },
          {
            "description": "snow"
          },
          {
            "description": "mist"
          },
          {
            "description": "fog"
          },
          {
            "description": "haze"
          }
        ]
      };
      
      // Call the displayHaiku function with weather data
      const randomIndex = Math.floor(Math.random() * weatherData.weather.length);
      return weatherData.weather[randomIndex].description;
      
  }

  const randomWeatherDescription = getRandomWeatherDescription();

function getSelectedCityWeather() {
    const cityDropdown = document.getElementById('cityDropdown');
    const selectedCity = cityDropdown.value;
  
    // Call getWeatherForCity with the selected city name
    getWeatherForCity(selectedCity);
  }


function displayHaiku(randomWeatherDescription) {
    
    let description = weatherDescription.toLowerCase();
    let haiku = '';

    // Conditions to associate haikus with weather descriptions
    if (description.includes('clear')) {
        haiku = "Golden rays embrace,\nNature's canvas painted bright,\nSerenade of warmth.";
    } else if (description.includes('clouds')|| description.includes('overcast')) {
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
    let city = $('#cityDropdown').val().split(' ')[0];

    $.ajax({
        type: 'POST',
        url: '/get_weather',
        data: { city: city },
        success: function (response) {
            displayHaiku(response);
            console.log(response);
        },
        error: function (error) {
            console.log('Error fetching weather data. Please try again.');
        }
    });
}

function updateWeatherIconAndTemperature(temperature) {
    const weatherIconElement = document.querySelector('.weather-icon');
    const temperatureElement = document.querySelector('.temperature');
    let selectedIcon = '☀️';

    for (const icon in temperatureRanges) {
        if (temperature >= temperatureRanges[icon].min && temperature <= temperatureRanges[icon].max) {
            selectedIcon = icon;
            break;
        }
    }

    weatherIconElement.textContent = selectedIcon;
    temperatureElement.textContent = `${temperature}°C`;
}

function predict() {
    showMainFrame();
    
    // Assuming you have a function fetchDataFromCSV() to fetch data from the CSV file
    fetchDataFromCSV()
        .then(data => {
            // Display pollutant values
            document.getElementById('city').textContent = `City: ${data.city}`;
            document.getElementById('SO2').textContent = `SO2: ${data.SO2}`;
            document.getElementById('NO2').textContent = `NO2: ${data.NO2}`;
            document.getElementById('CO').textContent = `CO: ${data.CO}`;
            document.getElementById('PM25').textContent = `PM25: ${data.PM25}`;
            document.getElementById('O3').textContent = `O3: ${data.O3}`;
            document.getElementById('overallAQI').textContent = `Overall AQI: ${data.overallAQI}`;

            
            // Compare pollutant values for minimum and maximum
            let minPollutant = '';
            let maxPollutant = '';
            let minVal = Number.MAX_VALUE; // Initialize to a very large number
            let maxVal = Number.MIN_VALUE; // Initialize to a very small number

            // Compare each pollutant value and update min/max values
            if (data.SO2 < minVal) {
                minVal = data.SO2;
                minPollutant = 'SO2';
            }
            if (data.SO2 > maxVal) {
                maxVal = data.SO2;
                maxPollutant = 'SO2';
            }

            if (data.NO2 < minVal) {
                minVal = data.NO2;
                minPollutant = 'NO2';
            }
            if (data.NO2 > maxVal) {
                maxVal = data.NO2;
                maxPollutant = 'NO2';
            }

            // Continue the comparisons for CO, PM25, O3, etc.

            // Display the minimum and maximum pollutants in respective divs
            if (minPollutant !== '') {
                document.querySelector('.box-5 h2').textContent = 'Current Low';
                document.querySelector('.box-5 p').textContent = minPollutant;
                document.querySelector('.box-5 .num').textContent = `${minVal} PPM`;
            }

            if (maxPollutant !== '') {
                document.querySelector('.box-3 h2').textContent = 'Current High';
                document.querySelector('.box-3 p').textContent = maxPollutant;
                document.querySelector('.box-3 .num').textContent = `${maxVal} PPM`;
            }
            
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}

function displayAQIAdvice(aqi) {
    let allages = '';
    let elderly = '';
    let health_is = '';
    let joke = '';
    if (aqi <= 0.2) {
        allages = "For all age groups: Enjoy outdoor activities, air quality is good.";
        joke = "Silent flakes descend, painting the world white. Time for cozy warmth and wonder.";
    } else if (aqi <= 1) {
        allages = "For all age groups: Air quality is moderate. Consider reducing prolonged outdoor activities.";
        joke = "Pitter-patter sounds, nature's symphony in the rain. Dance and rejuvenate!";
    } else if (aqi <= 1.4) {
        allages = "For all age groups: Air quality is unhealthy for sensitive groups. Avoid prolonged outdoor exertion.";
        joke = "A misty ballet of clouds awaits! Perfect weather for contemplation.";
    } else {
        allages = "For all age groups: Air quality is unhealthy. Avoid outdoor activities.";
        joke = "Clear skies, open spaces! Embrace the warmth and nature's beauty.";
    }

    if (aqi <= 0.2) {
        elderly += "\n\nFor the elderly: No particular precautions advised.";
    } else if (aqi <= 1) {
        elderly += "\n\nFor the elderly: Consider limiting outdoor activities.";
    } else if (aqi <= 1.4) {
        elderly += "\n\nFor the elderly: Limit outdoor activities and stay indoors when possible.";
    } else {
        elderly += "\n\nFor the elderly: Avoid outdoor activities. Stay indoors.";
    }

    if (aqi <= 0.2) {
        health_is += "\n\nFor those with health issues: No particular precautions advised.";
    } else if (aqi <= 1) {
        health_is += "\n\nFor those with health issues: Reduce prolonged outdoor exertion.";
    } else if (aqi <= 1.4) {
        health_is += "\n\nFor those with health issues: Limit outdoor exertion and stay indoors when possible.";
    } else {
        health_is += "\n\nFor those with health issues: Avoid outdoor activities. Stay indoors.";
    }
    // Display the advice in the HTML element
    document.getElementById('id_allages').innerText = allages;
    document.getElementById('id_elderly').innerText = elderly;
    document.getElementById('id_health_is').innerText = health_is;
    document.getElementById('id_joke').innerText = joke;
    return allages, elderly, health_is, joke;
}

// Fetch data from the CSV file
function fetchDataFromCSV() {
    return fetch('/get_csv_data')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch CSV data');
            }
            return response.text(); // Fetch as plain text
        })
        .then(csvData => {
            // Split the CSV data into rows
            const rows = csvData.trim().split('\n');

            // Split the header row into column names
            const columns = rows[0].split(',');

            // Create an array to hold the data
            const data = [];

            // Loop through the rows (excluding the header)
            for (let i = 1; i < rows.length; i++) {
                const values = rows[i].split(',');

                // Create an object to store the row data
                const rowData = {};

                // Assign values to the corresponding columns
                for (let j = 0; j < columns.length; j++) {
                    rowData[columns[j]] = values[j];
                }

                // Add the row data to the array
                data.push(rowData);
            }

            // Log the parsed data (for verification)
            console.log(data);

            // Display data in HTML or update elements as needed
            const predictionResultsDiv = document.getElementById('predictionResults');
            if (predictionResultsDiv) {
                for (let i = 0; i < columns.length; i++) {
                    const columnName = columns[i];
                    const columnValue = data[0][columnName]; // Accessing first row data

                    // Create a new paragraph element
                    const paragraph = document.createElement('p');
                    paragraph.textContent = `${columnName}: ${columnValue}`;

                    // Append the paragraph to the predictionResultsDiv
                    predictionResultsDiv.appendChild(paragraph);
                }
            }
            
            // Return the parsed data if needed further
            return data;
        })
        .catch(error => {
            console.error('Error fetching CSV data:', error);
            throw new Error('Failed to fetch CSV data');
        });
}

function updateAQIAdviceFromCSV() {
    fetchDataFromCSV()
        .then(data => {
            let aqi = data.overallAQI; // Assuming overallAQI is the AQI value in your CSV
            let advice = displayAQIAdvice(aqi);
            document.getElementById('aqiAdvice').innerText = advice;
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}



let predictionsReceived = false;
let selectedCity = '';

function fetchAndDisplayPredictions(selectedCity) {
    $.ajax({
        type: 'POST',
        url: '/predict',
        data: { city: selectedCity },
        success: function (response) {
            predict();
        },
        error: function (error) {
            console.log(error);
        }
    });
}

function fetch_main() {
    let selectedCity = $('#cityDropdown').val();
    fetchAndDisplayPredictions(selectedCity);
}

function showMainFrame() {
    const mainFrame = document.getElementById('main-frame');
    mainFrame.style.display = 'block'; // Show main frame
}