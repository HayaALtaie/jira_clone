// script.js

function toggleTheme() {
    const body = document.body;
    const currentTheme = body.classList.contains('bg-dark') ? 'dark' : 'light';

    if (currentTheme === 'light') {
        body.classList.add('bg-dark');
        document.getElementById('theme-toggle').textContent = '🌞'; // Change button to sun icon
    } else {
        body.classList.remove('bg-dark');
        document.getElementById('theme-toggle').textContent = '🌙'; // Change button to moon icon
    }
}
