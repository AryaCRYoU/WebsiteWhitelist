document.getElementById('registrationForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
 
    const formData = new FormData();
    formData.append('username', username);

    fetch('main.py', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Registration successful.');
        } else {
            alert('Registration failed.');
        }
    })
    .catch(error => {
        console.error('Error:',error);
        alert('An error occurred while registering.');
    });
});