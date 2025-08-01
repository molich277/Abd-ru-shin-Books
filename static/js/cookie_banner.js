// static/js/cookie_banner.js
document.addEventListener('DOMContentLoaded', function() {
    const cookieBanner = document.getElementById('cookie-banner');
    const acceptButton = document.getElementById('accept-cookies');

    // Check if cookie consent has been given
    if (!localStorage.getItem('cookie_consent_given')) {
        cookieBanner.style.display = 'flex'; // Show the banner
    }

    // Handle accept button click
    if (acceptButton) {
        acceptButton.addEventListener('click', function() {
            localStorage.setItem('cookie_consent_given', 'true');
            cookieBanner.style.display = 'none'; // Hide the banner
        });
    }
});
