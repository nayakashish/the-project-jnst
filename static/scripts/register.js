document.addEventListener('DOMContentLoaded', function() {
    // Your code here
    console.log('DOM fully loaded and parsed');
});

document.querySelector('.login-form').addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent the default form submission behavior

    // Get the username and password from the form
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Create a JSON object
    const userData = { username, password };

    try {
        // Send the JSON object to the back-end server
        const response = await fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData),
        });

        // Handle the response
        if (response.ok) {
            const result = await response.json();
            alert(`Registration successful: ${result.message}`);
            window.location.href = 'login.html'; // Redirect to the login page
        } else {
            const error = await response.json();
            alert(`Registration failed: ${error.message}`);
        }
    } catch (err) {
        console.error('Error occurred:', err);
        alert('An error occurred. Please try again later.');
    }
});
