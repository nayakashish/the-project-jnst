document.addEventListener('DOMContentLoaded', function() {
    // Your code here
    // Check for success message in URL parameters and display an alert
    function getQueryParameter(name) { //for code reuse
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(name);
    }

    
    const alertMSG = getQueryParameter('alert_msg');
    if (alertMSG) {
        alert(alertMSG);
    }
    
    console.log('Register page loaded');
    
});


// document.querySelector('.login-form').addEventListener('submit', async (event) => {
//     event.preventDefault(); // Prevent the default form submission behavior

//     // Get the username and password from the form
//     const username = document.getElementById('username').value;
//     const password = document.getElementById('password').value;

//     // Create a JSON object
//     const userData = { username, password };

//     try {
//         // Send the JSON object to the back-end server
//         const response = await fetch('/register', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//             body: JSON.stringify(userData),
//         });

//         // Handle the response
//         if (response.ok) {
//             const result = await response.json();
//             alert(`Registration successful: ${result.message}`);
//             window.location.href = 'the-project-jnst/templates/index.html'; // Redirect to the login page
//         } else {
//             const error = await response.json();
//             alert(`Registration failed: ${error.message}`);
//         }
//     } catch (err) {
//         console.error('Error occurred:', err);
//         alert('An error occurred. Please try again later.');
//     }
// });
