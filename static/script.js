async function login() {
    const email = document.getElementById('email').value;
    if (!email) {
        alert('Please enter an email');
        return;
    }
    const loadingOtp = document.getElementById('loading-otp');

    if (email.trim() === "") return;

    // Show loading spinner during OTP generation
    loadingOtp.style.display = 'block';

    const response = await fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
    });

    loadingOtp.style.display = 'none';

    const data = await response.json();
    if (data.success) {
        document.getElementById('login-form').style.display = 'none';
        document.getElementById('otp-form').style.display = 'block';
    } else {
        alert('Login failed. Please check your email.');
    }
}

async function verifyOTP() {
    const otp = document.getElementById('otp').value;
    if (!otp) {
        alert('Please enter OTP');
        return;
    }
    const loadingVerify = document.getElementById('loading-verify');

    if (otp.trim() === "") return;

    // Show loading spinner during OTP verification
    loadingVerify.style.display = 'block';

    const response = await fetch('/verify-otp', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ otp })
    });

    loadingVerify.style.display = 'none';

    const data = await response.json();
    if (data.verified) {
        document.getElementById('otp-form').style.display = 'none';
        document.getElementById('chat-container').style.display = 'block';
    } else {
        alert('Invalid OTP. Please try again.');
    }
}

const badWords = ['badword1', 'badword2', 'badword3'];

// Function to filter bad words
function filterBadWords(text) {
    badWords.forEach(word => {
        const regex = new RegExp(word, 'gi'); // Case insensitive match
        text = text.replace(regex, '*'.repeat(word.length));
    });
    return text;
}

// Function to show loading effect (typing indicator)
function showLoading() {
    const chatWindow = document.getElementById('chat-window');
    const loadingMessage = document.createElement('div');
    loadingMessage.classList.add('typing-indicator');
    loadingMessage.innerHTML = '<span>...</span>';
    chatWindow.appendChild(loadingMessage);
    chatWindow.scrollTop = chatWindow.scrollHeight; // Scroll to the bottom
}

// Function to hide loading effect
function hideLoading() {
    const loadingMessage = document.querySelector('.typing-indicator');
    if (loadingMessage) {
        loadingMessage.remove();
    }
}

// Function to send user message and get bot response
async function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    const userId = document.getElementById('email').value;

    if (userInput.trim() === "") return;

    // Filter the message
    const filteredMessage = filterBadWords(userInput);

    // Display user message
    displayMessage(filteredMessage, 'user');

    document.getElementById('user-input').value = '';

    // Show loading effect while waiting for bot response
    showLoading();

    const response = await fetch('/webhook', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, message: filteredMessage })
    });

    hideLoading();

    const data = await response.json();
    displayMessage(data.reply, 'bot');
}


// Function to handle document upload
async function uploadDocument() { 
    const fileInput = document.getElementById('document-input');
    const file = fileInput.files[0];
    const formData = new FormData();

    formData.append('document', file);

    // Show loading spinner during document upload
    showLoading();

    const response = await fetch('/upload-document', {
        method: 'POST',
        body: formData
    });

    hideLoading();

    const data = await response.json();
    displayMessage(data.summary, 'bot');
}

// Function to display messages in the chat window
function displayMessage(message, sender) {
    const chatWindow = document.getElementById('chat-window');
    const messageDiv = document.createElement('div');

    // Add correct class based on sender (user or bot)
    messageDiv.classList.add('message');
    messageDiv.classList.add(sender === 'user' ? 'user' : 'bot');
    messageDiv.textContent = message;

    chatWindow.appendChild(messageDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight; // Scroll to the bottom
}
