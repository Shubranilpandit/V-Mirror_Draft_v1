async function signup() {
    const username = document.getElementById("username")?.value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const res = await fetch('/signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username,
            email,
            password
        })
    });

    const data = await res.json();

    if (data.message) {
        alert(data.message);
        window.location.href = '/login';
    } else {
        alert(data.error);
    }
}

async function login() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const res = await fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email,
            password
        })
    });

    const data = await res.json();

    if (data.message) {
        window.location.href = '/';
    } else {
        alert(data.error);
    }
}