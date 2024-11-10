const uniqueValues = ['Comedy',
    'Romance',
    'Drama',
    'Adventure',
    'Action',
    'Fantasy',
    'Family',
    'Thriller',
    'Crime',
    'History',
    'Horror',
    'Science Fiction',
    'Animation',
    'TV Movie',
    'War',
    'Music',
    'Mystery',
    'Documentary',
    'Western'];

// Function to create radio buttons
function createCheckboxes(values) {
const checkboxDiv = document.getElementById('checkboxes');

values.forEach(value => {
const checkbox = document.createElement('input');
checkbox.type = 'checkbox';
checkbox.name = "genre";
checkbox.id = value; // Unique ID for the checkbox
checkbox.value = value; // Sets the value for the checkbox

const label = document.createElement('label');
label.htmlFor = value; // Associates label with the checkbox
label.innerText = value;

// Create a custom checkmark
// const checkmark = document.createElement('span');
// checkmark.className = 'checkmark';

// Append the checkbox and label to the div
checkboxDiv.appendChild(checkbox);
checkboxDiv.appendChild(label);
// label.appendChild(checkmark);

});
}

// Call the function to create checkboxes

createCheckboxes(uniqueValues);

// Handle form submission


// document.getElementById('featureForm').addEventListener('submit', function(event) {
// event.preventDefault(); // Prevent form submission
// const selectedValues = Array.from(document.querySelectorAll('input[type="checkbox"]:checked')).map(cb => cb.value);
// const inputDuration = document.getElementById("duration").value;
// const numberDuration = parseInt(inputDuration, 10)

// const min = 60
// const max = 180

// const inputChoice = document.getElementById("choice_input")

// if (selectedValues.length > 3) {
// alert('Please select a maximum of 3 choices.');
// } else if(selectedValues.length < 1){
// alert('Please select at least one genre');
// } else if (isNaN(numberDuration) || inputDuration.trim() === '') {
// alert("Please enter a valid number.");
// } else if (numberDuration < min || numberDuration > max) {
// alert(`Please input duration between ${min} and ${max} minutes.`);
// } 
// else {
//     inputChoice.innerHTML='You tried to make a movie with duration of ' + inputDuration +" minutes with genre(s) of " +selectedValues.join(', ')
// }
// });