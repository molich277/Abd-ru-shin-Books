window.onload = function() {
    if (!localStorage.getItem('cookiesAccepted')) {
        document.getElementById('cookie-popup').style.display = 'block';
    }
}
function acceptCookies() {
    localStorage.setItem('cookiesAccepted', true);
    document.getElementById('cookie-popup').style.display = 'none';
}
