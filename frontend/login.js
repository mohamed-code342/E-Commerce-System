const loginForm = document.getElementById("login-form");

loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("http://127.0.0.1:8000/users/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        const data = await response.json();

        console.log(data);

        if (response.ok) {

            localStorage.setItem(
                "token",
                data.access_token
            );

            localStorage.setItem(
                "token_type",
                data.token_type
            );

            localStorage.setItem(
                "role",
                data.role
            );

            alert("Login successful!");

            // Redirect based on role
            if (data.role === "admin") {

                window.location.href =
                    "admin.html";

            } else {

                window.location.href =
                    "index.html";
            }

        } else {

            alert(
                data.detail || "Login failed"
            );
        }

    } catch (error) {

        console.error(error);

        alert("Server error");
    }
});