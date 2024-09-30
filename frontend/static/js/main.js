// static/js/main.js
async function fetchUsersInit() {
    const response = await fetch(`${config.backendUrl}/usersInit`); // Use the URL from config.js
    const users = await response.json();
    const userList = document.getElementById('user-list');
    console.log(users);
    users.forEach(user => {
        const li = document.createElement('li');
        li.textContent = `${user.name} (${user.username}) - ${user.email}`;
        userList.appendChild(li);
    });
}

async function fetchUsers() {
    const response = await fetch(`${config.backendUrl}/users`); // Use the URL from config.js
    const users = await response.json();
    if (users.length === 0) {
        fetchUsersInit();    
    }

    const userList = document.getElementById('user-list');
    console.log(users);
    
    users.forEach(user => {
        const li = document.createElement('li');
        li.textContent = `${user.name} (${user.username}) - ${user.email}`;
        userList.appendChild(li);
    });
}

document.addEventListener('DOMContentLoaded', fetchUsers);

