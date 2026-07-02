let editingId = null;

async function loadEmployees() {
    let res = await fetch("/api/employees");
    let data = await res.json();

    let tbody = document.getElementById("empTable");
    tbody.innerHTML = "";

    data.forEach(e => {
        tbody.innerHTML += `
        <tr>
            <td>${e.id}</td>
            <td>${e.name}</td>
            <td>${e.email}</td>
            <td>${e.department}</td>
            <td>${e.status}</td>
            <td>
                <button onclick="editEmployee(${e.id}, '${e.name}', '${e.email}', '${e.department}', '${e.status}')">Edit</button>
                <button onclick="deleteEmp(${e.id})">Delete</button>
            </td>
        </tr>`;
    });
}

async function loadStats() {
    let res = await fetch("/api/employees/stats");
    let s = await res.json();

    document.getElementById("statsBox").innerHTML = `
        <b>Total:</b> ${s.total} |
        <b>Active:</b> ${s.active} |
        <b>Inactive:</b> ${s.inactive}
    `;
}

function showAddModal() {
    editingId = null;
    document.getElementById("modalTitle").innerText = "Add Employee";

    document.getElementById("name").value = "";
    document.getElementById("email").value = "";
    document.getElementById("dept").value = "";
    document.getElementById("status").value = "Active";

    document.getElementById("modal").style.display = "block";
}

function editEmployee(id, name, email, dept, status) {
    editingId = id;

    document.getElementById("modalTitle").innerText = "Edit Employee";

    document.getElementById("name").value = name;
    document.getElementById("email").value = email;
    document.getElementById("dept").value = dept;
    document.getElementById("status").value = status;

    document.getElementById("modal").style.display = "block";
}

async function saveEmployee() {
    let payload = {
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        department: document.getElementById("dept").value,
        status: document.getElementById("status").value
    };

    if (editingId) {
        await fetch("/api/employees/" + editingId, {
            method: "PUT",
            headers: {"Content-Type":"application/json"},
            body: JSON.stringify(payload)
        });
    } else {
        await fetch("/api/employees", {
            method: "POST",
            headers: {"Content-Type":"application/json"},
            body: JSON.stringify(payload)
        });
    }

    closeModal();
    loadEmployees();
    loadStats();
}

async function deleteEmp(id) {
    await fetch("/api/employees/" + id, { method: "DELETE" });
    loadEmployees();
    loadStats();
}

function closeModal() {
    document.getElementById("modal").style.display = "none";
}

loadEmployees();
loadStats();
