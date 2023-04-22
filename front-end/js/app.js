//button functionality
const uploadButton = document.getElementById('uploadButton');

//get input file
const fileInput = document.getElementById('fileInput');

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
