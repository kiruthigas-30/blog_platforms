// REGISTER VALIDATION
function validateRegister() {

    let username = document.getElementById("username").value;

    let email = document.getElementById("email").value;

    let password = document.getElementById("password").value;

    if(username == "" || email == "" || password == "") {

        alert("All fields are required");

        return false;
    }

    alert("Registration Successful");

    return true;
}

// LOGIN VALIDATION
function validateLogin() {

    let email = document.getElementById("email").value;

    let password = document.getElementById("password").value;

    if(email == "" || password == "") {

        alert("Enter Email and Password");

        return false;
    }

    return true;
}

// CREATE POST VALIDATION
function validatePost() {

    let title = document.getElementById("title").value;

    let content = document.getElementById("content").value;

    if(title == "" || content == "") {

        alert("Post fields cannot be empty");

        return false;
    }

    return true;
}

// COMMENT VALIDATION
function validateComment() {

    let comment = document.getElementById("comment").value;

    if(comment == "") {

        alert("Comment cannot be empty");

        return false;
    }

    return true;
}

// DELETE CONFIRMATION
function confirmDelete() {

    return confirm("Are you sure you want to delete this post?");
}