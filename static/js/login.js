const form = document.getElementById('loginForm');
const result = document.getElementById('loginResult');
const username = form.elements['username'];
const password = form.elements['password'];

console.log("setup login form");

form.addEventListener('submit', (event) => {
    console.log("login attempted");
    if (username.value != 'benthecat') {
        event.preventDefault();
        result.innerHTML = 'Invalid username';
        return;
    }
    if (md5(password.value) != 'd88208c2bf53a7cf9f6c3a022614c95b') {
        event.preventDefault();
        result.innerHTML = 'Invalid password';
        return;
    }
});
