$(document).ready(function() {
    setTimeout(function() {
        $('.flashed-messages').fadeOut('slow');
    }, 3000);
});

window.onload = () => {
    const chatGptTextArea = document.getElementById('chatGptTextArea');
    const chatGptSubmitBtn = document.getElementById('chatGptSubmitBtn');
    const loaderOverlay = document.getElementById('loader-overlay');

    chatGptSubmitBtn.addEventListener('click', function() {
        if (chatGptTextArea.value.trim() !== "") {
            loaderOverlay.style.display = "flex";
        }
    });
};

window.addEventListener('pageshow', (event) => {
    if (event.persisted) {
        document.getElementById('loader-overlay').style.display = 'none';
    }
});

function updateButtonState() {
    const userInput = document.getElementById("userInput").value;
    const conversation = document.querySelector(".conversation");
    const sendButton = document.getElementById("sendBtn");
    const clearButton = document.getElementById("clearBtn");

    sendButton.disabled = userInput.trim() === "";
    clearButton.disabled = conversation.innerHTML.trim() === "";
}

document.getElementById("sendBtn").addEventListener("click", function() {
    const sendButton = document.getElementById("sendBtn");
    const originalButtonText = sendButton.textContent;
    const userInput = document.getElementById("userInput").value;

    sendButton.textContent = "Loading...";
    sendButton.disabled = true;

    fetch('/task/gpt', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({prompt: userInput})
    })
    .then(response => response.json())
    .then(data => {
        const qaContainer = document.createElement("div");
        qaContainer.className = "qa-container";

        const userMessage = document.createElement("div");
        userMessage.className = "user-message";
        userMessage.innerHTML = "<strong>User: " + userInput + "</strong>";
        qaContainer.appendChild(userMessage);

        const aiMessage = document.createElement("div");
        aiMessage.className = "assistant-message";
        aiMessage.innerHTML = "<strong>AI:</strong> " + data.response;
        qaContainer.appendChild(aiMessage);

        document.querySelector(".conversation").appendChild(qaContainer);

        sendButton.textContent = originalButtonText;
        sendButton.disabled = false;

        document.getElementById("userInput").value = '';
        updateButtonState();
    })
    .catch(error => {
        console.error('Error:', error);
        sendButton.textContent = originalButtonText;
        sendButton.disabled = false;
    });
});

document.getElementById("clearBtn").addEventListener("click", function() {
    if (window.confirm("Are you sure you want to clear the conversation?")) {
        document.querySelector(".conversation").innerHTML = '';

        fetch('/task/clear_conversation', {
            method: 'POST',
        })
        .then(() => {
            console.log('Conversation cleared on the server.');
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    updateButtonState();
});

document.getElementById("userInput").addEventListener("input", function() {
    updateButtonState();
});

updateButtonState();