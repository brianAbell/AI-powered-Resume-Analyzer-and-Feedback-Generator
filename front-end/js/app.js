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

function uploadResume() {
    console.log("Botton clicked!");

    const inputText = "Your prompt text goes here";

    // Call the backend route and process the response
    fetch("/gpt4", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ input: inputText }),
    })
        .then((response) => response.json())
        .then((data) => {
            console.log("GPT-4 response:", data.output);
        })
        .catch((error) => {
            console.error("Error:", error);
        });
}
