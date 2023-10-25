// Wait until the HTML document is fully loaded before running the JavaScript code
window.addEventListener('DOMContentLoaded', (event) => {
    // Get the reference to the upload button element
    const uploadButton = document.getElementById('uploadButton');
    const fileInput = document.getElementById('fileInput');

    uploadButton.addEventListener('click', function() {
        fileInput.click();
    });


    // Attach an event listener to the upload button to handle file uploads
    fileInput.addEventListener('change', function() {
        // When a file is uploaded, get a reference to the file
        const file = this.files[0];
        // Create a new FileReader to read the content of the uploaded file
        const reader = new FileReader();

        // Attach an event listener to the FileReader that triggers when the file has been read
        reader.onload = function(evt) {
            // Send a POST request to the '/process-file' route with the content of the uploaded file
            fetch('http://127.0.0.1:5000/process-file', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ fileContent: evt.target.result }),
            })
            .then(response => response.text())  // First, just get the raw text
            .then(text => {
                console.log("Response text:", text);  // Log the raw response text
                if (!text) {
                    throw new Error("Empty response from server");
                }                
                return JSON.parse(text);  // Try to parse the text as JSON
            })

            
            .then(data => {
                // After the '/process-file' route returns a response, send a POST request to the '/get-gpt-response' route
                // with the extracted text from the uploaded file
                fetch('http://127.0.0.1:5000/resume-feedback', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ input_text: data.extractedText }),
                })
                .then(response => response.json())
                
                .then(data => {
                    // Get the reference to the feedbackArea
                    const feedbackArea = document.getElementById('feedbackArea');
                    
                    // Display the GPT-4 response in the feedback area
                    feedbackArea.textContent = data.reply;
                })
                .catch((error) => {
                    // Log any errors that occur during the '/get-gpt-response' request
                    console.error('Error:', error);
                });
            })
            .catch((error) => {
                // Log any errors that occur during the '/process-file' request
                console.error('Error:', error);
            });
        };

        // Start reading the uploaded file. When done, the 'onload' event listener will be triggered
        // NOTE: remember this reads content of file as data URL INCLUDING a mime type
        reader.readAsDataURL(file);
    });
});
