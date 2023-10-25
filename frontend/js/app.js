// Wait until the HTML document is fully loaded before running the JavaScript code
window.addEventListener('DOMContentLoaded', (event) => {
    
    // References to DOM elements
    const uploadButton = document.getElementById('uploadButton');
    const fileInput = document.getElementById('fileInput');
    const feedbackArea = document.getElementById('feedbackArea');
    
    // Trigger the hidden file input when the upload button is clicked
    uploadButton.addEventListener('click', function() {
        fileInput.click();
    });

    // Process the uploaded file when its content changes
    fileInput.addEventListener('change', function() {
        processUploadedFile(this.files[0]);
    });

    /**
     * Process the uploaded file: Extract text from it and get feedback from GPT-4.
     * @param {File} file - The uploaded file object.
     */
    function processUploadedFile(file) {
        // Create a new FileReader to read the content of the uploaded file
        const reader = new FileReader();

        reader.onload = function(evt) {
            sendFileToBackend(evt.target.result)
                .then(data => sendTextForFeedback(data.extractedText))
                .catch(error => console.error('Error during processing:', error));
        };

        // Start reading the uploaded file as a data URL (with MIME type)
        reader.readAsDataURL(file);
    }

    /**
     * Send the file content to the backend for processing.
     * @param {string} fileContent - The content of the uploaded file.
     * @returns {Promise} - A promise resolving with the backend's response.
     */
    function sendFileToBackend(fileContent) {
        return fetch('http://127.0.0.1:5000/process-file', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ fileContent }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Server returned an error");
            }
            return response.json();
        });
    }

    /**
     * Send the extracted text to get feedback from GPT-4.
     * @param {string} input_text - The extracted text from the file.
     */
    function sendTextForFeedback(input_text) {
        fetch('http://127.0.0.1:5000/resume-feedback', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ input_text }),
        })
        .then(response => response.json())
        .then(data => {
            // Display the GPT-4 response in the feedback area
            feedbackArea.textContent = data.reply;
        })
        .catch(error => console.error('Error getting feedback:', error));
    }

});

