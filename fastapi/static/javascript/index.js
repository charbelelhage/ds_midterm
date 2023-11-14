//Function after checking/unchecking Start Time
function toggleStartTime() {
    var startTimeInput = document.getElementById("start_time");
    var startTimeCheckbox = document.getElementById("start_time_checkbox");

    if (!startTimeCheckbox.checked) {
        // startTimeInput.disabled = true;
        startTimeInput.style.display = "none";
        startTimeInput.value = "0";
    }
    else {
        // startTimeInput.disabled = false;
        startTimeInput.style.display = "block";
        startTimeInput.value = "";
    }
}
//Function after checking/unchecking End Time
function toggleEndTime() {
    var endTimeInput = document.getElementById("end_time");
    var endTimeCheckbox = document.getElementById("end_time_checkbox");

    if (!endTimeCheckbox.checked) {
        // endTimeInput.disabled = true;
        endTimeInput.style.display = "none";
        endTimeInput.value = "9999999999";
    }
    else {
        // endTimeInput.disabled = false;
        endTimeInput.value = "";
        endTimeInput.style.display = "block";
    }
}
var pid=0;
const form = document.querySelector('form');
const successMessage = document.getElementById('success-message');
const spinner = document.querySelector('.spinner');
const bagfile = document.getElementById("bagfile");
const startTimeInput = document.getElementById("start_time");
const endTimeInput = document.getElementById("end_time");
const output_folder = document.getElementById("output_folder");
const submit_button = document.getElementById("submit");
const errorMessage = document.getElementById("error-message");
const cancelButton = document.getElementById("cancel");


bagfile.addEventListener('change', (event) => {
    const file = event.target.files[0];
    const extension = file.name.split('.').pop();
    console.log(extension);
    if (extension != "bag") {
        errorMessage.innerHTML = "Only bag files are accepted!"
        errorMessage.style.display = "block";
        submit_button.disabled = true
    } else {
        submit_button.disabled = false;
        errorMessage.style.display = "none";
    }
});

//Listener to call the uploadtest function and wait for the response. It is used to call the API and receive it's response without reloading the whole page.
//PS Anthony: I have commented this function and tried to call the api directly, but the issue persisted.
form.addEventListener('submit', (event) => {
    
    event.preventDefault();
    errorMessage.style.display = "none";
    submit_button.disabled = true;

    //checking if startTime was empty after clicking the submit button even if it was checked
    if (startTimeInput.value == "") {
        startTimeInput.style.display = "none";
        startTimeInput.value = 0;
        document.getElementById("start_time_checkbox").checked = false;
    }
    //checking if EndTime was empty after clicking the submit button even if it was checked
    if (endTimeInput.value == "") {
        endTimeInput.style.display = "none";
        endTimeInput.value = 9999999999;
        document.getElementById("end_time_checkbox").checked = false;

    }
    //Checking if Output folder input was empty even after clicking submit button
    if (output_folder.value == "") {
        output_folder.value = "default/";
    }
    //Display the spinner to the user waiting for the APIs response
    spinner.style.display = 'block';
    //Calling the API function
    fetch('/upload', {
        method: 'POST',
        body: new FormData(event.target),
    })
        .then(response => {
            console.log("response");
            console.log(response);
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Network response was not ok.');
            }
        })
        .then(data => {
            //performing actions after receiving the response from the API.

            //Hide the spinner since we received a response from the API
            spinner.style.display = 'none';
            submit_button.disabled = false;
            console.log(data); // for debugging
            pid=data.pid
            //Check the status of the API's response.
            if (data.status == "success") {
                successMessage.style.display = 'block';
                successMessage.innerHTML = data.message;
                bagfile.value = '';
                startTimeInput.value = "";
                endTimeInput.value = "";
                startTimeInput.style.display = "block";
                endTimeInput.style.display = "block";
                output_folder.value = "";
                start_time_checkbox.checked = true;
                end_time_checkbox.checked = true;
                setTimeout(function () {
                    successMessage.style.display = 'none';
                }, 5000);
                cancelButton.style.display="block";
            }
            else if (data.status == "fail") {
                bagfile.value = '';
                errorMessage.innerHTML = data.message;
                errorMessage.style.display = "block";
            }

        })
        .catch(error => {
            console.error('Error:', error);
        });
});


function callFastAPI() {
    console.log(pid);
  fetch('/terminate-command/' + pid, {
    method: 'POST', // or 'GET' depending on your FastAPI function
    // Add headers and body if required by your FastAPI function
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      // Add any required data for your FastAPI function
    })
  })
  .then(response => response.json())
  .then(data => {
    console.log(data); // Handle the response data from FastAPI
    // Handle the response as needed
    if (data.status == "success") {
        successMessage.style.display = 'block';
        successMessage.innerHTML = data.message;
        setTimeout(function () {
            successMessage.style.display = 'none';
        }, 5000);
        cancelButton.style.display="none";
    }else{
        errorMessage.style.display = 'block';
        errorMessage.innerHTML = data.message;
        setTimeout(function () {
            errorMessage.style.display = 'none';
        }, 5000);
        cancelButton.style.display="none";
    }
  })
  .catch(error => {
    console.error('Error:', error); // Handle any errors
  });
}
