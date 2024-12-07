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
    console.log('DOM fully loaded and parsed');
});