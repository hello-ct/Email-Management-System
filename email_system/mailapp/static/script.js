// Simple client-side validation (optional)
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('loginForm');

    form.addEventListener('submit', function (e) {
        const username = form.username.value.trim();
        const password = form.password.value.trim();

        if (username === '' || password === '') {
            e.preventDefault();
            alert('Please fill in both username and password.');
        }
    });
});