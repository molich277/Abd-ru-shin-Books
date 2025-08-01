// /home/yuri/Websites/Abd-ru-shin-Books/static/js/cookie_banner.js

document.addEventListener('DOMContentLoaded', function() {
    const cookieBanner = document.getElementById('cookie-banner');
    const acceptButton = document.getElementById('accept-cookies');

    // Function to get a cookie by name
    function getCookie(name) {
        const nameEQ = name + "=";
        const ca = document.cookie.split(';');
        for (let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) === ' ') c = c.substring(1, c.length);
            if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
        }
        return null;
    }

    // Function to set a cookie
    function setCookie(name, value, days) {
        let expires = "";
        if (days) {
            const date = new Date();
            date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
            expires = "; expires=" + date.toUTCString();
        }
        document.cookie = name + "=" + (value || "") + expires + "; path=/; SameSite=Lax";
    }

    // Check if the user has already accepted cookies
    const cookieConsent = getCookie('cookie_consent');

    if (!cookieConsent) {
        // If not accepted, show the banner
        cookieBanner.style.display = 'block';
    }

    // Event listener for the accept button
    if (acceptButton) {
        acceptButton.addEventListener('click', function() {
            setCookie('cookie_consent', 'true', 365); // Set cookie for 1 year
            cookieBanner.style.display = 'none'; // Hide the banner
        });
    }
});
