document.addEventListener('DOMContentLoaded', function () {
    console.log('Chatbot script loaded');

    // Get DOM elements
    const chatbotToggle = document.getElementById('chatbotToggle');
    const chatbotBox = document.getElementById('chatbotBox');
    const closeChatbot = document.getElementById('closeChatbot');
    const userInput = document.getElementById('userInput');
    const sendMessage = document.getElementById('sendMessage');
    const chatMessages = document.getElementById('chatMessages');

    console.log('Elements found:', {
        chatbotToggle,
        chatbotBox,
        closeChatbot,
        userInput,
        sendMessage,
        chatMessages
    });

    if (chatbotToggle) {
        chatbotToggle.onclick = function () {
            console.log('Toggle clicked');
            if (chatbotBox.style.display === 'none' || chatbotBox.style.display === '') {
                chatbotBox.style.display = 'flex';
                if (chatMessages.children.length === 0) {
                    addBotMessage("नमस्ते! मैं आपका AgriConnect AI सहायक हूँ। मैं आपकी किस प्रकार सहायता कर सकता हूँ?");
                }
            } else {
                chatbotBox.style.display = 'none';
            }
        };
    }
    if (closeChatbot) {
        closeChatbot.onclick = function () {
            console.log('Close clicked');
            chatbotBox.style.display = 'none';
        };
    }

    function getCsrfToken() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return value;
            }
        }
        return '';
    }

    async function handleSendMessage() {
        const message = userInput.value.trim();
        if (message) {
            addUserMessage(message);
            userInput.value = '';

            try {
                addTypingIndicator();

                const response = await fetch('/chatbot/response/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCsrfToken(),
                    },
                    body: JSON.stringify({ message: message })
                });

                removeTypingIndicator();

                const data = await response.json();

                if (data.status === 'success') {
                    addBotMessage(data.message || "उत्तर प्राप्त हुआ।");
                } else {
                    addBotMessage("मुझे खेद है, मैं आपका अनुरोध संसाधित नहीं कर सका। कृपया पुनः प्रयास करें।");
                }
            } catch (error) {
                console.error('Error:', error);
                removeTypingIndicator();
                addBotMessage("मुझे खेद है, मैं कनेक्ट करने में समस्या का सामना कर रहा हूँ। कृपया बाद में पुनः प्रयास करें।");
            }
        }
    }

    if (sendMessage && userInput) {
        sendMessage.onclick = handleSendMessage;
        userInput.onkeypress = function (e) {
            if (e.key === 'Enter') {
                handleSendMessage();
            }
        };
    }

    // Helper functions
    function addBotMessage(message) {
        const div = document.createElement('div');
        div.className = 'message bot-message';
        div.textContent = message;
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function addUserMessage(message) {
        const div = document.createElement('div');
        div.className = 'message user-message';
        div.textContent = message;
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function addTypingIndicator() {
        const div = document.createElement('div');
        div.className = 'message bot-message typing-indicator';
        div.innerHTML = '<span></span><span></span><span></span>';
        div.id = 'typingIndicator';
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function removeTypingIndicator() {
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
});
