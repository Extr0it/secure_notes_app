const registerBtn = document.getElementById("registerBtn");
const loginBtn = document.getElementById("loginBtn");

const notesSection = document.getElementById("notesSection");
const authSection = document.getElementById("authSection");


const createNoteBtn = document.getElementById("createNoteBtn");
const loadNotesBtn = document.getElementById("loadNotesBtn");
const notesContainer = document.getElementById("notesContainer");
const logoutBtn = document.getElementById("logoutBtn");

let token = "";
localStorage.setItem("token", token);



registerBtn.addEventListener("click", async () => {

    const username = document.getElementById("registerUsername").value;
    const password = document.getElementById("registerPassword").value;

    const response = await fetch("http://127.0.0.1:8000/register", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            username: username,
            password: password
        })

    });

    const data = await response.json();

    alert(data.msg);

});


loginBtn.addEventListener("click", async () => {

    const username = document.getElementById("loginUsername").value;
    const password = document.getElementById("loginPassword").value;

    const formData = new FormData();

    formData.append("username", username);
    formData.append("password", password);

    const response = await fetch("http://127.0.0.1:8000/login", {

        method: "POST",

        body: formData

    });

    const data = await response.json();

    token = data.access_token;

    if(token){

        authSection.classList.add("hidden");
        notesSection.classList.remove("hidden");

        alert("Login successful");

    } else {

        alert("Login failed");

    }

});


createNoteBtn.addEventListener("click", async () => {
    const title = document.getElementById("noteTitle").value;
    const content = document.getElementById("noteContent").value;

    const response = await fetch("http://127.0.0.1:8000/notes", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
            title: title,
            content: content
        })
    });

    const data = await response.json();

    alert("Note created");
    console.log(data);
});

loadNotesBtn.addEventListener("click", async () => {
    const response = await fetch("http://127.0.0.1:8000/notes", {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    const data = await response.json();

    notesContainer.innerHTML = "";

    data.forEach(note => {
        notesContainer.innerHTML += `
            <div class="note">
                <h3>${note.title}</h3>
                <p>${note.content}</p>
            </div>
        `;
    });
});


logoutBtn.addEventListener("click", () => {
    token = "";
    localStorage.removeItem("token");

    notesSection.classList.add("hidden");
    authSection.classList.remove("hidden");

    alert("Logged out");
});