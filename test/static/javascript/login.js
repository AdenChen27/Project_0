var login_container = document.getElementById("login-container"), 
    register_container = document.getElementById("register-container"), 
    login_nav_btn = document.getElementById("login-nav-btn"), 
    register_nav_btn = document.getElementById("register-nav-btn");

function to_login(){
    login_container.style.display = "block";
    if (!login_nav_btn.classList.contains("nav-active")) {
        login_nav_btn.classList.add("nav-active");
    }
    register_container.style.display = "none";
    if (register_nav_btn.classList.contains("nav-active")) {
        register_nav_btn.classList.remove("nav-active");
    }
    login_container.scrollIntoView();
}


function to_register(){
    login_container.style.display = "none";
    if (login_nav_btn.classList.contains("nav-active")) {
        login_nav_btn.classList.remove("nav-active");
    }
    register_container.style.display = "block";
    if (!register_nav_btn.classList.contains("nav-active")) {
        register_nav_btn.classList.add("nav-active");
    }
    register_container.scrollIntoView();
}

