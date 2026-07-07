async function loadTasks() {
    const res = await fetch("/api/tasks");
    const data = await res.json();

    const table = document.getElementById("taskTable");
    table.innerHTML = "";

    data.forEach(t => {
        table.innerHTML += `
        <tr>
            <td>${t.id}</td>
            <td>${t.title}</td>
            <td>${t.status}</td>
            <td>${t.priority}</td>
            <td>${t.assigned_to}</td>
        </tr>`;
    });
}

loadTasks();
