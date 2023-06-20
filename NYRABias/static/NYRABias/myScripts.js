function initializeForm() {
	document.getElementById('raceParams').addEventListener('submit', handleFormSubmit);
}

// Initialize the form when the page is ready
document.addEventListener('DOMContentLoaded', initializeForm);

function updateConditionOptions() {
	var surface = document.getElementById("surface");
	var condition = document.getElementById("condition");
	var selectedValue = surface.value;

	// Clear the existing options in the second select
	condition.innerHTML = "";

	// Add new options based on the selected value of the first select
	if (selectedValue === "Dirt") {
		condition.innerHTML += '<option value="Any">Any</option>';
		condition.innerHTML += '<option value="Fast">Fast</option>';
		condition.innerHTML += '<option value="Off">Good-Sloppy</option>';

	} else {
		condition.innerHTML += '<option value="Any">Any</option>';
		condition.innerHTML += '<option value="Firm">Firm</option>';
		condition.innerHTML += '<option value="Off">Good-Yielding</option>';

	}
}

function updateStartDate() {
	var startDate = document.getElementById("start-date");
	var endDate = document.getElementById("end-date");

	if (new Date(endDate.value) < new Date(startDate.value)) {
		startDate.value = endDate.value;
	}
}

function addFlashEffect() {
	var searchButton = document.querySelector('.search-button');
	var outputItem = document.querySelector('.output-container');

	searchButton.addEventListener('click', function() {
		// Add the flash-effect class
		searchButton.classList.add('flash-effect');
		outputItem.classList.add('flash-effect');

		// Remove the flash-effect class after 300 milliseconds (0.3 seconds)
		setTimeout(function() {
			searchButton.classList.remove('flash-effect');
			outputItem.classList.remove('flash-effect');
		}, 400);
	});
}

document.addEventListener('DOMContentLoaded', addFlashEffect);

function handleFormSubmit(event) {
	event.preventDefault(); // Prevent the form from submitting normally

	var formElements = document.getElementById('raceParams').elements; // Get all form elements

	// Create a query string with the form data
	var queryString = '',
		callFS = '',
		surface = '',
		names = '';

	// Loop through each form element
	for (var i = 0; i < formElements.length; ++i) {
		var element = formElements[i];
		if (element.name === 'call') {
			callFS = element.value
		} else if (element.type !== 'submit') {
			if (element.name === 'condition') {
				names = handleConditionString(element.name, element.value, surface)
			} else {
				if (element.name === 'surface') {
					surface = element.value
				}
				names = handleQueryStrings(element.name, element.value)
			}
			if (Object.keys(names).length !== 0) {
				queryString += names.elemName + '=' + names.elemValue + '&'; // Add the element's name and value to the query string
			}
		}
	}
	// Create a new XMLHttpRequest object
	var xhr = new XMLHttpRequest();

	// Set up the request
	xhr.open('GET', 'get/?' + queryString, true);

	// Define the callback function for when the request is complete
	xhr.onload = function() {
		if (xhr.status === 200) {
			// Handle the successful response
			var response = JSON.parse(xhr.responseText); // Parse the response JSON
			response = handleResponse(response, callFS);

			// Update the input fields with the new values
			document.getElementById('lead').value = response.lead;
			document.getElementById('withinTwo').value = response.withinTwo;
			document.getElementById('twoToFour').value = response.twoToFour;
			document.getElementById('fourToSix').value = response.fourToSix;
			document.getElementById('sixPlus').value = response.sixPlus;
		} else {
			// Handle the error response
			console.error('Request failed. Status:', xhr.status);
		}
	};

	// Send the GET request
	xhr.send();
}

function handleQueryStrings(elemName, elemValue) {
	switch (elemName) {
		case 'fieldSize':
			if (elemValue === '7') {
				elemName = 'fieldSize_gt';
				return {
					elemName,
					elemValue
				};
			} else if (elemValue === '8') {
				elemName = 'fieldSize_lt';
				return {
					elemName,
					elemValue
				};
			}
			  return {};
    case 'maidens':
      if (elemValue !== 'All') {
        return {
          elemName,
          elemValue
        };
      }
        return {};
      default:
        return {
          elemName, elemValue
        };
	}
}

function handleConditionString(elemName, elemValue, surface) {
	if (elemValue === 'Fast' || elemValue === 'Firm') {
		return {
			elemName,
			elemValue
		};
	} else if (elemValue === 'Off') {
		elemName = 'condition_neg';
		if (surface === 'Dirt') {
			elemValue = 'Fast';
		} else {
			elemValue = 'Firm';
		}
		return {
			elemName,
			elemValue
		};
	}
	return {};
}

function handleResponse(response, callFS) {
	let lead = 0,
		withinTwo = 0,
		twoToFour = 0,
		fourToSix = 0,
		sixPlus = 0;
	
	let lengthsBehind = callFS + "LengthsBehind"

	for (var i = 0; i < response.length; ++i) {
		var race = response[i];
		
		if (race[lengthsBehind] < 0.5){
			++lead;
		} else if (race[lengthsBehind] < 2 || race[callFS] <= 3){
			++withinTwo
		} else if (race[lengthsBehind] < 4){
			++twoToFour
		} else if (race[lengthsBehind] < 6){
			++ fourToSix
		} else{
			++sixPlus
		}
	}
	return {
		lead,
		withinTwo,
		twoToFour,
		fourToSix,
		sixPlus
	};
}

