
//DOMContentLoaded event to ensure that the HTML document has been fully loaded
//and parsed before attempting to access any elements
//Task: this code first gets the reference to the button element then it attaches
//an event listender to it which then waits for the "click" event. Finally,
//uploadResume function is executed.
document.addEventListener("DOMContentLoaded", function () {
    //button functionality
    const uploadButton = document.getElementById("uploadButton");
    uploadButton.addEventListener("click", uploadResume);
});


//event listener for button / button functionality
uploadButton.addEventListener('click', () => {
    fileInput.click();
});

//handle file selection
fileInput.addEventListener('change', (event) => {
    const file = event.target.files[0];
    if(file) {
        //TODO: we process the resume here / add gpt4 API usage
        console.log('Selected file: ${file.name}');
    } else {
        console.log('No file selected');
    }
});
