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


function set_register_error(msg) {
    document.getElementById("register-error-msg").innerHTML = msg;
}


function check_register_info(){
    set_register_error("");
    var name = document.getElementById("register-name").value;
    var user = document.getElementById("register-user").value;
    var pass = document.getElementById("register-password-1").value;
    var pass2 = document.getElementById("register-password-2").value;
    if (!name) {
        set_register_error("Name cannot be blank");
        return false;
    }
    if (!user) {
        set_register_error("Username cannot be blank");
        return false;
    }
    if (!pass) {
        set_register_error("Password cannot be blank");
        return false;
    }
    if (pass != pass2) {
        set_register_error("Password and confirm password does not match");
        return false;
    }
    var pass_input = document.getElementById("register-password-1");
    pass_input.value = md5(pass_input.value);
    return true;
}


function submit_signin_info(){
    var pass_input = document.getElementById("login-password");
    pass_input.value = md5(pass_input.value);
    return true;
}


if (init_page == "login") {
    to_login();
} else {
    to_register();
}

