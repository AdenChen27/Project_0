if (user.length == 0) {
    // not yet logged in
    document.getElementById("logged-in-info").style.display = "none";
    document.getElementById("log-in-link").style.display = "block";
} else {
    // logged in
    document.getElementById("logged-in-info").style.display = "block";
    document.getElementById("log-in-link").style.display = "none";
}

