document.addEventListener('DOMContentLoaded', () => {
    const sendButton = document.getElementById('send-button');
    const userInput = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');
    const fileUpload = document.getElementById('file-upload');

    sendButton.addEventListener('click', () => {
        const message = userInput.value.trim();
        if (message) {
            addMessage('user', message);
            sendMessage(message);
            userInput.value = '';
        }
    });

    userInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            sendButton.click();
        }
    });

    fileUpload.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            const formData = new FormData();
            formData.append('file', file);

            fetch('/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                addMessage('hermes', data.response);
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
    });

    function addMessage(sender, text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;

        if (sender === 'hermes') {
            typeWriter(messageDiv, text, 50); // Adjust the typing speed here
        } else {
            messageDiv.innerHTML = `<div class="text">${text}</div>`;
        }
    }

    function typeWriter(element, text, speed) {
        let index = 0;
        element.innerHTML = '<div class="text"></div>';
        const typingElement = element.querySelector('.text');
        const cursor = document.createElement('span');
        cursor.className = 'cursor';
        cursor.textContent = '|';
        typingElement.appendChild(cursor);
    
        function type() {
            if (index < text.length) {
                typingElement.innerHTML = text.substring(0, index + 1);
                index++;
                setTimeout(type, speed);
            } else {
                // Remove the cursor when typing is done
                cursor.style.display = 'none';
            }
        }
        type();
    }
    
    function sendMessage(message) {
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
        })
        .then(response => response.json())
        .then(data => {
            addMessage('hermes', data.response);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
});
