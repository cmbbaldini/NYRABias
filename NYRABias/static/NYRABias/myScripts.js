function updateConditionOptions() {
    var surface = document.getElementById("surface");
    var condition = document.getElementById("condition");
    var selectedValue = surface.value;

    // Clear the existing options in the second select
    condition.innerHTML = "";

    // Add new options based on the selected value of the first select
    if (selectedValue === "Dirt") {
    condition.innerHTML += '<option value="Fast">Fast</option>';
    condition.innerHTML += '<option value="Off">Off</option>';
    condition.innerHTML += '<option value="All">All</option>';
    }
    else if (selectedValue === "Turf" || "Innerturf") {
    condition.innerHTML += '<option value="Firm">Firm</option>';
    condition.innerHTML += '<option value="Off">Off</option>';
    condition.innerHTML += '<option value="All">All</option>';
    }  
}

function handleFormSubmit(event) {
    event.preventDefault(); // Prevent the form from submitting normally
    
    var formElements = document.getElementById('raceParams').elements; // Get all form elements
    
    // Create a query string with the form data
    var queryString = '';
    var callFS = ''
    
    // Loop through each form element
    for (var i = 0; i < formElements.length; ++i) {
      var element = formElements[i];
      if (element.type !== 'submit') {
        if (element.name === 'call'){
            callFS = element.value
            console.log(callFS)
        }
        else {
            let names = handleQueryStrings(element.name, element.value)
            if (Object.keys(names).length !== 0){
                queryString += names.elemName + '=' + names.elemValue + '&'; // Add the element's name and value to the query string
                console.log(names.elemName)
                console.log(names.elemValue)
            }
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
        document.getElementById('twoToSix').value = response.twoToSix;
        document.getElementById('sixPlus').value = response.sixPlus;
      } else {
        // Handle the error response
        console.error('Request failed. Status:', xhr.status);
      }
    };
    
    // Send the GET request
    xhr.send();
  }
  
  function initializeForm() {
    document.getElementById('raceParams').addEventListener('submit', handleFormSubmit);
  }
  
  // Initialize the form when the page is ready
  document.addEventListener('DOMContentLoaded', initializeForm);

function handleQueryStrings(elemName, elemValue){
    switch (elemName) {
        case 'condition':
            if (elemValue !== 'All'){
                return {elemName, elemValue} 
            }
            return {}
        case 'fieldSize':
            if (elemValue === 7){
                elemName = 'fieldSize_gt'
                return {elemName, elemValue}
            }
            else if (elemValue === 8){
                elemName = 'fieldSize_lt'
                return {elemName, elemValue}
            }
            return {}
        case 'maidens':
            if (elemValue !== 'All'){
                return {elemName, elemValue}
            }
            return {}
        default:
            return {elemName, elemValue}
      }
}

function handleResponse(response, callFS) {
    let lead = 0,
      withinTwo = 0,
      twoToSix = 0,
      sixPlus = 0;
  
    for (var i = 0; i < response.length; ++i) {
      var race = response[i];
      switch (race[callFS]) {
        case 1:
          ++lead;
          break;
        case 2:
          ++withinTwo;
          break;
        case 3:
          ++twoToSix;
          break;
        default:
          ++sixPlus;
          break;
      }
    } 
    return {lead, withinTwo, twoToSix, sixPlus};
  }